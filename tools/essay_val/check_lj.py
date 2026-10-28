#!/usr/bin/env python3
"""檢查 lj_data.json：每子題有 ans；拆解裡的 § 條號都在該卡範文；kw 逐字在卡內；checks 5-9、hot 2-3。"""
import re,sys,json,html
sys.path.insert(0,'/tmp/w')
P='/home/claude/brokerx/不動產估價概要_申論題實戰範文.html'
s=open(P,encoding='utf-8').read()
cards=list(re.finditer(r'<div class="essay-card[^"]*"[^>]*\bid="([^"]+)"',s))
def card_html(i):
    for k,m in enumerate(cards):
        if m.group(1)==i:
            e=cards[k+1].start() if k+1<len(cards) else len(s)
            return s[m.start():e]
def card(i):
    h=card_html(i)
    return None if h is None else html.unescape(re.sub(r'<[^>]+>','',h))
def card_nokw(i):
    """剝掉「得分關鍵詞」區（.sk2）再取文字。
    kw 檢查若用整張卡，關鍵詞自己就在卡裡，檢查形同虛設——
    2026-10-29 外部審稿時發現 e101-2／e114-1 列了內容裡根本沒有的詞卻照樣通過。"""
    h=card_html(i)
    if h is None: return None
    h=re.sub(r'<div class="sk2"[^>]*>.*?</div>\s*(?=<div class="detail-content")','',h,flags=re.S)
    h=re.sub(r'<div class="sk2c">.*?</div>','',h,flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>','',h))
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
    tk=re.sub(r'\s+','',card_nokw(k) or '')
    for w in d.get('kw',[]):
        if re.sub(r'\s+','',w) not in tk: print(k,'kw 不在卡內（扣除關鍵詞區）',w); bad+=1
    c=d['checks']
    if not 5<=len(c)<=9: print(k,'checks 數量',len(c)); bad+=1
    h=sum(1 for x in c if x.get('hot'))
    if not 2<=h<=3: print(k,'hot 數量',h); bad+=1
    for x in c:
        if x.get('sub',1)>len(d['subs']): print(k,'check sub 超界'); bad+=1
print('cards',len(D),'bad',bad)
missing=[i for i in ids if i not in {d['k'] for d in D}]
print('missing',missing)
