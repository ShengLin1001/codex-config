---
name: p-claude-toolchain-upgrade
description: ALWAYS invoke BEFORE checking or upgrading the Claude Code toolchain on Windows or zcm6 — CLI, VS Code extension, plugins, MCP servers, codex-config skills/agents/hooks, cc-connect, Happy, claude-sessions, Claude-Code-Usage-Monitor — or re-aligning zcm6 with Windows. Do NOT update or reconfigure any of these without loading this skill first. 触发：检查 Claude 配置要不要升级、升级插件/MCP/扩展、按维护清单检查、扩展版本和 CLI 不一致、HUD 显示不对、usage monitor 任务栏小部件显示或位置不对、zcm6 与 Windows 对齐、skill 安装副本漂移。
---

# Claude 工具链检查与升级（Windows + zcm6）

## 依据

- 版本基线和逐组件细节在 `F:\BaiduSyncdisk\version20240608\main_code_space\other\temp\check_claude\ai-guide\reports\20261026-claude-ai-toolchain-maintenance.md`（下称"清单"）。本 skill 只写流程、检查入口和坑，基线以清单为准。
- cc-connect、Happy、推送 hook 的现状以 `F:\BaiduSyncdisk\version20240608\main_code_space\other\claude-desktop-phone\README.md` 的"当前状态"为准。清单 2.9 已落后：两端都改跑自编译 fork `v1.5.1-beta.4-pj2`，Discord channels 插件两端都已 disabled。
- 不在范围内：Codex、Hermes；Karma 已退役（清单 2.4）；zcm6 上的 VS Code 扩展（用户在 zcm6 不用它）。

## 流程

1. **只读检查**：在 Windows git-bash 跑本 skill 目录下的 `scripts/check.sh`（约 1 分钟，反向隧道不在时加 `-skip_zcm6`）。输出两端已装版本、上游最新版、codex-config 漂移，以及清单第 4 节里能自动判断的待决项。
2. **出表交给用户**：组件 / Windows / zcm6 / 最新 / 建议（升、不升、等），每条建议写理由（安全修复、行为变化、要重打的补丁）。再附上清单第 4 节仍未决的项。**只升用户点头的项**。
3. **升级前读变更**：release notes 或 `git log HEAD..origin/main`。插件、MCP、hooks、cc-connect、Happy 都以完整权限运行；cc-connect、Happy 还要读新版源码。跨大版本，或改了 hook 注入方式、入口文件、运行时要求的，先停下给用户讲清楚再升。
4. **升级后核验**：版本号 + 功能。插件和 MCP 要开新会话才生效，在新会话里验。
5. **回写**：更新清单第 2、3 节的基线和日期；本次过程写报告到清单同目录，文件名按全局"交付文档命名"规则。

## 组件速查

