#!/usr/bin/env python3
"""房屋型 + 3×3 矩阵技术路线图的初稿生成器（开题报告图 2），新图从这里复制改起。

坐标单位 u = 0.1 mm，幻灯片 = 成品尺寸（14.6 × 10.3 cm），字号按成品 pt 算。
每个框只放一个短语（≤ 2 行、同字号），层级靠容器和颜色，不靠框内大小字。
配色是早期的扁平藏青单色系，列靠位置区分、不靠色相；正式出图按 SKILL.md 第 2 节换成渐变立体风。
脚本把形状写成 officecli batch 命令一次建好 pptx；交付后 pptx 是唯一源文件，
之后用 officecli set 按 @name= 改，不再重跑本脚本（会覆盖用户在 PowerPoint 里的手改）。
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

SLIDE_W_U, SLIDE_H_U = 1460, 1030
FONT = "Microsoft YaHei"
PT_PER_U = 0.28346  # 0.1 mm → pt
LBATCH = []

NAVY, LIGHT, ARROW = "1F3A68", "E3E9F2", "5E7397"  # 屋顶和板块头 / 横梁和行标签 / 块箭头
BAND, CARD_LINE, OUT_FILL = "F3F5F8", "8FA1BC", "E6ECF4"
DICT_COL_X = {"普适": 170, "薄膜": 623, "跨尺度": 1076}
COL_W = 353  # 列间距 100：放得下 68 长的块箭头
X_GAP1, X_GAP2 = 573, 1026  # 两个列间隙的中线
ROW_H, CARD_H = 170, 116  # 行带高、卡片高；卡片在行带内上下各留 27，竖向箭头与卡片各隔 12
LROW = [("热力学", 318), ("动力学", 500), ("力学", 682)]
RADIUS = 6  # 成品尺寸下的小圆角
SIZE_LABEL, SIZE_HEAD, SIZE_CARD, SIZE_NOTE = 34, 38, 36, 29  # 9.6 / 10.8 / 10.2 / 8.2 pt


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


def add_box(name, x, y, w, h, fill, line, llines, size_u, color, margin="0", bold=True, **props):
    add("shape", name, x, y, w, h, geometry="roundRect", adj=adj_round(RADIUS, w, h), fill=fill, line=line,
        **props, **text_props(llines, size_u, color, bold=bold, margin=margin))


def add_label(name, x, y, w, h, llines, **props):
    # 行标签浅底深字：深色只留给屋顶和板块头，行与列一眼分开
    add_box(name, x, y, w, h, LIGHT, "none", llines, SIZE_LABEL, NAVY, **props)


def add_textbox(name, x, y, w, h, llines, size_u, color, bold=False, align="center"):
    add("textbox", name, x, y, w, h, fill="none", line="none", **text_props(llines, size_u, color, bold, align))


def add_right_arrow(name, x, y, w, h, shaft, head):
    add("shape", name, x, y, w, h, geometry="rightArrow", fill=ARROW, line="none",
        adj=f"adj1:val {round(shaft / h * 100000)},adj2:val {round(head / min(w, h) * 100000)}")


def add_down_arrow(name, x, y, w, h, shaft, head):
    add("shape", name, x, y, w, h, geometry="downArrow", fill=ARROW, line="none",
        adj=f"adj1:val {round(shaft / w * 100000)},adj2:val {round(head / min(w, h) * 100000)}")


def run_officecli(largs, stdin=None):
    for _ in range(5):
        result = subprocess.run(["officecli"] + largs, input=stdin, capture_output=True)
        out = result.stdout.decode("utf-8", "replace")
        err = result.stderr.decode("utf-8", "replace")
        if result.returncode == 0:
            return out
        # 文件可能被杀毒、索引或刚关闭的 PowerPoint 短暂占用，保存时报这个错；文件未改动，可原样重试
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


### 屋顶（科学问题）、横梁（尺度跨越）
add("shape", "屋顶", 20, 20, 1420, 120, geometry="trapezoid", adj="adj:val " + str(round(125 / 120 * 100000)),
    fill=NAVY, line="none")
# 梯形的文字区比外框窄很多，标题放进去会折行，所以单独用文本框
add_textbox("科学问题", 120, 52, 1220, 70, ["基于相工程的 FCC 金属强韧化机制"], 50, "FFFFFF", bold=True)
# 横梁本身做成通栏块箭头表示尺度跨越，不另画细线箭头（全图只有一种箭头）；杆高 40，箭头头部高 52、长 40
add("shape", "横梁", 20, 142, 1420, 52, geometry="rightArrow", adj="adj1:val 76923,adj2:val 76923", fill=LIGHT,
    line="none", **text_props(["第一性原理 · 百原子 · 0 K"], SIZE_NOTE, NAVY, bold=True, align="left", margin="0.2cm,0,0.2cm,0"))
# 体系原子数最能体现跨尺度，数量级取自正文；右端文字让开箭头尖，否则字会伸出变窄的箭头头部
add_textbox("横梁右", 930, 148, 460, 40, ["机器学习势 · 百万原子 · 有限温度"], SIZE_NOTE, NAVY, bold=True, align="right")

### 柱头：三个研究板块（对象 + 角色，两行同字号）
# 板块头行和成果行位置自明，不加“研究板块”“预期成果”标签；只有主线行有行标签
dict_head = {"普适": ["FCC金属", "应变诱导相变"], "薄膜": ["超薄金膜", "相变机制"], "跨尺度": ["多相金", "跨尺度模拟"]}
for key, llines in dict_head.items():
    # 不加图标：板块头只放文字，居中
    add_box("板块-" + key, DICT_COL_X[key], 200, COL_W, 104, NAVY, "none", llines, SIZE_HEAD, "FFFFFF",
            margin="0.08cm,0,0.08cm,0")

### 三层楼：行带 + 竖排行标签 + 9 个研究单元（每格一个短语）
dict_label = {"热力学": "相稳定性", "动力学": "相变路径", "力学": "力学响应"}
for row, y in LROW:
    add("shape", "行带-" + row, 20, y, 1420, ROW_H, geometry="roundRect", adj=adj_round(RADIUS, 1420, ROW_H),
        fill=BAND, line="none")
    add_label("标签-" + row, 30, y + 10, 110, ROW_H - 20, [dict_label[row]], textDirection="eaVert")

dict_card = {
    ("热力学", "普适"): ["二维应变", "能量景观"],
    ("热力学", "薄膜"): ["厚度与应变", "贡献分离"],
    ("热力学", "跨尺度"): ["多相金", "BPNN势函数"],
    ("动力学", "普适"): ["滑移势垒与", "相变能垒"],
    ("动力学", "薄膜"): ["逐层与协同", "相变路径"],
    ("动力学", "跨尺度"): ["有限温度", "形核与扩展"],
    ("力学", "普适"): ["四阶连续介质", "弹性模型"],
    ("力学", "薄膜"): ["HCP 金弹性", "与力学稳定性"],
    ("力学", "跨尺度"): ["HCP/FCC 异质结构", "强韧化机制"],
}
for (row, key), llines in dict_card.items():
    # 卡片常规字重：粗体只给屋顶、板块头、行标签，10 pt 粗体雅黑在成品尺寸下发糊
    add_box(f"卡片-{row}-{key}", DICT_COL_X[key], dict(LROW)[row] + (ROW_H - CARD_H) // 2, COL_W, CARD_H, "FFFFFF",
            CARD_LINE + ":0.75", llines, SIZE_CARD, NAVY, margin="0.1cm", bold=False)

### 行内箭头：只用一种块箭头，不标字、不设图例
for row, y in LROW:
    add_right_arrow(f"箭头-{row}-1", X_GAP1 - 34, y + 67, 68, 36, 18, 20)
    add_right_arrow(f"箭头-{row}-2", X_GAP2 - 34, y + 67, 68, 36, 18, 20)
# 竖向箭头全图同一尺寸（38 × 42），与上下框各隔 12
y_card_bottom = (ROW_H + CARD_H) // 2
for i, (row, y) in enumerate(LROW[:-1]):
    add_down_arrow(f"箭头-跨尺度-下{i + 1}", DICT_COL_X["跨尺度"] + COL_W // 2 - 19, y + y_card_bottom + 12, 38, 42, 18, 19)

### 预期成果
dict_out = {"普适": ["热力学-动力学", "相变机制"], "薄膜": ["薄膜相变物理起源"], "跨尺度": ["势函数与强韧化设计"]}
y_out_arrow = LROW[-1][1] + y_card_bottom + 12
for key, llines in dict_out.items():
    x = DICT_COL_X[key]
    add_down_arrow("箭头-成果-" + key, x + COL_W // 2 - 19, y_out_arrow, 38, 42, 18, 19)
    # flowChartOffpageConnector = 下指五边形；它的文字区本身只到 80% 高度，居中即落在方形部分，
    # 不要再加下边距。两行 9.6 pt 字约 0.9 cm 高，所以框高 1.26 cm（方形部分 1.0 cm）
    add("shape", "成果-" + key, x, y_out_arrow + 53, COL_W, 126, geometry="flowChartOffpageConnector", fill=OUT_FILL,
        line=NAVY + ":0.75", **text_props(llines, SIZE_LABEL, NAVY, bold=False, margin="0.1cm,0.02cm,0.1cm,0.02cm"))

### main
parser = argparse.ArgumentParser(description="生成房屋型 + 3×3 矩阵技术路线图初稿 pptx（officecli）")
parser.add_argument("-output", required=True, help="输出 .pptx")
parser.add_argument("-if_overwrite", action="store_true", help="允许覆盖已有 pptx（只在初稿迭代时用）")
args = parser.parse_args()

path_pptx = Path(args.output).resolve()
if path_pptx.suffix != ".pptx":
    fail("-output 必须是 .pptx：" + str(path_pptx))
if path_pptx.exists() and not args.if_overwrite:
    fail("已存在，可能有用户手改，不覆盖：" + str(path_pptx) + "（初稿迭代加 -if_overwrite）")
build_pptx(path_pptx, LBATCH)
### to here

# test_args = {"output": "house-matrix.pptx", "if_overwrite": False}  # 首次生成
# test_args = {"output": "house-matrix.pptx", "if_overwrite": True}   # 初稿迭代
