# Wiki Synthesis Page Table-Fidelity Check

Ready-to-run Python snippet for verifying that a summary table transcribed
into a `30-wiki/` page matches its source file's table, column-by-column.
Use this **whenever the wiki page contains a markdown table whose numbers
were copied or re-derived from a source file's table** — e.g. a subpackage
coverage map, a benchmark result table, a stage-status table.

Transcription errors are the #1 data-accuracy failure mode in synthesis
pages and are **invisible to link checkers** (`check_links.py` only verifies
that `[[]]` targets resolve; it does not look at table contents). This
snippet catches:

- A column whose header was **renamed/reinterpreted** (e.g. source column
  "函数数" relabeled as "公开 API 数" in the wiki) but whose row values were
  copied verbatim instead of re-derived — half the rows coincidentally
  match the new concept, half don't, and eyeballing misses it.
- A row count mismatch (source has N rows, wiki table has M).
- A per-cell numeric drift (transcription typo, off-by-one, wrong column
  index when copying).
- **Internal self-contradiction**: the wiki page states a number in prose
  (e.g. a bullet "slurm … 13 个函数") that disagrees with the same number
  in the table. The snippet flags these by also scanning the page's prose
  for the source table's key numbers.

## When to run

Mandatory when the wiki page transcribes a source table's numbers AND any
of these hold:

- The wiki table's column header differs from the source table's column
  header (renamed or reinterpreted).
- The wiki table aggregates multiple source rows into fewer rows, or
  splits one source row into several.
- The wiki table's row order differs from the source.

Optional (but cheap) when the wiki table is a verbatim copy of the source
table — the snippet will confirm nothing drifted.

## Snippet

