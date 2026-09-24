# skills-using/root 调用方式汇总

本目录未用 `explicit/` `implicit/` 目录分组。隐式类靠 `description` 触发条款路由；显式类另有硬开关，见下。

## 显式调用（用户点名 / 明确要求才触发）

硬开关只有一处：`agents/openai.yaml` 的 `policy.allow_implicit_invocation: false`。Codex 直接认它（用 `$<name>` 调用）；Claude Code 靠 `pei_ai_univ_reinstall -hook` 把它翻译成 settings.json 的 `skillOverrides: user-invocable-only`（只能由用户输入 `/<name>` 调用，自然语言点名不会加载）。不在 SKILL.md 加 `disable-model-invocation`。`description` 里的 `Use ONLY when` 只是软约束。

| Skill | 触发判据 |
|---|---|
| p-literature-download | `Use ONLY when the user explicitly asks`；正文要求显式点名，如 `$p-literature-download` |
| p-tdd | `Use ONLY when the user explicitly asks for test-driven`；事后补测试不触发 |
| p-code-review | `Use ONLY when ... explicitly asks`；裸「review」/ 贴 diff 不自动启动，需 `$p-code-review` |
| p-grill-me | `Use ONLY when ... explicitly asks`；任务中的普通澄清提问不触发 |
| p-diagnosing-bugs | `Use ONLY when ... explicitly asks`；语法错 / 一行小修 / 已知原因不触发 |
| p-handoff | `Use ONLY when ... explicitly asks`；普通「总结刚才做了什么」不触发 |
| p-research | `Use ONLY when ... explicitly asks`；已在上下文的事实 / 快速查阅不触发 |
| p-article-evaluated | `Use ONLY when ... explicitly asks`；只诊断不改写，需 `$p-article-evaluated` |
| p-article-polishing | `Use ONLY when ... explicitly asks`；改写 / 润色 / 定 outline，需 `$p-article-polishing` |
| p-ppt-academic | `Use ONLY when ... explicitly asks`；仅 Windows，碰到 .pptx 不自动启动，需 `$p-ppt-academic` |

## 隐式调用（按任务类型 / 动作自动触发）

| Skill | 触发时机 |
|---|---|
| p-agent-doc-writing | 写 / 重构 agent 指令文件前（`ALWAYS invoke BEFORE`） |
| p-code-style | 写 / 改 PJ 脚本类代码前，含一行小修（`ALWAYS invoke BEFORE`） |
| p-git-commit | 写 commit message 前（`ALWAYS invoke BEFORE`） |
| p-edge-browser | 用 Playwright MCP 浏览器前，或 WebFetch 失败 / 需登录态、点击、填表、下载时（`ALWAYS invoke BEFORE`） |
| p-plot-figure | 写 / 改 matplotlib 绘图代码前（`ALWAYS invoke BEFORE`） |

## 备注

- 显式类 skill 均在 `SKILL.md` 正文加了 `## 触发条件` 段，写明 `/<name>`（Claude Code）与 `$<name>`（Codex）两种调用方式。
- 被 `~/.claude/hooks/gate.json` 强制要求加载的 skill 不能设成显式，否则模型无法加载，流程会卡死。
- p-code-review 与内置 `code-review` skill 触发词曾重叠，改为显式点名后，裸「review」交给内置。

## 外部仓库 skill 的上游同步（git subtree）

`p-literature-download`、`p-edge-browser`、`p-ppt-academic`（上游仓库名 `p-ppt-generate`）
是从各自的 GitHub 仓库以 `git subtree --squash` 引入的，
拉上游更新在 codex-config 仓库根目录执行：

```bash
git subtree pull --prefix=skills-using/root/p-edge-browser p-edge-browser main --squash
git subtree pull --prefix=skills-using/root/p-ppt-academic p-ppt-generate main --squash
```

`p-edge-browser`、`p-ppt-generate` 是 `git remote add` 过的远端名（`git@github.com:ShengLin1001/<名字>.git`）。

⚠️ **别用 `git subtree add/pull --prefix=... <URL> main`**：分支名 `main` 会被解析成**本地** main，
结果把 codex-config 自己塞进子目录。一律先 `git remote add` + `git fetch`，再用 `<remote>/main` 或 `<remote> main`。
