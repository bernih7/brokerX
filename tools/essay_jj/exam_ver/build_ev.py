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
n = 0
for cid, blocks in EV.items():
    i = s.find('<details id="%s" ' % cid); assert i >= 0, cid
    j = s.find('<details id="es-', i + 10); j = len(s) if j < 0 else j
    a = s.find('<button type="button" class="vt" data-v="0">', i); assert i < a < j, cid
    s = s[:a] + '<button type="button" class="vt" data-v="4">考場版</button>' + s[a:]
    k = s.find('<div class="vp" data-v="1"', i)
    pan = '<div class="vp ev" data-v="4" hidden>' + ''.join(
        '<div class="blk b%d"><span class="blk-l">%s</span><p>%s</p></div>' % (x + 1, html.escape(h), fmt(p))
        for x, (h, p) in enumerate(blocks)) + '</div><!--/ev-->'
    s = s[:k] + pan + s[k:]; n += 1
CSS = '.vp.ev .blk{border-left:0;border-radius:10px;padding:10px 13px}.vp.ev .blk p{margin:4px 0 0;line-height:1.85}.vp.ev .art{color:var(--sub);font-weight:400}'
if 'vp.ev .blk' not in s:
    s = s.replace('</style>', CSS + '\n</style>', 1)
io.open(F, 'w', encoding='utf-8').write(s)
print('考場版', n, '張')
