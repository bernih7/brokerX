# 用法：python3 find.py 卡號 "片段" ...  → 列出該片段在 範文HTML（該卡區塊）、exam_ver/out_*.json、lj_data.json 的原始出現處
import sys,re,json,glob,os
R='/home/claude/brokerx'; V=R+'/tools/essay_val'
H=open(R+'/不動產估價概要_申論題實戰範文.html',encoding='utf-8').read()
def block(cid):
    i=H.find(f'id="{cid}"'); j=H.find('<div class="essay-card',i+10)
    return i,(j if j>0 else len(H))
cid=sys.argv[1]
for q in sys.argv[2:]:
    print('====',cid,q)
    i,j=block(cid); b=H[i:j]
    for m in re.finditer(re.escape(q),b): print('  HTML@',m.start(),'…'+b[max(0,m.start()-150):m.end()+150].replace('\n','⏎')+'…')
    for f in [V+'/exam/exam_ver.json']+sorted(glob.glob(V+'/exam/out_*.json')):
        d=json.load(open(f,encoding='utf-8'))
        for k,blk in enumerate(d.get(cid,[])):
            t=blk[1]
            for m in re.finditer(re.escape(q),t): print('  ',os.path.basename(f),k,blk[0],'…'+t[max(0,m.start()-120):m.end()+120]+'…')
    lj=json.load(open(V+'/lj_data.json',encoding='utf-8'))
    for c in lj:
        if c['k']==cid:
            s=json.dumps(c,ensure_ascii=False)
            for m in re.finditer(re.escape(q),s): print('  lj …'+s[max(0,m.start()-120):m.end()+120]+'…')
