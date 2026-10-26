# 掃四個專區頁：每題連結（#q=）第一次出現在哪一節 → mem.json，給法條解析練習「相關整理頁」用
import re,os,json,html
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
PAGES=[('民法_繼承專區','繼承專區'),('民法_共有專區','共有專區'),('民法_物權變動與登記','物權變動與登記'),('民法_抵押權總整理','抵押權總整理')]
MEM={}
for f,title in PAGES:
    s=open(os.path.join(R,f+'.html'),encoding='utf-8').read()
    secs=[(m.start(),m.group(1)) for m in re.finditer(r'<details[^>]*\bid="(s\d+)"',s)]
    def sec_of(pos):
        cur=None
        for p,i in secs:
            if p<=pos: cur=i
        return cur
    names={}
    for p,i in secs:
        m=re.search(r'<summary[^>]*>(.*?)</summary>',s[p:p+3000],re.S)
        t=re.sub(r'<[^>]+>','',m.group(1)) if m else i; t=html.unescape(re.sub(r'\s+',' ',t)).strip()
        names[i]=re.split(r'\s{2,}|\d+ 個步驟|§',t)[0].strip()[:30]
    seen={}
    for m in re.finditer(r'#q=([0-9,\-]+)',s):
        sid=sec_of(m.start())
        if not sid: continue
        for k in m.group(1).split(','):
            if not k: continue
            # 優先非「考古題」節
            prev=seen.get(k)
            isq='考古' in names.get(sid,'')
            if prev is None or ('考古' in names.get(prev,'') and not isq): seen[k]=sid
    for k,sid in seen.items(): MEM.setdefault(k,[]).append([f,sid,names.get(sid,sid),title])
json.dump(MEM,open(os.path.join(H,'mem.json'),'w',encoding='utf-8'),ensure_ascii=False)
print('題數',len(MEM),'連結',sum(len(v) for v in MEM.values()))
