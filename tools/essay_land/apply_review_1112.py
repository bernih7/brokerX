# -*- coding: utf-8 -*-
"""11-12 四位審稿者（只審不改）對 92 張土地法申論卡的 528 項修正，套到所有版本：
總覽頁、src.html、essays.json、exam_ver*.json、lj_data.json、5 分鐘衝刺／推理版的 CARDS。
比對方式：old 是去標籤後的文字，逐字之間允許夾 HTML 標籤；只在該卡範圍內取代。不可重跑（套完 old 就不在了，會自動略過）。"""
import json, re, os, sys, collections
R = os.path.join(os.path.dirname(__file__), '..', '..')
F = lambda p: os.path.join(R, p)
A = json.load(open(F(sys.argv[1] if len(sys.argv) > 1 else 'tools/essay_land/review_1112.json'), encoding='utf-8'))
SKIP = [x for x in A if re.search(r'待補核|待查', x['new'])]
A = [x for x in A if x not in SKIP]
SEP = r'(?:<[^<>]*>|&lt;[^&]*?&gt;)*'
def rx(old):
    return re.compile(SEP.join(re.escape(c) for c in old))
def sub(s, x):
    r = rx(x['old']); n = len(r.findall(s))
    return (r.sub(lambda m: x['new'], s), n) if n else (s, 0)
by = collections.defaultdict(list)
for x in A: by[x['id']].append(x)
for k in by: by[k].sort(key=lambda x: -len(x['old']))
ES = json.load(open(F('tools/essay_land/data/essays.json'), encoding='utf-8'))
def k_of(cid):
    a, b = cid.split('-', 1)
    return {'q': b, 'pr': 'P' + b, 'mk': 'K' + b, 'x': 'X' + b}[a]
KEY = {cid: k_of(cid) for cid in by}
hit = collections.Counter(); miss = []
inv = {v: k for k, v in KEY.items()}
def walk(o, xs, tag):
    if isinstance(o, str):
        for x in xs:
            o, n = sub(o, x)
            if n: hit[(tag, id(x))] += n; x.setdefault('_hit', set()).add(tag)
        return o
    if isinstance(o, list): return [walk(v, xs, tag) for v in o]
    if isinstance(o, dict): return {k: walk(v, xs, tag) for k, v in o.items()}
    return o
# 1) 總覽頁與 src.html：卡片區塊
for f in ['土地法_申論題分類總覽.html', 'tools/essay_land/src.html']:
    s = open(F(f), encoding='utf-8').read()
    for cid, xs in by.items():
        m = re.search(r'<[a-z]+ [^>]*?id="%s"' % re.escape(cid), s)
        if not m: continue
        nx = re.search(r'<[a-z]+ [^>]*?id="(?:q|pr|mk|x)-', s[m.end():])
        a, b = m.start(), (m.end() + nx.start()) if nx else len(s)
        blk = s[a:b]
        for x in xs:
            blk, n = sub(blk, x)
            if n: x.setdefault('_hit', set()).add(f)
        s = s[:a] + blk + s[b:]
    open(F(f), 'w', encoding='utf-8').write(s)
# 2) essays.json
ES = [walk(e, by.get(e.get('idv')) or by.get(inv.get(e.get('key')), []), 'essays') for e in ES]
json.dump(ES, open(F('tools/essay_land/data/essays.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 3) exam_ver*.json、lj_data.json
for f in ['exam_ver.json', 'exam_ver_off.json', 'exam_ver_more.json']:
    p = F('tools/essay_land/data/' + f); d = json.load(open(p, encoding='utf-8'))
    for cid, xs in by.items():
        k = KEY.get(cid)
        if k in d: d[k] = walk(d[k], xs, f)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
p = F('tools/essay_land/data/lj_data.json'); d = json.load(open(p, encoding='utf-8'))
d = [walk(c, by.get(inv.get(c.get('k')), []), 'lj') for c in d]
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# 4) 衝刺／推理版 CARDS
for f in ['土地法_申論5分鐘衝刺.html', '土地法_申論5分鐘_推理版.html']:
    s = open(F(f), encoding='utf-8').read(); i = s.index('var CARDS=') + 10
    C, e = json.JSONDecoder().raw_decode(s[i:]); seg = s[i:i + e]
    C = [walk(c, by.get(c['id'], []), f) for c in C]
    out = json.dumps(C, ensure_ascii=False)
    if '<\\/' in seg: out = out.replace('</', '<\\/')
    s = s[:i] + out + s[i + e:]
    open(F(f), 'w', encoding='utf-8').write(s)
nohit = [x for x in A if '土地法_申論題分類總覽.html' not in x.get('_hit', ())]
print('套用', len(A), '｜總覽沒套到', len(nohit), '｜略過（待補核）', len(SKIP))
for x in nohit: print('  NOHIT', x['id'], x['where'], x['old'][:30])
print(collections.Counter(t for x in A for t in x.get('_hit', ())))
