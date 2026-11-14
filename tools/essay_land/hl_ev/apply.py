# -*- coding: utf-8 -*-
"""11-14 使用者：「申論考場版內容，請補上黃底的重點提示」。
土地法申論總覽考場版（vp data-v=4）：意義、涵攝每點正文、結論加 <mark class="hl">。
重點由人工逐段挑選（picks1～4.py，索引對 segs.json）；只標正文（例／理由不標），不標條號。
可重跑：已有 mark 的段落略過。之後重產 5 分鐘衝刺／推理版（sprint/build_sprint.py、build_reason.py）。"""
import re, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
ROOT = os.path.join(H, '..', '..', '..'); F = os.path.join(ROOT, '土地法_申論題分類總覽.html')
P = {}
for n in '1234': P.update(__import__('picks' + n).P)
s = open(F, encoding='utf-8').read()
segs = json.load(open(os.path.join(H, 'segs.json')))
def mark_seg(h, phrases, miss, tag):
    if 'class="hl"' in h: return h, 0
    n = 0
    for ph in phrases:
        # 只在標籤外的文字找；不可落在已標範圍或 <span class="art"> 內
        pos = 0; done = False
        while True:
            i = h.find(ph, pos)
            if i < 0: break
            pre = h[:i]
            in_tag = pre.rfind('<') > pre.rfind('>')
            in_mark = pre.count('<mark') > pre.count('</mark>')
            in_art = pre.rfind('<span class="art">') > pre.rfind('</span>')
            if not (in_tag or in_mark or in_art) and '<' not in ph:
                h = h[:i] + '<mark class="hl">' + ph + '</mark>' + h[i + len(ph):]; n += 1; done = True; break
            pos = i + 1
        if not done: miss.append((tag, ph))
    return h, n
miss = []; total = 0; k = 0; out = []; last = 0
for m in re.finditer(r'<details class="es[^"]*" id="([^"]+)"', s):
    cid = m.group(1); st = m.end()
    j = s.find('<div class="vp" data-v="4"', st); nx = s.find('<details class="es', st)
    if j < 0 or (nx > 0 and j > nx): continue
    e = s.find('<div class="esrd"', j)
    if e < 0 or (nx > 0 and e > nx): e = s.find('<label class="done"', j)
    vp = s[j:e]
    def rep_fdb(cls, vp):
        global k, total
        mm = re.search(r'(<details class="blk %s".*?<div class="fdb">)(.*?)(</div></details>)' % cls, vp, re.S)
        if not mm: return vp
        assert segs[k][0] == cid, (k, segs[k][0], cid)
        new, n = mark_seg(mm.group(2), P.get(k, []), miss, f'{k}|{cid}'); total += n; k += 1
        return vp[:mm.start(2)] + new + vp[mm.end(2):]
    vp = rep_fdb('b1', vp)
    b3 = re.search(r'(<details class="blk b3".*?<div class="fdb">)(.*)(</div></details><details class="blk b4")', vp, re.S)
    if b3:
        body = b3.group(2)
        def rp(mm):
            global k, total
            assert segs[k][0] == cid and segs[k][1] == 'ham', (k, segs[k], cid)
            new, n = mark_seg(mm.group(2), P.get(k, []), miss, f'{k}|{cid}'); total += n; k += 1
            return mm.group(1) + new + mm.group(3)
        body = re.sub(r'(<div class="evp">(?:<p class="evh">.*?</p>)?<p>)(.*?)(</p>)', rp, body, flags=re.S)
        vp = vp[:b3.start(2)] + body + vp[b3.end(2):]
    vp = rep_fdb('b4', vp)
    out.append(s[last:j]); out.append(vp); last = e
out.append(s[last:]); s2 = ''.join(out)
assert k in (0, len(segs)) or k == len(segs), k
open(F, 'w', encoding='utf-8').write(s2)
print('segments', k, 'marks', total, 'miss', len(miss))
for x in miss: print('  MISS', x)
