#!/usr/bin/env python3
"""把 Claude Code 侧的 hook 装好：拷 hook 文件 + 合并 settings.json。

被 `scripts/pei_ai_univ_reinstall -hook` 调用，也可以单独跑。

两件事都从仓库数据**推导**，不另维护一份清单：
1. `PreToolUse` 注册 → 指向刚拷过去的 `require_skill.py`。
2. `skillOverrides` → 凡 `agents/openai.yaml` 里 `allow_implicit_invocation: false`
   的 skill，在 Claude Code 侧设成 `user-invocable-only`。Codex 用 openai.yaml 那个开关，
   Claude Code 没有对应的 frontmatter 可用（`disable-model-invocation` 会往
   SKILL.md 里加第三个字段，破坏"只含 name+description"的跨 agent 可移植性），
   所以在 settings 层翻译一次，单一来源仍是 openai.yaml。

解释器写死成跑本脚本的这个 python（`sys.executable`）：安装是每台机器各跑一次，
把当机可用的解释器固化下来最稳，省得依赖 PATH 上有没有 `python3`（zcm6 上可能要
先 module load）。

Functions:
    fail / warn                 -- 统一错误出口与告警
    check_repo_layout           -- 校验仓库里该有的文件都在
    get_explicit_only_skill     -- 扫 openai.yaml 找出仅显式调用的 skill
    generate_hook_entry         -- 构造 PreToolUse 注册项
    merge_settings              -- 幂等合并进 settings.json
    main                        -- 编排
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

### ================ 常量 ================

LHOOK_FILE = ["require_skill.py", "gate.json"]

# 这道门要盯的工具。shell 工具也在里面：heredoc / sed -i / tee 改代码文件，
# 以及 `git commit` 这种命令门，都只有从这里看得见。
# Windows 上主 shell 是 PowerShell，漏了它等于在本机把 shell 那半边门整个关掉。
MATCHER = "Write|Edit|NotebookEdit|Bash|PowerShell"

# 认注册项的标记：命令串里出现这个文件名就算是我们装的那条，重装时替换而不是追加。
MARK_COMMAND = "require_skill.py"

RE_IMPLICIT_FALSE = re.compile(r"^\s*allow_implicit_invocation:\s*false\s*$", re.MULTILINE)


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def warn(msg):
    print(f"⚠️  {msg}")


### ================ check ================

def check_repo_layout(path_repo_root):
    """校验结构性前提：hook 源文件和 skills-using 都在。返回 hook 源目录。"""
    path_repo_root = Path(path_repo_root).resolve()
    path_src = path_repo_root / "claude" / "hooks"
    for name in LHOOK_FILE:
        if not (path_src / name).is_file():
            fail(f"缺 hook 源文件：{path_src / name}")
    if not (path_repo_root / "skills-using").is_dir():
        fail(f"找不到 {path_repo_root / 'skills-using'}")
    return path_src


### ================ 推导 ================

def get_explicit_only_skill(path_repo_root):
    """扫所有 agents/openai.yaml，返回声明了仅显式调用的 skill 名列表。

    只用正则不用 yaml：zcm6 上不保证有 pyyaml，这一行的格式又固定，没必要引依赖。
    """
    lskill = []
    for path_yaml in sorted(Path(path_repo_root).glob("skills-using/**/agents/openai.yaml")):
        if RE_IMPLICIT_FALSE.search(path_yaml.read_text(encoding="utf-8", errors="replace")):
            # <skill>/agents/openai.yaml → skill 目录名
            lskill.append(path_yaml.parent.parent.name)
    return sorted(set(lskill))


def generate_hook_entry(path_hook):
    """构造 PreToolUse 注册项。路径带引号，兼容含空格的家目录。"""
    command = f'"{sys.executable}" "{path_hook}"'
    return {"matcher": MATCHER,
            "hooks": [{"type": "command", "command": command, "timeout": 10}]}


### ================ 合并 ================

def merge_settings(path_settings, entry, lexplicit, uninstall=False):
    """幂等合并进 settings.json；返回 (改了什么, 新内容)。

    只动我们负责的两个键，其他配置一律原样保留 —— 这文件里还有用户的 env、
    statusLine、plugin 等等，覆盖写会把它们抹掉。
    """
    dict_cfg = {}
    if path_settings.is_file():
        try:
            dict_cfg = json.loads(path_settings.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path_settings} 不是合法 JSON（{exc}）。先手工修好，别让脚本覆盖掉现有配置。")

    lchange = []

    ### PreToolUse 注册
    dict_hooks = dict_cfg.setdefault("hooks", {})
    lpre = dict_hooks.setdefault("PreToolUse", [])
    # 找出我们之前装的那条（命令里带 MARK_COMMAND），有就换掉/删掉，没有才追加。
    idx_own = next((i for i, e in enumerate(lpre)
                    if any(MARK_COMMAND in h.get("command", "")
                           for h in e.get("hooks", []))), None)
    if uninstall:
        if idx_own is not None:
            lpre.pop(idx_own)
            lchange.append("移除 PreToolUse 注册")
    elif idx_own is None:
        lpre.append(entry)
        lchange.append("新增 PreToolUse 注册")
    elif lpre[idx_own] != entry:
        lpre[idx_own] = entry
        lchange.append("更新 PreToolUse 注册")

    # 键空了就删掉，别在配置里留 "PreToolUse": [] 这种噪声。
    if not lpre:
        dict_hooks.pop("PreToolUse")
    if not dict_hooks:
        dict_cfg.pop("hooks")

    ### skillOverrides：把 Codex 的 allow_implicit_invocation:false 翻译过来
    dict_over = dict_cfg.get("skillOverrides", {})
    for skill in lexplicit:
        want = None if uninstall else "user-invocable-only"
        if uninstall:
            if dict_over.get(skill) == "user-invocable-only":
                dict_over.pop(skill)
                lchange.append(f"移除 skillOverrides {skill}")
        elif dict_over.get(skill) != want:
            dict_over[skill] = want
            lchange.append(f"设 skillOverrides {skill}=user-invocable-only")
    if dict_over:
        dict_cfg["skillOverrides"] = dict_over
    elif "skillOverrides" in dict_cfg:
        dict_cfg.pop("skillOverrides")

    return lchange, dict_cfg


def build_parser():
    parser = argparse.ArgumentParser(description="装 Claude Code 侧的 skill 门 hook")
    parser.add_argument("-global", dest="want_global", action="store_true",
                        help="装成用户级 ~/.claude；不给则装进当前目录的 ./.claude")
    parser.add_argument("-repo_root", default=str(Path(__file__).resolve().parents[2]),
                        help="仓库根，默认按本脚本位置推")
    parser.add_argument("-config_dir", default="", help="直接指定 .claude 目录，覆盖 -global")
    parser.add_argument("-uninstall", action="store_true", help="只反注册，不删文件")
    parser.add_argument("-dry_run", action="store_true", help="只打印将要做的改动")
    return parser


args = build_parser().parse_args()

### ================ check ================
path_repo_root = Path(args.repo_root).resolve()
path_src = check_repo_layout(path_repo_root)

if args.config_dir:
    path_config = Path(args.config_dir).resolve()
elif args.want_global:
    path_config = Path.home() / ".claude"
else:
    path_config = Path.cwd() / ".claude"
### to here

### ================ prepare ================
path_hook_dir = path_config / "hooks"
path_settings = path_config / "settings.json"
lexplicit = get_explicit_only_skill(path_repo_root)

print("================ 📊 装 Claude Code skill 门")
print(f"📍 解释器      : {sys.executable}")
print(f"📁 仓库根      : {path_repo_root}")
print(f"📁 配置目录    : {path_config}" + ("（用户级）" if args.want_global else "（项目级）"))
print(f"🔒 仅显式调用  : {', '.join(lexplicit) or '（无）'}")
### to here

### ================ main ================
if args.dry_run:
    print("▶️  [dry_run] 不实际改动")

if not args.uninstall and not args.dry_run:
    path_hook_dir.mkdir(parents=True, exist_ok=True)
    for name in LHOOK_FILE:
        shutil.copy2(path_src / name, path_hook_dir / name)
        print(f"✅ 拷入 {path_hook_dir / name}")
elif not args.uninstall:
    for name in LHOOK_FILE:
        print(f"  [dry_run] 拷 {path_src / name} → {path_hook_dir / name}")

entry = generate_hook_entry(path_hook_dir / "require_skill.py")
lchange, dict_cfg = merge_settings(path_settings, entry, lexplicit, uninstall=args.uninstall)

if not lchange:
    print("✅ settings.json 已是目标状态，无需改动")
elif args.dry_run:
    for change in lchange:
        print(f"  [dry_run] {change}")
else:
    path_settings.parent.mkdir(parents=True, exist_ok=True)
    path_settings.write_text(json.dumps(dict_cfg, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    for change in lchange:
        print(f"✅ {change}")

print(f"📊 settings.json: {path_settings}")
# 实测：已开着的会话也会重新读 settings.json，装完当场就生效，不必重开。
print("🎉 完成。settings.json 会被重新读取，当前会话即生效；没生效就重开一个。")
### to here
