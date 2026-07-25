---
name: p-article-polishing
description: "Polish scientific manuscripts in PJ's established writing style, preferably as Git-tracked Markdown or LaTeX, and merge an advisor's tracked Word revisions back into the canonical text source. Preserve technical claims, intentional hyphenation, commands, citations, figures, numbers, and terminology. Use for academic articles, abstracts, introductions, methods, results, discussions, conclusions, figure captions, and advisor revision rounds."
---

# P Article Polishing

用于科研论文润色。Git 跟踪的 Markdown 或 LaTeX 是正文唯一权威源；Word 是导师审阅和修订的交换格式。目标不是记录谁在何时改过什么，而是稳定复现 PJ 的写作方式，并把导师在 Word 中确认的修改准确合并回文本源。

开始前完整阅读 [references/style-profile.md](references/style-profile.md)。它是直接用于改写的风格规范；历史文件和 Git commit 只是校正该规范的证据，不是润色任务的输出模板。

## 约束

- 当前用户指令、当前稿件数据与图表优先于历史风格。
- 不发明数据、机理、引用、实验条件或普适性结论。
- 不因“语言更顺”而改变因果方向、比较基准、限定条件、符号、数值或单位。
- 不把导师或合作者的一次修订机械当成真理；历史修订用于提炼稳定偏好，语法和科学内容仍需独立核对。
- 原文有歧义或证据不足时，保留原意并标记 `AUTHOR CHECK`；不要替作者猜答案。
- PJ 的连字符和悬挂连字符用法属于正确的作者风格，不得作为语法错误标记或擅自规范化。
- 对 Git 跟踪的 `.md` / `.tex` 做最小原位修改，由 Git 保留回溯能力；不在 Git 中的文件和 Word 文件默认输出 sibling，除非用户明确要求覆盖。
- 不执行整文件格式化、自动换行或段落重排来制造无意义 diff。
- 不主动 commit、push、reset、restore 或 checkout；只有用户明确要求时才改变 Git 历史或远程状态。

## 权威顺序

发生冲突时按以下顺序判断：

1. 用户本次明确要求；
2. 当前稿件的图、表、公式、数据和已确认事实；
3. 最新净稿中稳定保留的写法；
4. Yang Gao 的修订与批注所体现的稳定原则；
5. Jun Pei / 俊裴的后续重写；
6. 其他合作者的结构建议；
7. 通用学术英语习惯。

## 工作流

### 1. 明确任务边界

确认仓库根目录、目标文件、目标章节、期刊/字数限制和交付方式。若用户未说明：

- 保持原有期刊格式、引文格式、术语和时态；
- 只润色用户给定范围；
- Git 跟踪的 Markdown/LaTeX 原位修改；
- 非 Git 文件或 Word 文件输出 `<stem>_polished.<ext>`，不覆盖原稿；
- 摘要在不损失关键定量结果的前提下尽量控制在 200 词左右。

在 Git 仓库中先执行只读检查：

```bash
git rev-parse --show-toplevel
git status --short
git log --follow --format="%h%x09%an%x09%ad%x09%s" --date=short -- path/to/manuscript.tex
```

只在实际仓库根目录操作。工作区已有改动属于用户；不得覆盖、回退或混入无关文件。

### 2. 用 Git 回溯写作偏好

按任务需要选择最小范围，不做全仓库历史考古：

```bash
# 当前未提交改动
git diff --word-diff=plain -- path/to/manuscript.tex

# 某次提交具体改了什么
git show --word-diff=plain --format=fuller <commit> -- path/to/manuscript.tex

# 两个已知版本之间的变化
git diff --word-diff=plain <old_commit> <new_commit> -- path/to/manuscript.tex

# 查看旧版本正文
git show <commit>:path/to/manuscript.tex
```

- 优先研究用户明确指出的“满意版本”、导师修改 commit 和最终接受的 commit。
- 用 commit 作者、message、时间线和实际 diff 共同判断归属；`git blame` 只能定位来源，不能单独证明修改意图。
- 已接受且在后续版本稳定保留的变化权重更高；后来被撤销的修改不得写入稳定风格。
- Git 只能回溯已提交历史；未提交改动必须单独用 `git diff` 检查。

### 3. 保护 Markdown / LaTeX 结构

Markdown 中保留 frontmatter、标题层级、引用键、脚注、表格、图片路径、链接、代码块和数学分隔符。

LaTeX 中保留宏、命令、环境、`\label`、`\ref`、`\cite`、交叉引用、公式、表格和转义字符。除非用户明确要求，不改数学表达式和自定义命令。

- 只编辑自然语言及其必要的邻接标点。
- 沿用项目现有换行约定；不为“好看”重排整段。
- 新建文本稿且项目没有约定时，正文可采用一句一行，便于逐句 Git diff；渲染仍保持同一段落。
- `.bib` 仅在用户要求校正参考文献时修改，不因正文润色顺手整理。

### 4. 先查科学逻辑

逐段确定：

- 本段唯一主旨是什么；
- 主张对应哪一幅图、哪组数据或哪条引用；
- 比较对象、基准态、方向和条件是否明确；
- 新术语、缩写、符号是否在首次出现处定义；
- 结论是否超出已有证据。

逻辑有问题时先修逻辑，再改句子。若无法从稿件确认，添加 `AUTHOR CHECK`，不要用流畅文字掩盖问题。