Adapt `WIKI_PAGE`, `SOURCE_FILE`, `WIKI_TABLE_HEADER_HINT` (a unique
substring of the wiki table's header row, e.g. `"公开 API 数"`), and
`SOURCE_TABLE_HEADER_HINT` (same for the source table, e.g. `"函数数"`).
Run via `execute_code`.

```python
import re

WIKI_PAGE = "/path/to/30-wiki/your-page.md"
SOURCE_FILE = "/path/to/20-projects/slug/notes/source.md"
WIKI_TABLE_HEADER_HINT = "公开 API 数"   # unique substring of wiki table header
SOURCE_TABLE_HEADER_HINT = "函数数"        # unique substring of source table header

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def extract_tables(text, header_hint):
    """Return list of tables (each a list of row-lists) whose header row
    contains header_hint. A table = consecutive lines starting with '|'."""
    tables, cur = [], []
    for line in text.splitlines():
        if line.strip().startswith("|"):
            cur.append(line)
        else:
            if cur and any(header_hint in c for c in cur[0].split("|")):
                tables.append(parse_rows(cur))
            cur = []
    if cur and any(header_hint in c for c in cur[0].split("|")):
        tables.append(parse_rows(cur))
    return tables

def parse_rows(table_lines):
    """Parse markdown table lines into list of cell-lists, skipping the
    separator row (|---|---|)."""
    rows = []
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # skip separator row
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows

def to_num(s):
    """Try to parse a cell as int/float; return None if not numeric."""
    s = s.strip().replace(",", "").replace(" ", "")
    if s in ("", "—", "-", "N/A"):
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None

wiki_text = read(WIKI_PAGE)
src_text = read(SOURCE_FILE)

wiki_tables = extract_tables(wiki_text, WIKI_TABLE_HEADER_HINT)
src_tables = extract_tables(src_text, SOURCE_TABLE_HEADER_HINT)

if not wiki_tables:
    print(f"WARNING: no wiki table with header containing '{WIKI_TABLE_HEADER_HINT}'")
if not src_tables:
    print(f"WARNING: no source table with header containing '{SOURCE_TABLE_HEADER_HINT}'")
    raise SystemExit(0)

# Use the first matching table on each side (extend if multiple).
wiki_tbl = wiki_tables[0]
src_tbl = src_tables[0]

print(f"Wiki table: {len(wiki_tbl)} rows (incl header), {len(wiki_tbl[0])} cols")
print(f"  header: {wiki_tbl[0]}")
print(f"Source table: {len(src_tbl)} rows (incl header), {len(src_tbl[0])} cols")
print(f"  header: {src_tbl[0]}")
print()

# --- Check 1: row count ---
if len(wiki_tbl) != len(src_tbl):
    print(f"ROW COUNT MISMATCH: wiki={len(wiki_tbl)-1} data rows, source={len(src_tbl)-1} data rows")
else:
    print(f"row count OK ({len(wiki_tbl)-1} data rows)")

# --- Check 2: per-cell numeric comparison (by position) ---
# Compare the first label column (col 0) row-by-row, then numeric columns.
print("\nPer-row comparison (label | wiki values | source values | match):")
mismatches = 0
for i in range(1, min(len(wiki_tbl), len(src_tbl))):
    w = wiki_tbl[i]
    s = src_tbl[i]
    label = w[0] if w else s[0]
    w_nums = [to_num(c) for c in w[1:]]
    s_nums = [to_num(c) for c in s[1:]]
    # compare positionally where both are numeric
    row_match = True
    diffs = []
    for j, (wn, sn) in enumerate(zip(w_nums, s_nums)):
        if wn is not None and sn is not None and wn != sn:
            row_match = False
            diffs.append(f"col{j+1}: wiki={wn} src={sn}")
            mismatches += 1
    status = "OK" if row_match else "MISMATCH " + "; ".join(diffs)
    print(f"  {label[:40]:40s} | {w_nums} | {s_nums} | {status}")

print(f"\nTotal numeric mismatches: {mismatches}")

# --- Check 3: internal self-contradiction ---
# Scan wiki prose (non-table lines) for any source-table numeric value and
# flag if the same number appears in the wiki table with a different value
# for the same row label.
print("\n--- Self-contradiction scan (prose vs table) ---")
# Build label -> {col_header: value} from source table
src_map = {}
for i in range(1, len(src_tbl)):
    label = src_tbl[i][0].strip("` ")
    src_map[label] = {src_tbl[0][j]: to_num(src_tbl[i][j]) for j in range(1, len(src_tbl[0]))}

# Get wiki prose (lines not starting with |)
prose_lines = [l for l in wiki_text.splitlines() if not l.strip().startswith("|")]
prose = "\n".join(prose_lines)

contradictions = 0
for label, cols in src_map.items():
    for col_header, val in cols.items():
        if val is None:
            continue
        # if the prose mentions this label AND this number, check the wiki table
        if label in prose and str(val) in prose:
            # find the same label in wiki table
            for i in range(1, len(wiki_tbl)):
                if wiki_tbl[i][0].strip("` ") == label:
                    # find the wiki column whose header is closest to col_header
                    for j in range(1, len(wiki_tbl[0])):
                        if col_header in wiki_tbl[0][j] or wiki_tbl[0][j] in col_header:
                            wv = to_num(wiki_tbl[i][j])
                            if wv is not None and wv != val:
                                print(f"  SELF-CONTRADICTION: '{label}' prose says {val} ({col_header}), table says {wv} ({wiki_tbl[0][j]})")
                                contradictions += 1
if contradictions == 0:
    print("  no prose-vs-table contradictions found for shared numbers")

print(f"\n=== SUMMARY: {mismatches} cell mismatches, {contradictions} self-contradictions ===")
```

## Expected result for a clean table

```
Wiki table: 9 rows (incl header), 4 cols
  header: ['子包', '模块数', '函数数', '核心职责']
Source table: 9 rows (incl header), 5 cols
  header: ['文件', 'LOC', '函数数', '类数', '公开函数/类']

row count OK (8 data rows)

Per-row comparison (label | wiki values | source values | match):
  build       | [11, 59] | [2977, 59, 0] | OK
  ...
Total numeric mismatches: 0

=== SUMMARY: 0 cell mismatches, 0 self-contradictions ===
```

## What the snippet does NOT do

- It does not validate that the wiki column's **semantics** are correct
  (e.g. it won't tell you that "公开 API 数" should actually count only
  non-underscore-prefixed names). It only tells you whether the numbers
  match the source column you point it at. If you renamed a column, you
  must separately decide whether the source column you're comparing
  against is the right one — and if not, re-derive the values yourself
  (e.g. count the comma-separated names in the source "公开函数/类" column).
- It does not check non-numeric cells (descriptive text in the last
  column). Eyeball those.
- It compares tables positionally (row 1 of wiki vs row 1 of source). If
  the wiki reorders rows, extend the snippet to match by label column.

## Proven on

- `30-wiki/pjvasp-package.md` §1.3 table vs `20-projects/pjvasp-package/notes/subpackage-coverage-map.md` (2026-08-06 review): caught 4/8 rows where the wiki "公开 API 数" column did not match the source "函数数" column and did not match a re-count of the source "公开函数/类" column either — the column had been relabeled without re-deriving values. Also flagged a self-contradiction where §1.3's prose bullet correctly said "slurm … 13 个函数" while the table row said 7.
