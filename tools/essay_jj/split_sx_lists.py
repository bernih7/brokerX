# 考場速寫（data-v="1"）同一段 ①②③ 兩項以上 → 每項換行（內容不改）。可重跑
import re,os
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
f=os.path.join(R,'經紀法規_備考指揮中心.html'); s=open(f,encoding='utf-8').read()
CIR=re.compile(r'(?=[①-⑳])'); n=0
def para(m):
    global n
    p=m.group(1)
    if 'class="evli"' in p or len(re.findall('[①-⑳]',re.sub('<[^>]+>','',p)))<2: return m.group(0)
    parts=CIR.split(p); n+=1
    return '<p>'+parts[0]+''.join('<span class="evli">%s</span>'%x.strip('　 ') for x in parts[1:] if x)+'</p>'
out=[];pos=0
for m in re.finditer(r'<div class="vp" data-v="1" hidden>',s):
    a=m.start(); b=s.find('<div class="sk2">',a); c=s.find('<div class="vp"',a+10)
    e=min(x for x in (b,c) if x>0)
    out.append(s[pos:a]); out.append(re.sub(r'<p>(.*?)</p>',para,s[a:e],flags=re.S)); pos=e
out.append(s[pos:]); s=''.join(out)
CSS='.vp .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}'
if CSS not in s: s=s.replace('</style>',CSS+'\n</style>',1)
open(f,'w',encoding='utf-8').write(s); print('速寫分行段落',n)
