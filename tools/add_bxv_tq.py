#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「可作答」考古題面板（bxv-topic-qa.js）掛到估價的整理頁上。

做法：在檔尾插一段 mount script，用 JS 依錨點把 <div class="bxv-tq"> 建出來，
再載入面板本體——不用字串切位置（v525 折舊圖那次就是切壞 HTML）。
mount script 一定要排在面板本體**前面**，否則面板開機時還看不到那個 div。

⚠️ 題號一律先對 bxv-quiz-data.js 驗過才寫入。
⚠️ 跨科題號不可混入：《地價調查估計規則專欄》第九節寫的 102-8、103-18、103-6、101-9
   是**土地法科**的題號，估價題庫裡同一個號碼是完全不同的題（102-8 是 DCF 證券化、
   103-6 是路沖屬何種因素）。那四個不掛，頁面上也已經標明是跨科連結。

可重複執行。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "bxv-quiz-data.js"

# 頁面 → [(掛在哪個錨點, 面板標題, 題號 or None＝用章)]
PLAN = {
    "估價_營造施工費四法.html": [
        ("s4", "營造或施工費四法（C1）",
         "99-7,99-36,101-4,101-12,102-33,104-19,106-14,106-40,108-13,109-18,110-9,111-7,112-12,114-18", None),
    ],
    "估價_地價調查估計規則專欄.html": [
        ("s8", "地價調查估計規則", "106-21,105-13,103-1,103-23", None),
    ],
    "估價_租金估計攻略表.html": [
        (None, "租金估計（F1 全章）", None, "F1"),
    ],
}

MOUNT_RE = re.compile(r'<script id="bxvtq-mount">.*?</script>\n?', re.S)
LOAD_RE = re.compile(r'<script src="bxv-topic-qa\.js"></script>\n?', re.S)


def main():
    src = DATA.read_text(encoding="utf-8")
    i = src.find("items:[")
    items = json.loads("[" + src[i + len("items:["):src.find("\n]", i)] + "]")
    have = {f'{a["y"]}-{a["n"]}': a for a in items}

    for fn, panels in PLAN.items():
        p = ROOT / fn
        s = p.read_text(encoding="utf-8")
        before = len(s)
        s = MOUNT_RE.sub("", s)
        s = LOAD_RE.sub("", s)

        mounts = []
        for anchor, title, qs, chs in panels:
            if qs:
                miss = [k for k in qs.split(",") if k not in have]
                if miss:
                    sys.exit(f"{fn}：題庫找不到 {miss}")
                n = len(qs.split(","))
                print(f"  {fn} → {title}：{n} 題（已逐題對過題庫）")
            else:
                n = len([a for a in items if a["ch"] == chs])
                print(f"  {fn} → {title}：整章 {chs}，{n} 題")
            mounts.append({"a": anchor, "t": title, "q": qs, "c": chs})

        payload = json.dumps(mounts, ensure_ascii=False, separators=(",", ":"))
        mount = ('<script id="bxvtq-mount">\n'
                 "(function(){var M=" + payload + ";\n"
                 "M.forEach(function(m){var host=m.a?document.getElementById(m.a):null;\n"
                 "  if(!host)host=document.querySelector('.wrap')||document.body;\n"
                 "  var d=document.createElement('div');d.className='bxv-tq';\n"
                 "  d.setAttribute('data-title',m.t);\n"
                 "  if(m.q)d.setAttribute('data-qs',m.q);else d.setAttribute('data-chs',m.c);\n"
                 "  host.appendChild(d)});\n"
                 "})();\n</script>")
        block = mount + '\n<script src="bxv-topic-qa.js"></script>\n'

        if "</body>" in s:
            s = s.replace("</body>", block + "</body>", 1)
        else:
            s = s.rstrip("\n") + "\n" + block
        p.write_text(s, encoding="utf-8")
        print(f"  寫入 {fn}：{before} → {len(s)} 字元\n")


if __name__ == "__main__":
    main()
