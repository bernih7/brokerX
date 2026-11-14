# -*- coding: utf-8 -*-
"""11-14 使用者：公平法§15Ⅰ但書八款口訣「補進申論，好背誦」。fw12、g1 兩張：邏輯拆解口訣（lj_data mnem）、考場速寫口訣、
完整四段式（法條塊後加口訣塊，逐款對照）；定義填空 S 卡口訣同步。可重跑（已含口訣者略過）。之後跑 mk_card_viewer、build_sprint、build_reason、es_fill。"""
import os, re, json
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
K = '八款：規、研、專，出、入、景，中小、其他'
H = os.path.join(R, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
BOX = ('<div class="blk b5"><span class="blk-l">口訣（§15Ⅰ但書八款）</span>'
       '<p><b>規、研、專，出、入、景，中小、其他</b></p>'
       '<p>①統一<b>規</b>格或型式<br>②共同<b>研</b>究開發<br>③分別作<b>專</b>業發展<br>'
       '④確保或促進輸<b>出</b>（專就國外市場之競爭予以約定）<br>⑤國外商品或服務之輸<b>入</b>（採取共同行為）<br>'
       '⑥經濟不<b>景</b>氣（限制產銷數量、設備或價格）　⑦<b>中小</b>企業<br>⑧<b>其他</b>促進產業發展、技術創新或經營效率所必要</p>'
       '<p>前三款＝提升效率；中間三款＝對外貿易＋景氣；後兩款＝中小企業＋概括。八款之外還要「有益於整體經濟與公共利益」＋「經申請主管機關許可」（§15Ⅰ）。</p></div>')
REP = {'es-fw12': ['聯合行為：原則禁、許可例外；公會決議也算', '聯合行為：原則禁、許可例外 <small'],
       'es-g1': ['三個月決定、五年許可；屆滿前三到六個月書面續命', '三個月決定、五年許可 <small']}
def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()
for cid, olds in REP.items():
    i = h.find('<details id="%s"' % cid); j = h.find('<details id="es-', i + 10); s = h[i:j]
    if K in s: continue
    for o in olds:
        assert o in s, (cid, o)
        n = o.replace(' <small', '') + '；' + K + (' <small' if o.endswith('<small') else '')
        s = s.replace(o, n)
    a = s.find('<div class="vp" data-v="0"'); b3 = s.find('<div class="blk b3"', a); assert a > 0 and b3 > 0 and b3 < div_end(s, a)
    s = s[:b3] + BOX + s[b3:]
    h = h[:i] + s + h[j:]
open(H, 'w', encoding='utf-8').write(h)
L = os.path.join(R, 'tools/essay_jj/lj_data.json'); t = open(L, encoding='utf-8').read()
for o in ['聯合行為：原則禁、許可例外；公會決議也算', '三個月決定、五年許可；屆滿前三到六個月書面續命']:
    if o + '；' + K not in t: t = t.replace('"' + o + '"', '"' + o + '；' + K + '"')
open(L, 'w', encoding='utf-8').write(t)
F = os.path.join(R, 'tools/jj_fill/es_fill.py'); f = open(F, encoding='utf-8').read()
o = '聯合行為：原則禁、許可例外；三個月決定、五年許可〔自編〕'
if o in f: f = f.replace(o, '聯合行為：原則禁、許可例外；三個月決定、五年許可；八款「規、研、專，出、入、景，中小、其他」〔自編〕')
open(F, 'w', encoding='utf-8').write(f)
print('ok')
