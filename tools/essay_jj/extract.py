# 從經紀法規指揮中心抽出 65 題申論卡內容，供邏輯拆解撰寫與複核使用
import re, json, os, html
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..')
s=open(os.path.join(ROOT,'經紀法規_備考指揮中心.html'),encoding='utf-8').read()
def txt(h):
    h=re.sub(r'<br\s*/?>','\n',h); h=re.sub(r'</p>','\n',h); h=re.sub(r'</div>','\n',h)
    h=re.sub(r'<[^>]+>','',h); h=html.unescape(h)
    return re.sub(r'\n{3,}','\n\n',re.sub(r'[ \t]+',' ',h)).strip()
out=[]
for m in re.finditer(r'<details id="(es-[^"]+)" class="essay-detail([^"]*)">(.*?)(?=<details id="es-|<div class="group-label|$)',s,re.S):
    eid,cls,body=m.group(1),m.group(2),m.group(3)
    num=re.search(r'<span class="essay-num">([^<]*)</span>',body).group(1)
    ti=re.search(r'<span class="es-t">([^<]*)</span>',body).group(1)
    q=re.search(r'<p class="essay-question">(.*?)</p>',body,re.S)
    kcs=re.findall(r'<span class="kc">([^<]*)</span>',body)
    lv=re.search(r'<span class="es-lv[^"]*">([^<]*)</span>',body)
    def vp(v):
        a=body.find('<div class="vp" data-v="%d"'%v)
        if a<0: return ''
        b=body.find('<div class="vp" data-v="',a+5)
        return body[a: b if b>0 else len(body)]
    full,quick,keys=vp(0),vp(1),vp(2)
    cites=re.findall(r'<b class="bn">([^<]*)</b><span class="bti">([^<]*)</span>',full)
    out.append(dict(eid=eid,num=num,title=ti,level=(lv.group(1) if lv else ''),kw=kcs,
        question=txt(q.group(1)) if q else '', full=txt(full), quick=txt(quick), keys=txt(keys),
        cites=[{'n':a,'t':b} for a,b in cites]))
json.dump(out,open(os.path.join(HERE,'essays.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
for o in out[:2]: print(o['eid'],o['num'],o['title'][:30],len(o['full']),len(o['quick']),len(o['keys']))
