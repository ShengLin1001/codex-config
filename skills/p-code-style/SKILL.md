---
name: p-code-style
description: PJ（用户）写工作流 / 自动化 / 脚本生成类代码时的风格与工程约束。当为 PJ 编写或重构这类代码时使用：用 Python/Bash 生成并提交脚本（Slurm/HPC 作业、批量提交引擎）、遍历目录批处理、用 Python 拼接生成 bash、argparse/CLI 工具、科研计算工作流（VASP/LAMMPS/n2p2，或 mymetal package 风格的通用函数）。目的：让初版代码就贴近 PJ 手写标准，避免反复返工。证据基准是 PJ 亲手重写的 gold standard 与 mymetal package。
---

# P Code Style

## 概述

这是一份**写代码前必须遵守的约束**，不是事后审查清单。它从一次真实事件中提炼：
Claude 改写一个"同一任务批量提交"的 Slurm 引擎（bash + python），初版严重不合格，
PJ 亲手重写成满意版本。本 skill 把那次"初版 → 终版"的差距固化为规则，使 Claude
下次第一版就接近 PJ 的标准。

适用范围是**通用的**——任何工作流 / 自动化 / 脚本生成类代码都适用；Slurm 提交脚本只是
最初的例子，不是边界。

## 何时使用

- 写或重构 Python/Bash 脚本，尤其是**用 Python 生成另一段 shell/Slurm 脚本**。
- 批量遍历目录做计算 / 提交 / 后处理（HPC、VASP/LAMMPS/n2p2 工作流）。
- 写 argparse/CLI 工具、作业提交引擎、收敛检查、结果汇总。
- 往 mymetal package 或类似科研代码库里加通用函数。
- 被要求"简化""重构""精简"已有脚本时——先读规则 3、4，别误删输出。

## 先读：为什么"默认 LLM 代码"会被 PJ 返工（根因复盘）

不要重复这些根因。它们是行为习惯层面的，不是单个 bug：

1. **一坨大函数**：把所有逻辑塞进一个函数。PJ 要的是小而专的 `generate_*` / `check_*` /
   `get_*` / `split_*` 拆分（见 gold standard 的 `generate_script_header` /
   `generate_launcher_command` / `generate_loop` / `get_lsubdir` / `split_chunks`）。
2. **用 f-string 生成 bash**：导致 `${...}` / `$((...))` 的花括号与 f-string 冲突，
   被迫到处转义 / 双写花括号。PJ 刻意用**普通字符串拼接**写 bash，只在注入 Python 值处用 `+`。
3. **分不清"检查"和"输出"**：被要求"精简"时把 emoji 回显 / 逐文件打勾 / summary 也删了。
   这些是 PJ 要保留的人类可读进度；该删的是**冗余校验逻辑**。
4. **过度校验 / 校验错位**：堆一堆无关紧要的格式检查；或把本该在 `cmd` 里做的内容检查
   提前到 Python 里做。
5. **路径随意**：用相对路径、不 `chdir` 回根、不校验绝对路径。
6. **自创约定**：自己发明退出码语义、改下游契约（PJ 尊重既有约定，如退出码 0/10 = 已收敛、
   `pei_vasp_univ_sbatch` 的行为）。
7. **注释只说"做了什么"**：复述代码。PJ 的注释解释**为什么**、写明取舍与坑（常双语）。
8. **配置散落**：magic string 到处写。PJ 把枚举 / 配置集中成默认参数字典
   （`MODULE_BLOCKS` / `MODES` / `LAUNCHERS`）。
9. **不诚实**：没验证就宣称完成；用 mock / 占位糊弄而不留显式 TODO。

## 核心约束

每条 = 命令式原则 + 证据 + 在非 Slurm 场景如何套用。

### 1. 小而专的函数，动词命名

把流程拆成单一职责的小函数，用 `generate_* / get_* / check_* / split_*` 这类动词前缀命名。
主函数只做编排（check → prepare → main control flow）。
- 证据：`test.py` 的 `generate_script_header`、`generate_loop`、`get_lsubdir`、`split_chunks`；
  mymetal `check/atoms.py::get_cna_count`。
- 泛化：任何脚本都先想"能拆成哪几个可独立测试的小步骤"，而不是一条龙写到底。

### 2. 用 Python 生成 shell：拼接，不要 f-string

