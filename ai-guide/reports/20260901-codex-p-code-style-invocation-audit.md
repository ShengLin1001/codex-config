# p-code-style 八月隐式调用审计

## 结论

`p-code-style` 在 description 精简前就已经存在漏调用和调用过晚，因而不能把近期代码风格偏离直接归因于 description 精简。

更关键的是：仓库源码虽然已经换成短 description，但本地和 zcm6 当前安装的副本、以及受查会话中的 skill 快照仍是旧的长 description。因此，本次分界后的样本并没有真正暴露于短 description，不能构成有效的前后 A/B 测试。

用户关于“以前写代码前似乎都会调用”的印象在部分环境中有事实基础：zcm6 Codex 的八月相关小样本为 2/2 提前调用，Hermes 本地也累计调用了 44 次。但从 Claude Code、本地 Codex 和 Hermes 的完整日志看，精简前已有大量反例。

## 审计范围

- 时间范围：2026-08-01 00:00 至 2026-09-01 00:00 UTC。
- 边界补查：额外检查 2026-09-01 00:00–07:00 UTC，避免遗漏本机 PDT 8 月 31 日晚间事件；没有发现需要加入主表的新代码写入事件。
- Agent：Claude Code、Codex、Hermes。
- 环境：本地 Windows、SSH 主机 zcm6。
- 目标 skill：`p-code-style`。
- 审计为只读操作；没有修改任何 agent 配置或 skill。

## 分界点

description 在提交 `fab0b9ab03d919b0eccf9946c3a1701fd1ec2d99` 中被精简：

- 本地时间：2026-08-30 22:19:34 PDT。
- UTC：2026-08-31 05:19:34。
- 提交：`refactor(skills): :truck: 重构 skill 目录为 skills-using 分层布局`。

修改前：

> PJ 写工作流 / 自动化 / 脚本生成类代码时的固定风格约束。当为 PJ 编写或重构这类代码时使用：Python/Bash 脚本、用 Python 拼接生成 bash、批量遍历目录、Slurm/HPC 作业与提交引擎、argparse/CLI 工具、科研计算工作流或 mymetal 风格的通用函数。规则已从 PJ 满意的代码中提炼并内联于此，开箱即用，无需另读大量文件。

修改后：

> 按 PJ 规范编写科研工作流、自动化脚本和 CLI。

## 统计口径

状态定义：

- **提前调用**：在该 agent 上下文第一次实际修改相关代码前，已加载 `p-code-style` 正文。
- **调用过晚**：先修改相关代码，之后才加载 skill。
- **未调用**：该代码写入上下文从未加载 skill。

实际调用证据按 agent 区分：

- Claude Code：会话中的真实 `Skill` 调用记录。
- Codex：会话中真实读取 `p-code-style/SKILL.md` 的工具调用。
- Hermes：SQLite 会话库中的成功 `skill_view(name="p-code-style")`。

代码写入证据包括 `Write`、`Edit`、`apply_patch`、`write_file`、`patch`，以及能明确识别写入 Python、Bash、PowerShell、Slurm/CLI 工作流文件的 shell 命令。Markdown 报告写入和纯读取操作不计入。

Claude Code 的 Bash 写入形式较多，主表采用人工复核、去重后的高置信持续性任务；Codex 和 Hermes 主要按实际写代码的 agent 会话统计。因此各行适合判断各自漏调用情况，但不应把所有行机械相加后计算统一成功率。

## 审计结果

表中顺序为“提前调用 / 调用过晚 / 未调用”。

| Agent | 环境 | description 修改前 | 修改后 | 结论 |
|---|---|---:|---:|---|
| Claude Code | 本地 | **0 / 0 / 4** | **0 / 1 / 1** | 修改前已有明确漏调用；修改后两个样本均未提前调用 |
| Claude Code | zcm6 | **5 / 0 / 5** | 无八月样本 | 修改前约一半任务正确触发，不是稳定默认调用 |
| Codex | 本地 | **5 / 3 / 7** | 无样本 | 修改前已同时存在过晚和完全漏调用 |
| Codex | zcm6 | **2 / 0 / 0** | 无样本 | 小样本中全部提前调用，符合用户印象 |
| Hermes | 本地 | **32 / 1 / 50** | **0 / 0 / 2** | 调用频繁，但逐写代码上下文看仍有大量漏调用 |
| Hermes | zcm6 | **1 / 0 / 4** | 无样本 | 修改前已存在明显漏调用 |

修改后主表实际只有 4 个本地写代码样本：Claude Code 2 个、Hermes 2 个；结果为 0 次提前调用、1 次过晚、3 次未调用。该窗口很短，且这些会话仍看到旧长 description，不能据此评价新短 description 的因果效果。

## 代表性漏调用

### Claude Code 本地

修改前已出现以下持续性自动化代码任务未调用：

- Obsidian `_scripts/check_links.py`。
- Obsidian `_scripts/sync_sources.py`。
- MathType 监控自动化脚本。
- Fluent `.claude/hooks/update-db.py`。

修改后：

- 一个 PDF 自动化任务先写代码、后调用 skill，属于调用过晚。
- 一个 Word 转换自动化任务始终未调用。

### Claude Code zcm6

修改前正确提前调用的任务包括 GSFE 工作流、初版 `sbatch_retry`、清理脚本和 stage2 MD 工作流；明确漏调用的任务包括后续 `sbatch_retry` 修改、绘图工作流、Slurm 修复和 n2p2 工作流。

