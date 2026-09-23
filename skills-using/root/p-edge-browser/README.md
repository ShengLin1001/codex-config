# p-edge-browser

让**第三方供应商**（`ANTHROPIC_BASE_URL` 指向非官方中继）下的 Claude Code 接管用户日常 Edge 浏览器的 Agent Skill。

第三方中继下 WebSearch（Anthropic 服务端工具）静默失效——不报错，返回的是模型自由发挥；claude.ai connectors 因走 `ANTHROPIC_AUTH_TOKEN` 也被禁用。剩下的 WebFetch 只能读公开静态页。本 skill 补回搜索、登录态访问、点击填表、下载，以及 Cloudflare 人机验证的脚本/接管过法。

## 安装

```bash
git clone <this-repo> ~/.agents/skills/p-edge-browser
ln -s ~/.agents/skills/p-edge-browser ~/.claude/skills/p-edge-browser
```

MCP 配置（`~/.claude.json` → `mcpServers.playwright`），token 在 Edge 扩展状态页生成，**不要提交**：

```json
{
  "command": "npx",
  "args": ["-y", "@playwright/mcp@latest", "--extension", "--browser", "msedge"],
  "env": {
    "PLAYWRIGHT_MCP_EXTENSION_TOKEN": "<扩展状态页生成的 43 字符 token>",
    "NODE_OPTIONS": "--dns-result-order=ipv4first"
  }
}
```

`NODE_OPTIONS` 不是可选项：relay 硬编码监听 `localhost`，Node 24 解析成 `[::1]`，本机 IPv6 回环被拦时扩展报 `Failed to connect to MCP relay: WebSocket error`，且失败完全静默。

## 目录

| 路径 | 说明 |
|---|---|
| `SKILL.md` | skill 本体：何时用、连接排障、操作规范、人机验证分流 |
| `scripts/turnstile-click.js` | 拟人轨迹点击 Cloudflare Turnstile，由 `browser_run_code_unsafe` 执行 |
| `scripts/check-conn.sh` | 一条命令回答"浏览器通不通"，直接报出是哪类故障 |
| `references/site-notes.md` | 站点经验，只追加：哪个站会质询、怎么过的 |
| `ai-guide/reports/` | 开发记录：接入方案的实测、踩坑与最终取舍 |

## 边界

图形验证码（hCaptcha / reCAPTCHA 的选图与扭曲字符）**不由 agent 识别作答**，一律弹标签页 + 响铃交给人。
脚本只点 Turnstile 这类纯行为复选框，且两轮不过就交人。

## 安全

CDP / 扩展接管都会暴露整个浏览器（全部登录态、全部标签页）。token 等同该 profile 的接管凭证，泄露后在扩展状态页 "Generate new token" 并重启 Edge。
