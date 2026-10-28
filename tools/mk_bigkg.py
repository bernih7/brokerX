#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「選擇題歷屆導引」掛到《估價_四大方法比較表》的程序卡與陷阱卡上。

樣式＝C 版（整區收合）＋「練這 N 題」：
  平常只有一行「🖋 選擇題考過 3 題・102-9・104-16・107-19 ▾」，
  點開才出現逐題（題號→考題小卡、正解、章別、題幹一行、考點一句）。

做法：
  1. 依 pc-* class 與 trap-label 文字，給 4 張程序卡與 14 張陷阱卡加上 id。
  2. 題目資料與版型由頁尾的 <style id="kg-css"> 與 <script id="kg-js"> 產生，
     用 JS 依 id 追加到卡片裡——不用字串切位置（v525 折舊圖那次就是切壞 HTML）。
  3. 可重複執行：每次先把舊的 kg-css／kg-js 與 id 標記清掉再寫。

題目對應是人工確認過的（2026-10-28 與使用者逐項核對），不是關鍵詞自動配。
改對應請改本檔的 MAP，然後重跑。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "估價_四大方法比較表.html"
DATA = ROOT / "bxv-quiz-data.js"
CARD = "估價_考題小卡.html"
DRILL = "估價解析版練習.html"

# ── 程序卡：pc-* class → (id, 標題用的名字) ────────────────────────────
PROC = [("pc-comp", "kg-pc1"), ("pc-cost", "kg-pc2"),
        ("pc-inc", "kg-pc3"), ("pc-dev", "kg-pc4")]

# ── 陷阱卡：trap-label 開頭文字 → id ──────────────────────────────────
TRAP = [
    ("陷阱 01｜", "kg-t01"), ("陷阱 01B｜", "kg-t01b"), ("陷阱 02｜", "kg-t02"),
    ("陷阱 03｜", "kg-t03"), ("陷阱 04｜", "kg-t04"), ("陷阱 05｜", "kg-t05"),
    ("陷阱 06｜", "kg-t06"), ("陷阱 07｜", "kg-t07"), ("陷阱 08｜", "kg-t08"),
    ("陷阱 09｜", "kg-t09"), ("陷阱 10｜", "kg-t10"), ("陷阱 11｜", "kg-t11"),
    ("陷阱 12｜", "kg-t12"), ("陷阱 13｜", "kg-t13"),
]

