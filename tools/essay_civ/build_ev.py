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
def fmt(t):
    return '<br>'.join(ART.sub(lambda m: '<span class="art">' + m.group(1) + '</span>', html.escape(p, quote=False)) for p in t.split('<br>'))
n = 0
for key, blocks in EV.items():
    i = s.find('data-key="%s"' % key); assert i >= 0, key
    j = s.find('<details class="essay', i + 10); j = len(s) if j < 0 else j
    a = s.find('<button data-v="0">完整四段式</button>', i); assert i < a < j, key
    s = s[:a] + '<button data-v="4">考場版</button>' + s[a:]
    k = s.find('<div class="vp" data-v="0"', i); assert i < k < j + 40, key
    pan = '<div class="vp ev" data-v="4" hidden>' + ''.join(
        '<div class="evb e%d"><b class="evh">%s</b><p>%s</p></div>' % (x + 1, html.escape(h), fmt(p))
        for x, (h, p) in enumerate(blocks)) + '</div><!--/ev-->'
    s = s[:k] + pan + s[k:]; n += 1
CSS = ('<style id="ev-css">.ebody .vp.ev{display:grid;gap:8px;margin-top:4px}.ebody .vp.ev[hidden]{display:none}'
       '.ebody .evb{background:color-mix(in srgb,var(--c) 11%,var(--surface));border-radius:10px;padding:9px 13px}'
       '.ebody .evb .evh{display:block;color:var(--c);font-size:.86rem;margin-bottom:2px}'
       '.ebody .evb p{margin:0;font-size:.95rem;line-height:1.85}'
       '.ebody .evb.e1{--c:var(--b3)}.ebody .evb.e2{--c:var(--b1)}.ebody .evb.e3{--c:var(--b4)}.ebody .evb.e4{--c:var(--bad)}'
       '.ebody .evb .art,#pEss .ebody .evb a.lw{color:var(--sub);font-weight:400;text-decoration:underline dotted;text-underline-offset:3px;border-bottom:0;background:none}</style>')
s = re.sub(r'<style id="ev-css">.*?</style>', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
io.open(F, 'w', encoding='utf-8').write(s)
print('考場版', n, '張')
