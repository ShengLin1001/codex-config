#!/usr/bin/env python3
"""Export one slide of a .pptx diagram to a high-resolution PNG with PowerPoint (COM).

PowerPoint itself renders the slide, so the PNG matches what the user sees when editing.
officecli `view screenshot` is an HTML approximation and is not used for delivery.
The slide size is the figure size (1:1), so pixel size = slide size × dpi.
"""

import argparse
import sys
from pathlib import Path

import pywintypes
import win32com.client

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

PT_PER_INCH = 72


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def get_presentation(app, path_pptx):
    """Reuse the presentation if the user already has it open (exports the unsaved state too).

    Returns:
        (presentation, opened_here)
    """
    for pres in app.Presentations:
        try:
            if Path(pres.FullName).resolve() == path_pptx:
                return pres, False
        except pywintypes.com_error:
            continue  # 受保护视图等窗口读 FullName 会报 "Automation rights are not granted"
    # WithWindow=False：不弹窗口；ReadOnly：不锁文件，用户可同时在 PowerPoint 里改
    return app.Presentations.Open(str(path_pptx), ReadOnly=True, Untitled=False, WithWindow=False), True


def export(path_pptx, path_png, dpi, index_slide):
    app = win32com.client.Dispatch("PowerPoint.Application")
    pres, opened_here = get_presentation(app, path_pptx)
    try:
        if not 1 <= index_slide <= pres.Slides.Count:
            fail(f"-slide {index_slide} 超出范围（共 {pres.Slides.Count} 页）")
        width = round(pres.PageSetup.SlideWidth / PT_PER_INCH * dpi)
        height = round(pres.PageSetup.SlideHeight / PT_PER_INCH * dpi)
        print(f"▶️  PowerPoint: slide {index_slide} → {width}×{height} px @ {dpi} dpi")
        pres.Slides(index_slide).Export(str(path_png), "PNG", width, height)
    finally:
        if opened_here:
            pres.Close()
        # 只在没有别的演示文稿时退出，避免关掉用户正在用的 PowerPoint
        if app.Presentations.Count == 0:
            app.Quit()
    if not path_png.is_file():
        fail("导出失败：" + str(path_png))
    print(f"✅ {path_png}")


### main
parser = argparse.ArgumentParser(description="pptx 单页 → PNG（PowerPoint COM）")
parser.add_argument("-input", required=True, help=".pptx 文件")
parser.add_argument("-output", default=None, help="PNG 路径，默认与 pptx 同名")
parser.add_argument("-dpi", type=int, default=500, help="预览 200，交付 500")
parser.add_argument("-slide", type=int, default=1, help="导出第几页（1 起）")
args = parser.parse_args()

path_pptx = Path(args.input).resolve()
if not path_pptx.is_file():
    fail("pptx 不存在：" + str(path_pptx))
if args.dpi < 1:
    fail("-dpi 必须是正整数")
path_png = Path(args.output).resolve() if args.output else path_pptx.with_suffix(".png")
export(path_pptx, path_png, args.dpi, args.slide)
### to here

# test_args = {"input": "assets/house-matrix.pptx", "output": None, "dpi": 200, "slide": 1}  # 快速预览
# test_args = {"input": "assets/house-matrix.pptx", "output": None, "dpi": 500, "slide": 1}  # 交付分辨率
