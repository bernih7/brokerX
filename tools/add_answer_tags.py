#!/usr/bin/env python3
"""2026-10-31 使用者：「刷題結果於錯誤的時候要顯示我選的、正確的，不然不好辨識」。
在各刷題頁選項按鈕上加文字標籤（CSS ::after），不改作答邏輯。可重跑（先移除舊 #ans-tag-css）。"""
import re, sys
from pathlib import Path
R = Path(__file__).resolve().parent.parent
BASE = ("{margin-left:8px;display:inline-block;font-size:12px;font-weight:700;line-height:1.5;"
        "padding:0 6px;border-radius:4px;white-space:nowrap;vertical-align:middle;border:1px solid currentColor}")
G = "var(--green,#2F6B45)"; Rd = "var(--red,var(--stamp,#A84030))"
def css(ok_sel, ng_sel, ok_txt="✓ 正確答案", extra=""):
    return (f'<style id="ans-tag-css">{ok_sel}::after{{content:"{ok_txt}";color:{G}}}{ok_sel}::after{BASE}'
            f'{ng_sel}::after{{content:"✗ 你選的";color:{Rd}}}{ng_sel}::after{BASE}{extra}</style>')
PAGES = {}
for f in sorted(R.glob("估價刷題練習_*.html")):
    PAGES[f.name] = css(".opt.correct-answer", ".opt.wrong-selected")
for n in ["估價_綜合模擬卷一","估價_綜合模擬卷二","估價_綜合模擬卷三","估價_綜合模擬卷四","估價_綜合模擬卷五","估價_自編補強卷"]:
    PAGES[n+".html"] = css(".opt.correct-ans", ".opt.wrong-ans")
PAGES["估價_來勝模擬試題一.html"] = css(".opt.ok", ".opt.bad")
PAGES["估價_診斷卷一.html"] = css(".opt.rv", ".opt.ng",
    extra=f'.opt.ok::after{{content:"✓ 你選的・正確";color:{G}}}.opt.ok::after{BASE}')
fail = []; out = {}
for name, block in PAGES.items():
    p = R / name; s = p.read_text(encoding="utf-8")
    s = re.sub(r'<style id="ans-tag-css">.*?</style>', '', s, flags=re.S)
    if s.count("</head>") != 1: fail.append(f"{name}: </head> {s.count('</head>')}"); continue
    out[p] = s.replace("</head>", block + "</head>")
if fail: sys.exit("\n".join(fail))
for p, s in out.items(): p.write_text(s, encoding="utf-8")
print("寫入", len(out), "頁")
