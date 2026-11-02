# 移除經紀法規申論「多層次傳銷」（100-二 / es-fw10 / T17），可重跑
import json,re,os
os.chdir(os.path.join(os.path.dirname(__file__),'..','..'))
def rd(f): return open(f,encoding='utf-8').read()
def wr(f,s): open(f,'w',encoding='utf-8').write(s)

# 1) 指揮中心：刪卡、官方範文 G 組題數
f='經紀法規_備考指揮中心.html'; s=rd(f)
i=s.find('<details id="es-fw10"')
if i>=0:
    j=s.find('</details>',s.find('<label class="esdone"',i))+len('</details>')
    s=s[:i]+s[j:]
    # G 組「官方範文（真題 3 題）」→ 2
    k=s.find('<div class="ess-panel" data-k="g"')
    m=s.find('官方範文（真題 3 題）',k)
    if m>0 and m-k<2000: s=s[:m]+'官方範文（真題 2 題）'+s[m+len('官方範文（真題 3 題）'):]
s=s.replace('；含已退場的多層次傳銷（100-二）','')
s=s.replace('<span>官方 0／32</span>','<span>官方 0／31</span>')
wr(f,s)

# 2) 115 出題預測：拿掉 T17 主題、100-二 格子不連結
f='經紀法規_申論115出題預測.html'; s=rd(f)
a=s.find('var D=');b=s.find('\n',a)
D=json.loads(s[a+6:b].rstrip().rstrip(';'))
D['topics']=[t for t in D.get('topics',[]) if t.get('code')!='T17'] if 'topics' in D else D.get('topics')
for r in D['grid']:
    for q in r['q']:
        if q.get('fw')=='fw10':
            q.pop('fw',None); q['t']='多層次傳銷（不在考試範圍）'
s=s[:a]+'var D='+json.dumps(D,ensure_ascii=False)+';'+s[b:]
s=s.replace("var a=document.createElement('a');a.className='cell p'+p;a.href=HUB+'#es-'+q.fw;",
            "var a=document.createElement(q.fw?'a':'div');a.className='cell p'+p;if(q.fw)a.href=HUB+'#es-'+q.fw;")
s=s.replace('二、17 個主題','二、16 個主題').replace('>全部 17<','>全部 16<')
s=s.replace('<button class="tbtn" data-t="退場">退場 1</button>','')
wr(f,s)

# 3) 篇章主題答題模板：刪 100-二 範例
f='經紀法規申論題_篇章主題答題模板.html'; s=rd(f)
a=s.find('const GROUPS = ');b=s.find('\n',a)
G=json.loads(s[a+len('const GROUPS = '):b].rstrip().rstrip(';'))
for g in G:
    g['examples']=[e for e in g.get('examples',[]) if '多層次' not in e.get('tag','')]
    g['signal']=g['signal'].replace('、多層次傳銷（已退場考點）','')
s=s[:a]+'const GROUPS = '+json.dumps(G,ensure_ascii=False)+';'+s[b:]
s=s.replace('/30題','/29題').replace('30題收錄','29題收錄').replace('本頁只收 30 題','本頁只收 29 題')
wr(f,s)

# 4) 資料源：essays / lj 拿掉 es-fw10，避免重 build 又長回來
for f in ['tools/essay_jj/essays.json','tools/essay_jj/lj_data.json','tools/essay_jj/lj_in/in_6.json','tools/essay_jj/lj_out/out_6.json']:
    if not os.path.exists(f): continue
    d=json.loads(rd(f))
    def keep(x): return not (isinstance(x,dict) and (x.get('eid') in('es-fw10','fw10') or x.get('id') in('es-fw10','fw10') or x.get('k') in('es-fw10','fw10')))
    if isinstance(d,list): d2=[x for x in d if keep(x)]
    elif isinstance(d,dict):
        d2={k:v for k,v in d.items() if k not in('es-fw10','fw10') and keep(v)}
        for k,v in list(d2.items()):
            if isinstance(v,list): d2[k]=[x for x in v if keep(x)]
    print(f, len(d), '->', len(d2)); wr(f,json.dumps(d2,ensure_ascii=False,indent=1))

# 5) 指揮中心公平法分頁按鈕題數
f='經紀法規_備考指揮中心.html'; s=rd(f)
wr(f,s.replace('<b>公平交易法</b><small>官方 3・預測 7</small>','<b>公平交易法</b><small>官方 2・預測 7</small>'))

# 6) 答題模板進度鍵依索引（g_0 是多層次），移除後 g_1→g_0、g_2→g_1；一次性搬移
MIG="(function(){try{var K='brokerlaw_essay_template_mastery_v2',F='bxj-tpl-mig-1102';if(localStorage.getItem(F))return;var m=JSON.parse(localStorage.getItem(K)||'{}'),n={};Object.keys(m).forEach(function(k){if(k.indexOf('g_')!==0){n[k]=m[k];return}var i=+k.slice(2);if(i>0)n['g_'+(i-1)]=m[k]});localStorage.setItem(K,JSON.stringify(n));localStorage.setItem(F,'1')}catch(e){}})();\n"
f='bxj-use.js'; s=rd(f)
if 'bxj-tpl-mig-1102' not in s: s=MIG+s
s=s.replace('er+em,30,"已讀 "+(er+em)+"／30 題範例','er+em,29,"已讀 "+(er+em)+"／29 題範例')
wr(f,s)
f='經紀法規申論題_篇章主題答題模板.html'; s=rd(f)
if 'bxj-tpl-mig-1102' not in s: s=s.replace("const STORAGE_KEY = 'brokerlaw_essay_template_mastery_v2';",MIG+"const STORAGE_KEY = 'brokerlaw_essay_template_mastery_v2';",1)
wr(f,s)
