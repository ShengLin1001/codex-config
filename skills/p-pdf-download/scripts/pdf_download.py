#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按 dois_row.txt 逐篇调用 scansci-pdf browser-get 下载官网正文 PDF。

本 skill 先在 literatures/ 下建好目录、写好 dois_row.txt（多篇还有 summary.md），
本脚本只消费、不取名。

Functions:
    fail / warn: 统一错误与告警出口。
    sanitize_name: 把子目录名清洗成 Windows 合法文件名。
    parse_dois: 解析 dois_row.txt → 去重后的 [(doi, 子目录名 or None)]。
    check_dois_file / check_scansci_pdf: 结构性前提校验（文件在、命令在）。
    get_outdir: 按单 / 多篇模式算出每篇的绝对落盘目录。
    download_one: 跑一篇 browser-get 并判定是否真落地 PDF。
    main: 编排 check → prepare → main → summary。

目录约定（目录名与子目录名已由本 skill 写入 dois_row.txt，本脚本只消费）:
    单篇:        literatures/YYMMDD_中文名/
                   dois_row.txt              # 仅 1 行 DOI
                   <DOI>_Official.pdf        # 直接落在此目录
    多篇(调研):  literatures/YYMMDD_investigate_主题/
                   dois_row.txt              # 每行 "DOI<空格>子目录名"
                   summary.md                # 建目录阶段写的调研摘要，本脚本不动
                   子目录名1/<DOI1>_Official.pdf
                   子目录名2/<DOI2>_Official.pdf

dois_row.txt 每行格式:
    单篇:  仅写 DOI（即便写了子目录名也忽略，直接落同级目录）。
    多篇:  DOI<空格>子目录名   （规范写法用空格；本脚本也兼容 TAB / " | "，缺名回退为 DOI 清洗后的目录名）。
    空行与 # 注释行忽略；重复 DOI 自动去重。

模式判定: 有效 DOI 行数 == 1 → 单篇; >= 2 → 多篇。

用法:
    scanscipy                                # 先激活 scansci-pdf venv，使 scansci-pdf 进 PATH
    python pdf_download.py literatures/YYMMDD_xxx/dois_row.txt [--wait 300] [--skip-existing] [--dry-run]
    python pdf_download.py literatures/YYMMDD_xxx          # 传目录亦可，自动找 dois_row.txt
