# 学术表达库

从 [corpus.md](corpus.md) 登记的已发表论文中提炼的可复用表达。写作时用它选表达，评价时用它查表达的语义边界对不对。它回答的不是"哪个词更高级"，而是"在当前修辞功能和证据强度下，哪种说法更准确"。这些是可追溯的表达模式，不是逐字引文。

**这些表用来做选择，不是用来造句。**句子先按科学内容写出来，再用表核对：这个功能下我选的动词、限定词、连接词，语义边界对不对。表的价值在「何时使用」一列——近义表达之间的分界，那是模型最容易出错的地方；`X/Y/A/B` 那一列只是分界的例子，不是待填空的模板。

因此：表里没有的更贴切写法，优先于表里有但要迁就内容的写法；一段里不堆同功能的句子；一篇稿件里不重复同一个开头句式；目标稿的既有写法高于本表。

## 建立背景与重要性

避免 `X is very important.`——说明重要在哪里、为什么重要，或难在哪里。

| 意图 | 可选表达 | 何时使用 |
|---|---|---|
| 长期研究主题 | `X has long been a central topic in Y.` | 有充分文献支持长期关注 |
| 持续研究投入 | `Considerable experimental and theoretical effort has been directed at X.` | 同时概括实验与理论进展 |
| 尚未解决的难题 | `Achieving X remains an ongoing challenge.` | 强调目标困难，而非知识未知 |
| 说明具体重要性 | `X is particularly important because it is related to Y.` | 能给出明确的性质、机制或应用后果 |
| 科学与应用双重定位 | `For both scientific and technological reasons, X remains ...` | 两类价值都有正文或引文支撑 |

## 指出研究空白

不同表达对应不同类型的"未知"，不能互换。

| 空白类型 | 可选表达 | 语义边界 |
|---|---|---|
| 已研究 A，不了解 B | `X has been widely studied; however, little is known about Y.` | 建立明确的已知—未知对照 |
| 文献中尚无报道 | `To the best of our knowledge, X has not been reported.` | 只在完成可靠检索后使用 |
| 领域基本未触及 | `X remains unexplored.` / `X remains nearly unexplored.` | `nearly` 表示已有少量相关工作 |
| 机理研究不足 | `The mechanism governing X remains insufficiently investigated.` | 现象已有，机理证据不足 |
| 缺少实验证明 | `Experimental evidence for X remains missing.` | 理论或间接迹象已有，实验验证缺失 |
| 具体问题待答 | `Whether X controls Y remains unresolved.` / `How X controls Y remains to be determined.` | 本文能直接回应的问题 |
| 测量本身困难 | `Measuring X remains an experimental challenge because Y.` | 空白来自方法或分辨率限制 |

比 `X is not well studied` 更好的是说清缺的是报道、知识、机理、实验验证还是测量能力。

## 引出本文目的与路线

| 写作动作 | 可选表达 | 何时使用 |
|---|---|---|
| 中性报告 | `Here, we report on X.` | 介绍测量、数据集或现象，不提前强化结论 |
| 方法导向 | `Here, we use A and B to investigate X.` | 同时点明方法组合与研究对象 |
| 结果导向 | `Here, through X, we show that Y.` | 摘要中直接给出核心发现 |
| 推进已有方法 | `In this work, we advance X to Y.` | 确实扩展了方法能力或适用范围 |
| Letter 体例 | `In this Letter, we show that X.` | 仅限采用该体例的期刊 |
| 机理导向 | `Herein, X and Y are employed to elucidate Z.` | 多种手段共同解释物理来源 |
| 重新检验 | `In this study, we revisit X using Y and validate the result with Z.` | 对已有结论重新评估且有独立支持 |

`report` 最中性；`investigate` 只说动作不预设结果；`show` 直接给发现；`elucidate` 只用于真正解释机理；`advance` 只用于真实的方法推进，不能替代普通的 `use`。

## 描述方法与验证

