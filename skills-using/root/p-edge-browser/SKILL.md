---
name: p-edge-browser
description: "ALWAYS invoke BEFORE using the mcp__playwright__browser_* tools. Use when WebFetch fails (403, empty or JS-only content, anti-bot page) or the task needs the user's real Edge: logged-in sites, clicking, form filling, downloading papers. Do NOT invoke for ordinary search or readable public pages — WebSearch/WebFetch come first. 触发：WebFetch 403 / 抓不到内容、网站进不去、用我的浏览器打开、登录后操作、下载文献、填网页表单。"
---

# 真实 Edge 浏览器操作

## 何时用

按顺序升级，前一级够用就停：

1. **WebSearch**：找信息、找链接。它返回的是搜索引擎的索引摘要，**不是页面原文**；需要准确数字 / 原文时要进页面核对。
2. **WebFetch**：读公开静态页。
3. **本 skill（Playwright MCP 浏览器）**：WebFetch 返回 403 / 空内容 / 验证页，或需要登录态、JS 渲染、点击、填表、下载。

## 连接

- 工具是 `mcp__playwright__browser_*`，经 Playwright Extension 接管用户**日常 Edge**（带全部登录态），token 免确认。
- 连不上时依次查 `~/.claude.json` → `mcpServers.playwright`：
  - 报 `Extension not found in ...Google\Chrome` → args 缺 `--browser msedge`。
  - 扩展页报 `Failed to connect to MCP relay: WebSocket error` → env 缺 `NODE_OPTIONS=--dns-result-order=ipv4first`（本机 IPv6 回环被拦，relay 默认听 `[::1]`）。
  - 弹出选标签页界面 / token 不符 → 扩展状态页重新生成 token、重启 Edge，再从扩展 localStorage 读出写回配置（不在对话中显示 token）。

## 操作规范

- 读内容用 `browser_evaluate` 取 `document.body.innerText` 的目标片段，不要整页 snapshot 灌进上下文；要点击 / 填表时再用 `browser_snapshot` 拿元素 ref。
- 自己新开的标签页用完关闭；不动用户原有标签页。
- 点击、填表、下载可直接做；**提交不可撤回的内容**（投稿、付款、发送消息、删除）前先向用户确认。
- 文献下载优先用 `$p-literature-download`（批量、按 DOI、带重试）；本 skill 只处理零星单篇。

## 人机验证

1. 先 `browser_wait_for`（`textGone: "Just a moment"` 或等 10 s），很多验证会自动放行。
2. 仍停在验证页：告诉用户在该标签页完成验证，完成后继续读取。不要反复刷新重试——会加重风控。
3. 同站点验证通过后 cookie 通常可用一段时间，后续访问不必再验证。
