# -*- coding: utf-8 -*-
"""11-14：完整四段式重點過少（≤3 處）的卡，手動補 mark.hl；fw16 刪重複句。可重跑。"""
import re, os
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
H = os.path.join(R, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
dup = '依第16條，經紀人員應專任一經紀業，並不得為自己或他經紀業執行仲介或代銷業務，故甲應以A公司名義承接本件；'
h = h.replace(dup + dup, dup)
M = {
 'es-fw04': ['須經雙方書面同意', '告知買受人或承租人依仲介專業應查知之不動產瑕疵', '不能因雙方代理而降低對任一方之專業服務水準'],
 'es-fw16': ['方得刊登廣告及銷售', '並註明經紀業名稱', '應專任一經紀業'],
 'es-fw18': ['土地、土地定著物或房屋及其可移轉之權利', '經紀人或經紀營業員', '於經營代銷業務者不適用'],
 'es-fw27': ['應併標明之', '標明加盟店或加盟經營字樣'],
 'es-fw30': ['前三項得以影本為之', '於代銷經紀業不適用', '先限期改正，屆期未改正始處罰鍰'],
 'es-mk8': ['使不特定多數人知悉其宣傳內容之傳播', '看廣告主是誰、不實的是哪一種內容', '內政部與公平會協調處理'],
 'es-a2': ['1 個月內補足', '停業滿 1 年廢止許可'],
 'es-a3': ['處分對象不同'],
 'es-fw19': ['使用分區或編定', '法定建蔽率、容積率', '八項特殊管制'],
 'es-d2': ['五種類型', '管線費由賣方負擔'],
 'es-fw28': ['應召開臨時會議'],
 'es-e7': ['樓板管線→3、4 樓區分所有權人共同負擔'],
 'es-e9': ['(一)(二)不是管委會職務'],
 'es-g6': ['其餘欺罔顯失公平→§25'],
}
def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()
n = 0; miss = []
for cid, segs in M.items():
    i = h.find('<details id="%s"' % cid); a = h.find('<div class="vp" data-v="0"', i); b = div_end(h, a); v = h[a:b]
    for t in segs:
        if '<mark class="hl">' + t in v: continue
        # 只在 b3/b4 內、且不在既有 mark 中
        j = v.find('<div class="blk b3"'); p = j
        while True:
            p = v.find(t, p)
            if p < 0: miss.append((cid, t)); break
            if v.rfind('<mark', 0, p) > v.rfind('</mark>', 0, p): p += 1; continue
            v = v[:p] + '<mark class="hl">%s</mark>' % t + v[p + len(t):]; n += 1; break
    h = h[:a] + v + h[b:]
open(H, 'w', encoding='utf-8').write(h)
print('補 mark', n, '未對中', miss)
