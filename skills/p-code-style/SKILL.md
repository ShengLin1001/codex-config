---
name: p-code-style
description: PJ 写工作流 / 自动化 / 脚本生成类代码时的固定风格约束。当为 PJ 编写或重构这类代码时使用：Python/Bash 脚本、用 Python 拼接生成 bash、批量遍历目录、Slurm/HPC 作业与提交引擎、argparse/CLI 工具、科研计算工作流或 mymetal 风格的通用函数。规则已从 PJ 满意的代码中提炼并内联于此，开箱即用，无需另读大量文件。
---

# P Code Style

写工作流 / 自动化 / 脚本生成类代码时，**初版就按下面写**，别等 PJ 返工。
这是从 PJ 手写的合格代码里提炼出的硬约束，已内联，直接遵守即可。

**按改动规模裁剪**：小修一处只取适用条款（如路径纪律、检查 vs 输出、注释写"为什么"），
跳过 `test_args`、`check → prepare → main` 分段等"从零写脚本"才需要的仪式；
新建文件或大改时才走全套。别给小改动套重流程。

## 最常见的返工点（别犯）

一坨大函数 · 用 f-string 拼 bash · "精简"时删掉 emoji/逐项/summary 输出 ·
在编排层提前做业务内容检查 · 相对路径 / 不回根目录 · 自创退出码或约定 ·
注释只复述代码 · magic string 散落 · 没验证就说"完成" ·
CLI 开关用 `--` / 连字符 / 留短别名 · 改开关取值却漏同步库比较·枚举表·tests·docs·跨脚本调用 ·
Slurm 调用（sbatch/squeue/srun/mpirun）不加轮询重试 / 重试时把已提交作业重投。

## 约束

**结构**
- 单一职责的小函数，动词前缀：`generate_* / get_* / check_* / split_*`。
- 主函数只做编排：`check → prepare → main`，用 `###` 注释分段、配 "to here" 收尾。

**mymetal / VASP 工作流边界**
- 先检索并复用 `mymetal` 现有逻辑；生成核心放 `mymetal/build/workflow/<name>.py`，后处理的数据读取与分析放 `mymetal/post/<name>.py`，`vasp_utils/.../pei_*` 只保留薄 Python CLI。
- **`mymetal` 库模块 import-only**：内部**不得**出现 `argparse` / `build_parser()` / `main()` / `if __name__ == "__main__"`。库只暴露 `generate_*` / `post_*` 这类可复用函数（参数是已解析好的 `Path` / list / dict），失败走 `fail()`。
- **CLI 概念全部落在 `pei_*` 可执行脚本**：argparse（含 `type=` 解析器如 `parse_pair`、"KPAR:NCORE" 这类字符串→元组）、参数回显、cwd 名 / `--dir` 归一、`sys.stdout.reconfigure(line_buffering=True)` 之类的输出编排，最后直接调库函数——模块级顺序写，别再包一层 `main()`。写新入口先照抄同域已有 workflow（如 `hoec_energy` 的 `pei_vasp_run_/plot_` 对）的这套拆分。
- "薄 CLI" 指**不含业务逻辑**，**不是** `from lib import main; main()`：把 argparse/main 留在库里、CLI 只转发，正是要避免的反模式。
- 新增工作流及后处理入口都用 Python；不要用 Bash 包 Python，也不要硬编码解释器、仓库或 package 路径。先激活 `dft` / `codexpy` 等目标 venv，入口通过 `#!/usr/bin/env python3` 使用当前环境，并实际验证解析到的 Python。
- 后处理默认先运行 `pei_vasp_univ_post` 生成标准文件；大目录或重复绘图时提供并遵循现有 `-skip_univ_post` 契约，只复用已确认有效的 `y_post_*`。

