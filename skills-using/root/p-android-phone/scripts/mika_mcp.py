"""Minimal Streamable-HTTP MCP client for Mika over adb forward. Token read from phone, never printed.

Usage: python mika_mcp.py tools
       python mika_mcp.py call <tool> '<json args>'
"""
import json
import subprocess
import sys
import urllib.request

ADB = "D:/software/platform-tools/adb.exe"
URL = "http://127.0.0.1:8765/mcp"


def get_token():
    out = subprocess.run([ADB, "shell", "cat", "/sdcard/Android/data/com.wangzan101.mika/files/mcp-usb.json"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["token"]


class Mika:
    def __init__(self):
        self.headers = {"Authorization": "Bearer " + get_token(), "Content-Type": "application/json",
                        "Accept": "application/json, text/event-stream"}
        self.nid = 0
        self.post("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "cc", "version": "0"}})
        self.post("notifications/initialized", None, notify=True)

    def post(self, method, params, notify=False):
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            self.nid += 1
            msg["id"] = self.nid
        req = urllib.request.Request(URL, data=json.dumps(msg).encode(), headers=self.headers)
        with urllib.request.urlopen(req, timeout=600) as res:
            sid = res.headers.get("Mcp-Session-Id")
            if sid:
                self.headers["Mcp-Session-Id"] = sid
            body = res.read().decode("utf-8")
        if notify or not body.strip():
            return None
        # SSE 响应取最后一个 data 行；普通 JSON 直接解析
        if body.lstrip().startswith("{"):
            return json.loads(body)
        ldata = [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
        return json.loads(ldata[-1])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    m = Mika()
    if sys.argv[1] == "tools":
        for t in m.post("tools/list", {})["result"]["tools"]:
            print("================", t["name"])
            print("  ", t.get("description", "")[:400].replace("\n", " "))
            print("   args:", json.dumps(t["inputSchema"].get("properties", {}), ensure_ascii=False)[:400])
    else:
        res = m.post("tools/call", {"name": sys.argv[2], "arguments": json.loads(sys.argv[3])})
        for c in res.get("result", {}).get("content", []):
            print(c.get("text", "[" + c.get("type", "?") + "]"))
        if "error" in res:
            print("❌", res["error"])


if __name__ == "__main__":
    main()
