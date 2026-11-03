# -*- coding: utf-8 -*-
"""經紀法規申論「考場版」：讀 ev_*.json，插入指揮中心官方申論卡（分頁：邏輯拆解｜考場速寫｜考場版｜完整四段式）。
規格依《備考_跨科同步施工單_申論考場版_20261102》。可重跑（先移除舊的考場版再插入）。"""
import io, json, os, re, glob, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
F = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
EV = {}
for f in sorted(glob.glob(os.path.join(H, 'ev_*.json'))): EV.update(json.load(io.open(f, encoding='utf-8')))
s = io.open(F, encoding='utf-8').read()
# 移除舊版
s = re.sub(r'<button type="button" class="vt" data-v="4">考場版</button>', '', s)
s = re.sub(r'<div class="vp ev" data-v="4" hidden>.*?</div><!--/ev-->', '', s, flags=re.S)
ART = re.compile(r'(§\s*\d+(?:之\d+)?|第\s*\d+\s*條(?:之\d+)?(?:第\s*\d+\s*[項款])*(?:第\s*\d+\s*款)?)')
CIR = re.compile(r'(?=[①-⑳])')
def lst(x):
    # 同一段有兩個以上 ①②③：每項換行（內容不改）
    if len(re.findall('[①-⑳]', x)) < 2: return x
    p = CIR.split(x); return p[0] + ''.join('<span class="evli">%s</span>' % i for i in p[1:] if i)
def fmt(t):
    # 條號灰色一般字（v664 規則）；保留 <br>
    parts = t.split('<br>')
    return '<br>'.join(lst(ART.sub(lambda m: '<span class="art">' + m.group(1) + '</span>', html.escape(p, quote=False))) for p in parts)
PT = re.compile(r'^（[一二三四五六七八九十]+）')
def point(t):
    """涵攝一點：小標粗體；「例：」「理由在於」各自換行並加小標籤"""
    t = t.strip()
    m = re.search(r'(?:。|；|」)\s*例：', t); ex = why = ''
    r = re.search(r'(?:。|；|」)\s*理由在於', t)
    cut = [x for x in (m, r) if x]
    main = t[:min(x.start() for x in cut) + 1] if cut else t
    if m: ex = t[m.end():(r.start() + 1 if r and r.start() > m.start() else len(t))]
    if r: why = t[r.end():(m.start() + 1 if m and m.start() > r.start() else len(t))]
    hm = PT.match(main); h = ''
    if hm:
        rest = main[hm.end():]; c = rest.find('：')
        if 0 < c <= 22: h = hm.group(0) + rest[:c]; main = rest[c + 1:]
        else: h = hm.group(0); main = rest
    o = '<div class="evp">' + ('<p class="evh">%s</p>' % fmt(h) if h else '') + '<p>%s</p>' % fmt(main)
    if ex: o += '<p class="evx"><span class="evt">例</span><span>%s</span></p>' % fmt(ex)
    if why: o += '<p class="evx"><span class="evt">理由</span><span>%s</span></p>' % fmt(why)
    return o + '</div>'

# ── 法條塊：一條一行並附本條名稱（11-03 使用者：「只有法條數字，你少了這條的重點核心」）
#    名稱優先取本卡邏輯拆解條文標題（lawh），再取條文庫 lawfull.json 標題；只補名稱，不新增內容
import sys as _sys
_sys.path.insert(0, os.path.join(ROOT, 'tools'))
from sprint_sx_law import titles as _lj_titles
LJD = {x['k']: x for x in json.load(io.open(os.path.join(H, '..', 'lj_data.json'), encoding='utf-8'))}
LAWF = json.load(io.open(os.path.join(H, '..', 'law', 'lawfull.json'), encoding='utf-8'))
LAWN = [('不動產經紀業管理條例施行細則', '施行細則'), ('不動產經紀業管理條例', '經紀業條例'), ('公寓大廈管理條例施行細則', '公寓大廈施行細則'),
        ('公寓大廈管理條例', '公寓大廈'), ('消費者保護法施行細則', '消保法施行細則'), ('消費者保護法', '消保法'), ('公平交易法', '公平法'),
        ('平均地權條例', '平均地權條例'), ('管理條例', '經紀業條例'), ('條例', '經紀業條例')]
ROM = 'ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ'; CIRN = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
ITEM = re.compile(r'第(\d+)條(之\d+)?(?:第(\d+)項)?(?:第(\d+)款)?')
def _short(t):
    t = (t or '').split('｜')[-1]; t = re.sub(r'（[^）]*）$', '', t).strip()
    return t
