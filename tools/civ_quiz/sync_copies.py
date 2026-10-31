# 刷題 A～E 篇（const QS）是民法 520 題解析的唯一來源。本檔把解析同步到兩份副本：
#   ① 四支《完整考題小卡》的 exps（＋★ 總結 → trap）
#   ② 《民法概要_25題模擬測驗》PAPERS（107～114 整卷）的 exps（＋★ → trap）
# 之後請再跑 mkdata.py → build.py 更新《法條解析練習》。可重複執行。
import re,json,os,sys
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
def span(s,start):
    i=s.index('[',start);d=0;ins=False;esc=False
    for j in range(i,len(s)):
        c=s[j]
        if ins:
            if esc:esc=False
            elif c=='\\':esc=True
            elif c=='"':ins=False
            continue
        if c=='"':ins=True
        elif c=='[':d+=1
        elif c==']':
            d-=1
            if d==0:return i,j+1
PRE=re.compile(r'[✓✗]\s*([ABCD])(?:（[^）]*）)?\s*[\.．、:：]\s*')
QS={}
for p in 'ABCDE':
    s=open(os.path.join(R,'民法刷題練習_%s篇.html'%p),encoding='utf-8').read();a,b=span(s,s.index('const QS='))
    for q in json.loads(s[a:b]):
        ex=[];tip=[]
        for e in q['exp']:
            m=PRE.match(e)
            if m: ex.append(e[m.end():])
            else: tip.append(re.sub(r'^★\s*','',e))
        assert len(ex)==len(q['opts']),(q['year'],q['num'])
        QS[(q['year'],q['num'])]=(ex,tip)
n1=n2=0
def upd(c,yn):
    ex,tip=QS[yn];ch=0
    if c['exps']!=ex: c['exps']=ex;ch=1
    if tip and c.get('trap')!=tip[0]: c['trap']=tip[0];ch=1
    return ch
for f in ['民法A_完整考題小卡','民法BC_完整考題小卡','民法D_完整考題小卡','民法E_完整考題小卡']:
    fn=os.path.join(R,f+'.html');s=open(fn,encoding='utf-8').read();a,b=span(s,s.index('[{"id"'))
    C=json.loads(s[a:b]);assert json.dumps(C,ensure_ascii=False)==s[a:b]
    for c in C:
        y,n=map(int,re.match(r'(\d+)年第(\d+)題',c['year']).groups());n1+=upd(c,(y,n))
    open(fn,'w',encoding='utf-8').write(s[:a]+json.dumps(C,ensure_ascii=False)+s[b:])
fn=os.path.join(R,'民法概要_25題模擬測驗.html');s=open(fn,encoding='utf-8').read();i=s.index('const PAPERS=')+13
P,e=json.JSONDecoder().raw_decode(s[i:]);assert json.dumps(P,ensure_ascii=False)==s[i:i+e]
for y,Lq in P.items():
    for c in Lq:
        yy,nn=map(int,re.match(r'(\d+)年第(\d+)題',c['year']).groups());n2+=upd(c,(yy,nn))
open(fn,'w',encoding='utf-8').write(s[:i]+json.dumps(P,ensure_ascii=False)+s[i+e:])
print('完整小卡更新',n1,'題；整卷模擬更新',n2,'題')
