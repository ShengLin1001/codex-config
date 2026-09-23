---
name: p-edge-browser
description: "ALWAYS invoke BEFORE using the mcp__playwright__browser_* tools. Use when WebFetch fails (403, empty or JS-only content, anti-bot page) or the task needs the user's real Edge: logged-in sites, clicking, form filling, downloading papers. Do NOT invoke for ordinary search or readable public pages — WebSearch/WebFetch come first. 触发：WebFetch 403 / 抓不到内容、网站进不去、Just a moment 验证页、过人机验证、用我的浏览器打开、登录后操作、下载文献、填网页表单。"
---

# 真实 Edge 浏览器操作

## 何时用

按顺序升级，前一级够用就停：

1. **WebSearch**：找信息、找链接。它返回的是搜索引擎的索引摘要，**不是页面原文**；需要准确数字 / 原文时要进页面核对。第三方供应商下 WebSearch 不可用（见 `ai-guide/reports/`），直接跳到第 3 级用浏览器搜。
2. **WebFetch**：读公开静态页。
3. **本 skill（Playwright MCP 浏览器）**：WebFetch 返回 403 / 空内容 / 验证页，或需要登录态、JS 渲染、点击、填表、下载。

## 连接

- 工具是 `mcp__playwright__browser_*`，经 Playwright Extension 接管用户**日常 Edge**（带全部登录态），token 免确认。
- 连不上时先跑 `bash scripts/check-conn.sh`，它会直接告诉你是哪一类故障。**浏览器任务进行中别跑**——扩展同时只服务一个客户端，会把当前连接挤掉。
- 脚本没覆盖到的，查 `~/.claude.json` → `mcpServers.playwright`：
  - 报 `Extension not found in ...Google\Chrome` → args 缺 `--browser msedge`。
  - 扩展页报 `Failed to connect to MCP relay: WebSocket error` → env 缺 `NODE_OPTIONS=--dns-result-order=ipv4first`（本机 IPv6 回环被拦，relay 默认听 `[::1]`）。
  - 弹出选标签页界面 / token 不符 → 扩展状态页重新生成 token、重启 Edge，再从扩展 localStorage 读出写回配置（不在对话中显示 token）。

## 操作规范

- 读内容用 `browser_evaluate` 取 `document.body.innerText` 的目标片段，不要整页 snapshot 灌进上下文；要点击 / 填表时再用 `browser_snapshot` 拿元素 ref。
- 自己新开的标签页用完关闭；不动用户原有标签页。
- 点击、填表、下载可直接做；**提交不可撤回的内容**（投稿、付款、发送消息、删除）前先向用户确认。
- 文献下载优先用 `$p-literature-download`（批量、按 DOI、带重试）；本 skill 只处理零星单篇。

## 人机验证

先判状态再决定对策——两类验证的处理方式相反。取 `document.documentElement.outerHTML` 前 200k 转小写后匹配：

| 状态 | 判据 | 对策 |
|---|---|---|
| Cloudflare 质询 | `just a moment` / `cf-turnstile` / `cf_chl_opt` / `challenges.cloudflare.com` / `verifying you are human` / `request verification` / `enable javascript and cookies to continue` | 等 → 脚本点 → 交人 |
| 图形验证 | `hcaptcha` / `g-recaptcha` / `recaptcha/api` | 直接交人 |

**Cloudflare 质询**

1. `browser_wait_for`（`textGone: "Just a moment"`，或 `time: 10`）。多数 Turnstile 在日常 Edge 上自动放行，到此为止。
2. 仍在质询页：`browser_run_code_unsafe`，`filename` 传 `scripts/turnstile-click.js` 的**绝对路径**（实测可用，不必贴全文）。脚本拟人轨迹点复选框，内含 6s 等待并回报 `passed`。
3. `passed:false` 再跑一次，**最多两轮**；两轮不过按下面交人。

**交人接管**

图形验证码一律走这条，Cloudflare 两轮不过也走这条。用户多半没盯着终端，所以顺序是**先让他看见，再等**：

1. 把标签页弹到前台——`browser_run_code_unsafe`：
   ```js
   async (page) => { await page.bringToFront(); return page.url(); }
   ```
2. 响铃提醒（PowerShell，响在用户机器上）：`[console]::beep(880,300)`。
   别在 `browser_run_code_unsafe` 里往 stdout 写 `\a`——那是 MCP 的 JSON-RPC 流，会冲掉协议。
3. 告诉用户"请在已弹出的标签页完成验证"，然后每 5s 用 `browser_evaluate` 复判状态，放行后继续。

**不要刷新页面**——刷新重置质询并加重风控评分。

**陷阱**

- 绝不点 hCaptcha / reCAPTCHA 的复选框：点了会升级成图片题，比原地不动更糟。脚本只认 Turnstile。
- Cloudflare 主要按**出口 IP** 打分。本机 Edge 走系统代理（`127.0.0.1:7897`）时质询可能永远停在 in progress；这种情况脚本再点也没用，要么让用户临时关代理，要么交人。
- 过一次后 `cf_clearance` cookie 对该站点通常可用一段时间，后续访问别再主动触发质询。
- 任何情况下都不要反复刷新重试。

撞过的站点先查 `references/site-notes.md`，过完再把新情况追加一条。
