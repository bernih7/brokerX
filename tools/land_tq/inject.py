# 把「考古題面板」放進土地法整理頁（可重跑：已放過的會先清掉再放）
import re,json,os,html
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
d=open(R+'/bxl-quiz-data.js',encoding='utf-8').read()
bank={x['k'] for x in json.loads(d[d.find('{"q":'):d.rfind('};')+1].replace('{"q":','{"q":',1))['q']}
ID=re.compile(r'(?<![\d.])(\d{2,3})-(\d{1,2})(?![\d年%])')
def ids(txt):
    out=[]
    for y,n in ID.findall(txt):
        k=f'{int(y)}-{int(n)}'
        if k in bank and k not in out: out.append(k)
    return out
def strip(t): return html.unescape(re.sub(r'<[^>]+>',' ',t)).strip()
def clean(t): return re.sub(r'<div class="bxl-tq"[^>]*></div>','',t)
def panel(qs,title): return f'<div class="bxl-tq" data-qs="{",".join(qs)}" data-title="{html.escape(title,quote=True)}"></div>'
def addjs(t):
    t=re.sub(r'<script src="bxl-topic-q.js" defer></script>','',t)
    return re.sub(r'(<script src="bx-use.js"[^>]*></script>)',r'\1<script src="bxl-topic-q.js" defer></script>',t,count=1)
def run(name,fn):
    p=R+'/'+name; t=clean(open(p,encoding='utf-8').read()); t2,n=fn(t); t2=addjs(t2); open(p,'w',encoding='utf-8').write(t2); print(name,n,'個面板')
def penalty(t):
    n=0; out=[]; pos=0
    for m in re.finditer(r'<span class="exam">([^<]*)</span></div>',t):
        qs=ids(m.group(1)); 
        if not qs: continue
        tt=re.findall(r'<div class="tt">(.*?)</div>',t[:m.start()],re.S); title=strip(tt[-1]) if tt else '本條'
        out.append(t[pos:m.end()]+panel(qs,title)); pos=m.end(); n+=1
    out.append(t[pos:]); return ''.join(out),n
def fenshu(t):
    n=0; out=[]; pos=0
    for m in re.finditer(r'<div class="qr">(.*?)</div>',t,re.S):
        qs=ids(strip(m.group(1)))
        if not qs: continue
        nm=re.findall(r'<span class="nm">(.*?)</span>',t[:m.start()],re.S); title=strip(nm[-1]) if nm else '本考點'
        out.append(t[pos:m.end()]+panel(qs,title)); pos=m.end(); n+=1
    out.append(t[pos:]); return ''.join(out),n
def color(t):
    n=0; out=[]; pos=0
    for m in re.finditer(r'<p>(?:(?!</p>).)*?class="bulink" href="[^"]*#q=([\d,\-]+)"(?:(?!</p>).)*?</p>',t,re.S):
        qs=[k for k in m.group(1).split(',') if k in bank]
        if not qs: continue
        b=re.search(r'<b>(.*?)</b>',m.group(0)); title=strip(b.group(1)) if b else '本段'
        out.append(t[pos:m.end()]+panel(qs,title)); pos=m.end(); n+=1
    out.append(t[pos:]); return ''.join(out),n
def bottom(label):
    def f(t):
        body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S)
        qs=ids(strip(body))
        if not qs: return t,0
        box='<div style="max-width:980px;margin:0 auto;padding:0 16px 24px">'+panel(qs,label)+'</div>'
        i=t.find('<script src="bx-use.js"'); return t[:i]+box+t[i:],1
    return f
run('土地法_罰則總整理.html',penalty)
run('土地法_分數倍數數字分析.html',fenshu)
run('土地法_彩色重點速記.html',color)
run('土地法_稅制與取得方式比較表.html',bottom('本頁提到的考古題'))
run('土地法_繼承專區.html',bottom('本頁提到的考古題'))
