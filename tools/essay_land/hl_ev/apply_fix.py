# apply.py 第一輪中因含條號而沒標到的 6 段，改標不含條號的片語（可重跑：已標者略過）
import re, json, os
H = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(H, '..', '..', '..', '土地法_申論題分類總覽.html')
s = open(F, encoding='utf-8').read()
FIX = [('q-100-一', '本題店面出租予便利商店供營業使用，', '非自用住宅用地'),
       ('mk-1', '依平均地權條例罰則章，', '並無處罰'),
       ('pr-23', '仍須依', '得全體同意'),
       ('pr-09', None, '為債權效力'),
       ('pr-44', '；', '10年以內之租賃'),
       ('pr-10', '由直轄市或縣（市）政府', '製定使用分區圖')]
for cid, ctx, ph in FIX:
    st = s.find(f'id="{cid}"'); j = s.find('<div class="vp" data-v="4"', st); e = s.find('<div class="esrd"', j)
    seg = s[j:e]
    if f'<mark class="hl">{ph}' in seg: continue
    i = seg.find(ph)
    while i >= 0:
        pre = seg[:i]
        if pre.count('<mark') == pre.count('</mark>') and pre.rfind('<') < pre.rfind('>'): break
        i = seg.find(ph, i + 1)
    assert i >= 0, (cid, ph)
    seg = seg[:i] + '<mark class="hl">' + ph + '</mark>' + seg[i + len(ph):]
    s = s[:j] + seg + s[e:]; print('ok', cid, ph)
open(F, 'w', encoding='utf-8').write(s)
