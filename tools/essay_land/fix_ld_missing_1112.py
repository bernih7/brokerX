# 補「看全文」段落缺少的首句（b.ld）：原 fmt_full2_1112 只在首個「。」<160 字時才加，60 段漏掉
import re,sys
F='土地法_申論題分類總覽.html'
s=open(F,encoding='utf-8').read()
PAT=re.compile(r'(<div class="full2">)(.*?)(</div></details>)',re.S)
def cut(t):
    # 切在第一個「。／：／；」之後（純文字第 20 字以後、不在「」或 mark 內）；都沒有再找「，」(30 字後)
    tag=False;dm=0;q=0;si=0;i=0;comma=None
    while i<len(t):
        c=t[i]
        if c=='<':
            j=t.find('>',i); tg=t[i:j+1]
            if tg.startswith('<mark'): dm+=1
            elif tg.startswith('</mark'): dm-=1
            i=j+1; continue
        if c=='「': q+=1
        elif c=='」': q=max(0,q-1)
        if dm==0 and q==0:
            if c in '。：；' and si>=20: return i
            if c=='，' and si>=30 and comma is None: comma=i
        si+=1;i+=1
    return comma
n=0
def rep(m):
    global n
    a,body,c=m.groups()
    if 'class="ld"' in body: return m.group(0)
    pm=re.match(r'(<p[^>]*>)(.*?)(</p>)',body,re.S)
    if not pm: return m.group(0)
    t=pm.group(2); k=cut(t)
    if k is None: return m.group(0)
    head=t[:k+1]; rest=t[k+1:]
    rest=re.sub(r'^\s*<br\s*/?>','',rest)
    newp=pm.group(1)+'<b class="ld">'+head+'</b>'+rest+pm.group(3)
    n+=1
    return a+newp+body[pm.end():]+c
s=PAT.sub(rep,s)
open(F,'w',encoding='utf-8').write(s)
print('補 ld',n)
