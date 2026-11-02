# 申論篇別按鈕「官方 N・預測 N・模擬 N」與標題總數，依頁面實際卡片重算。可重跑
import re,os
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
f=os.path.join(R,'經紀法規_備考指揮中心.html'); s=open(f,encoding='utf-8').read()
tot={'off':0,'pred':0,'mock':0}
for k in re.findall(r'<div class="ess-panel" data-k="(\w)"',s):
    i=s.find('<div class="ess-panel" data-k="%s"'%k); j=s.find('<div class="ess-panel"',i+10); j=len(s) if j<0 else j
    ids=re.findall(r'<details id="(es-[^"]+)" class="essay-detail',s[i:j])
    o=sum(x.startswith('es-fw') for x in ids); m=sum(x.startswith('es-mk') for x in ids); p=len(ids)-o-m
    tot['off']+=o;tot['pred']+=p;tot['mock']+=m
    lab='官方 %d・預測 %d'%(o,p)+('・模擬 %d'%m if m else '')
    s=re.sub(r'(<button type="button" class="ess-b[^"]*" data-k="%s"><b>[^<]*</b><small>)[^<]*(</small>)'%k,r'\g<1>'+lab+r'\g<2>',s)
s=re.sub(r'申論題（官方 \d+ 題＋預測 \d+ 題＋模擬卷 \d+ 題）','申論題（官方 %d 題＋預測 %d 題＋模擬卷 %d 題）'%(tot['off'],tot['pred'],tot['mock']),s)
open(f,'w',encoding='utf-8').write(s); print(tot)
