---
name: vault-wiki-synthesis
title: Obsidian Vault 30-wiki Synthesis Page Authoring
description: "Use when creating a 30-wiki page from multiple source files."
tags: [vault, obsidian, wiki, synthesis, creation-layer]
category: vault
---

# Obsidian Vault 30-wiki Synthesis Page Authoring

Use when the task is to **create or substantially revise a `30-wiki/<slug>.md` synthesis page** that combines knowledge from multiple source files in `10-sources/` or `20-projects/<slug>/notes/`. This is the vault's **creation layer** — the only layer where cross-source synthesis, dedup, interlinking, and inference are allowed. The output is a reorganized knowledge page, NOT a concatenation or per-source-file summary.

The vault lives at `~/mysoft/pei/myobsidian` (or the session WORKSPACE PATH). Conventions are defined in `AGENTS.md` (three-tier write model — `30-wiki/` is the only creation layer) and `SCHEMA.md` (frontmatter, naming, double-link syntax, §5 source-page footer requirement). Read both before authoring.

**Relationship to `vault-integration`**: that skill covers the *archive layer* (importing source Markdown into `10-sources/`/`20-projects/` verbatim, with provenance). This skill covers the *creation layer* (synthesizing multiple already-imported source files into a new `30-wiki/` page). They are sequential: integration first, synthesis second. A source file must already live in `10-sources/` or `20-projects/` before it can be synthesized into `30-wiki/`.

## When to use

- "在 30-wiki/ 下新建一篇综合知识页，把 20-projects/X/notes/ 下未被引用的源文件综合成结构化知识页"
- "把 10-sources/Y/ 下的几篇笔记综合成一篇 wiki 页"
- "为项目 X 写一个 wiki 总览页"
- "30-wiki/vasp.md 需要补充新导入的源文件"
- Any task that creates or revises a `30-wiki/*.md` page by combining multiple source files.

## When NOT to use

- Importing source Markdown into `10-sources/`/`20-projects/` → use `vault-integration` (archive layer, verbatim copy).
- Editing a single source file's content → no synthesis needed.
- Creating a page that is just one source file reformatted → that's not synthesis; either import verbatim or write a stub linking to the source.

## Workflow

### 1. Read vault conventions and reference wiki pages

- `AGENTS.md` §1 (three-tier write model: `30-wiki/` is the ONLY creation layer; `10-sources/`/`20-projects/` are read-only raw material — do NOT modify them during synthesis).
- `SCHEMA.md` §1 (frontmatter for `native` vault-original pages: `source_repo: native`), §2 (kebab-case filenames), §3 (`[[file-name]]` double-link syntax), §5 (source-page footer requirement).
- **Read 1-2 existing `30-wiki/*.md` pages as structural templates** — `30-wiki/vasp.md` and `30-wiki/tools.md` are the canonical examples. Note: topic-dimensional H2 sections, `> blockquote` opening that declares scope and cross-wiki division of labor, per-section `→ [[source-file]]` pointers, footer with "综合了以下源页面" list + "未采纳的候选及排除理由".

### 2. Inventory the source files to synthesize

The task usually specifies which source files. If it says "未被任何 wiki 页引用的孤儿文件":

- List all `.md` in the target `20-projects/<slug>/notes/` (or `10-sources/<topic>/`).
- For each existing `30-wiki/*.md`, grep its `[[wikilinks]]` to find which source files are already referenced.
- The orphans = source files NOT referenced by any existing wiki page.

Record the full orphan list — it becomes the "综合了以下源页面" footer.

### 3. Read ALL source files completely

Do not skim. Read every orphan source file in full (`read_file`; if it reports `is_binary:true` or `total_lines:0` for a `.md` that `wc -l` says has content, fall back to `terminal` `cat` — see Pitfalls). You cannot synthesize what you haven't read.

For each file, note: title, date, topic, key facts/numbers, cross-references to sibling files, and which other wiki pages (if any) already cite it.

### 4. Read existing wiki pages for cross-link targets and dedup

Before writing, read every existing `30-wiki/*.md` that might overlap with the new page's topic. Goal: know what's already synthesized so you can cross-link instead of repeat.

For each overlapping wiki page, record: which sections cover which subtopics, which source files it cites. This determines the **division of labor** (see step 6).

### 5. Structure by topic dimension, NOT by source file

