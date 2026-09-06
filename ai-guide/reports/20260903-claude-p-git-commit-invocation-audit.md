# p-git-commit 八月调用审计

## 结论

**与 p-code-style 不同，`p-git-commit` 在八月大部分时间根本没有被写进本地 agent 的系统提示词**，因此对本地 Claude Code 和本地 Codex 不存在"已写约束却漏用"的问题。

- **本地 Codex**：八月凡是真正执行 `git commit` 的会话（7 个会话、约 10 次提交）**全部在提交前加载了 `p-git-commit`**。其中 5 个会话发生在约束写入 `~/.codex/AGENTS.md`（2026-08-27）之前，说明这一行为在无系统级约束时已经稳定，靠的是仓库 README 工作流、`~/.codex/memories` 记录和用户习惯性输入 `$p-git-commit`。**无漏用。**
- **本地 Claude Code**：八月本地几乎不用 Claude Code 提交——全月只有 1 次真实 `git commit`（2026-08-31，`temp/download_pdf` 项目），且**该次调用了 `p-git-commit`**。样本量为 1，无法评价漏用。
- **Hermes**：八月约 54 个会话执行过 `git commit`，其中约 28 个（52%）有会话内加载 `p-git-commit` 的证据，约 26 个没有。漏用集中在 8 月 3—6 日的手稿 / Sphinx 文档 / Obsidian 批量同步提交和 cron 流水线提交。**Hermes 的 `SOUL.md` 从未写入该约束**，只有一条 `memories/MEMORY.md` 记录。存在明显但可解释的漏用。

一句话：本地两个 agent 的约束是 8 月底才补上的，补之前 Codex 已经做得很好；真正长期靠"隐式 + memory"运行、且有一半提交没走 skill 的是 Hermes。

## 关键区别：系统提示词中是否写入过该约束

| 位置 | 八月是否含 "用 p-git-commit 生成 commit message" | 依据 |
|---|---|---|
| 本地 `~/.codex/AGENTS.md` | **2026-08-27 起有**；8 月 1—26 日为旧版（CentOS HPC），无 Git Commit 段 | 会话内嵌 `<INSTRUCTIONS>` 快照在 `2026-08-27T00:27Z` 出现该段；文件 mtime `2026-08-30 04:45 PDT`（后续再同步） |
| 本地 `~/.claude/CLAUDE.md` | **2026-08-30 起有**；8 月 1—29 日无 | 全部 8 月 Claude 会话中，最早出现"生成 commit message 时使用 `p-git-commit` skill"的是 `2026-08-30T06:13`；文件 mtime `2026-08-30 04:45 PDT` |
| 仓库 `codex-config/AGENTS.md`（本仓库项目级） | **整个八月都没有** | 该约束曾以"更新工作流 / 3. 使用 `$p-git-commit`"形式存在（2026-05-21 加入），于 **2026-07-30 提交 `4771680`「移除更新工作流说明」整段删除** |
| `codex/AGENTS_zcm6.md`（zcm6 Codex 的 AGENTS 存档副本） | **整个八月都有** | "## Git Commit / 生成 Git commit message 时，默认使用 `$p-git-commit` skill。" 自 2026-05-21 `58f9c14` 加入后未再改动 |
| `hermes/zcm6/SOUL.md` | **从未有** | HEAD 与全历史中 `SOUL.md` 无任何 `git commit` / `p-git-commit` 内容；仅 `hermes/zcm6/memories/MEMORY.md` 有一条 p-git-commit 行为记录 |
| 仓库 `README.md` | 有（`2. 使用 $p-git-commit 生成中文 commit message`），但这是 README，不是任何 agent 的系统提示词 | — |

补充：本地 `~/.codex/AGENTS.md` 与 `~/.claude/CLAUDE.md` 的 mtime 完全相同（`2026-08-30 04:45`），即用户所说"前段时间规范 CLAUDE.md 等系统提示词"的那次统一改动。但从会话快照看，Codex 侧的 Git Commit 段其实早在 8 月 27 日就先行生效，8 月 30 日只是把两份文件对齐再同步了一次。

## 审计方法

沿用 `20260901-codex-p-code-style-invocation-audit.md` 的口径。

