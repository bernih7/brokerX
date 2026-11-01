# 刷題 12 頁與 bxj-topic-q.js 接上 bxjHL（可重複執行）
import glob,re,os
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
O1="b.querySelector('.nt').textContent=(q.explains&&q.explains[L])||'';"
N1="var _x=(q.explains&&q.explains[L])||'';if(window.bxjHL)b.querySelector('.nt').innerHTML=bxjHL(q.year+'-'+q.qnum,i,_x);else b.querySelector('.nt').textContent=_x;"
O2="[].forEach.call(ex.querySelectorAll('.eh'),function(e,i){e.textContent=(q.explains&&q.explains[LB[i]])||''});"
N2="[].forEach.call(ex.querySelectorAll('.eh'),function(e,i){var _x=(q.explains&&q.explains[LB[i]])||'';if(window.bxjHL)e.innerHTML=bxjHL(q.year+'-'+q.qnum,i,_x);else e.textContent=_x});"
TAG='<script src="bxj-hl.js"></script>'
for f in sorted(glob.glob(f'{R}/經紀法規刷題練習_*.html')):
    s=open(f,encoding='utf-8').read(); c=0
    if O1 in s: s=s.replace(O1,N1); c+=1
    if O2 in s: s=s.replace(O2,N2); c+=1
    if TAG not in s:
        s=s.replace('<script src="bxj-use.js"></script>','<script src="bxj-use.js"></script>\n'+TAG,1); c+=1
    assert N1 in s and N2 in s and TAG in s, f
    open(f,'w',encoding='utf-8').write(s); print(os.path.basename(f),c)
f=f'{R}/bxj-topic-q.js'; s=open(f,encoding='utf-8').read()
O3="'</span><span>' + rich(t) + '</span></div>';"
N3="'</span><span>' + (window.bxjHL ? bxjHL(q.k, i, t) : rich(t)) + '</span></div>';"
if O3 in s: s=s.replace(O3,N3); open(f,'w',encoding='utf-8').write(s)
assert N3 in s; print('topic-q ok')
