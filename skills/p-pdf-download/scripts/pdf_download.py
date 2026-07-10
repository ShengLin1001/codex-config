#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""按 dois.txt（每行一个 DOI）批量调用 scansci-pdf browser-get 下载官网正文 PDF。

scansci-pdf 自己会把 PDF 写成 <safe_doi>_Official.pdf 并默认落在用户级 papers 目录，
本脚本只做两件它不做的事：把输出目录钉在当前目录，把文件名统一成短名。

命名规则: 取 DOI 后缀（'/' 之后）清洗为合法文件名，超长截断 + 6 位哈希保唯一。
    10.1016/j.actamat.2024.120459  ->  j.actamat.2024.120459.pdf
    10.1103/PhysRevB.108.014102    ->  PhysRevB.108.014102.pdf

用法:
    scanscipy                                     # 先激活 scansci-pdf venv
    python pdf_download.py                        # 读 ./dois.txt，PDF 落 ./
    python pdf_download.py dois.txt --dry-run
    python pdf_download.py dois.txt -o refs/ --skip-existing --wait 600
    python pdf_download.py --selftest
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Windows 控制台按 UTF-8，避免论文元数据乱码（与 CLAUDE.md 约定一致）
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

MAX_STEM = 60  # 文件名主干上限，给长目录路径留余量


def fail(msg):
    print("❌ ERROR: " + str(msg))
    raise SystemExit(1)


def normalize_doi(raw):
    """与 scansci_pdf.identifiers.normalize_doi 对齐：剥掉 doi.org / doi: 前缀。"""
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", raw.strip(), flags=re.I)
    return re.sub(r"^doi:\s*", "", value, flags=re.I).strip()


def scansci_name(doi):
    """scansci-pdf browser-get 实际写出的文件名，用来定位待重命名的文件。"""
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", doi).strip("_") or "paper"
    return stem + "_Official.pdf"


def short_name(doi):
    """统一短命名：DOI 后缀清洗；过长则截断 + 6 位哈希。"""
    # ponytail: 丢掉 10.xxxx 注册商前缀换短名，只有不同出版商后缀同名才会撞（极罕见）；
    #           真撞了就把前缀拼回 stem。
    suffix = doi.split("/", 1)[-1] or doi
    stem = re.sub(r"[^A-Za-z0-9._-]+", "_", suffix).strip("._-") or "paper"
    if len(stem) > MAX_STEM:
        stem = stem[:MAX_STEM] + "_" + hashlib.sha1(doi.encode("utf-8")).hexdigest()[:6]
    return stem + ".pdf"


def parse_dois(path_file):
    """dois.txt → 去重后的 DOI 列表；空行与 # 注释行忽略。

    utf-8-sig：PowerShell 写出的 txt 常带 BOM，普通 utf-8 读会污染首行 DOI。
    行内只取第一段（DOI 不含空白），容忍旧格式残留的第二列名字。
    """
    ldoi, seen = [], set()
    for line in path_file.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        doi = normalize_doi(line.split()[0])
        if doi in seen:
            continue
        seen.add(doi)
        ldoi.append(doi)
    return ldoi


