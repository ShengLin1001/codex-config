# 从 zcm6 远程使用

链路：zcm6 的 `playwright` MCP = `ssh winbrowser` → Windows `sshd`（`127.0.0.1:2222`，只认 `~/.ssh/id_ed25519_winbrowser`）→ `mcp-remote` → Windows 桌面会话里的 `scripts/serve-http.ps1`（`127.0.0.1:8931`，由计划任务「Playwright MCP HTTP (zcm6)」在登录时启动）→ 用户日常 Edge。`winbrowser` 经 37897 端口的 Clash 代理 CONNECT 回 Windows 本机。

前提：笔记本开机且已登录、Fuyu 的 zcm6 隧道在线、Edge 在运行。

## 和本机的差别

- 工具返回的路径都是 Windows 路径。取文件：`scp "winbrowser:C:/Users/louis/.claude/playwright-output-remote/<文件>" <目标>`。目标放 home 下，不放 `/tmp`：ln2 是多人共用的登录节点。
- 网页触发的下载落在 Edge 默认下载目录 `C:/Users/louis/Downloads/`，不进上面的输出目录；扩展模式下 Playwright 收不到 `download` 事件，别等它（会超时）。点完下载用 `ssh winbrowser "dir C:\Users\louis\Downloads"` 确认文件，再 scp 取回；取回后删掉 Windows 上的那份。
- `browser_run_code_unsafe` 里没有 `require`，写不了本地文件。
- `browser_run_code_unsafe` 的 `filename` 由 Windows 侧读取，且只能读输出目录里的文件：先 `ssh winbrowser "copy C:\Users\louis\.agents\skills\p-edge-browser\scripts\turnstile-click.js C:\Users\louis\.claude\playwright-output-remote\"`，再传 `C:/Users/louis/.claude/playwright-output-remote/turnstile-click.js`。
- 「交人接管」的响铃从 zcm6 发不出来，用户也可能不在电脑前：在对话里说明要处理的标签页，然后等待。
- 接管的是用户日常 Edge，带全部登录态。`~/.ssh/id_ed25519_winbrowser` 不复制、不外传、不放宽权限。

## 连不上时按顺序查

1. `ssh winbrowser whoami` 失败：查 Fuyu 隧道（37897）和 Windows 服务 `sshd`。
2. `ssh winbrowser "netstat -ano | findstr :8931"` 没有 LISTENING：`ssh winbrowser 'schtasks /run /tn "Playwright MCP HTTP (zcm6)"'`，日志在 Windows 的 `C:\Users\louis\.claude\playwright-serve-http.log`。
3. 8931 在监听，但报扩展连不上或弹出选标签页界面：按 SKILL.md「连接」排查 Windows 侧。`serve-http.ps1` 启动时从 `~/.claude.json` 读 token，改了 token 要重跑第 2 步的计划任务（先结束旧进程）。