- 时间范围：2026-08-01 00:00 – 2026-09-01 00:00 UTC。
- Agent / 环境：本地 Windows 的 Claude Code、Codex、Hermes。zcm6 会话本次未拉取，仅据仓库存档副本判断其系统提示词状态。
- 目标 skill：`p-git-commit`。
- "应调用"事件 = 会话内真实执行了 `git commit`（Bash / `exec_command` / `terminal` 工具调用，排除 `git log`、`--dry-run` 和 skill 文档里的 `git commit -m "<type>(<scope>)…"` 示例行）。纯生成 message 而不提交的情况本次未单独统计（本地基本都是"提交并推送"）。
- "已调用"证据：
  - Claude Code：`Skill` 工具调用 input 含 `p-git-commit`，或读取 `p-git-commit/SKILL.md`。
  - Codex：`exec_command` 里 `Get-Content …\p-git-commit\SKILL.md`，或显式 `$p-git-commit`（会话中注入 `<name>p-git-commit</name> … SKILL.md` 块）。
  - Hermes：`state.db` 中 `tool_name='skill_view'` 且 content 含 `p-git-commit`，或会话内出现 `name: p-git-commit` / `<name>p-git-commit</name>` / `p-git-commit/SKILL.md` 内联内容。
- 只读审计，未改动任何配置或 skill。

## 各 agent 结果

### 本地 Codex — 无漏用

八月本地 Codex 共 95 个会话，其中 7 个执行过真实 `git commit`：

| 会话起始 (UTC) | 提交数 | 提交前是否加载 p-git-commit | 约束是否已生效 (≥08-27) |
|---|---|---|---|
| 2026-08-20T22:25 | 1 | 是（05:29 读 SKILL.md → 05:37 提交） | 否 |
| 2026-08-20T22:46 | 2 | 是（会话初 05:49 加载；两次提交在其后） | 否 |
| 2026-08-21T02:06 | 1 | 是（09:17 读 → 09:18 提交） | 否 |
| 2026-08-24T01:50 | 3 | 是（每次提交前都重新读 SKILL.md） | 否 |
| 2026-08-25T21:53 | 1 | 是（16:02 读 → 16:03 提交） | 否 |
| 2026-08-28T01:12 | 1 | 是（用户显式 `$p-git-commit 提交并git push`） | 是 |
| 2026-08-29T05:16 | 1 | 是（12:16 读 → 12:25 提交） | 是 |

7/7 会话在提交前加载了 skill，其中 5 个发生在系统级约束写入之前。Codex 的稳定来源是：仓库 README 的提交工作流、`~/.codex/memories` 里的 p-git-commit 使用记录、以及用户经常直接输入 `$p-git-commit`（八月有 6 个会话是显式 `$` 调用）。

> 注：曾出现"56/95 会话加载了 SKILL.md"的初步统计，经核查是 Codex skill 目录在 8 月 27 日后改版，catalog 行里出现 `(file: r0/p-git-commit/SKILL.md)` 造成的字符串误匹配，非真实调用，已剔除。

### 本地 Claude Code — 样本不足

八月本地 Claude Code 会话中只有 **1 次**真实 `git commit`：

- 2026-08-31T13:17（`other/temp/download_pdf`）：`feat(pdf-download): :sparkles: 改用 Edge CDP 主路径下载官网 PDF`。该会话调用了 `p-git-commit`（`skillcall=1`）。发生在 CLAUDE.md 约束生效（08-30）之后。

其余约 30 个提到 "git commit" 的 8 月 Claude 会话，全部是 available-skills 列表里 p-git-commit 自身 description（"…创建 git commit message 时使用"）的字符串，不是真实提交。本地的提交几乎都由 Codex / Hermes 完成，Claude Code 在此机器上不承担提交职责，故无法评价其漏用。

### Hermes — 存在漏用，但从未写入约束

`~/.hermes/skills/.usage.json`：`p-git-commit` `use_count=34`、`view_count=16`，2026-08-02 起活跃，最后使用 2026-08-31。

`state.db` 八月数据：

- 执行过 `git commit` 的会话：**约 54 个**。
- 其中有会话内 p-git-commit 加载证据（`skill_view` 或内联 SKILL 内容）：**约 28 个（52%）**。
- 无加载证据：**约 26 个**。

按日分布（提交会话数 / 有加载证据数）：

```
08-02  2/1    08-03  9/3    08-04  7/2    08-05  4/3    08-06  3/0
08-07  4/4    08-09  1/1    08-10  3/2    08-11  4/2    08-12  1/1
08-20  6/3    08-21  2/1    08-28  1/0    08-29  1/0    08-30  3/3    08-31  3/2
```

