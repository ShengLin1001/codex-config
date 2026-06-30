---
name: p-pdf-download
description: 当用户要求用 scansci-pdf 下载学术 PDF / DOI 全文时使用。所有出版商（含 Elsevier 10.1016）一律走 browser-get --manual 官方浏览器、由用户逐篇人工过验证，确保拿到官网正文当前版而非 API 历史版。会剔除预印本 / arXiv / SI 并去重。
---

# PDF 下载（统一走可见浏览器）

## 核心原则

只要官网正文的**当前版**。**所有出版商一律走可见浏览器手动模式（`browser-get --manual`）**，由用户逐篇过人机验证 / 登录机构 / 打开 PDF，脚本只负责抓取出现的官方 PDF。不引入 Sci-Hub / LibGen 等灰色来源。**预印本、arXiv、SI（补充材料）都不要。**

底层命令是 `scansci-pdf browser-get <DOI> --manual --output <绝对目录>`；本技能用 `scripts/pdf_download.py` 按 `dois_row.txt` 逐篇编排，并把每篇落到约定好的目录里。目录与 `dois_row.txt` 由上游 **p-pdf-preview（literature-folder-builder）** skill 建好，本脚本只消费、不取名：

```
单篇:        literatures/YYMMDD_简练中文名/     # 目录名 = 据文章内容取的中文名
               dois_row.txt              # 仅 1 行 DOI
               <DOI>_Official.pdf        # 直接落在此目录（与 dois_row.txt 同级）
多篇(调研):  literatures/YYMMDD_investigate_主题/   # 目录名 = investigate_<调研主题>
               dois_row.txt              # 每行 "DOI<TAB>子目录名"
               summary.md                # 上游写的调研摘要，下载脚本不动它
               子目录名1/<DOI1>_Official.pdf
               子目录名2/<DOI2>_Official.pdf
```

> **为什么 Elsevier 也走浏览器**：Elsevier 官方 API（`get`/`batch`）有时会落到论文的**历史版本**，而非 ScienceDirect 官网当前的下载版。为保证逐篇都是官网正文当前版，本技能不再用 API，Elsevier 与其余出版商（Nature、APS、Wiley、Science、RSC、IEEE、ACM、OUP…）统一走 `browser-get --manual`，由用户在真实出版商页面手动通过。

## 环境加载

每个 shell 会话先加载预配置环境（bash，不要用 PowerShell / Windows `.exe` 路径）：

```bash
scanscipy
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
```

`scanscipy` 是激活 `scansci-pdf` 虚拟环境的 bash alias。如果它不可用，**停止并报告 alias 缺失**，不要退回到完整的 Windows venv 路径。设置 UTF-8 是为了中文论文元数据不乱码。

## 预检查（仅新线程或登录状态变化时）

```bash
scanscipy
scansci-pdf --help            # 确认 browser-get 在
scansci-pdf browser-status    # 浏览器路径需要 CloakBrowser 可用
```

- `browser-get` 会弹出**可见**浏览器，必须在用户的桌面会话里运行，不能在无头 / CI 环境里跑。
- 付费墙文章需要机构访问：用户在校园网内，或开了全隧道 VPN 客户端（aTrust/EasyConnect）；手动模式下由用户自行在页面里登录机构。
- 若 `browser-status` 显示未安装，这是硬性阻断，先报告。

## 步骤 0 · 整理 DOI 列表（剔除不需要的）

无论单篇还是多篇，先剔除**预印本、arXiv、空行、注释**并去重。SI 不在列表层处理（见下文，由工具自动排除）。

```bash
# 输入 dois.raw.txt → 干净列表 dois.clean.txt
grep -vE '^[[:space:]]*(#|$)' dois.raw.txt \
  | grep -viE 'arxiv|10\.48550|10\.21203|10\.26434|10\.2139/|10\.20944|10\.22541|10\.31219|10\.31234|biorxiv|medrxiv|chemrxiv|researchsquare|preprints?\.org|ssrn' \
  | grep -vE '10\.1101/20[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.' \
  | grep -vE '^[[:space:]]*[0-9]{4}\.[0-9]{4,5}([vV][0-9]+)?[[:space:]]*$' \
  | awk '!seen[$0]++' \
  > dois.clean.txt
```

剔除依据：

- **arXiv**：`10.48550/arXiv.*`、含 `arxiv` 的 URL、形如 `2401.12345` 的裸 arXiv ID。
- **预印本服务器**：Research Square `10.21203`、ChemRxiv `10.26434`、SSRN `10.2139`、Preprints.org `10.20944`、Authorea `10.22541`、OSF `10.31219/10.31234`，以及 bioRxiv/medRxiv（按 URL 关键字）。
- 注意：`10.1101` 既是 bioRxiv/medRxiv 也是 CSH 正式期刊，**不要**只凭前缀盲删。上面的正则按"日期式后缀"识别预印本（如 `10.1101/2020.03.22.20041079`），同时保留 `10.1101/gr.*`、`10.1101/gad.*` 这类 CSH 正式期刊。
- 剔除后给用户一句话说明丢了哪些行，便于核对。

