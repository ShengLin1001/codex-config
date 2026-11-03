---
name: p-archive-message
description: ALWAYS invoke BEFORE writing any forwarded message, link, paper, idea or tool note into this archive repo (inbox/, todo/, literatures/, tools/, DONOT_PROCESS.md), including a one-line note or appending to an existing entry. Do NOT archive without loading this skill first. Do NOT invoke for downloading PDFs or writing paper summaries (use p-literature-queue). 触发：整理：、归档、记一下、转发的公众号文章、存个链接、这个工具记下来、bot 收到的任何消息。
---

# 归档消息

目录和格式以仓库根目录的 `AGENTS.md` 为准，本 skill 只讲顺序。

## 步骤

1. **同步**：先 `git pull --rebase --autostash -q`。失败时照常归档，最后回复里注明"未同步"。
2. **原文入 inbox**：在 `inbox/$(date +%Y-%m).md` 末尾追加下面的块，原文一字不改：

   ````markdown
   ## `<date -Iseconds>`

   ```text
   <消息原文>
   ```

   → <去向路径，第 4 步回填>
   ````

3. **分类**：一条消息里有几件事，就拆成几项分别处理。
   - 论文或公众号论文推文 → 文献。公众号链接用 `python3 <本 skill 目录>/scripts/wx_fetch.py -url "<完整链接>"` 读，其他链接用 WebFetch，拿到标题、期刊和 DOI；读不到时标 `待补`，不要去猜 DOI。
   - 工具、skill、MCP、科研软件 → 追加到对应的 `tools/<topic>-tools.md`，条目格式照抄该文件最后一条。
   - 明确要做的事、调研请求、"帮我下载/精读" → `todo/I-want-to-do.md`；发散想法、讨论结论 → `todo/idea.md`。
   - 生活信息、无上下文的图片或链接、教程科普 → `DONOT_PROCESS.md` 一行 + 理由。
4. **写文献目录**：
   - 先查重：`grep -rlF "<DOI>" literatures --include=dois_raw.txt`，再用标题关键词 `grep -rlF` 搜 `note.txt`。已存在就只往 `note.txt` 追加来源行。
   - 新建 `literatures/$(date +%Y%m%d)-中文简名/`，写 `note.txt`（第一行 `状态：待下载`）和 `dois_raw.txt`。
   - 不下载 PDF，也不写 `paper.bib` 和 `summary.md`。
5. **回填 inbox 去向**，然后提交：

   ```bash
   git add <本次改动的路径>       # 只 add 自己写的文件，不用 -A
   git commit -q -m "docs(archive): :card_file_box: 归档 <一句话简述>"
   git push -q || { git pull --rebase -q && git push -q; }
   ```

6. **回复**：每项一行，写 `类别 → 路径`，有待补字段就列出来。不复述原文，也不展开总结。

## 讨论类消息

用户问文章内容、要观点或比较时，可以读链接后直接回答。值得保留的结论追加到 `todo/idea.md` 并提交；纯闲聊不落库，也不写 inbox。

## 陷阱

- 公众号链接要原样保留完整 URL，`sn=`、`chksm=` 这些参数都不能删，删了会打不开。
- 公众号链接不要用 WebFetch，它只会拿到"环境异常"验证页。`wx_fetch.py` 也失败时，就用消息里用户附带的标题和文字归档，缺的字段标 `待补`。
- 一个公众号推文介绍了多篇论文时，每篇建一个目录，`note.txt` 里写同一个来源行。
- 只发来一个 DOI 或 arXiv 号时，也按文献处理，来源写 `用户直接发送`。
- 不改历史目录名，不批量改写旧条目，不删除任何文件。
