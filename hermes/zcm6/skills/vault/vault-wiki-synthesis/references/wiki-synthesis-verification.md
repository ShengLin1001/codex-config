# Wiki Synthesis Page Link Verification

Ready-to-run Python snippet for verifying that a single `30-wiki/` page's
`[[wikilinks]]` and `![[embeds]]` all resolve against the vault file index.
Use this when you want to confirm your new/edited page specifically adds
**0 new unresolved links**, independent of the global `check_links.py` run
(which reports unresolved links across the entire vault, making it hard to
tell if *your* page is the source of any new unresolved entry).

This mirrors the logic in the vault's own `_scripts/check_links.py` but
scopes the output to one page. Key behaviours shared with that script:

- Strips ``` fenced code blocks and `` `inline code` `` before scanning, so
  sample text shown as illustration isn't treated as real links.
- Builds a name index from **all** vault files (not just `.md`), lowercased
  by stem — Obsidian wikilinks can target any file type (e.g. `.ahk`).
- Embed links (`![[...]]`) are resolved as vault-relative file paths.
- Doc links (`[[...]]` without leading `!`) are resolved by stem lookup.

## Snippet

Adapt `PAGE` and `VAULT` to your session. Run via `execute_code` or save as
a script under `_scripts/` and run with `python`.

```python
import os, re

VAULT = os.path.expanduser("~/mysoft/pei/myobsidian")  # or session WORKSPACE PATH
PAGE = os.path.join(VAULT, "30-wiki/<your-page>.md")

EXCLUDE_DIRS = {".git", ".obsidian", "_import", "_scripts", "90-archive", "ai-guide"}

with open(PAGE, encoding="utf-8") as f:
    text = f.read()

# Strip code fences and inline code so sample text isn't treated as links.
lines = text.split("\n")
in_fence = False
out = []
for line in lines:
    if line.strip().startswith("```"):
        in_fence = not in_fence
        out.append("")
        continue
    out.append("" if in_fence else line)
clean = "\n".join(out)
clean = re.sub(r"`[^`\n]*`", "", clean)

# Build name index (stem, lowercased) -> path, over ALL vault files.
name_index = {}
for root, dirs, files in os.walk(VAULT):
    rel = os.path.relpath(root, VAULT)
    top = rel.split(os.sep)[0]
    if top in EXCLUDE_DIRS:
        dirs[:] = []
        continue
    for fn in files:
        stem = os.path.splitext(fn)[0].lower()
        name_index.setdefault(stem, os.path.join(root, fn))

EMBED_RE = re.compile(r'!\[\[([^|\]#]+)')
WIKILINK_RE = re.compile(r'(?<!!)\[\[([^|\]#]+)')

# Collect unique links.
my_links = set()
for m in WIKILINK_RE.finditer(clean):
    my_links.add(m.group(1).strip())

# Check embeds as file paths.
missing_images = []
for m in EMBED_RE.finditer(clean):
    t = m.group(1).strip()
    full = os.path.join(VAULT, t.replace("/", os.sep))
    if not os.path.isfile(full):
        missing_images.append(t)

# Check doc links by stem lookup.
unresolved = []
for target in sorted(my_links):
    if target.startswith(("http://", "https://")):
        continue
    key = os.path.splitext(target)[0].split("/")[-1].lower()
    if key not in name_index:
        unresolved.append(target)

print(f"Page: {os.path.relpath(PAGE, VAULT)}")
print(f"Unique wikilinks: {len(my_links)}")
print(f"Missing images: {len(missing_images)}")
for m in missing_images:
    print(f"  MISSING IMAGE: {m}")
print(f"Unresolved doc-links: {len(unresolved)}")
for u in unresolved:
    print(f"  unresolved: [[{u}]]")
```

## Expected result for a clean page

```
Page: 30-wiki/pjvasp-package.md
Unique wikilinks: 28
Missing images: 0
Unresolved doc-links: 0
```

If `Unresolved doc-links` is non-zero, either fix the link target (typo,
wrong stem) or, if the target is a file that genuinely doesn't exist yet
(e.g. a not-yet-imported source), note it explicitly in the page footer.
Missing images are a hard failure — `check_links.py` exits non-zero on
those.

## Proven on

- `30-wiki/pjvasp-package.md` (2026-08-06): 28 unique wikilinks, 0 missing
  images, 0 unresolved doc-links. Global `check_links.py` reported the same
  16 pre-existing `00-inbox/` unresolved links as the baseline (no new
  entries from the new page).