# ── 對應表：id → (年, 題號, 考點一句) ─────────────────────────────────
# 空 list ＝ 該卡掛「選擇題未考過」一行，不掛題目清單。
MAP = {
 "kg-pc1": [],   # 比較法程序：16 年無官方選擇題考排列
 "kg-pc2": [],   # 成本法程序：同上
 "kg-pc3": [
  (102, 9,  "六步驟順序：蒐集→有效總收入→總費用→淨收益→決定資本化率→收益價格。選項只是把編號打亂。"),
  (104, 16, "同一條順序換一組編號再考。先推總費用、再算淨收益；決定資本化率排在倒數第二。"),
  (107, 19, "三年考三次都是同一條順序。把「決定資本化率」排到最前面的選項一律錯。"),
 ],
 "kg-pc4": [
  (104, 22, "八步驟全考。第一步是「確定開發內容及預期開發時間」，<b>不是蒐集資料</b>——這點和其他三法相反。"),
  (106, 36, "只問最後四步：總銷售金額→各項成本費用→利潤率及資本利息綜合利率→價格。"),
  (111, 25, "現況勘察調查的是<b>勘估標的</b>的工程進度與施工狀況；寫「比較標的」就錯——土開沒有比較標的。"),
 ],
 "kg-t01": [
  (100, 7,  "重置成本的成立依據＝替代原則。成本法用的是替代原則的「重置觀點」。"),
  (105, 8,  "三法共同的評價基礎就是替代原則；比較法＝交易、成本法＝重置、收益法＝投資，只是觀點不同。"),
 ],
 "kg-t01b": [
  (104, 8,  "收益法＝投資觀點→收益價格。比較法得出的是「比較價格」不是「成交價格」；成本法沒有「未來成本」這個概念。"),
 ],
 "kg-t02": [
  (104, 31, "§87：得採土開法，並參酌「<b>比較法或收益法</b>」——不是參酌成本法。正解①③。"),
 ],
 "kg-t03": [
  (105, 28, "§92 林地採成本法時，總費用只考量<b>造林費、林地改良費、道路開挖費用</b>三項；「營運費用」是收益法 §38 的東西。"),
 ],
 "kg-t04": [
  (100, 26, "官方答案說比較法「較不適宜」，但現行 §95 規定池沼、墓地<b>以比較法為原則</b>。⚠️ 答案與現行法衝突，考試以官方答案為準。"),
  (110, 15, "同上，官方答案選「不具一般市場性，較難以比較法估價」。⚠️ 同樣與現行 §95 衝突。"),
 ],
 "kg-t05": [
  (100, 16, "建物折舊前之價格，<b>以求取重建成本為原則</b>。"),
  (102, 14, "「相同或極類似建材、<b>重新複製</b>」＝重建成本。"),
  (104, 18, "材料已無生產或施工方法已改變 → 得採<b>重置成本</b>替代。這是唯一的例外。"),
  (105, 16, "和 102-14 幾乎一字不改，再考一次。"),
  (106, 38, "「<b>相同效用</b>、現代建材」＝重置成本。和重建成本的差別只在「相同複製」對「相同效用」。"),
  (107, 9,  "一題同時考兩個：甲＝重建（原則）、乙＝重置（例外）。"),
  (108, 10, "又是重建成本的定義，第三次。"),
  (109, 21, "第四次。這個定義 16 年考了 6 次，背熟就是送分題。"),
 ],
 "kg-t06": [
  (99, 31,  "不計入總費用的就是<b>所得稅、土地增值稅、貸款利息</b>三個，六題在輪流考這三個。本題考所得稅。"),
  (100, 25, "貸款利息不計入——屬融資的財務成本，不是經營不動產的客觀成本。"),
  (102, 10, "所得稅，第二次。"),
  (105, 34, "土地增值稅不計入——那是處分時的稅。"),
  (107, 2,  "貸款利息，第二次。"),
  (112, 9,  "土地增值稅，第二次。"),
 ],
 "kg-t07": [
  (101, 18, "Pn′＝<b>期末價值</b>（分析期間結束時的處分價值）。"),
  (102, 27, "同一條公式改考 n′＝<b>折現現金流量分析期間</b>。⚠️ Pn′ 和 n′ 常被對調。"),
  (114, 23, "§32：計入期末處分價值時用「<b>折現率 Y</b>」折現，不是資本化率。"),
 ],
 "kg-t08": [
  (104, 23, "§79 公式：年利率×（土地價值比率＋建物價值比率<b>×½</b>）×開發年數。土地一開始全額投入、建物施工期間陸續投入，所以只有建物乘½。"),
  (107, 10, "3%×(40%＋60%×0.5)×3＝<b>6.3%</b>。"),
  (109, 10, "反推年利率：4.8%÷[(0.6＋0.4×½)×2]＝4.8%÷1.6＝<b>3.0%</b>。"),
  (114, 12, "只問公式長相，不用算。"),
 ],
 "kg-t09": [
  (105, 7,  "§6 後段：<b>只有特定價格</b>要敘明估價條件並同時估計正常價格。"),
  (111, 13, "同一條再考一次。"),
 ],
 "kg-t10": [
  (103, 11, "只有<b>等速、初期加速、初期減速</b>三種路徑。「後期減速折舊」是不存在的選項。"),
  (103, 28, "⚠️ 收益法的建物<b>折舊提存費</b>只有「等速折舊型」與「償債基金型」兩種（①④）——不要跟累積折舊額的三種路徑搞混。"),
  (106, 26, "§68：選哪一種路徑要視「<b>建物特性及市場動態</b>」。"),
 ],
 "kg-t11": [
  (106, 16, "§89 污染：2,000－500＝<b>1,500 萬</b>。先估未受污染的正常價格，再扣減損額。"),
  (109, 3,  "§88 設施通過：錯的選項把「正常價格」寫成「<b>特定價格</b>」。§88／§89 都是先估<b>正常價格</b>再扣減損額。"),
 ],
 "kg-t12": [
  (107, 7,  "收益法要蒐集最近 <b>3 年</b>。"),
  (99, 35,  "這題的 D 選項也寫「最近三年間」，是<b>對的</b>；錯的是 C——含建物時「<b>應</b>」加計折舊提存費。"),
 ],
 "kg-t13": [
  (99, 8,   "資本利息依「<b>分期投入資本數額及資本使用年數</b>」計息。"),
  (99, 38,  "自有資金「<b>應</b>」計息（利率不高於一年期定存、不低於活存）。寫「不應計息」就錯。"),
  (109, 17, "§59：<b>預售收入之資金不計息</b>。寫「以定存利率計息」就錯。"),
  (114, 2,  "出售不動產的所得稅不屬於總成本——和收益法排除所得稅是同一個邏輯。"),
 ],
}

