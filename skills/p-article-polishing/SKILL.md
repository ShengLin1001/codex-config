---
name: p-article-polishing
description: PJ 写英文科研论文（DFT / 相变 / 力学类 Acta 风格）时的固定写作风格约束。当为 PJ 润色、改写、扩写或从零写论文正文、摘要、引言、方法、结果、Discussion、结论、图注、审稿回复时使用。规则已从 PJ 两篇已接收论文的定稿和导师多轮修订中提炼并内联于此，开箱即用，无须再读修订记录或额外文件。
---

# P Article Polishing

润色或写 PJ 的论文时，**初稿就按下面写**，别等导师返工。
下面每条都来自 PJ 已接收定稿 + 导师（Yang Gao）反复提出的同类修改，直接遵守即可。

**只负责正文语言与结构。** 不改数据、机理、数值、单位、引文键、公式；
不做 Word 修订合并、格式转换、参考文献整理。含义有歧义就问，别用流畅措辞盖过去。

**按改动规模裁剪**：改一句只取适用条款（记号、数字三件套、指代明确）；
整节重写或新写才走"全文骨架"和自检全套。别给小改动套重流程。

## 最常见的返工点（别犯）

给了晶格常数不给应变（"你不能让读者自己去算应变"）· 符号/术语没定义就用（"a′ 是什么？还是没有解释"）·
断言没引文（"参考文献"）· 断言没图号（"Where?"）· 描述图漏 panel（"为什么完全没有对图 8a 和 b 的描述？"）·
论证走回头路（"怎么又绕回到 surface effect 了？？？？"）· 同一结论在引言/小节尾/Discussion/结论重复四遍（"redundant"）·
段首先下结论再摆数据 · 图段落缺总起句（"总起句：fig6 做了啥"）· 术语中途漂移（surface effect↔surface effects）·
把 `FCC- and HCP- phases` 的悬挂连字符"修正"掉 · 用 `FCC-to-HCP` · 句首写 `Fig.` · `et al` 漏点号。

## 约束

**记号（机械规则，逐条可检，不要凭通用语法/linter 改）**

- 有方向的转变用箭头：`FCC→HCP phase transition`、`FCC→9R→HCP`、`HCP-to-FCC` 一律写成 `→`。**禁止 `FCC-to-HCP`**。
  无方向的并称保留连字符：`FCC-HCP phase transition`、`HCP-FCC energy difference`。
- **悬挂连字符：并列修饰语每一项都留连字符 + 后跟空格**，这是 PJ 已确认的作者风格，任何情况下不得规范化：
  `FCC- and HCP- phases`、`thermodynamic- and kinetic- mechanisms`、`stepwise- and concerted- transitions`、
  `bulk- and slab- cases`、`Mo- and W- dichalcogenide monolayers`、`HCP- and FCC- slabs`。
- 其他已确认写法照抄：`low-SFE`、`in-plane` / `out-of-plane`、`close-packed`、`strain-induced`、`phase-transition pathway`、
  `24-atomic-layer`、`7.6-nm-thick`、`equal-biaxial`、`γ-line`、`Γ-centered`、`−ICOHP`。
- 负号用 `−`（U+2212）不用连字符：`−2.9%`、`−0.3%`、`10−8 eV/supercell`、`2π/81 Å−1`。
- 二元运算符两侧留空格：`i = 0`、`a// = 2.8 Å`、`c/a ≈ 1.6`、`strain < 3%`、`8 × 8 grid`、`≈ 5.4 nm`。
  `~` 贴数字：`~2.8 Å`、`~6.0 GPa`；区间 `2~3%`。
- 单位写斜杠形式：`meV/atom`、`mJ/m2`、`J/m2`、`meV/Å`（**不写** `meV per atom`）。
- 图：图作句子主语时拼全 `Figure 3(d) shows ...` / `Figures 7(g-i) present ...`；在介词短语里用缩写 `as shown in Fig. 3(d)`。
  panel 一律带括号（不写 `Fig. 3d`）；连续 panel 用区间 `Figs. 7(a-b)`、`Figs. 8(d-f)`；不连续才并列 `Figs. 2(e) and 2(h)`。
- 章节引用大写 `Section`：`as discussed in Section 3.1`、`presented in Appendix B`、`Fig. S5`、`Table 3`。
- 缩写首次出现给全称 + 括号，之后只用缩写：`density functional theory (DFT)`、`atomic-level precision chemical etching (ALPE)`、
  `climbing image nudged elastic band (CI-NEB)`、`generalized stacking fault energy (GSFE)`、`negative integrated crystal orbital
  Hamilton population, −ICOHP`。文献作者一律 `Huang et al.`（有点号）。