触发本次调查的最新 zcm6 Claude 会话发生在八月 UTC 窗口之后：第一次代码编辑早于 `Skill` 调用，仍可独立确认是一次调用过晚，但未计入主表。

### Codex 本地

修改前未调用或过晚的代表任务包括：

- `daily-activate.ps1`。
- `browser_direct.py`。
- `pdf_download.py`。
- `scripts/pei_ai_univ_reinstall` 和相关同步脚本。

### Hermes 本地与 zcm6

本地 Hermes 的 `.usage.json` 显示八月 `p-code-style` 累计使用 44 次，zcm6 为 9 次。这说明 skill 并非没有被发现，而是调用不稳定。

代表性漏调用包括：

- 本地 `pei_ai_univ_reinstall`、Word/PDF 自动化、`publisher_strategies.py`、`workflow_md.py`。
- zcm6 `sync-hermes-device.sh` 和多个 `glm_extrapolation_grade.py` 子任务。

Hermes 中相当一部分代码由子 agent 写入。父会话调用 skill 不代表子会话自动继承；审计必须以实际写代码的子上下文为单位。

## 安装状态与因果判断

当前存在明确的源码/安装副本漂移：

| 位置 | 当前 description |
|---|---|
| 仓库 `skills-using/root/p-code-style/SKILL.md` | 新的短 description |
| 本地 `~/.agents/skills/p-code-style/SKILL.md` | 旧的长 description |
| 本地 `~/.claude/skills/p-code-style` 指向的安装副本 | 旧的长 description |
| 本地 Hermes 会话中的 skill 内容 | 旧的长 description |
| zcm6 已安装副本及受查会话快照 | 旧的长 description |

因此：

1. 当前观察到的漏调用不能由短 description 直接造成。
2. 漏调用和过晚调用在精简前已经存在。
3. 短 description 尚未真正上线；下次用户级重装后才会影响新会话。
4. 已运行会话通常保留启动时的 skill 清单和 description；仅修改仓库源文件不会刷新会话。

## 为什么“允许隐式调用”仍会漏掉

`allow_implicit_invocation: true` 只表示允许模型自主选择该 skill，不表示建立了“首次写代码前必须执行”的硬钩子。

通常启动上下文只提供 skill 名称和 description；正文需要 agent 真正发起 `Skill`、`skill_view` 或读取 `SKILL.md` 才加载。description 是语义路由提示，任务表述、上下文长度、可用 skill 数量、子 agent 边界和模型判断都会影响是否选择它。

Claude Code 官方文档也把 description 作为触发匹配依据，并在 skill 不触发时建议让 description 更具体：

- <https://code.claude.com/docs/en/skills#skill-not-triggering>
- <https://code.claude.com/docs/en/skills#frontmatter-reference>

OpenAI 当前 Responses schema 对本地 skill 使用 `name`、`description` 和 `path` 表示能力元数据，也没有把 description 定义为强制的 pre-write hook：

- <https://developers.openai.com/api/reference/cli/resources/beta/subresources/responses>

## 用户印象的来源

“以前似乎总会调用”并非凭空产生：

- zcm6 Codex 的八月相关样本确实为 2/2 提前调用。
- Hermes 本地和 zcm6 分别累计调用 44 次和 9 次，成功调用在对话中非常显眼。
- 成功调用时 agent 往往主动说明“先加载代码风格约束”；漏调用则没有对应提示，通常要等代码风格出问题才会被发现。

但把所有 agent 和环境合并后，精简前已有大量漏调用，无法支持“以前总会默认调用”的全局判断。

## 建议

### 1. 恢复具体 description

短 description 丢失了 Python、Bash、Slurm/HPC、argparse、批量目录、mymetal 等高辨识度关键词。虽然它不是本批问题的直接原因，但在下一次重装后很可能降低语义召回。

建议恢复原长 description，或保留更紧凑但仍覆盖关键触发词的版本。

### 2. 增加硬路由规则

如果目标是“任何相关代码首次写入前都必须调用”，不能只依靠隐式 description。应在全局 `AGENTS.md` 和 Claude 的全局规则中加入类似要求：

> 首次创建或修改 Python、Bash、PowerShell、Slurm/HPC、科研工作流或 CLI 代码前，必须先加载 `p-code-style`；委派给子 agent 时同样适用。

### 3. 重装后用新会话验证

仓库源修改不会自动更新已安装副本和运行中会话。变更后应：

1. 通过本仓库 `skills-using/` 的统一安装脚本重新安装。
2. 核对本地和 zcm6 实际安装文件的 description。
3. 关闭旧会话并启动新会话。
4. 使用同一组 Python/Bash/Slurm/CLI 提示做可重复验证。

### 4. 持续审计采用事件顺序

后续检查应继续区分：

- skill 已安装或 description 出现在启动上下文；
- skill 正文被实际加载；
- skill 在首次代码写入前加载；
- skill 在写入后才加载；
- skill 始终未加载。

仅搜索 `p-code-style` 字符串会把启动时的 description、skill 列表和讨论文本误算成真实调用。

## 数据来源

- 仓库 Git 历史及 `p-code-style` 源文件。
- 本地 `~/.claude/projects/` Claude Code JSONL 会话。
- 本地 `~/.codex/sessions/2026/08/` Codex JSONL 会话。
- 本地 `~/.hermes/state.db` 和 `~/.hermes/skills/.usage.json`。
- zcm6 对应的 Claude、Codex、Hermes 会话目录及 Hermes SQLite 数据库。

