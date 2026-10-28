#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
申論頁標示修正（2026-10-28）：

一、版本鈕「完整四段式」名實不符 → 改「完整版」，三顆鈕各加 title 說明。
   盤點結果：**32 張官方卡大多是「依題目小題分段」**（題目問三件事就分三段），
   只有預測卡是嚴格的定義→法條→涵攝→結論。依題目分段在考場才是對的作法，
   內容沒有問題，是**按鈕名稱**會讓人以為每張都是四段。

二、順手修掉三個寫死而且已經過期的數字（本來就錯，不是這次改出來的）：
   stats-bar 總題數 53 → 54（實際卡數）
   stats-bar 預測 **14** → 22（頁上早就有 21 張，這個數字停在很久以前）
   header 副標 21 題預測 → 22，並把「四段式架構」改成誠實的寫法

可重複執行。改完要重跑 gen_lj.py 才會套用到 54 張卡的版本鈕。
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAGE = ROOT / "不動產估價概要_申論題實戰範文.html"
GEN = HERE / "gen_lj.py"

EDITS = [
    (GEN,
     '''<button class="ver-btn" data-ver="full" onclick="setVer(this.closest(\\'.essay-card\\'),\\'full\\')">完整四段式</button>''',
     '''<button class="ver-btn" data-ver="full" title="完整範文。預測題為定義→法條→涵攝→結論四段；官方題依題目小題分段（題目問幾件事就分幾段）" onclick="setVer(this.closest(\\'.essay-card\\'),\\'full\\')">完整版</button>'''),
    (GEN,
     '''<button class="ver-btn active" data-ver="lj" onclick="setVer(this.closest(\\'.essay-card\\'),\\'lj\\')">邏輯拆解</button>''',
     '''<button class="ver-btn active" data-ver="lj" title="一步一步推：問一句→條文／公式→本題→小結，附採分點勾選" onclick="setVer(this.closest(\\'.essay-card\\'),\\'lj\\')">邏輯拆解</button>'''),
    (GEN,
     '''<button class="ver-btn" data-ver="quick" onclick="setVer(this.closest(\\'.essay-card\\'),\\'quick\\')">考場速寫</button>''',
     '''<button class="ver-btn" data-ver="quick" title="考場上來不及時的最小可得分版本：公式、代入、常見失分點、得分關鍵詞" onclick="setVer(this.closest(\\'.essay-card\\'),\\'quick\\')">考場速寫</button>'''),

    (PAGE,
     '<div class="sub">32題完整版＋21題預測（A/B/C三級）· 四段式架構（定義→法條→涵攝→結論）· 99–114年</div>',
     '<div class="sub">官方32題＋預測22題（A/B/C三級）· 預測題為四段式（定義→法條→涵攝→結論），'
     '官方題依題目小題分段 · 99–114年</div>'),
    (PAGE, '<span class="stat-chip">總題數 <strong>53</strong></span>',
           '<span class="stat-chip">總題數 <strong>54</strong></span>'),
    (PAGE, '<span class="stat-chip stat-pred">預測 <strong>14</strong></span>',
           '<span class="stat-chip stat-pred">預測 <strong>22</strong></span>'),
]


def main():
    for path, old, new in EDITS:
        s = path.read_text(encoding="utf-8")
        if new in s:
            print(f"  － {path.name}：已是新版")
            continue
        if s.count(old) != 1:
            sys.exit(f"✗ {path.name}：原文出現 {s.count(old)} 次 → {old[:50]}…")
        path.write_text(s.replace(old, new, 1), encoding="utf-8")
        print(f"  ✔ {path.name}：{old[:46]}… 已更新")


if __name__ == "__main__":
    main()
