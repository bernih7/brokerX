#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把經紀法規 v553 的「可就地作答」考古題面板移植到估價，產出 bxv-topic-qa.js。

來源：bxj-topic-q.js（261 行）。這裡不是手抄，是**程式化取代**，所以上游改了重跑即可。

估價與經紀法規的三個實質差異（不是改名字而已）：
  1. **紀錄 id 不同**。經紀法規是「章-年-題號」；估價的 BXREP.qid 是
     `章-year-id`，其中 year 是中文「99年第2題」、id 是「VA1_99_2」。
     所以 adapter 要把 `_year`／`_id` 帶上，rec／tag／conf 一律走 BXREP。
  2. **r.c 存的是「選項索引」不是字母**。估價解析版練習傳的是 idx，
     這裡也要傳 idx，否則同一題在兩頁的紀錄格式會不一致。
  3. **要雙寫章節頁存檔**。估價有 16 支刷題章節頁，各自用
     `bxv-st:<ANS[ch]>_answers`／`_errortags`；解析版練習就是這樣雙寫的。
     不雙寫的話，在面板答過的題到刷題頁會顯示「還沒做」。
  4. 估價題庫沒有「本題相關法條」欄位，所以法條區自動不會出現（law 給空物件）。

另外估價既有的 bxv-topic-q.js（只讀版、四大方法比較表與特殊標的總整理在用）**不動**。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "bxj-topic-q.js"
OUT = ROOT / "bxv-topic-qa.js"

# CSS 變數：估價各頁的 token 名稱不一致，一律補 fallback
VARS = {
    "--muted": "#7A8C84", "--line": "#DDD6C3", "--paper2": "#F0EDE0",
    "--paper": "#FFFEFA", "--ink": "#25302C", "--paper-dark": "#F0EDE0",
    "--pri": "#2F5D50", "--onc": "#ffffff",
    "--vermillion": "#A84030", "--green": "#2F6B45", "--gold": "#B8782E",
    "--hot": "#A84030", "--hotbg": "rgba(168,64,43,.10)",
    "--numfg": "#25302C", "--numbg": "rgba(240,185,60,.30)",
}
# 估價頁面常用的別名（先試頁面自己的，再 fallback）
ALIAS = {"--ink": "--fg", "--pri": "--primary", "--vermillion": "--hi-red",
         "--green": "--hi-grn", "--gold": "--hi-gold"}

TQ_DARK_JS = '''  var TQ_DARK = '--paper2:#222926;--paper-dark:#1C2825;--paper:#1A1F1D;'
    + '--muted:var(--sub,var(--ink-soft,var(--ink-2,#9AA79F)));'
    + '--primary:var(--pri,#84C2AE);--onc:#10201B;'
    + '--hi-red:var(--red,var(--stamp,var(--trap,#E07060)));'
    + '--hi-grn:var(--green,var(--note,#8FCB93));'
    + '--hi-gold:var(--gold,var(--warn,#E0B070));'
    + '--hot:#E58A78;--hotbg:rgba(224,112,96,.16);--numfg:#F0D9A0;--numbg:rgba(240,185,60,.16)';
'''
TQ_DARK_CSS = '''    /* 深色：頁面多半沒定義 --paper2／--paper-dark／--muted／--hi-*，原 fallback 是淺色值 → 在面板上補深色 token（兩份式）；bxv-hl.js 的「完整解析」摺疊鈕 fallback #2F5D4E 在沒 --pri/--green 的頁（四大方法）會深底深字，面板內一併蓋掉 */
    + '@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .bxv-tq{' + TQ_DARK + '}'
    + ':root:not([data-theme="light"]) .bxv-tq .tg.on,:root:not([data-theme="light"]) .bxv-tq .sg.on{color:#10201B}:root:not([data-theme="light"]) .bxv-tq details.exp-more>summary{color:var(--pri,var(--green,#84C2AE))}}'
    + ':root[data-theme="dark"] .bxv-tq{' + TQ_DARK + '}'
    + ':root[data-theme="dark"] .bxv-tq .tg.on,:root[data-theme="dark"] .bxv-tq .sg.on{color:#10201B}:root[data-theme="dark"] .bxv-tq details.exp-more>summary{color:var(--pri,var(--green,#84C2AE))}'
'''

