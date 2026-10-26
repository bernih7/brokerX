#!/usr/bin/env python3
"""以章節頁（單一資料來源）為準，同步《估價_考題小卡.html》CARDS 的 exps／note（只動 id 相同的題）。
用法：node tools/quiz_val/extract_items.js > /tmp/quiz_items.json && python3 tools/quiz_val/sync_cards.py [--write]"""
import json,sys
F='估價_考題小卡.html'
s=open(F,encoding='utf-8').read()
a=s.index('const CARDS=')+len('const CARDS=')
d=0;j=a;ins=False;esc=False
while True:
    c=s[j]
    if ins:
        if esc: esc=False
        elif c=='\\': esc=True
        elif c=='"': ins=False
    else:
        if c=='"': ins=True
        elif c=='[': d+=1
        elif c==']':
            d-=1
            if d==0: break
    j+=1
raw=s[a:j+1]
cards=json.loads(raw)
dump=lambda x:json.dumps(x,ensure_ascii=False)
pg={x['id']:x for x in json.load(open('/tmp/quiz_items.json'))}
ne=nn=0;changed=[]
for c in cards:
    p=pg.get(c['id'])
    if not p: continue
    ch=False
    for k in ('q','opts'):
        if c[k]!=p[k]: c[k]=p[k];ch=True;print(k,'更新',c['id'])
    if c['correct']!=p['correct']: c['correct']=p['correct'];ch=True;print('correct 更新',c['id'])
    if c['exps']!=p['exps']: c['exps']=p['exps'];ne+=1;ch=True
    if (c['note'] or None)!=(p['note'] or None): c['note']=p['note'];nn+=1;ch=True
    if ch: changed.append(c)
print('exps 更新',ne,'note 更新',nn,'張數',len(changed))
if '--write' in sys.argv:
    # 只替換有變動的那幾張物件（其餘位元組不動，避免格式雜訊）
    out=raw
    for c in changed:
        start=out.index('{"id": "%s"'%c['id'])
        end=out.find('}, {"id": "',start)
        end=(end+1) if end>=0 else out.rindex('}')+1
        out=out[:start]+dump(c)+out[end:]
    assert len(json.loads(out))==len(cards)
    open(F,'w',encoding='utf-8').write(s[:a]+out+s[j+1:]);print('已寫入')
