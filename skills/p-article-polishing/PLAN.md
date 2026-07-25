# `p-article-polishing` 独立审视提示词

你是独立审稿人，不是当前 skill 的维护者。请基于原始 Word 修订证据，审视
`p-article-polishing` 是否真正提炼了 PJ 的科研写作风格，以及导师 Word 修订合并回
Git 跟踪的 Markdown/LaTeX 的流程是否可靠。

## 工作边界

- 仓库根目录：
  `F:\BaiduSyncdisk\version20240608\main_code_space\codex-config`
- 不调用 `p-skill-creator` 或 `skill-creator` 流程。
- 本轮只新增审视报告
  `skills/p-article-polishing/REVIEW.md`；不要修改 `SKILL.md`、
  `references/style-profile.md`、`agents/openai.yaml` 或
  `scripts/extract_docx_revisions.py`。
- 原始 DOCX 只读，不覆盖、不另存、不接受或拒绝修订。
- 保留现有提取脚本。可以检查和运行它，但不要删除、替换或扩展它。
- 不修改或暂存仓库中的其他改动，尤其是 `scripts/reinstall-skills.sh`。
- 不 commit、不 push；完成后只报告新增的 `REVIEW.md` 和验证结果。
- 不需要联网。结论必须来自本地文件、修订作者、批注和版本时间线。

用户已经明确确认：PJ 的连字符和悬挂连字符用法是正确的作者风格。不得把
`FCC- and HCP- phases`、`thermodynamic- and kinetic- mechanisms`、
`low-SFE`、`strain-induced`、`out-of-plane`、`phase-transition` 等写法判为
语法错误，也不要用通用 linter 或期刊习惯反驳这项约束。你要审视的是当前 skill
是否准确保护了这种用法及其语义，而不是重新裁决它是否“标准”。

## 审视顺序

### 1. 先从证据独立重建风格

为避免确认偏误，在形成自己的风格提炼之前，不要阅读当前的 `SKILL.md` 和
`references/style-profile.md`。可以先阅读提取脚本，确认它只读 DOCX，并按仓库
`AGENTS.md` 指定的 Codex Python 环境运行：

```powershell
& "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe" `
  skills/p-article-polishing/scripts/extract_docx_revisions.py -selftest
```

原始证据目录：

1. 第一篇文章

   - `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\20251001\old-figure-manuscriot`
   - `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\review\manuscript\old`
   - `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2024\相变机制\组稿\publish`

2. 第二篇文章

   - `F:\BaiduSyncdisk\version20240608\Being_a_phd_student_baiducloud\every-year\2026\面内应变-general\组稿\20260601_acta\manuscript`

优先检查这些有明确修订归属的文件：

- `manuscript_20250714-gao.docx`
- `manuscript_20250803-gao.docx`
- `manuscript_20250804-gao.docx`
- `manuscript_20250818-gao.docx`
- `manuscript_20250921-BY.docx`
- `manuscript_20260530.docx`

同时用以下净稿或批注稿判断某种改法是否在后续稳定保留：

- `manuscript_20260106-gy.docx`
- `manuscript_20260107-pj.docx`
- `manuscript_20260108-2.docx`
- `manuscript_20260605_3.docx`

身份归属：

- `俊 裴` / `Jun Pei`：PJ；
- `Yang Gao`：导师；
- `B YIN`：另一位合作者，不得与导师合并归因。

使用脚本分别提取 `Yang Gao` 的 tracked changes 和 comments。例如：

```powershell
& "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe" `
  skills/p-article-polishing/scripts/extract_docx_revisions.py `
  "<manuscript.docx>" -author "Yang Gao"

& "C:\Users\louis\mysoft\env\pyenv\codex\Scripts\python.exe" `
  skills/p-article-polishing/scripts/extract_docx_revisions.py `
  "<manuscript.docx>" -author "Yang Gao" -comments_only
