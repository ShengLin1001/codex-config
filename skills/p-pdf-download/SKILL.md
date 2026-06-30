---
name: p-pdf-download
description: 当用户要求用 scansci-pdf 下载学术 PDF / DOI 全文时使用。按出版商分流——Elsevier(10.1016) 走 get/batch 官方 API；其余出版商走 browser-get --manual 官方浏览器、由用户逐篇人工过验证。会自动拆分混合 DOI 列表，并剔除预印本 / arXiv / SI。
---

# PDF 下载（按出版商分流）

## 核心原则

只要官方版。**Elsevier 走 API，其余出版商走可见浏览器手动模式**，由用户逐篇过人机验证 / 登录机构 / 打开 PDF，脚本只负责抓取出现的官方 PDF。不引入 Sci-Hub / LibGen 等灰色来源。**预印本、arXiv、SI（补充材料）都不要。**

| 输入 | Elsevier（DOI 前缀 `10.1016/`） | 其余所有出版商 |
| --- | --- | --- |
| 单篇 | `scansci-pdf get <DOI> --output DIR` | `scansci-pdf browser-get <DOI> --manual --output DIR` |
| 多篇 | `scansci-pdf batch dois.txt --output DIR` | `scansci-pdf browser-get --file dois.txt --manual --output DIR` |

> Elsevier 已配置官方 API，`get`/`batch` 能直接拿到正文 PDF，无需浏览器。其余出版商（Nature、APS、Wiley、Science、RSC、IEEE、ACM、OUP…）多半有 Cloudflare 或付费墙，必须用可见浏览器由用户手动通过，才能保证是官网正文。

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
scansci-pdf --help            # 确认 get / batch / browser-get 都在
scansci-pdf browser-status    # 非 Elsevier 路径需要 CloakBrowser 可用
```

- `browser-get` 会弹出**可见**浏览器，必须在用户的桌面会话里运行，不能在无头 / CI 环境里跑。
- 付费墙文章需要机构访问：用户在校园网内，或开了全隧道 VPN 客户端（aTrust/EasyConnect）；手动模式下由用户自行在页面里登录机构。
- 若 `browser-status` 显示未安装，这是非 Elsevier 路径的硬性阻断，先报告。

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

## 步骤 1 · 按出版商拆分（混合列表才需要）

把干净列表按 `10.1016/` 拆成两份，分别处理：

```bash
grep -E  '10\.1016/' dois.clean.txt > doi-elsevier.txt     || true
grep -vE '10\.1016/' dois.clean.txt > doi-non-elsevier.txt || true
wc -l doi-elsevier.txt doi-non-elsevier.txt
```

匹配不锚定行首，能同时覆盖裸 DOI 和 `https://doi.org/10.1016/...` 形式。哪个文件为空就跳过对应步骤。单篇输入则直接判断该 DOI 是否含 `10.1016/`，无需建文件。

## 步骤 2a · Elsevier 下载（API 官方）

```bash
# 单篇
scansci-pdf get 10.1016/j.actamat.2026.122243 --output DIR --no-bibtex
# 多篇
scansci-pdf batch doi-elsevier.txt --output DIR
```

- `get`/`batch` 经官方 Elsevier API 取正文 PDF；`batch` 会把汇总写到 `DIR/batch_results.json`。
- 只有真正落地了 PDF 才算成功。若返回的是 full text 但 `pdf_path` 为空、或只拿到 XML，**不要当作成功**——对该 DOI 改走 `browser-get --manual`（ScienceDirect 页面）兜底。
- 如果 Elsevier 命令大量失败，先确认 API key：`scansci-pdf elsevier-setup`（无参数会显示是否已配置）。

## 步骤 2b · 非 Elsevier 下载（浏览器手动）

```bash
# 单篇
scansci-pdf browser-get 10.1103/PhysRevB.88.064104 --manual --output DIR
# 多篇
scansci-pdf browser-get --file doi-non-elsevier.txt --manual --output DIR --wait 300
```

`--manual` 模式的分工——**用户做、脚本抓**：

1. 脚本逐篇打开真实出版商页面（不经 WebVPN 改写），弹出可见浏览器。
2. 用户负责：过 Cloudflare 人机验证 → 登录机构 → **点开/打开正文 PDF**。
3. 脚本捕捉任意标签页里出现的 PDF，自动落盘为 `<doi>_Official.pdf`，然后切到下一篇。
4. **SI 自动排除**：MOESM / MediaObjects / ESM / supplementary / supp 等补充材料链接在抓取层被丢弃，不会被误存为正文。

参数：

- `--manual` / `-m`：手动模式（本技能的非 Elsevier 默认方式，最稳，覆盖 IEEE/ACM 等 JS 阅读器）。
- `--file` / `-f`：从文件读 DOI（每行一个，空行和 `#` 注释自动忽略）。
- `--output`：下载目录。
- `--wait`：每篇等待手动操作的超时秒数（默认 300）。机构登录较慢时调大，如 `--wait 600`。

> 提示：少数出版商（Nature/Springer/Science 等会发 `citation_pdf_url`）不加 `--manual` 的自动模式也能抓到正文。但本技能默认用 `--manual` 以保证逐篇都是官网正文；只有用户明确想试自动模式时才去掉 `--manual`。

## --output 路径控制

`get`、`batch`、`browser-get` 三个命令都支持 `--output DIR`，统一控制落盘目录。建议：

- 同一批任务用同一个 `--output`，Elsevier 与非 Elsevier 两条线汇到同一目录便于核对。
- 不传 `--output` 时落到配置里的默认目录（`~/.scansci-pdf/papers`）。

## 失败处理

- **不要把 HTML / 机器人验证页当成 PDF。** browser-get 已校验 `%PDF-` magic bytes 且大小 >5KB；若用户关窗太快或没点开 PDF，会判为该篇失败，重跑那一篇即可。
- **付费墙非 Elsevier**：手动模式下用户必须在页面里登录机构后再打开 PDF；脚本自己做不了 Shibboleth 登录，抓取循环会在用户操作期间重试。
- **APS（journals.aps.org / link.aps.org）**：Cloudflare 保护，**不能**走 ZJU WebVPN 改写代理；只能用 `browser-get --manual`（真实域名 + 用户手过验证 + 机构 IP/VPN）。
- **Elsevier 命令报 import error / publisher-batch 失败**：视为当前安装的包 bug，改用 `get`/`batch`/`browser-get` 直接探测，不要纠缠该子命令。
- **抓到的是 SI**：说明用户当时没登录机构、正文被墙而 SI 免费。让用户先登录机构再打开正文；列表层与抓取层的 SI 过滤是兜底而非替代登录。

## 报告结果

完成后向用户说明：

- 列表整理情况：剔除了哪些预印本 / arXiv 行、去重后剩几条。
- 出版商拆分：Elsevier N 篇、非 Elsevier M 篇。
- 各自走的命令路径（`get`/`batch` 还是 `browser-get --manual`）与成功数。
- 每篇成功 PDF 的落盘路径；失败的给一句简短原因（关窗太快、未登录机构、Cloudflare 没过、Elsevier 只拿到 full text 无 PDF 等）。