This is the core of synthesis. The page must be organized by **theme/subtopic**, not by "source file A's content, then source file B's content". Multiple source files contributing to the same subtopic are merged into one section with per-fact `→ [[source]]` pointers.

Bad structure (per-file摘抄):
```
## vasp-universal-tool-manual.md 的内容
## known-errors.md 的内容
## stage-0-handoff.md 的内容
```

Good structure (topic-dimensional):
```
## 1. 工具包概览
## 2. 核心功能与子包设计
## 3. VASP 通用工具集
## 4. 工作流与自动化
## 5. 文档工程演进
## 6. 踩坑
```

Typical topic dimensions for a software-tool-package wiki page: 概览/核心功能/工作流/文档与演进/踩坑. For a science-topic page: 理论/方法/实践/踩坑. Adapt to the source material.

### 6. Dedup via cross-link, not repetition

When a subtopic is already covered in another `30-wiki/` page, **do not repeat it**. Instead:

1. Declare the division of labor in the opening `> blockquote`: "与 [[other-wiki-page]] 的分工：[[other-wiki-page]] 专注 X；本页专注 Y。凡 [[other-wiki-page]] 已综合的条目均交叉引用而非重复。"
2. In the relevant section, write "见 [[other-wiki-page]] 第N节" and move on.
3. In the footer, if a source file was already cited by another wiki page as "未采纳候选", note that and explain why your page also does (or does not) adopt it.

Example from `30-wiki/pjvasp-package.md`: `known-errors.md` and `lattice-mismatch.md` were already listed as "未采纳候选" in `30-wiki/vasp.md`'s footer. The new page references them lightly (§1.2 context, §6 pitfalls) but does not re-summarize, and explicitly cites vasp.md's exclusion reasoning.

### 7. Write the page

Frontmatter (vault-original, per SCHEMA.md §1):
```yaml
---
title: "<Chinese descriptive title>"
date: <YYYY-MM-DD>
tags: [<slug>, wiki, <topic-tags>, synthesis]
source_repo: native
imported: <YYYY-MM-DD>
---
```

Filename: kebab-case, lowercase, no Chinese, no spaces (SCHEMA.md §2). E.g. `pjvasp-package.md`, not `PjvaspPackage.md` or `pjvasp_package.md`.

Body structure:
1. Opening `> blockquote`: what this page synthesizes, how many source files, the topic dimensions used, and the division of labor with overlapping wiki pages.
2. Numbered H2 sections by topic dimension. Each fact/conclusion cites its source via `→ [[source-file-name]]` (stem only, no `.md`).
3. A "踩坑" (pitfalls) section aggregating errors/workarounds from all sources, each as a numbered item with conclusion + source pointer.
4. Footer: "综合了以下源页面" list (every source file as `[[]]` link + path), then "交叉引用" (other wiki pages), then "未采纳的候选及排除理由" (source files you judged not to include, with reason).

**Inference rule** (AGENTS.md §1): the creation layer allows inference, but inferences must be labeled. Write "（推断：...）" or "合理推断" / "建议" — do not present inference as sourced fact.

### 8. Verify links AND data fidelity

**8a. Link check** — run the vault's link checker:
```bash
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python _scripts/check_links.py
```

- **Image-link check must be 0 missing** (exit code 0). The script exits non-zero on missing images.
- **Doc-link check** reports unresolved `[[wikilink]]`s but does NOT fail the script (some legitimately point at not-yet-imported content). Compare the unresolved list **before and after** your edit — your new page should add **0 new unresolved** entries.

