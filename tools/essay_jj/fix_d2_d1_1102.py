# es-d2 履約擔保 四種→五種（第七點之一含公會辦理連帶保證協定）；es-d1 審閱期含糊語寫定三日。可重跑
import json,os,re
os.chdir(os.path.join(os.path.dirname(__file__),'..','..'))
def fix_d2(t):
    t=t.replace('價金信託、價金返還保證、同業連帶擔保','價金返還之保證、價金信託、同業連帶擔保、公會辦理連帶保證協定')
    return t.replace('四種','五種')
D1_OLD='<b>確切日數待查官方公告原文</b>，勿憑記憶作答'
D1_NEW='委託銷售契約依其應記載事項第一點，審閱期間「不得少於三日」'
def fix_d1(t): return t.replace(D1_OLD,D1_NEW).replace('確切日數待查官方公告原文，勿憑記憶作答',D1_NEW)
f='經紀法規_備考指揮中心.html'; s=open(f).read()
for cid,fn in [('es-d2',fix_d2),('es-d1',fix_d1)]:
    a=s.find('<details id="%s"'%cid); b=s.find('<details id="es-',a+10)
    s=s[:a]+fn(s[a:b])+s[b:]
open(f,'w').write(s)
for f in ['tools/essay_jj/essays.json','tools/essay_jj/lj_data.json','tools/essay_jj/lj_in/in_6.json','tools/essay_jj/lj_out/out_6.json']+[os.path.join('tools/essay_jj/lj_in',x) for x in os.listdir('tools/essay_jj/lj_in')]+[os.path.join('tools/essay_jj/lj_out',x) for x in os.listdir('tools/essay_jj/lj_out')]:
    d=json.load(open(f)); ch=0
    for x in d:
        k=x.get('eid') or x.get('k')
        if k in('es-d2','d2'): y=json.loads(fix_d2(json.dumps(x,ensure_ascii=False))); ch+=y!=x; x.clear(); x.update(y)
        if k in('es-d1','d1'): y=json.loads(fix_d1(json.dumps(x,ensure_ascii=False))); ch+=y!=x; x.clear(); x.update(y)
    if ch: json.dump(d,open(f,'w'),ensure_ascii=False,indent=1); print(f,ch)
# 其他頁面同步
for f in ['經紀法規_備考指揮中心.html','經紀法規_定型化契約專區.html']:
    s=open(f).read()
    s=re.sub(r'履約擔保(<[^>]+>)?四種方式',lambda m:'履約擔保'+(m.group(1) or '')+'五種方式',s)
    open(f,'w').write(s.replace('價金信託、價金返還保證、同業連帶擔保','價金返還之保證、價金信託、同業連帶擔保、公會辦理連帶保證協定'))
f='經紀法規_備考指揮中心.html'; s=open(f).read()
open(f,'w').write(s.replace('價金返還保證、同業連帶擔保','價金返還之保證、同業連帶擔保、公會辦理連帶保證協定'))
