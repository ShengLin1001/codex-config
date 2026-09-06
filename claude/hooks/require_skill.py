#!/usr/bin/env python3
"""PreToolUse 门：做受管动作前，若对应 skill 未加载则拦一次。

对所有 skill 通用 —— 规则表在同目录 `gate.json`，加新 skill 只改那张表，不动本文件。
两类规则：`gates` 按**写入目标路径**判，`command_gates` 按 **shell 命令**判
（`git commit` 这种动作不写文件，路径那张表盖不住）。

设计取舍
--------
* **判"已加载"认 transcript 里真实的 `Skill` tool_use**，不 grep skill 名：
  启动时的 skill 清单本身就含所有 skill 名，grep 名字必然假阳性（审计报告踩过这个坑）。
* **每个 skill 每会话最多拦一次**（two-try）。模型不配合时死循环比漏调用更糟：拦一次
  给足信息，第二次无条件放行。marker 按 `session_id + skill` 存 —— 若按会话存一个，
  写 .py 拦掉的那一次会把后面 `git commit` 的额度也用光。
* **匹配写入目标 / 命令本身，不匹配 prompt 关键词**。社区实测提示词关键词型 hook 反而把
  激活率从 55% 拉到 41%；写入目标和命令是确定事实，不是猜意图。
* 规则表放 `gate.json` 而不是各 skill 的 frontmatter `metadata:`：SKILL.md 要同时装给
  Codex，而 OpenAI 官方 skill-creator 明确"只允许 name + description"。本 hook 只服务
  Claude Code，没必要为此赌 SKILL.md 的跨 agent 兼容性。

出参遵循 Claude Code PreToolUse 约定：exit 2 阻断，消息走 stderr。
"""

import fnmatch
import json
import os
import re
import sys
from pathlib import Path

# 拦截消息是这道门的全部价值，不能因为宿主没给 PYTHONIOENCODING 就被转义成 \uXXXX。
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PATH_GATE = Path(__file__).resolve().parent / "gate.json"

LWRITE_TOOL = ["Write", "Edit", "NotebookEdit"]
LSHELL_TOOL = ["Bash", "PowerShell"]

# shell 里"往文件写"的判据：重定向 / tee / sed -i 的**目标**必须是文件路径，
# 并捕获该路径交给同一张 glob 表判。
# 判据必须落在目标上：只匹配 `>` 会被 `grep ... 2>/dev/null` 这类只读命令骗到
# （命令里恰好带 .py 路径），写 harness 时就这么误判过一次。
RE_SHELL_TARGET = re.compile(
    r"""(?:>>?|\btee\b(?:\s+-a)?)\s*['"]?([^\s'"|;&<>]+)"""
    r"""|\bsed\s+-i\S*\s+[^|;&]*?['"]?([^\s'"|;&<>]+)\s*(?:$|[|;&])"""
)


