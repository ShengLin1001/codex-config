# 站点经验

只追加，不整理成体系。一条一个站点，写"实际遇到什么 + 怎么过的"，不写通用原理。
日期是实测日期，站点风控会变，过期条目留着当参考不当保证。

## sciencedirect.com / pdf.sciencedirectassets.com

**2026-09-23**

- 文章页（`doi.org/10.1016/j.actamat.*` → `www.sciencedirect.com/science/article/pii/*`）：
  **零质询直达**，日常 Edge profile 里 `.sciencedirect.com` 的 `cf_clearance` 还在有效期。
  页面显示 `Brought to you by: Zhejiang University Library` + `Full text access`，机构授权正常。
- PDF 路径（文章页的 `/pdfft?...` 链接）：**会撞质询**。跳到
  `pdf.sciencedirectassets.com/craft/capi/cfts/init?...`，标题 `Security verification`，
  URL 里带 `c=pdf_country_code_mismatch` —— 出口 IP 是 CN，与签名 URL 的归属地不符触发的。
- `scripts/turnstile-click.js` 一次点击通过，页面直接跳到签名后的 `main.pdf`。
  **这是脚本唯一一次真实质询验证，也是它当前全部的实战证据。**

## nowsecure.nl

**2026-09-23** 真 Turnstile，但在日常 Edge 上自动放行，没给点击的机会。
有用的是它的 DOM 形状：页面挂 **2 个** `cf-turnstile-response` 隐藏 input，
第二个 `y = -404`（屏幕外）。`.first()` 会有一半概率点到看不见的那个——
脚本因此改成只挑可见的 widget。

## demo.turnstile.workers.dev

**2026-09-23** Cloudflare 官方 demo，用的是 **testing sitekey**：
token 恒为 `XXXX.DUMMY.TOKEN.XXXX`，永远自动通过，**不能用来验证点击逻辑**。
它唯一的价值是确认"隐藏 input 的父元素"这条取框路径能拿到合理的 box（300×71）。

## 通用观察（从上面三个站点得出）

`iframe[src*='challenges.cloudflare.com']` 这个选择器**在真实页面上恒为 0 命中**：
widget 在 shadow DOM 里，iframe 的 `src` 是空的。任何抄来的 Turnstile 代码用它做
兜底都是死代码——已从脚本里换成 `.cf-turnstile` 容器。
