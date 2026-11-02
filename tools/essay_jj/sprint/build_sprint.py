# -*- coding: utf-8 -*-
"""經紀法規「申論 5 分鐘衝刺」頁：從指揮中心申論卡（考場版）＋ lj_data.json（關鍵檢核 checks）產生。
內容一字不改，只換呈現方式。可重跑：python3 tools/essay_jj/sprint/build_sprint.py
紀錄與指揮中心同步：bxj-es-log（輪數／秒數／自評，與申論卡共用）＋ bxj-es-sprint（每次衝刺分數）。"""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
hub = open(os.path.join(ROOT, '經紀法規_備考指揮中心.html'), encoding='utf-8').read()
LJ = {x['k']: x for x in json.load(open(os.path.join(ROOT, 'tools/essay_jj/lj_data.json'), encoding='utf-8'))}
GRP = {'a': '經紀業管理條例', 'c': '不動產說明書', 'd': '定型化契約', 'e': '公寓大廈管理', 'g': '公平交易法', 'h': '消費者保護法'}
TIER = {'tierA': 0, 'tierB': 1, 'tierC': 2}

def clean(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()

cards = []
ms = list(re.finditer(r'<details id="(es-[^"]+)" class="essay-detail ([^"]+)">', hub))
for n, m in enumerate(ms):
    cid, cls = m.group(1), m.group(2)
    end = ms[n + 1].start() if n + 1 < len(ms) else len(hub)
    c = hub[m.start():end]
    a = c.find('<div class="vp ev" data-v="4" hidden>'); b = c.find('<!--/ev-->', a)
    assert a > 0 and b > 0, cid
    ev = c[a + len('<div class="vp ev" data-v="4" hidden>'):b]
    ev = ev[:ev.rfind('</div>')]  # 去掉外層 div 的結尾
    blocks = re.findall(r'<div class="blk (b\d)">(.*?)</div>(?=<div class="blk b\d">|$)', ev, re.S)
    assert len(blocks) == 4, (cid, len(blocks))
    q = re.search(r'class="essay-question">(.*?)</p>', c, re.S)
    qt = clean(q.group(1)) if q else ''
    qt = re.sub(r'^【[^】]+】\s*', '', qt)
    lj = LJ.get(cid, {})
    kind = 'off' if cid.startswith('es-fw') else ('mock' if cid.startswith('es-mk') else 'pred')
    tier = next((TIER[t] for t in TIER if t in cls.split()), 3)
    pk = re.search(r'pk-([a-z])', cls).group(1)
    cards.append({
        'id': cid,
        'no': clean(re.search(r'class="essay-num">(.*?)</span>', c).group(1)),
        't': clean(re.search(r'class="es-t">(.*?)</span>', c).group(1)),
        'lv': clean(re.search(r'class="es-lv[^"]*">(.*?)</span>', c).group(1)) if 'class="es-lv' in c else '',
        'k': kind, 'tier': tier, 'g': GRP.get(pk, ''), 'q': qt,
        'nq': len(lj.get('subs', [])) or 1,
        'b': [blk for _, blk in blocks],
        'ck': [{'x': ck['txt'], 'h': bool(ck.get('hot'))} for ck in lj.get('checks', [])],
        'mn': lj.get('mnem', ''),
    })
miss = [c['id'] for c in cards if not c['ck']]
assert not miss, ('缺檢核', miss)

tpl = open(os.path.join(H, 'tpl.html'), encoding='utf-8').read()
out = tpl.replace('/*__DATA__*/[]', json.dumps(cards, ensure_ascii=False))
open(os.path.join(ROOT, '經紀法規_申論5分鐘衝刺.html'), 'w', encoding='utf-8').write(out)
print('申論 5 分鐘衝刺：', len(cards), '張；檢核項', sum(len(c['ck']) for c in cards))
