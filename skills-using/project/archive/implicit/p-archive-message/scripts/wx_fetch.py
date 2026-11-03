#!/usr/bin/env python3
"""抓取微信公众号文章，输出标题、公众号名、正文里的 DOI 和正文开头。

WebFetch 的请求特征会被微信判成爬虫，返回"环境异常"验证页；同一台 VPS 用浏览器 UA 直接请求就能拿到全文。
只用标准库，VPS 上直接 python3 跑即可。

用法：python3 <p-archive-message skill 目录>/scripts/wx_fetch.py -url "<完整公众号链接>" [-max_chars 3000]
"""
import argparse
import html
import re
import sys
import urllib.request

UA_BROWSER = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
RE_DOI = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>，。；、）)\]]+")


def fail(msg):
    print(f"❌ ERROR: {msg}")
    raise SystemExit(1)


def get_html(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA_BROWSER})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as exc:  # 网络错误统一给出可读提示，bot 据此标 待补
        fail(f"请求失败：{exc}")


def get_meta(page, prop):
    m = re.search(r'<meta property="' + prop + r'" content="([^"]*)"', page)
    return html.unescape(m.group(1)).strip() if m else ""


def get_account(page):
    m = re.search(r'var nickname = htmlDecode\("([^"]*)"\)', page) or \
        re.search(r'id="js_name">\s*([^<]+)<', page)
    return html.unescape(m.group(1)).strip() if m else ""


def get_body_text(page):
    m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', page, re.S)
    body = m.group(1) if m else page
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    text = re.sub(r"<br\s*/?>|</p>|</section>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\n\s*\n+", "\n", re.sub(r"[ \t ]+", " ", text)).strip()


def check_article_page(page):
    # 验证页、"参数错误"页都没有正文容器 js_content
    if 'id="js_content"' not in page:
        reason = "环境异常验证页" if "环境异常" in page else "非文章页（链接参数不全或文章已删除）"
        fail("微信返回了" + reason + "，请确认传入的是完整 URL")


### main
parser = argparse.ArgumentParser(description="抓取微信公众号文章的标题、公众号名、DOI 和正文")
parser.add_argument("-url", required=True, help="完整公众号链接，保留 sn/chksm 等全部参数")
parser.add_argument("-max_chars", type=int, default=3000, help="正文最多输出的字符数")
args = parser.parse_args()
sys.stdout.reconfigure(encoding="utf-8")

if "mp.weixin.qq.com" not in args.url:
    fail("不是公众号链接：" + args.url)
page = get_html(args.url)
check_article_page(page)
text = get_body_text(page)
ldoi = list(dict.fromkeys(d.rstrip(".") for d in RE_DOI.findall(text)))

print("================ 📊 公众号文章")
print("标题：" + (get_meta(page, "og:title") or "待补"))
print("公众号：" + (get_account(page) or "待补"))
print("DOI：" + ("；".join(ldoi) if ldoi else "正文未出现"))
print("================ 📄 正文（前 " + str(args.max_chars) + " 字）")
print(text[:args.max_chars])
### to here
