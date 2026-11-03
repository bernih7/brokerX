# 估價：考場速寫（.quick-ans 的 qa-blk）同一段 ①②③ 兩項以上 → 每項一行（內容不改）。可重跑。
# 切行規則同經紀法規／民法 split_sx_lists.py：只在段首或「　 ，；：、。（→」之後、不在 <b>/<sup>/<mark> 內切，§4⑤ 款號不切。
import re,os,sys
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.normpath(os.path.join(H,'..','..'))
sys.path.insert(0,os.path.join(H,'exam')); from render_ev import lst
F=os.path.join(R,'不動產估價概要_申論題實戰範文.html'); s=open(F,encoding='utf-8').read()
n=0
def blk(m):
    global n
    head,body,tail=m.group(1),m.group(2),m.group(3)
    segs=re.split(r'(<br\s*/?>)',body); out=[]
    for x in segs:
        if x.startswith('<br') or 'class="evli"' in x: out.append(x); continue
        y=lst(x)
        if y!=x: n+=1
        out.append(y)
    return head+''.join(out)+tail
out=[];pos=0
for m in re.finditer(r'<div class="quick-ans">',s):
    a=m.start(); b=s.find('<div class="detail-content',a); e=s.find('<div class="exam-ver"',a)
    end=min(x for x in (b,e) if x>0)
    out.append(s[pos:a])
    out.append(re.sub(r'(<div class="qa-label">.*?</div>)(.*?)(</div>)',blk,s[a:end],flags=re.S)); pos=end
out.append(s[pos:]); s=''.join(out)
CSS='.quick-ans .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}'
if CSS not in s: s=s.replace('</style>',CSS+'\n</style>',1)
open(F,'w',encoding='utf-8').write(s); print('速寫分行段落',n)