## 步骤 1 · 建目录 + 写 dois_row.txt（交给上游 p-pdf-preview skill）

目录组织、取名、写 `dois_row.txt`（多篇还有 `summary.md`）这一步**不在本技能里做**，由 **p-pdf-preview（literature-folder-builder）** skill 负责——它读文章内容取中文目录名 / 子目录名，在 `literatures/` 下建好标准结构。把步骤 0 整理好的干净 DOI 交给它即可。

本技能与它的对接契约（`pdf_download.py` 据此解析）：

- 文件名 `dois_row.txt`（脚本也兼容旧名 `dois.row.txt`）。
- 单篇：1 行 DOI，PDF 落到 `dois_row.txt` 同级目录。
- 多篇：每行 `DOI<TAB>子目录名`（上游固定 TAB；脚本也容忍空格 / ` | `），各篇落到对应子目录。
- 空行与 `#` 注释行忽略；重复 DOI 自动去重；缺子目录名时脚本回退为清洗后的 DOI 并告警。

## 步骤 2 · 运行下载脚本

```bash
scanscipy                                   # 先激活 venv，使 scansci-pdf 进 PATH
export PYTHONUTF8=1; export PYTHONIOENCODING=utf-8
python <技能目录>/scripts/pdf_download.py literatures/<YYMMDD_目录>/dois_row.txt
# 传目录亦可，脚本会自动找其中的 dois_row.txt：
python <技能目录>/scripts/pdf_download.py literatures/<YYMMDD_目录>
```

脚本按行数自动判定单 / 多篇，逐篇调用 `scansci-pdf browser-get <DOI> --manual --output <绝对目录>`：单篇落到 `dois_row.txt` 同级目录，多篇落到各自子目录。**先 `--dry-run` 看一眼每篇的落盘目录对不对，再去掉它正式跑。**

脚本参数：

- `--dry-run`：只打印将执行的命令与落盘目录，不真正下载。
- `--wait N`：每篇手动操作超时秒数（默认 300）。机构登录慢时调大，如 `--wait 600`。
- `--skip-existing`：目标目录已有 PDF 时跳过。**默认强制重抓**（保证拿官网当前版、避免历史版残留），只有想在失败后只补缺时才加这个开关。

`--manual` 模式的分工——**用户做、脚本抓**（每篇串行，不能并发）：

1. 脚本逐篇打开真实出版商页面（不经 WebVPN 改写），弹出可见浏览器。Elsevier 会落到 ScienceDirect 当前版页面。
2. 用户负责：过 Cloudflare 人机验证 → 登录机构 → **点开/打开正文 PDF**。
3. 脚本捕捉任意标签页里出现的 PDF，自动落盘为 `<doi>_Official.pdf`，然后切到下一篇。
4. **SI 自动排除**：MOESM / MediaObjects / ESM / supplementary / supp 等补充材料链接在抓取层被丢弃，不会被误存为正文。

> 提示：少数出版商（Nature/Springer/Science 等会发 `citation_pdf_url`）不加 `--manual` 的自动模式也能抓到正文。但本技能默认用 `--manual` 以保证逐篇都是官网正文当前版；只有用户明确想试自动模式时才另行手动调 `browser-get`。

## 失败处理

- **不要把 HTML / 机器人验证页当成 PDF。** browser-get 已校验 `%PDF-` magic bytes 且大小 >5KB；若用户关窗太快或没点开 PDF，会判为该篇失败，重跑那一篇即可。
- **付费墙**：手动模式下用户必须在页面里登录机构后再打开 PDF；脚本自己做不了 Shibboleth 登录，抓取循环会在用户操作期间重试。
- **APS（journals.aps.org / link.aps.org）**：Cloudflare 保护，**不能**走 ZJU WebVPN 改写代理；只能用 `browser-get --manual`（真实域名 + 用户手过验证 + 机构 IP/VPN）。
- **Elsevier / ScienceDirect**：在弹出的页面上由用户登录机构后点开正文 PDF；落盘的就是官网当前版，避免了 API 的历史版问题。
- **抓到的是 SI**：说明用户当时没登录机构、正文被墙而 SI 免费。让用户先登录机构再打开正文；列表层与抓取层的 SI 过滤是兜底而非替代登录。

## 报告结果

脚本结尾自带 summary（成功 / 失败 / 共计 + 逐篇落盘路径）。完成后再向用户说明：

- 列表整理情况：剔除了哪些预印本 / arXiv 行、去重后剩几条。
- 目录：单篇 `YYMMDD_中文名/` 还是多篇 `YYMMDD_investigate_主题/`，以及各篇子目录名。
- 成功数与每篇 PDF 的落盘路径；失败的给一句简短原因（关窗太快、未登录机构、Cloudflare 没过等）。
- 有失败时：用同一份 `dois_row.txt` 加 `--skip-existing` 重跑，已落 PDF 跳过、只补失败的几篇（不加则默认全部重抓）。
