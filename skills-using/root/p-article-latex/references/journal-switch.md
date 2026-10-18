# 期刊模板细节与转换坑

## REVTeX 4.2（PRB / PRM）

- 不写 `\date`。`\date{}` 也会印出 "(Dated:)"，要整行删掉。
- 通讯作者写 `\author{…}` 后紧跟 `\email[Contact author: ]{…}`，星号排在单位编号之后。不要为了挪释义的位置手工加星号。
- 修订颜色全部剥掉，正文用默认黑色。
- `widetext` 的起止横线落在栏尾公式上时，把 `\begin{widetext}` 上移，让整段推导都通栏；或者把公式拆开，让后半落到下一栏栏顶。
- `ruledtabular` 会重设 `\tabcolsep`，所以 `\setlength{\tabcolsep}{3pt}` 要写在环境里面。
- REVTeX 会把 `[1,2,3]` 压成 `[1–3]`，PDF 里搜不到 `[2]` 并不是漏引。
- 集群 TeX Live 2013 没有 revtex4-2。要从 CTAN 取 `revtex.tds.zip`，解压到 `TEXMFHOME`。

## REVTeX → elsarticle

| REVTeX | elsarticle |
|---|---|
| `ruledtabular` | booktabs 三线表，分组线用 `\cmidrule(lr)` |
| `widetext` | `\usepackage{cuted}` + `\begin{strip}` |
| `\footnotemark[n]`/`\footnotetext[n]` | `\textsuperscript{a}`，表下另起 `\par\vspace{5pt}\raggedright\footnotesize` 段落 |
| `acknowledgments` 环境 | `\section*{Acknowledgements}` |
| `Appendix~\ref{}` | `\ref{}`，否则印成 "Appendix Appendix A" |

- 四级标题需要编号时设 `\setcounter{secnumdepth}{4}`。直接挂在 section 下的 `\paragraph` 会印成 A.0.0.1，要提升为 `\subsection`。
- 11 列宽表溢出时，表内加 `\footnotesize` 并把 `\tabcolsep` 设为 4pt。
- `preprint,review` 首页会报约 24–31pt 的 Overfull `\vbox`，这是类内部行为，版面上看不出问题，但会让 `compile_manuscript.sh` 判失败。报告里要说明这一点，不要去改脚本。
- Highlights 按期刊要求做成独立文件。

## 表与 SI

- 同号续表：在第二个 `\begin{table}` 之后、`\caption` 之前写 `\addtocounter{table}{-1}`，图注里加 "(continued)"。
- SI 的编号：`\renewcommand{\thefigure}{S\arabic{figure}}`；`table`、`equation`、`section` 同理。
- 参考文献按正文首次引用的顺序编号，表注、图注里的引用也算在内。`\bibitem{refN}` 与 md 编号一一对应。
- SI 里指向主文文献的 `Ref.~[NN]` 是硬编码的。主文文献每次增删或重排后，都要回头手改 SI（这个坑已经踩过 5 次）。
- 交叉引用写法：
  - 主文引 SI 用括号式，例如 `(Fig. S3 of the SM)`、`(Fig. S1)`，不扩写 "see"，全文统一一种写法。
  - SI 引主文写 `Fig. 3 of the main text`。
  - SI 里不加 "Reference numbers in this SM refer to…" 这类说明句。

## 投稿源文件包

- 另出一份投稿用的 tex：删掉 `%` 注释、`\rev` 和 xcolor，拍平目录并写 `\graphicspath{{./}}`，保留 `\linenumbers`。然后用 `pdftotext` 与送审版比对，正文差异应为 0 行。
- pdflatex 读不了 TIFF：zip 里的图用 PDF；若期刊要求单独上传 TIFF，另出一套 600 dpi LZW 的 TIFF。
- 中文路径下用 PowerShell 的 `Compress-Archive` 打包，7-Zip 等工具会失败。
- 集群上的 PyMuPDF 太旧，跑不了 `shrink_pdf.py`，改用 Ghostscript 逐档降 dpi：

  ```bash
  gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dDetectDuplicateImages=true \
     -dAutoFilterColorImages=false -dColorImageFilter=/DCTEncode -dDownsampleColorImages=true \
     -dColorImageDownsampleType=/Bicubic -dColorImageResolution=300 \
     -dAutoFilterGrayImages=false -dGrayImageFilter=/DCTEncode -dDownsampleGrayImages=true \
     -dGrayImageDownsampleType=/Bicubic -dGrayImageResolution=300 \
     -dDownsampleMonoImages=true -dMonoImageResolution=600 \
     -sOutputFile=Manuscript_<MMDD>.pdf build.pdf
  ```

  体积不达标时，把三个 `*ImageResolution` 依次降到 250、200、150 再试。
