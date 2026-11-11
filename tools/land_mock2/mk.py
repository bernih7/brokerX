# -*- coding: utf-8 -*-
"""產生 土地法_診斷卷二.html：沿用 土地法_診斷卷一.html 的版型，換資料、加計時與申論分頁。"""
import json, re, sys, collections, os
sys.path.insert(0, os.path.dirname(__file__))
from data import Q, E
ROOT = os.path.join(os.path.dirname(__file__), '..', '..')
L = "ABCD"
# ---- 檢查 ----
err = []
cnt = collections.Counter(q['ch'] for q in Q)
want = dict(A=8, B=3, C=3, D=4, E=3, F=1, G=2, H=1)
if dict(cnt) != want: err.append(('配比', dict(cnt)))
for i, q in enumerate(Q, 1):
    if q['n'] != i: err.append((i, '題號'))
    if len(q['opts']) != 4 or len(q['notes']) != 4: err.append((i, '選項數'))
    k = L.index(q['ans'])
    neg = q.get('neg', False)
    marks = [x[0] for x in q['notes']]
    # 正向題：答案 ✅、其餘 ❌；問錯誤題：答案 ❌、其餘 ✅
    exp = ['❌' if (j == k) == neg else '✅' for j in range(4)]
    if marks != exp: err.append((i, '對錯標記', marks, exp))
    if neg != bool(re.search(r'錯誤|非屬|不包括|不屬', q['stem'])): err.append((i, '題幹正負', neg))
if err:
    print('\n'.join(map(str, err))); sys.exit(1)
print('配比', dict(cnt), '答案分布', collections.Counter(q['ans'] for q in Q), '問錯誤', sum(q.get('neg', False) for q in Q))

# ---- 組頁 ----
src = open(os.path.join(ROOT, '土地法_診斷卷一.html'), encoding='utf-8').read()
D = dict(Q=[dict(q, neg=False) for q in Q], E=E, timer=True)   # 不顯示「問錯誤」標籤：考場不會提示
i = src.index('var D=') + 6
_, end = json.JSONDecoder().raw_decode(src[i:])
rest = src[i + end:]
assert rest.startswith(',ID="landdiag1";')
out = src[:i] + json.dumps(D, ensure_ascii=False) + ',ID="landdiag2";' + rest[len(',ID="landdiag1";'):]
out = out.replace('<title>土地法診斷卷①</title>', '<title>土地法診斷卷②</title>', 1)
old_h = re.search(r'<header><h1>土地法診斷卷①</h1><div class="sub">.*?</div></header>', out).group(0)
new_h = ('<header><h1>土地法診斷卷②</h1><div class="sub">全真模擬：單選 25 題（每題 2 分）＋申論 2 題（各 25 分），可計時 90 分鐘'
         '｜配題依 107–114 年占比：A8／B3／C3／D4／E3／F1／G2／H1｜題幹仿考選部寫法：10 題問「錯誤／非屬」、長敘述選項、中文數字，題目上不另標示'
         '｜考點與診斷卷①不重複｜答錯可歸類 A 法條混淆／B 粗心／C 真的不熟｜答案已對照現行條文（2026-11-11）</div></header>')
out = out.replace(old_h, new_h, 1)
assert out.count('landdiag1') == 0, out.count('landdiag1')
open(os.path.join(ROOT, '土地法_診斷卷二.html'), 'w', encoding='utf-8').write(out)
print('ok', len(out))
