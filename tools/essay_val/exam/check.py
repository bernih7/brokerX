# 驗證估價考場版 out_N.json：四塊標題、字數、條號與引文都必須出自完整版
import json,re,sys,os
D=os.path.dirname(os.path.abspath(__file__))
H=['一、意義','二、法條','三、涵攝','四、結論']
def norm(t): return re.sub(r'\s+','',t)
def plain(t): return re.sub(r'<[^>]+>','',t)
def arts(t):
    t=norm(t); r=set()
    for m in re.finditer(r'§(\d+(?:-\d+)?)',t): r.add(m.group(1))
    for m in re.finditer(r'第(\d+(?:條之\d+)?)條',t): r.add(m.group(1))
    return r
def check(n):
    src={x['id']:x for x in json.load(open(f'{D}/in_{n}.json',encoding='utf-8'))}
    out=json.load(open(f'{D}/out_{n}.json',encoding='utf-8')); errs=[]
    for cid,x in src.items():
        v=out.get(cid)
        if not v: errs.append(f'{cid} 缺'); continue
        if [b[0] for b in v]!=H: errs.append(f'{cid} 標題須為 {H}'); continue
        body=''.join(plain(b[1]) for b in v); L=len(norm(body)); F=len(norm(x['full']))
        lo=min(700,int(F*0.8)); hi=min(1000 if x['calc'] else 850, F)
        if not(lo<=L<=hi): errs.append(f'{cid} 字數 {L}（應 {lo}～{hi}，完整版 {F}）')
        if re.search(r'<(?!br\s*/?>|/?b>)[^>]+>',''.join(b[1] for b in v)): errs.append(f'{cid} 只能用 <br> 與 <b>')
        miss=arts(body)-arts(x['full'])
        if miss: errs.append(f'{cid} 完整版沒有的條號：{sorted(miss)}')
        for q in re.findall(r'「([^」]{6,})」',body):
            if norm(q) not in norm(x['full']): errs.append(f'{cid} 引文不在完整版：「{q[:30]}」')
    return errs
for n in (sys.argv[1:] or [str(i) for i in range(1,7)]):
    if not os.path.exists(f'{D}/out_{n}.json'): print(f'part {n}: 尚無 out'); continue
    e=check(n); print(f'part {n}: '+('OK' if not e else f'{len(e)} 個問題')); [print('  ',x) for x in e[:30]]
