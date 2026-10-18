#!/usr/bin/env python3
"""按稿件里的实际印刷宽度把 PNG 图重采样到指定 dpi，写成 .tex 能直接 include 的 PDF。

为什么不用 shrink_pdf.py：那个走 PyMuPDF 的 rewrite_images，dpi_target 与成品体积
在本仓库的稿件上非单调（290 dpi 压出 2.25 MB，300 dpi 反而 5.13 MB），不可控。
这里自己 Lanczos 重采样 + Pillow 编码，dpi 与 quality 都是实打实的。

原图往往严重过采样：600 dpi 的 PNG 印在 5.7 in 宽的位置上，有效分辨率能到 1700 dpi。
本脚本按 `\\includegraphics[width=...\\textwidth]` 算出每张图的真实印刷宽度再重采样。

用法：
    # 投稿源文件包：600 dpi 无损
    python resample_figures.py -tex <version>/latex/submission/manuscript.tex \\
        -src <version>/figure -out <version>/latex/submission -dpi 600 -codec flate

    # 送审 PDF（5 MB 预算）：400 dpi JPEG q82
    python resample_figures.py -tex ... -src ... -out <tmpdir> -dpi 400 -codec jpeg -quality 82
"""
import argparse
import io
import re
from pathlib import Path

import fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

PT_PER_INCH = 72.27                       # TeX pt，不是 PostScript pt
DICT_WIDTH_PT = {'textwidth': 522.0,      # elsarticle[final,5p,times,twocolumn] 实测
                 'columnwidth': 252.0}    # 换 documentclass 要重测：\typeout{\the\textwidth}
RE_INCLUDE = re.compile(
    r'\\includegraphics\[width=([\d.]*)\\(textwidth|columnwidth)\]\{(figure-[\w.-]+?)\.\w+\}')


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def parse_figure_widths(path_tex):
    """从 .tex 读出 {图名: 印刷宽度(inch)}。"""
    dict_width = {}
    for frac, kind, name in RE_INCLUDE.findall(path_tex.read_text(encoding='utf-8')):
        dict_width[name] = float(frac or 1.0) * DICT_WIDTH_PT[kind] / PT_PER_INCH
    if not dict_width:
        fail(rf"{path_tex} 里没匹配到 \includegraphics[width=...\textwidth]")
    return dict_width


def encode_image(img, codec, dpi, quality):
    """按 codec 编码成字节流；flate 无损，jpeg 用 4:4:4 免得彩色细线被色度下采样糊掉。"""
    buf = io.BytesIO()
    if codec == 'flate':
        img.save(buf, format='PNG', dpi=(dpi, dpi), optimize=True)
    else:
        img.convert('RGB').save(buf, format='JPEG', quality=quality, subsampling=0,
                                dpi=(dpi, dpi), optimize=True)
    return buf.getvalue()


def resample_one(path_png, width_inch, path_pdf, dpi, codec, quality):
    """重采样到 width_inch x dpi 并封成单页 PDF，返回 (原宽, 新宽, 输出 MB)。"""
    img = Image.open(path_png)
    width_old = img.size[0]
    width_new = min(width_old, max(1, round(width_inch * dpi)))   # 不做上采样
    if width_new < width_old:
        img = img.resize((width_new, round(img.size[1] * width_new / width_old)),
                         Image.LANCZOS)
    data = encode_image(img, codec, dpi, quality)
    filetype = 'png' if codec == 'flate' else 'jpeg'
    path_pdf.write_bytes(fitz.open(stream=data, filetype=filetype).convert_to_pdf())
    return width_old, width_new, path_pdf.stat().st_size / 1e6


def build(path_tex, path_src, path_out, dpi, codec, quality):
    dict_width = parse_figure_widths(path_tex)
    path_out.mkdir(parents=True, exist_ok=True)
    print(f"📁 源图 {path_src}")
    print(f"📁 输出 {path_out}")
    print(f"▶️ {dpi} dpi / {codec}" + (f" q={quality}" if codec == 'jpeg' else " 无损"))

    total_mb = 0.0
    for name, width_inch in sorted(dict_width.items()):
        path_png = path_src / f'{name}.png'
        if not path_png.is_file():
            fail(f"找不到源图 {path_png}")
        width_old, width_new, mb = resample_one(path_png, width_inch, path_out / f'{name}.pdf',
                                                dpi, codec, quality)
        total_mb += mb
        print(f"✅ {name:48s} {width_old:5d}→{width_new:5d} px "
              f"(原 {width_old / width_inch:6.0f} dpi, 印刷宽 {width_inch:4.2f} in)  {mb:5.1f} MB")

    print("================ 📊 summary")
    print(f"{len(dict_width)} 张图  合计 {total_mb:.1f} MB")


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-tex', required=True, help='读印刷宽度的 manuscript.tex')
    parser.add_argument('-src', required=True, help='原始 PNG 所在目录')
    parser.add_argument('-out', required=True, help='输出 PDF 目录')
    parser.add_argument('-dpi', type=int, required=True)
    parser.add_argument('-codec', choices=['flate', 'jpeg'], default='flate')
    parser.add_argument('-quality', type=int, default=82, help='仅 -codec jpeg 生效')
    return parser


if __name__ == '__main__':
    args = build_parser().parse_args()
    build(Path(args.tex).resolve(), Path(args.src).resolve(), Path(args.out).resolve(),
          args.dpi, args.codec, args.quality)
