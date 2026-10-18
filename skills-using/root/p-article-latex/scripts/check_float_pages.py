#!/usr/bin/env python3
"""Report, for each float, its page vs the page of its first in-text \\ref.

Usage: python check_float_pages.py <path/to/manuscript.tex>
A copy with \\ref logging is compiled (3 pdflatex passes) from the tex's own
directory, so \\graphicspath and figure paths resolve, into a temp directory;
the latex/ directory stays clean.  Figures on or after the page of
\\label{sec:conclusion} are flagged.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PATH_OUT = Path(tempfile.gettempdir()) / "check_float_pages"
PASS_COUNT = 3

# \thepage inside \protected@write is expanded at shipout, i.e. the page the
# citing line actually lands on.  Refs inside captions are logged too, but they
# only point back to earlier figures, so they never change a "first citation".
LOG_REF = r"""
\makeatletter
\newcommand\refpage[2]{}% read back from the .aux, a no-op for LaTeX
\newcommand\declat[2]{}
\newcommand\logdecl[1]{\protected@write\@auxout{}{\string\declat{#1}{\thepage}}}
\NewCommandCopy\origref\ref% \let would copy only the robust wrapper of \ref
\DeclareRobustCommand\ref[1]{\origref{#1}\protected@write\@auxout{}{\string\refpage{#1}{\thepage}}}
\makeatother
"""


def fail(msg):
    print("❌ ERROR: " + msg)
    raise SystemExit(1)


def generate_variant(path_tex):
    text = path_tex.read_text(encoding="utf-8")
    if "\\begin{document}" not in text:
        fail("no \\begin{document} in " + str(path_tex))
    PATH_OUT.mkdir(exist_ok=True)
    path_variant = PATH_OUT / "check.tex"
    text = text.replace("\\begin{document}", LOG_REF + "\\begin{document}", 1)
    # log the page each float is declared on: the label sits in its caption
    for m in reversed(list(re.finditer(r"\\begin\{(figure\*?|table\*?)\}(?:(?!\\end\{\1\}).)*?\\label\{([^}]+)\}", text, re.S))):
        text = text[:m.start()] + "\\logdecl{" + m.group(2) + "}" + text[m.start():]
    path_variant.write_text(text, encoding="utf-8", newline="\n")
    return path_variant


def run_latex(path_variant, path_cwd):
    for npass in range(1, PASS_COUNT + 1):
        result = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                                 "-output-directory=" + str(PATH_OUT), str(path_variant)],
                                cwd=path_cwd, capture_output=True, text=True, errors="replace")
        if result.returncode != 0:
            fail("pdflatex pass " + str(npass) + " failed, see " + str(PATH_OUT / "check.log"))


def get_pages(path_aux):
    text = path_aux.read_text(encoding="utf-8", errors="replace")
    dict_label = {m.group(1): int(m.group(2)) for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}", text)}
    dict_first = {}
    for m in re.finditer(r"\\refpage\{([^}]+)\}\{(\d+)\}", text):
        dict_first[m.group(1)] = min(dict_first.get(m.group(1), 999), int(m.group(2)))
    dict_decl = {m.group(1): int(m.group(2)) for m in re.finditer(r"\\declat\{([^}]+)\}\{(\d+)\}", text)}
    return dict_label, dict_first, dict_decl


if len(sys.argv) != 2:
    fail("usage: python check_float_pages.py <path/to/manuscript.tex>")
path_tex = Path(sys.argv[1]).resolve()
path_variant = generate_variant(path_tex)
run_latex(path_variant, path_tex.parent)
dict_label, dict_first, dict_decl = get_pages(PATH_OUT / "check.aux")
page_concl = dict_label.get("sec:conclusion", 0)
if page_concl == 0:
    print("⚠️  no \\label{sec:conclusion}: the Conclusion check is skipped")
print("================ 📊 float page vs first citation (Conclusion starts p" + str(page_concl) + ")")
print("📍 sections: " + ", ".join(k.split(":")[1] + " p" + str(v) for k, v in dict_label.items() if k.startswith("sec:")))
lfig = sorted((k for k in dict_label if k.startswith(("fig:", "tab:"))), key=lambda k: (k[:3], int(k.split(":")[1])))
nsame, nbad = 0, 0
for label in lfig:
    page_float, page_cite = dict_label[label], dict_first.get(label, 0)
    mark = "✅" if page_float == page_cite else ("⚠️ " if abs(page_float - page_cite) == 1 else "❌")
    nsame += page_float == page_cite
    in_concl = label.startswith("fig:") and 0 < page_concl <= page_float
    nbad += abs(page_float - page_cite) > 1 or in_concl
    print(mark + " " + label + ": float p" + str(page_float) + ", first cited p" + str(page_cite)
          + ", declared p" + str(dict_decl.get(label, 0)) + ("  ❌ on/after Conclusion page" if in_concl else ""))
print("same page: " + str(nsame) + "/" + str(len(lfig)) + ", violations: " + str(nbad))
raise SystemExit(1 if nbad else 0)
