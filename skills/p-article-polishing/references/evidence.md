# 写作偏好证据索引

本文件用于维护和冲突核查，普通润色任务不读取。原始 DOCX/PDF 保持只读；这里只记录来源、修改者、代表性证据和当前判断，不保存全部修订转录。

## 状态

- `confirmed`：PJ 明确确认，或多个独立修订重复出现并在后续净稿保留。
- `candidate`：单次修改或尚未完成最终稿核验。
- `conditional`：只适用于特定章节、期刊、学科或上下文。
- `deprecated`：被更新证据推翻；保留溯源但不再执行。

## 身份

- `俊 裴` / `Jun Pei`：PJ。
- `Yang Gao`：导师。
- `B YIN`：合作者；其修改不得归入导师证据。

## 历史文章来源

### H1 第一篇：FCC-HCP phase transition in ultrathin gold films

原始路径：

- `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\20251001\old-figure-manuscriot`
- `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\review\manuscript\old`
- `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\publish`

高信息量修订稿：

| 文件 | Yang Gao tracked revisions | Yang Gao comments | 用途 |
|---|---:|---:|---|
| `manuscript_20250714-gao.docx` | 39 | 10 | 早期结构与术语 |
| `manuscript_20250803-gao.docx` | 23 | 29 | 段落、方法和图文对应 |
| `manuscript_20250804-gao.docx` | 25 | 28 | 上一轮修改的延续核查 |
| `manuscript_20250818-gao.docx` | 52 | 26 | 定量、图 panel、机理与逻辑 |
| `manuscript_20250921-BY.docx` | 0 | 0 | 另有 B YIN 的 35 条修订，单独归因 |

后续净稿/批注稿：

- `manuscript_20260106-gy.docx`
- `manuscript_20260107-pj.docx`
- `manuscript_20260108-2.docx`
- 最终发表 PDF：`publish\1-s2.0-S1359645426001060-main.pdf`

这些后续文件用于判断修改是否保留；重复出现的同一 comment 不重复计为独立证据。

### H2 第二篇：in-plane-strain study

原始路径：

- `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2026\面内应变-general\组稿\20260601_acta\manuscript`

高信息量文件：

| 文件 | Yang Gao tracked revisions | Yang Gao comments | 用途 |
|---|---:|---:|---|
| `manuscript_20260530.docx` | 40 | 14 | 句式、逐材料数据和 Discussion 逻辑 |
| `manuscript_20260605_3.docx` | 0 | 0 | 后续净稿核验 |

## 代表性证据

| ID | 来源 | 证据摘要 | 当前判断 |
|---|---|---|---|
| E01 | H1 `20250714`, comment 383；H1 `20250818`, comment 1191 | `γ-line` 未定义，要求首次出现先解释 | `confirmed`：P01 |
| E02 | H1 `20250818`, comment 1686；H1 `20260106/07/08` comments | `a’`、`ICOHP` 等符号或缩写缺少定义 | `confirmed`：P01 |
| E03 | H1 `20250818`, comment 880 | 图只给 lattice constant，不能让读者自行计算 3% strain | `confirmed`：P02 |
| E04 | H2 `20260530`, comments 450、484 | Au 之外必须补充 Cu、Ag 的具体数据 | `confirmed`：P02 |
| E05 | H1 `20250803/04`, comments 245/252、301/321；H1 `20250818`, comments 1236、1240 | 图号或结论位置不明确，反复追问 `Figures?`、`Where?` | `confirmed`：P03 |
| E06 | H1 `20250818`, comment 1222 | 要求大致说明 Fig. 8 的每个 panel | `confirmed`：P03 |
| E07 | H1 `20250803/04`, comments 573/622、582/631；H2 `20260530`, comments 605、627 | 要求解释图中参数、横轴、标记和数据点 | `confirmed`：P03 |
| E08 | H1 `20250803/04`, comments 307/335 | 用 `(1)/(2)` 区分两个 process，并说明各自对应因素 | `confirmed`：P04 |
| E09 | H1 `20250803`, comments 187、341、360 | 段首需要总起句，避免没头没尾的孤句 | `confirmed`：P04 |
| E10 | H1 `20250818`, comment 1604；H2 `20260530`, comment 585 | 不得绕回已排除的 surface effect；Discussion 不得推翻前文结论 | `confirmed`：P04 |
| E11 | H1 `20260106/07/08`, comments 91/96/78 等 | 多次标记内容 `redundant` | `confirmed`：P05 |
| E12 | H1 `20250818`, comments 36、1245、1316；H2 `20260530`, comments 91、629 | 强主张需要足够引用，引用顺序应服务于简洁逻辑 | `confirmed`：P02、P07 |
| E13 | H1 tracked revisions | `warrants → needs`、`likelihood → possibility` 等局部准确性修改 | `conditional`：不可全局替换 |
| E14 | H2 `20260530`, tracked revision paragraph 14 | 名词化开头改为 `By precisely tailoring ...`，并展开 FCC/HCP 两支比较 | `confirmed`：P06 的句法原则 |
| E15 | H1 多轮 tracked revisions | 图作句子主语时多次由 `Fig.` 改为 `Figure` | `conditional`：P10 |
| E16 | H1 最终发表稿、H2 后续净稿及用户确认 | `FCC- and HCP- phases` 等悬挂连字符稳定保留 | `confirmed`：P09 |
| E17 | H2 `20260530`, tracked revisions paragraphs 55、71 | `This is the first/second main result of this paper.` 在结果小节保留 | `conditional`：P08 |
| E18 | H1/H2 最终文本与 tracked revisions | `central topic`、`remarkable`、`It is worth noting` 在有证据语境中被采用 | `confirmed`：废弃对这些词的全局禁用 |

## Git 溯源

`codex-config` 中与本 skill 相关的历史提交：

- `5ef01f5`：首次创建个性化润色 skill。
- `6c55a2e`：聚焦“修订证据 → 最终稿 → 风格分类 → 润色”。
- `5373d89`：把大量规则内联到 `SKILL.md`，同时删除独立 profile 和只读提取脚本。

Git 历史是维护溯源，不是普通润色时的运行上下文。旧版本若与当前证据状态冲突，以本文件和 `personal-style.md` 的当前状态为准。

## 更新方法

1. 对新的 DOCX 按作者分别提取 revisions 和 comments。
2. 找到后续净稿或接收稿，判断修改被保留、撤销还是未知。
3. 在本文件新增证据行；不要把全部提取输出粘贴进来。
4. 只有证据达到 `confirmed` 时更新全局个人规则。
5. 若新证据推翻规则，将旧判断标为 `deprecated`，不要保留两个相互冲突的运行规则。
