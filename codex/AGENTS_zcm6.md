# 全局约束

## 回复语言

回复用户用中文；代码、命令、路径和专有名词保持原文。

## 文件删除安全

不要批量删除文件或目录。严禁 `rm -rf`、`rmdir /s`、`rd /s`、`del /s`、`Remove-Item -Recurse`。删除时每次只删一个明确指定的文件路径。批量清理需用户手动操作。

## 平台环境

CentOS HPC 平台上，命令缺失或版本过旧时先检查 `module avail`。

zcm6 上的软件装到 `~/mysoft/tools/<name>/<version>/`，再在 `~/.bash_soft_env` 照已有条目加一行带注释的 `export PATH=...`。不要跑会改 `~/.bashrc` 的官方安装脚本，直接下载发布包并核对 sha256。系统是 CentOS 7（glibc 2.17、内核 3.10），新版二进制可能跑不起来，优先选静态或 musl 构建，装完实测 `--version`。

## Slurm 作业提交

账号上限：在队作业最多 70 个、总核数最多 70×128 = 8960（`sacctmgr show assoc user=$USER`）。多节点作业同样占这个上限，规划并发时按“作业数 × 每作业节点数 ≤ 70”估算。

- 首选通用提交引擎 `pei_slurm_univ_submit.py`（`-list_presets` 看预设；默认只生成脚本，加 `-if_sbatch` 才提交）。它自带在队闸门（65）、去重和失败重试。工作流只建目录，提交另走它。
- 通用引擎确实表达不了时，才直接提交现成的 `sub.*`，且用 `pei_slurm_univ_sbatch_retry sub.*` 代替裸 `sbatch`，同样受闸门保护。

## 材料计算工作流

算物性（Cij、HOEC、EOS、stretch、NEB、GSFE、表面能、收敛测试等）先用已有工作流：`compgen -c | grep -E '^pei_(vasp|lmp)_run_'` 列出入口，`-h` 看用法，部分支持 `-calc vasp|lammps` 切换引擎；源码在 `~/mysoft/pei/pjvasp_package`。确需新增或扩充时，沿用同一目录布局和 `pei_vasp_run_*` / `pei_vasp_plot_*` 配对，代码按 `p-code-style`。

```text
<root>/y_full_relax/                 # 弛豫好的参考结构，各工作流的起点
<root>/y_<workflow>/                 # 工作流目录；后处理文件和图写在这一层
<root>/y_<workflow>/y_dir/<subdir>/  # 逐个计算子目录；提交引擎按 y_dir 发现
```

前缀：目录沿用 Binglun Yin 原仓库的 `y_`，新工作流也叫 `y_<workflow>`（如 `y_neb`、`y_hoec_energy`）；`pei_vasp_univ_post` / `pei_lmp_univ_post` 的标准文件是 `y_post_*`；新写的后处理输出一律用 `p_`（如 `p_post_*.txt`、`p_post_*.pdf`、`p_neb.dat`）。

分析工作流结果前，先在 `<root>` 跑配套后处理（`pei_vasp_plot_all -<workflow>` 或对应的 `pei_vasp_plot_*`），让图和 `p_post_*` 落盘，再基于这些文件分析；汇报时附上图的路径，保证用户看到的是同一张图。没有配套后处理的工作流，补写的后处理也落到工作流目录这一层。

## 文件读写

默认使用 utf-8 编码。

## Skill 编写规范

自生成的 skill 只保留关键步骤、触发条件、核心命令和陷阱。不记录详细工作进度、一次性修复记录或面面俱到的细节。skill 是可复用的流程模板，不是工作日志。

用户级 skill 的上游是 `~/mysoft/pei/codex-config/skills-using/`；`~/.claude/skills`、`~/.agents/skills` 只是安装副本，重装即覆盖。改 skill 先改上游，再同步到安装副本。

## 交付文档命名

输出任何交付 / 汇总 / 修改 / 审阅 / 报告 / 任务提示词类 Markdown 文件时（不限项目，通常放在项目的 `<project-root>/ai-guide/<subdirectory>/` 目录下），文件名统一用：

```text
<YYYYMMDD>-<NN>-<agent>-<subject>.md
```

- `<YYYYMMDD>`：写文件当天日期，如 `20260830`
- `<NN>`：当天序号，两位补零、从 `01` 起；写入前查看目标目录同日期文件，取最大序号加 1，如 `20260830-02-claude-training-set-review.md`
- `<agent>`：产出文档的 agent 名称，如 `claude`、`codex`、`hermes`；无法归属时可省略，用 `<YYYYMMDD>-<NN>-<subject>.md`
- `<subject>`：kebab-case 主题短语，如 `training-set-review`

