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
        srcs=a if isinstance(a,tuple) else (a,)
        hit=[x for x in sorted(srcs,key=len,reverse=True) if s.count(x)==1]  # 長的優先：舊版字串可能包含更舊版的片段
        if not hit: err.append((fn,srcs[0][:50],[s.count(x) for x in srcs])); continue
        s=s.replace(hit[0],b)
    if s!=o: open(p,'w',encoding='utf-8').write(s); done.append(fn)
X="(q.core||[])[{i}],(q.key||[])[{i}],(q.tk||[])[{i}]"
# v643：結論列改「字母＋〔本題答案〕＋對在／錯在＋結論」（opt 參數），拿掉 ✓／✗；顏色：綠＝答案、黃紅＝敘述對錯
OPT_I="'',{{L:{L},ans:{A}}}"
# 刷題 A～E
for p in 'ABCDE':
    patch('民法刷題練習_%s篇.html'%p,[
      ("o.appendChild(mk('div','nt',NT[i]));",
       "{const nt=mk('div','nt');nt.innerHTML=window.bxmExp?bxmExp(NT[i],"+X.format(i='i')+"):NT[i];o.appendChild(nt);}"),
      (("d.textContent=ln;ex.appendChild(d);",
        "if(ix<4&&NT[ix]&&window.bxmExp&&q.core){d.classList.remove('cl','wl');d.innerHTML=bxmExp(ln,"+X.format(i='ix')+",ln.slice(0,ln.length-NT[ix].length))}else d.textContent=ln;ex.appendChild(d);"),
       "if(ix<4&&NT[ix]&&window.bxmExp&&q.core){const an=isOK(q,LET[ix]);d.classList.remove('cl','wl');d.classList.add('xrow');if(an)d.classList.add('xrow-ans');d.innerHTML=bxmExp(ln,"+X.format(i='ix')+",ln.slice(0,ln.length-NT[ix].length),{L:LET[ix],ans:an})}else d.textContent=ln;ex.appendChild(d);"),
      ("else if(ln[0]==='★'||ln[0]==='※')d.classList.add('nl');","else if(ln[0]==='★'||ln[0]==='※')d.classList.add('nl','xstar');")])
# 法條解析練習（樣板）
p=os.path.join(H,'tpl.html'); s=open(p,encoding='utf-8').read(); o=s
if TAG not in s: s=s.replace('</style></head>','</style>'+TAG+'</head>',1)
srcs=["<span>'+hl(t,1)+","<span>'+(window.bxmExp?bxmExp(t,"+X.format(i='i')+"):hl(t,1))+"]
b="<span>'+(window.bxmExp?bxmExp(t,"+X.format(i='i')+",'',{ans:isOk}):hl(t,1))+"
if b not in s:
    hit=[a for a in srcs if s.count(a)==1]
    if not hit: err.append(('tpl',[s.count(a) for a in srcs]))
    else: s=s.replace(hit[0],b)
if s!=o: open(p,'w',encoding='utf-8').write(s); done.append('tpl.html')
# 完整考題小卡、考題小卡
C="(c.core||[])[j],(c.key||[])[j],(c.tk||[])[j]"
CARD_OLD=("<div class=\"exp-head\">${letters[j]}. ${mark}</div><div>${exp}</div>`;",
          "<div class=\"exp-head\">${letters[j]}. ${mark}</div><div>${window.bxmExp?bxmExp(exp,"+C+"):exp}</div>`;")
CARD_NEW="${window.bxmExp?'<div>'+bxmExp(exp,"+C+","+OPT_I.format(L='letters[j]',A='j===c.correct')+")+'</div>':'<div class=\"exp-head\">'+letters[j]+'. '+mark+'</div><div>'+exp+'</div>'}`;"
# E 完整考題小卡寫法不同（L 而非 letters、mark 內嵌）
patch('民法E_完整考題小卡.html',[(("<div class=\"exp-head\">${L[j]}. ${j===c.correct?'✓ 正解':'✗'}</div><div>${window.bxmExp?bxmExp(exp,"+C+"):exp}</div>`;",),
  "${window.bxmExp?'<div>'+bxmExp(exp,"+C+","+OPT_I.format(L='L[j]',A='j===c.correct')+")+'</div>':`<div class=\"exp-head\">${L[j]}. ${j===c.correct?'✓ 正解':'✗'}</div><div>${exp}</div>`}`;")])
for f in ['民法A_完整考題小卡','民法BC_完整考題小卡','民法D_完整考題小卡','民法A_考題小卡','民法BC_考題小卡','民法D_考題小卡','民法E_考題小卡']:
    patch(f+'.html',[(CARD_OLD,CARD_NEW)])
# 25 題整卷模擬
patch('民法概要_25題模擬測驗.html',[(("<div class=\"eh\">${L[j]}. ${q.ok.includes(j)?'✓ 正解':'✗'}</div>${e}</div>`).join('')}",
                                    "<div class=\"eh\">${L[j]}. ${q.ok.includes(j)?'✓ 正解':'✗'}</div>${window.bxmExp?bxmExp(e,"+X.format(i='j')+"):e}</div>`).join('')}"),
                                   "${window.bxmExp?bxmExp(e,"+X.format(i='j')+","+OPT_I.format(L='L[j]',A='q.ok.includes(j)')+"):`<div class=\"eh\">${L[j]}. ${q.ok.includes(j)?'✓ 正解':'✗'}</div>`+e}</div>`).join('')}")])
# 模擬試題一／二／來勝
for f in ['民法_模擬試題一','民法_模擬試題二','民法_來勝模擬試題一']:
    patch(f+'.html',[(('b.querySelector(".nt").textContent=cl2(q.notes[i]);',
                       'if(window.bxmExp)b.querySelector(".nt").innerHTML=bxmExp(cl2(q.notes[i]),'+X.format(i='i')+');else b.querySelector(".nt").textContent=cl2(q.notes[i]);'),
                      # v643：✅／❌ 是「是不是答案」，和對在／錯在打架 → 拿掉符號、答案加〔本題答案〕
                      'if(window.bxmExp){var t2=cl2(q.notes[i]),m2=t2.match(/^[✓✗]\\s*/);b.querySelector(".nt").innerHTML=bxmExp(t2,'+X.format(i='i')+',m2?m2[0]:"",{ans:/^✓/.test(t2)})}else b.querySelector(".nt").textContent=cl2(q.notes[i]);')])
print('patched',len(done),done); print('err',err)
if err: sys.exit(1)