### 5. 再做最小语言修改

- 优先局部替换、拆分过长句和删除重复表达，不整段重写。
- 每段按“主张 → 图/数据 → 比较 → 机理 → 小结”组织；不需要的环节不要硬凑。
- 用具体名词替代含糊的 `this`, `it`, `correlation`, `effect`。
- 用准确、克制的动词，删除无证据的 `perfect`, `remarkable`, `universal`, `fundamental` 等强化词。
- 同一概念只保留一个术语；尤其区分内禀/外加、面内/面外、单轴/等双轴、热力学/动力学。
- 不让读者自行换算关键应变、差值或阈值；稿件已有数据时直接写出。
- 保持 `Fig.`/`Figure`、箭头、单复数、冠词、时态和符号格式一致；连字符遵循 style profile，不按通用语法偏好改动。

### 6. 按章节检查

**标题**：对象、变量和范围准确；删除不能由正文支撑的宣传性表述。

**摘要**：背景/缺口 → 方法 → 核心定量结果 → 机理 → 意义。至少保留最能支撑主结论的数字；不要堆方法细节或重复结论。

**引言**：从具体研究问题收敛到明确缺口；避免空泛的 “has long been a central topic”。列出尚未解决的问题后，研究设计必须逐项回应。

**方法**：定义对象、约束、自由度、计算路径和输出量。方法时态遵循当前稿件或期刊的主导习惯，但全文必须一致。

**结果**：不仅说趋势，还给基准、变化方向、代表性数值和适用条件。每个正文引用的 panel 都应有解释。

**Discussion**：解释结果、边界和推广条件；只能深化或限定前文结论，不能无说明地反转因果或推翻 Results。

**结论**：回收已经证明的主线，不引入新数据、新机理或新普适性。

**图注**：逐 panel 说明对象；标清计算/实验、颜色/符号、open circle、虚线、单位和特殊条件，使图注可独立理解。

### 7. 强制 QA

交付前逐项检查：

- 所有数字、单位、材料名、方向和正负号与图表一致；
- 摘要、正文、结论中的阈值和机理不冲突；
- 缩写、符号和专有名词均先定义后使用；
- 每个需要文献支持的外部事实都有引用；
- 每个被引用的 figure panel 和每种关键材料都有正文描述；
- 不存在占位符、孤立公式、`Where?` 式无指向表述或让读者自行计算的关键量；
- 不存在一条句子中多处冠词、单复数、搭配、标点和术语错误；
- 修改前后科学含义一致，除非用户明确要求重构论点。

对 Markdown/LaTeX 额外执行：

```bash
git diff --check
git diff --word-diff=plain -- path/to/manuscript.tex
git status --short
```

确认 diff 只包含目标文字，没有整段 reflow、公式/命令损坏或无关文件。若仓库已有 `Makefile`、`latexmkrc`、README 构建命令或 Markdown 检查工具，使用现有命令验证；不要为一次润色新建构建系统。

## 合并导师的 Word 修订

Word 是导师的审阅界面，Markdown/LaTeX 是持续维护的正文。现有脚本必须保留，用它提取 Word 中的 tracked changes 和 comments：

```powershell
python scripts/extract_docx_revisions.py manuscript.docx -author "Yang Gao"
python scripts/extract_docx_revisions.py manuscript.docx -comments_only
python scripts/extract_docx_revisions.py -selftest
```

脚本只读 DOCX，打印每段修改前文本、导师修改后文本、作者、批注和锚定段落。它不直接写 Markdown/LaTeX；合并时执行语义三方比较：

- **base**：导出给导师的 Markdown/LaTeX 对应 commit；
- **theirs**：导师在 Word 中的修订后文本；
- **ours**：当前 Markdown/LaTeX 工作树。

推荐在导出 Word 前记录：

```bash
git rev-parse --short HEAD
```

将短 SHA 写入 Word 文件名或同时记录在交接说明中。收到导师稿后：

1. 确认 Word 基于哪个 commit；无法可靠确定 base 时先问用户，不根据日期硬猜。
2. 用脚本提取导师的修订和批注。
3. 从 base 找到对应原段，并在当前 Markdown/LaTeX 中定位同一论证单元。
4. 若 ours 与 base 相同，应用导师修改，同时恢复 LaTeX 命令、引用和数学标记。
5. 若 ours 已变化，合并导师的**修改意图**，保留 ours 中更新的数据、机理和结构；不得整段覆盖。
6. 导师批注转为待确认清单或源文件中的临时 `AUTHOR CHECK`，不要把批注正文写进论文。
7. 用 `git diff --word-diff=plain` 检查每项合并，确认没有遗漏导师修改，也没有损坏 Markdown/LaTeX 结构。

纯格式修改、作者单位变化和 Word 排版不自动回写正文。MathType、公式对象或域代码的提取空白不得当作导师删除。导师的文字修改与当前数据冲突时，以当前已确认数据为准并报告冲突。

## 交付

正文之外只给简短说明，分为：

- 已完成的语言/结构修改；
- 需要作者确认的科学歧义；
- 需要核对的数字、图表或引用。

同时报告目标文件、是否存在未提交 diff，以及是否按用户要求 commit。没有科学歧义或核对项时，不制造说明。
