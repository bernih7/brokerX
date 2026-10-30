#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-30：使用者截圖《估價四大方法系統攻略》成本法③償債基金法，問「錯了吧」。

錯在哪：
 ① 分子標「(1－s)×i　殘餘價格率×利率」——(1－s) 是「1 減殘餘價格率」，不是殘餘價格率。
 ② 分母標「(1＋i)ᴺ－1　複利終值係數」——複利終值係數是 (1＋i)ᴺ 本身；
    i÷[(1＋i)ᴺ－1] 是「償債基金係數」，[(1＋i)ⁿ－1]÷i 是「複利年金終值係數」。
 ③ 等號右邊「C×(1－s)×i÷((1＋i)ᴺ－1)÷C」＝左邊乘 C 再除 C，同義反覆，沒有意義。
 ④ 放在「成本法」卻只給 §40-1（收益法折舊提存費），**沒有成本法要的累積折舊額 Dn**。
    §40-1 的 C 是「建物總成本」，卡上寫「重建成本」。

同樣的錯誤標籤散在四頁：
 - 「(1－s)<small>殘餘價格率</small>」7 處（範文 5、計算題攻略 1、速記 1）
 - 「(1＋i)ᴺ－1<small>複利終值係數</small>」3 處（範文、計算題攻略、速記）＋系統攻略 1 處
 - 速記的償債基金式漏乘 C，等號右邊寫「每年提存 dn」（d 在 §41 是折舊提存率，易混）

數字範例（已實算）：C＝1,000 萬、s＝10%、i＝2%、N＝50、n＝10
  每年提存額＝900×0.02÷(1.02⁵⁰－1)＝10.64 萬
  10 年累積折舊＝10.64×(1.02¹⁰－1)÷0.02＝116.51 萬（定額法同條件＝180 萬 → 初期減速）

只跑一次。每項斷言出現次數，對不上整支不寫檔。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
F = {k: ROOT / v for k, v in {
    "sys": "估價四大方法系統攻略.html",
    "calc": "估價_計算題攻略.html",
    "essay": "不動產估價概要_申論題實戰範文.html",
    "memo": "估價彩色重點速記.html"}.items()}
S = {k: p.read_text(encoding="utf-8") for k, p in F.items()}
fail = []


def rep(k, name, old, new, n_exp):
    n = S[k].count(old)
    if n != n_exp:
        fail.append(f"✗ {F[k].name}｜{name}：出現 {n} 次（應為 {n_exp}）")
        return
    S[k] = S[k].replace(old, new)
    print(f"  ✔ {F[k].name}｜{name}（{n} 處）")


# ① (1－s) 的小字標籤
for k, n in [("essay", 5), ("calc", 1), ("memo", 1)]:
    rep(k, "(1－s) 標籤", "(1－s)<small>殘餘價格率</small>", "(1－s)<small>1－殘餘價格率</small>", n)

# ② 分母標籤
rep("essay", "分母標籤", "(1＋i)ᴺ－1<small>複利終值係數</small>",
    "(1＋i)ᴺ－1<small>複利終值係數 (1＋i)ᴺ 再減 1</small>", 1)
rep("calc", "分母標籤", '(1+<mark class="kwm">i</mark>)ᴺ－1<small>複利終值係數</small>',
    '(1+<mark class="kwm">i</mark>)ᴺ－1<small>複利終值係數 (1+i)ᴺ 再減 1</small>', 1)
rep("essay", "分子標籤", "C×(1－s)×i<small>可折舊額 × 利率</small>",
    "C×(1－s)×i<small>應折舊總額 × 利率</small>", 1)
rep("calc", "分子標籤", "<small>可折舊額 C(1－s) × 利率</small>",
    "<small>應折舊總額 C(1－s) × 利率</small>", 1)

# ③ 速記：漏乘 C、右邊 dn
rep("memo", "速記償債基金式",
    '<span class="kf-fr"><span class="kf-c k-s">(1－s) × <mark class="kwm">i</mark><small>殘餘價格率 × 利率</small></span>'
    '<span class="fr-line"></span><span class="kf-c k-o">(1+<mark class="kwm">i</mark>)ᴺ－1<small>複利終值係數</small></span></span>'
    '<span class="kf-op">＝</span><span class="kf-c k-m">每年提存 dn</span>',
    '<span class="kf-fr"><span class="kf-c k-s">C × (1－s) × <mark class="kwm">i</mark><small>應折舊總額 × 利率</small></span>'
    '<span class="fr-line"></span><span class="kf-c k-o">(1+<mark class="kwm">i</mark>)ᴺ－1<small>複利終值係數 (1+i)ᴺ 再減 1</small></span></span>'
    '<span class="kf-op">＝</span><span class="kf-c k-m">每年提存額</span>', 1)

