#!/usr/bin/env python3
"""生成给 browser_run_code_unsafe(filename=...) 用的 JS：把本地文件以 base64 内嵌，塞进页面的 <input type=file> 并触发 change。

扩展模式（接管日常 Edge）下 setInputFiles 会超时、browser_file_upload 设了文件页面也收不到，
run_code 里又没有 require/import 读本地文件，只能把文件内容编进代码里。
输出 JS 必须放在 Playwright MCP 的允许目录（~/.claude/playwright-output 或工作区）。
run_code 的返回会回显整段代码（几十万字符），结果只看开头的 ### Result。

用法：python make-upload-js.py -file <本地文件> -selector '<input 的 CSS 选择器>' -output <输出 .js>
"""
import argparse
import base64
import json
import mimetypes
import sys
from pathlib import Path


def fail(msg):
    print("❌ ERROR: " + msg)
    raise SystemExit(1)


def generate_js(path_file, selector):
    mime = mimetypes.guess_type(path_file.name)[0] or "application/octet-stream"
    args = json.dumps([base64.b64encode(path_file.read_bytes()).decode(), selector, path_file.name, mime])
    # 页面里重建 File 再用 DataTransfer 赋给 input.files；React 类页面要冒泡的 change 才会响应
    return ('async (page) => { const r = await page.evaluate(([b64, sel, name, mime]) => {'
            ' const bin = atob(b64); const u8 = new Uint8Array(bin.length);'
            ' for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);'
            ' const lin = [...document.querySelectorAll(sel)]; if (!lin.length) return "no input matched";'
            ' const dt = new DataTransfer(); dt.items.add(new File([u8], name, {type: mime}));'
            ' lin[0].files = dt.files; lin[0].dispatchEvent(new Event("change", {bubbles: true}));'
            ' return lin.length + " input(s), sent " + u8.length + " bytes to the first"; }, ' + args + ');'
            ' await page.waitForTimeout(2500); return r; }')


### main
parser = argparse.ArgumentParser()
parser.add_argument("-file", required=True)
parser.add_argument("-selector", required=True)
parser.add_argument("-output", required=True)
args = parser.parse_args()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

path_file = Path(args.file).expanduser().resolve()
if not path_file.is_file():
    fail("文件不存在：" + str(path_file))
path_out = Path(args.output).expanduser().resolve()
path_out.write_text(generate_js(path_file, args.selector), encoding="utf-8")
print("✅ " + str(path_out) + "（" + str(path_out.stat().st_size) + " 字节）")
### to here

# test_args = {"-file": "assets/discord-theme/icon.png", "-selector": 'input[type=file][aria-label="更改服务器图标"]', "-output": "~/.claude/playwright-output/upload.js"}
