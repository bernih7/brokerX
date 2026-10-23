# 從指揮中心申論卡的條文卡抽出逐字條文庫（經紀法規）
import re,json,os,html
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..')
s=open(os.path.join(ROOT,'經紀法規_備考指揮中心.html'),encoding='utf-8').read()
def txt(h):
    h=re.sub(r'<br\s*/?>','\n',h); h=re.sub(r'</p>','\n',h)
    h=re.sub(r'<[^>]+>','',h); h=html.unescape(h)
    return re.sub(r'\n{3,}','\n\n',h).strip()
law={}
for m in re.finditer(r'<details class="bt"><summary><b class="bn">([^<]*)</b><span class="bti">([^<]*)</span>.*?<div class="btx">(.*?)</div></details>',s,re.S):
    n,t,b=m.group(1),m.group(2),m.group(3)
    key=t.split('｜')[0]+' '+n
    body=txt(b)
    verbatim = '要點整理' not in body
    if key in law:
        if len(body)>len(law[key]['text']): law[key]={'art':n,'title':t,'text':body,'verbatim':verbatim}
    else:
        law[key]={'art':n,'title':t,'text':body,'verbatim':verbatim}
json.dump(law,open(os.path.join(HERE,'law.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(law),'條；逐字',sum(1 for v in law.values() if v['verbatim']),'要點整理',sum(1 for v in law.values() if not v['verbatim']))
for k in list(law)[:5]: print(' ',k,'|',law[k]['text'][:40].replace('\n','/'))
