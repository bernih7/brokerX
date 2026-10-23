# 經紀法規指揮中心申論卡：版本鈕改為「邏輯拆解 → 考場速寫 → 完整四段式」
# - 邏輯拆解（data-v=3）由 lj_data.json 產生，內含三種排法：① 推理鏈 ② 條文｜本題 ③ 地圖＋勾選
# - 考場速寫（data-v=1）併入原「得分關鍵・失分點」（data-v=2），包成 <div class="sk2">
# 可重複執行（已轉換過的卡片會以 lj_data.json 重新產生邏輯拆解）
#
# ⚠️ 題目區塊的邊界是「下一個 <details id="es-」，不是第一個 </details>——
#    範文的法條段裡嵌著 <details class="bt"> 條文卡，用 </details> 會把區塊從中間切斷，
#    導致 data-v=1／2 落在區塊外，速寫沒被隱藏、得分關鍵沒被併入（2026-10-23 踩過）。
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

TAG = re.compile(r'<(/?)div\b[^>]*?(/?)>', re.I)

def div_span(b, start):
    """start 指向某個 <div ...> 的 '<'，回傳 (內容起點, 該 div 的 </div> 結束位置)。"""
    depth = 0
    for m in TAG.finditer(b, start):
        if m.group(2) == '/':      # <div ... /> 自閉合
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return b.index('>', start) + 1, m.end()
    raise ValueError('div 不成對 @%d' % start)

def vp(b, v):
    m = re.search(r'<div class="vp" data-v="%s"[^>]*>' % v, b)
    if not m:
        return None
    inner, end = div_span(b, m.start())
    return m.start(), inner, end      # 整段起點、內容起點、整段結束

# 題目區塊：本題 <details id="es-"> 起，到下一個 <details id="es-"> 止
ms = list(re.finditer(r'<details id="(es-[^"]+)" class="essay-detail[^"]*">', s))
out = []; pos = 0; done = 0; missing = []
for idx, m in enumerate(ms):
    k = m.group(1); i = m.start()
    e = ms[idx + 1].start() if idx + 1 < len(ms) else len(s)
    blk = s[i:e]
    if k not in D:
        missing.append(k); continue

    # 1) 先把舊的邏輯拆解（若有）拿掉，確保可重跑
    r = vp(blk, 3)
    if r: blk = blk[:r[0]] + blk[r[2]:]
    # 2) 得分關鍵（v=2）併入速寫（v=1），包成 .sk2
    r2 = vp(blk, 2)
    if r2:
        a2, in2, e2 = r2
        inner = blk[in2:e2 - len('</div>')]
        blk = blk[:a2] + blk[e2:]
        r1 = vp(blk, 1)
        if r1 is None: sys.exit('✗ %s 有 data-v=2 卻沒有 data-v=1' % k)
        a1, in1, e1 = r1
        body1 = blk[in1:e1 - len('</div>')]
        blk = blk[:a1] + '<div class="vp" data-v="1" hidden>' + body1 \
              + '<div class="sk2">' + inner + '</div></div>' + blk[e1:]
    # 3) 換按鈕
    nb, cnt = re.subn(r'<div class="vtabs">.*?</div>', VT, blk, count=1, flags=re.S)
    if not cnt: sys.exit('✗ %s 找不到 vtabs' % k)
    blk = nb
    # 4) 其餘分頁隱藏
    blk = re.sub(r'<div class="vp" data-v="0"(?: hidden)?>', '<div class="vp" data-v="0" hidden>', blk, count=1)
    blk = re.sub(r'<div class="vp" data-v="1"(?: hidden)?>', '<div class="vp" data-v="1" hidden>', blk, count=1)
    # 5) 插入邏輯拆解（緊接 vtabs 之後）
    p = blk.index(VT) + len(VT)
    blk = blk[:p] + '<div class="vp" data-v="3">' + render(D[k]) + '</div>' + blk[p:]

    out.append(s[pos:i]); out.append(blk); pos = e; done += 1
out.append(s[pos:]); s = ''.join(out)
if missing: sys.exit('缺邏輯拆解資料：' + '、'.join(missing))

s = re.sub(r'<style id="lj-css">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="lj-js">.*?</script>', '', s, flags=re.S)
s = s.replace('</head>', '<style id="lj-css">' + CSS + '</style></head>', 1)
s = s.replace('</body>', '<script id="lj-js">' + JS + '</script></body>', 1)
open(HUB, 'w', encoding='utf-8').write(s)
print('已改寫', done, '題')
