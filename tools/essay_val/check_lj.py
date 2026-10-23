#!/usr/bin/env python3
"""檢查 lj_data.json：每子題有 ans；拆解裡的 § 條號都在該卡範文；kw 逐字在卡內；checks 5-9、hot 2-3。"""
import re,sys,json,html
sys.path.insert(0,'/tmp/w')
P='/home/claude/brokerx/不動產估價概要_申論題實戰範文.html'
s=open(P,encoding='utf-8').read()
cards=list(re.finditer(r'<div class="essay-card[^"]*"[^>]*\bid="([^"]+)"',s))
def card(i):
    for k,m in enumerate(cards):
        if m.group(1)==i:
            e=cards[k+1].start() if k+1<len(cards) else len(s)
            return html.unescape(re.sub(r'<[^>]+>','',s[m.start():e]))
def strs(o):
    if isinstance(o,str): yield o
    elif isinstance(o,list):
        for x in o: yield from strs(x)
    elif isinstance(o,dict):
        for x in o.values(): yield from strs(x)
D=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'lj_data.json',encoding='utf-8'))
bad=0
ids=[m.group(1) for m in cards]
for d in D:
    k=d['k']; t=card(k); tn=re.sub(r'\s+','',t)
    if t is None: print(k,'卡不存在'); bad+=1; continue
    for i,sub in enumerate(d['subs'],1):
        if not sub.get('ans','').strip(): print(k,'子題',i,'缺 ans'); bad+=1
        if not sub.get('steps'): print(k,'子題',i,'無 steps'); bad+=1
    body=' '.join(strs([d['subs'],d['checks'],d.get('mnem','')]))
    for n in set(re.findall(r'§\s*\d+(?:-\d+)?',body)):
        num=re.sub(r'\s','',n)
        if num not in tn and ('第'+num[1:]+'條') not in tn:
            print(k,'條號不在卡內',num); bad+=1
    for w in d.get('kw',[]):
        if re.sub(r'\s+','',w) not in tn: print(k,'kw 不在卡內',w); bad+=1
    c=d['checks']
    if not 5<=len(c)<=9: print(k,'checks 數量',len(c)); bad+=1
    h=sum(1 for x in c if x.get('hot'))
    if not 2<=h<=3: print(k,'hot 數量',h); bad+=1
    for x in c:
        if x.get('sub',1)>len(d['subs']): print(k,'check sub 超界'); bad+=1
print('cards',len(D),'bad',bad)
missing=[i for i in ids if i not in {d['k'] for d in D}]
print('missing',missing)