| 功能 | 可选表达 | 何时使用 |
|---|---|---|
| 说明计算框架 | `Calculations were performed within X, as implemented in Y, using Z.` | 需同时交代理论框架、软件和关键近似 |
| 说明实验动作 | `We used X to probe Y.` | 主体明确、动作直接 |
| 说明对象与条件 | `Measurements were carried out on X under Y.` | 方法已知，重点是对象和条件 |
| 跨体系一致设置 | `X was employed across all geometries, maintaining Y.` | 参数需在不同模型间保持可比 |
| 统一口径 | `Unless otherwise specified, all results refer to X.` | 后文反复使用同一方向、基准或条件 |
| 参数敏感性 | `We tested X from A to B and used C without significant loss of accuracy.` | 参数无文献值，需说明选择稳健 |
| 验证可靠性 | `The computed X agrees well with previous theoretical and experimental results [refs], confirming the reliability of Y.` | 有明确比较量和文献结果 |

## 定位图表与报告定量结果

| 功能 | 可选表达 | 何时使用 |
|---|---|---|
| 图展示变量关系 | `Figure X shows Y as a function of Z.` | 图作句子主语并展示函数关系 |
| 图展示代表性结果 | `Figure X presents representative Y for A and B.` | 说明图中案例具有代表性 |
| 起点与终点 | `X increases/decreases from A to B under C.` | 起点、终点、条件均已知 |
| 变化量 | `X increases/decreases by A at B.` | 强调差值而非端点 |
| 范围 | `X ranges from A to B, depending on C.` | 数值随样品、条件或模型变化 |
| 极值 | `X reaches a maximum of A at B.` | 数据存在清楚极值 |
| 倍数或超出量 | `X is A times as large as Y under C.` / `X exceeds Y by A%.` | 比 `larger than` 更可核对 |
| 并列量对齐 | `X and Y are A and B, respectively.` | 两组项目严格一一对应 |
| 趋势加解释 | `X increases with Y, suggesting Z.` | 趋势是数据，Z 是受限解释 |

## 选择证据动词

这些动词不是文采替换，而是证据等级。

| 动词 | 含义 | 模板 |
|---|---|---|
| `show` | 数据、图或实验直接呈现 | `Measurements show that X.` |
| `demonstrate` | 多项证据支持较强结论 | `Calculations demonstrate that X controls Y.` |
| `reveal` | 揭示此前不可见的结构、关系或路径 | `Further analysis reveals that X.` |
| `indicate` | 数据支持该解释，但不是唯一证明 | `The results indicate that X stems from Y.` |
| `suggest` | 间接、模型依赖或仍有不确定性 | `The calculations suggest that X may control Y.` |
| `confirm` | 独立手段验证前一结果 | `Measurements confirm the accessibility of X.` |

## 比较、对照与逐项对应

| 关系 | 可选表达 | 何时使用 |
|---|---|---|
| 同句直接对照 | `X increases, whereas Y remains unchanged.` | 两个对象结构严格平行 |
| 新句对照 | `In contrast, X ...` | 前后结论较长，需独立成句 |
| 指定比较基准 | `Compared with X, Y exhibits Z.` | 基准明确且比较维度一致 |
| 排除另一选择 | `X follows A rather than B.` | 数据能区分互斥路径或解释 |
| 判断主导因素 | `X is dominant over Y under Z.` | 已分别量化两个因素的贡献 |
| 一一对应 | `A and B correspond to X and Y, respectively.` | 项目数量和顺序完全一致 |

非时间关系的对比用 `whereas` 优于含糊的 `while`。

## 解释机理与因果

| 因果强度 | 可选表达 | 何时使用 |
|---|---|---|
| 直接机理来源 | `X stems from Y.` | 有计算、实验或理论链支撑 |
| 可能起源 | `X may arise from Y.` | 存在多个候选来源 |
| 归因于已知因素 | `X is attributed to Y.` | 引用或既有模型支持该解释 |
| 普通因果 | `X occurs because of Y.` / `X is due to Y.` | 因果已被单独验证，不只是相关 |
| 促进过程 | `X facilitates Y.` / `Y is facilitated by X.` | 降低能垒或增加可达性 |
| 阻碍过程 | `X hinders Y.` / `Y is hindered by X.` | 抑制转变、输运或响应 |
| 分离贡献 | `The change in X solely corresponds to the contribution from Y.` | 控制变量足以隔离单一贡献 |

不要由同步变化直接写 `is due to`。只有相关性时用 `is associated with`。

## 选择逻辑连接语

