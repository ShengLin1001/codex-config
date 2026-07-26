---
name: p-article-polishing
description: >-
  Build the structure of and polish English academic manuscripts, primarily in
  materials science, condensed-matter physics and computational research. Use for
  planning a paper's outline and throughline before drafting, for restructuring an
  existing draft, and for polishing language in abstracts, introductions, methods,
  results, discussions, conclusions and figure captions; also use when comparing
  alternative academic phrasings, explaining why one expression fits the evidence
  better, or updating the bundled expression bank from reference papers and
  manuscript revision records. Preserves the target manuscript's data,
  terminology, notation, citations, formulas and journal conventions.
---

# P Article Polishing

写或改英文科研文章分两件事：先定架构（outline 与主线），再做语言（表达与措辞）。

本 skill 只提供通用学术规范，不带任何学科的章节模板。目标稿的既有体例、目标期刊要求和用户本次的明确指示，都高于这里的默认写法。

## 选择入口

- 写新文章、新章节、新段落，或重排已有结构 → 读 [references/structure.md](references/structure.md)，先出 outline 并交作者确认，再写正文。
- 改已有文本的语言、比较几种表达 → 按下面四条自检改；遇到拿不准的选择（动词强度、限定词、空白类型、因果强度、连接词）再查 [references/language.md](references/language.md)。**先写句子后查表**，反过来就会为了套句式而扭曲结论。
- 写图注 → 图注的功能顺序见 [references/structure.md](references/structure.md) 的章节骨架。
- 两者都要（例如"帮我写 Discussion"）→ 先架构，再语言。
- 新增参考论文或新的修改记录 → 读 [references/corpus.md](references/corpus.md)。

## 四条自检

三个尺度加一条边界。写完任何一段文字都过这四条；绝大多数返修意见都落在这里面。

### 1. 断言尺度：每句话都要能被查

写完一个断言就问：读者要验证它，得看哪里？

- **主体明确**：主语是具体对象——`Figure 5(a) shows ...`、`We calculate ...`。不用 `It is found that`、`It can be seen that`、无主语观察句，也不让 `this`、`it`、`the effect`、`the condition` 独自承担关键含义。名词化开头改成明确的动作主体。
- **落点唯一**：结论落到具体的 figure、panel、表、公式、数值或文献；他人工作和领域性断言必须有引用。定位不了的 `as shown`、`consistent with`、`Where ...`，要么补落点，要么删。
- **首次出现即定义**：缩写、符号、参考态、比较基准、判据、自定义参数。同一概念全文用同一术语，不为避免重复而换近义词。
- **不让读者补算**：给了原始量，就同时给稿件真正用到的量（差值、百分比、应变、比值）。给了并列关系，就写出对应顺序；`respectively` 只用于数量和顺序严格一致的情况，它救不了含糊的对应。
- **强度匹配证据**：动词和限定词是证据等级，不是文采。直接数据用 `show`，受限解释用 `indicate`，间接或模型依赖用 `suggest`，独立手段验证用 `confirm`，多项证据支持强结论用 `demonstrate`。不要把 `prove` 当默认结果动词，也不要在一句里堆 `may possibly be likely to`。

### 2. 段落尺度：一段一个功能，单向不回头

- 段首一句说明这段要干什么（定位某图、提出某问题、建立某对照），段中给证据，段尾给一句有边界的结论。没头没尾的孤句要补总起句。
- 一旦开列并列对象——材料、条件、panel、机制——就必须逐项覆盖，顺序一致。写了 `similar trends` 就补上代表性数值、条件和 panel。
- 多个过程、机制或贡献分开编号，并说明每一步各自对应什么因素。
- **不回头**：已判定为次要或已被排除的因素，后文不得无新证据复活成主因；后一节不推翻前一节的结论；同一结论不在引言、小节尾、Discussion 和 Conclusion 反复整段复述——收口用一句话，不重列所有数字。
- 删重复时保留条件、数字、引用和限定语；删的是复述，不是证据。

### 3. 全文尺度：一条主线

- 全文能用一句话说出最终结论。每一节、每一段都要能回答："它把这条结论推进了哪一步？"
- 答不出来的段落是候选删除项，不是候选扩写项。
- 章节和段落顺序服从论证顺序，不服从做实验或读文献的时间顺序。看到什么讲什么就是没有主线。
- 摘要和结论不引入正文没有的数据、引用或因果。

### 4. 边界：跟随作者，不掺机器腔

