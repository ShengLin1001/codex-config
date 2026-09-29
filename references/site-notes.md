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

## sciencedirect.com（期刊 about/insights/OA/guide 页）

**2026-09-28** 期刊元数据页零质询直达（ZJU Library 授权态）。insights 页最重：
一次 navigate 60s 超时且**打断后续同批任务**（"interrupted by another navigation"
级联失败），批量抓取要每页一带 wait_for(5-8s)、失败单独重试。APC 数字在 OA 页
正文第二处 "Article Publishing Charge (APC)" 标题下（第一处是目录锚），用
lastIndexOf 取。

## pubs.aip.org

**2026-09-28** 首次访问 about/charges 常撞 "Just a moment"（403），但**同站先拿到
一个普通页后再访问，质询多数自愈放行**（charges→about 顺序两次实测）。当天全程
没用到 turnstile 脚本——等待 + 重试一次即可，别硬点。

## letpub.com.cn

**2026-09-28** 零质询。`view=search&searchname=<URL编码名>` GET 直出结果行，但
部分查询稳定空结果：JPCM（含冒号全名/简称/ISSN 均失败）、`Materials+%26+Design`
（%26 编码坏）、ISSN 当关键词无效。搜索结果行的分区列是**新锐期刊分区表**；
详情页（journalid 从结果行链接抽）才有「2025年3月升级版」+「2023年12月旧的
升级版」对照。详情页 `<title>` 里的 IF 是滞后值（Vacuum 标 3.9、行内 4.3），
以行内/详情页正文为准。

## nature.com

**2026-09-28** Scientific Reports 的 slug 是 **/srep/**（/scirep/* 全 404），
submission-guidelines 也 404；作者指引在 `/srep/author-instructions`
（内含 "first decision within 45 days"），评审标准原文在
`/srep/guide-to-referees`。页面 console 噪音大但正文稳定。

## mdpi.com

**2026-09-28** 期刊主页内嵌 "Impact Factor: x (2025)"；APC 价目页在
`/journal/<name>/apc`（`/journal/apc` 聚合页是 404）。零质询。