NONE_NOTE = ("選擇題<b>沒考過</b>本法的程序排列（16 年只有收益法與土開考過），"
             "程序本身只在<b>申論</b>出現，見上一行。")

CSS = """<style id="kg-css">
/* ⚠️ proc-grid 在 500px 以下是「1fr 1fr」兩欄，欄寬只有約 170px。
   grid item 預設 min-width:auto，子元素的 min-content 寬度會把整欄撐爆，
   連帶把頁面推寬（實測 390px 溢出 228px）。所以卡片與區塊都要 min-width:0。*/
.proc-card,.trap-card,.trap-body{min-width:0}
.kg,.kg>summary,.kg-l,.kg-l>li,.kg-h{min-width:0}
.kg{margin-top:11px;padding-top:9px;border-top:1px dashed var(--line)}
.kg>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;
  font-size:.78rem;color:var(--muted)}
.kg>summary::-webkit-details-marker{display:none}
.kg>summary:hover .kg-n{text-decoration:underline}
.kg-n{font-weight:800;color:var(--fg,#25302C);white-space:nowrap}
/* 題號列永遠只佔一行，放不下就省略，不折行──註記不可以比內容大聲 */
.kg-y{font-variant-numeric:tabular-nums;flex:1 1 0;min-width:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kg>summary::after{content:"▾";flex:none;color:var(--muted)}
.kg[open]>summary::after{content:"▴"}
.kg-top{margin:9px 0 2px}
.kg-all{display:inline-block;text-decoration:none;font-weight:800;font-size:.74rem;
  padding:2px 10px;border-radius:999px;background:var(--primary);color:#fff}
.kg-l{list-style:none;margin:7px 0 2px;padding:0;display:flex;flex-direction:column;gap:9px}
.kg-l>li{min-width:0}
.kg-h{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;font-size:.8rem}
.kg-no{text-decoration:none;font-weight:800;font-size:.74rem;padding:1px 8px;border-radius:999px;
  background:rgba(47,93,80,.12);color:var(--primary);font-variant-numeric:tabular-nums;white-space:nowrap}
.kg-no:hover{background:var(--primary);color:#fff}
.kg-a{font-size:.72rem;font-weight:800;color:var(--hi-grn)}
.kg-c{font-size:.69rem;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 5px}
.kg-q{font-size:.81rem;color:var(--muted);margin-top:1px}
.kg-p{font-size:.83rem;margin-top:2px}
.kg-p b{color:var(--hi-red)}
.kg-none{margin-top:11px;padding-top:9px;border-top:1px dashed var(--line);
  font-size:.78rem;color:var(--muted);line-height:1.7}
.kg-none b{color:var(--hi-red)}
</style>"""