生成 bash/Slurm 文本时用普通字符串拼接（`(... "\n" ...)`），**只在注入 Python 变量处用 `+`**，
并写一行注释说明"避免 `${}` / `$(())` 花括号被 f-string 吃掉"。注入路径 / 列表前转成 `str`。
- 证据：`test.py::generate_loop` 顶部注释与整段拼接写法；`subdirs = " ".join(group)`。
- 泛化：任何"代码生成代码"（生成 YAML、Dockerfile、另一段 Python）都优先拼接 + 局部注入，
  别让宿主语言的插值语法和目标语言打架。

### 3. 严格区分"输出"与"检查"

**输出**（emoji 状态回显、逐文件 ✅/❌、preflight 信息块、最终 summary）是刻意保留的，
用来快速确认与定位问题——**永远不要以"精简"为由删除**。要精简就删**冗余校验**
（重复的 `command -v` + `[[ -x ]]`、"多余参数"告警、复制粘贴的检查），靠抽公共函数 / 合并来减行数。
- 证据：memory `simplify-distinguish-output-from-checks`；`test.py` 的 summary 块、
  `not_convergenced_dirs` 逐个列出。
- 泛化：任何"简化/重构"请求都先分清两者，先问/先判断哪些是输出哪些是检查，再动手。

### 4. 只做要紧的检查，内容检查下推

入口处校验**结构性前提**：None、正整数、绝对路径、枚举合法性、目录存在。把**业务内容检查**
（文件里有没有某字符串、是否收敛）放到运行时的 `cmd` / 下游脚本里，不要提前在编排层做。
- 证据：`test.py` 顶部的 `check_none` 批量校验、`check_positive_int`、`check_absolute_path`、
  `mode not in MODES`；注释"不使用 check_file_contain 参数，这是在 cmd 里应该执行的"。
- 泛化：编排层只保证"能跑起来的前提成立"，不替下游判断业务结果。

### 5. 绝对路径纪律

`path_root` 之类的根必须是绝对路径并校验（`check_absolute_path`）；进入子目录处理前后
用 `os.chdir(start_dir)` 回到根再继续，保证每个子任务起点一致。生成脚本里同样
`cd "$start_dir"` 兜底。
- 证据：`test.py::get_lsubdir` 的绝对路径检查、`os.chdir(path_root)`、循环里 `cd "$start_dir"`；
  mymetal `check/convergence.py` 每轮 `os.chdir(path_cwd)` "for safety, always return"。
- 泛化：任何会 `cd` / 改工作目录的代码，都要有"回到已知起点"的不变量。

### 6. 配置与枚举集中化

把环境/模块块、合法枚举集中成**带默认值的参数字典/列表**（`MODULE_BLOCKS`、`MODES`、
`LAUNCHERS`），不要把魔法字符串散布在逻辑里。新增一类只改这一处。
- 证据：`test.py::pei_slurm_univ_submit` 签名里的 `MODULE_BLOCKS` / `LAUNCHERS` / `MODES` 默认参数。
- 泛化：任何"有几种模式/几种环境"的代码，都先建一张集中表，逻辑里只查表。

### 7. 注释解释"为什么"，必要处双语

注释写清取舍、坑、约定来源——不是复述代码。涉及 shell 引号 / word splitting /
变量展开时机这类易错点，写足背景（PJ 常用中文讲原理，关键处中英并存）。
- 证据：`test.py::generate_launcher_command` 关于单/双引号与 `$SLURM_NTASKS` 展开时机的长注释；
  `zcm6-lammps` 块里诚实的 `TODO ... intentionally left blank`。
- 泛化：每写一处"看起来怪但有意为之"的代码，都补一句为什么这么写。

### 8. 错误处理与退出码约定

用统一的小助手：`fail(msg)` 打印 `❌ ERROR` 并 `raise SystemExit(1)`；`warn(msg)` 打印 `⚠️`。
check 函数**通过则返回值、失败则 `fail()`**——调用处要**接住返回值**（如
`chunks = check_positive_int(chunks, ...)` 把字符串强转 int）。生成脚本里用退出码表达结果，
并在 summary 后按结果 `exit 0/1`。
- 证据：`test.py` 顶部 `fail/warn`、`check_positive_int` 的"必须接住返回值"注释、
  summary 末尾 `exit 1`。
- 泛化：错误要么早失败（fail），要么进 summary 被逐个列出；不要静默吞掉。

