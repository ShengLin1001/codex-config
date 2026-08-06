# 30-wiki Synthesis & Coverage Audit Workflow

Reproduce-able technique for (1) finding which source files are NOT yet synthesized into any wiki page, (2) filtering out process documents that don't belong in wiki, and (3) verifying data tables transcribed by work subagents. Proven on the 2026-08-06 wiki expansion (pjvasp-package.md + academic-writing.md).

## Phase 1: Coverage audit script

Run via `execute_code`. Collects all source markdown stems, regex-extracts wikilinks from each wiki page, reports orphans grouped by directory.

```python
import os, re, glob
from collections import defaultdict

VAULT = "/public3/home/scg6928/mysoft/pei/myobsidian"

# 1. Collect source stems (exclude project-management files)
sources = {}
EXCLUDE = {"LOG.md", "PLAN.md", "PROJECT-MAP.md"}
for d in ["10-sources", "20-projects"]:
    for p in glob.glob(f"{VAULT}/{d}/**/*.md", recursive=True):
        if os.path.basename(p) in EXCLUDE:
            continue
        stem = os.path.splitext(os.path.basename(p))[0]
        sources[stem] = p

# 2. For each wiki page, find which source stems it references
wiki_files = sorted(glob.glob(f"{VAULT}/30-wiki/*.md"))
all_referenced = {}  # stem -> [wiki pages]
for wf in wiki_files:
    with open(wf, encoding="utf-8") as f:
        content = f.read()
    # (?<!\!) excludes image embeds ![[...]]; strip #heading and |alias suffixes
    links = re.findall(r'(?<!\!)\[\[([^\]#|]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]', content)
    refs = set()
    for l in links:
        stem = l.strip().split("/")[-1]  # strip path prefix
        if stem in sources:
            refs.add(stem)
    for r in refs:
        all_referenced.setdefault(r, []).append(os.path.basename(wf))

# 3. Orphans = sources not referenced by any wiki
orphans = {s: p for s, p in sources.items() if s not in all_referenced}
print(f"Total source md: {len(sources)} | Orphans: {len(orphans)}")

by_dir = defaultdict(list)
for s, p in sorted(orphans.items()):
    rel = p.replace(VAULT + "/", "")
    parts = rel.split("/")
    top = "/".join(parts[:2])
    by_dir[top].append(rel)
for d, files in sorted(by_dir.items()):
    print(f"\n  [{d}] ({len(files)})")
    for f in files:
        print(f"    {f}")
```

## Phase 2: Process-document filter rules

Orphans that look like knowledge gaps but are actually process documents — do NOT make wiki pages for these:

| Pattern | Why excluded |
|---|---|
| `prb-20260721-polishing-decisions-*` (r2, r3, r4, r5, r6, r7) | Revision decision logs — "how we got here", not "what is true" |
| `prb-transfer-*` (handoffs, prompts, rewrites, tracked) | Manuscript-transfer process docs |
| `stage-*-handoff.md` | Already summarized in stage-status / the wiki covers the stable knowledge |
| `manuscript-*-self-check*`, `*-evaluation-*`, `*-cover-letter*` | Submission process records |
| `codex-ppt-*`, `workbuddy-*`, `topic-research-prompt.md` | Presentation instructions, one-off |
| `*-codex.md` / `*-claude.md` paired with a non-suffixed twin | The twin is canonical; the suffixed one is an AI-generated variant |
| `assessment-09-cover-letter-strategy`, `assessment-10-search-queries` | Process artifacts of a literature assessment |

Rule of thumb: **process docs are "how we got here", knowledge docs are "what is true"**. Only the latter belongs in 30-wiki.

## Phase 3: Table-cell verification (mandatory after delegated synthesis)

A work subagent transcribing a multi-row data table from a source file will silently transpose, mislabel, or invent numbers. Eyeballing does NOT catch this. Programmatic cell-by-cell comparison is mandatory.

### The bug that was caught (2026-08-06)

