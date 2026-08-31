# 任务：构建个人知识库 Vault（一次性迁移 + 可增量再同步）

> 这是给下一个 session 执行的任务说明。请完整读完再动手。
> 执行者：Claude Code / Codex / Hermes 均可。

---

## 0. 硬性约束（违反即返工）

1. **不使用 git submodule。** 来源仓库的内容要按主题**重新归类**并**物理复制**进 vault，不是挂载。
2. **来源仓库只读。** 全程不得修改、移动、删除 `myhexo` 和 `Being-a-phd-student` 里的任何文件。项目目录同理。
3. **不得遗漏。** 每一个来源文件都必须在 `_import/MANIFEST.csv` 里有一条记录，且 `disposition` 字段非空。没有"看着不重要就跳过"这种操作——跳过也要写明理由。
4. **不批量删除。** 遵守全局约束：一次只删一个明确路径，需要批删就停下来问用户。
5. **UTF-8。** 所有读写用 `encoding="utf-8"`；跑 Python 前设 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`。Windows 上用 `python`，不用 `python3`。
6. **分阶段提交，每阶段停下来给用户确认**，不要一口气跑完 6 个阶段。

---

## 1. 目标目录结构

Vault 位置（**开工前先向用户确认这个路径**，默认用它）：

```
F:/BaiduSyncdisk/version20240608/knowledge-vault/
```

选它的理由：在 BaiduSyncdisk 下自动同步、与 `main_code_space` 代码区分离、自身是独立 git 仓库便于推到服务器。

```
knowledge-vault/
├── README.md                  # vault 是什么、怎么用、目录含义
├── SCHEMA.md                  # ★ 写作与归档约定，agent 每次动 vault 前必读
├── 00-inbox/                  # 未分类投喂区，定期清空
├── 10-sources/                # 经验 / 日志 / 安装与使用记录，★按主题分类★
│   ├── vasp/
│   ├── lammps/
│   ├── log/                   # 我写的日志类内容
│   ├── python/
│   ├── linux-hpc/             # Slurm、module、集群环境、编译
│   ├── git/
│   ├── ai-agent/              # Claude Code / Codex / Hermes / MCP / skill
│   ├── writing/               # 学术写作、论文、英语
│   ├── tools/                 # Zotero、EndNote、Typora、VS Code 等
│   └── misc/                  # 确实归不进上面任何一类的
├── 20-projects/               # 每项目一个子目录
│   └── <project-slug>/
│       ├── LOG.md             # 工作日志，倒序，日期分节
│       ├── PLAN.md            # 计划 / 待办 / 里程碑
│       └── notes/             # 项目内沉淀的知识、交付文档、agent 总结
├── 30-wiki/                   # ★ 唯一允许 agent 自由创作的层 ★
│                              # 跨来源综合、去重、互链后的结构化页面
├── 90-archive/                # 无法转成 markdown 但要留索引的材料清单
├── _import/
│   ├── MANIFEST.csv           # ★ 覆盖率台账，证明"没有遗漏"
│   └── REPORT.md              # 每轮导入的人类可读报告
└── _scripts/
    └── sync_sources.py        # 增量再同步脚本（阶段 6 才写）
