# 参考论文语料索引

本文件登记用于提炼学术表达、论证功能和章节组织的论文。原始 PDF 位于 `ref/`；普通润色只读取已提炼的 [academic-style.md](academic-style.md)。

## 当前语料

| ID | 本地文件 | 论文与来源 | 来源角色 | 主要用途 |
|---|---|---|---|---|
| R1 | `01-1597741298-837123.pdf` | *Ultrahard carbon film from epitaxial two-layer graphene*, Nature Nanotechnology, DOI `10.1038/s41565-017-0023-9`, 7 pages | Yang Gao 署名论文；导师相关语料 | 紧凑摘要、定量结果、实验与计算互证、机理因果 |
| R2 | `01-1597741336-837125.pdf` | *Elastic coupling between layers in two-dimensional materials*, Nature Materials, DOI `10.1038/nmat4322`, 8 pages | Yang Gao 署名论文；导师相关语料 | 已知—未知对照、方法引入、谨慎解释、参数敏感性 |
| R3 | `01-1606899164-840005.pdf` | *Band Engineering of Large-Twist-Angle Graphene/h-BN Moiré Superlattices with Pressure*, Physical Review Letters, DOI `10.1103/PhysRevLett.125.226403`, 6 pages | Yang Gao 署名论文；导师相关语料 | Letter 体例、方法推进、压力依赖、理论确认实验 |
| R4 | `1-s2.0-S1359645426001060-main.pdf` | *FCC-HCP phase transition in ultrathin gold films: A first-principles investigation*, Acta Materialia 308 (2026) 122000, DOI `10.1016/j.actamat.2026.122000`, 14 pages | PJ 接收稿；另有导师修订证据 | 个人风格最终状态、方法验证、主结果组织、Discussion 与结论 |
| R5 | `s41467-025-56047-x.pdf` | *Challenging the ideal strength limit in single-crystalline gold nanoflakes through phase engineering*, Nature Communications, DOI `10.1038/s41467-025-56047-x`, 10 pages | 课题组/参考语料 | 实验—理论联合论证、强度比较、图文对应、有边界的意义 |

元数据与页数已于 2026-07-25 从本地 PDF 核对。

## 权重与状态

- R1–R3 是导师相关语料，R4 是带历史修订证据的 PJ 最终稿，R5 是课题组/参考语料。
- 参考论文中的表达可作为导师偏好候选，但不能仅凭署名推定由导师亲自修改。
- `candidate`：一个来源中出现的可复用表达。
- `repeated`：至少两个独立来源采用同一修辞功能或表达模式，可作为默认候选。
- `confirmed`：用户明确确认，或历史修订重复出现并在最终稿保留；只在 [personal-style.md](personal-style.md) 中作为个人规则执行。

## 功能覆盖

| 修辞功能 | 已核对来源 |
|---|---|
| 研究重要性与挑战 | R1、R2、R3、R4、R5 |
| 已知事实与研究空白 | R1、R2、R3、R4、R5 |
| 直接引出本文工作 | R1、R2、R3、R4、R5 |
| 图表定位与定量趋势 | R1、R2、R3、R4、R5 |
| `show / indicate / suggest / demonstrate / reveal / confirm` 证据强度 | R1、R2、R3、R4、R5 |
| 对照、基准和逐项对应 | R1、R2、R3、R4、R5 |
| 机理归因与促进/阻碍关系 | R1、R3、R4、R5 |
| 不确定性、限制和待解决问题 | R2、R3、R4、R5 |
| 有边界的意义表达 | R1、R4、R5 |

这些功能已提炼到 `academic-style.md`。来源标签表示该模式可在相应论文中追溯，不表示模板是逐字引文。

## 更新规则

- 根据待补充的修辞功能选择代表性论文；不要求每次遍历全部 `ref`。
- 保存短模板、语义条件和来源 ID，不复制长句或整段原文。
- 单篇好表达可进入表达库并标为 `candidate`；不得因只有一个来源而丢弃。
- 只有至少两个独立来源支持时才标为 `repeated`；不得写“全部论文均采用”而不逐项核对。
- 语料表达与目标稿、期刊体例或 `personal-style.md` 冲突时，服从后者。
