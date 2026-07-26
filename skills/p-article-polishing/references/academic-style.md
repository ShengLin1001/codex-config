# 学术表达语料库

本文件从 [corpus-index.md](corpus-index.md) 的本地论文中提炼可复用表达。它回答的不是“哪个词永远更高级”，而是“当前修辞功能和证据强度下，哪种表达更准确”。来源标签表示可追溯的语料模式，不表示逐字引文。

## 目录

- [状态与使用方法](#状态与使用方法)
- [建立背景与重要性](#建立背景与重要性)
- [指出研究空白](#指出研究空白)
- [引出本文目的与路线](#引出本文目的与路线)
- [描述方法与验证](#描述方法与验证)
- [定位图表与报告定量结果](#定位图表与报告定量结果)
- [选择证据动词](#选择证据动词)
- [比较、对照与逐项对应](#比较对照与逐项对应)
- [解释机理与因果](#解释机理与因果)
- [选择逻辑连接语](#选择逻辑连接语)
- [表达不确定性与限制](#表达不确定性与限制)
- [给出有边界的意义](#给出有边界的意义)
- [高频 A→B 选择](#高频-ab-选择)
- [段落与章节组合](#段落与章节组合)
- [使用限制](#使用限制)

## 状态与使用方法

- `confirmed`：历史修订或用户确认的个人规则；以 [personal-style.md](personal-style.md) 为准。
- `repeated`：至少两个独立语料来源支持，可作为默认候选。
- `candidate`：一个来源中的有效表达，可按语义选用，但不自动升级为个人规则。

使用时：

1. 先判断句子承担的功能：背景、空白、目的、结果、比较、机理、限制或意义。
2. 再判断证据强度：直接观察、模型解释、间接迹象、独立验证或推测。
3. 从相应表格选择语义匹配的写法，并替换 `X/Y/A/B`；不要按词表全局替换。
4. 同一段不要堆叠多个同功能连接词或意义句。
5. 目标稿、期刊体例和 `personal-style.md` 高于本表达库。

## 建立背景与重要性

避免只写 `X is very important.`。优先说明重要在哪里、为什么重要或难在哪里。

| 意图 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 长期研究主题 | `X has long been a central topic in Y.` | 有充分文献支持长期关注时 | R4, `candidate` |
| 持续研究投入 | `Considerable experimental and theoretical effort has been directed at X.` | 同时概括实验与理论进展时 | R1、R2, `repeated` |
| 尚未解决的难题 | `Achieving X remains an ongoing challenge.` | 强调目标困难，而不是知识未知时 | R1、R3, `repeated` |
| 说明具体重要性 | `X is particularly important because it is related to Y.` | 能明确给出性质、机制或应用后果时 | R2, `candidate` |
| 从应用与科学双重定位 | `For both scientific and technological reasons, X remains ...` | 两类价值都能被正文或引文支撑时 | R1, `candidate` |

`central topic`、`important` 或 `challenge` 后面必须有引用、事实或具体原因，不能只承担气氛渲染。

## 指出研究空白

不同表达对应不同类型的“未知”，不能互换。

| 空白类型 | 可选表达 | 语义边界 | 来源与状态 |
|---|---|---|---|
| 已研究 A，但不了解 B | `X has been widely studied; however, little is known about Y.` | 最适合建立明确的已知—未知对照 | R2, `candidate` |
| 文献中尚无报道 | `To the best of our knowledge, X has not been reported.` | 只有完成可靠检索后使用 | R2、R5, `repeated` |
| 研究领域基本未触及 | `X remains unexplored.` / `X remains nearly unexplored.` | `nearly` 表示已有少量相关工作 | R3、R5, `repeated` |
| 机理研究不足 | `The mechanism governing X remains insufficiently investigated.` | 已有现象或结果，但机理证据不充分 | R4, `candidate` |
| 缺少实验证明 | `Experimental evidence for X remains missing.` | 理论或间接迹象已有，但实验验证缺失 | R1, `candidate` |
| 具体问题尚待回答 | `Whether X controls Y remains unresolved.` / `How X controls Y remains to be determined.` | 用于可直接被本文回应的问题 | R4, `candidate` |
| 测量本身困难 | `Measuring X remains an experimental challenge because Y.` | 空白主要来自方法或分辨率限制时 | R2, `candidate` |

比起含糊的 `X is not well studied`，优先说明缺的是报道、知识、机理、实验验证还是测量能力。

## 引出本文目的与路线

| 写作动作 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 中性报告 | `Here, we report on X.` | 介绍测量、数据集或现象，不提前强化结论 | R2, `candidate` |
| 方法导向 | `Here, we use A and B to investigate X.` | 需要同时点明方法组合和研究对象 | R1, `candidate` |
| 结果导向 | `Here, through X, we show that Y.` | 摘要中直接给出核心发现 | R1、R5, `repeated` |
| 推进已有方法 | `In this work, we advance X to Y.` | 确实扩展了方法能力或应用范围 | R3, `candidate` |
| Letter 体例 | `In this Letter, we show that X.` | 仅限目标期刊采用 Letter 体例 | R3, `candidate` |
| 机理导向 | `Herein, X and Y are employed to elucidate Z.` | 多种手段共同解释物理来源或机理 | R4, `candidate` |
| 重新检验问题 | `In this study, we revisit X using Y and validate the result with Z.` | 对已有结论重新评估并有独立支持 | R4, `candidate` |

选择原则：

- `report` 最中性；
- `investigate` 说明研究动作，不预设结果；
- `show` 直接给核心发现；
- `elucidate` 只用于真正解释机理；
- `advance` 只用于真实的方法推进，不能代替普通的 `use`。

## 描述方法与验证

| 功能 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 说明计算框架 | `Calculations were performed within X, as implemented in Y, using Z.` | 软件、理论框架和关键近似需要同时交代 | R4, `candidate` |
| 说明实验动作 | `We used X to probe Y.` | 主体明确、动作直接时 | R1, `candidate` |
| 说明测量对象与条件 | `Measurements were carried out on X under Y.` | 方法已知，重点是对象和条件 | R3, `candidate` |
| 说明跨体系一致设置 | `X was employed across all geometries, maintaining Y.` | 参数需在不同模型间保持可比时 | R4, `candidate` |
| 统一口径 | `Unless otherwise specified, all results refer to X.` | 后文反复使用同一方向、基准或条件时 | R4, `candidate` |
| 测试参数敏感性 | `We tested X from A to B and used C without significant loss of accuracy.` | 参数未有文献值，需要说明选择稳健性 | R5, `candidate` |
| 验证计算参数 | `The computed X agrees well with previous theoretical and experimental results [refs], confirming the reliability of Y.` | 有明确比较量和文献结果时 | R4, `candidate` |

不要只写 `The method is reliable.`；必须给比较对象、结果和可靠性落点。

## 定位图表与报告定量结果

| 功能 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 图展示变量关系 | `Figure X shows Y as a function of Z.` | 图作句子主语并展示函数关系 | R2、R3、R4、R5, `repeated` |
| 图展示代表性结果 | `Figure X presents representative Y for A and B.` | 说明图中案例具有代表性 | R5, `candidate` |
| 报告起点与终点 | `X increases/decreases from A to B under C.` | 起点、终点和条件均已知 | R2、R3、R4, `repeated` |
| 报告变化量 | `X increases/decreases by A at B.` | 强调差值而不是端点 | R3, `candidate` |
| 报告范围 | `X ranges from A to B, depending on C.` | 数值随样品、条件或模型变化 | R1、R5, `repeated` |
| 报告极值 | `X reaches a maximum of A at B.` | 数据存在清楚极值 | R2, `candidate` |
| 对齐并列量 | `X and Y are A and B, respectively.` | 两组项目能够严格一一对应 | R1、R2、R4、R5, `repeated` |
| 给出物理解释 | `X increases with Y, suggesting Z.` | 趋势是直接数据，Z 是受限解释 | R3, `candidate` |

如果正文只写 `similar trends`，应补充相关材料、条件、panel 和代表性数值。

## 选择证据动词

这些动词不是文采替换，而是证据等级。

| 动词 | 推荐含义 | 可选模板 | 来源与状态 |
|---|---|---|---|
| `show` | 数据、图或实验直接呈现 | `Measurements show that X.` | R1、R2、R3、R5, `repeated` |
| `demonstrate` | 多项证据支持较强结论 | `Calculations demonstrate that X controls Y.` | R3、R4、R5, `repeated` |
| `reveal` | 揭示此前不可见的结构、关系或路径 | `Further analysis reveals that X.` | R3、R4、R5, `repeated` |
| `indicate` | 数据支持解释，但不是唯一证明 | `The results indicate that X stems from Y.` | R1、R2, `repeated` |
| `suggest` | 间接、模型依赖或仍有不确定性 | `The calculations suggest that X may control Y.` | R1、R2, `repeated` |
| `confirm` | 独立手段验证前一结果 | `Measurements confirm the accessibility of X.` | R3、R4, `repeated` |

避免把 `prove` 当作默认结果动词。若只有相关性、计算趋势或间接迹象，使用 `indicate` 或 `suggest`；只有独立验证才能写 `confirm`。

## 比较、对照与逐项对应

| 关系 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 同句直接对照 | `X increases, whereas Y remains unchanged.` | 两个对象或条件结构严格平行 | R1、R2、R4, `repeated` |
| 新句对照 | `In contrast, X ...` | 前后结论较长，需独立成句 | R3, `candidate` |
| 指定比较基准 | `Compared with X, Y exhibits Z.` | 基准明确且比较维度一致 | R2、R3、R4、R5, `repeated` |
| 排除另一选择 | `X follows A rather than B.` | 数据能够区分互斥路径或解释 | R4、R5, `repeated` |
| 判断主导因素 | `X is dominant over Y under Z.` | 已分别量化两个因素贡献 | R4, `candidate` |
| 一一对应 | `A and B correspond to X and Y, respectively.` | 项目数量和顺序完全一致 | R1、R2、R4、R5, `repeated` |

`whereas` 比含糊的对比性 `while` 更适合非时间关系；`respectively` 不能补救顺序不清或项目数量不一致。

## 解释机理与因果

| 因果强度 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 直接机理来源 | `X stems from Y.` | 有计算、实验或理论链支撑 | R1, `candidate` |
| 可能起源 | `X may arise from Y.` | 存在多个候选来源 | R4、R5, `repeated` |
| 归因于已知因素 | `X is attributed to Y.` | 引用或既有模型支持该解释 | R3, `candidate` |
| 普通因果 | `X occurs because of Y.` / `X is due to Y.` | 因果已被单独验证，不只是相关 | R1、R3、R5, `repeated` |
| 促进过程 | `X facilitates Y.` / `Y is facilitated by X.` | 因素降低能垒或增加可达性 | R1、R4, `repeated` |
| 阻碍过程 | `X hinders Y.` / `Y is hindered by X.` | 因素抑制转变、输运或响应 | R1, `candidate` |
| 分离贡献 | `The change in X solely corresponds to the contribution from Y.` | 控制变量足以隔离单一贡献 | R4, `candidate` |

不要由同步变化直接写 `is due to`。相关性优先用 `is associated with`；受限解释用 `indicate`、`suggest` 或 `may arise from`。

## 选择逻辑连接语

| 功能 | 推荐表达 | 使用条件 | 来源 |
|---|---|---|---|
| 转折或限制 | `However, ...` | 后句修正、限制或反驳前句 | R1–R5 |
| 句间对照 | `In contrast, ...` | 明确比较两个对象或方法 | R3 |
| 同句对照 | `whereas ...` | 两个平行分句 | R1、R2、R4 |
| 增加独立证据 | `Furthermore, ...` / `Moreover, ...` | 后句新增证据，不是同义重复 | R1、R3、R5 |
| 具体化 | `Specifically, ...` / `In particular, ...` | 后句给数字、条件或代表性案例 | R1、R4 |
| 强化前述解释 | `Indeed, ...` | 后句直接验证前句，不只是继续叙述 | R1、R2 |
| 局部综合 | `Overall, ...` | 汇总紧邻数据后给受限结论 | R2 |
| 真正更重要的结果 | `More importantly, ...` | 后句在论证层级上确实更关键 | R4 |

`Interestingly` 和 `Surprisingly` 只在结果相对基准或普遍预期确实反常时使用；不能代替机理解释。

## 表达不确定性与限制

| 判断状态 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 普通可能性 | `X may arise from Y.` | 有合理来源但未量化贡献 | R4, `candidate` |
| 较强概率判断 | `X is likely to Y.` | 多项迹象一致但未直接验证 | R3、R4、R5, `repeated` |
| 较弱候选判断 | `X might be Y.` | 证据更弱或存在多个等价解释 | R2、R4、R5, `repeated` |
| 防止过度解释 | `The agreement might be only a coincidence.` | 数值吻合但变量并非严格对应 | R2, `candidate` |
| 排除不足因素 | `X cannot be explained by Y alone.` | 定量结果已证明 Y 不足 | R4, `candidate` |
| 明确后续工作 | `X needs further investigation using Y.` | 能指出缺少的具体模型或实验 | R4, `candidate` |
| 保留未解问题 | `The question of how X occurs remains to be answered.` | 结论尚不足以解释机理 | R4, `candidate` |

不要把同一句同时堆成 `may possibly be likely to`。选择一个与证据相称的限定词。

## 给出有边界的意义

| 意义类型 | 可选表达 | 何时使用 | 来源与状态 |
|---|---|---|---|
| 开启研究路径 | `These results open up new ways to investigate X.` | 方法或现象确实使新研究成为可能 | R1, `candidate` |
| 奠定概念基础 | `These findings provide a foundation for X.` | 当前工作形成后续研究或操控的依据 | R4, `candidate` |
| 给出实践指导 | `These findings offer guidance for X.` | 结果可转化为设计、制备或实验选择 | R4, `candidate` |
| 提供机制认识 | `This study provides insight into X.` | 主要贡献是理解而非直接应用 | R5, `candidate` |

摘要或结论通常只保留一句意义。`insight`、`foundation`、`guidance` 和 `open up new ways` 对应不同贡献，不能为了变化而轮换。

## 高频 A→B 选择

这里的 A 是常见但信息不足的写法；B 不是固定替换，而是应按右栏语义选择。

| A：较弱或含糊 | B：更精确的选择 |
|---|---|
| `X is very important.` | `X is particularly important because Y.` / `X has long been a central topic in Y.` |
| `X is not well studied.` | `little is known about X` / `X remains unexplored` / `the mechanism remains insufficiently investigated` / `experimental evidence remains missing` |
| `We did X to study Y.` | `we use X to investigate Y` / `we report on X` / `through X, we show that Y` / `we advance X to Y` |
| `The results prove that X.` | `show`（直接结果）/ `indicate`（受限解释）/ `suggest`（较弱推断）/ `confirm`（独立验证） |
| `X is larger than Y.` | `X increases from A to B` / `X is A times as large as Y under C` / `X exceeds Y by A%` |
| `X and Y are different.` | `whereas`（同句对照）/ `In contrast`（句间对照）/ `Compared with`（指定基准） |
| `X may be due to Y.` | `stems from`（机理充分）/ `is attributed to`（已有解释）/ `may arise from`（候选来源）/ `is associated with`（仅相关） |
| `This result is meaningful.` | `provides insight into` / `provides a foundation for` / `offers guidance for` / `opens up new ways to investigate` |

## 段落与章节组合

不要机械套固定句数，只保证证据链完整。

### Abstract

`重要对象或问题 → 具体空白 → 本文行动 → 最重要的定量结果 → 机理或独立验证 → 一句有边界的意义`

### Introduction

`背景与代表性证据 → 明确空白 → 可回答的问题 → 本文方法与路线`

文献例子必须说明对象、方法或结论与本文问题的关系，不只堆作者名单。路线图只在目标稿需要时使用。

### Results

`Figure/panel 定位 → 条件和定量趋势 → 基准或对照 → 证据强度匹配的解释 → 段尾结论`

比较多个材料、条件或 panel 时逐项覆盖。主结果编号是否使用，服从 `personal-style.md` 的条件性规则。

### Discussion

`核心关系 → 多结果的统一机理 → 与已有研究比较 → 候选来源及其证据 → 限制或待验证贡献 → 有边界的综合`

已在 Results 中排除的因素，不得无新证据重新设为主因。

### Conclusion

`研究对象与方法 → 按正文顺序概括主结果和关键数字 → 机理或验证结论 → 一句意义`

不引入新数据、新引用或新因果。

### Figure captions

首句说明整图功能，随后按 `(a) ... (b) ...` 覆盖 panel，并解释颜色、线型、符号、箭头、插图和统计量。图注描述图中内容；机理讨论留在正文。

## 使用限制

- 不复制参考论文的长句或整段文字；只复用短表达和修辞功能。
- 来源标签代表模式可追溯，不代表导师亲自修改了该句。
- `candidate` 可以使用，但不能表述为 PJ 已确认的全局偏好。
- 不把 DFT、HRTEM、FCC/HCP 等领域词汇套到无关学科。
- 不机械套固定章节模板，不为覆盖表达库而堆叠同义句。
- 不改变目标稿的数据、单位、引文、术语、因果或限定条件。
