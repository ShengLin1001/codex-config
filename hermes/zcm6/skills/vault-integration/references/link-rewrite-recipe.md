# Internal-Link Rewrite Recipe (kebab-case rename)

When importing a batch of source Markdown files into the vault, filenames are converted to kebab-case (e.g. `stage0_1_param_scan_analysis.md` → `stage0-1-param-scan-analysis.md`). Files reference each other by their old filenames, so every internal link must be rewritten to the new name. This file gives the working Python recipe.

## Problem

Source files reference siblings in several forms:

1. `oldname.md` — explicit filename in prose / code blocks.
2. `oldname` — bare stem, in wikilinks `[[oldname]]` or in prose ("see oldname").
3. `ai-guide/<subdir>/oldname.md` — cross-subdir path references.
4. `(oldname.md)` — parenthesized.

A naive `str.replace(oldname, newname)` is **wrong** because it matches substrings (e.g. `mode` inside `model`) and corrupts prose.

## Recipe

```python
import re

# Map: old basename (with .md) -> new basename (with .md)
RENAME = {
    "stage0_1_param_scan_analysis.md": "stage0-1-param-scan-analysis.md",
    "fcc_hoec_energy_codex.md":         "fcc-hoec-energy-codex.md",
    # ... all files in the batch
}

def fix_internal_links(body):
    # Pass 1: full filename with .md (handles 'oldname.md', '(oldname.md)', 'sub/oldname.md')
    for old, new in RENAME.items():
        body = body.replace(old, new)
    # Pass 2: bare stem (no .md) — wikilinks [[oldname]] and prose "see oldname"
    #         word-boundary regex avoids matching 'mode' inside 'model'
    for old, new in RENAME.items():
        old_stem = old[:-3]   # strip '.md'
        new_stem = new[:-3]
        pattern = r'(?<![A-Za-z0-9_])' + re.escape(old_stem) + r'(?![A-Za-z0-9_])'
        body = re.sub(pattern, new_stem, body)
    return body
```

### Why two passes

Pass 1 (`str.replace` on `oldname.md`) is safe because the `.md` suffix makes collisions extremely unlikely. Pass 2 (regex on bare stem) is needed for `[[wikilinks]]` and prose, but MUST use word boundaries — otherwise `fcc` would match inside `fcc_hoec`, or `mode` inside `model`.

### Word-boundary choice

`(?<![A-Za-z0-9_])` and `(?![A-Za-z0-9_])` — i.e. not preceded or followed by a word char. This treats `_` as a word char so `fcc_hoec` is a single token and `fcc` alone won't match inside it. Adjust the character class if your filenames contain other delimiters.

### When bare-stem replacement is risky

If a stem is a common English word (e.g. `fcc`, `energy`, `mode`), the regex may still false-match unrelated prose. In that case, restrict Pass 2 to wikilink context only:

```python
# Only rewrite [[oldname]] form, leave prose mentions of 'energy' alone
for old, new in RENAME.items():
    old_stem = old[:-3]; new_stem = new[:-3]
    body = body.replace(f"[[{old_stem}]]", f"[[{new_stem}]]")
    body = body.replace(f"[[{old_stem}.md]]", f"[[{new_stem}.md]]")
```

For this vault's import batch (filenames like `stage0_1_param_scan_analysis`, `fcc_hoec_energy_codex`), the stems are distinctive enough that the word-boundary regex was safe across all files.

## Cross-subdir references

A file in `hoec/` referencing `training/stage0_1_param_scan_analysis.md` is handled by Pass 1 (the `.md` form is unique). No special-casing needed for the path prefix — `str.replace` rewrites `stage0_1_param_scan_analysis.md` wherever it appears in the string.

## Merged-block link rewrite

When merging a source file into an existing vault file, apply the same `fix_internal_links` to the merged block (not to the existing vault file's content — that was already imported and its links already point to vault files).

## Verification

After rewriting, grep the new files for any remaining old names:

```bash
grep -rln "stage0_1_param_scan\|fcc_hoec_energy_codex\|<other_old_names>" notes/<subdirs>/
# empty output = all links rewritten
```

## Common pitfalls

- **Order matters**: run `.md` pass before stem pass. If you run stem pass first, `stage0_1_param_scan_analysis` (stem) gets replaced, then the `.md` pass can't find `stage0_1_param_scan_analysis.md` anymore (the stem was already rewritten) — but actually both passes work regardless of order because Pass 1 operates on `old+'.md'` and Pass 2 on `old` stem. The two-pass design is about precision, not order.
- **Don't forget code blocks**: source files often contain paths in fenced code blocks (```text ... ```) and inline `code`. `str.replace` and `re.sub` rewrite inside code too, which is usually what you want (paths in code are real references). If a code block contains a *literal* old filename that should NOT be renamed (rare), exclude it manually before the rewrite.
- **README / index files**: if a source dir has an `index.md` or `README.md` that lists siblings, it needs the same rewrite. Don't skip it.
