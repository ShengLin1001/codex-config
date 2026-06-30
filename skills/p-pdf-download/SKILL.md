---
name: p-pdf-download
description: Use when the user wants to download or organize academic PDFs/DOIs into a standard root directory, defaulting to `literatures`, either for a single paper DOI or for a literature investigation topic. Creates folders, writes `dois_row.txt`/`summary.md`, then by default runs the bundled `scripts/pdf_download.py` against the created `dois_row.txt` unless the user explicitly asks to only preview/create folders.
---

# Literature Folder Builder + PDF Download

## 0. 环境检测

先检查下载环境。下载必须在 bash 里运行，不要用 PowerShell / Windows `.exe` 路径：

```bash
scanscipy
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
scansci-pdf --help
scansci-pdf browser-status
```

如果 `scanscipy` 不可用，或 `browser-status` 显示 CloakBrowser 不可用，停止并报告；不要退回到其他 Python 环境。

若用户明确要求“只创建目录/只预览”，仍创建文件结构，但不要运行下载脚本。

## 目标

当用户要求下载、整理单篇文献，或围绕主题做文献调研时：

1. 在指定 `root_dir` 下创建标准文献目录结构；
2. 写入 `dois_row.txt`，多篇调研时同时写入 `summary.md`；
3. 默认运行本 skill 自带的 `scripts/pdf_download.py`，参数指向刚创建的 `dois_row.txt`。

## root_dir 和日期

`root_dir` 是文献任务根目录，默认值为：

```text
literatures
```

如果用户指定其他目录，使用用户指定目录，并把后续所有结构中的 `root_dir` 替换成该目录。

新建子目录使用当前日期前缀 `YYMMDD`，例如 `260630`。

目录名和子目录名不要包含文件系统非法字符：

```text
/ \ : * ? " < > |
```

## 单篇文献

适用于用户提供单篇 DOI、标题、链接、摘要，或要求“下载这篇文献”。

目录结构：

```text
root_dir/
└── YYMMDD_简练中文名/
    └── dois_row.txt
```

目录名规则：

- 使用中文，简短明确，概括文章核心内容；
- 推荐 6-20 个中文字符；
- 不要机械翻译成长英文标题。

`dois_row.txt` 只写 1 行 DOI，不要标题、注释、编号或空行：

```text
10.xxxx/xxxxx
```

## 多篇文献调研

适用于用户要求调研、搜索、整理某个主题的一批文献。

目录结构：

```text
root_dir/
└── YYMMDD_investigate_主题/
    ├── dois_row.txt
    └── summary.md
```

`dois_row.txt` 每行必须是 `DOI<空格>子目录名`：

```text
10.1016/j.actamat.2024.xxxxxx    金薄膜相变
10.1016/j.commatsci.2023.xxxxxx  机器学习势多相模拟
10.1038/s41524-2024-xxxxx        神经网络势界面性质
```

第二列子目录名应简短中文，可保留必要英文缩写，如 `DFT`、`MD`、`MLP`、`SFE`、`FCC`、`HCP`。不要包含日期、DOI 或非法路径字符.

`summary.md` 写阶段性调研记录即可，至少包含：

```markdown
# 调研主题

## 1. 调研目标

## 2. 初步结论

## 3. 重要文献列表

## 4. 主题脉络

## 5. 后续阅读建议
```

## 质量检查

完成目录创建后检查：

```bash
find root_dir -maxdepth 2 -type f
```

确认：

- 单篇任务只有一个 `dois_row.txt`；
- 多篇调研任务同时包含 `dois_row.txt` 和 `summary.md`；
- `dois_row.txt` 没有表头、编号、Markdown 表格或多余空行；

## 下载脚本

建好目录后先质量检查，在运行下载脚本。默认先 dry-run，再正式运行：

```bash
python <p-pdf-download>/scripts/pdf_download.py "root_dir/<刚创建目录>/dois_row.txt" --dry-run
python <p-pdf-download>/scripts/pdf_download.py "root_dir/<刚创建目录>/dois_row.txt"
```

脚本约定：

- 单篇：PDF 落在 `dois_row.txt` 同级目录；
- 多篇：PDF 落在 `dois_row.txt` 第二列对应的子目录；
- `summary.md` 仅供人看，脚本不读、不动；
- 空行和 `#` 注释行忽略；
- 重复 DOI 自动去重；
- `--wait N` 可调整每篇手动操作超时；
- `--skip-existing` 只补缺，不重抓已有 PDF。

## 不要做

- 不要使用 Sci-Hub / LibGen 等灰色来源；
- 不要把 DOI 文件写成 Markdown 表格；
- 不要在 `dois_row.txt` 中加入说明文字；
- 不要把 `summary.md` 写成最终综述论文。