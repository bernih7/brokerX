# -*- coding: utf-8 -*-
"""土地法章節統一（2026-10-27）：以題庫 7 頁為準＋3 題改章，同步解析版 QUIZ_DATA 與考題小卡。
可重複執行。輸出 tools/land_chmap.json（year-num → ch）。"""
import re,json,glob,io,os,collections
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOVE={('114','17'):'E1',('112','3'):'E2',('110','20'):'E2'}
PAGE={'A1':'A1A2','A2':'A1A2','A3':'A3A4A5','A4':'A3A4A5','A5':'A3A4A5','B1':'B','B2':'B','B3':'B','C1':'C','C2':'C','C3':'C','C4':'C','D1':'D','D2':'D','D3':'D','D4':'D','E1':'E','E2':'E','F1':'FGHI','G1':'FGHI','H1':'FGHI','I1':'FGHI'}
NM={'A1':'A1 總則','A2':'A2 土地登記','A3':'A3 共有優先購買權','A4':'A4 基地耕地租賃','A5':'A5 公有土地','B1':'B1 區域計畫法','B2':'B2 都市計畫法','B3':'B3 國土計畫法','C1':'C1 規定地價','C2':'C2 市地重劃','C3':'C3 照價收買空地稅','C4':'C4 申報登錄預售屋','D1':'D1 徵收程序要件','D2':'D2 徵收補償標準','D3':'D3 區段徵收','D4':'D4 撤銷廢止徵收','E1':'E1 地價稅','E2':'E2 土地增值稅','F1':'F1 房屋稅','G1':'G1 契稅','H1':'H1 房地合一稅','I1':'I1 耕地三七五減租'}
pages={};cards={}
for f in glob.glob(os.path.join(R,'LandLaw_*_quiz.html')):
  s=io.open(f,encoding='utf-8').read();m=re.search(r'window\.BX_CARDS=(\[.*?\]);',s,re.S)
  pages[f]=(s,m,json.loads(m.group(1)))
allc=[]
for f,(s,m,C) in pages.items(): allc+=C
# apply moves
for c in allc:
  k=(c['year'],str(c['num']))
  if k in MOVE: c['ch']=MOVE[k]
CHMAP={c['year']+'-'+str(c['num']):c['ch'] for c in allc}
# redistribute into pages by PAGE
newp=collections.defaultdict(list)
for c in allc: newp[PAGE[c['ch']]].append(c)
for f,(s,m,C) in pages.items():
  key=re.search(r'LandLaw_(.+)_quiz',f).group(1)
  L=sorted(newp[key],key=lambda c:(c['ch'],int(c['year']),int(c['num'])))
  s=s[:m.start(1)]+json.dumps(L,ensure_ascii=False)+s[m.end(1):]
  io.open(f,'w',encoding='utf-8').write(s)
# 解析版
f=os.path.join(R,'土地法解析版練習.html');s=io.open(f,encoding='utf-8').read()
i=s.find('const QUIZ_DATA = ')+len('const QUIZ_DATA = ');j=s.find('];',i)+1
Q=json.loads(s[i:j]);n=0
for q in Q:
  c=CHMAP[q['year']+'-'+str(q['num'])]
  if q['chapter']!=c: q['chapter']=c;q['chapterName']=NM[c];n+=1
s=s[:i]+json.dumps(Q,ensure_ascii=False)+s[j:];io.open(f,'w',encoding='utf-8').write(s)
# 考題小卡
f=os.path.join(R,'土地法_考題小卡.html');s=io.open(f,encoding='utf-8').read();k=0
def fix(mm):
  global k
  d=json.loads(mm.group(0));y,nn=re.match(r'(\d+)年第(\d+)題',d['year']).groups();c=CHMAP[y+'-'+nn]
  if d['group']!=c:
    k+=1;old=d['group'];d['group']=c
    if d['cat'].startswith(old):d['cat']=NM[c].replace(c+' ',c+' ',1) if not d['cat'] else d['cat'].replace(old,c,1)
  return json.dumps(d,ensure_ascii=False)
s=re.sub(r'\{"id": "L[^{}]*?"exps": \[.*?\]\}',fix,s);io.open(f,'w',encoding='utf-8').write(s)
json.dump(CHMAP,io.open(os.path.join(R,'tools','land_chmap.json'),'w',encoding='utf-8'),ensure_ascii=False)
print('解析版改',n,'小卡改',k,collections.Counter(CHMAP.values()))
