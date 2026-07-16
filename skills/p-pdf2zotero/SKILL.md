---
name: p-pdf2zotero
description: Import local academic PDFs into a specified Zotero collection without duplicates, attach only missing PDFs, rate only clearly important papers with star tags, and write concise searchable descriptions to Extra. Use when the user asks to put a local PDF folder into Zotero and organize its importance or directly visible notes.
---

# 本地 PDF 导入 Zotero

用于实际修改本机 Zotero Desktop 文献库。默认只处理用户明确给出的 PDF 目录和目标 collection，不重组其他 collection，不删除正文或附件。

## 规则

- 先按 DOI，其次按规范化题名去重；库中已有条目时复用该条目，只补 collection 成员关系或缺失的本地附件。
- `Extra` 是直接展示的说明位置。写 1 句简明中文，不加 `Note:` 前缀；默认不创建 child note。
- 仅对明确重要的文献添加星级 tag，使用 `⭐⭐⭐`、`⭐⭐⭐⭐`、`⭐⭐⭐⭐⭐`。重要性不明确、仅背景相关或低价值的文献保持没有星级 tag。
- 不覆盖现有 `Extra`、非星级 tag 或已有星级，除非用户明确要求重写/重新评分整个 collection。
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

## 3. 重要性评分

以当前研究目标为准，而不是期刊名或引用数。仅在判断明确时添加一个星级 tag：

- `⭐⭐⭐⭐⭐`：核心理论/通用方法，或直接提供当前问题所需的高阶弹性常数与验证基准。
- `⭐⭐⭐⭐`：与目标材料、结构、应变路径或计算方法直接相关，可支撑主要实现或比较。
- `⭐⭐⭐`：可靠的实现细节、材料案例或稳定性/连续体联系，可作辅助参考。
- 不加 tag：背景、弱相关应用、不可复用的案例，或无法可靠判断重要性。

保留无星级为空白。没有用户明确授权时，不添加 `⭐` 或 `⭐⭐`，也不因为“所有文献”要求而给低价值条目凑评分。

## 4. 写入 Extra 与本地数据库

对需要说明的父条目，在 `Extra` 写一条便于检索的中文短句，例如：

```text
50-340 GPa 下 hcp epsilon-Fe 的二、三阶常数、Gruneisen 参数与稳定性。
```

写入前后遵循以下顺序：

1. 通过 API 记录精确 item key、collection key、现有 `Extra`、星级和 child note 状态。
2. 正常关闭 Zotero。
3. 将 `D:\software\zotero\zotero.sqlite` 复制为带时间戳的备份。
4. 只修改确认的行：
   - `tags` / `itemTags`：添加评分；
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
- 仅已判定重要的条目具有星级；
- 需要说明的条目 `Extra` 非空，且没有新增 child note。

汇报导入/复用数量、未评分数量、评分分布、`Extra` 覆盖数、任何跳过项、验证结果与数据库备份路径。
