# -*- coding: utf-8 -*-
"""11-11 使用者截圖《估價_自編補強卷》第8題（DCF 不包含何者）：頁面標 A 為正確答案，但資料 ans＝C、C 解析也寫非 DCF 要素。
原因：舊版殘留的覆寫 QUESTIONS[7].ans=0（原為另一題「A、D 都是 360」的修正，題目重排後指到第8題）。刪除。
順帶：第10題錯選項只寫「計算有誤」，依 v604 規則寫出誤算或正確值。可重跑。"""
import os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(ROOT, '估價_自編補強卷.html'); s = open(P, encoding='utf-8').read()
O = "\n// Fix Q8 answer - both A and D are 360, answer should be A(0)\nQUESTIONS[7].ans=0;\n"
if O in s: s = s.replace(O, "\n"); print('刪覆寫')
O2 = '"380萬計算有誤", "400萬計算有誤", "420萬計算有誤"'
N2 = ('"380萬：無法由題幹常見誤算得到；正確值 200＋160＝360萬", '
      '"400萬：土地套用建物資本化率 5,000×8%＝400萬，率用錯（土地應×4%），且漏了建物淨收益", '
      '"420萬：用簡單平均資本化率（4%＋8%）÷2＝6% 乘總值 7,000萬＝420萬；土地、建物要各乘自己的資本化率"')
if O2 in s: s = s.replace(O2, N2); print('Q10 錯選項')
open(P, 'w', encoding='utf-8').write(s)