"""

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows 控制台按 UTF-8，避免中文目录名 / 论文元数据乱码（与 CLAUDE.md 约定一致）
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Windows 文件名非法字符；子目录名落盘前必须替换，否则 mkdir 会炸
RE_INVALID = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def fail(msg):
    print("❌ ERROR: " + str(msg))
    raise SystemExit(1)


def warn(msg):
    print("⚠️  " + str(msg))


def sanitize_name(name):
    """把子目录名清洗成 Windows 合法、可落盘的名字。"""
    name = RE_INVALID.sub("_", str(name)).strip().strip(".")
    return name[:120] or "untitled"


def parse_dois(path_file):
    """解析 dois_row.txt → 去重后的 [(doi, 子目录名 or None)]。"""
    lentry = []
    seen = set()
    # utf-8-sig：建目录步骤若用 PowerShell（Out-File / Set-Content -Encoding utf8）写出会带 BOM，
    # 普通 utf-8 读 + strip() 不会去掉 ﻿，会污染第一行 DOI 导致首篇解析失败。
    for line in path_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # DOI 不含空白：空格是规范分隔；TAB / " | " 作为旧格式兼容
        if "\t" in line:
            doi, _, name = line.partition("\t")
        elif " | " in line:
            doi, _, name = line.partition(" | ")
        else:
            lpart = line.split(None, 1)
            doi = lpart[0]
            name = lpart[1] if len(lpart) > 1 else ""
        doi = doi.strip()
        name = name.strip().lstrip("|:").strip()
        if doi in seen:
            warn("跳过重复 DOI：" + doi)
            continue
        seen.add(doi)
        lentry.append((doi, name or None))
    return lentry


### check：只校验结构性前提（文件在、命令在），业务内容（DOI 是否预印本等）不在这里查
def check_dois_file(arg_path):
    """传文件就用文件，传目录就找其中的 DOI 列表（兼容 dois_row.txt / dois.row.txt）；返回绝对 Path。"""
    path_file = Path(arg_path).expanduser()
    if path_file.is_dir():
        # 标准名是 dois_row.txt；dois.row.txt 作旧名兜底
        lcandidate = [path_file / name for name in ("dois_row.txt", "dois.row.txt")]
        lfound = [cand for cand in lcandidate if cand.is_file()]
        if not lfound:
            fail("目录下找不到 dois_row.txt：" + str(path_file))
        path_file = lfound[0]
    if not path_file.is_file():
        fail("找不到 DOI 列表：" + str(path_file))
    return path_file.resolve()


def check_scansci_pdf(cmd, dry_run):
    """确认 scansci-pdf 可执行；dry-run 不强制。返回最终可执行路径。"""
    path_exe = shutil.which(cmd)
    if path_exe is None and not dry_run:
        fail("PATH 中找不到 " + cmd + "；请先在 bash 里运行 `scanscipy` 激活 venv，"
             "或用 --scansci-pdf 指定可执行文件。")
    return path_exe or cmd
### to here


def get_outdir(path_base, multi, doi, name, idx, total):
    """算出该篇的绝对落盘目录：单篇 = 同级目录；多篇 = 子目录（缺名回退 DOI）。"""
    if not multi:
        return path_base
    subdir = sanitize_name(name) if name else sanitize_name(doi.replace("/", "_"))
    if not name:
        warn("[" + str(idx) + "/" + str(total) + "] " + doi + " 无子目录名，回退为 " + subdir + "/")
    return path_base / subdir


def download_one(exe, doi, path_out, wait, skip_existing, dry_run):
    """跑一篇 browser-get；返回状态串。默认强制重抓官网当前版；仅 --skip-existing 时目标已有 PDF 才跳过。"""
    path_out.mkdir(parents=True, exist_ok=True)
    lexisting = list(path_out.glob("*.pdf"))
    if lexisting and skip_existing:
        print("  📁 已存在 PDF，--skip-existing 跳过：" + lexisting[0].name)
        return "已存在"

    # --manual：可见浏览器、用户逐篇过人机验证 / 登录机构；--output 传绝对路径
    cmd = [exe, "browser-get", doi, "--manual", "--output", str(path_out), "--wait", str(wait)]
    print("  ▶️  $ " + " ".join(cmd))
    if dry_run:
        return "dry-run"

    # 默认强制重抓会覆盖同名 <doi>_Official.pdf，故按 mtime（这轮之后被写过）判定成功，
    # 不能用“路径不在旧集合里”——覆盖同名时新旧同路径会被误判为失败。rc 仅作参考。
    t_start = time.time()
    rc = subprocess.run(cmd).returncode
    lnew = [p for p in path_out.glob("*.pdf") if p.stat().st_mtime >= t_start - 1]
    if lnew:
        print("  ✅ " + lnew[0].name)
        return "成功"
    print("  ❌ 未落地 PDF（rc=" + str(rc) + "）")
    return "失败"


def main(args):
    ### check
    path_file = check_dois_file(args.dois)
    exe = check_scansci_pdf(args.scansci_pdf, args.dry_run)
    ### to here

    ### prepare
    path_base = path_file.parent
    lentry = parse_dois(path_file)
    if not lentry:
        fail(str(path_file) + " 中没有有效 DOI")
    multi = len(lentry) > 1
    print("📁 列表：" + str(path_file))
    print("📁 落盘根目录：" + str(path_base))
    print("📊 模式：" + ("多篇(调研)" if multi else "单篇") + "  共 " + str(len(lentry)) + " 篇\n")
    ### to here

    ### main：逐篇下载。可见浏览器要用户人工过验证，必须串行，不能并发
    total = len(lentry)
    lresult = []
    for idx, (doi, name) in enumerate(lentry, 1):
        print("📍 [" + str(idx) + "/" + str(total) + "] " + doi)
        path_out = get_outdir(path_base, multi, doi, name, idx, total)
        status = download_one(exe, doi, path_out, args.wait, args.skip_existing, args.dry_run)
        lresult.append((status, doi, path_out))
        print("")
    ### to here

    ### summary
    print("================ 📊 summary")
    for status, doi, path_out in lresult:
        print(status.rjust(7) + "  " + doi + "  →  " + str(path_out))
    lfail = [r for r in lresult if r[0] == "失败"]
    nok = sum(1 for r in lresult if r[0] == "成功")
    print("成功 " + str(nok) + " · 失败 " + str(len(lfail)) + " · 共 " + str(total))
    if lfail:
        print("❌ 失败篇目重跑：用同一 dois_row.txt 加 --skip-existing 重跑，已落 PDF 跳过、只补失败几篇。")
        raise SystemExit(1)
    print("🎉 全部完成")
    ### to here


def build_parser():
    parser = argparse.ArgumentParser(description="按 dois_row.txt 逐篇 scansci-pdf browser-get 下载")
    parser.add_argument("dois", help="dois_row.txt 路径（或其所在目录，自动找 dois_row.txt）")
    parser.add_argument("--wait", type=int, default=300, help="每篇手动操作超时秒数（默认 300，机构登录慢可调大）")
    parser.add_argument("--skip-existing", dest="skip_existing", action="store_true",
                        help="目标目录已有 PDF 时跳过（默认强制重抓，确保拿官网当前版）")
    parser.add_argument("--dry-run", action="store_true", help="只打印将执行的命令，不真正下载")
    parser.add_argument("--scansci-pdf", dest="scansci_pdf", default="scansci-pdf",
                        help="scansci-pdf 命令（默认走 PATH，需先 scanscipy 激活）")
    return parser


if __name__ == "__main__":
    main(build_parser().parse_args())


# ---- 手动测试：注释掉上面的 main(...) 调用，改用下面任一 test_args ----
# test_single = argparse.Namespace(dois="literatures/260630_中文名/dois_row.txt",
#                                  wait=300, skip_existing=False, dry_run=True, scansci_pdf="scansci-pdf")
# test_multi  = argparse.Namespace(dois="literatures/260630_investigate_主题/dois_row.txt",
#                                  wait=600, skip_existing=False, dry_run=True, scansci_pdf="scansci-pdf")
# main(test_single)
# main(test_multi)
