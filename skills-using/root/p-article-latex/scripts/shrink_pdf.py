#!/usr/bin/env python3
"""一次性脚本：按 (dpi, quality) 逐档重压 PDF 内嵌图片，直到体积达标。"""
import sys
from pathlib import Path

import fitz


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def shrink_pdf(path_src, path_dst, target_mb):
    # ponytail: 逐档暴力搜索，比按图逐个调参少写一堆代码
    ldpi_quality = [(300, 80), (250, 75), (200, 70), (150, 65), (120, 55), (100, 50), (72, 40)]
    for dpi, quality in ldpi_quality:
        doc = fitz.open(path_src)
        doc.rewrite_images(dpi_threshold=dpi + 1, dpi_target=dpi, quality=quality)
        doc.save(path_dst, garbage=4, deflate=True, clean=True)
        doc.close()
        size_mb = path_dst.stat().st_size / 1e6
        print(f"  dpi={dpi} q={quality} ▶️ {size_mb:.2f} MB")
        if size_mb <= target_mb:
            return size_mb
    return size_mb


path_src = Path(sys.argv[1]).resolve()
path_dst = Path(sys.argv[2]).resolve()
if not path_src.is_file():
    fail(f"找不到 {path_src}")
print(f"📁 {path_src.name} ({path_src.stat().st_size / 1e6:.1f} MB)")
size_mb = shrink_pdf(path_src, path_dst, float(sys.argv[3]))
print(f"✅ {path_dst.name} = {size_mb:.2f} MB")
