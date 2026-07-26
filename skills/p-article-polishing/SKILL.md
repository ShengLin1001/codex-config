---
name: p-article-polishing
description: Apply PJ's evidence-backed writing preferences when polishing, drafting, translating, or restructuring English academic manuscripts across scientific fields. Use for manuscript sections, abstracts, introductions, methods, results, discussions, conclusions, figure captions, and reviewer responses; also use when updating PJ's likes and avoids from historical revisions or refreshing the bundled academic-expression corpus. Preserve scientific meaning, data, citations, terminology, formulas, and confirmed author-specific notation.
---

# P Article Polishing

润色或写 PJ 的英文科研文章时，先应用已确认的个人偏好，再按任务需要调用通用学术语料。不要把某篇材料学论文的章节模板机械套到所有学科，也不要把参考论文中的写法自动视为 PJ 的个人偏好。

## 按需读取

- 每次任务都读取 [references/personal-style.md](references/personal-style.md)。
- 写或重构整段、整节、摘要、引言、Discussion 或结论时，再读取 [references/academic-style.md](references/academic-style.md) 中对应部分。
- 只有在更新个人偏好、核查冲突或用户要求说明依据时，才读取 [references/evidence.md](references/evidence.md)。
- 只有在新增、替换或重新提炼参考论文时，才读取 [references/corpus-index.md](references/corpus-index.md) 和相应 PDF。
- 只有在读取新的 DOCX tracked changes 或 comments 时，才运行 `scripts/extract_docx_revisions.py`。

## 边界

- 只负责语言、论证顺序、段落结构和学术表达。
- 不改变数据、机理、比较基准、限定条件、引文键、图表编号、公式、符号、数值或单位。
- 不做 Word 修订合并、接受或拒绝修订、格式转换、参考文献管理、Git 提交或论文发布。
- 原文含义不清、证据不足或前后矛盾时，列出待 PJ 确认的问题，不用流畅措辞补齐缺口。
- 跟随目标期刊、目标稿和用户本次明确要求；它们高于本 skill 的默认写法。

## 证据优先级

发生冲突时按以下顺序处理：

1. 用户本次明确要求；
2. 用户明确确认的个人偏好；
3. 对应文章的最终接收稿或用户认可净稿；
4. 多个独立修订中重复出现、且在后续净稿保留的导师修改；
5. 单次 tracked change 或 comment；
6. 参考论文中跨文章重复的通用模式；
7. 通用学术英语习惯。

低层证据不得覆盖高层证据。单次修改只记为候选或条件性写法，不升级成全局规则。

## 润色或写作

1. 判断任务规模：一句、小段、整节或全文。只加载当前任务需要的参考内容。
2. 先核对目标文本中的科学对象、术语、符号、数据、引用和图号。
3. 标出命中的“避免”模式，再按“喜欢”模式做最小充分修改。
4. 维持原有事实和因果；需要重排时，优先调整句序和段落功能，不重写科学结论。
5. 对整段或整节使用“问题/对象 → 证据 → 解释 → 有边界的结论”的单向逻辑。
6. 交付润色文本，并简要列出采用的关键偏好和仍需确认的问题。用户只要净稿时，不附冗长说明。

## 更新个人风格

1. 确认初稿、修订稿、修改者和最终稿的对应关系。
2. 从 Git diff 或 DOCX 中提取 `before → after`、comments 和最终稿状态。
3. 将证据登记到 `references/evidence.md`，区分 `confirmed`、`candidate`、`conditional` 和 `deprecated`。
4. 只有 `confirmed` 规则进入 `references/personal-style.md` 的全局约束；特定学科或章节规则必须标明适用范围。
5. 新证据推翻旧规则时，不累计矛盾规则；更新当前状态，并在证据文件中保留溯源。

读取 DOCX 修订时：

```powershell
& "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe" `
  skills/p-article-polishing/scripts/extract_docx_revisions.py `
  "<manuscript.docx>" -author "Yang Gao"
```

脚本只读 DOCX；输出不是自动写作、版本对齐或三方合并结果。

## 更新参考语料

1. 在 `references/corpus-index.md` 登记题目、DOI、来源、用途和本地文件名。
2. 只提炼短表达、修辞功能、段落逻辑和章节组织，不复制长句或整段原文。
3. 单篇表达可作为候选模板；跨多篇重复的模式才总结为通用写作原则。
4. 将结果写入 `references/academic-style.md`，不得直接写入个人偏好。
5. 只有 PJ 明确确认或历史修订支持时，才能把语料模式提升为个人规则。

## 交付前检查

- 每项重要修改能追溯到个人规则、目标稿上下文或必要语言纠错。
- 没有把材料学专用符号、Acta 章节习惯或单篇参考论文模板套到无关稿件。
- 数字、单位、公式、术语、引用、图号和因果关系未漂移。
- 未定义符号、缺失数据、缺图号、缺引文、panel 遗漏和逻辑矛盾已修复或明确报告。
- PJ 确认的连字符、悬挂连字符和方向符号未被通用 linter 擅自改写。
