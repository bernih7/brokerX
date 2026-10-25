#!/usr/bin/env python3
"""由章節頁 ITEMS（extract_items.js 輸出）產生 bxv-quiz-data.js（估價解析版練習用）。
用法（repo 根目錄）：node tools/quiz_val/extract_items.js > /tmp/quiz_items.json && python3 tools/quiz_val/gen_data.py"""
import json,re
items=json.load(open('/tmp/quiz_items.json'))
LAB={"A1":"A1 估價原則","A2":"A2 價格種類","A3":"A3 影響因素","A4":"A4 估價程序","B":"B 比較法","C1":"C1 重建成本","C2":"C2 折舊計算","D1":"D1 直接資本化","D2":"D2 資本化率","D3":"D3 DCF","E1":"E1 土地開發","F1":"F1 租金估計","G1":"G1 樓層效用","H1H2":"H1H2 特殊宗地","H3I1":"H3I1 都更CAMA","I2J1":"I2J1 土地改良物・特殊宗地"}
GRP={"A1":"A","A2":"A","A3":"A","A4":"A","B":"B","C1":"C","C2":"C","D1":"D","D2":"D","D3":"D","E1":"E","F1":"F","G1":"G","H1H2":"H","H3I1":"H","I2J1":"H"}
GNAME={"A":"基礎原則・程序","B":"比較法","C":"成本法","D":"收益法","E":"土地開發","F":"租金估計","G":"樓層效用","H":"特殊標的"}
UNIT=re.compile(r'萬|元|%|％|坪|平方|㎡|m2|年|倍|率|公頃|公尺|億')
NOT_CALC={'VB1_105_37','VB1_105_38','VE1_104_23','VI1_107_4','VI1_111_6','VC1_112_11'}  # 選項有數字但屬記條文，不算計算題
def is_calc(it):
    if it['id'] in NOT_CALC: return False
    nums=sum(1 for o in it['opts'] if re.search(r'\d',o))
    return nums>=3 and re.search(r'\d',it['q']) is not None and UNIT.search(it['q']+''.join(it['opts'])) is not None
out=[]
for it in items:
    m=re.match(r'(\d+)年第(\d+)題',it['year'])
    y,n=(int(m.group(1)),int(m.group(2))) if m else (0,0)
    o={"id":it['id'],"ch":it['ch'],"cat":it['cat'],"year":it['year'],"y":y,"n":n,"q":it['q'],"opts":it['opts'],"exps":it['exps'],"correct":it['correct']}
    if it['note']: o["note"]=it['note']
    if is_calc(it): o["calc"]=1
    out.append(o)
js="/* 由 tools/quiz_val/gen_data.py 產生（來源：16 個估價刷題章節頁的 ITEMS）；不要手改，改題請改章節頁後重跑。 */\n"
js+="window.BXV_QUIZ={labels:%s,groups:%s,gnames:%s,items:[\n"%(json.dumps(LAB,ensure_ascii=False),json.dumps(GRP),json.dumps(GNAME,ensure_ascii=False))
js+=",\n".join(json.dumps(o,ensure_ascii=False,separators=(',',':')) for o in out)+"\n]};\n"
open('bxv-quiz-data.js','w',encoding='utf-8').write(js)
import collections
print('items',len(out),'calc',sum(1 for o in out if o.get('calc')),dict(collections.Counter(o['ch'] for o in out if o.get('calc'))),'bytes',len(js.encode()))
