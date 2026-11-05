# -*- coding: utf-8 -*-
"""把 es_cards.py 的申論四段卡寫進《民法_定義填空練習》DATA（S1～S6，可重跑：先移除舊 S 章再加）。"""
import os, re, json, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
sys.path.insert(0, H)
from es_cards import G
P = os.path.join(ROOT, '民法_定義填空練習.html')
f = open(P, encoding='utf-8').read()
i = f.find('const DATA = ') + 13; D, e = json.JSONDecoder().raw_decode(f[i:])
assert json.dumps(D, ensure_ascii=False, indent=1) == f[i:i + e]
D = [c for c in D if c['id'][0] != 'S']
RS = open(os.path.join(ROOT, '民法_申論5分鐘_推理版.html'), encoding='utf-8').read()
SP = open(os.path.join(ROOT, '民法_申論5分鐘衝刺.html'), encoding='utf-8').read()
RID = set(re.findall(r'"id": ?"([^"]+)"', RS)); SID = set(re.findall(r'"id": ?"([^"]+)"', SP))
L = [('e1', '問題定義'), ('e2', '法條定義'), ('e3', '問題核心'), ('e4', '結論'), ('e5', '結尾卓見')]
def conv(s):
    return re.sub(r'\[\[(.+?)\]\]', '___', s), re.sub(r'\[\[(.+?)\]\]', r'<span class="key">\1</span>', s)
n = 0
for k, (lab, cards) in enumerate(G.items(), 1):
    out = []
    for c in cards:
        parts = [re.sub(r'；(?![^\[]*\]\])', '；<br>', x) for x in (c['d'], c['l'], c['c'], c['z'], c['zj'])]
        secs = ''.join('<div class="esb %s"><span class="esl"%s>%s</span><div class="esc">%s</div></div>'
                       % (L[j][0], ' title="卓見為自編收尾句，非法條"' if j == 4 else '', L[j][1], parts[j]) for j in range(5))
        b, a = conv(secs)
        assert b.count('___') == a.count('class="key"'), c['t']
        x = {'term': c['t'], 'blank': b, 'answer': a, 'src': c['src'], 'mc': 0, 'es': c['es'],
             'es5': [[q, q if q in RID else '', q if q in SID else ''] for q in c['es']]}
        if c.get('m'): x['m'] = c['m']
        out.append(x); n += 1
    D.append({'id': 'S%d' % k, 'label': lab, 'cards': out})
f = f[:i] + json.dumps(D, ensure_ascii=False, indent=1) + f[i + e:]
open(P, 'w', encoding='utf-8').write(f)
nd = sum(len(c['cards']) for c in D if c['id'][0] != 'S')
print('申論四段', n, '張；定義', nd, '張')