CNUM = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}
def _cn(x):
    if x.isdigit(): return int(x)
    if x == '十': return 10
    if x.startswith('十'): return 10 + CNUM[x[1]]
    if len(x) == 2 and x[1] == '十': return CNUM[x[0]] * 10
    return CNUM.get(x, 0)
def law_block(cid, text):
    steps = [st for sb in LJD.get(cid, {}).get('subs', []) for st in sb['steps']]
    M = _lj_titles(steps)
    segs = [x.strip().rstrip('、；。') for x in re.split(r'(?<=[；、。])', text.strip()) if x.strip().rstrip('、；。')]
    law = None; rows = []   # [文字, 名稱]
    for sg in segs:
        for full, key in LAWN:
            if full in sg and (sg.find(full) < sg.find('第') if '第' in sg else True):
                law = key; break
        if '廣告處理原則' in sg: law = '廣告處理原則'
        elif sg.startswith('施行細則'): law = '施行細則'
        m = ITEM.search(sg); name = None
        if m:
            n, zhi, xiang, kuan = m.groups(); art = n + (zhi or '')
            tok = '§' + art + (ROM[int(xiang) - 1] if xiang and int(xiang) <= 10 else '') + (CIRN[int(kuan) - 1] if kuan and int(kuan) <= 20 else '')
            if law in (None, '經紀業條例'): name = M.get(tok)
            if not name:
                v = LAWF.get('%s §%s' % (law or '經紀業條例', art)); name = _short(v.get('title')) if v else None
            if not name and law in (None, '經紀業條例', '公寓大廈', '公平法', '消保法'):
                b = M.get('#' + art.replace('之', '-')) or []; name = b[0] if b else None
        else:
            mp = re.search(r'第([一二三四五六七八九十\d]+)點', sg)
            if mp and law:
                v = LAWF.get('%s §%d點' % (law, _cn(mp.group(1)))); name = _short(v['title']) if v else None
            elif re.match(r'^第\d+[項款]', sg) and rows:   # 「第2項」「第5款」接回上一條
                rows[-1][0] += '、' + sg; continue
        if '（' in sg: name = None   # 原文已有說明，不重複
        rows.append([sg, name])
    lines = [fmt(t) + ('<span class="lawn">（%s）</span>' % html.escape(nm) if nm else '') for t, nm in rows]
    if len(lines) < 2: return '<p>%s</p>' % (lines[0] if lines else fmt(text))
    return '<p>' + ''.join('<span class="evli">%s</span>' % l for l in lines) + '</p>'
def body(h, p, cid=''):
    if h.startswith('二') and cid: return law_block(cid, p)
    if not h.startswith('三'): return '<p>%s</p>' % fmt(p)
    return ''.join(point(x) if PT.match(x.strip()) else '<p>%s</p>' % fmt(x) for x in p.split('<br>') if x.strip())
n = 0
for cid, blocks in EV.items():
    i = s.find('<details id="%s" ' % cid); assert i >= 0, cid
    j = s.find('<details id="es-', i + 10); j = len(s) if j < 0 else j
    a = s.find('<button type="button" class="vt" data-v="0">', i); assert i < a < j, cid
    s = s[:a] + '<button type="button" class="vt" data-v="4">考場版</button>' + s[a:]
    k = s.find('<div class="vp" data-v="1"', i)
    pan = '<div class="vp ev" data-v="4" hidden>' + ''.join(
        '<div class="blk b%d"><span class="blk-l">%s</span>%s</div>' % (x + 1, html.escape(h), body(h, p, cid))
        for x, (h, p) in enumerate(blocks)) + '</div><!--/ev-->'
    s = s[:k] + pan + s[k:]; n += 1
CSS = '.vp.ev .blk{border-left:0;border-radius:10px;padding:12px 15px}.vp.ev .blk p{margin:4px 0 0;line-height:1.85;max-width:44em}.vp.ev .art{color:var(--sub);font-weight:400}.vp.ev .evp{margin-top:12px}.vp.ev .evp .evh{font-weight:700;margin-top:0}.vp.ev .evx{display:flex;gap:8px;align-items:baseline}.vp.ev .lawn{color:var(--ink);font-weight:500;margin-left:2px}.vp.ev .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}.vp.ev .evt{flex:none;font-size:.74em;line-height:1.6;padding:0 7px;border-radius:999px;background:color-mix(in srgb,var(--ink) 9%,transparent);color:var(--sub);font-weight:600}'
import re as _r
s = _r.sub(r'\.vp\.ev \.blk\{border-left:0;[^\n]*\n</style>', '</style>', s, count=1)
s = s.replace('</style>', CSS + '\n</style>', 1)
io.open(F, 'w', encoding='utf-8').write(s)
print('考場版', n, '張')