def get_gate_table(path_gate, key):
    """读规则表里的一张（`gates` 或 `command_gates`）。
    表坏了就放行 —— 门坏掉不该把整个会话锁死。"""
    try:
        dict_raw = json.loads(path_gate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    dict_gate = dict_raw.get(key)
    return dict_gate if isinstance(dict_gate, dict) else {}


def get_write_target(data):
    """从 tool_input 里取出这次要写的目标路径列表。

    Write/Edit 直接给 file_path；shell 得从命令里扒重定向 / tee / sed -i 的目标。
    扒不到的写法（`python -c "open(...,'w')"`、`cp a.py b.py`、编辑器）本层就是盖不住 ——
    这是这道门的天花板，靠 description 那层兜。
    """
    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input") or {}

    if tool_name in LWRITE_TOOL:
        target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        return [target] if target else []

    if tool_name in LSHELL_TOOL:
        command = str(tool_input.get("command") or "")
        # findall 每条命中给一个分组元组，取非空的那个分组。
        return [group for ltuple in RE_SHELL_TARGET.findall(command)
                for group in ltuple if group]

    return []


def is_match(target, pattern):
    """glob 匹配：按模式形状决定跟"文件名"还是"整条路径"比。

    两个都踩过的坑，都是 `fnmatch` 不认 `**` 导致的：
    * `**/*.py` 被编成 `.*.*/.*\\.py`，硬要求路径里有 `/`，于是 `batch.py` 这种
      裸相对文件名一个都匹配不上 —— 而 agent 写的恰恰多是相对路径。
    * 反过来，`**/*fig*.py` 变成"路径里任意位置含 fig"，于是仓库名 `codex-config`
      里的 "config" 命中，整个仓库的 .py 全被判成绘图文件。

    所以：去掉 `**/` 前缀后不含 `/` 的，是**文件名模式**，只跟 basename 比；
    含 `/` 的才是路径模式，跟整条路径比。
    """
    tail = pattern[3:] if pattern.startswith("**/") else pattern
    if "/" not in tail:
        return fnmatch.fnmatch(target.rsplit("/", 1)[-1], tail)
    return fnmatch.fnmatch(target, pattern)


def get_required_skill(path_target, dict_gate):
    """返回该写入目标命中的 skill 名列表。"""
    # glob 用 posix 分隔符比较：Windows 上 tool_input 给的是反斜杠路径。
    target = str(path_target).replace("\\", "/")
    lskill = []
    for skill, lpattern in dict_gate.items():
        if any(is_match(target, pattern) for pattern in lpattern):
            lskill.append(skill)
    return lskill


def get_command_gated_skill(data, dict_cmd_gate):
    """shell 命令本身命中规则时要求的 skill。

    `git commit` 这类动作不产生文件写入，路径那张表看不见它，所以单独一张命令表。
    命令先做空白归一（`git   commit` 也要命中 `*git commit*`），再整条拿去 glob。
    """
    if data.get("tool_name") not in LSHELL_TOOL:
        return []
    command = " ".join(str((data.get("tool_input") or {}).get("command") or "").split())
    return [skill for skill, lpattern in dict_cmd_gate.items()
            if any(fnmatch.fnmatch(command, pattern) for pattern in lpattern)]


def get_loaded_skill(path_transcript, lcandidate):
    """从 transcript 里找已经真实调用过的 skill 名集合。"""
    if not path_transcript or not path_transcript.is_file():
        return set()
    text = path_transcript.read_text(encoding="utf-8", errors="replace")
    # 直接子串匹配 tool_use 的入参形状，比逐行 json.loads 快一个量级；
    # 门跑在每次写入前，不能慢。
    return {skill for skill in lcandidate
            if f'"skill":"{skill}"' in text or f'"skill": "{skill}"' in text}


### ================ main ================

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

lrequired = []
lhit = []          # 给人看的命中原因，形如 "写 batch.py" / "跑 git commit -m …"

dict_gate = get_gate_table(PATH_GATE, "gates")
for path_target in get_write_target(data):
    lskill = get_required_skill(path_target, dict_gate)
    if lskill:
        lhit.append(f"写 {path_target}")
        lrequired += [skill for skill in lskill if skill not in lrequired]

lcmd_skill = get_command_gated_skill(data, get_gate_table(PATH_GATE, "command_gates"))
if lcmd_skill:
    lhit.append(f"跑 {str((data.get('tool_input') or {}).get('command'))[:40]}")
    lrequired += [skill for skill in lcmd_skill if skill not in lrequired]

if not lrequired:
    sys.exit(0)

sloaded = get_loaded_skill(Path(data.get("transcript_path") or ""), lrequired)
lmissing = [skill for skill in lrequired if skill not in sloaded]
if not lmissing:
    sys.exit(0)

# 每个 skill 每会话拦一次。marker 落在系统临时目录，会话结束不用清理。
path_tmp = Path(os.environ.get("TEMP") or os.environ.get("TMPDIR") or "/tmp")
session = data.get("session_id", "unknown")
lblock = [skill for skill in lmissing
          if not (path_tmp / f"skillgate-{session}-{skill}").exists()]
if not lblock:
    sys.exit(0)
for skill in lblock:
    (path_tmp / f"skillgate-{session}-{skill}").write_text("", encoding="utf-8")

print(f"⚠️  {'、'.join(lhit)} 前必须先加载：{', '.join(lblock)}。"
      f"用 Skill 工具加载后重做这次操作。", file=sys.stderr)
sys.exit(2)
### to here