```

先写出一份简洁的独立风格模型，再查看当前 skill。提炼时将规则分成四层，不能混为
“PJ 风格”：

1. PJ 明确确认或稳定保留的作者风格；
2. 导师多轮重复体现的审阅偏好；
3. 通用学术英语和科学论证底线；
4. Word、Git、Markdown/LaTeX 的工作流约束。

tracked changes 和 comments 是强归属证据；净稿之间的差异只能作为弱归属证据。
一次性改写、后来撤销的改写、作者单位、参考文献机械调整、纯 Word 排版、
response letter 和仅 SI 内容不能直接提升为稳定正文风格。

### 2. 再逐条审视当前 skill

完整阅读：

- `skills/p-article-polishing/SKILL.md`
- `skills/p-article-polishing/references/style-profile.md`
- `skills/p-article-polishing/agents/openai.yaml`
- `skills/p-article-polishing/scripts/extract_docx_revisions.py`

逐条判断当前规则属于哪一层，并给出以下结论之一：

- `supported`：有跨版本或明确用户指令支持；
- `overgeneralized`：由少量或特定语境证据扩大而来；
- `missing`：证据稳定存在但当前 skill 未提炼；
- `contradicted`：与用户确认、后续净稿或可靠修订证据冲突；
- `generic`：合理，但属于通用写作要求而非 PJ 独有风格；
- `format-specific`：只适用于 Word、Markdown、LaTeX 或 Git 工作流。

重点回答：

1. 当前内容是否仍像修改历史摘要，而不是可直接执行的写作风格？
2. 哪些规则真正体现 PJ 的句子、段落、论证和措辞偏好？
3. 哪些规则其实来自导师审阅、合作者建议或通用写作常识，却被误写成 PJ 风格？
4. 当前例句和禁用表达是否有足够证据，还是一次性样本？
5. 对标题、摘要、引言、方法、结果、Discussion、结论和图注的规则是否有证据支撑？
6. 连字符保护是否明确、无内部冲突，并能阻止通用语法检查器误改？
7. frontmatter description 和 `agents/openai.yaml` 能否准确触发“按 PJ 风格润色”及
   “合并导师 Word 修订”两类任务？

不要因规则“听起来正确”就判为 `supported`。每个重要结论都要指出具体文件名、
修订作者和简短 before/after 或批注证据；短引文即可，不要大量复制论文正文。

### 3. 单独审视 Word → Markdown/LaTeX 合并流程

把当前流程视为语义三方合并：

- **base**：导出给导师的 Markdown/LaTeX 对应 commit；
- **theirs**：导师修订后的 Word 文本和批注意图；
- **ours**：当前 Markdown/LaTeX 工作树。

至少用三个场景做纸面演练：

1. `ours == base`，导师只改自然语言；
2. `ours != base`，当前稿已更新数据、术语、引用或段落结构；
3. Word 中含 MathType、公式对象、域代码、批注或纯格式变化。

检查当前流程是否：

- 要求可靠确定 base，而不是根据文件日期猜测；
- 合并导师的修改意图，而不是整段覆盖 ours；
- 能恢复和保护 LaTeX 命令、公式、引用键、交叉引用、Markdown 结构；
- 将 MathType 或公式提取空白识别为提取伪影，而不是删除；
- 区分导师文字修改、批注待办和纯 Word 排版；
- 在当前数据与导师旧文本冲突时保留已确认数据并报告冲突；
- 给出足够的最小 diff、逐项核对和冲突升级规则。

只指出现有脚本真实能够或不能够做的事。不要把“打印修订和批注”的脚本描述成自动
写回、自动对齐或自动三方合并工具。

## 交付文件

将结果写入 `skills/p-article-polishing/REVIEW.md`，使用以下结构：

1. **最终判断**：`ready`、`needs targeted revision` 或
   `needs re-derivation`，并用不超过五句话说明原因；
2. **P0/P1/P2 发现**：按影响排序，只列有证据的问题；
3. **独立重建的写作风格**：一页以内，并明确区分上述四层；
4. **逐条审视表**：当前规则、层级、证据、判断、严重度、最小修改建议；
5. **连字符专项结论**；
6. **Word 三方合并流程审视**：包含三个演练场景；
7. **最小修订计划**：精确到文件和章节，但本轮不要应用；
8. **仍需 PJ 确认的问题**；
9. **验证命令与结果**。

报告应简洁、可核查，避免泛泛的写作建议。若没有足够证据支持某项“个人风格”，应
明确降级为导师偏好、通用规则或待确认项，而不是补充猜测。
