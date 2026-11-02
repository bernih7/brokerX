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
def fmt(t):
    # 條號灰色一般字（v664 規則）；保留 <br>
    parts = t.split('<br>')
    return '<br>'.join(ART.sub(lambda m: '<span class="art">' + m.group(1) + '</span>', html.escape(p, quote=False)) for p in parts)
PT = re.compile(r'^（[一二三四五六七八九十]+）')
def point(t):
    """涵攝一點：小標粗體；「例：」「理由在於」各自換行並加小標籤"""
    t = t.strip()
    m = re.search(r'(?:。|；)\s*例：', t); ex = why = ''
    r = re.search(r'(?:。|；)\s*理由在於', t)
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
    if ex: o += '<p class="evx"><span class="evt">例</span>%s</p>' % fmt(ex)
    if why: o += '<p class="evx"><span class="evt">理由</span>%s</p>' % fmt(why)
    return o + '</div>'
def body(h, p):
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
        '<div class="blk b%d"><span class="blk-l">%s</span>%s</div>' % (x + 1, html.escape(h), body(h, p))
        for x, (h, p) in enumerate(blocks)) + '</div><!--/ev-->'
    s = s[:k] + pan + s[k:]; n += 1
CSS = '.vp.ev .blk{border-left:0;border-radius:10px;padding:12px 15px}.vp.ev .blk p{margin:4px 0 0;line-height:1.85;max-width:44em}.vp.ev .art{color:var(--sub);font-weight:400}.vp.ev .evp{margin-top:12px}.vp.ev .evp .evh{font-weight:700;margin-top:0}.vp.ev .evx{display:flex;gap:8px;align-items:baseline}.vp.ev .evt{flex:none;font-size:.74em;line-height:1.6;padding:0 7px;border-radius:999px;background:color-mix(in srgb,var(--ink) 9%,transparent);color:var(--sub);font-weight:600}'
import re as _r
s = _r.sub(r'\.vp\.ev \.blk\{border-left:0;[^\n]*\n</style>', '</style>', s, count=1)
s = s.replace('</style>', CSS + '\n</style>', 1)
io.open(F, 'w', encoding='utf-8').write(s)
print('考場版', n, '張')
