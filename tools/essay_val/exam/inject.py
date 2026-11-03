# 把 exam_ver.json（合併 out_*.json）注入《不動產估價概要_申論題實戰範文》：加「考場版」分頁（可重複執行）
import json,glob,os,re,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import render_ev as RV
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(os.path.dirname(os.path.dirname(D)))
P=f'{R}/不動產估價概要_申論題實戰範文.html'
data={}
if os.path.exists(f'{D}/exam_ver.json'): data=json.load(open(f'{D}/exam_ver.json',encoding='utf-8'))
for f in sorted(glob.glob(f'{D}/out_*.json')): data.update(json.load(open(f,encoding='utf-8')))
json.dump(data,open(f'{D}/exam_ver.json','w',encoding='utf-8'),ensure_ascii=False,indent=1,sort_keys=True)
s=open(P,encoding='utf-8').read()
CSS='''<style id="exam-ver-css">
.essay-card[data-v="exam"] .detail-content,.essay-card[data-v="exam"] .quick-ans,.essay-card[data-v="exam"] .sk2,.essay-card[data-v="exam"] .lj-panel{display:none!important}
.exam-ver{display:none;margin-top:10px}.essay-card[data-v="exam"] .exam-ver{display:flex;flex-direction:column;gap:8px}
.exam-ver{--ev1:#2F6B4F;--ev2:#2F6690;--ev3:#9A6A14;--ev4:#A8432F;--evbg:#FFFFFF;--evink:#26302C;--evsub:#6B746F}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .exam-ver{--ev1:#7CC4A0;--ev2:#82B4DA;--ev3:#DDB15E;--ev4:#E39482;--evbg:#1E2422;--evink:#E4E0D6;--evsub:#A7AFA9}}
:root[data-theme="dark"] .exam-ver{--ev1:#7CC4A0;--ev2:#82B4DA;--ev3:#DDB15E;--ev4:#E39482;--evbg:#1E2422;--evink:#E4E0D6;--evsub:#A7AFA9}
.exam-ver .evb{background:color-mix(in srgb,var(--c) 11%,var(--evbg));border-radius:10px;padding:9px 13px;color:var(--evink)}
.exam-ver .evb.e1{--c:var(--ev1)}.exam-ver .evb.e2{--c:var(--ev2)}.exam-ver .evb.e3{--c:var(--ev3)}.exam-ver .evb.e4{--c:var(--ev4)}
.exam-ver b.evh{display:block;color:var(--c);font-size:.86rem;margin-bottom:2px}
'''+RV.CSS+'''
.exam-ver .evb p{font-size:.95rem}
.vt4 .ver-label{display:none}.vt4 .seg-wrap{width:100%;max-width:100%}.vt4 .ver-btn{flex:1;text-align:center;padding:5px 2px}
</style>'''
if 'id="exam-ver-css"' in s: s=re.sub(r'<style id="exam-ver-css">.*?</style>',CSS,s,flags=re.S)
else: s=s.replace('</head>',CSS+'\n</head>',1)
done=0
for cid,blocks in data.items():
    a=s.find(f'id="{cid}"'); 
    if a<0: print('找不到卡',cid); continue
    b=s.find('<div class="essay-card',a+5); b=len(s) if b<0 else b
    c=s[a:b]
    html='<div class="exam-ver">'+''.join(f'<div class="evb e{i+1}"><b class="evh">{h}</b>{RV.body(h,t,cid)}</div>' for i,(h,t) in enumerate(blocks))+'</div>'
    e0=c.find('<div class="exam-ver">')
    if e0>=0:
        d=0
        for m in re.finditer(r'<div\b[^>]*>|</div>',c[e0:]):
            d+=1 if m.group(0).startswith('<div') else -1
            if d==0: c=c[:e0]+c[e0+m.end():]; break
    if 'data-ver="exam"' not in c:
        qb=re.search(r'<button class="ver-btn" data-ver="quick"[^>]*>考場速寫</button>',c) or re.search(r'<button class="ver-btn active" data-ver="lj"[^>]*>[^<]*</button>',c)
        assert qb,cid
        btn='<button class="ver-btn" data-ver="exam" title="考場 25 分鐘寫得完的版本：意義→法條→涵攝→結論" onclick="setVer(this.closest(\'.essay-card\'),\'exam\')">考場版</button>'
        c=c[:qb.end()]+btn+c[qb.end():]
    c=re.sub(r'(data-ver="full"[^>]*>)完整版(</button>)',r'\1完整四段式\2',c)
    c=c.replace('<div class="ver-bar vt3">','<div class="ver-bar vt4">',1)
    d=c.find('<div class="detail-content'); assert d>0,cid
    c=c[:d]+html+c[d:]
    s=s[:a]+c+s[b:]; done+=1
open(P,'w',encoding='utf-8').write(s); print('注入',done,'張')
