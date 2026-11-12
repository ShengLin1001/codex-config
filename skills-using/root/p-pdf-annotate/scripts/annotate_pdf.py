#!/usr/bin/env python3
"""给学术 PDF 加高亮 + 批注 + 首页阅读便签，另存新文件（原文件不动）。

spec（JSON）：
{
  "author": "claude",                       # 批注作者，同时用来防止在已标注版上重复叠加
  "summary": "首页便签正文，可多行",
  "summary_page": 1,                        # 出版商加了封面页时改成正文首页
  "note_place": "inline",                   # inline：批注挂在高亮上（Zotero/Acrobat）；margin：批注放页边便签（Edge 不挡字）
  "marks": [
    {"page": 1, "kind": "vocab", "start": "ab initio", "note": "..."},
    {"page": 2, "kind": "key", "start": "A more direct approach", "end": "melting point.", "note": "..."},
    {"page": 1, "kind": "vocab", "start": "coexistence", "n": 2, "note": "第 2 次出现处"}
  ]
}
kind：key / number / definition / caution / figure / vocab 用高亮，grammar 用下划线，颜色见 dict_color。
page 从 1 起；start/end 是锚点（几个连续词），高亮从 start 第一个词到 end 最后一个词；
end 省略时只高亮 start 本身；n 取第 n 次出现的 start（默认 1）。

用法：
  python annotate_pdf.py -input paper.pdf -dump > paper.txt      # 匹配器看到的文字，锚点从这里抄
  python annotate_pdf.py -input paper.pdf -spec x.annot.json -output annotated/paper.pdf [-render_dir dir]

退出码：全部标注落位为 0；有标注没找到（输出仍会保存）或前提不满足为 1。
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

import fitz

dict_color = {
    "key": (1.00, 0.85, 0.10),         # 黄：核心结论、支撑我们论点的原文
    "number": (0.20, 0.80, 0.30),      # 绿：数字、参数、可对照的量级
    "definition": (0.20, 0.50, 1.00),  # 蓝：定义、方法原理
    "caution": (1.00, 0.20, 0.20),     # 红：限定条件、局限、与我们做法不同处
    "figure": (1.00, 0.55, 0.00),      # 橙：图注开头，批注写整张图的解读
    "vocab": (0.70, 0.40, 1.00),       # 紫高亮：生词注释
    "grammar": (0.55, 0.15, 0.85),     # 紫下划线：语法注释（下划线才不会和重点高亮混淆）
}
dict_label = {
    "key": "核心结论", "number": "数字/参数", "definition": "定义/方法", "caution": "局限/差异",
    "figure": "图解读", "vocab": "生词", "grammar": "语法",
}
LEGEND = "【颜色】黄=核心结论 绿=数字 蓝=定义 红=局限 橙=图解读 紫=生词 紫下划线=语法"
OPACITY = 0.45
LEGEND_H = 13.0     # 图例条高度（pt），页边空白不够这么高就不画
LEGEND_FONT = 7.5
NOTE_ICON = 16.0    # margin 模式便签图标边长（pt）；PyMuPDF update() 会把 Text 图标固定成 16，设小了没用
MARGIN_PAD = 4.0    # 图标离页面左右边缘的距离（pt）
NUM_W = 12.0        # 编号小字的框宽（pt）
lnote_place = ["inline", "margin"]
MAX_SPAN_WORD = 150  # 超过多半是 end 锚点匹配到了远处的同名短语


def fail(msg):
    print("❌ ERROR: " + msg)
    raise SystemExit(1)


def warn(msg):
    print("⚠️  " + msg)


def normalize_word(word):
    # NFKC 把连字 ﬁ/ﬂ 拆回 fi/fl；句尾句点要去掉，否则 "neighbors." 和 "neighbors" 对不上
    token = unicodedata.normalize("NFKC", word).lower()
    token = re.sub(r"[^0-9a-zͰ-Ͽ+=.±]", "", token)
    return token.strip(".=+")


def tokenize(text):
    return [normalize_word(token) for token in text.split() if normalize_word(token)]


def find_sequence(lseq, ltoken, start=0):
    for i in range(start, len(lseq) - len(ltoken) + 1):
        if lseq[i:i + len(ltoken)] == ltoken:
            return i
    return -1


def get_span(page, start_text, end_text, n_occur):
    """返回 (按行切分的矩形列表, 高亮下的原文, 词数)；锚点找不到抛 LookupError。"""
    # 纯标点（单独的 "=" "("）归一后为空，会打断连续匹配，先剔掉
    lword = [word for word in page.get_text("words") if normalize_word(word[4])]
    lseq = [normalize_word(word[4]) for word in lword]
    ltoken_start = tokenize(start_text)
    i_start = -1
    for _ in range(n_occur):
        i_start = find_sequence(lseq, ltoken_start, i_start + 1)
        if i_start < 0:
            raise LookupError("start 未找到（第 %d 次）: %s" % (n_occur, start_text))
    i_end = i_start + len(ltoken_start) - 1
    if end_text:
        ltoken_end = tokenize(end_text)
        i_end = find_sequence(lseq, ltoken_end, i_start)
        if i_end < 0:
            raise LookupError("end 未找到: " + end_text)
        i_end += len(ltoken_end) - 1
    # 老文献的词序未必是阅读序（上一行的词会混进切片），按起止词的 y 范围裁掉；
    # 副作用：跨栏的 span 会被裁空，所以一条标注不能跨栏
    y_top = lword[i_start][1] - 3.0
    y_bottom = lword[i_end][3] + 3.0
    lrect = []
    ltext = []
    key_cur = None
    for word in lword[i_start:i_end + 1]:
        if word[1] < y_top or word[3] > y_bottom:
            continue
        ltext.append(word[4])
        key = (word[5], word[6])  # (block, line)：一行一个矩形，跨行高亮不糊成一大块
        if key != key_cur:
            lrect.append(fitz.Rect(word[:4]))
            key_cur = key
        else:
            lrect[-1] |= fitz.Rect(word[:4])
    if not lrect:
        raise LookupError("span 被裁空（多半跨栏了）: " + start_text)
    return lrect, " ".join(ltext), i_end - i_start + 1


def check_spec(dict_spec, n_page):
    lmark = dict_spec.get("marks", [])
    if not isinstance(lmark, list):
        fail("spec.marks 必须是列表")
    if dict_spec.get("note_place", "inline") not in lnote_place:
        fail("spec.note_place 必须是 %s 之一" % "/".join(lnote_place))
    summary_page = dict_spec.get("summary_page", 1)
    if not isinstance(summary_page, int) or not 1 <= summary_page <= n_page:
        fail("spec.summary_page 必须是 1-%d 的整数" % n_page)
    for i, mark in enumerate(lmark):
        tag = "marks[%d]" % i
        if not isinstance(mark.get("page"), int) or not 1 <= mark["page"] <= n_page:
            fail("%s.page 必须是 1-%d 的整数" % (tag, n_page))
        if mark.get("kind") not in dict_color:
            fail("%s.kind 必须是 %s 之一" % (tag, "/".join(dict_color)))
        if not tokenize(mark.get("start", "")):
            fail(tag + ".start 为空")
        if not mark.get("note"):
            fail(tag + ".note 为空")
    return lmark


def check_not_annotated(doc, author):
    # 在已标注版上再跑会叠出重复高亮；改标注应改 spec 后从原版重跑
    n_own = sum(1 for page in doc for annot in page.annots() if annot.info.get("title") == author)
    if n_own:
        fail("输入里已有 %d 个作者为 %s 的批注，请用未标注的原版作输入" % (n_own, author))


def add_summary(page, text, author):
    annot = page.add_text_annot(fitz.Point(page.rect.width - 26, 34), LEGEND + "\n" + text, icon="Note")
    annot.set_info(title=author)
    annot.update()


def get_legend_y(page):
    """页顶或页底空白里放得下图例条时返回条的上沿 y，否则 None。"""
    lrect = [fitz.Rect(block[:4]) for block in page.get_text("blocks")]
    area_page = page.rect.get_area()
    # 整页白底之类的大矩形不算占位
    lrect += [d["rect"] for d in page.get_drawings() if d["rect"].get_area() < 0.9 * area_page]
    lrect = [rect for rect in lrect if not rect.is_empty]
    if not lrect:
        return None
    y_top = min(rect.y0 for rect in lrect)
    y_bottom = max(rect.y1 for rect in lrect)
    if y_top >= LEGEND_H + 4:
        return (y_top - LEGEND_H) / 2
    if page.rect.height - y_bottom >= LEGEND_H + 4:
        return y_bottom + (page.rect.height - y_bottom - LEGEND_H) / 2
    return None


def add_legend(page, author):
    """在页边空白画一排图例：每格的底色/下划线与正文标注一致。放不下返回 False。"""
    y0 = get_legend_y(page)
    if y0 is None:
        return False
    x = 40.0
    for kind, label in [("", "图例")] + list(dict_label.items()):
        # CJK 字宽约等于字号，ASCII 约半个字号
        width = sum(LEGEND_FONT if ord(char) > 127 else LEGEND_FONT * 0.55 for char in label) + 8
        rect = fitz.Rect(x, y0, x + width, y0 + LEGEND_H)
        if kind == "grammar":
            text = '<span style="color:#8c26d9;text-decoration:underline">' + label + "</span>"
            fill = None
        else:
            text = label
            # 混白模拟 45% 透明的高亮；FreeText 的底色是不透明的
            fill = tuple(1 - OPACITY * (1 - c) for c in dict_color[kind]) if kind else None
        annot = page.add_freetext_annot(rect, text, richtext=True, fill_color=fill, border_width=0,
                                        # nowrap：字宽是估的，宁可溢出也别折行（折行后第二行被裁掉）
                                        style="font-size:%gpt;line-height:1.6;white-space:nowrap;"
                                              "text-align:center;" % LEGEND_FONT)
        annot.set_info(title=author)
        annot.update()
        x += width + 4
    return True


def add_mark(page, lrect, kind, note, author):
    lquad = [rect.quad for rect in lrect]
    if kind == "grammar":
        annot = page.add_underline_annot(quads=lquad)
    else:
        annot = page.add_highlight_annot(quads=lquad)
        annot.set_opacity(OPACITY)
    annot.set_colors(stroke=dict_color[kind])
    annot.set_info(title=author, content=note)
    annot.update()


def add_margin_notes(page, lnote, author):
    """margin 模式：便签图标放在标注首行同高的页边，同侧按 y 排序、重叠就往下推。

    lnote 元素为 (首行矩形, kind, 批注正文)。
    """
    dict_side = {"left": [], "right": []}
    # 编号按阅读顺序（先栏后行）给，读者顺着正文就能找到下一号
    lnote = sorted(lnote, key=lambda item: (item[0].x0 >= page.rect.width / 2, item[0].y0))
    for num, (rect, kind, note) in enumerate(lnote, start=1):
        # 通栏的行（摘要、图注）按起点离哪边近放哪边，左右分摊图标
        side = "left" if rect.x0 < page.rect.width / 2 else "right"
        dict_side[side].append((rect, kind, note, num))
    for side, litem in dict_side.items():
        x = MARGIN_PAD if side == "left" else page.rect.width - MARGIN_PAD - NOTE_ICON
        y_free = 0.0
        for rect, kind, note, num in sorted(litem, key=lambda item: item[0].y0):
            y = max(rect.y0, y_free)
            annot = page.add_text_annot(fitz.Point(x, y), "[%d] " % num + note, icon="Comment")
            annot.set_rect(fitz.Rect(x, y, x + NOTE_ICON, y + NOTE_ICON))
            annot.set_colors(stroke=dict_color[kind])
            annot.set_info(title=author)
            annot.update()
            # 编号放在图标靠正文一侧，和高亮左上角的同号小字对应
            x_num = x + NOTE_ICON if side == "left" else x - NUM_W
            add_number(page, fitz.Rect(x_num, y, x_num + NUM_W, y + NOTE_ICON), num, kind, author, 7)
            add_number(page, fitz.Rect(rect.x0 - 1, rect.y0 - 5, rect.x0 - 1 + NUM_W, rect.y0 + 1),
                       num, kind, author, 5)
            y_free = y + NOTE_ICON + 1


def add_number(page, rect, num, kind, author, size):
    r, g, b = (int(255 * c * 0.75) for c in dict_color[kind])  # 压暗一点，小字才看得清
    text = '<span style="color:#%02x%02x%02x;font-weight:bold">%d</span>' % (r, g, b, num)
    annot = page.add_freetext_annot(rect, text, richtext=True, border_width=0,
                                    style="font-size:%gpt;line-height:1;white-space:nowrap;" % size)
    annot.set_info(title=author)
    annot.update()


def dump_text(doc):
    for page in doc:
        print("================ 📍 p%d" % (page.number + 1))
        print(page.get_text())


def render_pages(doc, lpage, path_dir):
    path_dir.mkdir(parents=True, exist_ok=True)
    for page_no in sorted(set(lpage)):
        path_png = path_dir / ("p%02d.png" % page_no)
        doc[page_no - 1].get_pixmap(dpi=110, annots=True).save(path_png)
        print("  🖼️  " + str(path_png))


def annotate(doc, lmark, summary, summary_page, author, note_place):
    """逐条落位，返回 (成功页码列表, 失败描述列表)。"""
    dict_margin = {}  # 页码 → [(首行矩形, kind, 批注)]，margin 模式最后统一排位
    lpage_ok = [summary_page]
    if summary:
        add_summary(doc[summary_page - 1], summary, author)
    if not add_legend(doc[summary_page - 1], author):
        warn("p%d 页边空白放不下图例，只写在首页便签里" % summary_page)
    lfailed = []
    for mark in lmark:
        page = doc[mark["page"] - 1]  # 先绑定变量：临时 Page 被回收后 annot 会失效
        label = "p%d [%s] %s" % (mark["page"], mark["kind"], mark["start"][:40])
        try:
            lrect, text, n_word = get_span(page, mark["start"], mark.get("end", ""), mark.get("n", 1))
        except LookupError as exc:
            lfailed.append("%s → %s" % (label, exc))
            print("  ❌ " + lfailed[-1])
            continue
        if n_word > MAX_SPAN_WORD:
            lfailed.append("%s → 跨度 %d 词，疑似 end 锚点错配" % (label, n_word))
            print("  ❌ " + lfailed[-1])
            continue
        shown = text if len(text) <= 90 else text[:55] + " … " + text[-30:]
        if note_place == "margin":
            # 高亮不带正文，阅读器就不会在高亮开头画评论图标盖住上一行
            add_mark(page, lrect, mark["kind"], "", author)
            head = text if len(text) <= 40 else text[:40] + "…"
            dict_margin.setdefault(mark["page"], []).append(
                (lrect[0], mark["kind"], "「" + head + "」\n" + mark["note"]))
        else:
            add_mark(page, lrect, mark["kind"], mark["note"], author)
        lpage_ok.append(mark["page"])
        print("  ✅ %s | %d 行 | %s" % (label, len(lrect), shown))
    for page_no, lnote in dict_margin.items():
        add_margin_notes(doc[page_no - 1], lnote, author)
    return lpage_ok, lfailed


def main():
    parser = argparse.ArgumentParser(description="给学术 PDF 加高亮批注，另存新文件")
    parser.add_argument("-input", required=True, help="原版 PDF")
    parser.add_argument("-spec", help="标注 spec JSON")
    parser.add_argument("-output", help="输出 PDF，不能与 -input 相同")
    parser.add_argument("-dump", action="store_true", help="只打印逐页文字，用来抄锚点")
    parser.add_argument("-render_dir", help="把有标注的页渲染成 PNG 放到这里，供目视核对")
    args = parser.parse_args()

    ### check
    path_in = Path(args.input).resolve()
    if not path_in.is_file():
        fail("PDF 不存在: " + str(path_in))
    doc = fitz.open(path_in)
    if args.dump:
        dump_text(doc)
        return
    if not args.spec or not args.output:
        fail("标注模式需要 -spec 和 -output")
    path_spec = Path(args.spec).resolve()
    path_out = Path(args.output).resolve()
    if path_out == path_in:
        fail("-output 不能覆盖原文件")
    dict_spec = json.loads(path_spec.read_text(encoding="utf-8"))
    author = dict_spec.get("author", "claude")
    lmark = check_spec(dict_spec, doc.page_count)
    check_not_annotated(doc, author)
    ### to here

    ### annotate
    print("================ 📁 " + path_in.name)
    summary = dict_spec.get("summary", "")
    lpage_ok, lfailed = annotate(doc, lmark, summary, dict_spec.get("summary_page", 1), author,
                                 dict_spec.get("note_place", "inline"))
    path_out.parent.mkdir(parents=True, exist_ok=True)
    doc.subset_fonts()  # 图例的中文会嵌入整套 CJK 回退字体（约 3.6 MB），子集化后只剩几十 KB
    doc.save(path_out, garbage=3, deflate=True)
    if args.render_dir:
        render_pages(doc, lpage_ok, Path(args.render_dir).resolve())
    doc.close()
    ### to here

    print("================ 📊 %d/%d 处高亮落位%s -> %s" % (
        len(lmark) - len(lfailed), len(lmark), "，另加 1 条首页便签" if summary else "", path_out))
    if lfailed:
        print("没落位的（改锚点后从原版重跑）：")
        for item in lfailed:
            print("  - " + item)
        raise SystemExit(1)
    print("🎉 完成，原文件未改动")


if __name__ == "__main__":
    main()
