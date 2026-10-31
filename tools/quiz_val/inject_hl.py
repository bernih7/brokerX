#!/usr/bin/env python3
"""把 bxv-hl.js 的標記接到估價刷題章節頁、解析版練習、考古題面板（可重跑：已接過的跳過）。"""
import re,glob
TAG='<script src="bxv-hl.js"></script>'
def sub1(s,o,n,f):
    if n in s: return s
    assert s.count(o)==1,(f,o[:50]); return s.replace(o,n)
n=0
for f in sorted(glob.glob('估價刷題練習_*.html')):
    if '113真題' in f: continue
    s=open(f,encoding='utf-8').read();s0=s
    if TAG not in s: s=s.replace('</head>',TAG+'\n</head>',1)
    if 'I2J1' in f:
        s=sub1(s,'<b>${\'ABCD\'[i]}.</b>${o}</button>','<b>${\'ABCD\'[i]}.</b>${ans&&window.bxvHL?bxvHL(it.id,i,o,\'opt\'):o}</button>',f)
        s=sub1(s,'</span><span>${ex}</span>','</span><span>${window.bxvHL?bxvHL(it.id,i,ex,\'exp\'):ex}</span>',f)
        s=sub1(s,'<div class="explain-title">▸ 逐選項解析</div>','<div class="explain-title">▸ 逐選項解析${(window.BXV_HL||{})[it.id]?bxvHLlegend:\'\'}</div>',f)
    else:
        s=sub1(s,'<b>${letters[i]}.</b>${opt}</button>','<b>${letters[i]}.</b>${a&&window.bxvHL?bxvHL(it.id,i,opt,\'opt\'):opt}</button>',f)
        s=sub1(s,"const expText = (it.explains && it.explains[i]) ? it.explains[i] : '';","const expText = (it.explains && it.explains[i]) ? (window.bxvHL?bxvHL(it.id,i,it.explains[i],'exp'):it.explains[i]) : '';",f)
        s=sub1(s,"<div class=\"explain-title\">📚 逐選項解析</div>';","<div class=\"explain-title\">📚 逐選項解析' + ((window.BXV_HL||{})[it.id]&&window.bxvHLlegend?bxvHLlegend:'') + '</div>';",f)
    if s!=s0: open(f,'w',encoding='utf-8').write(s);n+=1
# 解析版練習
f='估價解析版練習.html';s=open(f,encoding='utf-8').read();s0=s
s=sub1(s,'<script src="bxv-quiz-data.js"></script>','<script src="bxv-quiz-data.js"></script>'+TAG,f)
s=sub1(s,'if(i===q.correct)el.classList.add("correct");else if(i===idx)el.classList.add("wrong")})','if(i===q.correct)el.classList.add("correct");else if(i===idx)el.classList.add("wrong");if(window.bxvHL)el.innerHTML=\'<span class="letter">\'+"ABCD"[i]+"</span>"+bxvHL(q.id,i,q.opts[i],"opt")})',f)
s=sub1(s,'(q.exps[i]||"（本選項解析待補）")','(q.exps[i]?(window.bxvHL?bxvHL(q.id,i,q.exps[i],"exp"):q.exps[i]):"（本選項解析待補）")',f)
if s!=s0: open(f,'w',encoding='utf-8').write(s);n+=1
# 面板
f='bxv-topic-qa.js';s=open(f,encoding='utf-8').read();s0=s
s=sub1(s,"'</span><span>' + esc(o) + '</span>'","'</span><span>' + (picked && window.bxvHL ? bxvHL(q._id, i, esc(o), 'opt') : esc(o)) + '</span>'",f)
s=sub1(s,"'</span><span>' + rich(t) + '</span></div>'","'</span><span>' + (window.bxvHL ? bxvHL(q._id, i, rich(t), 'exp') : rich(t)) + '</span></div>'",f)
if s!=s0: open(f,'w',encoding='utf-8').write(s);n+=1
for f in glob.glob('*.html'):
    s=open(f,encoding='utf-8').read()
    if '<script src="bxv-topic-qa.js"' in s and TAG not in s:
        s=re.sub(r'(<script src="bxv-topic-qa\.js")',TAG+r'\1',s,1);open(f,'w',encoding='utf-8').write(s);n+=1;print('panel page',f)
print('改',n,'檔')