To verify your page specifically (independent of the global check), run a Python snippet that:
1. Reads your page, strips ``` fences and `` `inline code` `` (so sample text isn't treated as links).
2. Builds a name index of all vault files (stem, lowercased).
3. Checks every `[[]]` and `![[]]` in your page resolves.

See `references/wiki-synthesis-verification.md` for the ready-to-run snippet.

**8b. Data-fidelity check (when the page transcribes a source table)** — if your wiki page contains a summary table whose numbers are transcribed from a source file's table (e.g. a subpackage coverage map, a benchmark result table, a stage-status table), you MUST mechanically re-verify every cell against the source, not eyeball it. Transcription errors are the #1 data-accuracy failure mode in synthesis pages and are invisible to link checkers. See `references/wiki-table-fidelity-check.md` for the ready-to-run snippet that diffs a wiki markdown table against its source markdown table column-by-column.

The check is mandatory whenever the wiki table's column header is **renamed or reinterpreted** vs. the source (e.g. source column "函数数" relabeled as "公开 API 数" in the wiki). Renaming a column without re-deriving every row's value from the source is how half a table silently goes wrong while the other half coincidentally matches.

### 9. Report

Report to the user: new file path, byte size, number of source files synthesized, `check_links.py` result (image missing count, doc-link unresolved count, exit code, and confirmation that your page added 0 new unresolved).

## Pitfalls

- **`read_file` reports valid UTF-8 `.md` as binary / 0 lines**: some files (long lines, certain encodings, mixed CRLF/LF) trigger `is_binary:true` or `total_lines:0` despite having content. Cross-check with `terminal` `wc -l <path>`; if it disagrees, read via `terminal` `cat <path>` or `execute_code` with `open(path, encoding="utf-8")`. **Do not treat a 0-line/binary report as "empty file" without a `wc -l` cross-check** — you will silently skip source material. This pitfall also appears in `vault-integration`; it applies equally here.
- **Per-file structure instead of topic-dimensional**: the most common synthesis failure. If your H2 headings are source filenames, you're summarizing, not synthesizing. Reorganize by subtopic; merge multiple sources into each section.
- **Repeating content already in another wiki page**: violates the vault's dedup principle. Always check existing `30-wiki/*.md` first; cross-link with "见 [[X]] 第Y节" instead of repeating.
- **Forgetting the source-page footer**: SCHEMA.md §5 makes it mandatory for `30-wiki/` pages. Every page must end with "综合了以下源页面" listing every source file as a `[[]]` link + its path.
- **Forgetting "未采纳的候选及排除理由"**: if you judged a source file not worth including, say so explicitly with a reason. This is the provenance trail for "why isn't X in this page".
- **Modifying source files in 10-sources/ or 20-projects/**: AGENTS.md §1 forbids this. The creation layer writes only to `30-wiki/`. Source files are read-only raw material.
- **Presenting inference as fact**: the creation layer allows inference, but it must be labeled ("推断"/"合理推断"/"建议"). Sourced facts get `→ [[source]]`; inferences get an explicit marker.
- **`check_links.py` exit code vs unresolved doc-links**: the script exits non-zero ONLY on missing images, not on unresolved `[[wikilink]]`s. A clean exit (0) with 16 unresolved doc-links is normal if those are pre-existing `00-inbox/` links unrelated to your page. Always diff the unresolved list before/after your edit.
- **Transcribed tables silently wrong when a column is renamed/reinterpreted**: if your wiki page has a summary table whose numbers come from a source file's table, and you rename or reinterpret a column (e.g. source "函数数" → wiki "公开 API 数"), you MUST mechanically re-derive every row's value from the source — do not copy the source column's numbers under the new label and assume they mean the same thing. A renamed column whose values were not re-derived will have some rows that coincidentally match the new concept and some that don't, making the error invisible to eyeballing. Worse, if the same page also states the correct number in prose (e.g. a bullet says "slurm … 13 个函数" while the table says 7), the page self-contradicts. Always run the table-fidelity snippet (`references/wiki-table-fidelity-check.md`) before reporting done. This is the #1 failure mode the link checker cannot catch.

## Support files

- `references/wiki-synthesis-verification.md` — ready-to-run Python snippet for verifying a single wiki page's `[[]]` and `![[]]` links resolve against the vault name index (strips code fences/inline code first). Use when you want to confirm your new page specifically adds 0 unresolved links, independent of the global `check_links.py` run.
- `references/wiki-page-structure-template.md` — annotated skeleton of a `30-wiki/` synthesis page (frontmatter, opening blockquote with division-of-labor declaration, topic-dimensional H2 sections, pitfalls section, source-page footer, excluded-candidates footer). Extracted from the proven `vasp.md` / `tools.md` / `pjvasp-package.md` pages.
- `references/wiki-table-fidelity-check.md` — ready-to-run Python snippet that diffs a wiki page's markdown table against its source file's markdown table, column-by-column, to catch transcription errors (especially when a column header was renamed/reinterpreted). Use whenever the wiki page transcribes a source table's numbers.
