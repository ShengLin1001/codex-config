#!/usr/bin/env bash
# 一条命令回答"浏览器通不通"。不依赖 Claude Code 重启：直接以 stdio JSON-RPC
# 驱动一个临时 MCP 服务器，让它开 example.com，看扩展有没有回连。
#
# 用法：bash scripts/check-conn.sh
#
# ⚠️ 它会另起一个 relay。扩展同一时刻只服务一个客户端，所以别在浏览器任务进行中
# 跑它——会把 Claude Code 当前会话的连接挤掉。
set -u

path_cfg="${USERPROFILE:-$HOME}/.claude.json"

echo "================ 📍 读取配置 $path_cfg"
token=$(node -e '
  const cfg = require(process.argv[1]);
  const srv = (cfg.mcpServers || {}).playwright || {};
  process.stdout.write(((srv.env || {}).PLAYWRIGHT_MCP_EXTENSION_TOKEN) || "");
' "$path_cfg" 2>/dev/null) || true

if [ -z "$token" ]; then
  echo "❌ 没读到 mcpServers.playwright.env.PLAYWRIGHT_MCP_EXTENSION_TOKEN"
  echo "   → 在 Edge 扩展状态页生成 token 写回配置（别贴进对话）"
  exit 1
fi
echo "✅ token 已读到（${#token} 字符，不回显）"

# initialize → initialized → 开一个页面。sleep 撑住 stdin，否则服务器会在扩展
# 回连之前就因为 EOF 退出，看起来像"连不上"。
req='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"check-conn","version":"1"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"browser_navigate","arguments":{"url":"https://example.com"}}}'

echo "================ ▶️ 拉起临时 MCP 并打开 example.com（最多 40s）"
out=$( { printf '%s\n' "$req"; sleep 40; } | \
  PLAYWRIGHT_MCP_EXTENSION_TOKEN="$token" \
  NODE_OPTIONS=--dns-result-order=ipv4first \
  npx -y @playwright/mcp@latest --extension --browser msedge 2>&1 | grep -v '^npm notice' )

echo "================ 📊 结论"
case "$out" in
  *"Example Domain"*)
    echo "✅ 扩展已回连，example.com 可读"
    exit 0 ;;
  *"Extension not found"*)
    echo "❌ 找错浏览器 → MCP 配置 args 缺 --browser msedge"
    exit 1 ;;
  *"MCP relay"*|*"WebSocket"*|*"Timeout"*|*"timed out"*)
    echo "❌ 扩展没回连 relay。依次试："
    echo "   1) MCP 配置 env 补 NODE_OPTIONS=--dns-result-order=ipv4first"
    echo "      （relay 默认听 [::1]，本机 IPv6 回环被拦）"
    echo "   2) 完全退出 Edge（托盘也要退）再重启"
    echo "   3) 扩展状态页重新生成 token，写回 $path_cfg"
    exit 1 ;;
  *)
    echo "⚠️  未匹配到已知症状，原始输出前 40 行："
    printf '%s\n' "$out" | head -40
    exit 1 ;;
esac