漏用高度集中在 8 月 3—6 日、8 月 20 日、8 月底：手稿（PRB / npj 转换、LaTeX 排版）、Sphinx / mymetal 在线文档、Obsidian 仓库同步的批量提交，以及 `cron_*` 流水线（`utils-stage-*-runner`、`utils-website-upgrade-stage-runner`）。这些"漏用"里相当一部分是：

- 用户显式说"提交并推送 / git 提交 XXX"的琐碎 `docs:` / `chore:` 同步提交；
- cron 无人值守流水线自动提交；
- 由子 agent 执行提交——父会话的 `skill_view` 不会传播到子上下文，反之亦然（与 p-code-style 审计的发现一致）。

Hermes 侧从始至终没有把该约束写进 `SOUL.md`，只有一条 memory 记录 p-git-commit 的默认行为。所以严格说，Hermes 的这些是"隐式路由 + memory 提醒下的漏用"，不是"违反已写规则"。

## 与 p-code-style 审计的对比

| 维度 | p-code-style | p-git-commit |
|---|---|---|
| 八月本地系统提示词中是否有显式约束 | 无（`allow_implicit_invocation: true`，靠 description 语义路由） | 本地 8 月底才补：Codex 08-27、Claude 08-30；仓库项目级 07-30 反而删掉了 |
| 精简前是否已有漏用 | 有大量（Claude 本地 0/0/4、Codex 本地 5/3/7、Hermes 本地 32/1/50） | 本地 Codex 无（7/7 命中）；本地 Claude 样本=1（命中）；Hermes 约一半漏 |
| 用户"以前似乎都会调用"的印象 | 部分环境有事实基础，整体不成立 | 对 Codex 成立且很强；对 Hermes 只有一半 |
| 主要风险点 | 首次写自动化 / 脚本代码前不加载 | Hermes 的批量 / cron / 子 agent 提交不加载 |

结论上，`p-git-commit` 的情况比 `p-code-style` **好**：本地 Codex 在没有硬约束时就近乎 100% 调用，本地约束又已在 8 月底补齐。唯一真正的缺口在 Hermes，且 Hermes 从没被写入过这条约束。

## 建议

1. **给 Hermes 补约束**：在 `hermes/zcm6/SOUL.md`（及其它设备的 SOUL）加入与全局 `~/.codex/AGENTS.md` / `~/.claude/CLAUDE.md` 一致的一行——"生成 commit message / 执行 git commit 前使用 `p-git-commit` skill；委派子 agent 提交时同样适用"。这是本次审计发现的唯一实质缺口。
2. **cron / 无人值守流水线单独说明**：`utils-*-runner` 这类自动提交要么在其 runner skill 里显式走 p-git-commit 流程，要么明确豁免并说明原因，不要留在灰色地带。
3. **本地约束刚上线，需用新会话验证**：`~/.codex/AGENTS.md`（08-27）和 `~/.claude/CLAUDE.md`（08-30）的 Git Commit 段生效不久，9 月的样本才是有效观察窗口。
4. **仓库项目级 `AGENTS.md` 的取舍**：2026-07-30 删除"更新工作流"段时一并删掉了 `$p-git-commit` 提示。若希望在本仓库内提交也走 skill，可在 `## Skill 路由` 或"其他说明"里补一句，不必恢复整段工作流。
5. **持续审计按事件顺序**：区分"skill 已安装 / description 在启动上下文"、"正文被加载"、"首次 `git commit` 前加载"、"提交后才加载"、"始终未加载"；只搜 `p-git-commit` 字符串会把 available-skills 列表和 catalog 的 `(file: …/SKILL.md)` 误算成调用。

## 数据来源

- 仓库 Git 历史：`AGENTS.md`（`bbd382f` 加入、`4771680` 删除）、`codex/AGENTS_zcm6.md`（`58f9c14`）、`hermes/zcm6/SOUL.md` 全历史。
- 本地 `~/.claude/CLAUDE.md`、`~/.codex/AGENTS.md`（mtime + 会话内嵌系统提示词快照）。
- 本地 `~/.claude/projects/**/*.jsonl`（8 月 Claude Code 会话）。
- 本地 `~/.codex/sessions/2026/08/**/*.jsonl`（95 个 8 月 Codex 会话，含 `<INSTRUCTIONS>` 快照）。
- 本地 `~/.hermes/state.db`（`messages` / `sessions` 表）与 `~/.hermes/skills/.usage.json`。
- 对照报告：`ai-guide/reports/20260901-codex-p-code-style-invocation-audit.md`。