- 术语、符号、连字符、单位写法、图号体例、时态、大小写：跟随目标稿的既有约定。不用通用 linter 或"看起来更学术"的直觉去覆盖作者已经统一的用法（包括作者刻意保留的悬挂连字符、方向符号、非常规单位形式）。
- 强调词（`critical`、`crucial`、`fundamental`、`remarkable`、`universal`、`It is worth noting` 等）不是禁用词。判据是有没有数字、引用或清楚逻辑支撑：有就留，没有就改写或删，不因为"像套话"而机械删除。
- **反向同样成立：不掺入模型腔。**不为显得学术而引入目标稿没有的模型化用词；不用破折号（`—`、`–`）插入解释，冒号尽量不用于句中引出解释，标点优先逗号和句号、分号少用。破折号不是连字符——`FCC- and HCP-`、`low-SFE` 这类构词属于上一条的作者约定，保留不动。完整词表和标点细则见 [references/language.md](references/language.md)。
- 某个句子里的词语替换只在那个句子里成立，不升级成全文查找替换。
- 原文含义不清、证据不足或前后矛盾时，列出待作者确认的问题，不用流畅措辞把缺口补平。

## 任务边界

- 只负责语言、论证顺序、段落结构和章节组织。
- 不改数据、机理、比较基准、限定条件、引文键、图表编号、公式、符号、数值、单位。
- 不做 Word 修订合并或接受、格式转换、参考文献管理、Git 提交、投稿。

## 三种协作模式

**默认模式 3。**作者说"模式 1/2/3"或表达等价要求时切换（"别问了，直接给净稿"就是模式 2；"先把问题列给我"就是模式 3），可以中途切换；语义不明确时不要自行猜模式，按默认走。

三种模式只决定语言润色时如何收集待确认信息。架构任务（新写、重排结构）不受模式影响，一律走 outline → 作者确认 → 正文。

| | 模式 | 行为 |
|---|---|---|
| **1** | 逐段对话 | 处理一段前先问清该段的阻断问题，得到答复后改这一段，再进下一段 |
| **2** | 一次性交付 | 不提问，按四条自检直接改，待确认的点列在结果后面 |
| **3** | 先列问题，一次答完（默认） | 通读全文，只标问题不改字，列成清单；作者一次性答复后执行修改并交付润色结果 |

模式 3 不是交完问题清单就结束——拿到答复必须继续把润色做完。

### 提问规则

用当前环境可用的提问机制；没有结构化提问工具时直接用简短文本提问，并遵守该工具的单次问题数量上限。

**该问**：

1. **科学含义不清**——原文想说什么无法从上下文确定，或证据不足以支撑该句。这类必须问，不能用流畅措辞猜圆。
2. **几种表达在科学上等价、但强调点不同**——作者偏好无法从证据推出。
3. **结构取舍**——某段是否保留、某个结果放 Results 还是 Discussion、某个限制写多细。

**不该问**：四条自检或 [references/language.md](references/language.md) 已能判定的（证据强度决定的动词、缺落点、体例一致性）。这些直接改，事后一行说明。把有默认答案的问题抛给作者，是把工作退回去。

只有确实存在互斥的几种解释时才给选项，并为每个选项附一句它强调什么、代价是什么——作者答完应当拿走这条分界，而不只是做了个选择。科学含义完全不清时用开放式提问，不要硬凑成选择题。

关键问题的总数不设硬上限。模式 1 每轮只问当前段落的阻断问题，不要连续审问；模式 3 通读全文后一次列出全部阻断问题，按章节和段落分组。四条自检就能定的不算阻断问题——没有阻断问题时不要凑，直接交付润色结果。

### 偏好回写

作者的回答若反映稳定偏好而非针对该句的一次性判断，**追加**写入被润色稿件同目录下的 `inbox.md`：

- 每条记：日期、原句、给过的选项、作者的选择和理由、建议合入 `language.md` 的哪张表。
- 只追加，不改动已有条目，交付时报告文件绝对路径。
- 没有稿件文件时（例如作者直接粘贴文本），不建文件，把这些条目写在交付说明里。

不要直接改 `language.md`。安装后的 skill 是 `~/.agents/skills/` 下的副本，改在那里进不了 Git 仓库，由作者自行合并 `inbox.md`。

## 交付

- 架构任务先交 outline，确认后再写正文；不要跳过 outline 直接产出全文。
- 交付时说明改了哪几类问题、哪些点仍需确认。
- 整稿任务在收尾时过一遍：语法、拼写、时态、单复数、英美拼写是否全文一致；术语、缩写、符号、单位是否全文同一口径（整稿才做，短段落不需要）。
