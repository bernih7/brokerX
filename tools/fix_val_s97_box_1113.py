# -*- coding: utf-8 -*-
"""11-13 特殊標的總整理 §97：v589 的「106-13 與 112-19 官方答案相反」建立在改寫過的 112-19 上，不成立；改寫紅框。可重跑。"""
import os,re
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=os.path.join(R,'估價_特殊標的總整理.html'); s=open(p,encoding='utf-8').read()
o1='<br><b>⚠️ 條文<span class="k">沒有列舉「比較標的」要選哪一種土地</span>——這點考過兩次而且官方答案相反，見下方紅框。</b>'
n1='<br><b>⚠️ 條文<span class="k">沒有列舉「比較標的」要選哪一種土地</span>，見下方紅框。</b>'
if o1 in s: s=s.replace(o1,n1)
i=s.find('<div class="box trap"><b>⚠️ §97 最大的陷阱'); j=s.find('<h2 id="s3">',i)
assert i>0 and j>i or '§97 考點' in s
if i>0:
    new='''<div class="box trap"><b>⚠️ §97 考點：公共設施用地及保留地＝<span class="k">比較法為原則</span></b><br>
<div class="qq">
<div class="qrow"><a class="qlk" href="估價_考題小卡.html#VH2_105_1">105-1</a><a class="qlk" href="估價_考題小卡.html#VH2_112_19">112-19</a>
<div class="qt">「公共設施用地及公共設施保留地之估價，以下列那一種方法估價為原則？」</div>
<div class="qa">官方答案：<span class="k">比較法</span>（§97）</div></div>
<div class="qrow"><a class="qlk" href="估價_考題小卡.html#VH2_106_13">106-13</a>
<div class="qt">題庫寫法：「依不動產估價技術規則規定，<b>得以下列何者為比較標的</b>？」（選項：一般建築用地／鄰近公保地或毗鄰非公保地／農業用地／都市計畫保護區土地）</div>
<div class="qa">題庫標示答案：都市計畫保護區土地　<span class="y">⚠️ 待對考選部原卷</span></div></div>
</div>
§97 無買賣實例時，比較的對象是「<span class="k">毗鄰土地</span>」（使用分區及使用強度差異、土地價值減損情況、毗鄰土地平均價格）；條文沒有列舉比較標的類型。
106-13 依題庫的題幹，「得以何者為比較標的」選保護區，條文推不出，<b>疑題幹有漏字（如「不得」）</b>，原卷確認前不要背這個答案。<br>
<span class="y">更正（11-13）</span>：本框舊版說「106-13 與 112-19 官方答案相反」——那是因為站上 112-19 被改寫成「比較標的應如何選取」，考選部原題其實是問「以何種方法為原則」（答比較法），兩題沒有相反。</div>

'''
    s=s[:i]+new+s[j:]
open(p,'w',encoding='utf-8').write(s); print('ok')
p=os.path.join(R,'估價_來勝模擬試題一.html'); s=open(p,encoding='utf-8').read()
s=s.replace('這是技術規則明文（§97）；比較標的怎麼選考過 106-13、112-19，兩題官方答案相反，見《特殊標的總整理》§97。','這是技術規則明文（§97）；歷屆 105-1、112-19 同考點，答案都是比較法。')
open(p,'w',encoding='utf-8').write(s)
