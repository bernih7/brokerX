# -*- coding: utf-8 -*-
"""土地法「申論 5 分鐘衝刺」：從《土地法_申論題分類總覽》的考場版＋ lj_data.json 關鍵檢核產生。內容一字不改，只換呈現方式。
可重跑：python3 tools/essay_land/sprint/build_sprint.py
紀錄：bx-land-es-log（與總覽頁共用：輪數／秒數／自評）＋ bx-land-es-sprint（每次衝刺分數）。"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from common import *
import sprint_hp as _hp
def blk(h, body):
    ps = [p for p in re.split(r'<br\s*/?>', body) if p.strip()]
    return '<span class="blk-l">%s</span>%s' % (h, ''.join('<p>%s</p>' % p for p in ps))
out = []
for x in cards():
    cid, c, a = x['id'], x['c'], x['a']; lj = LJ[ljkey(cid)]
    out.append({'id': cid, 'no': no(cid), 't': clean(re.search(r'<b class="et">(.*?)</b>', c).group(1)), 'lv': a.get('lv', ''),
                'k': kind(cid, a), 'tier': tier(a), 'g': x['g'], 'q': q_of(c), 'nq': len(lj.get('subs', [])) or 1,
                'b': [blk(h, body) for _, h, body in ev_blocks(c)],
                'ck': [{'x': ck['txt'], 'h': bool(ck.get('hot'))} for ck in lj.get('checks', [])], 'mn': lj.get('mnem', '')})
miss = [c['id'] for c in out if not c['ck']]; assert not miss, ('缺檢核', miss)
tpl = open(os.path.join(H, 'tpl.html'), encoding='utf-8').read()
open(os.path.join(ROOT, '土地法_申論5分鐘衝刺.html'), 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/[]', json.dumps(_hp.tag(out, 'land'), ensure_ascii=False)))
print('土地法 申論 5 分鐘衝刺：', len(out), '張；檢核項', sum(len(c['ck']) for c in out))