**CLI 开关命名（单横杠 `-` + 下划线 `_`，别用 `--` / 连字符）**
- 所有 CLI 开关统一 **单横杠前缀 + 下划线分隔**，bash 与 argparse 一致：`-path_root`、`-if_sbatch`、`-skip_univ_post`、`-child_wall_time`。argparse 单横杠长选项的 dest 仍把 `-`→`_`，`args.path_root` 照常；把长名放第一个（`add_argument("-input", ...)`）以定住 dest。
- 只留长名，**不留短别名**：删掉 `-i`/`-o`，只留 `-input`/`-output`。
- **取值同样用下划线**（限我们自己的枚举）：`-mode single_alloc`、`-preset zcm6_vasp_0`、`-chunk_parent_layout per_chunk`。改一个取值就要连库里 `mode == "..."` 比较、`PRESETS`/枚举表、tests、docs、生成脚本文件名一起改，一处漏改就漂移。
- **例外——沿用命名空间原生分隔符，别盲目 `_`↔`-`**：当开关名或取值本身是下游/外部命名空间的键时。① INCAR tag（VASP 用 `_`，`pei_vasp_univ_find_and_change` 还会 `[A-Za-z0-9_/]` 校验、直接拒绝 `-`）；② 外部工具 flag 原样保留（git `--porcelain/--rebase`、pip `--no-deps/--user`、sphinx `--keep-going`、curl `--max-time`、`ls --color`）；③ Slurm walltime `2-00:00:00`、Slurm 自带 `--time/-p/-N/-n`；④ `-h/--help` 惯例保留 `--`（argparse 内置，bash 里也照此）。
- 库（`mymetal`）虽 import-only，但 warn/fail/docstring 里引用 CLI flag 要用改名后的拼写；一个 pei 脚本调另一个 pei CLI（如 monitor 调 `pei_vasp_univ_check_phase_transition -dir`、slurm-monitor 透传 `-skip_ljobid` 给 vasp-monitor）要同步改，否则跨脚本调用当场断。
- 批量替换用带边界的正则（`(?<![\w-])--name`），**别误伤**散文里的 en-dash 范围（`M21--M23`、`eta4--eta6`、`A--K`）、matplotlib 样式串（`'--k'`）、minified JS（`--n`）、以及上面那些外部 flag。

**变量命名（按类型加前缀，一眼看出类型）**
- list / 序列用 `l` 前缀，循环变量用单数：`for subdir in lsubdir:`（**不是** `for subdir in subdirs:`）。
- 路径一律用 `pathlib.Path`（不用裸字符串 / `os.path`），变量名 `path_*`：`path_root`、`path_out`。
- dict 用 `dict_*`：`dict_mode`、`dict_cfg`。其他类型同理按"`类型_含义`"命名，逻辑里查表也好认。
  ```python
  from pathlib import Path
  path_root = Path(root).resolve()                 # 路径 → path_*，且用 Path
  lsubdir   = [p for p in path_root.iterdir() if p.is_dir()]   # list → l 前缀
  for subdir in lsubdir:                            # 循环变量用单数
      ...
  dict_mode = {"fast": 1, "full": 2}               # dict → dict_*
  ```

**用 Python 生成 shell**
- 普通字符串拼接，**不用 f-string**；只在注入 Python 值处用 `+`，注入前转 `str`。
  ```python
  loop = 'for d in "${arr[@]}"; do\n    cd "' + str(root) + '"\ndone\n'   # 对
  # f"...{arr}...${HOME}..."  # 错：${}/$(()) 花括号与 f-string 打架，到处要转义
  ```
- 生成的脚本顶部加"自动生成、请勿手改、每次覆盖"注释。

**检查 vs 输出（最易踩）**
- 输出 = emoji 回显 / 逐文件 ✅❌ / preflight 信息 / 末尾 summary：**永远保留**。
- "精简/重构"只删**冗余校验**，靠抽公共函数 / 合并减行，绝不删可读输出。
- 入口只校验**结构性前提**（None、正整数、绝对路径、枚举合法、目录存在）；
  **业务内容检查**（grep 文件、是否收敛）下推到 `cmd` / 下游，别在编排层提前做。

**路径**
- 一律 `pathlib.Path`，变量名 `path_*`；用 `/` 拼接、`.resolve()` 取绝对，不用裸字符串 / `os.path`。
- 根路径必须绝对并校验；处理每个子目录前后 `chdir` 回到已知起点（生成脚本里也 `cd` 兜底）。

**配置**
- 模式 / 环境等枚举集中成带默认值的 `dict`/`list` 参数，逻辑里查表，不散写魔法字符串。

