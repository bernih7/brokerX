# -*- coding: utf-8 -*-
"""11-12 估價申論重審修正引擎。每筆修正依類型套到所有來源，任何一筆找不到就中止（不寫檔）。
X(cid,old,new)  考場版：exam/exam_ver.json＋out_*.json（同卡所有區塊）
L(cid,old,new)  推理版資料 lj_data.json（該卡所有字串欄）＋範文頁該卡 lj 面板（rich() 轉換後）
H(cid,old,new)  範文頁該卡區塊（完整四段式／考場速寫等直接 HTML）
A(cid,old,new)  以上全部都試，至少一處命中
可重跑：new 已存在且 old 不存在者視為已套用。"""
import json, glob, os, re, html, sys
R='/home/claude/brokerx'; V=R+'/tools/essay_val'; PAGE=R+'/不動產估價概要_申論題實戰範文.html'
E_=html.escape
def rich(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', E_(t, quote=False))
class Ctx:
    def __init__(s):
        s.page=open(PAGE,encoding='utf-8').read()
        s.exf=[V+'/exam/exam_ver.json']+sorted(glob.glob(V+'/exam/out_*.json'))
        s.ex={f:json.load(open(f,encoding='utf-8')) for f in s.exf}
        s.lj=json.load(open(V+'/lj_data.json',encoding='utf-8'))
        s.log=[]; s.err=[]
    def blk(s,cid):
        i=s.page.find(f'id="{cid}"'); assert i>0,cid
        j=s.page.find('<div class="essay-card',i+10); return i,(j if j>0 else s.page.find('</main>',i))
    def rep_html(s,cid,old,new):
        i,j=s.blk(cid); b=s.page[i:j]; n=b.count(old)
        if n: s.page=s.page[:i]+b.replace(old,new)+s.page[j:]
        return n, (new in b)
    def rep_ex(s,cid,old,new):
        n=0;done=False
        for f,d in s.ex.items():
            for blk in d.get(cid,[]):
                c=blk[1].count(old); n+=c
                if c: blk[1]=blk[1].replace(old,new)
                if new in blk[1]: done=True
        return n,done
    def rep_lj(s,cid,old,new):
        n=0;done=False
        card=[c for c in s.lj if c['k']==cid]
        if not card: return 0,False
        def w(x):
            nonlocal n,done
            if isinstance(x,str):
                c=x.count(old); n+=c
                y=x.replace(old,new) if c else x
                if new in y: done=True
                return y
            if isinstance(x,list): return [w(v) for v in x]
            if isinstance(x,dict): return {k:w(v) for k,v in x.items()}
            return x
        nc=w(card[0]); card[0].clear(); card[0].update(nc)
        hn,hd=s.rep_html(cid,rich(old),rich(new))
        return n+hn, done or hd
    def apply(s,kind,cid,old,new):
        if kind=='X': r=[s.rep_ex(cid,old,new)]
        elif kind=='L': r=[s.rep_lj(cid,old,new)]
        elif kind=='H': r=[s.rep_html(cid,old,new)]
        else: r=[s.rep_ex(cid,old,new),s.rep_lj(cid,old,new),s.rep_html(cid,old,new)]
        n=sum(x[0] for x in r); done=any(x[1] for x in r)
        if n==0 and not done: s.err.append((kind,cid,old[:60]))
        s.log.append((kind,cid,n,old[:30]))
    def save(s):
        if s.err:
            for e in s.err: print('找不到：',e)
            sys.exit('有修正未命中，未寫檔')
        open(PAGE,'w',encoding='utf-8').write(s.page)
        for f,d in s.ex.items(): json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=1,sort_keys=f.endswith('exam_ver.json'))
        json.dump(s.lj,open(V+'/lj_data.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('套用',len(s.log),'筆；命中處',sum(x[2] for x in s.log))
