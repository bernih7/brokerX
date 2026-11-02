# -*- coding: utf-8 -*-
"""2026-11-02 使用者：102-29 解析很爛 → 依消保法 §50～§53 逐字重寫。可重跑。"""
import io, json, os, re, subprocess
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
J = os.path.join(ROOT, 'tools', 'essay_jj')
K = '102-29'
EXP = [
 '正確。§50Ⅰ逐字：「消費者保護團體對於同一之原因事件，致使眾多消費者受害時，得受讓『二十人以上』消費者損害賠償請求權後，以自己名義，提起訴訟。」白話：消保團體先向受害人收齊 20 人以上的請求權，再用團體自己的名義去告。之後有人終止讓與、人數掉到 20 人以下，也不影響訴訟（§50Ⅱ）。',
 '錯在「不包括」。§50Ⅲ逐字：「第一項讓與之損害賠償請求權，『包括』民法第一百九十四條、第一百九十五條第一項非財產上之損害。」白話：精神上的損害（慰撫金）也可以一起讓給消保團體去求償，不是只有財產損害。',
 '錯在倍數。§51：因企業經營者「過失」所致之損害，得請求損害額「一倍以下」之懲罰性賠償金；「三倍以下」是「重大過失」，「五倍以下」是「故意」。口訣：故意五、重過三、過失一。',
 '錯在把兩條的裁判費混在一起。前段「訴請停止或禁止之」是§53Ⅰ的不作為訴訟，§53Ⅱ規定這種訴訟「免繳裁判費」（不分金額，全部免繳）；「標的價額超過新臺幣六十萬元者，超過部分免繳裁判費」是§52，適用於消保團體依§50 提起的「損害賠償」團體訴訟。',
]
REF = '消費者保護法§50（團體訴訟：受讓二十人以上請求權、以自己名義起訴；讓與範圍包括非財產上損害）、§51（懲罰性賠償金：故意五倍、重大過失三倍、過失一倍以下）、§52（依§50起訴，標的價額超過六十萬元部分免繳裁判費）、§53（不作為訴訟，免繳裁判費）'
LAW = ['消保法 §50', '消保法 §51', '消保法 §52', '消保法 §53']
HL = [['『二十人以上』'], ['『包括』'], ['「一倍以下」', '故意五、重過三、過失一'], ['不分金額，全部免繳']]
for i, ps in enumerate(HL):
    for p in ps: assert p in EXP[i], (i, p)
full = json.load(io.open(os.path.join(J, 'law', 'lawfull.json'), encoding='utf-8'))
# quiz_data.json
qp = os.path.join(J, 'quiz_data.json'); old = io.open(qp, encoding='utf-8').read(); D = json.loads(old)
for x in D['q']:
    if x['k'] == K: x['exp'] = EXP; x['ref'] = REF; x['law'] = LAW
for k in LAW:
    if k not in D['law']: D['law'][k] = {'t': full[k].get('title', ''), 'x': full[k]['text'], 'v': full[k]['verbatim']}
new = json.dumps(D, ensure_ascii=False, indent=1); io.open(qp, 'w', encoding='utf-8').write(new)
# 法條解析練習：嵌入資料整段換掉
f = os.path.join(ROOT, '經紀法規_法條解析練習.html'); s = io.open(f, encoding='utf-8').read()
if old != new:
    assert s.count(old) == 1; s = s.replace(old, new); io.open(f, 'w', encoding='utf-8').write(s)
# 刷題 H3_1
f = os.path.join(ROOT, '經紀法規刷題練習_H3_1.html'); s = io.open(f, encoding='utf-8').read()
m = re.search(r'(const QUESTIONS = )(\[.*?\])(;\n)', s, re.S); qs = json.loads(m.group(2))
assert json.dumps(qs, ensure_ascii=False) == m.group(2)
for q in qs:
    if q['year'] == 102 and q['qnum'] == 29: q['explains'] = dict(zip('ABCD', EXP)); q['ref'] = REF
s = s[:m.start(2)] + json.dumps(qs, ensure_ascii=False) + s[m.end(2):]; io.open(f, 'w', encoding='utf-8').write(s)
# 黃底
hp = os.path.join(ROOT, 'tools', 'jj_hl', 'hl_data.json'); H = json.load(io.open(hp, encoding='utf-8')); H[K] = HL
json.dump(H, io.open(hp, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
print('ok')
