---
name: p-article-polishing
description: "Infer and apply PJ's scientific writing style from historical revisions and final accepted manuscripts. Use when polishing academic prose, identifying PJ's preferred and disliked writing patterns from Git or DOCX history, or updating the bundled style profile from evidence. Preserve scientific meaning, numbers, citations, terminology, and intentional hyphenation."
---

# P Article Polishing

用于从历史修订和最终成稿中提炼 PJ 真正喜欢与不喜欢的写法，再据此润色科研文本。不要把修改历史复述成风格，也不要把通用论文教程冒充个人偏好。

开始前阅读 [references/style-profile.md](references/style-profile.md)。它是当前已确认规则的简表；若与本次用户指令或更新的最终稿冲突，以新证据为准。

## 边界

- 只负责提炼写作偏好、识别应避免的写法和润色文本。
- 不负责 Word 修订合并、格式转换、接受或拒绝修订、版本发布或 Git 管理。
- DOCX 脚本只读取修订证据，不修改 Word，也不写回其他格式。
- 不把单次导师修改、纯排版、参考文献整理或通用语法规则直接归为 PJ 风格。
- 不发明或擅改数据、机理、引用、比较基准、限定条件、符号、数值和单位。

## 证据顺序

按以下顺序处理冲突：

1. 用户本次明确要求；
2. 对应的最终成稿或用户明确认可的版本；
3. 在多个独立段落或版本中重复出现、且在最终稿保留的修改；
4. 单次 tracked change、批注或 Git diff；
5. 通用学术英语规则，仅用于保证正确性，不称为个人风格。

## 提炼风格

### 1. 配对证据

确定修订记录对应的初稿、修改者和最终稿。只检查与当前任务相关的文件或章节；无法确认版本关系时，降低结论置信度，不根据文件日期猜测。

### 2. 提取修改

按需使用最小范围的 Git diff：

```bash
git diff --word-diff=plain <old> <new> -- path/to/manuscript
```

需要读取 DOCX 修订时，使用现有脚本：

```powershell
python <skill-dir>/scripts/extract_docx_revisions.py manuscript.docx -author "<author>"
```

只把输出作为 before/after 与批注证据；不要把它扩展为 Word 合并流程。

### 3. 判断是否属于个人风格

在工作上下文中用最小证据表记录：

| 写法 | 修订证据 | 最终稿状态 | 分类 | 适用范围 |
|---|---|---|---|---|
| before → after | 文件/版本/作者 | 保留、撤销或未知 | 喜欢、避免、条件性或证据不足 | 句子、段落或特定语境 |

- 将用户明确确认，或在独立实例中重复出现并被最终稿保留的模式，归为“喜欢”。
- 将用户明确否定，或反复被替换且未回到最终稿的模式，归为“避免”。
- 将只在特定语境成立的选择归为“条件性”，不要扩大成全局规则。
- 将单次改写、归属不清或未找到最终稿验证的模式归为“证据不足”。
- 排除纯格式、作者单位、参考文献机械调整和只改变科学内容而不反映表达偏好的修改。

### 4. 固化规则

仅在用户要求更新风格档案时修改 `references/style-profile.md`。只写可执行的“喜欢”和“避免”，合并重复规则，删除已被新证据推翻的规则；不要保存冗长历史摘要。

## 应用风格

1. 先标出目标文本中命中的“避免”模式，再按“喜欢”模式做最小修改。
2. 保持事实、因果、数据、图表、引用、术语、公式和限定条件不变。
3. 将风格规则作为决策依据，不机械套用固定句型或段落模板。
4. 对证据不足的偏好保持原文；对科学歧义请求作者确认，不用流畅措辞掩盖。
5. 保留 PJ 已确认的连字符和悬挂连字符写法，不让通用 linter 擅自规范化。

## 检查与交付

- 确认每项风格修改都能追溯到已确认规则，或只是必要的语言纠错。
- 确认没有把单次修改升级为全局偏好。
- 确认科学含义、数字、单位、引用和术语未漂移。
- 交付润色结果，并简要列出采用的偏好、避开的写法和仍需确认的问题。