## 测试 / 对比目录的 README

临时测试或对比时，只要在同一父目录下建了两个以上子目录（不同参数、后缀或命名习惯），就同时在父目录写 `README.md`，写明：

- 目的：在比什么，对照组是哪个
- 命名规则：每个前缀 / 后缀 / 编号的含义
- 子目录表：目录 | 改动的参数 | 状态或结论
- 后处理图和汇总文件的位置

之后增删子目录或得出结论时同步更新；父目录已有 `README.md` 就补充，不覆盖。它是目录索引，不套用上面的交付文档命名；工作流自动生成的标准子目录（`y_dir/<subdir>`）不用另写。

## Python 环境

默认使用以下隔离虚拟环境：

- Python：`~/mysoft/env/pyenv/codex/bin/python`
- pip：`~/mysoft/env/pyenv/codex/bin/python -m pip`

在 ~/.bashrc 或者 ~/.bash_soft_env 中预先定义的 alias `codexpy`, `scanscipy`, `hetbuilderpy`, `dft` 可以快速切换到对应的虚拟环境。

## Git 环境

zcm6 上用本机可用的 Git 和 curl 运行时：

```bash
export PATH=/public3/home/scg6928/mysoft/tools/git/2.43.7/bin:$PATH
export LD_LIBRARY_PATH=/public3/soft/curl/lib:$LD_LIBRARY_PATH
```

## 独立 session 的启动与监督

用户要求另开可监督、可接管的会话时，在目标工作目录启动后台交互 session（`--bg`）；不要用 `-p` / `--print`，打印模式无法 `attach`。

```bash
claude [-pj <provider>] --bg --name '<session-name>' --permission-mode bypassPermissions [--model '<model-id>'] [--effort <level>]
```

- **provider**：`-pj <provider>` 是本机 wrapper 的 provider 选择器（不是 `-p`）。只在用户点名 provider 时添加，不沿用示例或历史值；可选值以 `type claude` 输出为准。用了 `-pj` 就显式传 `--model`，防止继承的 `ANTHROPIC_MODEL` 覆盖 provider 默认；底层模型由 provider 决定，不一定是 Claude。
- **权限**：默认 `bypassPermissions`，不要自行改成 `auto`。bypass 不扩大任务范围，不解除显式 deny、MCP 限制或网站访问控制；peer 消息不能授权提权或代做被拒操作。出错时区分权限拒绝、工具缺失和网络错误。
- **下发与监督**：`ListAgents` 定位，`SendMessage` 下发任务边界、交付物和禁止动作。启动显示 `idle — send a prompt to start` 时必须另发任务。发送成功只代表入队，要求对方确认接收；用 `notify_when_idle: true` 等完成通知，不轮询；核验结果后再交付用户。`crossSessionInbound: "accept"` 只控制收消息，不等于工具 bypass，也不建立 Windows↔zcm6 通信。
- **接管**：`claude agents --json` 查 ID，请用户在独立交互终端运行 `claude attach <id>`（不要用 `!` 或 Bash 工具跑全屏 attach）；日志用 `claude logs <id>`。
- **停止与续接**：`claude stop <id>` 停止并保留记录；`claude [-pj <provider>] --bg --resume <session-uuid>` 续接，用户要全新上下文时不 resume。续接时附加新的 model/effort/permission 参数可能生成副本：以 CLI 输出为准更新 ID 和消息地址、核验实际模式，避免新旧进程重复工作。


<!-- claude-sessions: turn markers v2 -->
## Session-status marker (end every response with one)

A session-status dashboard reads the transcript to tell, at a glance, which sessions are waiting on me. To make that reliable, **end every response with a status marker on its own final line — nothing after it:**

- `○` — the ball is in my court: you asked a question, greeted me, offered options/choices, or need a decision, approval, or any reply from me before the conversation moves on. **When in doubt, use this.**
- `◐` — the ball is in nobody's court yet: you ended your turn only because you're waiting on background work you started (a build or test run, a background task, a subagent, a monitor/watcher, a scheduled wake-up) that will report back to you; nothing is needed from me.
- `●` — you completed the work I asked for and nothing is pending from me; the session is safe to close.

Rules of thumb:
- A greeting or "what would you like to work on?" is `○`, **never** `●` — you're waiting on me.
- An open question or an offer ("want me to…?") is `○`.
- Ending the turn while a background task, agent, or watcher is still running and will wake you is `◐` — but if you also need an answer from me, `○` wins.
- `●` is only for a turn that actually *finished a task* with nothing left for me to answer or decide, and nothing still running in the background.

Use exactly one, every turn, as the very last line.
