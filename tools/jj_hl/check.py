# 驗證 out_N.json：格式、每個詞須為該條解析的原文子字串、長度與數量限制
import json,sys,glob,os
D=os.path.dirname(os.path.abspath(__file__))
BAN=['敘述正確','非本題答案','本題答案','敘述錯誤','正確答案','錯誤敘述']
def check(n):
    src={x['k']:x for x in json.load(open(f'{D}/in_{n}.json',encoding='utf-8'))}
    out=json.load(open(f'{D}/out_{n}.json',encoding='utf-8'))
    errs=[]
    for k,x in src.items():
        if k not in out: errs.append(f'{k} 缺'); continue
        v=out[k]
        if not isinstance(v,list) or len(v)!=len(x['exp']): errs.append(f'{k} 長度'); continue
        for i,ps in enumerate(v):
            e=x['exp'][i] or ''
            if not isinstance(ps,list) or len(ps)>2: errs.append(f'{k}[{i}] 數量'); continue
            if e.strip() and not ps: errs.append(f'{k}[{i}] 空（解析有字卻沒標）')
            for p in ps:
                if p not in e: errs.append(f'{k}[{i}] 不是原文：{p}')
                if not(2<=len(p)<=24): errs.append(f'{k}[{i}] 長度{len(p)}：{p}')
                if any(b in p for b in BAN): errs.append(f'{k}[{i}] 標了套話：{p}')
            if len(ps)==2 and (ps[0] in ps[1] or ps[1] in ps[0]): errs.append(f'{k}[{i}] 重疊：{ps}')
    extra=set(out)-set(src)
    if extra: errs.append(f'多出的 key：{sorted(extra)[:5]}')
    return errs
for n in (sys.argv[1:] or ['1','2','3','4','5']):
    e=check(n); print(f'part {n}: {"OK" if not e else str(len(e))+" 個問題"}'); [print('  ',x) for x in e[:40]]
