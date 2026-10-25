# -*- coding: utf-8 -*-
"""把《經紀法規_模擬試題一_曾榮耀》的 25 題選擇題併進 quiz_data.json，標題源 sr='mock'。
官方 520 題不受影響：正確率分開算、智慧配題權重只用官方、錯題本共用。
可重複執行。"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(ROOT, '經紀法規_模擬試題一_曾榮耀.html')
QD = os.path.join(HERE, 'quiz_data.json')

# 章節歸類（依題幹主題，對照 chapters.json）
CH = {1: 'A2', 2: 'A5', 3: 'A4', 4: 'A2', 5: 'A3', 6: 'A4', 7: 'A4',
      8: 'D2', 9: 'D3',
      10: 'G1', 11: 'G1', 12: 'G1', 13: 'G1',
      14: 'H3', 15: 'H1', 16: 'H3', 17: 'H3', 18: 'H2',
      19: 'E2', 20: 'E2', 21: 'E3', 22: 'E3', 23: 'E3', 24: 'E1', 25: 'E5'}

# 本題相關法條（只掛條文庫裡確實有的；沒把握就留空）
LAW = {
 1: ['經紀業條例 §5', '經紀業條例 §7', '經紀業條例 §30'],
 2: ['經紀業條例 §6'],
 3: ['經紀業條例 §29', '經紀業條例 §31'],
 4: ['經紀業條例 §11', '經紀業條例 §12'],
 5: ['經紀業條例 §13', '經紀業條例 §14', '經紀業條例 §15'],
 6: ['經紀業條例 §22', '經紀業條例 §23', '經紀業條例 §24'],
 7: ['經紀業條例 §16', '經紀業條例 §17', '經紀業條例 §26'],
 10: ['公平法 §7', '公平法 §8', '公平法 §9'],
 11: ['公平法 §20'],
 12: ['公平法 §14', '公平法 §15', '公平法 §16'],
 13: ['公平法 §21'],
 15: ['消保法 §11之1', '消保法 §12', '消保法 §17'],
 16: ['消保法 §49', '消保法 §50'],
 17: ['消保法 §43', '消保法 §44', '消保法 §45'],
 18: ['消保法 §19', '消保法 §20'],
 20: ['公寓大廈 §21', '公寓大廈 §22'],
 21: ['公寓大廈 §18', '公寓大廈 §27'],
 22: ['公寓大廈 §30', '公寓大廈 §31', '公寓大廈 §32'],
 23: ['公寓大廈 §18', '公寓大廈 §57', '公寓大廈 §58'],
 25: ['公寓大廈 §47', '公寓大廈 §49'],
}

s = io.open(SRC, encoding='utf-8').read()
D0 = json.loads(re.search(r'var D=(\{[\s\S]*?\});\n', s).group(1))
SRCNOTE = '補習班模擬卷：《不動產經紀相關法規概要》模擬試題一，出題 曾榮耀（解答卷類科【永慶】，使用者提供照片）第 %d 題。解析由本站依老師解答與現行條文整理。'

D = json.load(io.open(QD, encoding='utf-8'))
D['q'] = [q for q in D['q'] if q.get('sr') != 'mock']          # 可重複執行
have = set(D['law'])
add, skip = [], {}
for x in D0['Q']:
    n = x['n']
    laws = [L for L in LAW.get(n, []) if L in have]
    miss = [L for L in LAW.get(n, []) if L not in have]
    if miss:
        skip[n] = miss
    exp = list(x.get('notes') or [])
    while len(exp) < 4:
        exp.append('')
    if x.get('trap'):
        i = 'ABCD'.index(x['ans'])
        exp[i] = (exp[i] + '　【陷阱】' + x['trap']).strip('　')
    add.append({'k': 'mk-%d' % n, 'y': 0, 'n': n, 'ch': CH[n], 'sr': 'mock',
                'stem': x['stem'], 'opt': x['opts'], 'ans': x['ans'],
                'exp': exp[:4], 'ref': SRCNOTE % n, 'law': laws})
D['q'] = D['q'] + add
json.dump(D, io.open(QD, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

off = [q for q in D['q'] if q.get('sr') != 'mock']
mk = [q for q in D['q'] if q.get('sr') == 'mock']
print('官方 %d 題｜補習班 %d 題｜合計 %d' % (len(off), len(mk), len(D['q'])))
print('有相關法條的補習班題：%d／%d' % (len([q for q in mk if q['law']]), len(mk)))
if skip:
    print('條文庫沒有、已略過：', {k: v for k, v in skip.items()})
import collections
print('章節分布：', dict(collections.Counter(q['ch'] for q in mk)))
