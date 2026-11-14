# -*- coding: utf-8 -*-
"""11-14 檢查：經紀法規完整四段式 57 張殘留「結尾卓見」（多為無出處的空泛目的句，比照土地法 v808、民法刪除）。
含條號或具體法律效果者保留內容、拿掉「結尾卓見」標籤；其餘整句刪除；空的一併刪。essays.json full 同步。可重跑。"""
import os, re, json
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
H = os.path.join(R, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
kept, dropped = [], []
def rep(m):
    inner = m.group(1); t = re.sub(r'<[^>]+>', '', inner).strip()
    if re.search(r'第\d+條|決議並訴請法院', t): kept.append(t); return '<p>' + inner + '</p>'
    dropped.append(t); return ''
h = re.sub(r'\s*<p><span class="zj">結尾卓見</span>(.*?)</p>', rep, h, flags=re.S)
open(H, 'w', encoding='utf-8').write(h)
E = os.path.join(R, 'tools/essay_jj/essays.json'); t = open(E, encoding='utf-8').read()
for d in dropped:
    if d: t = t.replace('結尾卓見' + d, '').replace('結尾卓見 ' + d, '')
open(E, 'w', encoding='utf-8').write(t)
print('刪', len(dropped), '保留', len(kept)); print('\n'.join(kept))
