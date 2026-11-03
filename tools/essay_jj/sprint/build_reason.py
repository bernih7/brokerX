# -*- coding: utf-8 -*-
"""經紀法規「申論 5 分鐘・推理版」：用邏輯拆解（推理鏈）＋考場速寫（得分關鍵詞／失分點／口訣）。內容一字不改。
用法：python3 build_reason.py demo   → demo/經紀法規_申論5分鐘_推理版_demo.html（3 張、不存紀錄）"""
import os, re, json, html, sys
import sys as _s, os as _o; _s.path.insert(0, _o.path.normpath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), '..', '..'))); import sprint_hp as _hp  # 115 高／中機率排序（11-03）
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from sprint_sx_law import annotate  # 速寫法條塊：條號＋本題名稱（11-03）
_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sx_law_names.json'); SXN = json.load(open(_f, encoding='utf-8')) if os.path.exists(_f) else {}

# 法條塊後備名稱：依本卡條文原文判斷是哪部法，取 law.json 的條文標題（｜後面）
_LAW = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'law.json'), encoding='utf-8'))
def jj_names(lj):
    from collections import Counter
    cnt = Counter()
    for s_ in lj['subs']:
        for st in s_['steps']:
            t = re.sub(r'\s+', '', st.get('law', ''))[:24]
            if len(t) < 10: continue
            for k, v in _LAW.items():
                if t in re.sub(r'\s+', '', v.get('text', '')): cnt[k.split(' ')[0]] += 1
    if not cnt: return {}
    law = cnt.most_common(1)[0][0]; out = {}
    for k, v in _LAW.items():
        if k.split(' ')[0] != law: continue
        art = k.split(' ', 1)[1].replace('之', '-'); nm = v.get('title', '').split('｜')[-1].strip()
        if nm and art.startswith('§'): out[art] = nm
    return out
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
hub = open(os.path.join(ROOT, '經紀法規_備考指揮中心.html'), encoding='utf-8').read()
LJ = {x['k']: x for x in json.load(open(os.path.join(ROOT, 'tools/essay_jj/lj_data.json'), encoding='utf-8'))}
GRP = {'a': '經紀業管理條例', 'c': '不動產說明書', 'd': '定型化契約', 'e': '公寓大廈管理', 'g': '公平交易法', 'h': '消費者保護法'}
def clean(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
def md(t):  # lj 的 **粗體** → <b>
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t, quote=False))

def card(cid):
    i = hub.find('<details id="%s"' % cid); j = hub.find('<details id="es-', i + 10); c = hub[i:j if j > 0 else len(hub)]
    a = c.find('<div class="vp" data-v="1"'); b = c.find('<div class="vp" data-v="0"', a); sx = c[a:b]
    blks = re.findall(r'<div class="blk (b\d)"><span class="blk-l">([^<]+)</span>(.*?)</div>(?=<div class="blk|<div class="kou|<div class="sk2)', sx, re.S)
    if not blks and '<div class="sk">' in sx:  # 模擬卷卡的速寫是 <h4>標題</h4><p>…</p>
        skh = sx[sx.find('<div class="sk">'):sx.find('<div class="sk2">') if '<div class="sk2">' in sx else len(sx)]
        hs = re.findall(r'<h4>(.*?)</h4>(.*?)(?=<h4>|</div>)', skh, re.S)
        blks = [('b%d' % (min(i, 3) + 1), re.sub(r'^[一二三四五六七八九十]+、', '', clean(h)), body) for i, (h, body) in enumerate(hs)]
    kou = re.search(r'<div class="kou"><b>口訣</b>(.*?)<small', sx, re.S)
    kws = [clean(x) for x in re.findall(r'<span class="kw">(.*?)</span>', sx)]
    lose = [clean(x) for x in re.findall(r'<li>(.*?)</li>', sx[sx.find('losebox'):]) ] if 'losebox' in sx else []
    q = re.search(r'class="essay-question">(.*?)</p>', c, re.S)
    lj = LJ[cid]
    pk = re.search(r'pk-([a-z])', c[:300]).group(1)
    cls = re.search(r'class="essay-detail ([^"]+)"', c[:300]).group(1).split()
    tier = 0 if 'tierA' in cls else 1 if 'tierB' in cls else 2 if 'tierC' in cls else 3
    kind = 'off' if cid.startswith('es-fw') else ('mock' if cid.startswith('es-mk') else 'pred')
    subs = [{'q': s['q'], 'pre': s.get('pre', ''), 'ans': md(s.get('ans', '')),
             'st': [{'ask': st.get('ask', ''), 'key': st.get('key', ''), 'lawh': st.get('lawh', ''), 'law': st.get('law', ''),
                     'facth': st.get('facth', ''), 'fact': st.get('fact', ''), 'res': st.get('res', ''), 'link': st.get('link', '')} for st in s['steps']]}
            for s in lj['subs']]
    return {'id': cid, 'no': clean(re.search(r'class="essay-num">(.*?)</span>', c).group(1)),
            't': clean(re.search(r'class="es-t">(.*?)</span>', c).group(1)), 'g': GRP.get(pk, ''),
            'q': re.sub(r'^【[^】]+】\s*', '', clean(q.group(1))) if q else '',
            'subs': subs, 'sx': [[bc, lab, annotate(body, [st for s_ in lj['subs'] for st in s_['steps']], jj_names(lj))[0] if lab.strip() == '法條' else body] for bc, lab, body in blks], 'kou': clean(kou.group(1)) if kou else '',
            'kws': kws, 'lose': lose, 'k': kind, 'tier': tier}

KWCN = json.load(open(os.path.join(H, 'kw_cn.json'), encoding='utf-8'))
ART = re.compile(r'§|第\s*\d+\s*條')
def kwfix(cid, kws):
    m = KWCN.get(cid, {}); out = []
    for k in kws:
        if k in m:
            if m[k] is None: continue
            out.append({'c': m[k], 'a': k})
        else:
            out.append({'c': k, 'a': ''})
    bad = [x['c'] for x in out if ART.search(x['c'])]
    return out, bad
ids = ['es-fw01', 'es-fw11', 'es-a1'] if 'demo' in sys.argv else [m for m in re.findall(r'<details id="(es-[^"]+)" class="essay-detail', hub)]
data = [card(x) for x in ids]
miss = {}
for d in data:
    d['kws'], bad = kwfix(d['id'], d['kws'])
    if bad: miss[d['id']] = bad
if miss:
    print('⚠ 關鍵詞仍是條號、尚無中文代表：', miss)
    if not ('demo' in sys.argv): sys.exit(1)
tpl = open(os.path.join(H, 'tpl_reason.html'), encoding='utf-8').read()
demo = 'demo' in sys.argv
out = tpl.replace('/*__DATA__*/[]', json.dumps(_hp.tag(data, 'jj'), ensure_ascii=False)).replace('/*__DEMO__*/false', 'true' if demo else 'false').replace('__ROOT__', '../' if demo else '')
dst = os.path.join(ROOT, 'demo', '經紀法規_申論5分鐘_推理版_demo.html') if demo else os.path.join(ROOT, '經紀法規_申論5分鐘_推理版.html')
open(dst, 'w', encoding='utf-8').write(out)
print(dst, len(data), [(d['id'], sum(len(s['st']) for s in d['subs']), len(d['kws']), len(d['lose'])) for d in data])
