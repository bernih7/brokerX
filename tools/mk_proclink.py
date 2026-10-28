#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《估價_估價程序總整理》：八個步驟各掛一組「選擇題考過哪幾題」，另在八大步驟最上方
加一組「全程序順序」。樣式＝C 版整區收合（同四大方法比較表 v551）。

這頁原本只有三個步驟寫了年份、而且沒有題號：
  ① 寫「99、101、103、104、105 年」→ 其中 **104 其實是全程序排序題（104-27）**，
     而且漏了 111、114（114-25 是去年剛考的）。本檔已更正。
  ④ 寫「103 年」✓　⑦ 寫「102 年」✓
  ②③⑤⑥⑧ 完全沒寫。

對應是人工逐題核對解析後配的（2026-10-28 與使用者確認），不是關鍵詞自動配。
可重複執行。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "估價_估價程序總整理.html"
DATA = ROOT / "bxv-quiz-data.js"
CARD = "估價_考題小卡.html"
DRILL = "估價解析版練習.html"

MAP = {
 "all": [
  (104, 27, "八項的正確順序是 <b>①②④③⑤⑦⑥⑧</b>——<b>蒐集資料在確認狀態之前</b>、<b>運用方法在決定價格之前</b>。口訣「基計蒐狀整估決書」就是這條。"),
  (111, 8,  "只問第七步＝<b>決定勘估標的價格</b>（在運用方法之後、報告書之前）。"),
 ],
 "s1": [
  (99, 29,  "四項之一是「價格種類<b>及條件</b>（估價條件）」——「估價條件」就是明定項目。"),
  (103, 29, "和 99-29 幾乎同一題，答案一樣是估價條件。"),
  (111, 21, "換個問法問「哪個<b>屬於</b>」，答估價目的。"),
  (114, 25, "去年剛考。①③④⑤ 都算，<b>②勘查日期不算</b>——它是步驟④的工作。"),
  (101, 8,  "問「哪個<b>不屬於</b>」：答<b>勘察日期</b>。基本事項裡的是<b>價格</b>日期。"),
  (105, 4,  "問「哪個不屬於」：答<b>估價方法</b>——方法要到步驟⑥才決定。"),
  (101, 10, "價格日期＝估價報告書上所載勘估標的價格之<b>基準日期</b>（§2⑦）。"),
  (102, 22, "同一個定義換句話問：價格日期是<b>不動產價格的基準日期</b>。"),
  (111, 18, "第三次考同一個定義。這三題背一次就全拿。"),
 ],
 "s2": [],
 "s3": [
  (103, 14, "§4Ⅰ：估價師應經常蒐集<b>比較標的</b>的交易、收益及成本案例，並詳予求證可靠性。"),
  (108, 23, "§4Ⅱ：到<b>實價登錄</b>查資料＝向<b>地政機關</b>蒐集。"),
  (102, 5,  "§12①：實例價格要屬<b>正常價格</b>或可調整為正常價格；寫成「特定或限定價格」就錯。"),
  (107, 3,  "同一個陷阱，這次把正常價格換成<b>限定價格</b>。"),
  (108, 18, "第三次考 §12①，這次 D 是對的敘述。"),
 ],
 "s4": [
  (103, 12, "問「何者<b>有誤</b>」：<b>確定勘估標的內容</b>是步驟①的事，不是現場勘察的事項。"),
  (101, 38, "要掌握所有權、面積、界線、鄰地地號 → <b>土地登記簿謄本＋地籍圖</b>（§13 確認基本資料及權利狀態）。"),
 ],
 "s5": [
  (103, 24, "§25：區域或個別因素<b>任一單項</b>調整率大於 <b>15%</b> → 排除該比較標的。"),
  (108, 15, "同一條再考一次，問法改成「何者為正確」。"),
  (113, 23, "§26 比的是試算價格之間的<b>差距</b>達 20%，不是「總調整率」大於 20%——總調整率的門檻是 <b>30%</b>。"),
  (113, 8,  "實算：(95－77)÷[(95＋77)/2]≈<b>20.9%</b> ≥ 20% → 比較標的二與三符合排除條件。"),
 ],
 "s6": [
  (113, 6,  "§15Ⅱ但書：證券化標的<b>進行清算時不適用</b>加重 DCF 權重那一條。"),
  (108, 6,  "以<b>契約</b>約定租金作為信託利益分配基礎 → <b>DCF 的收益價格</b>賦予較大權重。"),
 ],
 "s7": [
  (102, 29, "問「何者錯誤」：條文寫的是<b>契約租金</b>，選項誤植成<b>經濟租金</b>。"),
  (111, 10, "同一條的正面問法，答 DCF 之收益價格。⚠️ 契約租金 vs 經濟租金是這一步的固定陷阱。"),
 ],
 "s8": [
  (114, 17, "價格日期與勘查日期的先後是「<b>不一定</b>」——兩個都要註明，但沒有固定順序。"),
 ],
}

