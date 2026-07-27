---
name: p-article-shared
description: >-
  Internal shared reference package for the installed p-article-polishing and
  p-article-evaluated skills. Not a standalone workflow and not a user-facing
  entry point; do not invoke it directly for writing, polishing or evaluation
  requests. Holds the single definition of the academic expression bank, the
  section function skeleton, and the corpus provenance that both skills read on
  demand.
---

# P Article Shared References

只作为 `p-article-polishing` 和 `p-article-evaluated` 的依赖使用。用户的写作、润色、评价请求一律由那两个 skill 接。

按需读取被点名的那一份文件，不预载整个包；读完回到发起的 skill 执行它自己的流程、输出格式和交付自检。

| 何时读 | 文件 |
|---|---|
| 判断动词强度、限定词、空白类型、因果强度、连接词、意义句边界，或核对模型腔与标点 | [expression.md](expression.md) |
| 需要章节或图注的功能序列——写作时按它组织，评价时按它反查 | [section-skeleton.md](section-skeleton.md) |
| 新增参考论文、新增修改记录，或需要说明某条规范的出处 | [corpus.md](corpus.md) |

这里只放两个 skill 都要用的规范。写作独有的流程留在 `p-article-polishing`，评价独有的审计留在 `p-article-evaluated`。同一条规范不在两处各存一份。
