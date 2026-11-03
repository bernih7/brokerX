# -*- coding: utf-8 -*-
"""土地法 5 分鐘衝刺／推理版共用：從《土地法_申論題分類總覽》頁（考場版、考場速寫）＋ data/lj_data.json 取資料。內容一字不改。"""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
PAGE = open(os.path.join(ROOT, '土地法_申論題分類總覽.html'), encoding='utf-8').read()
LJ = {x['k']: x for x in json.load(open(os.path.join(ROOT, 'tools/essay_land/data/lj_data.json'), encoding='utf-8'))}
def clean(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
def ljkey(cid):
    p, n = cid.split('-', 1)
    return {'pr': 'P' + n, 'q': n, 'x': 'X' + n, 'mk': 'K' + n}[p]
def no(cid):
    p, n = cid.split('-', 1)
    return {'pr': '預P' + n, 'q': n, 'x': '專' + n, 'mk': '模' + n}[p]
GRPS = [(m.start(), m.group(1), clean(m.group(2))) for m in re.finditer(r'<details class="grp" id="cat-(\w+)"[^>]*>\s*<summary><span class="gl">\w+</span><span class="gname">([^<]*)</span>', PAGE, re.S)]
def cards():
    out = []
    ms = list(re.finditer(r'<details class="es[^"]*" id="([^"]+)"([^>]*)>', PAGE))
    for n, m in enumerate(ms):
        cid, attr = m.group(1), m.group(2)
        c = PAGE[m.start():ms[n + 1].start() if n + 1 < len(ms) else len(PAGE)]
        g = ''
        for pos, k, nm in GRPS:
            if pos < m.start(): g = nm
        a = dict(re.findall(r'data-(\w+)="([^"]*)"', attr))
        out.append(dict(id=cid, c=c, a=a, g=g))
    return out
def ev_blocks(c):
    a = c.find('<div class="vp" data-v="4"'); b = c.find('<div class="vp" data-v="0"', a)
    bl = re.findall(r'<details class="blk (b\d)"[^>]*><summary><h5>(.*?)</h5></summary><div class="fdb">(.*?)</div></details>', c[a:b], re.S)
    return [(bc, h, body) for bc, h, body in bl]
def q_of(c):
    q = re.search(r'<div class="oq">(.*?)</div>', c, re.S).group(1)
    return clean(re.sub(r'^\s*<b>.*?</b>\s*：', '', q))
def kind(cid, a):
    return 'mock' if cid.startswith('mk-') else ('off' if a.get('k') == 'off' else 'pred')
def tier(a):
    try: return max(0, 3 - int(a.get('pr', '0')))
    except ValueError: return 3
