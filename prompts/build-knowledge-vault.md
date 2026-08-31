# 任务：新建 Obsidian 知识库 myobsidian，从三个来源汇入

> 这是给下一个 session 执行的任务说明。请完整读完再动手。
> 执行者：Claude Code / Codex / Hermes 均可。

---

## 0. 核心决策（已定，不要再讨论）

**新建一个空的 vault 仓库，三个来源一视同仁地导入。不从任何现有仓库派生。**

- Vault：`F:/BaiduSyncdisk/version20240608/main_code_space/myobsidian/`
- 远程：`ShengLin1001/myobsidian`（我已创建）
- **三个来源仓库全部只读**，全程不得修改、移动、删除其中任何文件

为什么不从 myhexo 派生：笔记的创作时间在 frontmatter 的 `date` 里本来就有，编辑历史对知识库价值很低，而 myhexo 原样保留着、历史一条没丢。派生反而要背一堆 Hexo 残渣，还会逼出"仓库内移动"和"跨仓库导入"两套规则。**一套规则打三个来源，简单得多。**

不用 git submodule。三个来源的内容按主题**重新归类后复制**进 vault，靠 provenance frontmatter 保持可追溯。

---

## 1. 目标结构

```
myobsidian/                  ← Obsidian vault 根 = 仓库根
├── AGENTS.md                ★ agent 每次会话自动读，写清三层写权限
├── SCHEMA.md                ★ 归档与写作约定
├── README.md                #  vault 是什么、目录含义
│
├── 00-inbox/                #  未分类投喂区，定期清空
│
├── 10-sources/              ★ 经验 / 日志 / 安装与使用记录（按主题）
│   ├── vasp/
│   ├── lammps/
│   ├── log/                 #  日志、随笔、思考
│   ├── python/
│   ├── linux-hpc/           #  Slurm、module、集群环境、编译
│   ├── git/
│   ├── ai-agent/            #  Claude Code / Codex / Hermes / MCP / skill
│   ├── tools/               #  Zotero、EndNote、Typora、VS Code
│   ├── writing/             #  学术写作、论文、英语
│   └── theory/
│
├── 20-projects/             ★ 每项目一个子目录
│   └── <project-slug>/
│       ├── LOG.md           #  工作日志，日期倒序分节
│       ├── PLAN.md          #  计划 / 待办 / 里程碑
│       └── notes/           #  项目沉淀知识、交付文档、agent 总结
│
├── 30-wiki/                 ★ 唯一允许 agent 自由创作的层
│                            #  跨来源综合、去重、互链后的结构化页面
│
├── 90-archive/
│   └── INDEX.md             #  无法转 markdown 的材料索引（不复制本体）
│
├── images/                  #  所有图片，按来源文章/主题分子目录
│
├── _import/
│   ├── MANIFEST.csv         ★ 覆盖率台账，证明"没有遗漏"
│   └── REPORT.md            #  人类可读的导入报告
│
└── _scripts/
    ├── check_links.py       #  双链与图片完整性自检
    └── sync_sources.py      #  三个来源的增量同步报告
```

`10-sources/` 的主题目录**不是固定的**——阶段 1 看完实际分布再定，宁可少建几个也别建一堆空目录。

---

## 2. 硬性约束（违反即返工）

