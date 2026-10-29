#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-29（晚）：《估價_特殊標的總整理》§97 補上「比較標的怎麼選」這個考點。

起因：使用者問 112-19「公共設施保留地原則上採比較法估價，其比較標的應如何選取？」，
並指出本頁 §97 那一列沒有說明白。

查證結果（`bxv-quiz-data.js`）：**同一個考點考過兩次，官方答案相反**——
  106-13「公共設施保留地估價，依不動產估價技術規則規定，得以下列何者為比較標的？」
        選項：①一般建築用地 ②鄰近之公共設施保留地或毗鄰非公共設施保留地
             ③農業用地 ④都市計畫保護區土地
        **官方答案 ④ 都市計畫保護區土地**（correct:3）
  112-19「公共設施保留地原則上採比較法估價，其比較標的應如何選取？」
        選項：①鄰近之公共設施保留地或毗鄰非公共設施保留地 ②一般建築用地
             ③農業用地 ④都市計畫保護區土地
        **官方答案 ① 鄰近之公共設施保留地或毗鄰非公共設施保留地**（correct:0）

兩題的選項內容幾乎相同，答案卻互換。原因是 **§97 條文根本沒有列舉比較標的之類型**：
逐字只有「公共設施用地及公共設施保留地之估價，以比較法估價為原則。無買賣實例者，
得比較其與**毗鄰土地**使用分區及使用強度差異，及土地價值減損情況，並斟酌毗鄰土地
平均價格為基礎推算之。」

本頁原本只寫條文後段，**完全沒提這兩題與其矛盾**（全頁「公共設施保留地」只出現 1 次）。
解析其實存在，但只在刷題頁與考題小卡的題目解析裡，看整理頁的人看不到。

本腳本：
 ① §97 那一列加一句指向下方陷阱框
 ② 在該節的「🧠 整理」框後面加一個紅框，把兩題並排、講清楚為什麼矛盾、考場怎麼判斷
 ③ 本頁原本 0 個題號連結，補上 .qlk 樣式與兩題連結（連到《估價_考題小卡》）

可重複執行。
"""
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent.parent / "估價_特殊標的總整理.html"

TRAP = """
<div class="box trap"><b>⚠️ §97 最大的陷阱：「比較標的怎麼選」考過兩次，<span class="k">官方答案相反</span></b><br>
<div class="qq">
<div class="qrow"><a class="qlk" href="估價_考題小卡.html#VH2_106_13">106-13</a>
<div class="qt">「依不動產估價技術規則規定，<b>得以下列何者為比較標的</b>？」</div>
<div class="qa">官方答案：<span class="k">都市計畫保護區土地</span></div></div>
<div class="qrow"><a class="qlk" href="估價_考題小卡.html#VH2_112_19">112-19</a>
<div class="qt">「原則上採比較法估價，其<b>比較標的應如何選取</b>？」</div>
<div class="qa">官方答案：<span class="k">鄰近之公共設施保留地或<b>毗鄰</b>非公共設施保留地</span></div></div>
</div>
兩題的四個選項幾乎一樣（鄰近公保地或毗鄰非公保地／一般建築用地／農業用地／都市計畫保護區土地），
<b>106 年選「都市計畫保護區土地」，112 年選「鄰近公保地或毗鄰非公保地」</b>，答案互換。<br>
<b>為什麼會這樣：<span class="k">§97 條文根本沒有列舉比較標的之類型</span></b>。
條文只說「以比較法估價為原則；無買賣實例者，得比較其與<span class="k">毗鄰土地</span>
使用分區及使用強度差異，及土地價值減損情況，並斟酌毗鄰土地平均價格為基礎推算之」。
兩題都不是從條文直接推得。<br>
<b>考場怎麼判斷</b>（以下為<span class="y">依條文所作之判斷，非官方說法</span>）：
條文能確定的只有一件事——無買賣實例時，比較的對象是「<span class="k">毗鄰土地</span>」。
112-19 的正解含「毗鄰非公共設施保留地」，與條文後段用語最接近；
而「都市計畫保護區土地」在 §97 條文中完全沒有出現。
故若再考同一題型，<span class="k">優先選含「毗鄰土地」字樣的選項</span>；
但 106 年官方選的是「都市計畫保護區土地」，<b>兩個答案都要有印象</b>——
這一題型本身就是不穩定考點。</div>
"""

CSS = """
.box.trap{border-left-color:var(--red);min-width:0}
.qlk{color:var(--pri,#2F5D50);font-weight:700;text-decoration:none;
  border-bottom:1px dotted currentColor;font-variant-numeric:tabular-nums;white-space:nowrap}
/* 站規：比較表不做成一大張橫表，每列一張小卡、手機單欄。
   這裡刻意不用 <table>——display:block 的 table 在窄螢幕仍會以 min-content 撐寬，
   實測 390px 會溢出 242px。 */
.qq{margin:6px 0;display:flex;flex-direction:column;gap:6px;min-width:0}
.qrow{min-width:0;padding:6px 8px;background:var(--card);border-radius:7px;
  border:1px solid var(--line,rgba(128,128,128,.25))}
.qrow .qt,.qrow .qa{margin-top:2px;overflow-wrap:anywhere}
"""

EDITS = [
    ("§97 那列加指向陷阱框的一句",
     '<td>無買賣實例：比較其與毗鄰土地<span class="k">使用分區及使用強度差異</span>、'
     '<span class="k">土地價值減損情況</span>，並斟酌毗鄰土地平均價格為基礎推算</td>',
     '<td>無買賣實例：比較其與毗鄰土地<span class="k">使用分區及使用強度差異</span>、'
     '<span class="k">土地價值減損情況</span>，並斟酌毗鄰土地平均價格為基礎推算。'
     '<br><b>⚠️ 條文<span class="k">沒有列舉「比較標的」要選哪一種土地</span>'
     '——這點考過兩次而且官方答案相反，見下方紅框。</b></td>', 1),

    ("在本節整理框後面插入陷阱框",
     '溫泉地、高爾夫球場（§90、§91）只列考慮因素、未指定方法。</div>',
     '溫泉地、高爾夫球場（§90、§91）只列考慮因素、未指定方法。</div>' + TRAP, 1),

    ("補 CSS",
     "</style>",
     CSS + "</style>", 1),
]


def main():
    s = PAGE.read_text(encoding="utf-8")
    before = len(s)
    done, skip, fail = [], [], []
    for name, old, new, n_exp in EDITS:
        if new in s and old not in s:
            skip.append(name)
            continue
        n = s.count(old)
        if n != n_exp:
            fail.append(f"✗ {name}：原文出現 {n} 次（應為 {n_exp} 次）\n     找的是：{old[:95]}…")
            continue
        s = s.replace(old, new, 1)
        done.append(f"{name}（1 處）")
    if fail:
        for f in fail:
            print(f)
        sys.exit("\n有項目對不上，整支腳本不寫檔。")
    PAGE.write_text(s, encoding="utf-8")
    for d in done:
        print("  ✔", d)
    for d in skip:
        print("  －已是新版，略過：", d)
    print(f"寫入 {PAGE.name}：{before} → {len(s)} 字元")


if __name__ == "__main__":
    main()
