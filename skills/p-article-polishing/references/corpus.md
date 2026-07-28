# 语料来源与维护

只在新增参考论文、加入新的修改记录，或需要说明某条规范的出处时读本文件。普通写作和润色任务不需要。

## 已发表论文语料

[language.md](language.md) 的表达提炼自 `ref/` 下的本地 PDF：

| 本地文件 | 论文与来源 | 主要贡献的表达类型 |
|---|---|---|
| `01-1597741298-837123.pdf` | *Ultrahard carbon film from epitaxial two-layer graphene*, Nature Nanotechnology, `10.1038/s41565-017-0023-9` | 紧凑摘要、定量结果、实验与计算互证、机理因果 |
| `01-1597741336-837125.pdf` | *Elastic coupling between layers in two-dimensional materials*, Nature Materials, `10.1038/nmat4322` | 已知—未知对照、方法引入、谨慎解释、参数敏感性 |
| `01-1606899164-840005.pdf` | *Band Engineering of Large-Twist-Angle Graphene/h-BN Moiré Superlattices with Pressure*, Physical Review Letters, `10.1103/PhysRevLett.125.226403` | Letter 体例、方法推进、理论确认实验 |
| `1-s2.0-S1359645426001060-main.pdf` | *FCC-HCP phase transition in ultrathin gold films: A first-principles investigation*, Acta Materialia 308 (2026) 122000, `10.1016/j.actamat.2026.122000` | 本组接收稿；方法验证、主结果组织、Discussion 与结论 |
| `s41467-025-56047-x.pdf` | *Challenging the ideal strength limit in single-crystalline gold nanoflakes through phase engineering*, Nature Communications, `10.1038/s41467-025-56047-x` | 实验—理论联合论证、比较、图文对应、有边界的意义 |

元数据已于 2026-07-25 从本地 PDF 核对。

五篇集中在材料科学、凝聚态物理和第一性原理计算。SKILL.md 的四条自检是跨学科通用的论证要求，但本表达库的用词和章节习惯属于这个方向，不要当成综述、临床、方法学等稿型的依据。

## 修改记录来源

历史稿件路径见 `ref/历史修改文章记录.txt`。SKILL.md 的四条自检提炼自这两篇稿件的 tracked changes 与 comments：

- 第一篇（相变机制，已发表）：`manuscript_20250714` / `0803` / `0804` / `0818`，及 `20260106`–`0108` 净稿。
- 第二篇（面内应变）：`manuscript_20260530`，及 `20260605_3` 净稿。

修改记录用于**发现问题的类型**，不用于积累逐条清单。同一类问题反复出现，才值得写进自检条目；只出现一次的具体词语替换只在原句成立，不进任何规范。

读取 DOCX 修订与批注：

```powershell
& "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe" `
  skills/p-article-polishing/scripts/extract_docx_revisions.py `
  "<manuscript.docx>" -author "<name>"
```

脚本只读 DOCX，输出原始修订和批注；不做版本对齐或三方合并。原始 DOCX 与 PDF 保持只读。

## 维护方法

新增语料时：

1. 按当前缺口选代表性论文，不要求遍历全部 `ref/`。
2. 在上表登记题目、DOI、本地文件名和用途。
3. 只提炼短表达、修辞功能、语义条件和段落逻辑；不复制长句或整段原文。
4. 写入 [language.md](language.md) 对应功能表，保持"功能 → 表达 → 何时使用"三列。同一功能已有等价表达时替换或合并，不并列堆放。
5. 章节功能或论证顺序层面的发现，写入 [structure.md](structure.md)，不放进表达库。

润色对话中作者的回答也是语料，但**不直接改 `language.md`**：先按 SKILL.md「偏好回写」追加到 `inbox.md`，由作者合并进 Git 仓库。合并时同样按上面第 4 条处理——落到对应功能表的「何时使用」列，能替换已有条目就替换，不并列堆放。分不清是稳定偏好还是一次性判断的，先不写。

新增修改记录时：

1. 按作者提取 revisions 和 comments，找到后续净稿判断修改是否被保留。
2. 判断这条修改属于哪一类问题：断言不可查、段落功能不清、主线断裂，还是越权改写。
3. **已被现有自检覆盖的，不新增条目**；只在出现了四条自检都覆盖不到的新类别时，才扩写 SKILL.md。
4. 新证据与旧规范冲突时，直接改现有条目，不保留两条互相矛盾的规则。

保持精简：整个 skill 应停留在一份 SKILL.md 加三份 reference。新增内容前先问它能不能并进已有条目。
