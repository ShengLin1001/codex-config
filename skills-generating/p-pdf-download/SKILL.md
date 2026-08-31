---
name: p-pdf-download
description: Batch-download academic PDFs from DOI lists through publisher official websites only. Uses scansci-pdf browser-get with one persistent CloakBrowser session; no API, aggregator, repository, preprint substitution, Sci-Hub, or LibGen fallback.
---

# DOI 批量下载 PDF（仅出版商官网）

## 1. 环境检测

必须在 bash 中使用 scanscipy 环境：

```bash
scanscipy
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
scansci-pdf browser-status
python -m cloakbrowser info
```

若 CloakBrowser 不可用则停止。若 `info` 显示旧版无 key（例如 v146），说明自动过盾能力可能已经过时；报告并建议用户一次性运行 `cloakbrowser login` 获取最新免费版。不要改用其他 PDF 来源。

## 2. DOI 文件

每行一个 DOI，可在 TAB 后附名称；空行和 `#` 注释忽略。脚本会去重，并剥掉 `https://doi.org/` 或 `doi:` 前缀。

## 3. 默认自主下载

```bash
python <p-pdf-download>/scripts/auto_pdf_download.py dois.txt -o pdfs/
python <p-pdf-download>/scripts/auto_pdf_download.py dois.txt -o pdfs/ --skip-existing
python <p-pdf-download>/scripts/auto_pdf_download.py dois.txt --dry-run
```

默认流程只调用 `scansci-pdf browser-get`：从 DOI 跳转进入出版商官网，在同一持久 CloakBrowser 会话中定位并保存正文 PDF。不会调用 `scansci-pdf get`，因为后者会混入 API、聚合器和其他来源。

下载成功必须同时满足：

- 本轮在指定输出目录写入新 PDF；
- PDF 通过文件头、尾部 EOF 和最小尺寸校验；
- 来源为出版商官网浏览器路径；
- 不把旧缓存、其他目录文件、预印本或补充材料计作成功。

## 4. 人工兜底（仅用户明确同意时）

```bash
python <p-pdf-download>/scripts/auto_pdf_download.py dois.txt -o pdfs/ --skip-existing --manual --wait 300
```

`--manual` 仅用于自动模式失败后，由用户手动过验证或登录机构。不要把需要人工操作的结果描述为“完全自动化”。

## 不要做

- 不使用 `scansci-pdf get` 全源级联、Elsevier API、Unpaywall、OpenAlex、CORE、DOAJ 或预印本替代；
- 不使用 Sci-Hub / LibGen；
- 不宣称 CloakBrowser 或付费会员保证通过某个出版商，必须以隔离实测为准。