- 时态：方法章全篇统一（定稿两篇分别用过 `calculations were performed` 和 `are performed`），**跟随目标稿已有时态，不要单方面翻**；
  结果章描述图表用现在时（`Figure 3(d) shows`），描述所做操作用过去时（`we performed HRTEM measurements`）。

**每个断言的三件套：数字 + 出处 + 图号**

- 只要给了原始量就同时给派生量，反之亦然。读者不许自己换算：
  `as a// decreases from the equilibrium value (2.88 Å) to 2.8 Å (compressive strain of 2.9%), γusf decreases from 89.2 to 31.5 mJ/m2`
  `a critical in-plane compressive strain of 2~3% (corresponding to a lattice constant of ~2.8 Å)`
- 变化量写"从→到"，别只写终值：`ΔEH−F drops from 8.6 meV/atom to 6.1 meV/atom`；只有量级时写 `drops slightly by 0.2 meV/atom`。
- 并列量按 1:1 顺序对应并以 `respectively` 收尾：
  `the critical a// values are ~2.8 Å (Au), ~2.3 Å/~2.7 Å (Cu), and ~2.7 Å/~3.1 Å (Ag), which correspond to critical
  strain thresholds of −3% (Au), −8.6%/7.2% (Cu), −6.7%/7.1% (Ag), respectively`
- 凡涉及他人工作、材料体系、实验事实、"long-standing / widely reported / has been reported" 的句子，句末必须有 `[n]` 或 `[n-m]`。
  强调词（`remarkable`、`universal`、`fundamental`、`central topic`）本身不禁用——定稿里就有——**但必须由引文或数字兜住**。
- 凡是"我们观察到/计算表明/与预测一致"的句子，必须落到具体 panel：`consistent with the DFT predictions in Fig. 4(a)`。
- 图里的每个视觉元素都要在正文点名：`Arrow #1 in Fig. 3(d) denotes ...`、`The blue dashed line in Fig. 3(d) represents ...`、
  `marked with a star in Fig. 4(b)`、`highlighted by the black dashed boxes in Figs. 7(d-f)`。一个图有几个 panel 就都要提到。
- 符号首次出现即定义，并且全文不改名：`the in-plane lattice constant a// represents the nearest-neighbor atomic distance
  within the close-packed plane; the out-of-plane lattice constant a⊥ is defined as t/(n-1) for n-layer films, where t denotes
  the slab height`。术语同理：`surface effect` 就一直是 `surface effect`，不要换成 `surface effects`/`surface-induced effect`。

**段落怎么写**

- 一段一件事，段首是总起句（这段/这张图在干什么），中间摆证据和数字，**结论放段尾**用 `Thus, / Therefore, / Overall, ` 引出：
  `Therefore, equal-biaxial compression is the most preferred strain type for the FCC→HCP phase transition in Au.`
- 多步流程拆成独立成段的编号步骤，每步末尾说清这步单独归因于什么：
  `Step 1: reduce the film thickness from bulk and fix the in-plane lattice constants ... In this step, no in-plane strain is
  applied, meaning any reduction of ΔEH−F solely corresponds to the contribution from the thickness variation.`
- 小节开头写一句承上，结尾写一句启下，把推迟处理的问题指到具体章节：
  `As discussed in Section 3.1, the thickness-dependent intrinsic strain significantly reduces ΔEH−F but the FCC phase remains
  the ground state. ... The possible origin of the additional in-plane strain is discussed in Section 4.`
- 每个结果小节用一句话收口，**不要写整段总结重复已说过的话**：`To summarize Section 3.3.1, in-plane compressive strain can
  effectively facilitate ... via the modification of the stacking fault energy and slip system activation.`
- 论证单向推进：某个因素被判定为次要（如 thickness variation、surface effect 不足以翻转能量）之后，后文不得再把它当主因回捞。
- 限制与不确定性直说，不藏：`The current CI-NEB simulation with limited size reveals the upper bound of the true transition
  barriers in reality. In other word, ... However, even with the limited size, the effect of the in-plane strain is clearly
  presented.`；推测用 `may arise from` / `are likely to constitute` / `might be` / `We believe this is the main reason why ...`。
- 需要点题时用 `In other words, ... ` / `More importantly, ... ` / `It's worth noting that ... `（定稿在用，不必回避），
  但每次只用来引出新信息，不用来重复上一句。

