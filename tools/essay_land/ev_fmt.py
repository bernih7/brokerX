# -*- coding: utf-8 -*-
"""土地法考場版「三、涵攝」版面（11-05 使用者：「五分鐘好歹要有粗體或大標題」）：
每點（一）小標粗體獨立一行；「例：」「理由在於」各自一行加灰膠囊；同段兩項以上「一、二、」每項一行；條號灰字。內容一字不改。"""
import re
PT = re.compile(r'^（[一二三四五六七八九十]+）')
ART = re.compile(r'((?:土地法|土地稅法|平均地權條例|土地徵收條例|都市計畫法|區域計畫法|國土計畫法|房屋稅條例|契稅條例|所得稅法|農業發展條例|同法|同條例|本條例)?第\d+條(?:之\d+)?(?:第\d+項)?(?:第\d+款)?|§\s*\d+(?:-\d+)?[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]*[①-⑳]*)')
LI = re.compile(r'(?<=[：；])(?=[一二三四五六七八九十]{1,2}、)')
def art(t): return ART.sub(lambda m: '<span class="art">' + m.group(1) + '</span>', t)
def lst(t):
    if len(LI.findall(t)) < 2: return t
    p = LI.split(t); return p[0] + ''.join('<span class="evli">%s</span>' % i for i in p[1:] if i)
def f(t): return lst(art(t))
def point(t):
    t = t.strip()
    if '<' in t: return '<p>%s</p>' % t          # 已含標記者不動
    m = re.search(r'(?:。|；|」)\s*例：', t); r = re.search(r'(?:。|；|」)\s*理由在於', t)
    cut = [x for x in (m, r) if x]
    main = t[:min(x.start() for x in cut) + 1] if cut else t
    ex = t[m.end():(r.start() + 1 if r and r.start() > m.start() else len(t))] if m else ''
    why = t[r.end():(m.start() + 1 if m and m.start() > r.start() else len(t))] if r else ''
    h = ''; hm = PT.match(main)
    if hm:
        rest = main[hm.end():]
        c = min([i for i in (rest.find('。'), rest.find('：')) if i > 0] or [99])
        if c <= 24: h = hm.group(0) + rest[:c]; main = rest[c + 1:]
    o = '<div class="evp">' + ('<p class="evh">%s</p>' % h if h else '') + ('<p>%s</p>' % f(main) if main.strip() else '')
    xs = []
    if ex: xs.append((m.start(), '<p class="evx"><span class="evt">例</span><span>%s</span></p>' % f(ex)))
    if why: xs.append((r.start(), '<p class="evx"><span class="evt">理由</span><span>%s</span></p>' % f(why)))
    o += ''.join(x for _, x in sorted(xs))
    return o + '</div>'
def block(h, p):
    if not h.startswith('三') or 'class="evp"' in p: return p
    ps = [x for x in re.split(r'<br\s*/?>', p) if x.strip()]
    if not any(PT.match(x.strip()) for x in ps): return p
    return ''.join(point(x) for x in ps)