```

`10-sources` 的主题目录**不是固定的**——阶段 2 扫描完实际内容后按真实分布调整，宁可少建几个也别建一堆空目录。上面这份是起点建议。

---

## 2. 三个来源（一个都不能少）

### 来源 A：myhexo 博客

- 本地已有：`F:/BaiduSyncdisk/version20240608/main_code_space/myhexo`
- 远程：`git@github.com:ShengLin1001/myhexo.git`
- **开工前先 `git pull`**（本地可能落后）
- 正文在 `source/_posts/`，已按 7 类组织，共约 57 个 md：

  | 原目录 | 数量 | 建议去向 |
  |---|---|---|
  | `Software/` | 16 | 按软件名拆进 `10-sources/vasp|lammps|tools/...` |
  | `Developing/` | 11 | `10-sources/python`、`10-sources/git`、`10-sources/linux-hpc` |
  | `Thinking/` | 11 | `10-sources/log/`（随笔思考归日志） |
  | `Summary/` | 10 | 按内容判断，多半 `10-sources/` 或直接喂给 `30-wiki` |
  | `Theory/` | 4 | `10-sources/misc/` 或新建 `10-sources/theory/` |
  | `Program/` | 3 | `10-sources/python/` |
  | `Writing/` | 2 | `10-sources/writing/` |

- Hexo 的 frontmatter（`title/date/categories/tags`）要**保留并映射**到 vault frontmatter，不要丢日期。
- `source/images/` 里被正文引用到的图，复制进 `10-sources/<主题>/assets/` 并修好相对路径。**没被任何正文引用的图不复制**，在 MANIFEST 里记 `skipped: unreferenced-asset`。
- `themes/`、`node_modules/`、`public/`、`db.json`、`_config*.yml`、`package*.json` 全部 `skipped: build-artifact`。

### 来源 B：Being-a-phd-student

- 本地已有：`F:/BaiduSyncdisk/version20240608/main_code_space/Being-a-phd-student`
- 远程：`https://github.com/ShengLin1001/Being-a-phd-student.git`
- **开工前先 `git pull`**。用户提到 `technology_summary/` 下有软件使用记录，但**本地当前只有一个 pptx**——很可能本地落后于远程，或者内容在别的格式里。pull 完重新确认，如果 pull 后仍然只有 pptx，**停下来问用户**这些记录到底在哪。
- 这个仓库共约 4846 个文件，绝大多数是计算原始数据，**不要整体复制**。分类处理：

  | 类型 | 处理方式 |
  |---|---|
  | `.md`（约 5 个，主要在 `material-science/`、`my_program/`） | 正常导入 `10-sources/` |
  | `.docx`（44 个）、`.pptx`、`.xmind` | **不自动转换**。逐个在 `90-archive/INDEX.md` 登记：文件名、原路径、你从文件名推测的主题。列成清单交给用户决定哪些值得转成 markdown，转换是下一轮的事。 |
  | `.pdf`（216 个） | 同上，只登记索引，不复制。文献类 PDF 归 Zotero 管，不进 vault。 |
  | VASP/LAMMPS 计算数据（`INCAR/POSCAR/POTCAR/XDATCAR/*.dat/*.in/*.lmp/*.vasp/screen`） | 全部 `skipped: raw-calculation-data`。**但是**：如果某个计算目录旁边有 README 或注释性文本，那个文本要导入。 |
  | `.py/.sh/.pl/.m` 脚本 | 默认 `skipped: code`，除非脚本头部有大段注释说明用法——那种把注释提炼成 `10-sources/` 下的一篇经验笔记，正文里链回原脚本路径。 |
  | `.jpg` 等图片 | 只在被导入的 md 引用时才复制 |
  | `个人资料/`、`调研/` | 先 `ls` 看内容，含个人隐私的**停下来问用户**是否纳入 |

- 注意仓库里有 44 个 `.DS_Store`，全部 `skipped: junk`。

### 来源 C：工作项目里的 agent 总结 / 交付文档

候选目录在 `F:/BaiduSyncdisk/version20240608/main_code_space/` 下，已知含 md 的：

```
126  other/                  ← 数量最多，先摸清是什么
 92  fluent/
 25  pjvasp_package/
 18  cc-conect-summary/
  1  PJ-advanced-reasearch/
  1  vasp_utils/
```

另有 `pjvasp_package1/`、`pymatgen/`、`pymatgen-core/`、`scansci-pdf/`、`my-english-learning-website/`、`codex-config/` 待判定。

处理规则：

1. **先向用户确认哪些目录算"工作项目"**，不要自己拍板。`pymatgen`/`pymatgen-core` 大概率是第三方源码副本（`skipped: vendored`），`codex-config` 是配置仓库本身（`skipped: self`）。
2. 每个确认的项目在 `20-projects/<slug>/` 建目录，slug 用小写连字符。
3. 项目里的 md 分流：
   - 明显是**工作记录/进度/日志**性质 → 合并进该项目的 `LOG.md`，按日期倒序分节，每节标明原文件名
   - **计划/待办/路线图** → 合并进 `PLAN.md`
   - **交付文档、技术总结、agent 产出的分析报告** → 原样复制进 `notes/`，保留文件名
   - **README/API 文档/代码注释型 md** → `skipped: code-doc`，它属于代码仓库不属于知识库
   - 从项目笔记里提炼出的**通用经验**（比如"VASP 在 A 集群上怎么编译"）→ 除了留在项目里，**另外**在 `10-sources/` 对应主题下写一篇，两边互相 `[[链接]]`
4. `node_modules/`、`.git/`、`venv/`、`build/`、`dist/` 一律排除，但**要在 MANIFEST 里以目录为单位记一条** `skipped: dependency-dir (N files)`，不用逐文件展开。

---

## 3. Vault 内文件规范（写进 `SCHEMA.md`）

每个导入或新建的 markdown 必须有 frontmatter：

```yaml
---
title: VASP 在 XX 集群上的编译记录
date: 2024-03-15           # 原始创作日期，从 hexo frontmatter / git log / 文件 mtime 取，按此优先级
tags: [vasp, hpc, install]
source_repo: myhexo        # 来源仓库名；vault 内原创写 native
source_path: source/_posts/Software/vasp-compile.md
source_commit: 376a707     # 导入时来源仓库的 HEAD 短 sha
imported: 2026-08-03
---
```

`source_repo` / `source_path` / `source_commit` 三件套是**替代 submodule 的关键**——没有它们，以后就无法判断来源仓库更新了哪些内容。**不许省略。**

其他约定：

