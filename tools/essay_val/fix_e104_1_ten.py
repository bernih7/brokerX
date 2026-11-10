# -*- coding: utf-8 -*-
"""11-10 使用者問「十項原則的口訣」：站上 e104-1 沒有口訣；且 fix_review_9_amber 只改了申論頁，
lj_data（推理版／衝刺）仍是「九項」、漏外部性、最有效使用寫成「合理、合法、可能」三要件。
①考場版（二）加口訣〔自編〕：供替預變，均貢收，適外最（依①～⑩）；②lj_data e104-1 改十項＋§2⑰四前提＋口訣；③申論頁 lj 面板小結補口訣。可重跑。"""
import json, os, glob
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
MN = '供替預變，均貢收，適外最'
MNX = '口訣：<b>%s</b>' % MN
OLD = '（二）估價工作需掌握之十項原則（學理分類）：<br>'
NEW = '（二）估價工作需掌握之十項原則（學理分類）。' + MNX + '<br>'
for f in [os.path.join(H, 'exam', 'exam_ver.json')] + glob.glob(os.path.join(H, 'exam', 'out_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if 'e104-1' not in d: continue
    ch = False
    for b in d['e104-1']:
        if OLD in b[1]: b[1] = b[1].replace(OLD, NEW); ch = True
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=f.endswith('exam_ver.json')); print('改', os.path.basename(f))

LAW = ('供需（價格由供給與需求相互作用決定）；替代（效用相近者價格互相牽制）；預測（價格反映對未來收益與效用之預期）；變動（價格隨價格形成因素變動而變動）；'
       '均衡（內部構成要素組合平衡，價格最高）；貢獻（某要素對整體價格之貢獻決定其價值）；收益遞增遞減（追加投資收益先遞增後遞減）；適合（與環境相適合價格較高）；'
       '外部性（周邊環境與設施對價格之正負影響，如公園、嫌惡設施）；最有效使用（§2⑰：合法、實質可能、正當合理、財務可行四前提下，獲致最高利益之使用）。')
LJ = os.path.join(H, 'lj_data.json'); d = json.load(open(LJ, encoding='utf-8'))
for c in d:
    if c['k'] != 'e104-1': continue
    st = c['subs'][1]['steps'][0]
    st['lawh'] = '十項估價原則'; st['law'] = LAW
    st['res'] = '十項原則逐項列出（含外部性原則）；口訣〔自編〕：%s（依①～⑩）。' % MN
    st['key'] = '供需・替代・預測・變動・均衡・貢獻・遞增遞減・適合・外部性・最有效使用'
    c['subs'][1]['ans'] = '需掌握**供需、替代、預測、變動、均衡、貢獻、收益遞增遞減、適合、外部性、最有效使用**十項原則（口訣：%s），不景氣時特別留意價格日期（§6）、資料蒐集（§3）與特殊交易（§23）。' % MN
    for k in c['checks']:
        k['txt'] = k['txt'].replace('九項原則逐項列出並各附一句重點', '十項原則逐項列出並各附一句重點（含外部性）').replace('九項原則', '十項原則')
    c['mnem'] = '不景氣＝變動原則（兼供需・預測）→ 十原則「%s」→ 結合 §6 價格日期・§3 資料・§23 特殊交易' % MN
    print('lj_data e104-1')
json.dump(d, open(LJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

EP = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html'); s = open(EP, encoding='utf-8').read()
O2 = '十項原則逐項列出（含<b>外部性原則</b>）。'
N2 = '十項原則逐項列出（含<b>外部性原則</b>）；口訣〔自編〕：<b>%s</b>（依①～⑩）。' % MN
if O2 in s and N2 not in s: open(EP, 'w', encoding='utf-8').write(s.replace(O2, N2)); print('申論頁 lj')