NONE = {
 "s2": "選擇題<b>沒有單獨考過</b>估價計畫五項，只在 <b>104-27</b> 的全程序排序題裡出現過一次。",
}

# 步驟⑧ 的補充提醒（🔴 高頻是依條文重要性標的，不是依選擇題數）
S8NOTE = ("🔴 <b>§16 十五項條文重要（申論常考）</b>，但選擇題 16 年只考過 <b>1 題</b>"
          "（114-17，考價格日期與勘查日期的先後）。這個 🔴 是依條文重要性標的，不是依出題數。")

# ① 原本的 .hit 寫錯了，換成正確年份
HIT_OLD = '<div class="hit">🔴 <b>99、101、103、104、105 年</b>都考過——多考「四項是什麼」「不含什麼」。</div>'
HIT_NEW = ('<div class="hit">🔴 <b>99、101、103、105、111、114 年</b>都考過——多考「四項是什麼」「不含什麼」。'
           '<br>⚠️ 本頁原寫「104 年」是<b>錯的</b>：104 年考的是 104-27 全程序排序，不是基本事項。</div>')

CSS = """<style id="pk-css">
.pk{margin-top:10px;padding-top:9px;border-top:1px dashed var(--line);min-width:0}
.pk>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;
  font-size:.78rem;color:var(--muted);min-width:0}
.pk>summary::-webkit-details-marker{display:none}
.pk>summary:hover .pk-n{text-decoration:underline}
.pk-n{font-weight:800;color:var(--fg);white-space:nowrap}
.pk-y{font-variant-numeric:tabular-nums;flex:1 1 0;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pk>summary::after{content:"▾";flex:none;color:var(--muted)}
.pk[open]>summary::after{content:"▴"}
.pk-top{margin:9px 0 2px}
.pk-all{display:inline-block;text-decoration:none;font-weight:800;font-size:.74rem;
  padding:2px 10px;border-radius:999px;background:var(--hi-grn);color:#fff}
.pk-l{list-style:none;margin:7px 0 2px;padding:0;display:flex;flex-direction:column;gap:9px}
.pk-l>li{min-width:0}
.pk-h{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;font-size:.8rem;min-width:0}
.pk-no{text-decoration:none;font-weight:800;font-size:.74rem;padding:1px 8px;border-radius:999px;
  background:var(--hi-grn-bg);color:var(--hi-grn);font-variant-numeric:tabular-nums;white-space:nowrap}
.pk-no:hover{background:var(--hi-grn);color:#fff}
.pk-a{font-size:.72rem;font-weight:800;color:var(--hi-grn)}
.pk-c{font-size:.69rem;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 5px}
.pk-q{font-size:.81rem;color:var(--muted);margin-top:1px}
.pk-p{font-size:.83rem;margin-top:2px}
.pk-p b{color:var(--hi-red)}
.pk-none{margin-top:10px;padding-top:9px;border-top:1px dashed var(--line);
  font-size:.78rem;color:var(--muted);line-height:1.7}
.pk-none b{color:var(--hi-red)}
.pk-all-wrap{margin:14px 0 18px}
</style>"""


