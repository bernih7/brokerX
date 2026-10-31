# 產生 bxl-quiz-data.js：土地法 518 題（題幹／選項／答案／四選項解析），來源＝土地法_考題小卡.html（與解析版練習 QUIZ_DATA 逐題核對過：題集、章別、答案完全一致）
import re,json,os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
c=open(R+'/土地法_考題小卡.html',encoding='utf-8').read()
k=c.find('[{"id": "L99-1"'); cards,_=json.JSONDecoder().raw_decode(c[k:])
out=[]
for x in cards:
    y,n=map(int,re.match(r'L(\d+)-(\d+)',x['id']).groups())
    out.append({"k":f"{y}-{n}","ch":x['group'],"y":y,"n":n,"stem":x['q'],"opt":x['opts'],"ans":x['correct'],"exp":x['exps']})
open(R+'/bxl-quiz-data.js','w',encoding='utf-8').write('/* 土地法共用題庫（給整理頁的考古題面板）。由 tools/land_tq/mk_data.py 產生，不要手改。 */\nwindow.BXL_QUIZ={"q":'+json.dumps(out,ensure_ascii=False,separators=(',',':'))+'};\n')
print(len(out))
