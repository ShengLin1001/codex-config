# 判断原则与章节骨架

## 证据强度对账

不查表。每个承载主张的表达（结果动词、因果词、限定词、比较词、意义句）都执行三步：

1. **说出它预设的证据等级**——这个表达要成立，作者必须已经做到什么。用可核查的动作描述，不用形容词：「需要独立手段的第二次测量」而不是「需要较强证据」。
2. **在稿件里找这个等级的落点**，落点必须是具体的图、表、公式、实验、计算或引用。
3. **对不上就报断言边界问题**，resolution test 二选一：降到证据支持得起的表达，或补该等级的证据。

报告里必须写出第 1 步判定的等级，让作者能反驳你的判定。同一稿件内同类表达用同一标准。

判定卡在中间档时，问一句：**如果作者只有现在这些材料，一个持怀疑态度的审稿人会不会要求补做实验？**会 → 表达过强。

两端固定，不由推导决定：

- 只观察到同步变化或数值吻合 → 只能写相关，不能写因果、机理来源或唯一归因。
- 单一间接结果 → 不能用 `confirm`、`demonstrate`、`prove` 承载。`prove` 不作默认结果动词。
- 摘要和结论的意义句通常只有一句；多于一句，或意义超出正文建立的范围，是断言边界问题。

## 其他判断原则

命中不等于判错——先看技术含义、搭配和上下文，目标稿的既有写法和目标期刊体例优先。

- **空白必须说清缺的是哪一种**：报道、知识、机理、实验验证还是测量能力。`not well studied` 一类含糊表述，只有当空白本身不具体时才算问题，不替作者选一类。
- **比较必须口径一致**：对象、参考态、条件、变量、单位对齐才成立；`respectively` 救不了数量或顺序对不齐的对应关系。
- **连接词必须承载真实的逻辑关系**：后句只是同义重复却用 `Furthermore`，或同段堆叠多个同功能连接词，报为行文问题。

## 识别模型腔

只作待复核提示，**不自动判错**。命中记 `Preference only`，诊断写"待作者复核"，不赋 Severity，不进「优先问题」。

**零出现词**——LLM excess-vocabulary 清单中，在五篇材料科学、凝聚态与第一性原理参考论文里零出现的部分：

`delve, underscore, showcase, leverage, harness, foster, bolster, catalyze, unearth, illuminate, navigate, scrutinize, transcend, boast, embark, grapple, juxtapose, encompass, emphasize`；
`intricate, meticulous, pivotal, nuanced, multifaceted, groundbreaking, innovative, transformative, invaluable, commendable, renowned, exhaustive, actionable`；
`additionally, notably, seamlessly, profoundly, strategically, thoughtfully, undoubtedly, accurately`；
`realm, tapestry, testament, journey, milestone, ecosystem, prowess, essence, intricacy, utilization`；
`shed light on, deep dive, game changer, vital role, knowledge gap`。

**按词形严格生效，不外扩到同根词**：报句首的 `Additionally`（参考论文 0 次），`in addition`（7 次）和 `additional`（11 次）不报；报 `accurately`（0 次），`accurate`、`accuracy`（共 4 次）不报。

**灰名单，缺确切技术所指才报**：`align`、`complex`、`surpass`、`unveil`、`necessitate`、`noteworthy`、`versatile`、`deeper`、`advancement`。`aligned lattice`、`complex oxide` 这类实指不报，用作泛化强调才报。

**标点**：破折号（`—`、`–`）插入解释、冒号在句中引出解释或列举，报待复核。术语构词的连字符（`low-SFE`、`out-of-plane`）、题目里的冒号、图注编号和公式里的固定写法不报。

**不是禁用词**：`critical`、`crucial`、`fundamental`、`remarkable`、`universal`、`It is worth noting`。有数字、引用或清楚逻辑支撑就不报。

目标稿已稳定采用且语义准确的写法，不因另一种表达更常见就判错。

## 章节功能骨架

反查稿件做到哪一步、缺哪一环。**是功能骨架不是模板**：稿型或目标期刊另有体例时以后者为准，缺环只在确实断了证据链时报告。

| 章节 | 功能序列 |
|---|---|
| Title | 体系或对象 → 核心发现或关键手段 → 必要限定 |
| Abstract | 对象与问题 → 具体空白 → 本文做了什么 → 最重要的定量结果 → 机理或独立验证 → 一句有边界的意义 |
| Introduction | 背景与代表性证据 → 明确空白 → 本文能回答的问题 → 方法与路线 |
| Methods | 框架或仪器 → 关键参数与近似 → 统一口径 → 可靠性验证（要有比较量和文献结果） |
| Results（每小节） | 图/panel 定位 → 条件与定量趋势 → 基准或对照 → 与证据强度匹配的解释 → 段尾结论 |
| Discussion | 核心关系 → 多个结果的统一机理 → 与已有工作比较 → 候选来源及其证据强弱 → 限制与待验证部分 → 有边界的综合 |
| Conclusion | 对象与方法 → 按正文顺序概括主结果和关键数字 → 机理或验证结论 → 一句意义 |
| Figure caption | 首句整图功能 → 逐 panel 覆盖 → 颜色、线型、符号、箭头、插图、统计量 |

Discussion 深化和统一结果，不重复 Results 的数字；图注描述图里有什么，机理讨论留在正文。
