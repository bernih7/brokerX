# 民法：考場速寫（data-v="1"）同一段 ①②③ 兩項以上 → 每項換行（內容不改）。可重跑（改自經紀法規 split_sx_lists.py）
# 只在「段落開頭或 　 ，；：、。（ 之後」且不在 <b>/<mark> 標籤內的圈號前切；§4⑤ 這類款號不切。
import re,os
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
f=os.path.join(R,'民法_備考指揮中心.html'); s=open(f,encoding='utf-8').read()
OKPRE='　 ，；：、。（→'
def cuts(p):
    out=[];depth=0;i=0;prev=''
    while i<len(p):
        if p[i]=='<':
            j=p.find('>',i); tag=p[i:j+1]
            if re.match(r'<(b|mark)\b',tag): depth+=1
            elif re.match(r'</(b|mark)>',tag): depth-=1
            i=j+1; continue
        ch=p[i]
        if '①'<=ch<='⑳' and depth==0 and (prev=='' or prev in OKPRE): out.append(i)
        prev=ch; i+=1
    return out
n=0
def para(m):
    global n
    p=m.group(1)
    if 'class="evli"' in p: return m.group(0)
    c=cuts(p)
    if len(c)<2: return m.group(0)
    n+=1; parts=[p[:c[0]]]+[p[a:b] for a,b in zip(c,c[1:]+[len(p)])]
    return '<p>'+parts[0]+''.join('<span class="evli">%s</span>'%x.rstrip('　 ') for x in parts[1:])+'</p>'
out=[];pos=0
for m in re.finditer(r'<div class="vp" data-v="1" hidden>',s):
    a=m.start(); b=s.find('<div class="kou">',a); c=s.find('<div class="vp"',a+10)
    e=min(x for x in (b,c) if x>0)
    out.append(s[pos:a]); out.append(re.sub(r'<p>(.*?)</p>',para,s[a:e],flags=re.S)); pos=e
out.append(s[pos:]); s=''.join(out)
CSS='.ebody .vp .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}'
if CSS not in s: s=s.replace('</style>',CSS+'\n</style>',1)
open(f,'w',encoding='utf-8').write(s); print('速寫分行段落',n)
