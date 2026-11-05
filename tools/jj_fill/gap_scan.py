# -*- coding: utf-8 -*-
"""缺口盤點：互動單字卡、數字速查、程序總整理、罰則總整理 逐項以關鍵字比對定義填空（不含 S 章）。輸出 ✘ 清單供人工確認。"""
import re, html, json, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def strip(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()
f = rd('經紀法規_定義填空練習.html'); i = f.find('const DATA = ') + 13; D, _ = json.JSONDecoder().raw_decode(f[i:])
FT = ''.join(strip(x['term'] + x['answer'] + x.get('p', '') + x.get('m', '') + x.get('t', '') + x['src']) for c in D if c['id'][0] != 'S' for x in c['cards'])
FT = FT.replace(' ', '')
items = []
fc = rd('經紀法規概要_互動單字卡.html')
for m in re.finditer(r'"id": "([A-H]\d+)", "front": "(.*?)", "back": "(.*?)"', fc):
    items.append(('單字卡 ' + m.group(1), m.group(2), m.group(3)))
sq = rd('經紀法規_數字速查.html')
for nm in re.finditer(r'<div class="num[^"]*"><div class="nh"><span class="nv">(.*?)</span>(.*?)(?=<div class="num|<div class="sec|$)', sq, re.S):
    for it in re.finditer(r'<div class="ar2">(.*?)</div><div><span class="who2">(.*?)</span><span class="d2">(.*?)</span>', nm.group(2)):
        items.append(('速查 ' + strip(nm.group(1)), strip(it.group(1)) + '｜' + strip(it.group(3)), strip(nm.group(1))))
pn = rd('經紀法規_罰則總整理.html')
for m in re.finditer(r'<div class="tt">(.*?)</div><span class="amt">(.*?)</span></summary><div class="dt"><div class="pn">(.*?)</div>', pn, re.S):
    items.append(('罰則 ' + strip(m.group(1)), strip(m.group(3)), strip(m.group(2))))
pr = rd('經紀法規_程序總整理.html')
for m in re.finditer(r'<tr><td><b>(.*?)</b>(.*?)</tr>', pr, re.S):
    items.append(('程序 ' + strip(m.group(1)), strip(m.group(2))[:160], ''))
def kws(text):
    t = strip(text)
    ks = re.findall(r'「([^」]{2,12})」', t)
    ks += re.findall(r'(\d+(?:\.\d+)?\s*(?:萬|億|個月|日|年|小時|名|%|％|倍|分之))', t)
    return [k.replace(' ', '') for k in ks]
out = []
for src, front, back in items:
    ks = kws(front + ' ' + back)
    ks = [k for k in ks if len(k) >= 2]
    hit = [k for k in ks if k in FT]
    if not ks or len(hit) / len(ks) < .5:
        out.append('✘ [%s] %s ⇒ %s ｜kw:%s hit:%s' % (src, front[:90], back[:120].replace('\n', ' / '), ks[:6], hit[:4]))
print(len(items), '項；✘', len(out))
open('/tmp/claude-0/-home-claude/db4af835-7730-5160-a7cd-81cabbdf283a/scratchpad/gap.txt', 'w').write('\n'.join(out))
