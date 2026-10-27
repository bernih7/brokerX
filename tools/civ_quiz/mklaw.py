# 由 KB《民法_現行條文核實表》＋補遺 1017～1020（存於 law/）產生 law.json：{ "§N": {x:條文, s:來源等級} }
# 同條以較新的補遺為準；§1223 保留舊法（115 年考試適用），另加註新法。
import re,json,os
H=os.path.dirname(os.path.abspath(__file__)); L=os.path.join(H,'law')
def norm(k):return k.replace('之','-')
out={}
# 主表：### §N \n 條文（項以「  \n」分行）\n\n來源：
s=open(os.path.join(L,'民法_現行條文核實表.md'),encoding='utf-8').read()
for m in re.finditer(r'^### §(\d+(?:-\d+)?)\n(.*?)\n\n來源：',s,re.M|re.S):
    t='\n'.join(x.strip() for x in m.group(2).split('\n') if x.strip())
    out[m.group(1)]={'x':t,'s':'兩網站比對'}
SRC={'20261017':'官方全文（使用者提供）','20261018':'官方全文（使用者提供）','20261019':'法律人轉載','20261020':'法律人轉載','20261027':'官方全文（使用者提供）'}
for d in ['20261017','20261018','20261019','20261020','20261027']:
    s=open(os.path.join(L,'民法_現行條文核實表_補遺_%s.md'%d),encoding='utf-8').read()
    for m in re.finditer(r'^### (土地法 )?§(\d+(?:-\d+)?)([^\n]*)\n(.*?)(?=^#{2,3} |\Z)',s,re.M|re.S):
        if m.group(1): continue
        k=m.group(2); hd=m.group(3) or ''
        if '新法' in hd or hd.startswith('、'): continue
        lines=[]
        for x in m.group(4).split('\n'):
            x=x.strip()
            if not x or x.startswith(('（','來源','備註','用於','生效','-','>','取得時效中斷')): continue
            x=re.sub(r'（(注意|舊稿|第4項|「前條」)[^）]*）','',x).strip()
            if x: lines.append(x)
        if not lines: continue
        out[k]={'x':'\n'.join(lines),'s':SRC[d]}
if '1223' in out:
    out['1223']['n']='115.8.17 修正公布刪除兄弟姊妹特留分，自公布六個月後施行；115 年 11 月考試依上列修正前條文。'
json.dump(out,open(os.path.join(H,'law.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(out),'條')
