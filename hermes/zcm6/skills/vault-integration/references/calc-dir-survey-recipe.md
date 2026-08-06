# Calculation Directory Survey Recipe

Ready-to-run snippets for surveying large VASP/DFT calculation directories (100k+ files).
All patterns proven on the au_dft project (403k files, 6 top-level dirs).

## 1. Directory tree (understand structure first)

```bash
cd <root>
find . -maxdepth 2 -type d | sort
```

If deeper structure needed, go level-by-level to avoid timeouts:

```bash
for d in convergence electronic_structure strain substrate reproduce thick; do
  echo "=== $d ==="
  find "$d" -maxdepth 2 -type d | sort
done
```

## 2. Filter to key files only (skip raw VASP output)

```bash
# Find INCAR, KPOINTS, POSCAR, README, scripts, notebooks, shell scripts
# Exclude all VASP binary/large output files
timeout 90 find . -path ./.git -prune -o -type f \
  \( -name "INCAR" -o -name "KPOINTS" -o -name "POSCAR" \
     -o -name "README*" -o -name "*.py" -o -name "*.ipynb" \
     -o -name "*.sh" -o -name "*.md" -o -name "*.txt" \) \
  -print 2>/dev/null | sort > /tmp/keyfiles.txt
wc -l /tmp/keyfiles.txt
```

If still >10k results (parameter-sweep dirs have one INCAR/KPOINTS/POSCAR per point),
filter to top-level scripts and unique INCARs only:

```bash
# Show only .py, .ipynb, .md, .txt (skip INCAR/KPOINTS/POSCAR per-sweep-point)
grep -E "\.(py|ipynb|md|txt)$" /tmp/keyfiles.txt | grep -vE "/[0-9]{2,}[-/]"
```

## 3. Batch INCAR parameter extraction (Python via execute_code)

Walk each major subdirectory, read the first INCAR found, extract key tags:

```python
import subprocess, os

ROOT = "/path/to/calc/root"
subdirs = [
    "convergence",
    "electronic_structure/bulk",
    "strain/20250511_cineb",
    # ... add all top-level subdirs
]

for sd in subdirs:
    full = os.path.join(ROOT, sd)
    out = subprocess.run(["find", full, "-name", "INCAR", "-type", "f"],
                         capture_output=True, text=True, timeout=30)
    incars = out.stdout.strip().split("\n") if out.stdout.strip() else []
    if incars:
        with open(incars[0], "r", errors="replace") as f:
            content = f.read()
        tags = {}
        for line in content.split("\n"):
            line = line.split("#")[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip()
                if k in ["ENCUT","ISIF","ISMEAR","SIGMA","EDIFF","EDIFFG",
                         "NSW","IBRION","POTIM","ISYM","PREC","GGA","LASPH",
                         "LREAL","ISPIN","KPAR","NCORE","NPAR","LELF","LCHARGE",
                         "LWAVE","LORBIT","ICHARG","ISTART","NELM","ALGO","ADDGRID"]:
                    tags[k] = v
        print(f"\n=== {sd} ===")
        print(f"  (sample: {incars[0].replace(ROOT,'.')})")
        for k,v in tags.items():
            print(f"  {k} = {v}")
    else:
        print(f"\n=== {sd} === NO INCAR FOUND")
```

## 4. Read Jupyter notebook sources (skip outputs/metadata)

```python
import json

# In execute_code:
code = '''
import json
nb = json.load(open("path/to/notebook.ipynb"))
for i, cell in enumerate(nb["cells"][:3]):
    src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
    print(f"\n--- cell {i} ---\n{src}")
'''
# Or via terminal:
# python3 -c "import json; nb=json.load(open('path.ipynb')); [print('\n--- cell',i,'---\n'+''.join(c['source'])) for i,c in enumerate(nb['cells'][:3])]"
```

## 5. NEB-specific parameter extraction

```bash
# Find INCARs that contain NEB tags (IMAGES, LCLIMB, SPRING)
find . -name INCAR -exec grep -l "IMAGES" {} \; 2>/dev/null
# Then read the NEB-relevant tags:
grep -i "IMAGES\|LCLIMB\|SPRING" <neb_incar_file>
```

## 6. File size check (decide what to import vs summarize)

```bash
while read f; do
  sz=$(stat -c%s "$f" 2>/dev/null)
  echo "$sz	$f"
done < /tmp/keyfiles.txt | sort -rn
```

Import rule: scripts <50KB with reusable logic → `scripts/` with provenance header.
Scripts >50KB or project-specific → summarize methodology into `calculation-index.md`.

## 7. Count files per top-level directory (for MANIFEST)

```bash
for d in convergence electronic_structure reproduce strain substrate thick; do
  n=$(find "$d" -type f 2>/dev/null | wc -l)
  echo "$d: $n files"
done
echo "=== Total ==="
find . -type f 2>/dev/null | wc -l
```

## 8. Import scripts with provenance header

```bash
SRC=/path/to/source
DST=/path/to/vault/20-projects/<slug>/scripts

{
  cat << 'HEADER'
#!/usr/bin/env python3
# ---
# title: <descriptive title>
# date: <original date>
# tags: [<slug>, <topic>]
# source_repo: other/<slug>
# imported: <YYYY-MM-DD>
# ---

# 源路径: <relative/source/path.py>
# 用途: <one-line description>

HEADER
  cat "$SRC/<relative/path/script.py>"
} > "$DST/<kebab-case-name>.py"
```
