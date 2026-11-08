# -*- coding: utf-8 -*-
"""民法申論「考場版」：讀 exam_ver/ev_*.json，插入指揮中心申論卡（分頁：邏輯拆解｜考場速寫｜考場版｜完整四段式）。
規格依 KB《備考_跨科同步施工單_申論考場版_20261102》：四塊色塊（意義綠／法條藍／涵攝金／結論紅）不加框線、
頁首不放字數說明、條號灰色一般字。可重跑（先移除舊的考場版再插入）。"""
import io, json, os, re, glob, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
F = os.path.join(ROOT, '民法_備考指揮中心.html')
EV = {}
for f in sorted(glob.glob(os.path.join(H, 'exam_ver', 'ev_*.json'))): EV.update(json.load(io.open(f, encoding='utf-8')))
s = io.open(F, encoding='utf-8').read()
s = s.replace('<button data-v="4">考場版</button>', '')
s = re.sub(r'<div class="vp ev" data-v="4" hidden>.*?</div><!--/ev-->', '', s, flags=re.S)
ART = re.compile(r'((?:民法)?第\s*\d+\s*條(?:之\s*\d+)?(?:第\s*\d+\s*項)?(?:第\s*\d+\s*款)?(?:前段|後段|但書|本文)?)')
CIR = re.compile(r'(?=[①-⑳])')
def lst(x):
    # 同一段兩個以上 ①②③：每項一行（只在句讀後、且不切款號）
    c = [m.start() for m in re.finditer('[①-⑳]', x) if m.start() == 0 or x[m.start() - 1] in '　 ，；：、。（→']
    if len(c) < 2: return x
    p = [x[:c[0]]] + [x[a:b] for a, b in zip(c, c[1:] + [len(x)])]
    return p[0] + ''.join('<span class="evli">%s</span>' % i for i in p[1:] if i)
def fmt(t):
    return '<br>'.join(lst(ART.sub(lambda m: '<span class="art">' + m.group(1) + '</span>', html.escape(p, quote=False))) for p in t.split('<br>')).replace('&lt;mark&gt;', '<mark>').replace('&lt;/mark&gt;', '</mark>')
PT = re.compile(r'^（[一二三四五六七八九十]+）')
def point(t):
    """涵攝一點：小標粗體一行；「例：」「理由在於」各自一行並加灰色小標籤（內容不改）"""
    t = t.strip()
    m = re.search(r'(?:。|；|」)\s*例：', t); r = re.search(r'(?:。|；|」)\s*理由在於', t); ex = why = ''
    cut = [x for x in (m, r) if x]
    main = t[:min(x.start() for x in cut) + 1] if cut else t
    if m: ex = t[m.end():(r.start() + 1 if r and r.start() > m.start() else len(t))]
    if r: why = t[r.end():(m.start() + 1 if m and m.start() > r.start() else len(t))]
    hm = PT.match(main); h = ''
    if hm:
        rest = main[hm.end():]; c = rest.find('：')
        if 0 < c <= 44 and '「' not in rest[:c]: h = hm.group(0) + rest[:c]; main = rest[c + 1:]
        else: h = ''; main = '<b>' + hm.group(0) + '</b>' + rest
    o = '<div class="evp">' + ('<p class="evph">%s</p>' % fmt(h) if h else '') + '<p>%s</p>' % (fmt(main).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>'))
    if ex: o += '<p class="evx"><span class="evt">例</span><span>%s</span></p>' % fmt(ex)
    if why: o += '<p class="evx"><span class="evt">理由</span><span>%s</span></p>' % fmt(why)
    return o + '</div>'
def body(h, p):
    if not h.startswith('三'): return '<p>%s</p>' % fmt(p)
    return ''.join(point(x) if PT.match(x.strip()) else '<p>%s</p>' % fmt(x) for x in p.split('<br>') if x.strip())
n = 0
for key, blocks in EV.items():
    i = s.find('data-key="%s"' % key); assert i >= 0, key
    j = s.find('<details class="essay', i + 10); j = len(s) if j < 0 else j
    a = s.find('<button data-v="0">完整四段式</button>', i); assert i < a < j, key
    s = s[:a] + '<button data-v="4">考場版</button>' + s[a:]
    k = s.find('<div class="vp" data-v="0"', i); assert i < k < j + 40, key
    pan = '<div class="vp ev" data-v="4" hidden>' + ''.join(
        '<div class="evb e%d"><b class="evh">%s</b>%s</div>' % (x + 1, html.escape(h), body(h, p))
        for x, (h, p) in enumerate(blocks)) + '</div><!--/ev-->'
    s = s[:k] + pan + s[k:]; n += 1
CSS = ('<style id="ev-css">.ebody .vp.ev{display:grid;gap:8px;margin-top:4px}.ebody .vp.ev[hidden]{display:none}'
       '.ebody .evb{background:color-mix(in srgb,var(--c) 11%,var(--surface));border-radius:10px;padding:9px 13px}'
       '.ebody .evb .evh{display:block;color:var(--c);font-size:.86rem;margin-bottom:2px}'
       '.ebody .evb p{margin:0;font-size:.95rem;line-height:1.85}'
       '.ebody .evb .evp{margin-top:10px}.ebody .evb .evp:first-of-type{margin-top:2px}.ebody .evb .evph{font-weight:700}'
       '.ebody .evb .evx{display:flex;gap:8px;align-items:baseline;margin-top:2px}.ebody .evb .evli,.ebody .vp .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}'
       '.ebody .evb .evt{flex:none;font-size:.74em;line-height:1.6;padding:0 7px;border-radius:999px;background:color-mix(in srgb,var(--ink) 9%,transparent);color:var(--sub);font-weight:600}'
       '.ebody .evb.e1{--c:var(--b3)}.ebody .evb.e2{--c:var(--b1)}.ebody .evb.e3{--c:var(--b4)}.ebody .evb.e4{--c:var(--bad)}'
       '.ebody .evb .art,#pEss .ebody .evb a.lw{color:var(--sub);font-weight:400;text-decoration:underline dotted;text-underline-offset:3px;border-bottom:0;background:none}'
       '.ebody .evb mark{background:linear-gradient(transparent 50%,rgba(242,201,76,.55) 50%);color:inherit;font-weight:700;padding:0 1px;border-radius:2px}</style>')
s = re.sub(r'<style id="ev-css">.*?</style>', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
io.open(F, 'w', encoding='utf-8').write(s)
print('考場版', n, '張')
