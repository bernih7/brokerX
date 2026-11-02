# 用法：python3 check_ev.py ev_6.json  → 檢查字數、條號是否見於完整版、「」引文是否逐字
import json,re,sys,os
D=os.path.dirname(os.path.abspath(__file__))
full=json.load(open(os.path.join(D,'src/todo_full.json')))
law=json.load(open(os.path.join(D,'../law/lawfull.json')))
lawtxt=json.dumps(law,ensure_ascii=False)
def norm(x): return re.sub(r'\s|<br>','',x)
ev=json.load(open(sys.argv[1])); bad=0
for cid,blocks in ev.items():
  if cid not in full: print(cid,'不在待做清單'); bad+=1; continue
  F=full[cid]['full']+full[cid]['question']; t=''.join(b[1] for b in blocks); n=len(norm(re.sub(r'<[^>]+>','',t)))
  hs=[b[0] for b in blocks]
  if hs!=['一、意義','二、法條','三、涵攝','四、結論']: print(cid,'標題錯',hs); bad+=1
  arts=set(re.findall(r'第\d+條(?:之\d+)?',t))|set(re.findall(r'§\d+(?:之\d+|-\d+)?',t))
  fa=F+lawtxt
  miss=[a for a in arts if a not in F and a.replace('第','§').replace('條','') not in F]
  q=[x for x in re.findall(r'「([^」]{6,})」',t) if norm(x) not in norm(F) and norm(x) not in norm(lawtxt)]
  flag='' if 600<=n<=900 else ' ⚠字數'
  print(f'{cid} {n}字{flag} 條號不在完整版:{miss} 引文非逐字:{q[:3]}')
  if miss or q: bad+=1
print('問題卡數',bad)
