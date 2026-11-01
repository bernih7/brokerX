"""從《不動產估價概要_申論題實戰範文》產生 bxv-essay-meta.js（指揮中心申論入口的後備資料）。
範文頁開過一次就會把最新資料寫進 localStorage 'bx-essay-meta'，指揮中心優先用那份；這支只是沒開過範文頁時的預設值。
範文頁增刪卡片後重跑：python3 tools/essay_meta.py"""
import re, json, os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t=open(os.path.join(R,'不動產估價概要_申論題實戰範文.html'),encoding='utf-8').read()
cards=[]
for m in re.finditer(r'<div class="essay-card([^"]*)" data-v="lj" id="([^"]+)" data-pri="([^"]+)" data-type="([^"]+)">',t):
  cls,cid,pri,typ=m.groups()
  seg=t[m.end():m.end()+1500]
  y=re.search(r'class="card-year[^"]*">([^<]*)<',seg);ti=re.search(r'class="card-title">([^<]*)<',seg)
  k='off' if re.match(r'e\d',cid) else ('pred' if cid.startswith('pred-') else ('mock' if 'mock' in cls else 'other'))
  cards.append(dict(id=cid,pri=pri,typ=typ,k=k,title=((y.group(1).strip()+' ') if y else '')+(ti.group(1).strip() if ti else ''),yr=int(re.match(r'e(\d+)-',cid).group(1)) if k=='off' else 0))
def rank(c):
  if c['k']=='off': return {'A':0,'B':4}.get(c['pri'],5)
  if c['k']=='pred': return 1 if c['pri']=='A' else 2
  if c['k']=='mock': return 3
  return 6
order=[c['id'] for i,c in sorted(enumerate(cards),key=lambda x:(rank(x[1]),-x[1]['yr'],x[0]))]
types={}
for m in re.finditer(r'<button class="chip m-\w+" data-type="(\w+)"[^>]*>([^（<]+)',t): types[m.group(1)]=m.group(2)
M=dict(total=len(cards),off=sum(c['k']=='off' for c in cards),pred=sum(c['k']=='pred' for c in cards),mock=sum(c['k']=='mock' for c in cards),
  ids={c['id']:[c['pri'],c['k'],c['typ'],c['title']] for c in cards},order=order,types=types,t=0)
open(os.path.join(R,'bxv-essay-meta.js'),'w',encoding='utf-8').write('/* 由 tools/essay_meta.py 產生，勿手改 */\nwindow.BXV_ESSAY_META='+json.dumps(M,ensure_ascii=False)+';\n')
print(M['total'],M['off'],M['pred'],M['mock'],order[:5])