- 文件名用小写连字符，中文标题放 frontmatter 的 `title`，不放文件名（跨平台 + git 友好）
- 双链用 Obsidian 语法 `[[文件名]]`，不用相对路径链接
- 图片放同级 `assets/`，引用写 `![](assets/xxx.png)`
- 一个文件只讲一件事。原文件如果混了三个不相关主题，**拆成三个文件**并互链
- `30-wiki/` 的页面必须在正文末尾列出它综合了哪些 `10-sources` / `20-projects` 页面

---

## 4. `_import/MANIFEST.csv` 格式（"不遗漏"的凭证）

每个来源文件一行，UTF-8，逗号分隔：

```csv
source_repo,source_path,disposition,target_path,reason
myhexo,source/_posts/Software/vasp.md,imported,10-sources/vasp/vasp-basics.md,
myhexo,themes/next/package.json,skipped,,build-artifact
phd,material-science/xxx.docx,archived,90-archive/INDEX.md#L42,needs-manual-conversion
other/proj-a,docs/DELIVERY.md,imported,20-projects/proj-a/notes/delivery.md,
main_code_space/pymatgen,,skipped,,vendored-dir (1832 files)
```

`disposition` 只能是这五个值之一：`imported` / `merged` / `archived` / `skipped` / `pending`。

**阶段 5 的验收就是核对这个文件**：来源文件总数 == MANIFEST 行数覆盖的文件数（目录级记录按其声明的 N 计入）。对不上就是有遗漏，必须找出来。

---

## 5. 执行阶段（每阶段结束后停下来汇报，等用户确认再进下一阶段）

**阶段 1 — 建骨架**
确认 vault 路径 → `git init` → 建目录 → 写 `README.md` 和 `SCHEMA.md` → 写 `.gitignore`（排除 `.obsidian/workspace*`、`.DS_Store`、`Thumbs.db`）→ 首次提交。
不导入任何内容。让用户先看结构对不对。

**阶段 2 — 全量盘点，不搬运**
`git pull` 两个来源仓库 → 遍历三个来源 → 生成完整的 `MANIFEST.csv`，此时所有行的 `disposition` 填 `pending` 或已能确定的 `skipped` → 写 `_import/REPORT.md` 说明：各来源文件总数、按扩展名分布、你打算怎么分类、`10-sources` 主题目录的最终方案、`20-projects` 的项目清单。
**这一步产出的是计划，不是结果。** 用户在这里确认分类方案。

**阶段 3 — 导入来源 A（myhexo）**
只做 myhexo。57 个 md 全部处理完，图片路径修好，MANIFEST 对应行更新。提交。

**阶段 4 — 导入来源 B（Being-a-phd-student）+ 来源 C（项目）**
B 的重点是 `90-archive/INDEX.md` 那份待转换清单。
C 的重点是 `LOG.md` / `PLAN.md` 的合并质量——合并时保留每段的原始来源标注。提交。

**阶段 5 — 覆盖率验收**
按第 4 节的规则核对 MANIFEST，输出一份差额报告。有遗漏就补，直到归零。
另外跑一遍链接检查：所有 `[[...]]` 是否有对应文件，所有 `![](assets/...)` 是否存在。

**阶段 6 — 增量同步脚本**
写 `_scripts/sync_sources.py`：读 MANIFEST 里的 `source_commit`，对来源仓库跑 `git diff <commit>..HEAD --name-status`，输出"哪些已导入文件的上游变了 / 哪些是新增文件"的报告。
**只报告，不自动改 vault**——重新归类需要判断，交给 agent 下一轮做。
配一个最小自检：构造两条假 MANIFEST 记录，断言 diff 能正确识别 modified 和 added。

**阶段 7（可选，用户决定）— 起 wiki 层**
挑一个主题（建议 `vasp`）做示范：读完 `10-sources/vasp/` 全部内容，在 `30-wiki/vasp.md` 写一篇综合页——去重、按"安装 / 参数 / 收敛 / 后处理 / 踩坑"重组、互链回原始笔记。
这一篇是模板，用户认可后再铺开到其他主题。

---

## 6. 不要做的事

- 不要一开始就写自动化脚本做全量分类。**前 4 个阶段用 agent 逐文件判断**，分类质量比速度重要。等分类规则稳定了（阶段 6）再脚本化。
- 不要把 PDF / 计算数据 / 二进制拷进 vault。vault 要能被 grep、被 git diff、被塞进 LLM 上下文。来源 B 那 4846 个文件真搬进来就废了。
- 不要为了"完整"而导入代码文档和第三方源码。它们属于代码仓库。
- 不要自动转换 docx/pptx/xmind。先列清单让用户挑。
- 不要在 `10-sources/` 和 `20-projects/` 里自由创作。那两层是**归档层**，只放来源内容和用户写的东西。综合、推断、重组全部发生在 `30-wiki/`。

---

## 7. 开工第一句话

先向用户确认这三件事，然后再动手：

1. Vault 路径用 `F:/BaiduSyncdisk/version20240608/knowledge-vault/` 吗？
2. `main_code_space/` 下哪些目录算"工作项目"？（列出候选清单让用户勾选）
3. `Being-a-phd-student/个人资料/` 和 `调研/` 要不要纳入？