Work subagent wrote a subpackage-coverage table in `30-wiki/pjvasp-package.md` with a "公开 API 数" column. Source file `20-projects/pjvasp-package/notes/subpackage-coverage-map.md` has a "函数数" column. The subagent conflated the labels and got 4 of 8 rows wrong:

| subpackage | source 函数数 | wiki wrote | match |
|---|---|---|---|
| build | 59 | 53 | ✗ |
| calculate | 60 | 60 | ✓ |
| io | 14 | 14 | ✓ |
| post | 105 | 105 | ✓ |
| universal | 120 | 76 | ✗ |
| ml | 29 | 18 | ✗ |
| slurm | 13 | 7 | ✗ |
| cr | 17 | 17 | ✓ |

### Verification snippet

```python
import re

# Read source table
with open('<source>.md', encoding='utf-8') as f:
    src = f.read()
# Parse rows: | `name` | num1 | num2 | num3 | names |
src_rows = {}
for m in re.finditer(r'^\| `(\w+)` \| (\d+) \| (\d+) \| (\d+) \| (.*) \|$', src, re.MULTILINE):
    src_rows[m.group(1)] = {'loc': int(m.group(2)), 'func': int(m.group(3)), 'cls': int(m.group(4))}

# Read wiki table the same way
with open('<wiki>.md', encoding='utf-8') as f:
    wiki = f.read()
wiki_rows = {}
for m in re.finditer(r'^\| `(\w+)` \| (\d+) \| (\d+) \| (.+) \|$', wiki, re.MULTILINE):
    wiki_rows[m.group(1)] = {'modules': int(m.group(2)), 'func': int(m.group(3))}

# Compare
for name, s in src_rows.items():
    w = wiki_rows.get(name, {})
    func_ok = w.get('func') == s['func']
    print(f"{name:<12} src_func={s['func']:<6} wiki_func={w.get('func','?'):<6} {'✓' if func_ok else '✗ MISMATCH'}")
```

If mismatches: fix via `patch` with explicit old/new cell values, then re-run to confirm 0 mismatches. Do NOT re-dispatch a work subagent for a small table fix — that wastes a round-trip; the orchestrator patches directly.

## Delegation brief template (for work subagents)

Each work subagent gets this shape of brief:

- **Goal**: create `30-wiki/<topic>.md` synthesizing N source files from `<path>`.
- **Must read first**: AGENTS.md (write tiers), SCHEMA.md (frontmatter/link/naming), `30-wiki/vasp.md` (template), the source files.
- **Cross-reference constraint**: list existing wiki pages that cover adjacent topics; new page must do `见 [[existing]] 第X节` not copy.
- **Frontmatter**: `source_repo: native`, date, tags, imported.
- **Structure**: topic dimensions (4-6 sections), NOT source-by-source. Dedup across sources. `[[source-stem]]` links back for detail.
- **End matter**: "综合了以下源页面" list + "未采纳的候选及排除理由".
- **No fabrication**: if inferring, mark it. Don't invent content not in sources.
- **Verify**: run `PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python _scripts/check_links.py`; report 0 new unresolved links.
- **Report back**: file path, byte size, source count, check_links result.

## Review subagent brief additions

Beyond the standard checks (structure, dedup, links, source list, frontmatter, no-fabrication), add:

- **Table-cell verification**: if the wiki page contains a data table transcribed from a source file, programmatically compare every numeric cell against the source. Print a mismatch table. This is the check that catches the silent transcription errors described above.
- **Coverage spot-check**: pick 2-3 specific claims in the wiki, trace each back to the source file, confirm the source actually says that.

## Commit at key nodes (unmanned/yolo)

For unmanned sessions, commit via the `p-git-commit` skill. The orchestrator should:
1. Confirm repo boundary (`git rev-parse --show-toplevel`).
2. Stage explicit file whitelist (the new wiki pages + any HANDOFF/log updates).
3. `git diff --cached --check` must pass.
4. Commit with `docs(wiki): :memo: <中文标题>` convention.
5. `git pull --ff-only` then `git push`. If pull diverges, stop and report — do not auto-merge.