def main():
    src = DATA.read_text(encoding="utf-8")
    i = src.find("items:[")
    j = src.find("\n]", i)
    items = json.loads("[" + src[i + len("items:["):j] + "]")
    by = {(a["y"], a["n"]): a for a in items}

    s = PAGE.read_text(encoding="utf-8")
    orig = s

    # ---- 先清掉上一次產生的東西（可重複執行） ----
    s = re.sub(r'<style id="kg-css">.*?</style>\n?', "", s, flags=re.S)
    s = re.sub(r'<script id="kg-js">.*?</script>\n?', "", s, flags=re.S)
    s = re.sub(r'(<div class="(?:proc-card [a-z-]+|trap-card))" id="kg-[a-z0-9]+"', r'\1"', s)

    # ---- 1. 程序卡加 id ----
    for cls, cid in PROC:
        a = f'<div class="proc-card {cls}">'
        if s.count(a) != 1:
            sys.exit(f"找不到（或不只一個）程序卡 {cls}：{s.count(a)} 個")
        s = s.replace(a, f'<div class="proc-card {cls}" id="{cid}">')

    # ---- 2. 陷阱卡加 id（依卡內 trap-label 文字對應，不靠順序） ----
    chunks = s.split('<div class="trap-card">')
    if len(chunks) - 1 != len(TRAP):
        sys.exit(f"陷阱卡數量不符：頁面 {len(chunks)-1} 張、對應表 {len(TRAP)} 張")
    used = {}
    out = [chunks[0]]
    for ch in chunks[1:]:
        m = re.search(r'class="trap-label"[^>]*>(.*?)</', ch, re.S)
        lab = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""
        cid = None
        for pre, c in TRAP:                      # 「01B」要比「01」先比到
            if lab.startswith(pre) and c not in used:
                if cid is None or len(pre) > cid[0]:
                    cid = (len(pre), c)
        if cid is None:
            sys.exit(f"這張陷阱卡對不到 id：{lab!r}")
        used[cid[1]] = lab
        out.append(f'<div class="trap-card" id="{cid[1]}">' + ch)
    s = "".join(out)
    if len(used) != len(TRAP):
        sys.exit(f"只對到 {len(used)} 張陷阱卡")

    # ---- 3. 組出 JS 資料 ----
    js, miss, nq = {}, [], 0
    for cid, qs in MAP.items():
        rows = []
        for y, n, pt in qs:
            a = by.get((y, n))
            if a is None:
                miss.append(f"{y}-{n}")
                continue
            stem = re.sub(r"\s+", " ", a["q"]).strip()
            stem = re.split(r"[①②]", stem)[0].strip()      # 砍掉題幹裡的選項列舉
            if len(stem) > 46:
                stem = stem[:46] + "…"
            rows.append({"n": f"{y}-{n}", "i": a["id"], "a": "ABCD"[a["correct"]],
                         "c": a["ch"], "s": stem, "p": pt})
            nq += 1
        js[cid] = rows
    if miss:
        sys.exit("題庫裡找不到這些題：" + "、".join(miss))

    payload = json.dumps(js, ensure_ascii=False, separators=(",", ":"))
    script = ('<script id="kg-js">\n'
              "(function(){var D=" + payload + ";\n"
              'var NONE=' + json.dumps(NONE_NOTE, ensure_ascii=False) + ';\n'
              'var CARD=' + json.dumps(CARD, ensure_ascii=False) + ',DRILL='
              + json.dumps(DRILL, ensure_ascii=False) + ';\n'
              "Object.keys(D).forEach(function(id){var host=document.getElementById(id);if(!host)return;\n"
              '  var box=host.querySelector(".trap-body")||host;var rows=D[id];\n'
              "  if(!rows.length){var p=document.createElement('div');p.className='kg-none';\n"
              "    p.innerHTML='🖋 '+NONE;box.appendChild(p);return}\n"
              "  var d=document.createElement('details');d.className='kg';\n"
              "  var ns=rows.map(function(r){return r.n});\n"
              "  var ys=ns.length>4?ns.slice(0,4).join('・')+'…':ns.join('・');\n"
              '  var h=\'<summary><span class="kg-n">🖋 選擇題考過 \'+rows.length+\' 題</span>\'+\n'
              "        '<span class=\"kg-y\">'+ys+'</span></summary>'+\n"
              '        \'<div class="kg-top"><a class="kg-all" href="\'+DRILL+\'#q=\'+\n'
              "        ns.join(',')+'\">▶ 練這 '+rows.length+' 題</a></div><ul class=\"kg-l\">';\n"
              "  rows.forEach(function(r){h+='<li><div class=\"kg-h\">'+\n"
              '    \'<a class="kg-no" href="\'+CARD+\'#\'+r.i+\'">\'+r.n+\'</a>\'+\n'
              "    '<span class=\"kg-a\">正解 '+r.a+'</span><span class=\"kg-c\">'+r.c+'</span></div>'+\n"
              "    '<div class=\"kg-q\">'+r.s+'</div><div class=\"kg-p\">'+r.p+'</div></li>'});\n"
              "  d.innerHTML=h+'</ul>';box.appendChild(d)});\n"
              "})();\n</script>")

    # 這頁沒有 </body>／</html>，直接接在檔尾
    if "</body>" in s:
        s = s.replace("</body>", CSS + "\n" + script + "\n</body>", 1)
    else:
        s = s.rstrip("\n") + "\n\n" + CSS + "\n" + script + "\n"

    PAGE.write_text(s, encoding="utf-8")
    print(f"寫入 {PAGE.name}：{len(orig)} → {len(s)} 字元")
    print(f"區塊 {len(js)} 個（其中 {sum(1 for v in js.values() if not v)} 個標『選擇題未考過』）、題目 {nq} 題")


if __name__ == "__main__":
    main()
