---
name: p-literature-queue
description: ALWAYS invoke BEFORE downloading papers, writing paper.bib or summary.md, or changing a 状态 line under literatures/ in this repo, including handling a single queued paper. Do NOT process queued literature without loading this skill first. Do NOT invoke on the VPS archive bot. 触发：处理待下载、下载文献队列、bot 归档的文献、补 bib、写文献总结、精读这篇、处理 I-want-to-do 里的调研。
---

# 文献队列（PC 端）

格式规范以 `AGENTS.md` 为准。

## 步骤

1. 先 `git pull --rebase --autostash`，再列出队列：

   ```bash
   grep -lx '状态：待下载' literatures/*/note.txt literatures/*/*/note.txt
   ```

   同时看一眼 `todo/I-want-to-do.md` 里新增的调研或下载请求。先把清单给用户看，确认这次要处理哪些。
2. **下载**：用 `dois_raw.txt` 的 DOI 调用 `p-literature-download`，PDF 存为该目录下的 `paper.pdf`。DOI 是 `待补` 时，先按 `note.txt` 的标题查到 DOI 并回填；标题也是 `待补` 时，用 `python3 <p-archive-message skill 目录>/scripts/wx_fetch.py -url "<链接>"` 读公众号原文补全。下载成功后，状态改为 `已下载`。
3. **BibTeX**：写 `paper.bib`。来源是公众号时，`note` 字段写公众号标题和 URL，规则见 AGENTS.md。
4. **总结**：通读 PDF 全文后写 `summary.md`，包括：问题、方法、主要结果、关键图表或数据、启发、局限、可复现信息。写完后状态改为 `已总结`。
5. 需要导入 Zotero 时，用 `p-pdf2zotero`。
6. 提交：只 add `.bib`、`summary.md`、`note.txt` 和 `dois_raw.txt`（PDF 已被 .gitignore 排除），然后 commit 并 push。

## 陷阱

- Elsevier：每次只开当前 DOI 的标签页，核对 DOI、PII 和题目一致后再下载，否则会把别的论文存进来。
- 下载失败时状态保持 `待下载`，在 `note.txt` 末尾追加一行 `- 下载失败：<日期> <原因>`，不要删掉状态行。
- 调研请求按 AGENTS.md 建 `YYYYMMDD-investigate-主题/`，完成后在 `todo/I-want-to-do.md` 对应条目标注完成和目录路径。