HEADER = '''/* 估價｜整理頁內嵌「可作答」考古題面板　bxv-topic-qa.js
   用法：<div class="bxv-tq" data-qs="104-27,111-8" data-title="全程序順序"></div>
         或 <div class="bxv-tq" data-chs="F1" data-title="租金估計"></div>
   ⚠️ 本檔由 tools/mk_bxv_topicqa.py 從 bxj-topic-q.js 產生，**不要手改**，改上游再重跑。
   ⚠️ 與 bxv-topic-q.js（只讀版，四大方法比較表／特殊標的總整理在用）是兩支，那支不動。
   作答一律走 BXREP.rec／tag／conf，寫進共用的 bxv-q2，並雙寫章節頁存檔，
   所以在這裡答的題，刷題章節頁、錯題本、日拱一築面板都看得到。 */
(function () {
  /* 章 → 刷題章節頁的存檔前綴（與估價解析版練習的 ANS 相同） */
  var ANS = {A1:"valuation_practice_a1_v2",A2:"valuation_practice_a2_v2",A3:"valuation_practice_a3_v2",
    A4:"valuation_practice_a4_v2",B:"valuation_practice_b_v2",C1:"valuation_practice_c1_v2",
    C2:"valuation_practice_c2_v2",D1:"valuation_practice_d1_v2",D2:"valuation_practice_d2_v2",
    D3:"valuation_practice_d3_v2",E1:"valuation_practice_e1_v2",F1:"valuation_practice_f1_v2",
    G1:"valuation_practice_g1_v2",H1H2:"valuation_practice_h1h2_v2",
    H3I1:"valuation_practice_h3i1_v2",I2J1:"val_prac_i2j1_v1"};
  function stGet(k){try{return JSON.parse(localStorage.getItem("bxv-st:"+k)||"{}")||{}}catch(e){return {}}}
  function stSet(k,v){try{localStorage.setItem("bxv-st:"+k,JSON.stringify(v))}catch(e){}}
  /* BXREP 要的物件：**不可以帶 num**，帶了 qid 會變成 章-年-num */
  function ad(q){return {chapter:q.ch, year:q._year, id:q._id};}
'''

ADAPT = '''
  /* ── 把 BXV_QUIZ.items 轉成本面板要的形狀 ── */
  function build() {
    var Q = window.BXV_QUIZ; if (!Q || !Q.items) return null;
    return {
      law: {},
      q: Q.items.map(function (a) {
        return {
          k: a.y + '-' + a.n, ch: a.ch, y: a.y, n: a.n,
          stem: a.q, opt: a.opts, exp: a.exps, ans: 'ABCD'[a.correct],
          _year: a.year, _id: a.id
        };
      })
    };
  }
'''


