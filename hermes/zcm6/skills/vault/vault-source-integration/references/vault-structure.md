# Vault Structure and AGENTS.md Rules

## Vault root

```
/public3/home/scg6928/mysoft/pei/myobsidian/
```

## Directory layout

```
vault/
├── _import/
│   └── MANIFEST.csv          ← Import registry (ALL imports across ALL projects)
├── 00-inbox/                  ← Staging area for unsorted imports
├── 10-sources/               ← General knowledge archive (git, python, tools, theory, etc.)
│   └── <category>/<topic>.md
├── 20-projects/              ← Project-specific knowledge
│   └── <project-slug>/
│       ├── LOG.md            ← Project integration log (update on every import batch)
│       ├── PLAN.md           ← Project plan (optional, may be stub)
│       ├── notes/            ← Project notes (imported .md files go here)
│       └── images/           ← Project images (imported figures go here)
│           └── <subdir>/
├── 30-wiki/                  ← Curated knowledge wiki
├── 90-archive/
│   └── INDEX.md              ← Archive index (register non-imported binary/docx files here)
└── AGENTS.md                 ← Vault governance rules
```

## AGENTS.md key rules (for 10-sources/ and 20-projects/)

1. **Archive layer permissions**: You may transport, classify, format-convert, merge/dedup,
   supplement missing images, and fix format errors.
2. **No fabrication**: You may NOT generate new summaries or infer new conclusions not
   present in the source material.
3. **Provenance required**: Every imported file must have provenance frontmatter with
   `source_repo` and `imported` fields.
4. **File naming**: lowercase, hyphenated.
5. **Image embedding**: Use Obsidian wikilink syntax `![[images/subdir/file.png]]`.
6. **Binary exclusion**: Do NOT copy PDFs, `.pptx`, `.pkl`, `.pyc`, or raw calculation
   data into the vault. `.py` scripts may be imported as knowledge documents.

## Provenance frontmatter template

```yaml
---
title: <Descriptive title in the source language>
date: <Original source file date, YYYY-MM-DD>
tags: [<project-slug>, <topic-category>, <source-batch>]
source_repo: other/<project-name>
imported: <Import date, YYYY-MM-DD>
---
```

### Field conventions

- **title**: Match the source document's H1 or descriptive title. For CJK files, keep
  the original language title.
- **date**: Use the source file's creation or last-modified date, not the import date.
- **tags**: Start with the project slug (e.g. `inplane-strain-general`), then topic
  categories (e.g. `theory`, `modeling`, `manuscript`, `prb-transfer`), then any batch
  identifier.
- **source_repo**: Format is `other/<project-name>`. Check existing MANIFEST entries
  for the same project — prior batches may use a `-<year>` suffix (e.g.
  `other/inplane-strain-general-2026`). Follow the user's explicit instruction when
  they specify a different source_repo string.
- **imported**: The date the file was brought into the vault (today's date).

## MANIFEST.csv format

Located at: `_import/MANIFEST.csv` (vault root)

```csv
source_repo,source_path,disposition,target_path,reason
```

### Disposition values

| Disposition | Meaning |
|---|---|
| `imported` | New file created in vault |
| `already-exists` | Content already in vault, verified identical, no action |
| `merged` | New information merged into an existing vault file |
| `skipped` | Not imported (binary, superseded, out of scope) |
| `archived` | Registered in 90-archive/INDEX.md but not imported |
| `deleted` | Removed (empty stub, duplicate) |

### Reason field

Always include a reason for non-trivial decisions:
- For `already-exists`: cite the existing vault file and MANIFEST line number
- For `skipped`: explain why (binary artifact, superseded by X, tool code, etc.)
- For `merged`: describe what new information was added to which existing file

## LOG.md format

Located at: `20-projects/<project-slug>/LOG.md`

```markdown
# <project-slug> — Log

## YYYY-MM-DD: <integration batch description>

### New files created (N md + M images)

| Source file | Vault target | Content |
|---|---|---|
| `source/path/file.md` | `notes/vault-file-name.md` | Brief content description |

Images imported to `images/<subdir>/`:
- `file1.png`
- `file2.png`

### Files already in vault (verified identical, no action)

- `source-file.md` → already as `notes/existing-vault-file.md`

### Skipped (per AGENTS.md rules)

- `.py` scripts: executable tool code, not vault documentation
- `.pptx` / `__pycache__`: binary artifacts excluded
- `working-revision.md`: superseded by `vault-version.md` already in vault

### MANIFEST

All imports registered in `_import/MANIFEST.csv` (source_repo = `other/<project-name>`).
```

## Common naming conventions observed in this vault

| Convention | Pattern | Example |
|---|---|---|
| Assessment series | `assessment-NN-*.md` | `assessment-00-executive-summary.md` |
| PRB transfer | `prb-transfer-*.md` | `prb-transfer-modeling-hcp-static-vs-relax-mode-zh.md` |
| PRB submission | `prb-YYYYMMDD-*.md` | `prb-20260721-manuscript.md` |
| Manuscript | `manuscript-*-with-media.md` | `manuscript-acta-20260605-with-media.md` |
| Modeling notes | `prb-transfer-modeling-*.md` | `prb-transfer-modeling-task1-analytic-threshold-model.md` |

When importing a new batch, match the convention already used for that project's prior
imports. If no prior convention exists, use `prb-transfer-modeling-<topic>-zh.md` for
Chinese-language modeling notes.
