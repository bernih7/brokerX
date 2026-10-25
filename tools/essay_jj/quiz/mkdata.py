# 由刷題 12 頁（解析）＋互動練習（章節／一律給分）＋條文庫＋爭議題表，產生 quiz_data.json
import re,json,glob,collections,os
HERE=os.path.dirname(os.path.abspath(__file__)); J=os.path.join(HERE,'..'); ROOT=os.path.join(J,'..','..')
def grab(path,name):
    s=open(path,encoding='utf-8').read()
    m=re.search(r'(?:const|let|var)\s+%s\s*=\s*'%name,s); i=s.index('[',m.end()); d=0
    for j in range(i,len(s)):
        if s[j]=='[': d+=1
        elif s[j]==']':
            d-=1
            if d==0: return json.loads(s[i:j+1])
def grabobj(path,name):
    s=open(path,encoding='utf-8').read()
    m=re.search(r'(?:const|let|var)\s+%s\s*=\s*'%name,s); i=s.index('{',m.end()); d=0
    for j in range(i,len(s)):
        if s[j]=='{': d+=1
        elif s[j]=='}':
            d-=1
            if d==0: return json.loads(s[i:j+1])
IAp=os.path.join(ROOT,'經紀法規概要_互動練習.html')
IA={(q['year'],q['qnum']):q for q in grab(IAp,'ALL_QUESTIONS')}
MEM=grabobj(IAp,'MEM')
EX={}
for f in sorted(glob.glob(os.path.join(ROOT,'經紀法規刷題練習_*.html'))):
    for q in grab(f,'QUESTIONS'): EX[(q['year'],q['qnum'])]=q
full=json.load(open(os.path.join(J,'law','lawfull.json'),encoding='utf-8'))
DIS={d['k']:d for d in json.load(open(os.path.join(J,'disputed.json'),encoding='utf-8'))['items']}
CN={'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
def cn(t):
    if t.isdigit(): return int(t)
    tot=cur=0
    for c in t:
        if c=='百': tot+=(cur or 1)*100;cur=0
        elif c=='十': cur=(cur or 1)*10;tot+=cur;cur=0
        elif c in CN: cur=CN[c]
        else: return 0
    return tot+cur
# C 篇（說明書）引的條號多半是經紀業條例§22～§24；D 篇（定型化契約）多半是消保法
DEF={'A':'經紀業條例','C':'經紀業條例','D':'消保法','E':'公寓大廈',
     'F':'公寓大廈','G':'公平法','H':'消保法'}
# 長名優先，避免「公寓大廈管理條例施行細則」被「公寓大廈」先吃掉
NAMEPAT=[(r'公寓大廈管理服務人管理辦法|管理服務人管理辦法','公寓大廈管理服務人辦法'),
         (r'公寓大廈管理條例施行細則','公寓大廈施行細則'),
         (r'消費者保護法施行細則|消保法施行細則','消保法施行細則'),
         (r'不動產經紀業管理條例施行細則|經紀業管理條例施行細則|本細則|施行細則','施行細則'),
         (r'公寓大廈','公寓大廈'),(r'消費者保護法|消保法','消保法'),
         (r'公平交易法|公平法','公平法'),(r'多層次傳銷管理法','多層次傳銷管理法'),
         (r'不動產經紀業管理條例|經紀業管理條例|經紀條例','經紀業條例'),
         (r'本條例|本法|管理條例','@DEF'),  # 「本條例／本法」指該題所屬法規，不是固定某一部
         (r'民法','民法'),(r'土地法','土地法')]
ART=re.compile(r'(第\s*[0-9一二三四五六七八九十百]+\s*條(?:\s*之\s*[0-9一二三四五六七八九十]+)?)|(§\s*\d+(?:\s*[-之]\s*\d+)?)')
def arts_of(txt,default):
    cur=default; out=[]
    toks=[(m.start(),0,p) for pat,p in NAMEPAT for m in re.finditer(pat,txt)]
    toks+=[(m.start(),1,m.group(0)) for m in ART.finditer(txt)]
    for pos,kind,v in sorted(toks):
        if kind==0: cur=(default if v=='@DEF' else v)
        else:
            mm=re.search(r'第\s*([0-9一二三四五六七八九十百]+)\s*條(?:\s*之\s*([0-9一二三四五六七八九十]+))?',v)
            if mm: a='§%d'%cn(mm.group(1))+('之%d'%cn(mm.group(2)) if mm.group(2) else '')
            else:
                mm=re.search(r'§\s*(\d+)(?:\s*[-之]\s*(\d+))?',v); a='§%s'%mm.group(1)+('之%s'%mm.group(2) if mm.group(2) else '')
            out.append(cur+' '+a)
    return out
OUT=[];used=set();miss=collections.Counter()
for (y,n),a in sorted(IA.items()):
    b=EX[(y,n)];k='%d-%d'%(y,n);ch=a['chapter']
    txt=a['stem']+'｜'+'｜'.join(a['options'])+'｜'+'｜'.join(b['explains'].get(c,'') for c in 'ABCD')+'｜'+str(b.get('ref',''))
    keys=[]
    for key in arts_of(txt,DEF.get(ch[0],'經紀業條例')):
        if key in full:
            if key not in keys: keys.append(key)
        elif not key.startswith(('民法','土地法')): miss[key]+=1
    keys=keys[:5]; used.update(keys)
    o={'k':k,'y':y,'n':n,'ch':ch,'stem':a['stem'],'opt':a['options'],
       'ans':b['answer'],'exp':[b['explains'].get(c,'') for c in 'ABCD'],'ref':b.get('ref',''),'law':keys}
    if a.get('special'): o['sp']=a['special']
    d=DIS.get(k)
    if d: o['dis']={'kind':d['kind'],'acc':d['accept'],'why':d['why']}
    if k in MEM: o['mem']=MEM[k]
    OUT.append(o)
law={k:{'t':full[k].get('title',''),'x':full[k]['text'],'v':full[k]['verbatim']} for k in used}
dst=os.path.join(J,'quiz_data.json')
json.dump({'q':OUT,'law':law},open(dst,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('題數 %d｜有相關法條 %d（%.0f%%）｜用到條文 %d 條｜%d KB'%(
    len(OUT),sum(1 for q in OUT if q['law']),sum(1 for q in OUT if q['law'])*100/len(OUT),len(law),os.path.getsize(dst)//1024))
print('仍對不到的條號（前 10）:',miss.most_common(10))
