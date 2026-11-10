# -*- coding: utf-8 -*-
"""11-10 使用者：「（四）租金利益是什麼，為什麼 101 年的考題需要寫到這個」。
101-二 原題只問經濟／實質／支付租金的意義與金額，**沒問租金利益**——是本站延伸。處理：
①考場版、考場速寫拿掉租金利益（省時間）；②完整四段式、邏輯拆解保留但標「延伸（題目未問，可不寫）」，結尾卓見改回扣題目；
③推理版資料 lj_data 原寫「120,000－108,360＝11,640」（口徑不一，與頁面自己說的陷阱相反）及「支付＜實質＜經濟」當通則（114-24 官方答案：經濟與支付大小「不一定」）→ 改正。可重跑。"""
import json, os, glob
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
# ① 考場版
for f in [os.path.join(H, 'exam', 'exam_ver.json')] + glob.glob(os.path.join(H, 'exam', 'out_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if 'e101-2' not in d: continue
    ch = False
    for blk in d['e101-2']:
        o = '<br>（四）租金利益：<mark>支付口徑120,000－108,000</mark>＝<b>12,000元</b>；實質口徑120,400－108,360＝<b>12,040元</b>。'
        if o in blk[1]: blk[1] = blk[1].replace(o, ''); ch = True
        o2 = '本解假設「低於市場行情一成」指每期支付租金，承租人每年少付12,000元；若市場同樣收取兩個月押金，市場實質租金為120,400元，與本約實質租金108,360元相差12,040元。租金利益要同口徑相減，並寫明假設。'
        if o2 in blk[1]: blk[1] = blk[1].replace(o2, '本解假設「低於市場行情一成」指每期支付租金，經濟租金以支付租金÷0.9 還原。'); ch = True
    if ch: json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=f.endswith('exam_ver.json')); print('考場版', os.path.basename(f))
# ② 申論頁（完整四段式、邏輯拆解、速寫）
P = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html'); s = open(P, encoding='utf-8').read()
a = s.find('id="e101-2"'); b = s.find('class="essay-card', a + 50); c = s[a:b]; c0 = c
R = [
 ('<div class="ljar">↓ 承租人得到多少租金利益？</div>', '<div class="ljar">↓ 延伸（題目未問，可不寫）</div>'),
 ('<span class="ljno">9</span>租金利益怎麼算？</div>', '<span class="ljno">9</span>延伸（題目未問）：租金利益怎麼算？</div>'),
 ('<div class="ljh">口徑一致</div>租金利益＝', '<div class="ljh">延伸・口徑一致</div>租金利益＝'),
 ('<span class="ljno">9</span>租金利益 12,000（實質口徑 12,040），口徑要一致</li>', '<span class="ljno">9</span>延伸（題目未問）：租金利益 12,000，口徑要一致</li>'),
 ('年經濟租金 108,000÷0.9＝120,000 元；寫明假設，租金利益 12,000 元（實質口徑 12,040 元）', '年經濟租金 108,000÷0.9＝120,000 元；寫明假設（「低於一成」指支付租金）'),
 ('；經濟＝108,000÷0.9＝<span class="qa-kw">120,000</span>；租金利益 12,000（實質口徑 120,400－108,360＝12,040）', '；經濟＝108,000÷0.9＝<span class="qa-kw">120,000</span>'),
 ('不是×0.9；租金利益要同口徑相減；押金是兩個月', '不是×0.9；押金是兩個月'),
 ('<div class="cl">④ 租金利益（支付口徑）＝', '<div class="cl">④ 延伸（題目未問，可不寫）租金利益（支付口徑）＝'),
 ('<span class="zj">結尾卓見</span>租金利益要<span class="zjk">同口徑</span>相減，並寫明假設。', '<span class="zj">結尾卓見</span>三種租金先寫定義、再寫<span class="zjk">假設</span>，經濟租金以支付租金÷0.9 還原，數字才站得住。'),
]
for o, n in R:
    if n in c: continue
    assert c.count(o) >= 1, o[:40]; c = c.replace(o, n)
if c != c0: s = s[:a] + c + s[b:]; open(P, 'w', encoding='utf-8').write(s); print('申論頁')
# ③ lj_data（推理版用）
LJ = os.path.join(H, 'lj_data.json'); d = json.load(open(LJ, encoding='utf-8'))
for x in d:
    if x['k'] != 'e101-2': continue
    for sb in x['subs']:
        for st in sb['steps']:
            if st.get('facth') == '租金利益':
                st.update({'law': '本題：支付租金＜實質租金＜經濟租金（因本約租金低於市場行情；一般而言經濟租金與支付租金大小不一定，114-24）。',
                           'facth': '延伸（題目未問）',
                           'fact': '承租人每年少付 120,000－108,000＝12,000 元（同為支付口徑相減；不可用 120,000－108,360）。',
                           'res': '108,000＜108,360＜120,000。',
                           'key': '本題 支付＜實質＜經濟；大小關係一般不一定'})
                print('lj_data')
json.dump(d, open(LJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