**用词与语感（导师改得最多的一层，别用通用"学术化"替换）**

- **不要引入 PJ 自己不用的词。** 下列词在 PJ 两篇定稿里零出现，属于 LLM 润色的典型指纹（Kobak et al. 的
  excess-vocabulary 清单去掉 PJ 在用的部分后剩下的）——润色时冒出来就说明是模型的口音，不是 PJ 的：
  `delve, underscore, showcase, leverage, harness, foster, bolster, catalyze, unveil, unearth, illuminate, navigate,
  necessitate, scrutinize, surpass, transcend, boast, embark, grapple, juxtapose, align, encompass, emphasize`；
  `intricate, meticulous, pivotal, noteworthy, nuanced, multifaceted, groundbreaking, innovative, transformative,
  invaluable, commendable, versatile, renowned, exhaustive, actionable, complex, deeper`；
  `additionally, notably(慎用), seamlessly, profoundly, strategically, thoughtfully, undoubtedly, accurately`；
  `realm, landscape(仅限 energy landscape), tapestry, testament, journey, milestone, ecosystem, prowess, essence,
  intricacy, advancement, utilization`；`shed light on, deep dive, game changer, vital role, knowledge gap`。
- **反过来，别把 PJ 在用的词当"套话"删掉**：`critical / crucial / fundamental / significant / essential / remarkable /
  universal / thereby / subsequently / primarily / effectively / facilitate / elucidate / employ / exhibit / emerge /
  driving force / In addition / In summary` 都在定稿里，保留。强调词要的是引文/数字兜住，不是换词。
- **名词化主语改成 by-doing + 主动动词**：`Precise manipulation of thermodynamic ground states has enabled the synthesis of
  unconventional metallic phases` → `By precisely tailoring thermodynamic ground states, unconventional metallic phases
  can be stabilized and synthesized`。
- **无主语观察句点名主体**：`It's observed that the energy surfaces intersect` → `We plot the intersection contour that
  follows ...` 或 `Figure 5(a) shows ...`。不用 `It is found that` / `It can be seen that`。
- **省略式压缩要展开写全两支**：`FCC exhibits ductility but limited strength, and vice versa for HCP` →
  `FCC phases exhibit excellent ductility but relatively limited strength, whereas HCP phases possess substantially
  higher strength at the expense of deformability`。
- **句首给定位状语**，别让句子裸着开始：`Among various approaches, ` / `In this context, ` / `In particular, ` /
  `Experimentally, ` / `In general, ` / `Specifically, ` / `More importantly, `。
- **弱动词短语换成单个准确动词**（导师原样改过的）：`helps make → contributes to making`、`chose → used`、
  `warrants → needs`、`likelihood → possibility`、`Lastly → Finally`、`Typically → In general`、`toward → towards`、
  `exceptional → excellent`。比值改百分数：`volume change ratio is 0.6` → `the volume shrinks by 60%`。
- **并列定义别塞进一句**：`There are two critical quantities: the energy difference, and the energy barrier` →
  `The first is the energy difference ΔEH−F ... The second quantity is the energy barrier EBarrier ...`。
- 语域到"清楚准确"为止，不追求文采：句子普遍 20-35 词，一句一个逻辑动作，长定义按顺序拆句；不用生僻词提升"档次"。

**全文骨架（各章节的固定句式，照着填）**

- **Abstract**：①对象 + 为什么值得做（性质/应用，缩写就位）→ ②已知事实 + 空白：`..., but the fundamental mechanism governing
  the thickness-dependent FCC→HCP phase transition remains insufficiently investigated.` → ③`Herein, DFT calculations and
  HRTEM are employed to elucidate ...` → ④主结果带关键数字 → ⑤另一手段的印证（`HRTEM measurements confirm ...`）→
  ⑥机理/动力学结果 → ⑦一句话意义：`Our findings establish a foundation for ...`。不堆形容词，不写第二句意义。
