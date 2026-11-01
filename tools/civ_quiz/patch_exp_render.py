# 讓民法各刷題頁改用 bxm-exp.js 顯示解析（一句結論＋重點句標色）。可重複執行。
import os,re,sys
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
TAG='<script src="bxm-exp.js"></script>'
err=[];done=[]
def patch(fn,pairs):
    p=os.path.join(R,fn); s=open(p,encoding='utf-8').read(); o=s
    if TAG not in s:
        i=s.index('</head>'); s=s[:i]+TAG+s[i:]
    for a,b in pairs:
        if b in s: continue
        if s.count(a)!=1: err.append((fn,a[:50],s.count(a))); continue
        s=s.replace(a,b)
    if s!=o: open(p,'w',encoding='utf-8').write(s); done.append(fn)
X="(q.core||[])[{i}],(q.key||[])[{i}],(q.tk||[])[{i}]"
# 刷題 A～E
for p in 'ABCDE':
    patch('民法刷題練習_%s篇.html'%p,[
      ("o.appendChild(mk('div','nt',NT[i]));",
       "{const nt=mk('div','nt');nt.innerHTML=window.bxmExp?bxmExp(NT[i],"+X.format(i='i')+"):NT[i];o.appendChild(nt);}"),
      ("d.textContent=ln;ex.appendChild(d);",
       "if(ix<4&&NT[ix]&&window.bxmExp&&q.core){d.innerHTML=bxmExp(ln,"+X.format(i='ix')+",ln.slice(0,ln.length-NT[ix].length))}else d.textContent=ln;ex.appendChild(d);")])
# 法條解析練習（樣板）
p=os.path.join(H,'tpl.html'); s=open(p,encoding='utf-8').read(); o=s
if TAG not in s: s=s.replace('</style></head>','</style>'+TAG+'</head>',1)
a="<span>'+hl(t,1)+"; b="<span>'+(window.bxmExp?bxmExp(t,"+X.format(i='i')+"):hl(t,1))+"
if b not in s:
    if s.count(a)!=1: err.append(('tpl',s.count(a)))
    else: s=s.replace(a,b)
if s!=o: open(p,'w',encoding='utf-8').write(s); done.append('tpl.html')
# 完整考題小卡、考題小卡
C="(c.core||[])[j],(c.key||[])[j],(c.tk||[])[j]"
for f in ['民法A_完整考題小卡','民法BC_完整考題小卡','民法D_完整考題小卡','民法E_完整考題小卡']:
    patch(f+'.html',[("<div>${exp}</div>`;","<div>${window.bxmExp?bxmExp(exp,"+C+"):exp}</div>`;")])
for f in ['民法A_考題小卡','民法BC_考題小卡','民法D_考題小卡','民法E_考題小卡']:
    patch(f+'.html',[("<div>${exp}</div>`;","<div>${window.bxmExp?bxmExp(exp,"+C+"):exp}</div>`;")])
# 25 題整卷模擬
patch('民法概要_25題模擬測驗.html',[("</div>${e}</div>`).join('')}","</div>${window.bxmExp?bxmExp(e,"+X.format(i='j')+"):e}</div>`).join('')}")])
# 模擬試題一／二／來勝
for f in ['民法_模擬試題一','民法_模擬試題二','民法_來勝模擬試題一']:
    patch(f+'.html',[('b.querySelector(".nt").textContent=cl2(q.notes[i]);',
                      'if(window.bxmExp)b.querySelector(".nt").innerHTML=bxmExp(cl2(q.notes[i]),'+X.format(i='i')+');else b.querySelector(".nt").textContent=cl2(q.notes[i]);')])
print('patched',len(done),done); print('err',err)
if err: sys.exit(1)
