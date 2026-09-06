#!/usr/bin/env python3
"""p-code-style 隐式触发率测试。

对一组固定提示词各起一个 `claude -p` 新会话，再回读该会话的 transcript，
按"首次真实 Skill 调用" vs "首次代码写入"的先后给出 提前 / 过晚 / 未调用。

判据刻意跟审计报告 20260901 一致：只认 transcript 里真实的 tool_use
（`Skill(skill="p-code-style")`），不认启动时 skill 清单里的 description ——
grep 字符串会把清单和讨论文本误算成调用。

Functions:
    fail / warn                     -- 统一错误出口与告警
    check_positive_int              -- 结构性前提校验
    check_prompts_file              -- 解析提示词表并校验非空
    get_transcript_path             -- 由 session_id 定位 transcript jsonl
    generate_seed_script            -- 造出 edit_* case 需要的待改文件
    parse_transcript                -- 从 transcript 提取两个关键事件下标
    run_one_case                    -- 跑单个 case 并分类
    main                            -- 编排
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

### ================ 常量与旋钮 ================

# 认定为"代码写入"的文件后缀。审计口径：md / txt 写入不算。
LCODE_SUFFIX = [".py", ".sh", ".bash", ".ps1", ".slurm", ".sbatch"]

# 结构化写入工具。Bash 单独处理：bypassPermissions 下 agent 常用
# heredoc / sed -i 直接写文件，只匹配 Write|Edit 会漏掉这一大类。
LWRITE_TOOL = ["Write", "Edit", "NotebookEdit"]

# Bash 里"往代码文件写"的判据：重定向 / tee / sed -i 的**目标**必须是代码文件。
# 只匹配 `>` 会被 `grep ... 2>/dev/null` 这类只读命令骗到（命令里恰好带 .py 路径），
# 自检时就是这么误判成 LATE 的 —— 判据必须落在目标文件上。
_SUFFIX_ALT = "|".join(suffix.lstrip(".") for suffix in LCODE_SUFFIX)
RE_BASH_WRITE = re.compile(
    r"(?:>>?|\btee\b(?:\s+-a)?)\s*['\"]?[^\s'\"|;&]*\.(?:" + _SUFFIX_ALT + r")\b"
    r"|\bsed\s+-i\b[^|;&]*\.(?:" + _SUFFIX_ALT + r")\b"
)

DICT_STATUS = {
    "EARLY": "✅ 提前调用",
    "LATE": "⚠️  调用过晚",
    "NEVER": "❌ 未调用",
    "NO_CODE": "➖ 没写代码（样本无效）",
    "ERROR": "💥 会话失败",
}

DEFAULT_TIMEOUT = 600


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def warn(msg):
    print(f"⚠️  {msg}")


### ================ check ================

def check_positive_int(value, name):
    """结构性前提：正整数。返回强转后的值，调用处必须接住。"""
    try:
        value = int(value)
    except (TypeError, ValueError):
        fail(f"{name} 必须是整数，得到 {value!r}")
    if value <= 0:
        fail(f"{name} 必须为正，得到 {value}")
    return value


def check_prompts_file(path_prompts):
    """解析 `<case_name>|<prompt>` 表，返回 [(case_name, prompt), ...]。"""
    path_prompts = Path(path_prompts).resolve()
    if not path_prompts.is_file():
        fail(f"提示词文件不存在：{path_prompts}")

    lcase = []
    for lineno, line in enumerate(path_prompts.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            fail(f"{path_prompts}:{lineno} 缺少 `|` 分隔符：{line}")
        case_name, prompt = line.split("|", 1)
        lcase.append((case_name.strip(), prompt.strip()))

    if not lcase:
        fail(f"{path_prompts} 里没有有效 case")
    return lcase


def check_claude_cli(claude_bin):
    """确认 CLI 可执行；版本要一起打出来，不同版本 skill 路由行为会变。"""
    try:
        proc = subprocess.run([claude_bin, "--version"], capture_output=True,
                              text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        fail(f"跑不起来 {claude_bin}：{exc}")
    if proc.returncode != 0:
        fail(f"{claude_bin} --version 退出码 {proc.returncode}")
    return proc.stdout.strip()


### ================ prepare ================

def get_alias(name):
    """项目级副本得换个名字：同名时用户级会盖掉项目级（实测），而 skillOverrides
    按名字关，会把两份一起关掉。所以 `p-xxx` → `pj-xxx`，再单独关掉用户级那份。"""
    return "pj-" + name[2:] if name.startswith("p-") else name + "-t"


def generate_project_skill(path_case, path_src, alias, hide_name):
    """把仓库源码装成该 case 的项目级 skill，并关掉同域的用户级副本。

    这样测的是仓库里的源文件，不用先重装、也绕开了源码/安装副本漂移。
    """
    path_dst = path_case / ".claude" / "skills" / alias
    path_dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(path_src, path_dst, dirs_exist_ok=True)

    # 改名：frontmatter 的 name 要跟目录一致，否则清单里显示的名字对不上。
    path_skill = path_dst / "SKILL.md"
    text = path_skill.read_text(encoding="utf-8")
    text = re.sub(r"^name:.*$", f"name: {alias}", text, count=1, flags=re.MULTILINE)
    path_skill.write_text(text, encoding="utf-8")

    # 关掉用户级那份，否则两份同域 skill 抢路由，测出来的数字没意义。
    path_settings = path_case / ".claude" / "settings.json"
    path_settings.write_text(
        json.dumps({"skillOverrides": {hide_name: "off"}}, indent=2), encoding="utf-8")


def generate_seed_script(path_case):
    """edit_* / small_fix case 需要一个已存在的待改脚本，否则 agent 会先建新文件。"""
    seed = '''#!/usr/bin/env python3
"""把一个 .dat 转成 .csv。"""

import sys


def convert(src):
    out = "converted.csv"
    with open(src) as f, open(out, "w") as g:
        for line in f:
            g.write(",".join(line.split()) + "\\n")
    print("wrote", out)


if __name__ == "__main__":
    convert(sys.argv[1])
'''
    (path_case / "seed_convert.py").write_text(seed, encoding="utf-8")


### ================ 事件提取 ================

def get_transcript_path(session_id, path_projects):
    """session_id → transcript jsonl。

    直接 glob，不去复刻 Claude Code 把 cwd 转成目录名的那套 sanitize 规则 ——
    规则变了 glob 照样能命中。
    """
    lhit = sorted(Path(path_projects).glob(f"**/{session_id}.jsonl"))
    if not lhit:
        return None
    return lhit[-1]


def get_tool_use_blocks(entry):
    """从一条 transcript 记录里取出 tool_use block；不是 assistant 消息就返回空。"""
    content = (entry.get("message") or {}).get("content")
    if not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict) and b.get("type") == "tool_use"]


def is_code_write(block):
    """这个 tool_use 是否算"往代码文件写入"。"""
    name = block.get("name", "")
    tool_input = block.get("input") or {}

    if name in LWRITE_TOOL:
        path_target = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
        return any(path_target.endswith(suffix) for suffix in LCODE_SUFFIX)

    if name in ("Bash", "PowerShell"):
        return bool(RE_BASH_WRITE.search(str(tool_input.get("command") or "")))

    return False


def parse_transcript(path_transcript, skill_name):
    """返回 (idx_skill, idx_write)，下标是 tool_use 的全局出现序号，None 表示没出现。"""
    idx_skill = None
    idx_write = None
    idx = 0

    for line in path_transcript.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue  # transcript 尾部可能是半行，跳过而不是炸掉整次统计

        for block in get_tool_use_blocks(entry):
            idx += 1
            if block.get("name") == "Skill" and (block.get("input") or {}).get("skill") == skill_name:
                if idx_skill is None:
                    idx_skill = idx
            elif is_code_write(block):
                if idx_write is None:
                    idx_write = idx

    return idx_skill, idx_write


def get_status(idx_skill, idx_write):
    if idx_write is None:
        # 没写代码就没什么可判的；skill 加载了也不能算命中。
        return "NO_CODE"
    if idx_skill is None:
        return "NEVER"
    return "EARLY" if idx_skill < idx_write else "LATE"


### ================ main ================

def run_one_case(case_name, prompt, path_workdir, args):
    """跑一个 case：起会话 → 定位 transcript → 分类。返回结果 dict。"""
    path_case = (path_workdir / case_name).resolve()
    path_case.mkdir(parents=True, exist_ok=True)
    generate_seed_script(path_case)
    if args.path_skill_src:
        generate_project_skill(path_case, args.path_skill_src, args.alias, args.skill)

    lcmd = [args.claude_bin, "-p", prompt,
            "--output-format", "json",
            "--permission-mode", args.permission_mode]
    if args.model:
        lcmd += ["--model", args.model]

    print(f"  ▶️  {case_name}")
    try:
        # cwd=path_case：每个 case 独立目录，写入不互相污染，
        # 也让 transcript 落到各自的 projects 子目录。
        proc = subprocess.run(lcmd, cwd=str(path_case), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=args.timeout)
    except subprocess.TimeoutExpired:
        warn(f"{case_name} 超过 {args.timeout}s，判 ERROR")
        return {"case": case_name, "status": "ERROR", "note": "timeout"}

    if proc.returncode != 0:
        warn(f"{case_name} 退出码 {proc.returncode}：{(proc.stderr or '').strip()[:200]}")
        return {"case": case_name, "status": "ERROR", "note": f"exit {proc.returncode}"}

    try:
        session_id = json.loads(proc.stdout).get("session_id")
    except (json.JSONDecodeError, AttributeError):
        warn(f"{case_name} 解析不出 session_id，判 ERROR")
        return {"case": case_name, "status": "ERROR", "note": "bad json"}

    path_transcript = get_transcript_path(session_id, args.path_projects)
    if path_transcript is None:
        warn(f"{case_name} 找不到 transcript：{session_id}")
        return {"case": case_name, "status": "ERROR", "note": "no transcript"}

    idx_skill, idx_write = parse_transcript(path_transcript, args.alias or args.skill)
    status = get_status(idx_skill, idx_write)
    print(f"     {DICT_STATUS[status]}   skill@{idx_skill} write@{idx_write}")
    return {"case": case_name, "status": status, "session": session_id,
            "idx_skill": idx_skill, "idx_write": idx_write,
            "transcript": str(path_transcript)}


def build_parser():
    parser = argparse.ArgumentParser(
        description="测 p-code-style 在首次写代码前是否被隐式调用")
    parser.add_argument("-skill", default="p-code-style", help="待测 skill 名")
    parser.add_argument("-prompts", default=str(Path(__file__).resolve().parent / "prompts.txt"),
                        help="提示词表，格式 <case_name>|<prompt>")
    parser.add_argument("-workdir", default="", help="工作目录，默认 ./_runs/<tag>")
    parser.add_argument("-tag", default="run", help="本轮标签，用于 A/B 对比不同 description")
    parser.add_argument("-repeat", default=1, help="每个 case 重复次数")
    parser.add_argument("-model", default="", help="传给 claude --model，空则用默认")
    parser.add_argument("-timeout", default=DEFAULT_TIMEOUT, help="单个 case 超时秒数")
    parser.add_argument("-claude_bin", default="claude", help="claude CLI 路径")
    parser.add_argument("-permission_mode", default="bypassPermissions",
                        help="传给 claude --permission-mode；默认 bypassPermissions，"
                             "否则写文件被拦、样本全变 NO_CODE")
    parser.add_argument("-path_projects", default=str(Path.home() / ".claude" / "projects"),
                        help="transcript 根目录")
    parser.add_argument("-skill_src", default="",
                        help="仓库里 skill 源目录；给了就装成项目级副本来测（绕开安装漂移），"
                             "不给则测已安装的用户级副本")
    parser.add_argument("-alias", default="",
                        help="项目级副本的名字，默认 p-xxx → pj-xxx")
    parser.add_argument("-check_parse", default="",
                        help="自检：只对给定 transcript jsonl 跑一遍事件提取并打印，不起会话")
    return parser


args = build_parser().parse_args()

### ================ 自检出口（不起会话，先确认事件提取没写错） ================
if args.check_parse:
    path_transcript = Path(args.check_parse).resolve()
    if not path_transcript.is_file():
        fail(f"transcript 不存在：{path_transcript}")
    idx_skill, idx_write = parse_transcript(path_transcript, args.skill)
    print(f"📍 {path_transcript}")
    print(f"   skill@{idx_skill}  write@{idx_write}  → {DICT_STATUS[get_status(idx_skill, idx_write)]}")
    raise SystemExit(0)
### to here

### ================ check ================
args.repeat = check_positive_int(args.repeat, "-repeat")
args.timeout = check_positive_int(args.timeout, "-timeout")
lcase = check_prompts_file(args.prompts)
version = check_claude_cli(args.claude_bin)

path_projects = Path(args.path_projects).resolve()
if not path_projects.is_dir():
    fail(f"transcript 根目录不存在：{path_projects}")
args.path_projects = path_projects

path_workdir = Path(args.workdir).resolve() if args.workdir else \
    (Path(__file__).resolve().parent / "_runs" / args.tag)

args.path_skill_src = None
if args.skill_src:
    args.path_skill_src = Path(args.skill_src).resolve()
    if not (args.path_skill_src / "SKILL.md").is_file():
        fail(f"skill 源目录里没有 SKILL.md：{args.path_skill_src}")
args.alias = args.alias or (get_alias(args.skill) if args.path_skill_src else "")
### to here

### ================ prepare ================
path_workdir.mkdir(parents=True, exist_ok=True)

path_installed = args.path_skill_src / "SKILL.md" if args.path_skill_src else     Path.home() / ".claude" / "skills" / args.skill / "SKILL.md"
description = "（找不到 SKILL.md）"
if path_installed.is_file():
    for line in path_installed.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("description"):
            description = line
            break

print("================ 📊 p-code-style 触发率测试")
print(f"📍 claude        : {version}")
print(f"📁 workdir       : {path_workdir}")
print(f"📁 transcripts   : {args.path_projects}")
print(f"🏷️  tag           : {args.tag}")
print(f"🔁 repeat        : {args.repeat}")
mode = f"项目级副本 {args.alias} ← {args.path_skill_src}" if args.path_skill_src     else f"已安装的用户级 {args.skill}"
print(f"🧩 被测       : {mode}")
print(f"📝 description : {description[:160]}")
print(f"▶️  {len(lcase)} 个 case × {args.repeat} 轮 = {len(lcase) * args.repeat} 个会话")
### to here

### ================ main ================
lresult = []
for round_idx in range(1, args.repeat + 1):
    print(f"================ 🔁 round {round_idx}/{args.repeat}")
    for case_name, prompt in lcase:
        case_tag = case_name if args.repeat == 1 else f"{case_name}-r{round_idx}"
        lresult.append(run_one_case(case_tag, prompt, path_workdir, args))

dict_count = {status: 0 for status in DICT_STATUS}
for result in lresult:
    dict_count[result["status"]] += 1

print("================ 📊 summary")
for status, label in DICT_STATUS.items():
    print(f"  {label:<22} {dict_count[status]}")

n_valid = dict_count["EARLY"] + dict_count["LATE"] + dict_count["NEVER"]
if n_valid:
    print(f"  提前调用率            {dict_count['EARLY']}/{n_valid} = "
          f"{dict_count['EARLY'] / n_valid:.0%}")

lbad = [r for r in lresult if r["status"] in ("LATE", "NEVER")]
if lbad:
    print("================ ❌ 未达标 case")
    for result in lbad:
        print(f"  {result['status']:<6} {result['case']:<22} {result.get('transcript', '')}")

path_report = path_workdir / "result.json"
path_report.write_text(json.dumps(lresult, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"🎉 明细写入 {path_report}")

raise SystemExit(1 if lbad else 0)
### to here


# ================ test_args（手动切换场景） ================
# 全量跑一轮：
#   codexpy run_skill_trigger_test.py
# 只跑一个 case，重复 5 次看抖动：
#   codexpy run_skill_trigger_test.py -prompts one.txt -repeat 5 -tag jitter
# A/B 两种 description：先装长版跑 -tag long，再装短版跑 -tag short，比 result.json
#   codexpy run_skill_trigger_test.py -tag long_desc
#   codexpy run_skill_trigger_test.py -tag short_desc