| 功能 | 推荐表达 | 使用条件 |
|---|---|---|
| 转折或限制 | `However, ...` | 后句修正、限制或反驳前句 |
| 句间对照 | `In contrast, ...` | 明确比较两个对象或方法 |
| 同句对照 | `whereas ...` | 两个平行分句 |
| 增加独立证据 | `Furthermore, ...` / `Moreover, ...` | 后句新增证据，不是同义重复 |
| 具体化 | `Specifically, ...` / `In particular, ...` | 后句给数字、条件或代表性案例 |
| 强化前述解释 | `Indeed, ...` | 后句直接验证前句，不只是继续叙述 |
| 局部综合 | `Overall, ...` | 汇总紧邻数据后给受限结论 |
| 真正更重要 | `More importantly, ...` | 后句在论证层级上确实更关键 |

`Interestingly`、`Surprisingly` 只在结果相对基准或普遍预期确实反常时使用，且不能代替机理解释。同一段不堆叠多个同功能连接词。

## 表达不确定性与限制

| 判断状态 | 可选表达 | 何时使用 |
|---|---|---|
| 较强概率判断 | `X is likely to Y.` | 多项迹象一致但未直接验证 |
| 较弱候选判断 | `X might be Y.` | 证据更弱或存在多个等价解释 |
| 防止过度解释 | `The agreement might be only a coincidence.` | 数值吻合但变量并非严格对应 |
| 排除不足因素 | `X cannot be explained by Y alone.` | 定量结果已证明该因素不足 |
| 明确后续工作 | `X needs further investigation using Y.` | 能指出缺少的具体模型或实验 |
| 保留未解问题 | `The question of how X occurs remains to be answered.` | 结论尚不足以解释机理 |

## 给出有边界的意义

| 意义类型 | 可选表达 | 何时使用 |
|---|---|---|
| 开启研究路径 | `These results open up new ways to investigate X.` | 方法或现象确实使新研究成为可能 |
| 奠定概念基础 | `These findings provide a foundation for X.` | 本工作构成后续研究或操控的依据 |
| 给出实践指导 | `These findings offer guidance for X.` | 结果可转化为设计、制备或实验选择 |
| 提供机制认识 | `This study provides insight into X.` | 主要贡献是理解而非直接应用 |

摘要或结论通常只保留一句意义。这四种对应不同贡献，不为求变化而轮换。

## 不掺模型腔

以下是模型写作的识别特征，在英文正文里默认不用；目标稿原本就在用、且用得准确时才跟随。

**不用的词**——LLM excess-vocabulary 清单中，在 `../p-article-polishing/ref/` 五篇论文里零出现的部分：

`delve, underscore, showcase, leverage, harness, foster, bolster, catalyze, unearth, illuminate, navigate, scrutinize, transcend, boast, embark, grapple, juxtapose, encompass, emphasize`；
`intricate, meticulous, pivotal, nuanced, multifaceted, groundbreaking, innovative, transformative, invaluable, commendable, renowned, exhaustive, actionable`；
`additionally, notably, seamlessly, profoundly, strategically, thoughtfully, undoubtedly, accurately`；
`realm, tapestry, testament, journey, milestone, ecosystem, prowess, essence, intricacy, utilization`；
`shed light on, deep dive, game changer, vital role, knowledge gap`。

清单**按词形严格生效，不外扩到同根词**：不用的是句首的 `Additionally`（参考论文 0 次），而 `in addition`（7 次）和 `additional`（11 次）正常使用；不用的是 `accurately`（0 次），而 `accurate`、`accuracy`（共 4 次）不受限。同理只约束表中列出的那个词形。

**有确切技术所指才用**：`align`、`complex`、`surpass`、`unveil`、`necessitate`、`noteworthy`、`versatile`、`deeper`、`advancement`。这些在参考论文里出现过，用于 `aligned lattice`、`complex oxide` 这类实指没问题，不用作泛化的强调。`landscape` 在 `energy landscape` 中正常使用，不受限。

**标点**：优先逗号，其次句号，分号少用。

- 不用破折号（`—`、`–`）插入解释或补充说明，改逗号或拆成两句。这里说的是破折号，不是连字符：术语构词里的 `-`（`FCC- and HCP-`、`low-SFE`、`out-of-plane`）是作者约定，保留不动。
- 冒号尽量不用于句中引出解释或列举，同样改逗号或拆句。图注编号、比值、公式或标题里的固定写法不受影响。

反向不成立：`critical`、`crucial`、`fundamental`、`remarkable`、`universal`、`It is worth noting` 不是禁用词，判据是有没有数字、引用或清楚逻辑支撑。
