#!/usr/bin/env python3
"""分级容器 + 研究链技术路线图的初稿生成器（开题报告图 2），新图从这里复制改起。

坐标单位 u = 0.1 mm；幻灯片 33.867 × 19.05 cm，与组会 / 答辩 PPT 同尺寸，答辩时直接复制。
插入 Word（宽 14.6 cm）时整体缩放 0.43，所以框内字 ≥ 18 pt（缩放后约 7.8 pt）。
主次靠层级表达：总题通栏 > 阶段容器（大块箭头相连）> 行标签 > 链条框；每行右侧放一张示意图。
立体风格：明亮渐变底 + 细黑边 + 下投影 + 顶部斜面。
脚本把形状写成 officecli batch 命令一次建好 pptx；交付后 pptx 是唯一源文件，
之后用 officecli set 按 @name= 改，不再重跑本脚本（会覆盖用户在 PowerPoint 里的手改）。
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SLIDE_W_U, SLIDE_H_U = 3387, 1905
FONT = "Microsoft YaHei"
PT_PER_U = 0.28346  # 0.1 mm → pt
LBATCH = []

NAVY = "1F3A68"
# 每个阶段一个色相：title 给阶段标题和尺度字，line 给标签和卡片边框，label 给标签字，arrow 给链内箭头，
# container 是容器自上而下的渐变，band 是链条内衬（取渐变的深端，靠斜面和投影与容器区分）
DICT_STAGE = {
    "相变": {"title": "2F5597", "line": "2F5597", "label": "00448D", "arrow": "2F5597",
             "container": "DEEBF7-BDD7EE-90", "band": "BDD7EE"},
    "强韧": {"title": "4C8232", "line": "70AD47", "label": "407523", "arrow": "548235",
             "container": "E2F0D9-A9D18E-90", "band": "A9D18E"},
}
LINE_3D = "000000:0.75"
DICT_3D = {"shadow": "000000-4-90-3-40", "softEdge": "1pt", "bevel": "circle",
           "lighting": "threePt"}
DICT_BAND_3D = {"softEdge": "1pt", "bevel": "circle", "lighting": "threePt"}
SHADOW_ARROW = "000000-4-90-3-40"
RADIUS = 12
SIZE_TITLE, SIZE_STAGE, SIZE_LABEL, SIZE_CARD, SIZE_TAG = 99, 78, 71, 64, 56  # 28 / 22 / 20 / 18 / 16 pt

X0, X1 = 80, 3307  # 容器左右边
X_LABEL, W_LABEL = 140, 520
X_CHAIN, W_CARD, W_GAP = 710, 580, 100  # 链条 3 框 + 2 个箭头间隙
W_CHAIN = 3 * W_CARD + 2 * W_GAP
X_IMG, W_IMG = 2700, 590
ROW_H, CARD_H = 355, 265
H_STAGE_HEAD = 110
Y_GAP_ROW, Y_PAD, Y_GAP_STAGE = 30, 40, 210  # 行间距、容器下边距、两容器间（放大箭头）


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def cm(u):
    return f"{u / 100:.3f}cm"


def pt(u):
    return f"{u * PT_PER_U:.1f}pt"


def adj_round(radius, w, h):
    """roundRect 圆角半径 = min(w, h) × adj / 100000。"""
    return "adj:val " + str(round(radius / min(w, h) * 100000))


def add(kind, name, x, y, w, h, **props):
    dict_prop = {"name": name, "x": cm(x), "y": cm(y), "width": cm(w), "height": cm(h)}
    dict_prop.update({k: str(v) for k, v in props.items()})
    LBATCH.append({"command": "add", "parent": "/slide[1]", "type": kind, "props": dict_prop})


def text_props(llines, size_u, color, bold=False, align="center", valign="middle", margin="0"):
    # 用真换行符分段；字面量 "\\n" 有时不拆段。母版正文样式带 10 pt 段前距，这里清零
    return {"text": "\n".join(llines), "size": pt(size_u), "color": color, "bold": str(bold).lower(),
            "align": align, "valign": valign, "margin": margin, "autoFit": "none", "lineSpacing": "1x",
            "spaceBefore": "0pt"}


def add_box(name, x, y, w, h, fill, line, llines=None, size_u=SIZE_CARD, color=NAVY, bold=False, radius=RADIUS,
            margin="0.1cm", **props):
    dict_text = text_props(llines, size_u, color, bold=bold, margin=margin) if llines else {}
    dict_fill = {"fill": fill} if fill else {}  # 渐变框不给 fill，改走 props 里的 gradient
    dict_line = {"line": line} if line else {}
    add("shape", name, x, y, w, h, geometry="roundRect", adj=adj_round(radius, w, h), **dict_fill, **dict_line,
        **props, **dict_text)


def add_textbox(name, x, y, w, h, llines, size_u, color, bold=False, align="center"):
    add("textbox", name, x, y, w, h, fill="none", line="none", **text_props(llines, size_u, color, bold, align))


def add_right_arrow(name, x, y, w, h, shaft, head, fill):
    add("shape", name, x, y, w, h, geometry="rightArrow", fill=fill, line="none", shadow=SHADOW_ARROW,
        adj=f"adj1:val {round(shaft / h * 100000)},adj2:val {round(head / min(w, h) * 100000)}")


def add_stage_chevrons(cx, y_top):
    """阶段间的双层折线箭头（︾），上蓝下绿；比块箭头、倒三角、承接带轻，留白多。
    chevron 原本朝右，转 90° 朝下，所以框宽是竖向厚度、框高是横向宽度。V 形下落 80、带厚 45，两层错开 75，
    下层尖端只碰下方容器边框（Y_GAP_STAGE = 210）。"""
    for i, fill in enumerate(["8FAADC", "70AD47"]):
        yc = y_top + 70 + i * 75
        add("shape", f"箭头-阶段-{i + 1}", cx - 62.5, yc - 190, 125, 380, geometry="chevron", rotation=90,
            adj="adj:val 64000", fill=fill, line="none", shadow=SHADOW_ARROW, bevel="circle", lighting="threePt")


def get_transparent(path_img):
    """白底转透明：示意图直接放在容器浅底上，不加框，才能放大到行高。
    只清与图片边缘连通的白色，原子球高光、空心箭头内部的白色保留（全图按阈值清会透出底色）。
    照片（HRTEM 等）不要调用。"""
    path_out = Path(tempfile.gettempdir()) / "stage-chain-img" / path_img.name
    path_out.parent.mkdir(exist_ok=True)
    arr = np.array(Image.open(path_img).convert("RGBA"))
    label, _ = ndimage.label(arr[..., :3].min(axis=2) > 245)
    lborder = np.unique(np.concatenate([label[0], label[-1], label[:, 0], label[:, -1]]))
    arr[np.isin(label, lborder[lborder > 0]), 3] = 0
    Image.fromarray(arr).save(path_out)
    return path_out


def add_stage(stage, y, h, title, tag):
    """阶段容器：浅底框 + 居中阶段标题 + 右侧方法与尺度标注（取代单独的方法栏 / 横梁）。"""
    dict_c = DICT_STAGE[stage]
    add_box("容器-" + stage, X0, y, X1 - X0, h, None, LINE_3D, radius=24, gradient=dict_c["container"], **DICT_3D)
    add_textbox("阶段-" + stage, X0 + 600, y + 15, X1 - X0 - 1200, H_STAGE_HEAD - 20, [title], SIZE_STAGE,
                dict_c["title"], bold=True)
    add_textbox("尺度-" + stage, X1 - 960, y + 25, 900, H_STAGE_HEAD - 40, [tag], SIZE_TAG, dict_c["title"],
                align="right")


def add_row(stage, key, y, llabel, lcard, path_img):
    """一行研究链：行标签 → 浅色内衬上的 3 个框（块箭头相连）→ 右侧示意图（缺图时放占位框）。"""
    dict_c = DICT_STAGE[stage]
    y_card = y + (ROW_H - CARD_H) // 2
    add_box("标签-" + key, X_LABEL, y_card, W_LABEL, CARD_H, "FFFFFF", dict_c["line"] + ":1.5", llabel,
            SIZE_LABEL, dict_c["label"], bold=True)
    add_box("链条-" + key, X_CHAIN - 30, y + 10, W_CHAIN + 60, ROW_H - 20, dict_c["band"], "none", radius=20,
            **DICT_BAND_3D)
    for i, llines in enumerate(lcard):
        x = X_CHAIN + i * (W_CARD + W_GAP)
        add_box(f"卡片-{key}-{i + 1}", x, y_card, W_CARD, CARD_H, "FFFFFF", dict_c["line"] + ":1.5", llines,
                SIZE_CARD, NAVY)
        if i < len(lcard) - 1:
            add_right_arrow(f"箭头-{key}-{i + 1}", x + W_CARD + 12, y_card + CARD_H // 2 - 30, W_GAP - 24, 60, 30,
                            34, dict_c["arrow"])
    if path_img is None or not path_img.is_file():
        print(f"⚠️  {key}：没有示意图，放占位框")
        add_box("图-" + key, X_IMG, y + 10, W_IMG, ROW_H - 20, "FFFFFF", dict_c["line"] + ":0.75", ["示意图"],
                SIZE_TAG, dict_c["line"], lineDash="dash")
        return
    path_img = get_transparent(path_img)
    w_px, h_px = Image.open(path_img).size
    scale = min(W_IMG / w_px, ROW_H / h_px)
    w, h = w_px * scale, h_px * scale
    add("picture", "图-" + key, X_IMG + (W_IMG - w) / 2, y + (ROW_H - h) / 2, w, h, src=str(path_img))


def run_officecli(largs, stdin=None):
    for _ in range(5):
        result = subprocess.run(["officecli"] + largs, input=stdin, capture_output=True)
        out = result.stdout.decode("utf-8", "replace")
        err = result.stderr.decode("utf-8", "replace")
        if result.returncode == 0:
            return out
        # 文件被杀毒、索引或刚关闭的 PowerPoint 短暂占用，保存时报这个错；文件未改动，可原样重试
        if "Unable to remove the file to be replaced" not in out + err:
            break
        print("⚠️  officecli " + largs[0] + "：文件被占用，2 s 后重试")
        time.sleep(2)
    fail("officecli " + " ".join(largs[:2]) + " 失败：\n" + out[-2000:] + err[-2000:])


def build_pptx(path_pptx, lbatch):
    # 不起常驻进程：写完即落盘，PowerPoint 导出时不会读到旧文件或撞文件锁
    os.environ["OFFICECLI_NO_AUTO_RESIDENT"] = "1"
    path_pptx.unlink(missing_ok=True)
    run_officecli(["create", str(path_pptx)])
    run_officecli(["set", str(path_pptx), "/", "--prop", "slideWidth=" + cm(SLIDE_W_U), "--prop", "slideHeight=" + cm(SLIDE_H_U)])
    # 主题字体设成雅黑：形状不必逐个写字体，用户在 PowerPoint 里新加的文本框也是雅黑
    run_officecli(["set", str(path_pptx), "/theme", "--prop", "bodyFont=" + FONT, "--prop", "bodyFont.ea=" + FONT,
                   "--prop", "headingFont=" + FONT, "--prop", "headingFont.ea=" + FONT])
    run_officecli(["add", str(path_pptx), "/", "--type", "slide", "--prop", "background=FFFFFF"])
    out = run_officecli(["batch", str(path_pptx), "--json"], stdin=json.dumps(lbatch, ensure_ascii=False).encode("utf-8"))
    dict_summary = json.loads(out)["data"]["summary"]
    print(f"📊 batch: {dict_summary['succeeded']}/{dict_summary['total']} succeeded")
    print(f"✅ {path_pptx}")


### main
parser = argparse.ArgumentParser(description="生成分级容器 + 研究链技术路线图初稿 pptx（officecli）")
parser.add_argument("-output", required=True, help="输出 .pptx")
parser.add_argument("-img_dir", default=None, help="示意图目录（row1.png、row2.png、row3.png）；不给则放占位框")
parser.add_argument("-if_overwrite", action="store_true", help="允许覆盖已有 pptx（只在初稿迭代时用）")
args = parser.parse_args()

path_pptx = Path(args.output).resolve()
path_img_dir = Path(args.img_dir).resolve() if args.img_dir else None
if path_pptx.suffix != ".pptx":
    fail("-output 必须是 .pptx：" + str(path_pptx))
if path_pptx.exists() and not args.if_overwrite:
    fail("已存在，可能有用户手改，不覆盖：" + str(path_pptx) + "（初稿迭代加 -if_overwrite）")


def get_img(name):
    return path_img_dir / name if path_img_dir else None


### 总题通栏：暖色渐变，与下面的冷色阶段容器拉开
add_box("总题", X0, 40, X1 - X0, 150, None, LINE_3D, ["基于相工程的 FCC 金属强韧化机制"], SIZE_TITLE, "843C0C",
        bold=True, radius=16, gradient="FBE5D6-F8CBAD-90", **DICT_3D)

### 阶段一：相变机制（第一性原理），两行
Y_A = 240
H_A = H_STAGE_HEAD + 2 * ROW_H + Y_GAP_ROW + Y_PAD
add_stage("相变", Y_A, H_A, "应变诱导 FCC→HCP 相变机制", "第一性原理 · 百原子")
add_row("相变", "普适", Y_A + H_STAGE_HEAD, ["FCC 金属", "应变诱导相变"],
        [["二维应变", "能量景观"], ["滑移势垒与", "相变能垒"], ["四阶连续介质", "弹性模型"]], get_img("row1.png"))
add_row("相变", "薄膜", Y_A + H_STAGE_HEAD + ROW_H + Y_GAP_ROW, ["超薄金纳米片", "相变机制"],
        [["厚度与应变", "贡献分离"], ["逐层与协同", "相变路径"], ["HCP 金力学性质", "与稳定性"]], get_img("row2.png"))

### 阶段二：强韧化（机器学习势），一行；阶段间一个大块箭头
Y_B = Y_A + H_A + Y_GAP_STAGE
H_B = H_STAGE_HEAD + ROW_H + Y_PAD
add_stage("强韧", Y_B, H_B, "HCP/FCC 两相金强韧化设计", "机器学习势 · 百万原子")
add_row("强韧", "跨尺度", Y_B + H_STAGE_HEAD, ["多相金", "跨尺度模拟"],
        [["多相金", "BPNN 势函数"], ["有限温度", "形核与扩展"], ["HCP/FCC 异质结构", "强韧化机制"]], get_img("row3.png"))
add_stage_chevrons(X_CHAIN + W_CHAIN // 2, Y_A + H_A)

if Y_B + H_B > SLIDE_H_U - 30:
    fail(f"超出幻灯片高度：{Y_B + H_B} > {SLIDE_H_U - 30}")
build_pptx(path_pptx, LBATCH)
### to here

# test_args = {"output": "stage-chain.pptx", "img_dir": None, "if_overwrite": False}           # 占位框
# test_args = {"output": "stage-chain.pptx", "img_dir": "<dir>/img", "if_overwrite": True}      # 带示意图