- **Introduction（五段）**：
  1. 对象与近期进展，每个例子一句 + 引文 + 数字（`Huang et al. fabricated ... with a phase-transition thickness of ~2.4 to 6 nm [1]`），
     段末落到未解问题：`However, ... remains to be answered.`
  2. 领域层背景（`The modulation of metallic phases has long been a central topic in materials science [8-10, 12, 19-21]`）→
     早期/块体研究逐条带引文和数字 → 为什么低维/本体系不同 → 类比体系（Ti 膜、Fe、VO2、HEA、MD）各一句一引文 →
     最近的同门工作 + 它的边界（`Although this work provided important mechanistic insights, its conclusions were limited to ...`）。
  3. 读懂本文所需的结构/判据基础（两相原子排布、HRTEM 指纹、间距数值、术语口径约定：`Unless otherwise specified, all the
     results and discussion in this work refer to the Basal plane orientation.`）。
  4. 定义支配量（必要时给行间公式 `ΔEH−F = EHCP − EFCC,`）→ `Therefore, two critical questions emerge ... First, ... Second, ...`
     → `Thus, in this study, we ...` 按同一顺序逐条回应，并给出各自的落点（`... and demonstrate that intrinsic compressive strain
     is dominant over the thickness variation`）。三个以上关键量用 `(i) ... (ii) ... (iii) ...` 列。
  5. 路线图：`The remainder of this paper is organized as follows. In Section 2, we describe ... The effects of ... are discussed
     in Section 3.1. ... and summarize the work in Section 5.` 有子小节就写到子小节号。
- **Methodology**：一节一方法（DFT 参数 / supercell / tilted-cell / CI-NEB）；每个参数给数值 + 引文；末尾收一句验证：
  `The DFT parameters were validated in the bulk FCC state. The computed lattice constants, elastic constants and stacking fault
  energies agree well with previous theoretical and experimental results [39-42], as listed in Table 1, confirming the reliability
  of the DFT calculations.`
- **Results**：小节序 = 变量序（`Phase stability vs. thickness` → `vs. in-plane strain` → `Kinetics vs. in-plane strain`）。
  主结果小节末尾明确编号：`This is the first main result of this paper.`（第二、第三节同理）。这是 PJ 两篇定稿都在用的标志性写法，别删。
- **Discussion**：`To sum up, we have elucidated ...` → 用 `(i) / (ii)` 把机理拆开 → `In fact, ...` 打通量与量的关系 →
  `From the perspective of electronic structure, ...` → 指出仍不清楚的点 → `Herein, we propose several possible origins of ...` →
  每个候选来源一段（文献 + 数字 + 它在图里怎么画）→ `To summarize, ... are likely to constitute ... However, the contributions of
  these origins and the underlying mechanisms require further investigations.`
- **Conclusion**：`In this work, we investigate ... using DFT calculations. Our results demonstrate that ...` → 按正文顺序复述各主结果
  （每条带关键数字）→ 一句话展望：`These findings provide a foundation for ... and offer guidance for ...`。不引入新数据、新引文。
- **图注**：`Fig. 3. The structural parameters of ...` 首句给图做什么，然后逐 panel `(a) ...`，符号在图注里也要解释一遍。

## 交付前自检

- [ ] 每个晶格常数/能量都配了应变或百分比；变化量写了"从→到"；并列量用 `respectively` 对齐。
- [ ] 每个涉及他人工作或"广泛报道"的句子都有 `[n]`；每个观察/一致性判断都有 `Fig. x(y)`。
- [ ] 每个符号、缩写、术语在首次出现处定义，全文没换名；`surface effect` 之类单复数没漂移。
- [ ] 提到的图，panel 一个不漏；图里的箭头/虚线/星号/方框都在正文点名。
- [ ] 悬挂连字符原样保留（`FCC- and HCP- phases`）；无 `FCC-to-HCP`；负号是 `−`；单位是 `meV/atom`。
- [ ] 句首 `Figure`、句中 `Fig.`；连续 panel 用 `Figs. 7(a-b)`；`Section` 大写；`et al.` 带点。
- [ ] 段首是总起句、结论在段尾用 `Thus/Therefore/Overall` 引出；多步流程写成 `Step 1/2/3` 独立段并各自归因。
- [ ] 每个结果小节一句话收口；主结果标了 `This is the N-th main result of this paper.`；没有重复的整段总结。
- [ ] 论证没有回头路；被判次要的因素后文没被重新当主因。
- [ ] 限制和推测用了 `may / likely / might / We believe`，没有超出证据的断言。
- [ ] 没有引入禁用表里的词（`delve / underscore / intricate / meticulous / pivotal / realm / showcase / shed light on ...`）；
      也没有把 PJ 在用的 `critical / crucial / fundamental / remarkable` 当套话删掉。
- [ ] 没有名词化主语堆叠、没有 `It is found/observed that`、没有 `vice versa` 式省略；句首有定位状语。
- [ ] 数据、数值、单位、引文键、公式、术语口径与原稿一致；改动仅限语言与结构；存疑处已列出待 PJ 确认，而非自行编圆。
