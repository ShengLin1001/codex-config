---
name: p-wezterm-hermes
description: "配置和排查 Windows 上的 WezTerm、Git Bash 与 Hermes。"
---

# WezTerm and Hermes

## 核心流程

1. 确认实际启动的 shell、`bash.exe` 路径、登录参数和启动目录。
2. 在 WezTerm 中用 `default_prog` 指向目标 shell；只在终端支持时启用 kitty keyboard 等协议。
3. 分别在 WezTerm 和 VS Code 终端验证 `SHELL`、`PATH`、alias、交互键和 Hermes TTY 输出。
4. 修改配置后完全重启终端，再用真实 ANSI/Hermes 输出复测。

## 易踩点

- Windows 路径传入 Git Bash 时优先用 `F:/path` 或正确引号，不硬编码某台机器的盘符位置。
- VS Code 终端不一定支持 WezTerm 的键盘协议，配置要分开。
- wrapper 启动无报错不代表子进程或 TTY 功能正常。