1. **三个来源仓库全部只读。** 不修改、不移动、不删除其中任何文件。
2. **不用 git submodule，不从现有仓库派生。**
3. **不得遗漏。** 每个来源文件在 `_import/MANIFEST.csv` 里必须有记录且 `disposition` 非空。跳过也要写理由。
4. **不批量删除。** 遵守全局约束：一次只删一个明确路径，需要批删就停下来让用户手动执行。
5. **UTF-8。** 读写用 `encoding="utf-8"`；跑 Python 前设 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`。Windows 用 `python`，不用 `python3`。
6. **分阶段提交，每阶段停下来给用户确认**，不要一口气跑完。

---

## 3. 三个来源

导入前先对每个来源仓库 `git pull` 并记下 HEAD 短 sha（写进 provenance frontmatter）。

### 来源 A：myhexo

`F:/BaiduSyncdisk/version20240608/main_code_space/myhexo`

**只导入内容，Hexo 建站部分全部 `skipped`。**

正文在 `source/_posts/`，57 篇 md 已分 7 类：

| 现目录 | 数量 | 归入 |
|---|---|---|
| `Software/` | 16 | 按软件名拆进 `10-sources/vasp\|lammps\|tools/` |
| `Developing/` | 11 | `10-sources/python\|git\|linux-hpc/` |
| `Thinking/` | 11 | `10-sources/log/` |
| `Summary/` | 10 | 逐篇判断；综述性质的挑出来做 `30-wiki/` 素材 |
| `Theory/` | 4 | `10-sources/theory/` |
| `Program/` | 3 | `10-sources/python/` |
| `Writing/` | 2 | `10-sources/writing/` |

**⚠️ 图片路径必须转换（头号风险）**：18 篇文章共 92 张图，用的是 Hexo 站点根绝对路径

```markdown
![vasp5.4.4](/images/Install-Software/1.png)
```

Obsidian 把前导 `/` 当文件系统根，不转换则图全挂。转成 **Obsidian 嵌入式双链**：

```markdown
![[images/Install-Software/1.png]]
```

选 wikilink 不选相对路径：wikilink 从 vault 根全局解析，与文件位置无关，以后重新归类文章图也不会断。

- 正则：`!\[([^\]]*)\]\(/images/([^)]+)\)` → `![[images/$2]]`（alt 文本丢弃；alt 里有中文和标点，用 `|` 分隔容易出问题）
- `source/images/`（17 个子目录、92 文件）整体复制到 vault 的 `images/`
- 转换后立即跑 `check_links.py` 校验每个 `![[images/...]]` 目标存在，**缺失必须为 0**
- `post_asset_folder: true` 造成的 8 个文章同名资源目录引用方式可能不同，单独核对

**frontmatter 处理**：`title`/`date`/`tag` 保留并转成 vault 格式；`categories` 转成 `tags` 的一部分（它记录了原始归类，有价值）；`mathjax: true` 删（Obsidian 原生支持 `$...$`）；`typora-root-url` 删（图片改双链后无用且误导）。

**根目录三样是内容，不要当 Hexo 残渣跳过**：

| 路径 | 去向 |
|---|---|
| `zhihu/`（8 个知乎文章 PDF） | → `90-archive/INDEX.md` 登记标题与主题。其中 `lammps-*.pdf`、`Lammps-RDF-*.pdf` 的正文可能已在 `_posts` 里，核对后标注"已有 md 版本" |
| `typora_font_color/AutoHotKey.ahk` | → `10-sources/tools/`，同时写一篇 `typora-字体配色.md` 说明它干什么、怎么用 |
| `source/about/index.md` | 先读内容。个人介绍 → `00-inbox/` 待定；博客说明 → `skipped: hexo-page` |

**`skipped: hexo-infra`**：`themes/`(89) `_config*.yml` `package*.json` `scaffolds/` `.github/` `sbatch.bash` `db.json` `node_modules/`(8546) `public/`(282)，按目录记一条即可，不逐文件展开。

### 来源 B：Being-a-phd-student

`F:/BaiduSyncdisk/version20240608/main_code_space/Being-a-phd-student`

- 开工前 `git pull`（本地最后 push 是 2025-09，可能落后）
- 只需要分析 `F:\BaiduSyncdisk\version20240608\main_code_space\Being-a-phd-student\notes` 和 `F:\BaiduSyncdisk\version20240608\main_code_space\Being-a-phd-student\technology_summary` 两个目录，其他全部 `skipped: raw-calculation-data`（数千文件） 
- 全仓库约 **4846 个文件**，绝大多数是计算原始数据。**绝不整体复制**：

| 类型 | 数量 | 处理 |
|---|---|---|
| `.pptx` | 若干 |  判断主题 → `10-sources/<主题>/`；未成型的 → `00-inbox/` |

主要就是我之前记录的一些使用经验和总结，日志等

### 来源 C：工作项目的 agent 总结 / 交付文档

这些有的不在本地，我们主要有这三个项目：金的相变机制（F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制，已发表），低层错能FCC金属的相变机制 （F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2026\面内应变-general），金的神经网络势函数 （F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2025\机器学习势函数），我们的python包（F:\BaiduSyncdisk\version20240608\main_code_space\pjvasp_package）
之前的日志md文件和每个项目下的日志md文件是有冲突的，不需要把之前的LOG.md 文件拆分到各个项目下，直接把之前的LOG.md文件放到00-inbox/下，后续再整理。每个项目的LOG.md为空就行了

## 4. 文件规范（写进 `SCHEMA.md`）

**每个导入的文件都要有 provenance frontmatter，三个来源一视同仁，无例外**：

```yaml
---
title: VASP 在 XX 集群上的编译记录
date: 2024-03-15           # 优先级：原 frontmatter > git log 首次提交 > 文件 mtime
tags: [vasp, hpc, install]
source_repo: myhexo        # myhexo | phd | other/proj-a | ... ；vault 内原创写 native
source_path: source/_posts/Software/vasp-compile.md
source_commit: 5f2a1b0     # 导入时该来源仓库 HEAD 短 sha
imported: 2026-08-03
---
```

`source_repo` / `source_path` / `source_commit` 是**替代 submodule 的唯一手段**——没有它们就无法判断来源仓库后续更新了什么。**不许省略。**

其他约定：

- 文件名小写连字符，中文标题放 frontmatter 的 `title`
- **全库统一用 Obsidian 双链**：文档间 `[[文件名]]`，图片 `![[images/子目录/x.png]]`
- 图片一律放 `images/<来源文章名或主题>/`，不散在文章旁边
- 一个文件只讲一件事。原文件混了三个不相关主题就**拆成三个**并互链
- `30-wiki/` 的页面正文末尾必须列出它综合了哪些源页面

---

## 5. `_import/MANIFEST.csv`（"不遗漏"的凭证）

每个来源文件一行，UTF-8：

```csv
source_repo,source_path,disposition,target_path,reason
myhexo,source/_posts/Software/ase-poscar.md,imported,10-sources/tools/ase-poscar.md,
myhexo,source/images/Install-Software/1.png,imported,images/Install-Software/1.png,
myhexo,themes/,skipped,,hexo-infra (89 files)
myhexo,zhihu/lammps-Add-new-pair-style.pdf,archived,90-archive/INDEX.md#L7,
phd,material-science/note.md,imported,10-sources/vasp/xxx.md,
phd,material-science/xxx.docx,archived,90-archive/INDEX.md#L42,needs-manual-conversion
phd,calc/run01/,skipped,,raw-calculation-data (87 files)
other/proj-a,docs/DELIVERY.md,imported,20-projects/proj-a/notes/delivery.md,
main_code_space/pymatgen,,skipped,,vendored-dir (1832 files)
```

`disposition` 五选一：`imported` / `merged` / `archived` / `skipped` / `pending`

**验收就是核对这个文件**：来源文件总数 == MANIFEST 覆盖的文件数（目录级记录按声明的 N 计入）。对不上就是有遗漏，必须找出来。

---

## 6. Obsidian 与 agent 对接

### Obsidian 配置

- Vault 根 = 仓库根。全库文件数在几百量级，秒开。
- 设置 → 文件与链接 → **排除的文件**：`_import`、`90-archive`
- 设置 → 文件与链接 → **新附件默认位置**：指定文件夹 `images`
- `.gitignore`：`.DS_Store`、`Thumbs.db`、`.obsidian/workspace*`、`.obsidian/cache`
  **`.obsidian/` 其余部分（插件配置、外观、快捷键）要提交** —— 本地和服务器打开同一 vault 配置一致
- 数字前缀 `00-/10-/20-/30-/90-` 保证文件树排序稳定

### `AGENTS.md`（vault 根）

Claude Code、Codex、Hermes 都会自动读（Hermes 查找优先级 `HERMES.md` > `AGENTS.md` > `CLAUDE.md`，只取第一个匹配）。至少覆盖：

1. **三层写权限**（最重要）：
   - `10-sources/` `20-projects/` = **归档层**，只放来源内容和用户手写的东西，agent 不在这里自由创作
   - `30-wiki/` = **唯一创作层**，综合、推断、重组都在这里
   - `00-inbox/` = 投喂区，agent 负责清空归类
2. 双链约定（文档 `[[]]`、图片 `![[images/...]]`）、frontmatter 字段、命名规则（指向 `SCHEMA.md`）
3. 禁止事项：**三个来源仓库只读**、不批量删除、不把 PDF/计算数据/二进制拷进 vault
4. UTF-8 与 Windows 注意事项

---

## 7. 执行阶段（每阶段结束停下来汇报，等确认再继续）

| 阶段 | 内容 | 产出 |
|---|---|---|
| **0** | `mkdir myobsidian` → `git init` → `gh repo create ShengLin1001/myobsidian --private` → 建目录骨架 → 写 `AGENTS.md`/`SCHEMA.md`/`README.md`/`.gitignore` → 配 Obsidian | 空骨架 |
| **1** | 全量盘点，**不搬运**：三个来源 `git pull` 并记 HEAD sha → 遍历 → 生成 `MANIFEST.csv`（多为 `pending`）+ `REPORT.md`（各来源统计、扩展名分布、`10-sources/` 主题目录方案、**57 篇逐篇归类表**、项目清单） | **计划，让用户确认** |
| **2** | 导入来源 A。先复制 `source/images/` → `images/`，再逐篇转换图片双链并导入，跑 `check_links.py` 校验（**缺失必须为 0**）。抢救 `zhihu/`、`.ahk`、`about/index.md` | 提交 |
| **3** | 导入来源 B。重点产出是 `90-archive/INDEX.md` 待转换清单 | 提交 |
| **4** | 导入来源 C。重点是 `LOG.md`/`PLAN.md` 合并质量，每段保留原始来源标注 | 提交 |
| **5** | 覆盖率验收：核对 MANIFEST 到差额归零；跑 `check_links.py` 查所有 `[[...]]` 和图片；Obsidian graph view 目测有没有大片孤岛（有孤岛说明双链没建起来） | 验收报告 |
| **6** | 写 `_scripts/sync_sources.py`：读 MANIFEST 各行的 `source_repo`+`source_commit`，对每个来源仓库跑 `git diff <commit>..HEAD --name-status`，报告"哪些已导入文件的上游变了 / 哪些是新增文件"。**只报告不自动改**。配最小自检：造两条假 MANIFEST 记录，`assert` 能识别 modified/added | 脚本 + 自检 |
| **7**（可选） | 起 wiki 层示范：读完 `10-sources/vasp/` + 项目里 vasp 相关笔记 → `30-wiki/vasp.md`，按"安装/参数/收敛/后处理/踩坑"重组并互链回源 | 模板页，认可后铺开 |

`check_links.py`（阶段 2 写）：扫全库 `![[...]]`、`[[...]]`、`![](...)`，断言目标存在，输出缺失清单。阶段 5 复用。

---

## 8. 不要做的事

- **不要修改三个来源仓库的任何文件。** 它们只读。
- **不要在图片双链校验通过前推进到来源 B。** 那 92 张图是最容易静默失败的地方。
- **不要把 `zhihu/`、`.ahk`、`about/index.md` 当 Hexo 残渣跳过**，它们是内容。
- 不要一开始就写脚本做全量分类。前几个阶段 agent 逐文件判断，分类质量比速度重要。规则稳定了（阶段 6）再脚本化。
- 不要把 PDF / 计算数据 / 二进制拷进 vault。vault 要能 grep、能 git diff、能塞进 LLM 上下文。
- 不要为了"完整"导入代码文档和第三方源码。
- 不要自动转换 docx/pptx/xmind。先列清单让用户挑。
- 不要在 `10-sources/` 和 `20-projects/` 里自由创作。那是**归档层**。综合、推断、重组全部发生在 `30-wiki/`。
