# 30-wiki Synthesis Page Structure Template

Annotated skeleton of a `30-wiki/` synthesis page, extracted from the three
proven pages in this vault:

- `30-wiki/vasp.md` — science-topic synthesis (5 source dirs, 12 source files)
- `30-wiki/tools.md` — tool-collection synthesis (9 source files, 6 topic dimensions)
- `30-wiki/pjvasp-package.md` — software-package synthesis (23 source files, 6 topic dimensions)

Use this as a structural checklist when authoring a new synthesis page. The
section count and topic dimensions adapt to the source material — do not
force every page into exactly six sections. But every page MUST have:
frontmatter, opening blockquote, topic-dimensional body, pitfalls section,
and the two-part footer.

## Skeleton

```markdown
---
title: "<Chinese descriptive title — what this page covers, comma-separated>"
date: <YYYY-MM-DD>
tags: [<slug>, wiki, <topic-tags>, synthesis]
source_repo: native
imported: <YYYY-MM-DD>
---

> 本页综合 `<source-dir>/` 下 N 篇源文件（<one-line description of what kinds>），
> 按"<topic-dim-1> / <topic-dim-2> / ... / 踩坑"N 个主题维度重新组织，去重后
> 每条只讲一次，细节用 `[[源文件名]]` 指回原始笔记。
>
> **与 [[other-wiki-page]] 的分工**：<other-page> 专注 X；本页专注 Y。凡
> [[other-wiki-page]] 已综合的条目均交叉引用而非重复。
>
> **与 [[third-wiki-page]] 的分工**：<scope boundary>。

## 1. <topic-dim-1>

<prose synthesizing facts from multiple source files, each fact cited with
`→ [[source-file-name]]`. Tables for structured data. No per-file headings.>

## 2. <topic-dim-2>

<...>

## 3. <topic-dim-3>

<...>

## N. 踩坑

汇总各源文件记录的踩坑，每条只给结论和指路，完整上下文见链接：

1. **<pitfall title>**：<one-line conclusion>. → [[source-file-1]]、[[source-file-2]]
2. **<pitfall title>**：<...>. → [[source-file-3]]
...

---

## 综合了以下源页面

- [[source-file-1]] — `<path/to/source-file-1.md>`（<which section cited it>）
- [[source-file-2]] — `<path/to/source-file-2.md>`（<which section cited it>）
...

交叉引用：[[other-wiki-page]] — `30-wiki/other-wiki-page.md`（<which section
already covers X; this page cross-links rather than repeats>）；[[third-wiki-page]]
— `30-wiki/third-wiki-page.md`（<scope boundary>）。

未采纳的候选及排除理由：`<path/to/excluded-source.md>`（<one-line reason:
already cited by other-wiki-page / only images no text / off-topic / project
management file not knowledge source>）。
```

## Annotations

### Frontmatter
- `title`: Chinese, descriptive, comma-separated subtopics. Goes in the
  `title` field, NOT the filename.
- `source_repo: native` — this is vault-original content, not imported.
  (SCHEMA.md §1.)
- `imported`: today's date — when the page was created.
- `tags`: always include `wiki` and `synthesis` plus the project/topic slug.

### Opening blockquote
Mandatory. Three jobs, in order:
1. **Scope declaration**: how many source files, what kinds, what topic
   dimensions the page uses. Sets reader expectations.
2. **Cross-wiki division of labor**: for every existing `30-wiki/` page that
   overlaps, declare who covers what. This is the dedup contract — without
   it, you will repeat content and the reader will see the same fact twice.
3. **Third-party scope boundaries** (if applicable): e.g. Python environment
   management belongs to `[[python-toolchain]]`, not this page.

### Topic-dimensional body sections
- Numbered H2 (`## 1.`, `## 2.`, ...). Not source filenames.
- Every factual claim cites its source inline: `→ [[source-file-name]]`
  (stem only, no `.md`, no path).
- Tables for structured/quantitative data (parameter lists, script tables,
  stage-status grids).
- When a subtopic is already in another wiki page, write
  "见 [[other-page]] 第N节" and stop — do not re-explain.

### Pitfalls section
- Always the last numbered section before the footer.
- Each pitfall: numbered, bold title, one-line conclusion, `→ [[source]]`.
- Do not reproduce full debug transcripts — those live in the source files.

### Footer (SCHEMA.md §5 — mandatory)
Three parts:
1. **综合了以下源页面**: every source file as `[[]]` link + path +
   one-line note on which section cited it. This is the provenance trail.
2. **交叉引用**: other `30-wiki/` pages, with path and a note on which
   section already covers the overlapping subtopic.
3. **未采纳的候选及排除理由**: source files you considered but did NOT
   synthesize, each with a one-line reason. This proves you didn't silently
   skip anything. Common reasons: "already cited by [[other-page]] as
   未采纳候选", "正文只有图片无可综合的文字", "项目管理文件而非知识源文件",
   "与本页主题维度不重叠".

## Adapting topic dimensions

The section count and dimension names depend on the source material:

| Page type | Typical dimensions |
|---|---|
| Software tool package | 概览 / 核心功能 / 工作流 / 文档与演进 / 踩坑 |
| Science topic (VASP, DFT) | 安装 / 理论 / 参数与收敛 / 工具链 / 踩坑 |
| Tool collection | 按工具分组（ASE / Pymatgen / ...）/ 其他工具 / 书签精选 |
| Method / algorithm | 理论 / 实现 / 实践 / 踩坑 |

When in doubt, look at what the source files naturally cluster around —
the clusters ARE your topic dimensions.
