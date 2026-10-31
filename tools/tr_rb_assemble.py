#!/usr/bin/env python3
"""技術規則專欄 B 版型組裝：把 tr/tN.html 片段換進 估價_技術規則專欄.html 的 details#tN > .tp-b，並插入 rb.css。
用法：python3 tools/tr_rb_assemble.py <片段資料夾> [--out 檔名]（預設覆寫原檔）"""
import re,sys,os
src='估價_技術規則專欄.html'
d=sys.argv[1];out=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else src
s=open(src,encoding='utf-8').read()
css=open(os.path.join(d,'rb.css'),encoding='utf-8').read()
s=re.sub(r'<style id="rb-css">[\s\S]*?</style>','',s)
s=s.replace('</head>','<style id="rb-css">\n'+css+'\n</style>\n</head>',1)
n=0
for i in range(1,9):
    f=os.path.join(d,f't{i}.html')
    if not os.path.exists(f): continue
    frag=open(f,encoding='utf-8').read().strip()
    a=s.index(f'<details class="tp" id="t{i}"')
    b=s.index('<div class="tp-b">',a)+len('<div class="tp-b">')
    e=s.index('</div></details>',b)
    s=s[:b]+frag+s[e:];n+=1
open(out,'w',encoding='utf-8').write(s);print('replaced',n,'->',out)
