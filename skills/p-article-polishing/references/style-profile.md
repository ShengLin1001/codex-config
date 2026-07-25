# PJ 科研论文写作风格规范

## 一句话风格

PJ 的文章以明确的物理问题为主线：先定义对象和判据，再用定量结果建立趋势，随后解释机理，最后给出有边界的结论。语言服务于论证，不追求华丽或“像 AI 的高级表达”。

## 核心声音

四个关键词：**直接、机理化、定量、克制**。

- 直接：一句话只承担一个主要逻辑动作，避免长句中连续插入定义和转折。
- 机理化：写清“条件改变 → 哪个物理量改变 → 能量景观/结构如何响应 → 结论”。
- 定量：关键趋势配代表性数值、基准和条件，不让读者从图中自行换算。
- 克制：结论强度与证据一致，不靠 `remarkable`, `perfect`, `universal` 等词制造重要性。
- 连贯：段落之间通过研究问题、变量或上一段结论连接，不靠空泛过渡词拼接。
- 可核对：关键判断能立即回到图、表、公式、数据或引用。

## 稳定写作偏好

### 1. 先消除概念歧义

- 首次出现时定义术语、符号、参考态和正负方向；
- 同一段不要用多个近义词指同一物理量；
- 若两个概念不同，必须显式区分，不能依赖上下文让读者猜。
- 明确区分 surface-induced strain 与 externally applied strain、uniform strain 与 equal-biaxial strain。
- `intersection`、`correlation`、`γ-line`、energy gap 等抽象名词必须说明相交对象、关联量、路径或参考态。

### 2. 把复杂定义拆成顺序清楚的句子

首选“列出对象，再逐一定义”的结构：

> The first is the energy difference between the two phases, which determines the direction of the transition driving force. The second quantity is the energy barrier, which represents the maximum obstacle to be overcome for the phase transition.

- 先报数量或对象，再逐个定义；
- 公式紧跟定义；
- 定义完成后再进入文献背景或结果解释。

### 3. 摘要必须短，但不能丢掉定量锚点

若期刊没有更严格要求，摘要尽量控制在 200 词左右，并按以下顺序组织：

1. 研究对象与具体缺口；
2. 方法；
3. 决定性因素和临界条件；
4. 实验/计算互证；
5. 动力学或机理解释；
6. 有边界的意义。

压缩时优先删除宣传语、重复方法和同义结论，不先删阈值、代表性数据与限制条件。

### 4. 不让读者自己计算或猜图

每个关键结果至少包含：

- 对象和条件；
- 基准值；
- 变化后的代表值或幅度；
- 趋势的物理解释；
- 对应的 figure panel。

不要要求读者从 lattice constant 自行计算应变。多材料比较需给出各材料的代表性数据；正文引用的每个 panel 都要说明。图注逐 panel 写清数据类型、符号、颜色、open circle 等特殊标记和约束条件。

### 5. 章节结构服从论证，不服从素材堆积

稳定结构是：

- 先建立参考态和定义；
- 再区分竞争因素；
- 再给扩展能量景观或参数扫描；
- 最后讨论动力学、机理和实验意义。

段落若只是在展示结构信息或方法细节，不得提前宣称它已经证明主机制。

### 6. Discussion 深化结论，不能反转结论

- Discussion 先复述需要解释的已证结果；
- 再说明机制、适用边界、反例或推广；
- 如果新解释改变前文因果，必须同步回查摘要、Results、图和结论，不能只润色 Discussion。
- Discussion 可以提高文章深度，但不能为了制造“新见解”推翻前文已建立的因果链。

### 7. 引用必须紧贴外部事实

- 他人实验或计算结果；
- 材料的一般行为、阈值或性能；
- 方法选择的可靠性；
- 机理的既有解释；
- “与实验一致”或“已被报道”的判断。

不得为了补齐引用而虚构文献。缺少可确认来源时标记 `AUTHOR CHECK: citation needed`。

### 8. 连字符属于正确的作者风格

- 保留 PJ 已使用的连字符与悬挂连字符，不得把它们标记为语法错误。
- `FCC- and HCP- phases`、`thermodynamic- and kinetic- mechanisms` 这类写法是有意风格，不改写为其他结构。
- 保留 `low-SFE`、`strain-induced`、`out-of-plane`、`phase-transition` 等复合修饰语的连字符。
- 不因语言模型或通用 linter 的偏好批量移除、添加或替换连字符。
- `FCC-HCP` 表示体系或无方向关系，`FCC→HCP` 表示有方向的转变；这是语义区别，不是标点纠错。
- 仅当同一术语在当前稿件内部写法冲突，或连字符确实改变科学含义时，才提出 `AUTHOR CHECK`，不要直接修改。

### 9. 语法检查不能被科学修改挤掉

- 最后一遍必须独立检查冠词、单复数、主谓一致、介词、时态、标点和复合形容词；
- 避免 contraction，如 `it's`；正式正文用 `it is`；
- 避免 `Herein this work` 等重复结构；
- 语法修正不得顺带改动已经确认的连字符、术语、符号和科学含义。

## 推荐段落骨架

### Results

1. 开头句给本段结论；
2. 指向 figure panel 和条件；
3. 给基准与代表性数值；
4. 比较不同材料、方向或约束；
5. 用一到两句解释机理；
6. 必要时用末句连接下一段。

### Discussion

1. 明确要解释的已证观察；
2. 给因果链；
3. 用数据或文献排除替代解释；
4. 说明适用范围与限制；
5. 回扣文章主线。

### Figure caption

1. 一句话说明整图目的；
2. 逐 panel 说明对象和操作；
3. 定义颜色、线型、符号和特殊标记；
4. 说明单位、归一化和约束；
5. 区分 calculated、measured、fitted、interpolated。

## 应避免的 AI 味

- 空泛开场：`has long been a central topic`, `has attracted tremendous attention`；
- 过度评价：`remarkable`, `perfect candidate`, `universal mechanism`；
- 没有指向的连接：`This correlation`, `These effects`, `It is worth noting`；
- 同义反复：连续使用 `modulate`, `regulate`, `reshape` 却没有新增信息；
- 假精确：用复杂句式掩盖未定义的参考态、阈值或因果；
- 机械重写：整段替换后引入新的数字矛盾、术语漂移或引文错位。

## 最终判断标准

满意的润色应让作者能够回答：

- 每段只读首句，能否看见完整论证主线？
- 每个关键结论能否立即找到数据、图或引用？
- 术语和符号是否不需要猜？
- 语言是否比原文更短、更准确，而不是更花哨？
- 修改是否保留了作者真正想说的科学内容？