| 组件 | 升级方式 | 坑 |
|---|---|---|
| Claude Code CLI | 两端自动更新，不用管 | 长会话提示 `/restart to apply` 后才用上新版；`happy` 启动的会话设了 `DISABLE_AUTOUPDATER=1`；`~/.claude.json` 的 `autoUpdates: false` 是残留字段，别改；`Auto-update failed` 多半是旧会话占着文件，退出旧会话即可 |
| VS Code 扩展（仅 Windows） | VS Code 全局 `extensions.autoUpdate` 是 `"off"`，只给 Claude Code 扩展单独勾了 Auto Update。VS Code 启动时和之后每 12 小时检查一次；`extensions.autoUpdateDelay` 已设为 0（默认 12 小时，新版发布满这么久才装），查到新版就装。CLI 升级时也会用 `code --install-extension` 顺带装一次，但继承了代理变量，在 `%APPDATA%\Code\logs\*\cli.log` 里报 `BAD_DECRYPT` | VS Code 不开就不会查，落后半天以内属正常。急用时手动补装：`env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy code --install-extension anthropic.claude-code --force`（bash 的代理变量会让 `code` 报 `BAD_DECRYPT`），或在 VS Code 扩展面板里点更新 |
| claude-hud、ponytail | 每端各跑 `claude plugin marketplace update <m>` → `claude plugin update <p>@<m>` | 两个 marketplace 都没开 `autoUpdate`，ponytail 也不要开（会冲掉补丁）。有没有新版要看 marketplace 克隆里的 `.claude-plugin/plugin.json` / `package.json`，`plugin list` 只显示已装版本。ponytail 的 Windows 本地补丁升级会丢，照清单 2.3 重打。claude-hud 升级后必须做 statusLine 验收（清单 2.3），并确认 `~/.claude/plugins/claude-hud/config.json` 的显示项仍生效 |
| windows-mcp | `uv pip install --python D:/software/Windows-MCP/.venv/Scripts/python.exe -U windows-mcp`，重启 Claude Code | 只装在 Windows |
| Playwright MCP | `npx @latest` 每次启动自动拉 | 是否固定版本仍待用户决定 |
| skills CLI | `npm i -g skills@latest` | 要求 Node ≥ 22.20；验收用 `npx --yes skills list -g --agent claude-code` |
| codex-config | 在仓库根跑 `./scripts/pei_ai_univ_reinstall -global -root -local`（zcm6 先 `git pull --ff-only`）；`claude/agents/` 有变化时手动复制 | **要加 `-local`**：不加就从 GitHub 装，副本变成 CRLF，还会丢掉被 git 忽略的文件（如 `p-article-polishing/ref/*.pdf`）。改了上游要先 commit、push，zcm6 才拉得到。本 skill 在 `skills-using/project/remote/`，在清单所在项目根跑 `pei_ai_univ_reinstall -project remote -local` 安装 |
| cc-connect | 把 fork 分支 `fix/discord-askq-2157` 合到新 tag 再编译（见 phone README） | **禁止** `cc-connect update` 和 IM 里的 `/upgrade`：会升到官方 v1.5.0，bypass 下会自动替你答选择题 |
| Happy | `npm install --prefix` 到新版本目录，再跑 `happy-patch-dist.sh`（清单 2.9） | **禁止** `npm i -g happy@latest`、`npm update`（会覆盖补丁）和 `happy connect claude`（会交出 Claude 凭据） |
| claude-sessions | fork 分支 rebase 到新 tag，重编 GUI 版和 zcm6 musl 版（清单 2.5） | 不用 `install-app`（会装到 C 盘） |
| Claude-Code-Usage-Monitor（仅 Windows） | `gh release download` 新版 exe 并核对 sha256 → `taskkill //IM claude-code-usage-monitor.exe` → 换掉 `D:\software\Claude-Code-Usage-Monitor\` 下的 exe → `wscript D:\software\Claude-Code-Usage-Monitor\start-with-proxy.vbs` 重启 | 开机自启的 HKCU Run 值 `ClaudeCodeUsageMonitor` 指向这个 vbs，它负责设好代理再启动。所以程序菜单里的 Start with Windows 显示为未勾选，**不要去点**：点了会把 Run 值写回 exe，开机就不走代理了。改用自建主题时，主题副本不会随升级更新，见下 |

**claude-hud 只显示 5 小时额度、不显示周额度**：不是坏了。周额度默认要到 `display.sevenDayThreshold`（默认 80%）才显示；要常显，在 `config.json` 的 `display` 里设 `"sevenDayThreshold": 0`。

**Usage Monitor 的 Fable 周额度**：目前用内置主题，Fable 正常显示（`%APPDATA%\ClaudeCodeUsageMonitor\settings.json` 的 `active_theme_path` 指向 `themes\classic-usage-widget.json`）。程序设置里没有隐藏单个额度的开关；要隐藏时把 `active_theme_path` 改指自建主题 `themes\classic-no-fable.json`。它是内置主题的旧副本，先和内置版 diff；有变化就重新复制，再做三处改动：顶部 `id`、`name` 改名；`fable-provider` 层的 `render` 改成 `"0"`；`surfaces[0].width` 删掉末尾的 `+ providers.claude.enabled * claude.model.fable.available * 93`。改 `settings.json` 前先停进程，它运行时会回写这个文件。

**Usage Monitor 被拖离任务栏后回不去**：停进程，删掉 `settings.json` 里的 `placement_override`，再启动，它就停回托盘左侧（上游测试也用这个方法复位）。托盘左侧要留有空位：TrafficMonitor 已设成 `task_bar_wnd_on_left = true`，不要改回右侧。

## zcm6 操作

- 先在 Windows 确认隧道：`ps -ef | grep keep_zcm6`。不要手动 `ssh zcm6-proxy`。
- 每条非交互命令开头加 `source ~/.bash_soft_env >/dev/null 2>&1`。漏了会出三种问题：外网静默超时；git 落到 1.8.3，`claude plugin marketplace add` 报 `unable to parse command-line config`；node 落到 `~/.local/bin` 的坏版本，报 `GLIBC_2.28 not found`。
- 用 `grep -v "post-quantum\|store now\|openssh.com/pq"` 过滤 ssh 的警告。
- 改 `~/.claude/settings.json` 前先 `cp -p` 备份。两端哪些照搬 Windows、哪些保留 zcm6 自己的，见清单 3.4。
- 长期运行的 screen 会话（如 `cc-connect`）有自己的 PATH。验证插件 hook 时查 `/proc/<pid>/environ`，或真开一个 `claude -p` 会话，只看 `type -P node` 不够。

## 删除

旧插件缓存、备份、残留目录都只列给用户手动清理；自己只删单个明确的文件路径。