# ④ 系統攻略 ③ 整塊重寫
OLD_SYS = ('<div class="kf"><div class="kf-step"><div class="kf-t"><b>★</b>年折舊提存費占重建成本之比率（§40-1，每年等額提存）</div>'
           '<div class="kf-eq"><span class="kf-fr"><span class="kf-c k-s">(1－s)×i 殘餘價格率×利率</span><span class="fr-line"></span>'
           '<span class="kf-c k-o">(1＋i)ᴺ－1 複利終值係數</span></span><span class="kf-op">＝</span>'
           '<span class="kf-c k-m">C×(1－s)×i÷((1＋i)ᴺ－1)÷C</span></div>'
           '<div class="kf-ex">i＝利率　N＝耐用年數　s＝殘餘價格率（此為§40-1「折舊提存費」之比率）<br>'
           '⚠ §41 的「每年折舊提存率 d」＝i÷((1＋i)ⁿ′－1)，n′為<b>剩餘</b>耐用年數，與此不同，勿混用<br>'
           '概念：每年等額提存一筆錢到基金帳戶，到期累計剛好補足折舊金額（複利概念）</div></div></div>')
NEW_SYS = ('<div class="kf">'
           '<div class="kf-step"><div class="kf-t"><b>1</b>每年提存額（與 §40-1 收益法「折舊提存費・償債基金型」同一個算式）</div>'
           '<div class="kf-eq"><span class="kf-fr"><span class="kf-c k-s">C × (1－s) × i<small>應折舊總額 × 利率</small></span>'
           '<span class="fr-line"></span><span class="kf-c k-o">(1＋i)ᴺ－1<small>複利終值係數 (1＋i)ᴺ 再減 1</small></span></span>'
           '<span class="kf-op">＝</span><span class="kf-c k-m">每年提存額</span></div></div>'
           '<div class="kf-step"><div class="kf-t"><b>2</b>經歷 n 年的累積折舊額 Dn（成本法要的是這個）</div>'
           '<div class="kf-eq"><span class="kf-c k-s">C × (1－s)</span><span class="kf-op">×</span>'
           '<span class="kf-fr"><span class="kf-c k-o">(1＋i)ⁿ－1</span><span class="fr-line"></span><span class="kf-c k-o">(1＋i)ᴺ－1</span></span>'
           '<span class="kf-op">＝</span><span class="kf-c k-m">累積折舊額 Dn</span></div></div>'
           '<div class="kf-step"><div class="kf-t"><b>3</b>建物成本價格（§69）</div>'
           '<div class="kf-eq"><span class="kf-c k-s">C</span><span class="kf-op">－</span><span class="kf-c k-o">Dn</span>'
           '<span class="kf-op">＝</span><span class="kf-c k-m">建物成本價格</span></div></div>'
           '<div class="kf-ex">C＝建物總成本　s＝殘餘價格率（所以 1－s 是「要折舊掉的比率」）　i＝利率　'
           'N＝經濟耐用年數　n＝經歷年數<br>'
           '係數名稱別記混：(1＋i)ᴺ＝<b>複利終值係數</b>；i÷[(1＋i)ᴺ－1]＝<b>償債基金係數</b>；'
           '[(1＋i)ⁿ－1]÷i＝<b>複利年金終值係數</b>。第 2 式＝每年提存額 × 年金終值係數。<br>'
           '第 1 式為 §40-1 條文；第 2 式為教材公式（§68 只規定三種路徑，沒有列算式）。<br>'
           '⚠ §41 的「每年折舊提存率 d」＝i÷[(1＋i)ⁿ′－1]，n′為<b>剩餘</b>可收益年數，前面沒有 (1－s)，勿混用。</div></div>'
           '<p style="margin-top:10px;font-size:13px;"><b>計算範例</b>：C＝1,000 萬、s＝10%、i＝2%、N＝50 年，求經歷 10 年的累積折舊</p>'
           '<div class="cbox"><div class="cl">每年提存額＝900×0.02÷(1.02⁵⁰－1)≈<b>10.64 萬</b><br>'
           'Dn＝900×(1.02¹⁰－1)÷(1.02⁵⁰－1)≈<b class="rs">116.51 萬</b>（同條件定額法＝900÷50×10＝180 萬 → 初期折舊較少，就是「初期減速」）</div></div>')
rep("sys", "③ 整塊重寫", OLD_SYS, NEW_SYS, 1)
rep("sys", "③ 標籤", '<span class="freq">收益法折舊提存費用</span>',
    '<span class="freq">每年提存額同 §40-1</span>', 1)

if fail:
    print("\n".join(fail))
    sys.exit("\n有項目對不上，全部不寫檔。")
for k, p in F.items():
    p.write_text(S[k], encoding="utf-8")
print("寫入完成")
