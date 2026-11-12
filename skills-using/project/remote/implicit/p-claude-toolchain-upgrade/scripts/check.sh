#!/usr/bin/env bash
# 只读检查 Claude Code 工具链：Windows 本机 + zcm6 的已装版本、上游最新版、配置漂移。
# 不安装、不改任何文件（git fetch 只更新远程跟踪分支）。在 Windows git-bash 跑：
#   bash check.sh              # 两端都查
#   bash check.sh -skip_zcm6   # 反向隧道不在时只查本机

CODEX_CONFIG=/f/BaiduSyncdisk/version20240608/main_code_space/codex-config
CLAUDE_SESSIONS_SRC=/f/BaiduSyncdisk/version20240608/main_code_space/other/claude-sessions
WINDOWS_MCP_PY=D:/software/Windows-MCP/.venv/Scripts/python
PQ_NOISE='post-quantum\|store now\|openssh.com/pq'   # 每次 ssh 都在 stderr 打两遍，无害

section() { echo; echo "================ $1"; }

# claude plugin list 每个插件占 3–4 行，压成一行：名称 版本 状态
summarize_plugins() { awk '/❯/{n=$2} /Version:/{v=$2} /Status:/{print "  " n " " v " " $3}'; }

check_windows() {
  section "🪟 Windows 已装"
  echo "cli: $(claude --version)"
  echo "vscode-ext: $(code --list-extensions --show-versions 2>/dev/null | grep anthropic.claude-code)"
  echo "plugins:"; claude plugin list 2>&1 | summarize_plugins
  echo "plugin cache: $(cd ~/.claude/plugins/cache && ls -d */*/*/ | tr '\n' ' ')"
  echo "windows-mcp: $($WINDOWS_MCP_PY -c 'import importlib.metadata as m;print(m.version("windows-mcp"))')"
  echo "skills-cli: $(npm ls -g skills --depth=0 2>/dev/null | grep -o 'skills@.*')"
  echo "happy dirs: $(ls D:/software/happy | tr '\n' ' ')"
  echo "cc-connect 启动版本: $(grep -i 'cc-connect.exe' ~/.cc-connect/start-cc-connect-claude.cmd | grep -o 'v[0-9][^\\" ]*' | sort -u | tr '\n' ' ')"
  echo "claude-sessions fork base: $(git -C $CLAUDE_SESSIONS_SRC describe --tags --abbrev=0)"

  section "🔀 Windows codex-config 漂移（无输出 = 一致）"
  git -C $CODEX_CONFIG fetch -q
  echo "codex-config: $(git -C $CODEX_CONFIG log --oneline -1) | 未提交 $(git -C $CODEX_CONFIG status --porcelain | wc -l) 个 | 本地领先/落后 $(git -C $CODEX_CONFIG rev-list --left-right --count HEAD...@{u})"
  diff -rq $CODEX_CONFIG/skills-using/root ~/.agents/skills | grep -v '__pycache__\|: README.md$'
  diff -rq $CODEX_CONFIG/claude/agents ~/.claude/agents
  # 这些 hook 文件来自 claude-desktop-phone 项目或是备份，本来就不在 codex-config 里
  diff -rq $CODEX_CONFIG/claude/hooks ~/.claude/hooks | grep -v '__pycache__\|install_hook.py\|test_require_skill.py\|cc_connect_push\|push_away\|\.bak'

  section "📌 Windows 待决项"
  grep -q "awk '{print }'" ~/.claude/settings.json && echo "⚠️  statusLine 仍是 awk '{print }'（\$2 丢了，清单 2.3）"
  grep -q 'disabled_commands' ~/.cc-connect/config.toml || echo "⚠️  PC cc-connect 未配 disabled_commands = [\"upgrade\"]（清单 2.9）"
}

check_zcm6() {
  section "🐧 zcm6 已装"
  ssh zcm6 bash -s <<'EOF' 2>&1 | grep -v "$PQ_NOISE"
source ~/.bash_soft_env >/dev/null 2>&1   # 代理 + git 2.43 + nvm node；不 source 会静默超时或用到坏 node
echo "cli: $(claude --version) | 已下载: $(ls ~/.local/share/claude/versions | tr '\n' ' ')"
echo "plugins:"; claude plugin list 2>&1 | awk '/❯/{n=$2} /Version:/{v=$2} /Status:/{print "  " n " " v " " $3}'
echo "node: $(node --version)"
echo "cc-connect 启动版本: $(grep -o 'tools/cc-connect/v[^/:" ]*' ~/.cc-connect/start-cc-connect.sh | sort -u | tr '\n' ' ')"
echo "happy wrapper 版本: $(grep -o 'path_happy_root/[0-9][^/" ]*' ~/mysoft/tools/happy/bin/happy | sort -u | tr '\n' ' ')"
echo "screen: $(screen -ls | awk '/^\t[0-9]+\./{print $1}' | tr '\n' ' ')"
C=~/mysoft/pei/codex-config
git -C $C fetch -q
echo "codex-config: $(git -C $C log --oneline -1) | 落后 $(git -C $C rev-list --count HEAD..@{u})"
echo "---- 漂移（无输出 = 一致）"
for s in $(ls ~/.claude/skills); do
  [ -d $C/skills-using/root/$s ] && ! diff -rq $C/skills-using/root/$s ~/.claude/skills/$s >/dev/null && echo "skill drift: $s"
done
diff -rq $C/claude/agents ~/.claude/agents
EOF
}

check_upstream() {
  section "🌐 上游最新"
  echo "claude-code: $(npm view @anthropic-ai/claude-code version)"
  echo "claude-hud: release $(gh release view -R jarrodwatts/claude-hud --json tagName -q .tagName) | main $(gh api repos/jarrodwatts/claude-hud/contents/.claude-plugin/plugin.json --jq .content | base64 -d | grep -o '"version": *"[^"]*"')"
  echo "ponytail: release $(gh release view -R DietrichGebert/ponytail --json tagName -q .tagName) | 补丁 PR #1192 $(gh pr view 1192 -R DietrichGebert/ponytail --json state -q .state)"
  echo "windows-mcp: $(curl -s --max-time 20 https://pypi.org/pypi/windows-mcp/json | python -c 'import json,sys;print(json.load(sys.stdin)["info"]["version"])')"
  echo "playwright-mcp: $(npm view @playwright/mcp version)（npx @latest 每次启动自动跟）"
  echo "skills-cli: $(npm view skills version)"
  echo "happy: $(npm view happy version)"
  echo "cc-connect:"; gh release list -R chenhg5/cc-connect -L 3 | awk -F'\t' '{print "  " $1 " " $2}'
  echo "claude-sessions: $(git -C $CLAUDE_SESSIONS_SRC ls-remote --tags origin | grep -o 'v[0-9.]*$' | sort -V | tail -1)"
}

### main
if [ "$(ps -ef | grep -c '[k]eep_zcm6')" = 0 ]; then
  echo "⚠️  zcm6 反向隧道没在跑（keep_zcm6），zcm6 和部分外网检查会超时"
fi
check_windows
[ "$1" = "-skip_zcm6" ] || check_zcm6
check_upstream
section "🎉 检查完成（只读）"
### to here
