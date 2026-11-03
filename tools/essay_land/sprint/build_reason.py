# -*- coding: utf-8 -*-
"""土地法「申論 5 分鐘・推理版」：邏輯拆解（推理鏈，lj_data.json）＋考場速寫（總覽頁的速寫四段、關鍵詞、失分點、口訣）。內容一字不改。
可重跑：python3 tools/essay_land/sprint/build_reason.py"""
import os, sys, json, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from common import *
import sprint_hp as _hp
def md(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t, quote=False))
LAB = {'定義': '定義', '法條': '法條', '涵攝': '涵攝', '結論': '結論'}
def sx_of(c):
    a = c.find('<div class="vp" data-v="1"'); b = c.find('<div class="vp" data-v="0"', a); sx = c[a:b]
    segs = re.findall(r'<div class="seg[^"]*"><b class="t">[①②③④]\s*(\S+?)</b>(.*?)</div>(?=<div class="seg|<p class="nt"|<p class="kou2"|<div class="sk2"|</div><div class="vp")', sx, re.S)
    res = []
    for i, (lab, body) in enumerate(segs):
        if lab == '涵攝': body = re.sub(r'(?<!^)(（[二三四五六七八九十]）)', r'<br>\1', body)
        res.append(['b%d' % (i + 1), lab, '<p>%s</p>' % body])
    kws = [{'c': clean(k), 'a': ''} for k in re.findall(r'<i>(.*?)</i>', sx[sx.find('class="kwc"'):sx.find('</div>', sx.find('class="kwc"'))])] if 'class="kwc"' in sx else []
    lose = [clean(k) for k in re.findall(r'<li>(.*?)</li>', sx[sx.find('class="lose"'):])] if 'class="lose"' in sx else []
    return res, kws, lose
data = []
for x in cards():
    cid, c, a = x['id'], x['c'], x['a']; lj = LJ[ljkey(cid)]
    sx, kws, lose = sx_of(c)
    assert len(sx) == 4, (cid, len(sx))
    subs = [{'q': s['q'], 'pre': s.get('pre', ''), 'ans': md(s.get('ans', '')),
             'st': [{k: st.get(k, '') for k in ('ask', 'key', 'lawh', 'law', 'facth', 'fact', 'res', 'link')} for st in s['steps']]} for s in lj['subs']]
    data.append({'id': cid, 'no': no(cid), 't': clean(re.search(r'<b class="et">(.*?)</b>', c).group(1)), 'g': x['g'], 'q': q_of(c),
                 'subs': subs, 'sx': sx, 'kou': lj.get('mnem', ''), 'kws': kws, 'lose': lose, 'k': kind(cid, a), 'tier': tier(a)})
tpl = open(os.path.join(H, 'tpl_reason.html'), encoding='utf-8').read()
s = tpl.replace('/*__DATA__*/[]', json.dumps(_hp.tag(data, 'land'), ensure_ascii=False)).replace('/*__DEMO__*/false', 'false').replace('__ROOT__', '')
open(os.path.join(ROOT, '土地法_申論5分鐘_推理版.html'), 'w', encoding='utf-8').write(s)
print('土地法 推理版：', len(data), '張；步驟', sum(len(s_['st']) for d in data for s_ in d['subs']), '；無關鍵詞', [d['id'] for d in data if not d['kws']], '；無失分點', [d['id'] for d in data if not d['lose']])