def main():
    src = DATA.read_text(encoding="utf-8")
    i = src.find("items:[")
    items = json.loads("[" + src[i + len("items:["):src.find("\n]", i)] + "]")
    by = {(a["y"], a["n"]): a for a in items}

    s = PAGE.read_text(encoding="utf-8")
    before = len(s)

    # 可重複執行
    s = re.sub(r'<style id="pk-css">.*?</style>\n?', "", s, flags=re.S)
    s = re.sub(r'<script id="pk-js">.*?</script>\n?', "", s, flags=re.S)
    s = s.replace(HIT_NEW, HIT_OLD)

    # ① 的年份更正
    if HIT_OLD not in s:
        sys.exit("找不到步驟① 原本的 .hit 那一行，請確認頁面沒被改過")
    s = s.replace(HIT_OLD, HIT_NEW, 1)

    # 組資料
    js, nq = {}, 0
    for key, qs in MAP.items():
        rows = []
        for y, n, pt in qs:
            a = by.get((y, n))
            if a is None:
                sys.exit(f"題庫找不到 {y}-{n}")
            stem = re.sub(r"\s+", " ", a["q"]).strip()
            stem = re.split(r"[①②]", stem)[0].strip()
            if len(stem) > 44:
                stem = stem[:44] + "…"
            rows.append({"n": f"{y}-{n}", "i": a["id"], "a": "ABCD"[a["correct"]],
                         "c": a["ch"], "s": stem, "p": pt})
            nq += 1
        js[key] = rows
    for k, v in js.items():
        print(f"   {k:5s} {len(v):2d} 題  " + "、".join(r["n"] for r in v))

    payload = json.dumps(js, ensure_ascii=False, separators=(",", ":"))
    none_payload = json.dumps(NONE, ensure_ascii=False, separators=(",", ":"))

    script = (
        '<script id="pk-js">\n'
        "(function(){var D=" + payload + ",NONE=" + none_payload + ";\n"
        'var S8=' + json.dumps(S8NOTE, ensure_ascii=False) + ';\n'
        'var CARD=' + json.dumps(CARD, ensure_ascii=False) + ',DRILL=' + json.dumps(DRILL, ensure_ascii=False) + ';\n'
        "function block(rows){var ns=rows.map(function(r){return r.n});\n"
        "  var ys=ns.length>4?ns.slice(0,4).join('・')+'…':ns.join('・');\n"
        "  var d=document.createElement('details');d.className='pk';\n"
        '  var h=\'<summary><span class="pk-n">🖋 選擇題考過 \'+rows.length+\' 題</span>\'+\n'
        "    '<span class=\"pk-y\">'+ys+'</span></summary>'+\n"
        '    \'<div class="pk-top"><a class="pk-all" href="\'+DRILL+\'#q=\'+ns.join(\',\')+\'">▶ 練這 \'+rows.length+\' 題</a></div><ul class="pk-l">\';\n'
        "  rows.forEach(function(r){h+='<li><div class=\"pk-h\">'+\n"
        '    \'<a class="pk-no" href="\'+CARD+\'#\'+r.i+\'">\'+r.n+\'</a>\'+\n'
        "    '<span class=\"pk-a\">正解 '+r.a+'</span><span class=\"pk-c\">'+r.c+'</span></div>'+\n"
        "    '<div class=\"pk-q\">'+r.s+'</div><div class=\"pk-p\">'+r.p+'</div></li>'});\n"
        "  d.innerHTML=h+'</ul>';return d}\n"
        "['s1','s2','s3','s4','s5','s6','s7','s8'].forEach(function(id){\n"
        "  var sec=document.getElementById(id);if(!sec)return;\n"
        "  if(id==='s8'){var e=document.createElement('div');e.className='hit';e.innerHTML=S8;sec.appendChild(e)}\n"
        "  var rows=D[id]||[];\n"
        "  if(!rows.length){if(NONE[id]){var p=document.createElement('div');p.className='pk-none';\n"
        "    p.innerHTML='🖋 '+NONE[id];sec.appendChild(p)}return}\n"
        "  sec.appendChild(block(rows))});\n"
        "var s1=document.getElementById('s1');\n"
        "if(s1&&D.all&&D.all.length){var w=document.createElement('div');w.className='pk-all-wrap';\n"
        "  var b=block(D.all);b.querySelector('.pk-n').textContent='🖋 全程序順序考過 '+D.all.length+' 題';\n"
        "  w.appendChild(b);s1.parentNode.insertBefore(w,s1)}\n"
        "})();\n</script>")

    if "</body>" in s:
        s = s.replace("</body>", CSS + "\n" + script + "\n</body>", 1)
    else:
        s = s.rstrip("\n") + "\n\n" + CSS + "\n" + script + "\n"

    PAGE.write_text(s, encoding="utf-8")
    print(f"寫入 {PAGE.name}：{before} → {len(s)} 字元；題目 {nq} 題")


if __name__ == "__main__":
    main()
