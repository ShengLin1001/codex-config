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

## edge://（浏览器内部页）

**2026-10-18** 扩展模式进不去：`edge://settings/...` 导航报 `Detached while handling command`，
`context.newCDPSession` 报 `Not allowed`。改站点权限只能让用户点，或 PowerShell
`Start-Process msedge.exe "edge://settings/content/siteDetails?site=<编码后的源>"` 打开后交人。
按站删 cookie 别用 `clearCookies`（版本旧时会清全部）：`context.cookies([url])` 取出后
`addCookies` 同名同域同路径、`expires: 1` 覆盖即删。

## reddit.com / scholar.google.com（经机房 IP 代理）

**2026-10-18** Reddit 会用 cookie（`loid` / `csv` / `edgebucket`）记住从机房 IP 被拦过的浏览器，
换成能放行的出口后要删这几个 cookie 才恢复。学术「每次都要验证」先查站点 cookie 是否被屏蔽
（Preferences `profile.content_settings.exceptions.cookies` 值 2），不是代理问题。

## discord.com/developers（Developer Portal）与 discord.com/oauth2/authorize

**2026-11-03** 新建 bot 应用、改设置、把 bot 拉进服务器：

- 「创建 APP」和 OAuth「授权」两步都弹 **hCaptcha**，按「直接交人」处理，用户点完即放行。
- 条款复选框、Privileged Intent 开关：`click` 被 label/stack 遮挡超时，`force` 和 `mouse.click` 也不切换状态；**`focus()` 后按 `Space`** 能切换，切换后底部会出现「保存更改」。
- 关「公开 APP」时保存报「私密 APP 无法拥有默认授权关联」：要先去「安装」页把默认安装链接设成 None。
- 重置令牌会再弹一次多重认证（Edge 自动填好密码，点「提交」即可）；新 token 只显示一次。**读取 token 不要截图或 evaluate 出原文**，点页面里的「复制」后由 shell 从剪贴板直接写入目标文件。
- OAuth 授权页在后台标签页里一直白屏（innerText 为空），先 `page.bringToFront()` 才会渲染。

## discord.com/channels（服务器、频道、身份组设置）

**2026-11-03** 改服务器名和图标、频道名和话题、身份组颜色、类别权限：

- **上传图片**：`setInputFiles` 超时；点按钮触发的 file chooser 用 `browser_file_upload` 设文件后页面没反应，而且每点一次都排队一个 chooser，要逐个空调用 `browser_file_upload` 取消。用 `scripts/make-upload-js.py` 生成内嵌文件的 JS，再用 `browser_run_code_unsafe` 的 `filename` 执行，会弹出裁剪框，点「应用」→「保存更改」。
- 侧栏频道的齿轮「编辑频道」一直等不到 stable，`click` 会超时：先选中频道，再对齿轮按钮 `focus()` + `Enter`；或者点频道欢迎区里的「编辑频道」按钮（服务器默认频道没有这个按钮）。焦点不在按钮上时按 Enter 会触发顶部「下载 APP」横幅，多开一个下载页。
- 频道话题是 Slate 富文本，不是 textarea。定位时限定在 `getByRole('dialog', {name: '频道设置'})` 里，否则会命中底下的消息输入框；点进去后用 `keyboard.insertText`。
- 第一次打开「服务器设置」或频道设置要懒加载 2–3 s，先等再找元素。身份组列表的文字在预览里有隐藏副本，用 `getByText(..., {exact: true}).filter({visible: true})`。
- bot 的托管身份组可以改名和改颜色，色块按钮的 aria-label 就是色号（`button[aria-label="#3498db"]`）。零权限邀请的 bot 没有托管身份组。

## chatgpt.com

**2026-11-10** 零质询，登录态可用。批量开会话 / 收图时踩到的：

- 标签页在后台（`document.hidden`）时 `locator.click()` 永远等不到 "stable"，生成的图也不渲染
  （gallery 高度 0、没有 `<img>`）。发消息用 `focus()` + `fill()` + `Enter`；页面还显示
  `Loading profile` 时回车会被吞，等它消失再发。输入框是 `getByRole('textbox')`，没有 `#prompt-textarea`。
- 后台标签页发消息后 URL 不跳转、输入框留着草稿，但会话已建成。**别按 URL 判断成败**，
  按项目页 `main a[href*="/c/"]` 新增链接或后端接口的 user 消息数判断，否则会重复提交。
- 收结果不靠 DOM：页面内 `fetch('/api/auth/session')` 取 `accessToken`，再调
  `/backend-api/gizmos/<g-p-id>/conversations`、`/backend-api/conversation/<id>`；图片在
  `image_asset_pointer` 里，经 `/backend-api/files/download/<file_id>?conversation_id=<id>` 换
  `download_url`（estuary，需 cookie，只能页面内 fetch）。
- `browser_run_code_unsafe` 里没有 `require`/`import`，写不了文件。图片在页面内用
  `OffscreenCanvas` 缩小转 base64，交给 `browser_evaluate` 的 `filename` 落盘再解码；
  落盘内容是 JS 对象字面量格式，不是严格 JSON。
- 会话里图片出完后 assistant 状态可能一直停在 `in_progress`，不影响取图和追问。
- **2026-11-14** Edge 窗口不在前台时（`document.hidden` 为真，`bringToFront` 只切标签页、不抬窗口），`fill` 后按 `Enter` 不发送，草稿留在输入框里，脚本照常返回。改成页面内点发送按钮：`page.evaluate(() => document.querySelector('form button[aria-label="Send"]').click())`，后台也能发。每次调用只发一条，发完用 gizmos conversations 接口核对会话数。

## github.com（issue 里传图）

**2026-11-14** 新版 issue 页没有 `input[type=file]`，`gh` 也传不了附件。做法：在 `issues/new` 的
`textarea[aria-label="Markdown value"]` 上派发 `ClipboardEvent('paste', {clipboardData: dt})`（dt 里放 File），
GitHub 会上传并插入 `https://github.com/user-attachments/assets/<id>`，轮询 textarea 取地址；全部传完清空 textarea、
不提交，再用 `gh issue create --body-file` 发正文。文件别编进 run_code 的代码里（整段会回显进上下文）：
本地 `python -m http.server` 起服务，在 run_code 里用 `page.context().request.get()` 取（走 Node，不受页面 CSP 限制），
`buf.toString('base64')` 作为 `page.evaluate` 的参数传进去。`gh issue create` 偶尔报 `graphql: EOF`，先用 REST 查是否已建成再重发。
