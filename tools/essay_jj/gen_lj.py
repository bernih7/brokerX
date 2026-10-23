# 經紀法規指揮中心申論卡：版本鈕改為「邏輯拆解 → 考場速寫 → 完整四段式」
# - 邏輯拆解（data-v=3）由 lj_data.json 產生，內含三種排法：① 推理鏈 ② 條文｜本題 ③ 地圖＋勾選
# - 考場速寫（data-v=1）併入原「得分關鍵・失分點」（data-v=2）
# 可重複執行（已轉換過的卡片會以 lj_data.json 重新產生邏輯拆解）
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lj_render import render, CSS, JS
ROOT = os.path.join(HERE, '..', '..')
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
DATA = os.path.join(HERE, 'lj_data.json')
D = {x['k']: x for x in json.load(open(DATA, encoding='utf-8'))}
s = open(HUB, encoding='utf-8').read()

VT = ('<div class="vtabs">'
      '<button type="button" class="vt on" data-v="3">邏輯拆解</button>'
      '<button type="button" class="vt" data-v="1">考場速寫</button>'
      '<button type="button" class="vt" data-v="0">完整四段式</button></div>')

out = []; pos = 0; done = 0; missing = []
for m in re.finditer(r'<details id="(es-[^"]+)" class="essay-detail[^"]*">', s):
    k = m.group(1); i = m.start()
    e = s.index('</details>', s.index('<div class="essay-body">', i))
    blk = s[i:e]
    if k not in D:
        missing.append(k); continue

    def seg(b, v):
        a = b.find(f'<div class="vp" data-v="{v}"')
        if a < 0: return None, None
        nxt = b.find('<div class="vp" data-v="', a + 5)
        return a, (nxt if nxt > 0 else len(b))

    # 1) 先把舊的邏輯拆解（若有）拿掉，確保可重跑
    a3, b3 = seg(blk, 3)
    if a3 is not None:
        blk = blk[:a3] + blk[b3:]
    # 2) 得分關鍵（v=2）併入速寫（v=1）
    a2, b2 = seg(blk, 2)
    if a2 is not None:
        inner = re.sub(r'^<div class="vp" data-v="2"[^>]*>', '', blk[a2:b2])
        inner = inner[:inner.rindex('</div>')]
        blk = blk[:a2] + blk[b2:]
        a1, b1 = seg(blk, 1)
        body1 = blk[a1:b1]; body1 = body1[:body1.rindex('</div>')]
        blk = blk[:a1] + body1 + '<div class="sk2">' + inner + '</div></div>' + blk[b1:]
    # 3) 換按鈕
    blk = re.sub(r'<div class="vtabs">.*?</div>', VT, blk, count=1, flags=re.S)
    # 4) 其餘分頁隱藏
    blk = re.sub(r'<div class="vp" data-v="0"(?: hidden)?>', '<div class="vp" data-v="0" hidden>', blk, count=1)
    blk = re.sub(r'<div class="vp" data-v="1"(?: hidden)?>', '<div class="vp" data-v="1" hidden>', blk, count=1)
    # 5) 插入邏輯拆解（緊接 vtabs 之後）
    p = blk.index(VT) + len(VT)
    blk = blk[:p] + '<div class="vp" data-v="3">' + render(D[k]) + '</div>' + blk[p:]

    out.append(s[pos:i]); out.append(blk); pos = e; done += 1
out.append(s[pos:]); s = ''.join(out)
if missing:
    sys.exit('缺邏輯拆解資料：' + '、'.join(missing))

s = re.sub(r'<style id="lj-css">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="lj-js">.*?</script>', '', s, flags=re.S)
s = s.replace('</head>', '<style id="lj-css">' + CSS + '</style></head>', 1)
s = s.replace('</body>', '<script id="lj-js">' + JS + '</script></body>', 1)
open(HUB, 'w', encoding='utf-8').write(s)
print('已改寫', done, '題')
