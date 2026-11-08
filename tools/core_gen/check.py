# 用法：python3 tools/core_gen/check.py land01   → 檢查 out/land01.json 對 in/land01.json
import json,sys
b=sys.argv[1];I=json.load(open('tools/core_gen/in/%s.json'%b))
try:O=json.load(open('tools/core_gen/out/%s.json'%b))
except Exception as e:print('讀不到輸出或 JSON 格式錯：',e);sys.exit(1)
bad=[]
for q in I:
    c=O.get(q['k'])
    if not isinstance(c,list) or len(c)!=len(q['opt']):bad.append((q['k'],'缺題或數量不對'));continue
    for i,t in enumerate(c):
        if not isinstance(t,str) or not t.strip():bad.append((q['k'],i,'空白'));continue
        n=len(t)
        if n<4 or n>24:bad.append((q['k'],i,'長度%d'%n,t))
        if any(x in t for x in '\n「」<>'):pass
        if t.endswith('。'):bad.append((q['k'],i,'句尾不要句號',t))
extra=set(O)-set(q['k'] for q in I)
if extra:bad.append(('多出的題號',sorted(extra)))
print('OK' if not bad else '\n'.join(map(str,bad)));print('題數',len(I),'已寫',len([k for k in O if k in {q["k"] for q in I}]))
