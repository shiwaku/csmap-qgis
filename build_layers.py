"""csmap-on-maplibre のレイヤー定義から load_csmap.py の CS_LAYERS を作り直す。

    python build_layers.py            # GitHub の main から取得
    python build_layers.py ../csmap-on-maplibre   # ローカルのチェックアウトから取得

レイヤーの順序と表示名は src/layers.ts、タイルURLと出典は public/style/pale.json による。
zmax はソースの maxzoom → csmap-tiles の datasets.json → ZMAX_FALLBACK の順で決める。
"""

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

VIEWER_RAW = "https://raw.githubusercontent.com/shiwaku/csmap-on-maplibre/main/"
CATALOG = "https://raw.githubusercontent.com/shiwaku/csmap-tiles/main/datasets.json"
TARGET = Path(__file__).with_name("load_csmap.py")

# maxzoom を持たない外部配信分。実タイルの取得確認による（2026-09-25）
ZMAX_FALLBACK = {
    "nagano-cs": 18, "ehime-cs": 18, "kochi-cs": 18, "hyogo-cs": 18, "tochigi-cs": 18,
    "shiga-cs": 18, "gifu-cs": 18, "tottori-cs": 18, "hiroshima-cs": 17, "okayama-cs": 17,
    "fukushima-cs": 17, "kumamoto-oita-cs": 17, "noto-cs": 17,
}
SHIMA = {"01": "大島", "02": "利島・新島・式根島・神津島", "03": "三宅島",
         "04": "御蔵島", "05": "八丈島", "06": "青ヶ島"}


def read(src, path):
    if src:
        return (Path(src) / path).read_text(encoding="utf-8")
    with urllib.request.urlopen(VIEWER_RAW + path, timeout=30) as r:
        return r.read().decode("utf-8")


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    sources = json.loads(read(src, "public/style/pale.json"))["sources"]
    ts = read(src, "src/layers.ts").split("export const CS_LAYERS")[1].split("];")[0]
    with urllib.request.urlopen(CATALOG, timeout=30) as r:
        catalog = {d["url"]: d["maxzoom"] for d in json.load(r)}

    rows = []
    for m in re.finditer(r'\{\s*ids:\s*\[(.*?)\],\s*name:\s*"(.*?)"', ts, re.S):
        for lid in re.findall(r'"([^"]+)"', m.group(1)):
            s = sources[lid]
            url = s["tiles"][0]
            if s.get("scheme") == "tms":
                url = url.replace("{y}", "{-y}")
            zmax = s.get("maxzoom") or catalog.get(url) or ZMAX_FALLBACK.get(lid)
            if zmax is None:
                sys.exit(f"zmax 不明: {lid}（ZMAX_FALLBACK に追加すること）")
            att_html = s.get("attribution", "")
            att = html.unescape(re.sub("<[^>]+>", "", att_html)).strip()
            href = (re.findall(r"href='([^']*)'", att_html) or [""])[0]
            name = m.group(2)
            if lid.startswith("tokyo-shima-"):
                name = name.replace("(島しょ地域)", f"(島しょ地域・{SHIMA[lid[12:14]]})")
            rows.append((lid, name, url, zmax, att, href))

    body = "".join(f"    {r!r},\n" for r in rows)
    code = TARGET.read_text(encoding="utf-8")
    code = re.sub(r"(CS_LAYERS = \[\n).*?(\])", lambda mm: mm.group(1) + body + mm.group(2),
                  code, count=1, flags=re.S)
    TARGET.write_text(code, encoding="utf-8")
    print(f"{len(rows)} レイヤーを {TARGET.name} に書き込みました")


if __name__ == "__main__":
    main()
