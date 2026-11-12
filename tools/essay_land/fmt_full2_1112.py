# -*- coding: utf-8 -*-
"""申論總覽「涵攝分析・看全文」排版：刪重複小標、首句粗體成一行、句首依／同條／舉例而言／本題…換行、
三項以上列舉逐項換行、黃底粗體重點（tools/essay_land/hl_full2_1112.json，由審稿助手挑、逐字比對）。可重跑（已排過的段落略過）。"""
import re, json, os, html
R = os.path.join(os.path.dirname(__file__), '..', '..')
F = os.path.join(R, '土地法_申論題分類總覽.html')
HL = json.load(open(os.path.join(R, 'tools/essay_land/hl_full2_1112.json'), encoding='utf-8'))
s = open(F, encoding='utf-8').read()
CSS = '.full2 p{line-height:1.85}.full2 b.ld{display:block;margin-bottom:6px;padding-bottom:6px;border-bottom:1px dashed var(--line);color:var(--ink);font-size:15.5px}'
if CSS not in s: s = s.replace('.full2 p{margin:4px 0}', '.full2 p{margin:4px 0}' + CSS, 1)
BRK = r'(?=(?:依|另依|又依|同條|同法|同項|同辦法|同款|第[0-9]+項|舉例而言|本題|至於|惟|但|故|例如|再依|復依))'
PAT = re.compile(r'<details class="sub2"><summary><b>(.*?)</b>(.*?)<div class="full2">(.*?)</div></details>', re.S)
out = []; last = 0; n = 0; ch = 0
for m in PAT.finditer(s):
    i = n; n += 1
    head, mid, body = m.group(1), m.group(2), m.group(3)
    out.append(s[last:m.start(3)]); last = m.end(3)
    pm = re.match(r'<p>(.*)</p>$', body, re.S)
    if 'class="ld"' in body or not pm or '<table' in body:
        out.append(body); continue
    h = re.sub(r'^（[一二三四五六七八九十]+）', '', html.unescape(re.sub(r'<[^>]+>', '', head)))
    t = pm.group(1)
    if t.startswith(h + '：'): t = t[len(h) + 1:]
    for ph in HL.get(str(i), []):
        e = ph.replace('&', '&amp;').replace('<', '&lt;')
        k = t.find(e)
        if k >= 0 and t[:k].count('<') == t[:k].count('>'):
            t = t[:k] + '<mark class="hl">' + e + '</mark>' + t[k + len(e):]
    k = t.find('。')
    if 0 < k < 160 and t[:k].count('<mark') == t[:k].count('</mark>'):
        t = '<b class="ld">' + t[:k + 1] + '</b>' + t[k + 1:]
    t = re.sub(r'。' + BRK, '。<br>', t)
    if re.search(r'；[三四五六]、', t):
        t = re.sub(r'([：；])([一二三四五六七八九十]{1,2}、)', r'\1<br>\2', t)
    t = re.sub(r'(<br>)+', '<br>', t)
    out.append('<p>' + t + '</p>'); ch += 1
out.append(s[last:])
s = ''.join(out)
print('段落', n, '｜排版', ch)
open(F, 'w', encoding='utf-8').write(s)
