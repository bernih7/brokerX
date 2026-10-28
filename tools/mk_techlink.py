#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《估價_技術規則專欄》：把內文裡的題號（104-27、105-4…）變成可點的連結，
並在八個專題區塊（#t1～#t8）各加一行「▶ 練這 N 題」。

安全規則（這頁同時有條號與題號，弄錯會把 §118-1 連成「118年第1題」）：
  * 只在「文字節點」上取代，不碰標籤內部。
  * 題號樣式必須是 99～119 年 ＋「-」＋ 1～2 位數字。
  * 前面是 § 或數字或「-」一律跳過（§101-1、§118-1、§122-1、2026-10-22）。
  * 取代前先確認該題真的在 bxv-quiz-data.js 裡，找不到就不碰。
可重複執行：每次先把舊的連結還原成純文字，再重做。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "估價_技術規則專欄.html"
DATA = ROOT / "bxv-quiz-data.js"
CARD = "估價_考題小卡.html"
DRILL = "估價解析版練習.html"

PAT = re.compile(r"(?<![0-9§\-])(9[0-9]|1[01][0-9])-([0-9]{1,2})(?![0-9\-])")

CSS = """<style id="qlk-css">
/* 內文裡的題號：不用膠囊，膠囊在句子中間太吵；只加色與虛線底 */
a.qlk{color:var(--pri,#2F5D50);font-weight:700;text-decoration:none;
  border-bottom:1px dotted currentColor;font-variant-numeric:tabular-nums;white-space:nowrap}
a.qlk:hover{border-bottom-style:solid}
.qlk-bar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;min-width:0;
  margin:14px 0 2px;padding-top:9px;border-top:1px dashed var(--line,#ddd);
  font-size:.8rem;color:var(--muted,#777)}
.qlk-bar b{color:var(--ink,#25302C)}
.qlk-all{text-decoration:none;font-weight:800;font-size:.75rem;padding:2px 10px;
  border-radius:999px;background:var(--pri,#2F5D50);color:#fff;white-space:nowrap}
</style>"""


def text_spans(s):
    """回傳所有「不在標籤內」的區間。"""
    out, pos = [], 0
    for m in re.finditer(r"<[^>]*>", s):
        if m.start() > pos:
            out.append((pos, m.start()))
        pos = m.end()
    if pos < len(s):
        out.append((pos, len(s)))
    return out


def main():
    src = DATA.read_text(encoding="utf-8")
    i = src.find("items:[")
    items = json.loads("[" + src[i + len("items:["):src.find("\n]", i)] + "]")
    have = {(a["y"], a["n"]): a for a in items}

    s = PAGE.read_text(encoding="utf-8")
    before = len(s)

    # ── 可重複執行：先把上一次的東西清掉 ──
    s = re.sub(r'<a class="qlk" href="[^"]*">([^<]*)</a>', r"\1", s)
    s = re.sub(r'<style id="qlk-css">.*?</style>\n?', "", s, flags=re.S)
    s = re.sub(r'<script id="qlk-js">.*?</script>\n?', "", s, flags=re.S)

    # ── 1. 內文題號 → 連結（由後往前取代，位移才不會跑掉）──
    jobs = []
    for a, b in text_spans(s):
        for m in PAT.finditer(s[a:b]):
            y, n = int(m.group(1)), int(m.group(2))
            q = have.get((y, n))
            if q is None:
                continue
            jobs.append((a + m.start(), a + m.end(), m.group(0), q["id"]))
    for st, en, tok, qid in sorted(jobs, reverse=True):
        s = s[:st] + f'<a class="qlk" href="{CARD}#{qid}">{tok}</a>' + s[en:]
    print(f"內文題號連結：{len(jobs)} 處，{len({j[2] for j in jobs})} 題")

    # ── 2. 八個專題各算一次「練整批」──
    groups = {}
    for m in re.finditer(r'<details class="tp" id="(t[0-9])"', s):
        gid = m.group(1)
        nxt = re.search(r'<details class="tp" id="t[0-9]"', s[m.end():])
        chunk = s[m.end(): m.end() + (nxt.start() if nxt else len(s))]
        seen, order = set(), []
        for mm in re.finditer(r'<a class="qlk" href="[^"]*">([^<]*)</a>', chunk):
            if mm.group(1) not in seen:
                seen.add(mm.group(1))
                order.append(mm.group(1))
        title = re.search(r'class="tp-t">([^<]*)<', chunk)
        groups[gid] = {"n": order, "t": title.group(1) if title else gid}
    for gid, g in groups.items():
        print(f"   {gid} {g['t']:<12s} {len(g['n']):2d} 題")
    if not groups:
        sys.exit("找不到 <details class=\"tp\" id=\"tN\">")

    payload = json.dumps({k: v["n"] for k, v in groups.items() if v["n"]},
                         ensure_ascii=False, separators=(",", ":"))
    script = (
        '<script id="qlk-js">\n'
        "(function(){var G=" + payload + ";\n"
        "Object.keys(G).forEach(function(id){var d=document.getElementById(id);if(!d)return;\n"
        '  var box=d.querySelector(".tp-b")||d;var ns=G[id];\n'
        "  var bar=document.createElement('div');bar.className='qlk-bar';\n"
        "  bar.innerHTML='🖋 這一區的條文考過 <b>'+ns.length+'</b> 題'+\n"
        '    \'<a class="qlk-all" href="' + DRILL + "#q='+ns.join(',')+'\">▶ 練這 '+ns.length+' 題</a>';\n"
        "  box.appendChild(bar)});\n"
        "})();\n</script>")

    if "</body>" in s:
        s = s.replace("</body>", CSS + "\n" + script + "\n</body>", 1)
    else:
        s = s.rstrip("\n") + "\n\n" + CSS + "\n" + script + "\n"

    PAGE.write_text(s, encoding="utf-8")
    print(f"寫入 {PAGE.name}：{before} → {len(s)} 字元")


if __name__ == "__main__":
    main()