**错误处理**
- 统一小助手；check 通过返回值、失败即终止，调用处**接住返回值**（含类型强转）。
  ```python
  def fail(msg): print(f"❌ ERROR: {msg}"); raise SystemExit(1)
  def warn(msg): print(f"⚠️  {msg}")
  chunks = check_positive_int(chunks, "chunks")   # 必须接住，否则后续按 int 用会炸
  ```
- 批处理结尾给 summary：各计数 + 逐个列出失败 / 未收敛项 + 正确 `exit 0/1`。

**Slurm 调用轮询重试（sbatch / squeue / srun / mpirun）**
- 凡能**暂态失败**（slurmctld 繁忙 / 超时 / 通信抖动）的 Slurm 调用都必须轮询重试，默认 **99 次 × 10s**；次数 / 间隔走环境变量旋钮（`PEI_*_RETRY_MAX/_SLEEP`），别散写常量。按"失败代价"选三套机制：
  - **提交 `sbatch`** → 包 `pei_slurm_univ_sbatch_retry`。提交失败=没创建作业、不占分配 → 重试廉价安全，用**黑名单**（除 `Invalid partition`、脚本不存在等永久错误快速放弃外，一律重试）。
  - **启动 `srun` / `mpirun`** → 包 `pei_slurm_univ_launch_retry`。重试握着整个分配空转烧 walltime → 用**白名单**（只在命中启动失败特征串时重试）。
  - **查询 `squeue`** → 失败即重试，`returncode==0` 才采信 stdout；**绝不**把空输出当"队列为空"（会误判作业已离队）。在 `$(...)` 里被调用时诊断一律走 **stderr**，否则污染捕获结果。
- **铁律：区分"提交 / 查询成功" vs "作业跑起来后才失败"**——前者原样透传退出码、**绝不重试**；只有暂态失败才重试。判据：sbatch 成功必打印 `Submitted batch job`（`--wait` 下作业算崩时退出码≠0 但已提交，命中此串即透传，绝不把必崩算例重投重跑 99 遍）。
- 新增任何 Slurm 调用先套上对应机制；别让一次提交 / 查询抖动直接跳过整个子目录或中断流水线。

**约定与诚实**
- 沿用下游既有约定（退出码、目录命名、文件契约），不自创语义。
- 不确定处留**显式 TODO** 并说明；声称"完成"前真验证，并确认所用 flag/模式真的支持。

**注释与输出风格**
- 注释解释**为什么** / 取舍 / 坑（shell 引号、变量展开时机等），必要处中英并存；不复述代码。
- emoji 词汇：📁目录 ▶️将执行 📍当前 ✅成功·收敛 ❌失败·未收敛 ⚠️警告 📊summary 🎉完成。
- 分隔线统一 `================ <emoji> <内容>`。

**交付**
- 脚本底部放几组 `test_args` 字典 + 注释切换的调用，方便手动覆盖多场景。
- 库函数配模块 docstring（开头列 `Functions:`）+ Google 风格 `Args/Returns`。

## 交付前自检

- [ ] 输出（emoji / 逐项 / summary）没被当"格式检查"删掉。
- [ ] 函数小而专；主函数只编排。
- [ ] 生成 shell 用拼接而非 f-string；路径绝对且每轮回根。
- [ ] 变量按类型命名：list 用 `l` 前缀（循环变量单数）、路径用 `Path` 且 `path_*`、dict 用 `dict_*`。
- [ ] check 失败 `fail()`、成功返回值且调用处接住了。
- [ ] 新增的 sbatch/squeue/srun/mpirun 都加了 99×10s 轮询重试；"已提交 / 查询成功"透传不重试，只重试暂态失败。
- [ ] `mymetal` 库模块 import-only（无 argparse/main/build_parser/`__main__`）；argparse/回显/入口逻辑全在 `pei_*` CLI，且照抄了同域 workflow 的拆分。
- [ ] CLI 开关单横杠 `-` + 下划线 `_`、只留长名、我们自己的取值也下划线；INCAR tag / 外部工具 flag / Slurm walltime / `-h/--help` 保持原样；跨脚本调用与库内 warn/fail/docstring 引用一并改。
- [ ] 沿用了下游约定；不确定留 TODO；声称完成的部分是真验证过的。
