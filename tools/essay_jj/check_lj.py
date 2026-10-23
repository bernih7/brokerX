# 邏輯拆解資料自動檢查：①條號都出現在該題範文 ②每子題有答案 ③checks 5–9 點且 sub 合法
import json,os,re,sys
HERE=os.path.dirname(os.path.abspath(__file__))
ES={x['eid']:x for x in json.load(open(os.path.join(HERE,'essays.json'),encoding='utf-8'))}
f=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'lj_data.json')
D=json.load(open(f,encoding='utf-8'))
ART=re.compile(r'§\s*\d+(?:\s*[之\-]\s*\d+)?')
CNUM={'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn(t):
    if t.isdigit(): return int(t)
    if '十' not in t: return sum(CNUM.get(c,0) for c in t) if len(t)==1 else int(''.join(str(CNUM.get(c,0)) for c in t))
    a,_,b=t.partition('十')
    return (CNUM.get(a,1) if a else 1)*10+(CNUM.get(b,0) if b else 0)
def cn2art(t):
    out=[]
    for m in re.finditer(r'第([0-9一二三四五六七八九十百]+)條(?:之([0-9一二三四五六七八九十]+))?',t):
        a=cn(m.group(1)); out.append('§%d'%a)
        if m.group(2): out.append('§%d之%d'%(a,cn(m.group(2))))
    for m in re.finditer(r'§\s*(\d+)\s*[-之]\s*(\d+)',t): out.append('§%s之%s'%(m.group(1),m.group(2)))
    for m in re.finditer(r'第([0-9一二三四五六七八九十]+)點',t): out.append('§%d點'%cn(m.group(1)))
    return ''.join(out)
def norm(a):
    a=a.replace(' ','').replace('-','之')
    return a
bad=0
for d in D:
    k=d['k']; e=ES.get(k)
    if not e: print('✗',k,'essays.json 查無此題'); bad+=1; continue
    raw=e['full']+e['quick']+e['keys']+e['question']
    pool=norm(raw)+cn2art(raw)
    txt=json.dumps(d,ensure_ascii=False)
    arts={norm(a) for a in ART.findall(txt)}
    miss=[a for a in sorted(arts) if a not in pool]
    if miss: print('✗',k,'條號不在範文內：',miss); bad+=1
    for i,sb in enumerate(d['subs'],1):
        if not sb.get('ans','').strip(): print('✗',k,'子題',i,'沒有答案'); bad+=1
        if not sb.get('steps'): print('✗',k,'子題',i,'沒有步驟'); bad+=1
        for st in sb['steps']:
            if bool(st.get('lawh'))!=bool(st.get('law')): print('✗',k,'子題',i,'lawh/law 必須同時有或同時無'); bad+=1
            for need in ('ask','fact','key'):
                if not st.get(need): print('✗',k,'子題',i,'缺',need); bad+=1
    n=len(d.get('checks',[]))
    if not (5<=n<=9): print('✗',k,'採分點',n,'點（應 5–9）'); bad+=1
    for c in d.get('checks',[]):
        if c['t'] not in ('law','fact','ans'): print('✗',k,'checks t 非法:',c['t']); bad+=1
        if not (1<=c['sub']<=len(d['subs'])): print('✗',k,'checks sub 超出子題數'); bad+=1
print(('全部通過' if not bad else f'共 {bad} 項問題'),f'｜題數 {len(D)}')
sys.exit(1 if bad else 0)