def main():
    s = SRC.read_text(encoding="utf-8")
    orig = len(s)

    # 1) 名字
    for a, b in [("bxj-tq", "bxv-tq"), ("bxj-q2", "bxv-q2"), ("bxj-wclr", "bxv-wclr"),
                 ("經紀法規_法條解析練習.html", "估價解析版練習.html")]:
        if a not in s:
            sys.exit(f"來源找不到 {a}，上游可能改過，請重看")
        s = s.replace(a, b)

    # 2) CSS 變數補 fallback（估價各頁 token 名稱不一致）
    def fx(m):
        v = m.group(1)
        fb = VARS.get(v, "inherit")
        return f"var({ALIAS[v]},var({v},{fb}))" if v in ALIAS else f"var({v},{fb})"
    s = re.sub(r"var\((--[a-z0-9-]+)\)", fx, s)

    # 2b) 深色：估價頁多半沒定義 --paper2／--paper-dark／--muted／--hi-*，fallback 是淺色 → 面板上補深色 token（兩份式）
    anchor = "  var CSS = ''\n"
    if anchor not in s:
        sys.exit("找不到 var CSS")
    s = s.replace(anchor, TQ_DARK_JS + anchor, 1)
    anchor = "    + '@media(max-width:420px){.bxv-tq"
    if anchor not in s:
        sys.exit("找不到 CSS 結尾的 max-width:420px")
    s = s.replace(anchor, TQ_DARK_CSS + anchor, 1)

    # 3) 取代 qid／rec／tagIt／sureIt／「再作答一次」：改走估價的 BXREP ＋ 雙寫
    old_qid = "  function qid(q) { return q.ch + '-' + q.y + '-' + q.n; }"
    if old_qid not in s:
        sys.exit("找不到 qid 定義")
    s = s.replace(old_qid, "  function qid(q) { return q.ch + '-' + q._year + '-' + q._id; }")

    i = s.find("  /* 作答一律走 BXREP")
    j = s.find("  function accept(q)")
    if i < 0 or j < 0 or j <= i:
        sys.exit("找不到 rec／tagIt／sureIt 區塊")
    s = s[:i] + '''  /* 作答一律走 BXREP（寫 bxv-q2），再雙寫章節頁存檔，兩邊才看得到同一筆 */
  function rec(q, chosenLetter, ok) {
    var idx = 'ABCD'.indexOf(chosenLetter);
    try { if (window.BXREP && BXREP.rec) BXREP.rec(ad(q), idx, ok); } catch (e) { }
    var p = ANS[q.ch]; if (!p) return;
    var a = stGet(p + '_answers'); a[q._id] = { selected: idx, correct: !!ok }; stSet(p + '_answers', a);
    var t = stGet(p + '_errortags'); if (q._id in t) { delete t[q._id]; stSet(p + '_errortags', t); }
  }
  function tagIt(q, k) {
    try { if (window.BXREP && BXREP.tag) BXREP.tag(ad(q), k); } catch (e) { }
    var p = ANS[q.ch]; if (!p) return;
    var t = stGet(p + '_errortags'); t[q._id] = k; stSet(p + '_errortags', t);
  }
  function sureIt(q, sh) {
    try { if (window.BXREP && BXREP.conf) BXREP.conf(ad(q), sh === 1 ? 'shaky' : (sh === 2 ? 'guess' : 'sure')); } catch (e) { }
  }
''' + s[j:]

    # 「你選的」判斷：經紀法規存字母，估價存索引 → 轉回字母
    old = "var picked = q._r && q._r.n ? (q._r.c || '') : '';"
    if old not in s:
        sys.exit("找不到 picked 那一行")
    s = s.replace(old, "var picked = (q._r && q._r.n && q._r.c != null && q._r.c !== '') ? 'ABCD'[q._r.c] || '' : '';")

    # 「再作答一次」也要清掉章節頁存檔，否則刷題頁仍顯示已作答
    old = ("        if (t.closest('.again')) {\n"
           "          var DB = db(); if (DB[qid(q)]) { DB[qid(q)].n = 0; DB[qid(q)].c = ''; delete DB[qid(q)].sh; sv('bxv-q2', DB); }\n"
           "          draw(); return;\n"
           "        }")
    if old not in s:
        sys.exit("找不到『再作答一次』區塊")
    s = s.replace(old, '''        if (t.closest('.again')) {
          var DB = db(); if (DB[qid(q)]) { DB[qid(q)].n = 0; DB[qid(q)].c = ''; delete DB[qid(q)].sh; sv('bxv-q2', DB); }
          var p = ANS[q.ch];
          if (p) { var aa = stGet(p + '_answers'); if (q._id in aa) { delete aa[q._id]; stSet(p + '_answers', aa); } }
          draw(); return;
        }''')

    # 4) 資料來源：改成由 BXV_QUIZ 轉形
    s = s.replace("    var Q = window.BXJ_QUIZ; if (!Q) return;",
                  "    var Q = build(); if (!Q) return;")
    old_boot = """  function boot() {
    if (!document.querySelector('.bxv-tq')) return;
    if (window.BXJ_QUIZ) { init(); return; }
    var s = document.createElement('script'); s.src = 'bxj-quiz-data.js'; s.onload = init; document.head.appendChild(s);
  }"""
    if old_boot not in s:
        sys.exit("找不到 boot()")
    s = s.replace(old_boot, """  function boot() {
    if (!document.querySelector('.bxv-tq')) return;
    if (window.BXV_QUIZ) { init(); return; }
    var s = document.createElement('script'); s.src = 'bxv-quiz-data.js'; s.onload = init; document.head.appendChild(s);
  }""")

    # 5) 換掉開頭註解、插入 adapter
    s = re.sub(r"^/\*.*?\*/\n\(function \(\) \{\n", HEADER, s, count=1, flags=re.S)
    k = s.find("  function init() {")
    if k < 0:
        sys.exit("找不到 init()")
    s = s[:k] + ADAPT + "\n" + s[k:]

    # 6) 殘留檢查（跳過開頭註解——那裡本來就會提到來源檔名）
    body = s[len(HEADER):]
    for bad in ["bxj-", "BXJ_", "經紀法規"]:
        if bad in body:
            p = body.find(bad)
            sys.exit(f"還有殘留的 {bad}：…{body[max(0, p - 60):p + 60]}…")

    OUT.write_text(s, encoding="utf-8")
    print(f"產生 {OUT.name}：{orig} → {len(s)} 字元")


if __name__ == "__main__":
    main()
