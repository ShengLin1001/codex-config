#!/usr/bin/env python3
"""require_skill.py 的自检。跑法：codexpy test_require_skill.py"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PATH_HOOK = Path(__file__).resolve().parent / "require_skill.py"
PATH_TMP = Path(tempfile.mkdtemp(prefix="skillgate-test-"))


def run_hook(tool_name, path_target, session_id, transcript="", command=""):
    """跑一次 hook，返回 (returncode, stderr)。TEMP 指到临时目录，别污染真 marker。"""
    path_transcript = ""
    if transcript:
        path_transcript = PATH_TMP / f"{session_id}.jsonl"
        path_transcript.write_text(transcript, encoding="utf-8")
    tool_input = {"command": command} if command else {"file_path": str(path_target)}
    payload = json.dumps({
        "tool_name": tool_name,
        "tool_input": tool_input,
        "session_id": session_id,
        "transcript_path": str(path_transcript),
    })
    proc = subprocess.run([sys.executable, str(PATH_HOOK)], input=payload,
                          capture_output=True, text=True, encoding="utf-8",
                          env={"TEMP": str(PATH_TMP), "SystemRoot": "C:\\Windows"})
    return proc.returncode, (proc.stderr or "").strip()


### ================ main ================

# 1. 受管后缀 + 未加载 + 无 marker → 拦
code, err = run_hook("Write", r"C:\x\batch_stat.py", "s1")
assert code == 2, (code, err)
assert "p-code-style" in err, err
print(f"✅ 首次写 .py 被拦：{err[:60]}")

# 2. 同会话再写一次 → 放行（two-try，不死循环）
code, err = run_hook("Write", r"C:\x\other.py", "s1")
assert code == 0, (code, err)
print("✅ 同会话第二次放行（marker 生效）")

# 3. 不在规则表里的文件 → 放行
code, err = run_hook("Write", r"C:\x\notes.txt", "s2")
assert code == 0, (code, err)
print("✅ .txt 不受管，放行")

# 4. transcript 里已有真实 Skill 调用 → 放行
code, err = run_hook("Write", r"C:\x\a.py", "s3",
                     transcript='{"message":{"content":[{"type":"tool_use",'
                                '"name":"Skill","input":{"skill":"p-code-style"}}]}}\n')
assert code == 0, (code, err)
print("✅ skill 已加载，放行")

# 5. 只出现 skill 名（启动清单那种）不算调用 → 仍然拦。审计报告踩过的假阳性。
code, err = run_hook("Write", r"C:\x\b.py", "s4",
                     transcript='{"skills":["p-code-style","p-plot-figure"]}\n')
assert code == 2, (code, err)
print("✅ 光有 skill 名不算调用，仍然拦")

# 6. SKILL.md 命中 p-agent-doc-writing，且能一次报多个
code, err = run_hook("Write", r"C:\x\skills\foo\SKILL.md", "s5")
assert code == 2, (code, err)
assert "p-agent-doc-writing" in err, err
print("✅ SKILL.md 命中 p-agent-doc-writing")

# 7. heredoc 写 .py → 拦
code, err = run_hook("Bash", "", "s6", command="cat > batch.py <<'EOF'\nprint(1)\nEOF")
assert code == 2, (code, err)
assert "batch.py" in err, err
print("✅ heredoc 重定向写 .py 被拦")

# 8. sed -i 改 .py → 拦
code, err = run_hook("Bash", "", "s7", command="sed -i 's/a/b/' scripts/run.py")
assert code == 2, (code, err)
assert "run.py" in err, err
print("✅ sed -i 改 .py 被拦")

# 9. tee -a 追加 .sh → 拦
code, err = run_hook("Bash", "", "s8", command="echo hi | tee -a collect.sh")
assert code == 2, (code, err)
print("✅ tee -a 写 .sh 被拦")

# 10. 只读命令带 .py 路径 + 2>/dev/null → 放行。这是写 harness 时踩过的假阳性。
code, err = run_hook("Bash", "", "s9",
                     command='grep -n "def" scripts/run.py 2>/dev/null | head -5')
assert code == 0, (code, err)
print("✅ 只读 grep（含 2>/dev/null 与 .py 路径）不误拦")

# 11. 重定向到非受管文件 → 放行
code, err = run_hook("Bash", "", "s10", command="ls -la > out.txt")
assert code == 0, (code, err)
print("✅ 重定向到 .txt 不受管，放行")

# 12. 扒不到目标的写法 → 放行（已知天花板，靠 description 那层兜）
code, err = run_hook("Bash", "", "s11",
                     command="""python -c "open('gen.py','w').write('x')" """)
assert code == 0, (code, err)
print("✅ python -c 写文件扒不到（已知天花板，见 get_write_target 注释）")

# 13. 目录名含 "fig"（codex-con*fig*）不该把普通 .py 判成绘图文件。
#     实测踩过：`**/*fig*.py` 被 fnmatch 当成"路径里任意位置含 fig"，整个仓库沦陷。
code, err = run_hook("Write", "F:/x/codex-config/scratchpad/probe.py", "s12")
assert code == 2, (code, err)
assert "p-code-style" in err and "p-plot-figure" not in err, err
print("✅ codex-config 里的 probe.py 只要 p-code-style，不误判为绘图")

# 14. 真正的绘图文件名才要 p-plot-figure
code, err = run_hook("Write", "F:/x/plot_band.py", "s13")
assert code == 2 and "p-plot-figure" in err, (code, err)
print("✅ plot_band.py 命中 p-plot-figure")

# 15. git commit 未加载 p-git-commit → 拦（命令表，不产生文件写入）
code, err = run_hook("Bash", "", "s14", command='git add -A && git commit -m "feat: x"')
assert code == 2 and "p-git-commit" in err, (code, err)
print("✅ git commit 未加载 p-git-commit 被拦")

# 16. 已加载 p-git-commit → 放行
code, err = run_hook("Bash", "", "s15", command="git commit -m 'x'",
                     transcript='{"name":"Skill","input":{"skill":"p-git-commit"}}\n')
assert code == 0, (code, err)
print("✅ p-git-commit 已加载，git commit 放行")

# 17. 只是 git status / git log 不拦
code, err = run_hook("Bash", "", "s16", command="git log --oneline -5")
assert code == 0, (code, err)
print("✅ git log 不误拦")

# 18. marker 按 skill 分开：写 .py 拦掉后，同会话 git commit 仍要拦。
#     若 marker 按会话存一个，这里就会被前一次拦截的额度吃掉。
code, err = run_hook("Write", r"C:\x\a.py", "s17")
assert code == 2 and "p-code-style" in err, (code, err)
code, err = run_hook("Bash", "", "s17", command="git commit -m 'x'")
assert code == 2 and "p-git-commit" in err, (code, err)
print("✅ marker 按 skill 分开，两道门互不吃额度")

print("🎉 18/18 通过")
### to here