### 9. 尊重下游约定，不自创语义

沿用既有契约，不要发明自己的。例：退出码 `0` 或 `10` = 已收敛（`pei_vasp_univ_sbatch` 约定）；
bash/python 双引擎必须生成**字节级一致**的脚本。
- 证据：`test.py` 的 `(( status == 0 || status == 10 ))` 注释；memory `slurm-submit-dual-engine`
  （改一个引擎必须镜像改另一个，用 `--dry-run --show-script` diff 验证一致）。
- 泛化：动既有系统前先找它的约定（退出码、目录命名、文件契约），延续它。

### 10. 诚实：TODO 要显式，"完成"要验证

不确定 / 无法确定的地方留**显式 TODO**并说明，不要假装填好。改完不要凭"本地能跑"就宣称完成——
按下游真实环境验证；在 PJ 的工作目录里跑命令前，先确认该 flag/模式真的支持
（如 single-alloc 没有 `--dry-run`，误传会触发真实运行）。
- 证据：`test.py` 的 `zcm6-lammps` TODO 块；memory `simplify-distinguish-output-from-checks`
  与 `slurm-submit-dual-engine` 的验证要求。
- 泛化：分清"我验证过"和"我以为"；没验证就说没验证。

### 11. 输出风格：固定 emoji 词汇 + 结构化 summary

沿用 PJ 的 emoji 词汇：📁 目录 / ▶️ 即将执行 / 📍 当前位置 / ✅ 成功·收敛 / ❌ 失败·未收敛 /
⚠️ 警告 / 📊 summary / 🎉 全部完成。结尾给 summary：各计数 + 逐个列出失败/未收敛的目录。
分隔用 `================ <emoji> <内容>`。
- 证据：`test.py::generate_loop` 与 parallel 分支的 summary；mymetal `check/convergence.py` 的 ✅/❌。
- 泛化：批处理类脚本都给"逐项进度 + 末尾汇总"，让人一眼知道哪几个出了问题。

### 12. 自带测试入口

文件底部放几组 `test_args*` 字典覆盖典型场景，用注释切换调用，方便手动验证多种模式。
mymetal 风格的库函数则配模块级 docstring（开头列 `Functions:`）+ Google 风格 `Args/Returns`。
- 证据：`test.py` 末尾 `test_args1/2/3` + 注释掉的调用；mymetal 各文件顶部 docstring。
- 泛化：交付脚本时附带"怎么自测"的入口，别让 PJ 自己拼调用。

## 动手前自检（写之前过一遍）

- [ ] 能拆成哪些小函数？主函数是否只做编排（check → prepare → main）？
- [ ] 要生成 shell 吗？→ 用拼接而非 f-string，规划好哪里 `+` 注入 Python 值。
- [ ] 有几种模式/环境？→ 先建集中配置表（dict/list 默认参数）。
- [ ] 入口要校验哪些**结构性前提**？内容检查是否该下推到 cmd？
- [ ] 有没有既有下游约定（退出码、目录命名、文件契约）要沿用？

## 交付前自检（提交/汇报之前过一遍）

- [ ] 没有把 emoji 回显 / 逐文件状态 / summary 当"格式检查"删掉。
- [ ] 路径都是绝对路径并校验；每轮回到已知起点。
- [ ] check 函数失败 `fail()`、成功返回值且调用处接住了。
- [ ] 易错处（shell 引号、展开时机、特意为之的写法）都有"为什么"注释。
- [ ] 不确定处留了显式 TODO；声称"完成"的部分是真验证过的（且 flag 确实支持）。
- [ ] 有 emoji 词汇一致的进度输出 + 结构化 summary + 正确 exit code。
- [ ] 附带了测试入口 / 文档 docstring。

## 证据来源（核对后再复用，可能已演进）

- Gold standard（PJ 手写、令其满意）：`/public3/home/scg6928/mywork/test-sbatch/y_E_in_1_2_bulk/test.py`
- 已落仓同源引擎：`slurm_utils/slurm_universal/pei_slurm_univ_submit`(+`.py`)、
  `test_pei_slurm_univ_submit.py`；用 `git log` 看其重构历史。
- 风格样本库：`mymetal/`（`universal/check`、`universal/print`、`post/`、`io/` 等）。
- 项目 memory：`.../memory/simplify-distinguish-output-from-checks.md`、`slurm-submit-dual-engine.md`。
