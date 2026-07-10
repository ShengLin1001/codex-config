---
name: p-pdf-download
description: Use when the user wants to batch-download academic PDFs from a list of DOIs. Reads `dois.txt` (one DOI per line) and runs the bundled `scripts/pdf_download.py`, which drives `scansci-pdf browser-get` inside the scanscipy venv, saves PDFs to the current directory, and renames them to short DOI-suffix names.
---

# DOI 批量下载 PDF

## 1. 环境检测

下载必须在 bash 里运行，不要用 PowerShell / Windows `.exe` 路径：

```bash
scanscipy
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
scansci-pdf browser-status
```

如果 `scanscipy` 不可用，或 `browser-status` 显示 CloakBrowser 不可用，停止并报告；不要退回到其他 Python 环境。

## 2. dois.txt

每行一个 DOI，不写中文名、标题、编号，也不要写成 Markdown 表格：

```text
10.1016/j.actamat.2024.120459
10.1103/PhysRevB.108.014102
10.1038/s41524-024-01234-5
```

- 空行与 `#` 注释行忽略；
- 重复 DOI 自动去重；
- `https://doi.org/` 和 `doi:` 前缀会自动剥掉。

## 3. 下载

```bash
python <p-pdf-download>/scripts/pdf_download.py                        # 读 ./dois.txt，PDF 落 ./
python <p-pdf-download>/scripts/pdf_download.py dois.txt --dry-run     # 先看命令与落盘文件名
python <p-pdf-download>/scripts/pdf_download.py dois.txt -o refs/ --skip-existing
```

脚本约定：

- 输出目录默认当前目录 `./`，用 `-o` 改；绝不落到用户级 papers 目录；
- 文件名取 DOI 后缀：`10.1016/j.actamat.2024.120459` → `j.actamat.2024.120459.pdf`，
  主干超 60 字符则截断并追加 6 位哈希；
- `--wait N` 每篇人工验证超时（默认 300 秒，机构登录慢可调大）；
- `--skip-existing` 只补缺，不重抓已有 PDF；失败篇目重跑用它；
- 浏览器可见，需要逐篇人工过人机验证 / 机构登录，串行执行，不要并发；
- `--selftest` 跑命名与解析自检，不下载。

## 不要做

- 不要使用 Sci-Hub / LibGen 等灰色来源；
- 不要把 DOI 文件写成 Markdown 表格；
- 不要在 `dois.txt` 中加入说明文字或第二列。