def main(args):
    ### check
    path_file = Path(args.dois).expanduser()
    if not path_file.is_file():
        fail("找不到 DOI 列表：" + str(path_file))
    exe = shutil.which(args.scansci_pdf)
    if exe is None and not args.dry_run:
        fail("PATH 中找不到 " + args.scansci_pdf + "；请先在 bash 里运行 `scanscipy` 激活 venv。")
    exe = exe or args.scansci_pdf
    ### to here

    ### prepare
    ldoi = parse_dois(path_file)
    if not ldoi:
        fail(str(path_file) + " 中没有有效 DOI")
    path_out = Path(args.output).expanduser().resolve()
    path_out.mkdir(parents=True, exist_ok=True)

    ltodo = []
    for doi in ldoi:
        if args.skip_existing and (path_out / short_name(doi)).is_file():
            print("📁 已存在，跳过：" + short_name(doi))
            continue
        ltodo.append(doi)
    print("📁 列表：" + str(path_file))
    print("📁 落盘目录：" + str(path_out))
    print("📊 待下载 " + str(len(ltodo)) + " / 共 " + str(len(ldoi)) + " 篇\n")
    if not ltodo:
        print("🎉 全部已下载")
        return
    ### to here

    ### main：browser-get 内部逐篇串行开可见浏览器，人工过验证 / 机构登录
    cmd = [exe, "browser-get", *ltodo, "--manual", "--output", str(path_out), "--wait", str(args.wait)]
    print("▶️  $ " + " ".join(cmd) + "\n")
    if args.dry_run:
        for doi in ltodo:
            print("  " + doi + "  →  " + str(path_out / short_name(doi)))
        return
    t_start = time.time()
    subprocess.run(cmd)  # 部分失败时 rc=1，逐篇结果下面按落盘文件判定，rc 不用
    ### to here

    ### summary：只认这轮新写出的文件，避免把上轮残留的 _Official.pdf 误判为成功
    lok, lfail = [], []
    for doi in ltodo:
        path_src = path_out / scansci_name(doi)
        if path_src.is_file() and path_src.stat().st_mtime >= t_start - 1:
            path_dst = path_out / short_name(doi)
            os.replace(path_src, path_dst)  # 覆盖同名旧版；Windows 上 Path.rename 遇同名会炸
            lok.append((doi, path_dst))
        else:
            lfail.append(doi)

    print("\n================ 📊 summary")
    for doi, path_dst in lok:
        print("   成功  " + doi + "  →  " + path_dst.name)
    for doi in lfail:
        print("   失败  " + doi)
    print("成功 " + str(len(lok)) + " · 失败 " + str(len(lfail)) + " · 共 " + str(len(ltodo)))
    if lfail:
        print("❌ 失败篇目重跑：同一 dois.txt 加 --skip-existing，已落 PDF 跳过、只补失败几篇。")
        raise SystemExit(1)
    print("🎉 全部完成")
    ### to here


def selftest():
    assert normalize_doi(" https://doi.org/10.1016/x ") == "10.1016/x"
    assert normalize_doi("doi: 10.1016/x") == "10.1016/x"
    assert short_name("10.1016/j.actamat.2024.120459") == "j.actamat.2024.120459.pdf"
    assert short_name("10.1103/PhysRevB.108.014102") == "PhysRevB.108.014102.pdf"
    assert short_name("10.1002/(SICI)1097-0088(199601)16:1<1::AID>3.0.CO;2-Q") == "SICI_1097-0088_199601_16_1_1_AID_3.0.CO_2-Q.pdf"
    assert scansci_name("10.1016/j.actamat.2024.120459") == "10.1016_j.actamat.2024.120459_Official.pdf"
    long_doi = "10.1016/" + "a" * 80
    assert len(Path(short_name(long_doi)).stem) == MAX_STEM + 7 and short_name(long_doi) != short_name(long_doi + "b")

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        path_file = Path(tmp) / "dois.txt"
        path_file.write_text("﻿10.1016/a\n\n# c\n10.1016/a\n10.1103/b 金薄膜相变\n", encoding="utf-8")
        assert parse_dois(path_file) == ["10.1016/a", "10.1103/b"]
    print("✅ selftest ok")


def build_parser():
    parser = argparse.ArgumentParser(description="按 dois.txt 批量 scansci-pdf browser-get 下载官网 PDF")
    parser.add_argument("dois", nargs="?", default="dois.txt", help="DOI 列表，每行一个 DOI（默认 ./dois.txt）")
    parser.add_argument("-o", "--output", default=".", help="PDF 输出目录（默认当前目录 ./）")
    parser.add_argument("--wait", type=int, default=300, help="每篇人工操作超时秒数（默认 300，机构登录慢可调大）")
    parser.add_argument("--skip-existing", dest="skip_existing", action="store_true",
                        help="目标 PDF 已存在时跳过（默认强制重抓，确保拿官网当前版）")
    parser.add_argument("--dry-run", action="store_true", help="只打印将执行的命令与落盘文件名，不真正下载")
    parser.add_argument("--scansci-pdf", dest="scansci_pdf", default="scansci-pdf",
                        help="scansci-pdf 命令（默认走 PATH，需先 scanscipy 激活）")
    parser.add_argument("--selftest", action="store_true", help="跑命名 / 解析自检，不下载")
    return parser


if __name__ == "__main__":
    _args = build_parser().parse_args()
    if _args.selftest:
        selftest()
    else:
        main(_args)
