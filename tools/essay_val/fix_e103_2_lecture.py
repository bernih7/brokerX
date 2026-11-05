# -*- coding: utf-8 -*-
"""11-05 使用者貼 103-二 講義擬答：已設定地上權土地＝依買受人分限定／正常價格（同本站，對講義 A 結案）。
①完整版：拿掉「各家擬答略有差異」提示，改註已對講義；價格種類表後補 §6 租金種類（講義列入正常租金、限定租金）。可重跑。"""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '不動產估價概要_申論題實戰範文.html')
s = open(P, encoding='utf-8').read()
a = s.find('id="e103-2"')
old1 = '<div class="note">📌 此小題各家擬答略有差異；作答時先寫四種價格定義，再依「買受人是否為地上權人」下判斷並寫出理由，即可得分。</div>'
new1 = '<div class="note">📌 已對補習班講義（11-05）：講義擬答同樣依買受人區分——地上權人承購（土地法§104 優先購買權）＝限定價格；公開標售、不限資格＝正常價格。作答先寫價格種類定義，再依「買受人是否為地上權人」下判斷並寫理由。</div>'
old2 = '<tr><td>特殊價格</td><td>對<strong>不具市場性</strong>之不動產所估計之價值</td></tr>\n    </table>\n    <div class="section-h">二、已設定地上權'
new2 = ('<tr><td>特殊價格</td><td>對<strong>不具市場性</strong>之不動產所估計之價值</td></tr>\n    </table>\n'
        '    <p>另 §6 估計租金種類：<strong>正常租金</strong>（§2 第五款，正常租賃條件形成之合理租賃價值）、<strong>限定租金</strong>（§2 第六款，基於續訂租約或不動產合併為目的形成之租賃價值）；講義擬答一併列出，作答可附帶一句。</p>\n'
        '    <div class="section-h">二、已設定地上權')
for o, n in ((old1, new1), (old2, new2)):
    if n in s: continue
    i = s.find(o, a); assert i > 0, o[:40]
    s = s[:i] + n + s[i + len(o):]
open(P, 'w', encoding='utf-8').write(s); print('ok')
