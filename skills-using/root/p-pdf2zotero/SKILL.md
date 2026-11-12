---
name: p-pdf2zotero
description: "Use ONLY when the user explicitly asks to import local academic PDFs into the local Zotero Desktop library and tidy their metadata. This modifies the real Zotero database: do NOT invoke merely because Zotero / PDF / 文献 appear in the conversation, and NEVER reorganize other collections or delete attachments beyond what was asked. 触发：把这个目录的 PDF 导进 Zotero、按 DOI 去重导入、补 Extra 说明、加星级 tag、重评某个 collection 的星级。"
---

# 本地 PDF 导入 Zotero

用于实际修改本机 Zotero Desktop 文献库。默认只处理用户明确给出的 PDF 目录和目标 collection，不重组其他 collection，不删除正文或附件。

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-pdf2zotero`，Codex 写 `$p-pdf2zotero`。
对话里只是出现 Zotero、PDF、文献等字眼，不走本流程——它会改真实的 Zotero 数据库。

## 规则

- 先按 DOI，其次按规范化题名去重；库中已有条目时复用该条目，只补 collection 成员关系或缺失的本地附件。
- 星级和 `Extra` 先写成确认文档交用户修改，用户明确确认后才写库。导入和 collection 修正不必等这一步。
- 星级是批内相对排序：只标本批最该先读、最不可替代的几篇，建议数量受配额限制（见第 3 步）。
- `Extra` 是 Zotero 里直接展示的说明，不加 `Note:` 前缀；默认不创建 child note。
- 不覆盖现有 `Extra`、非星级 tag 或已有星级，除非用户明确要求重写或重评。
- 导入、collection 修正、`Extra` 和 tag 写入都必须在数据库备份和验证后完成。

## 1. 盘点与导入判断

1. 列出指定目录下的 PDF，计算 SHA-256，避免同一文件在目录内重复导入。
2. 用 PDF 首页/全文提取 DOI、题名、作者、年份；优先文件自身信息，不要求用户手工补录已有元数据。
3. 通过 Zotero 本地 API 查询 DOI 和题名，记录：
   - 已有 Zotero 条目 key；
   - 是否已在目标 collection；
   - 是否已有附件；
   - 本地目录中重复的 PDF。
4. 用 Zotero helper 检查桌面端、API 和 Connector：

```powershell
$helper = '<plugin-root>/skills/zotero/scripts/zotero.py'
python $helper status --json
python $helper selected-target --json
```

5. 目标 collection 不清楚时先问用户；目标清楚时可直接执行。

## 2. 导入并校正 collection

1. 只为缺失文献构造 RIS；RIS 必须包含 DOI、题名、已知作者/期刊信息和本地 PDF 附件路径 `L1`。
2. 确认当前 Zotero 选中 collection 就是目标 collection，再执行：

```powershell
python $helper import-ris --file <new-items.ris> --yes
```

3. Connector 超时或 API 暂时返回 500 时，不要立即重导。等待后按 DOI/题名及附件再次查询，因为 Zotero 常在后台继续完成导入。
4. Connector 若导入到错误 collection，关闭 Zotero、备份数据库后，仅修改对应 `collectionItems` 行；不要重新导入条目。

## 3. 起草星级与 Extra，交用户确认

1. 先用一句话写明本次研究目标（从对话和 collection 名推断，推断不出就问用户）。评分和 `Extra` 都以它为准，不看期刊名或引用数。
2. 待评条目：本批中没有星级、没有 `Extra` 的条目；重评时为用户指定的全部条目。读摘要、结论和关键图表后，逐篇起草建议星级和 `Extra`。
3. 建议星级守配额：有星条目不超过 `ceil(0.2 × N)`（N 为待评条目数），其中 `⭐⭐⭐⭐⭐` 至多 1 篇，允许一篇都不给。超额时按“去掉这篇会不会丢掉关键数据或方法”取舍。
   - `⭐⭐⭐⭐⭐`：本批最不可替代的一篇，如核心方法原文、直接决定结论的数据。
   - `⭐⭐⭐⭐`：主要实现或主要比较所依赖的文献。
   - `⭐⭐⭐`：有用的辅助参考。
   - 其余留空；不使用 `⭐`、`⭐⭐`。
4. `Extra` 格式为 `【标签】首句。补充。`：
   - 标签五选一：方法出处 / 关键数据 / 对照 / 综述背景 / 工具。
   - 首句约 20 字内，先总结这篇对研究目标最重要的内容，让人扫一眼就知道它是什么；需要时再补一两句关键数字、条件或内容上的注意点，全条约 60 字内。
   - 不只翻译题名；“DOI 未核对”“SI 已挂附件”这类处理状态不写进 `Extra`，只进汇报。
5. 把草稿写成确认文档，放在这批文献所属项目的交付文档目录（通常是当前工作目录的 `ai-guide/zotero/`），按交付文档命名规范命名（主题如 `<collection>-rating`）。开头写研究目标、配额和建议有星数，之后每篇一节，按建议重要性排序：

```markdown
## 1. Assessing melting points from machine learning interatomic potentials (2024) `ABCD1234`

- 星级：⭐⭐⭐⭐⭐
- Extra：【关键数据】PBEsol 算 Au 熔点为 1114 K。TPC-MTP 两相共存，PBE 844 K、实验 1337 K，见 Table S4。
- 理由：本批唯一直接给出 PBEsol 下 Au 熔点的文献。
```

   没有星级写 `- 星级：无`。
6. 用 Typora 打开确认文档（`Start-Process 'D:\software\Typora\Typora.exe' -ArgumentList '"<文件>"'`；没有 Typora 时用 `code -r <文件>`），并告诉用户路径。等用户改完并明确确认后再进入第 4 步。写库前重新读取该文件，以每节的 `星级` 和 `Extra` 两行为准，不用对话里的旧草稿。

## 4. 写入本地数据库

1. 通过 API 记录精确 item key、collection key、现有 `Extra`、星级和 child note 状态。
2. 正常关闭 Zotero。
3. 将 `D:\software\zotero\zotero.sqlite` 复制为带时间戳的备份。
4. 只修改确认的行：
   - `tags` / `itemTags`：添加评分；重评时先删除该条目原有星级 tag 的 `itemTags` 行；
   - `fieldsCombined(fieldName='extra')`、`itemData`、`itemDataValues`：写 `Extra`；
   - `collectionItems`：仅在导入落错 collection 时修正成员关系。
5. 直接修改元数据时，将受影响 `items.synced=0`，并更新时间戳。
6. 默认不写 `itemNotes`。用户明确要求把本次新增 child note 删除时，仅删除/标记这些已确认 note，不触碰导入前已有 note。
7. 运行 `PRAGMA integrity_check`，结果必须为 `ok`；随后重启 Zotero。

## 5. 验证与汇报

重启后通过 API 验证：

- 目标 collection 中的顶级条目数；
- 新 PDF 对应条目、附件和 collection 成员关系；
- collection 内没有重复 DOI；
- 每篇的星级和 `Extra` 与确认文档一致，且没有新增 child note。

汇报导入/复用数量、评分分布、`Extra` 覆盖数、处理状态（未核对项、已挂 SI 等）、任何跳过项、验证结果、确认文档路径与数据库备份路径。
