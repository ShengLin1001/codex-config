---
name: p-windows-desktop
description: "ALWAYS invoke BEFORE the first mcp__windows-mcp__* call that clicks, types, scrolls, presses keys, or launches or switches apps on PJ's Windows desktop, including a one-off click or a demo. Do NOT drive the desktop through windows-mcp without loading this skill first. Do NOT invoke when PowerShell, an API or p-edge-browser can do the job. 触发：操作桌面软件、点一下、在某个窗口里输入、打开或切换应用窗口、用 windows-mcp、演示 windows-mcp、接管电脑。"
---

# Windows 桌面操作（windows-mcp）

只在命令行 / API 和 `p-edge-browser` 都不够时才动桌面。核心顺序：**先只读侦察，确认框获批后才改变桌面**。

## 授权规则

- 需要接管的调用（relaxed 策略）：`Click`、`Type`、`Scroll`、`Move`、`Shortcut`、`MultiSelect`、`MultiEdit`，以及 `App` 的 `switch` / `resize`。`Screenshot`、`Snapshot`、`PowerShell`、`App launch`、`Process` 不需要接管——正因如此，不能拿它们在获批前改变桌面。`ControlStatus` 可查 `state` 和 `policy`（strict 策略下全部要接管）。
- 每段控制期的第一个需接管调用会先弹确认框（琥珀色边缘 + 10 秒倒计时），调用一直阻塞到有结果：点 Allow 或无人应答到倒计时结束 → 接管；点 Deny → `CONTROL_DENIED`；用户继续用电脑但不回答 → `USER_CONTROL`。
- 许可持续到用户接管（碰鼠标键盘）为止，之后的调用会重新弹框。用户拒绝、无视确认框或从 AI 手里抢回桌面后，在他静止 10 秒之前，调用一律直接返回 `USER_CONTROL`，不再弹框。

## 流程

运行脚本：`powershell -NoProfile -ExecutionPolicy Bypass -File "<本 skill 目录>/scripts/desktop-state.ps1"`，输出前台窗口的 pid、标题、矩形，以及各窗口是否最小化。

1. **只读侦察**：跑脚本留底，确定目标窗口标题或要启动的程序；要看屏幕就用 `Screenshot`。这一步不启动、不切换、不最小化、不点击。
2. **接管**：先用一句话告诉用户“即将接管，请别碰鼠标键盘；确认框点 Allow now 后立刻松手，或等倒计时”。然后第一个需接管调用就发 `Shortcut` `win+m`，获批后才最小化全部窗口。
3. **单独调出目标窗口**：已有窗口用 `App switch`，name 写完整窗口标题，它会把窗口从最小化还原并核验前台；新程序先 `App launch`，再 `App switch` 一次。
4. **核验**：再跑一次脚本，前台的 pid 和标题对上才继续，并记下矩形。之后所有坐标都要落在这个矩形里。
5. **操作**：核验过就连续下发，不必每步截图。`Type` 带 `loc` 时会先点击该点，把焦点拉回目标；`Shortcut` 会发给当前前台窗口，发之前要确认前台。弹出新窗口或对话框、或者任何调用报错后，回到第 4 步。
6. **收尾**：按 PID 关掉自己开的进程（自己开的 Notepad 用 `Stop-Process` 直接关，不会弹保存框）。用 PowerShell 跑 `(New-Object -ComObject Shell.Application).UndoMinimizeALL()` 还原窗口，它不需要接管，用户中途抢回桌面也能用。最后再跑一次脚本，和第 1 步的结果对照。还原后前台可能换成别的窗口：仍在控制期就用 `App switch` 切回第 1 步的前台窗口，否则告诉用户。

## 陷阱

- `USER_CONTROL`：用户正在用电脑，或者刚拒绝过。不要循环重试：先收尾还原桌面，再问用户。需要等待时用 PowerShell `Start-Sleep -Seconds <wait_seconds + 1>`，等到 `ControlStatus` 返回 `ready` 再试。
- `CONTROL_PREEMPTED` 且 `executed_steps: 0`：刚接管、光晕还没出来时用户动了鼠标，这一步什么都没执行。等用户静止后重试一次即可。
- 置顶窗口（如 Claude sessions 小窗）不受 `Win+M` 影响，可能盖住目标窗口的一部分，坐标要避开它。
- `App launch` 后新窗口显示在最上层，前台焦点却可能还在 explorer 上，这时 `Shortcut` 会发到桌面。
- `Screenshot` 截图时会隐藏 AI 光晕和提示条，截不到不代表没接管。
- `Snapshot` 只在需要元素名称或 id 时用，其他窗口会挤占它的元素名额。
- WebView2 应用（如新版 Outlook）第一次读 UI Automation 只能拿到外壳，几秒后再读。
- 演示和试验只在自己新开的窗口里做，不要在用户已打开的文件上试。
