# -*- coding: utf-8 -*-
"""陷阱題盤點：題庫解析含「陷阱／易混／混淆／偷換」的題，看定義填空有無對應卡（卡片 qk 含題號，或同法同條的卡）。"""
import re, json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
s = open(os.path.join(ROOT, 'bxj-quiz-data.js'), encoding='utf-8').read()
Q = json.loads(s[s.find('{'):s.rstrip().rstrip(';').rfind('}') + 1])['q']
f = open(os.path.join(ROOT, '經紀法規_定義填空練習.html'), encoding='utf-8').read(); i = f.find('const DATA = ') + 13
D, _ = json.JSONDecoder().raw_decode(f[i:])
cards = [x for c in D if c['id'][0] != 'S' for x in c['cards']]
QK = set(k for x in cards for k in x.get('qk', []) + x.get('mcx', []))
def norm_law(t):
    t = t.replace('經紀業條例', 'J').replace('施行細則', 'JS').replace('公寓大廈管理條例', 'P').replace('公寓', 'P').replace('公平法', 'G').replace('消保法', 'H')
    return t
ART = set()
for c in D:
    if c['id'][0] == 'S': continue
    dl = {'A': 'J', 'B': 'JS', 'E': 'P', 'F': 'P', 'G': 'G', 'H': 'H'}.get(c['id'], '')
    for x in c['cards']:
        cur = dl
        for m in re.finditer(r'([一-龥]*)§(\d+)(?:[-之](\d+))?', x['src']):
            nm = m.group(1)
            if '公寓' in nm: cur = 'P'
            elif '公平' in nm: cur = 'G'
            elif '消保' in nm: cur = 'H'
            elif '細則' in nm and c['id'] in 'AB': cur = 'JS'
            elif '條例' in nm and c['id'] in 'AB': cur = 'J'
            ART.add(cur + '§' + m.group(2) + ('-' + m.group(3) if m.group(3) else ''))
hit = [q for q in Q if re.search('陷阱|易混|混淆|偷換', json.dumps(q.get('exp', ''), ensure_ascii=False))]
res = {'qk': [], 'art': [], 'none': []}
for q in hit:
    if q['k'] in QK: res['qk'].append(q['k']); continue
    arts = []
    for l in q.get('law', []):
        m = re.match(r'(\S+) §(\d+)(?:之(\d+)|-(\d+))?', l)
        if not m: continue
        a = norm_law(m.group(1)) + '§' + m.group(2) + ('-' + (m.group(3) or m.group(4)) if (m.group(3) or m.group(4)) else '')
        arts.append(a)
    if arts and any(a in ART for a in arts): res['art'].append((q['k'], arts))
    else: res['none'].append(q)
print(len(hit), {k: len(v) for k, v in res.items()})
out = []
for q in res['none']:
    tr = [e for e in q['exp'] if re.search('陷阱|易混|混淆|偷換', e)]
    out.append('%s [%s] %s｜law:%s\n  陷阱：%s' % (q['k'], q['ch'], q['stem'][:70], q.get('law'), ' ◆ '.join(t[:220] for t in tr)))
open('/tmp/claude-0/-home-claude/db4af835-7730-5160-a7cd-81cabbdf283a/scratchpad/trap_none.txt', 'w').write('\n'.join(out))
open('/tmp/claude-0/-home-claude/db4af835-7730-5160-a7cd-81cabbdf283a/scratchpad/trap_art.txt', 'w').write('\n'.join('%s %s' % x for x in res['art']))
