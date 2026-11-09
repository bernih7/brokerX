# -*- coding: utf-8 -*-
"""11-09 使用者：「估價申論為什麼少了用分類類別的收納整理」——七類群組預設全部展開，一打開頁面就攤成一長串。
改為比照民法指揮中心申論分頁：類別預設收起（只看類別標頭：題數、115 預估、讀懂進度），點開才列題目；
搜尋、#卡號直達、「全部展開」仍會自動展開。可重跑。add_mock_cards.py／new_preds.py 的定位字串已同步改為不含 open。"""
import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '不動產估價概要_申論題實戰範文.html')
s = open(P, encoding='utf-8').read()
s, n = re.subn(r'<details class="tgroup" open data-g=', '<details class="tgroup" data-g=', s)
open(P, 'w', encoding='utf-8').write(s); print('收起', n, '組')
# 類別標頭在手機上排成一欄（標題→說明→題數→115→讀懂），不擠成窄條
CSS = '<style id="vgc-css">@media(max-width:600px){.tgroup>summary .g-head{flex:1 1 calc(100% - 28px)}.tgroup>summary .g-count{flex-basis:100%;padding-left:0;font-size:.76rem;color:var(--muted)}}</style>'
s = open(P, encoding='utf-8').read()
if 'id="vgc-css"' in s: s = re.sub(r'<style id="vgc-css">.*?</style>', CSS, s, flags=re.S)
else: s = s.replace('</head>', CSS + '\n</head>', 1)
open(P, 'w', encoding='utf-8').write(s)
