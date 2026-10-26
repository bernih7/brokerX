# 產生《民法_法條解析練習》資料 quiz_data.json
# 來源：刷題 A～E 篇（題目、答案、逐選項解析、多重給分）＋完整小卡（小類、陷阱）＋ law.json（KB 核實表＋補遺逐字）
# law.json 由 mklaw.py 從 law/（KB 核實表＋補遺 1017～1020）產生。
# 對齊：年份＋題號（全科唯一）。共用紀錄 bxm-q2 的 id＝「刷題篇別-年-題」，所以 p 一律取刷題頁篇別。
import re,json,os,collections
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
def arr(s,start):
    i=s.index('[',start);d=0
    for j in range(i,len(s)):
        if s[j]=='[':d+=1
        elif s[j]==']':
            d-=1
            if d==0:return json.loads(s[i:j+1])
QS={}
for p in 'ABCDE':
    s=open(os.path.join(R,'民法刷題練習_%s篇.html'%p),encoding='utf-8').read()
    for q in arr(s,s.index('const QS=')): QS[(q['year'],q['num'])]=(p,q)
ACODE={'自然人':'A1','法人':'A2','物':'A3','法律行為效力':'A4','意思表示瑕疵':'A5','代理':'A6','消滅時效除斥期間':'A7'}
CARD={}
for f in ['民法A_完整考題小卡','民法BC_完整考題小卡','民法D_完整考題小卡','民法E_完整考題小卡']:
    s=open(os.path.join(R,f+'.html'),encoding='utf-8').read()
    for c in arr(s,s.index('"cat"')-400 if False else s.index('[{"id"')):
        y,n=map(int,re.match(r'(\d+)年第(\d+)題',c['year']).groups())
        cat=c['cat']; code=ACODE.get(cat) or cat[:2]; name=ACODE.get(cat) and cat or cat[2:]
        CARD[(y,n)]=(code,name,c.get('trap',''))
LAW=json.load(open(os.path.join(H,'law.json'),encoding='utf-8'))  # mklaw.py 產生
OTHER=re.compile(r'(土地法|土地登記規則|公寓大廈|消保法|消費者保護法|條例|細則|家事事件法|強制執行法|憲法|刑法|民事訴訟法|非訟)\s*$')
ART=re.compile(r'§\s*(\d+)(?:\s*[-之]\s*(\d+))?|第\s*(\d+)\s*條(?:\s*之\s*(\d+))?')
def arts(txt):
    out=[]
    for m in ART.finditer(txt):
        pre=txt[max(0,m.start()-12):m.start()]
        if OTHER.search(pre): continue
        a=m.group(1) or m.group(3); b=m.group(2) or m.group(4)
        k=a+('-'+b if b else '')
        if k in LAW and k not in out: out.append(k)
    return out
# 完整小卡分類明顯錯置者，依題目內容改歸（11 題）
FIX={'114-14':'C4','110-20':'E2','110-21':'E2','107-6':'D6','104-36':'E3','103-29':'E2','102-16':'B6','102-27':'C1','101-12':'B2','100-10':'C3','99-40':'E2'}
MEMP=os.path.join(H,'mem.json'); MEM=json.load(open(MEMP,encoding='utf-8')) if os.path.exists(MEMP) else {}  # gen_mem.py 產生
CHN={}; OUT=[]
def kk(x): return [int(t) for t in x.split('-')]
for (y,n),(p,q) in sorted(QS.items(),key=lambda t:(-t[0][0],t[0][1])):
    code,name,trap=CARD[(y,n)]; CHN[code]=name
    code=FIX.get('%d-%d'%(y,n),code)
    exps=[];tip=[]
    for e in q['exp']:
        m=re.match(r'[✓✗]\s*([ABCD])(?:（[^）]*）)?\s*[\.．、:：]\s*',e)
        if m: exps.append(e[m.end():])
        else: tip.append(re.sub(r'^★\s*','',e))
    assert len(exps)==4,(y,n)
    acc=list(q['ans']) if q['ans'] else list(q['acc'])
    law=sorted(arts(q['stem']+'｜'+'｜'.join(q['opts'])+'｜'+'｜'.join(q['exp'])),key=kk)[:6]
    o={'k':'%d-%d'%(y,n),'y':y,'n':n,'p':p,'ch':code,'stem':q['stem'],'opt':q['opts'],'acc':acc,'exp':exps,'law':law}
    if tip: o['tip']=tip
    if q.get('note'): o['note']=q['note']
    if not q['ans'] and not q['acc']: o['free']=1
    if o['k'] in MEM: o['mem']=MEM[o['k']]
    OUT.append(o)
used=sorted({k for q in OUT for k in q['law']},key=kk)
law={k:LAW[k] for k in used}
json.dump({'q':OUT,'law':law},open(os.path.join(H,'quiz_data.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
ORDER=['A1','A2','A3','A4','A5','A6','A7','B1','B2','B3','B4','B5','B6','C1','C2','C3','C4','C5','D1','D2','D3','D4','D5','D6','E1','E2','E3','E4']
cnt=collections.Counter(q['ch'] for q in OUT)
json.dump({c:'%s %s'%(c,CHN[c]) for c in ORDER},open(os.path.join(H,'chapters.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('題數',len(OUT),'有相關法條',sum(1 for q in OUT if q['law']),'用到條文',len(law),'小類',len(cnt))
