---
name: p-article-latex
description: "ALWAYS invoke BEFORE writing, converting, or editing a journal manuscript or SI in LaTeX for PJ, including a small layout tweak, a colour toggle, or just recompiling the PDF. Do NOT touch a manuscript .tex without loading this skill first. 触发：md 转 latex、换期刊模板、双栏/单栏、字号/页边距/行距、参考文献字号、图表位置/浮动体/同页、行号、改动标红标蓝或去色、md 同步到 tex、编译或压缩稿件 PDF。"
---

# P Article LaTeX

给 PJ 排期刊稿件 LaTeX 时按下面做。总原则：版式用期刊模板默认值，只动排版不动内容，图表落在首次引用页。
REVTeX 细节、REVTeX↔elsarticle 转换、表格与 SI 的坑见 [references/journal-switch.md](references/journal-switch.md)。

## 边界

- md（或作者指定的稿件）是内容权威源，tex 是派生物。tex 侧只改排版，不改正文、图注、文献文字；补文献只在原句后加 `\cite`。作者说"只动排版 / 只改颜色"时，措辞建议写进报告，不改进稿件。
- 小需求直接改：去色就是改一处开关再重编译，不开子 agent 做规划。
- 换期刊先读官方 Guide for Authors 的版式条款（栏数、行距、图表放正文还是文末，npj 要求放文末），再定 documentclass。
- 改 tex/md 用 Edit 或 Python `newline=""`：MSYS `sed -i` 会把整份 CRLF 文件转成 LF，bash heredoc 会吞 `\`。
- 新 PDF 另起文件名（`Manuscript_<MMDD>.pdf`、`SI_<MMDD>.pdf`），旧版不覆盖。

## 栏数与字号

版心、字号、行距先用模板默认。作者嫌留白多、字大或篇幅超了才打补丁，并在补丁旁注释原因。

| 场景 | documentclass | 字号与版心 |
|---|---|---|
| Elsevier 双栏（作者首选，像 PRB 那种双栏） | `[final,5p,times,twocolumn]{elsarticle}` | 10pt；`\textwidth` 522pt，`\columnwidth` 252pt |
| Elsevier 单栏双倍行距（Guide 明确要求时） | `[preprint,review,11pt]{elsarticle}` + `\usepackage[a4paper,margin=2cm]{geometry}` + `\raggedbottom` | 12pt 会排到 54 页，作者嫌字大；11pt 加 2 cm 边距约 32 页 |
| Elsevier SI | `[preprint,10pt]{elsarticle}` + `geometry{a4paper,margin=1.6cm}` | 单栏 |
| APS 正文（PRB/PRM） | `revtex4-2[aps,prb,reprint,superscriptaddress,amsmath,amssymb,longbibliography,floatfix,nofootinbib]`（PRM 把 `prb` 换成 `prmaterials`） | 双栏 10pt，栏宽 246pt，通栏 510pt |
| APS SI | 同上，加 `onecolumn`、去 `longbibliography` | 单栏 |

elsarticle 双栏上下留白太多时只收纵向，横向不动：

```latex
\addtolength{\textheight}{54pt}   % 模板给 running head 留了 50pt
\addtolength{\topmargin}{-27pt}
```

elsarticle 通用导言：

```latex
\PassOptionsToPackage{sort&compress}{natbib}  % 输出 [1-3]；必须写在 \documentclass 之前
\usepackage{caption}
\captionsetup{labelsep=period,singlelinecheck=false,font=footnotesize}  % "Fig. 1."，图注靠左
\renewcommand{\figurename}{Fig.}
\setlength{\emergencystretch}{3em}   % 长复合词断不开时给余量，不改文字
```

图表本体 `\centering`，图注、表注靠左；标签统一写 `Fig. 1.`、`Table 1.`、`Fig. S1.`、`Table S1.`。

**参考文献字号**：作者要求字小、尽量排进一页，参照其已发表的 Acta Mater. 文章：

```latex
\renewcommand{\bibfont}{\fontsize{6.4}{8}\selectfont}
\setlength{\bibsep}{0pt}
```

**行号**（双栏）：

```latex
\usepackage{lineno}                              % 不用 [switch]，否则第 2 页起行号压字
\setlength{\linenumbersep}{5pt}
\AtBeginDocument{\setlength{\columnsep}{26pt}}   % 写在导言区会被模板覆盖
\linenumbers
```

## 图表位置

验收标准：

1. 每张图、表尽量与正文首次引用同页。做不到时最多差一页，而且要紧挨引用：放前一页页底（`[!b]`）或后一页页顶（`[!t]`），中间不能隔着其他小节的正文。
2. Conclusion 所在页及之后不放任何图，主文图也不能落进 Acknowledgments 或 Appendix。
3. 不能出现只有浮动体的整页：位置参数里不写 `p`。
4. 图号顺序与声明顺序一致。figure 和 figure* 共用一个输出队列，挪动声明时绝不能改变图与图的先后。

调整手段，按顺序尝试：

1. 浮动体声明放在首次引用的段落前后，不照搬 md 里"图表集中在文末"的结构；挪段落时连同对应的 figure 块一起挪。
2. 只靠移动声明位置和 `[!t]`、`[!b]` 来调。`figure*` 默认只能放页顶，加 `\usepackage{stfloats}` 才能放页底，而且至少延后一页，所以要在目标页被切断之前的正文里声明它。
3. 同一页既有栏内 figure 又有 figure* 时，先声明栏内 figure 占住栏顶，再在该页左栏声明 figure*，用 `[!b]`。
4. 声明已经挪到引用附近、再挪也没用时，原因是大图会把自己的引用段一起往后推，偏移不会变。此时真正起作用的是图高，比如纵长图改成栏内 `figure` 加 `\columnwidth`。改图幅或改全局浮动参数（`\topfraction` 等）之前先问作者。
5. 不用 `[H]` 或 `\clearpage` 硬塞，也不用 `cuted` 的 `strip` 代替 `figure*`，否则图和图注会被拆到两页。

环境怎么分：双栏下多面板图和横幅图用 `figure*` 加 `\textwidth`，单面板图和纵长图用 `figure` 加 `\columnwidth`，宽表用 `table*`。单栏文档里不要混用带星和不带星的环境，两类会互相穿插。

复查：

```bash
python <本 skill 目录>/scripts/check_float_pages.py <path/to/manuscript.tex>   # 结果须为 violations: 0
```

- 脚本依赖两类标签：`\label{sec:conclusion}`，以及 `fig:<整数>`、`tab:<整数>` 形式的浮动体标签。
- 脚本跑完后，还要逐页看渲染图，确认没有空栏、没有纯图页、行号不压字。
- 报告里列出每张图表的首次引用页和实际落页。
- REVTeX 的 `float is stuck` 警告无害，要盯的是 `!` 开头的错误和 Overfull。

## 公式

- 默认留在栏内。超宽时用 `split`、`aligned` 或 `multline` 在运算符前折行，不靠缩小字号。
- 只有确实很长的推导才通栏，而且一整段连续推导放进一个块：REVTeX 用 `widetext`，elsarticle 用 `cuted` 的 `strip`。不要每条公式各开一个块，那样会出现多组分隔横线。
- 每个公式单独编号。
- 单栏稿不用 `adjustwidth` 外扩，也不用 `\nolinenumbers`，否则行号会消失、文字越出页边；版心放宽后长公式自然能排下。

## 改动标色

- 期刊格式转换中因硬性要求增删改的文字标红：`\newcommand{\rev}[1]{\textcolor{red}{#1}}`。润色同步时照 md 里蓝 span 的位置标蓝，只包改动的词组。参考文献的增删和改号都不标色。
- 整段标色写 `{\leavevmode\color{blue} …\par}`。`\textcolor` 不能跨 `\par`；不加 `\leavevmode` 的话，竖直模式下的 `\color` 会变成分页点，节标题会孤零零落在栏底。
- 图注标色：导言区写 `\DeclareCaptionFont{blue}{\color{blue}}`，再在该 figure 内写 `\captionsetup{font+=blue}`。直接写 `\color` 会被 caption 包重置。
- 去色只改一处开关 `\usepackage[monochrome]{xcolor}`，标记仍留在源码里。反过来说，带 `monochrome` 时所有标色都看不见，要查一下当前是哪种状态。

## 编译与交付

- pdflatex 跑 3 遍。文献用 `thebibliography` 内嵌，不跑 BibTeX。日志里 `Overfull \hbox`/`\vbox` 和 undefined 都要为 0。仓库里有 `compile_manuscript.sh` 就用它。
- `-draftmode` 不出 PDF。交付前确认目标 PDF 确实被重新写出（看修改时间）。
- 在 scratchpad 里用 `-output-directory` 编译，`latex/` 下不留 aux、log。PDF 被预览锁住时换个输出名；编译中断后出现满屏 `?`，删掉 aux 重跑 3 遍。
- 默认按压缩流程出片，成品 ≤3 MB，不留大体积中间 PDF：

  ```bash
  bash compile_manuscript.sh build.pdf
  python <本 skill 目录>/scripts/shrink_pdf.py build.pdf Manuscript_<MMDD>.pdf 3
  rm build.pdf
  ```

- 压完图发糊时换 `scripts/resample_figures.py`，它按 `\includegraphics` 的印刷宽度做重采样：
  - 送审 PDF：`-dpi 400 -codec jpeg -quality 82`。体积还不够就按 380/q86 → 360/q88 → 350/q90 往下挪，不要直接砍 dpi。
  - 源文件包：`-dpi 600 -codec flate`。
  - 换了 documentclass 要先用 `\typeout{\the\textwidth}` 实测版心宽度，改脚本里的 `DICT_WIDTH_PT`。
  - `shrink_pdf.py` 的 dpi 与成品体积不是单调关系。图的真实 dpi 用 `pdfimages -list` 看。
- 篇幅、页数这类一次性问题按字数和图幅估算，不建编译工程。
