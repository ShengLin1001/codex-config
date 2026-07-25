---
name: p-article-polishing
description: "Polish English scientific manuscripts in PJ's established revision style: preserve technical claims, repair causal logic before wording, add quantitative support already present in the manuscript, and audit definitions, figures, numbers, and references. Use for academic articles, abstracts, introductions, methods, results, discussions, conclusions, and figure captions."
---

# P Article Polishing

用于英文科研论文润色。目标不是把文字改得更华丽，而是让论证更清楚、数据更具体、术语更准确，同时保留作者原有技术判断和行文习惯。

开始前完整阅读 [references/style-profile.md](references/style-profile.md)。其中的规则来自 PJ 两篇论文的多轮 Word 修订、批注和后续净稿；材料学例句只说明写法，不得把其中的科学内容迁移到别的文章。

## 约束

- 当前用户指令、当前稿件数据与图表优先于历史风格。
- 不发明数据、机理、引用、实验条件或普适性结论。
- 不因“语言更顺”而改变因果方向、比较基准、限定条件、符号、数值或单位。
- 不把导师或合作者的一次修订机械当成真理；历史修订用于提炼稳定偏好，语法和科学内容仍需独立核对。
- 原文有歧义或证据不足时，保留原意并标记 `AUTHOR CHECK`；不要替作者猜答案。
- 对现有 Word 稿件做最小、局部、可追踪的修改。默认保留原文件，输出同目录 sibling 文件；只有用户明确要求时才覆盖。

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

确认目标文件或文本、目标章节、期刊/字数限制和交付方式。若用户未说明：

- 保持原有期刊格式、引文格式、术语和时态；
- 只润色用户给定范围；
- Word 文件输出 `<stem>_polished.docx`，不覆盖原稿；
- 摘要在不损失关键定量结果的前提下尽量控制在 200 词左右。

### 2. 先查科学逻辑

逐段确定：

- 本段唯一主旨是什么；
- 主张对应哪一幅图、哪组数据或哪条引用；
- 比较对象、基准态、方向和条件是否明确；
- 新术语、缩写、符号是否在首次出现处定义；
- 结论是否超出已有证据。

逻辑有问题时先修逻辑，再改句子。若无法从稿件确认，添加 `AUTHOR CHECK`，不要用流畅文字掩盖问题。

### 3. 再做最小语言修改

- 优先局部替换、拆分过长句和删除重复表达，不整段重写。
- 每段按“主张 → 图/数据 → 比较 → 机理 → 小结”组织；不需要的环节不要硬凑。
- 用具体名词替代含糊的 `this`, `it`, `correlation`, `effect`。
- 用准确、克制的动词，删除无证据的 `perfect`, `remarkable`, `universal`, `fundamental` 等强化词。
- 同一概念只保留一个术语；尤其区分内禀/外加、面内/面外、单轴/等双轴、热力学/动力学。
- 不让读者自行换算关键应变、差值或阈值；稿件已有数据时直接写出。
- 保持 `Fig.`/`Figure`、箭头/连字符、单复数、冠词、时态和符号格式一致。

### 4. 按章节检查

**标题**：对象、变量和范围准确；删除不能由正文支撑的宣传性表述。

**摘要**：背景/缺口 → 方法 → 核心定量结果 → 机理 → 意义。至少保留最能支撑主结论的数字；不要堆方法细节或重复结论。

**引言**：从具体研究问题收敛到明确缺口；避免空泛的 “has long been a central topic”。列出尚未解决的问题后，研究设计必须逐项回应。

**方法**：定义对象、约束、自由度、计算路径和输出量。方法时态遵循当前稿件或期刊的主导习惯，但全文必须一致。

**结果**：不仅说趋势，还给基准、变化方向、代表性数值和适用条件。每个正文引用的 panel 都应有解释。

**Discussion**：解释结果、边界和推广条件；只能深化或限定前文结论，不能无说明地反转因果或推翻 Results。

**结论**：回收已经证明的主线，不引入新数据、新机理或新普适性。

**图注**：逐 panel 说明对象；标清计算/实验、颜色/符号、open circle、虚线、单位和特殊条件，使图注可独立理解。

### 5. 强制 QA

交付前逐项检查：

- 所有数字、单位、材料名、方向和正负号与图表一致；
- 摘要、正文、结论中的阈值和机理不冲突；
- 缩写、符号和专有名词均先定义后使用；
- 每个需要文献支持的外部事实都有引用；
- 每个被引用的 figure panel 和每种关键材料都有正文描述；
- 不存在占位符、孤立公式、`Where?` 式无指向表述或让读者自行计算的关键量；
- 不存在一条句子中多处冠词、单复数、搭配、标点和术语错误；
- 修改前后科学含义一致，除非用户明确要求重构论点。

## Word 修订历史

需要从新的 `.docx` 修订稿更新风格证据时，运行：

```powershell
python scripts/extract_docx_revisions.py manuscript.docx -author "Yang Gao"
python scripts/extract_docx_revisions.py manuscript.docx -comments_only
python scripts/extract_docx_revisions.py -selftest
```

脚本只读 DOCX，向标准输出打印修订前后文本、修订作者、批注和锚定段落。净稿之间的差异不能可靠归属作者，必须结合文件名、Word 元数据和时间线判断。

## 交付

正文之外只给简短说明，分为：

- 已完成的语言/结构修改；
- 需要作者确认的科学歧义；
- 需要核对的数字、图表或引用。

如果没有后两类问题，不制造说明。
