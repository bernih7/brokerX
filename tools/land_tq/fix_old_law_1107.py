# 105-34 依現行法改答案 A→B（土地法第34條之1執行要點第3點第2項，112.8.22修正、113.1.1生效）；五處同步。可重跑。
import json,re,os,subprocess
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S='甲、乙、丙、丁、戊、己等六人分別共有A地，其中的甲、乙、丙、丁將A地全部出賣給戊'
NEW=1
EX=[
 '依現行規定錯誤。土地法第34條之1執行要點第3點第2項（112.8.22修正、113.1.1生效）：「有償讓與之處分行為，共有人除依本法條規定優先購買外，不得為受讓人」。戊是共有人，甲乙丙丁不得依§34-1把A地全部有償處分給戊。⚠️ 105年考選部答案為本項（A），因規定修正，本站改依現行法。',
 '現行法答案。執行要點第3點第2項明定「共有人除依本法條規定優先購買外，不得為受讓人」，113-17官方答案即採此說。⚠️ 105年考選部答案為（A）；兩題答案不同是因規定修正，以現行規定為準。',
 '理由錯誤。現行規定是直接以「共有人不得為受讓人」排除，不是以「利害衝突、顯失公平」個案判斷（105年官方答案亦不採此項）。',
 '錯誤。部分共有人依§34-1出賣共有物「全部」時，他共有人仍得以出賣之同一條件共同或單獨優先購買（112-18 官方視為正確敘述），己不因「不是出賣應有部分」而喪失先買權。']
HL=[["不得為受讓人","105年考選部答案為本項"],["現行法答案","113-17官方答案"],["不是以「利害衝突、顯失公平」個案判斷"],["同一條件共同或單獨優先購買"]]
def rec(c):
    i=c.find(S);assert i>0;j=c.rfind('{',0,i)
    while True:
        try:o,e=json.JSONDecoder().raw_decode(c[j:]);return o,j,j+e
        except Exception:j=c.rfind('{',0,j)
def put(c,o,a,b,sep): return c[:a]+json.dumps(o,ensure_ascii=False,separators=sep)+c[b:]
def sepof(s): return (', ',': ') if '", "' in s[:3000] else (',',':')
# 1 題庫 A3A4A5
f=R+'/LandLaw_A3A4A5_quiz.html';c=open(f,encoding='utf-8').read();o,a,b=rec(c)
o['ans']=NEW;o['exps']=[('✓ ' if i==NEW else '❌ ')+x for i,x in enumerate(EX)]
c=put(c,o,a,b,sepof(c[a:b]));open(f,'w',encoding='utf-8').write(c)
# 2 考題小卡
f=R+'/土地法_考題小卡.html';c=open(f,encoding='utf-8').read();o,a,b=rec(c)
o['correct']=NEW;o['exps']=EX[:];c=put(c,o,a,b,sepof(c[a:b]));open(f,'w',encoding='utf-8').write(c)
# 3 解析版練習（QUIZ_DATA answer＋EXPS）
f=R+'/土地法解析版練習.html';c=open(f,encoding='utf-8').read();o,a,b=rec(c)
o['answer']=NEW;c=put(c,o,a,b,sepof(c[a:b]))
k=c.find('const EXPS = ')+len('const EXPS = ');E,e=json.JSONDecoder().raw_decode(c[k:]);E['105-34']=EX[:]
c=c[:k]+json.dumps(E,ensure_ascii=False,separators=sepof(c[k:k+e]))+c[k+e:];open(f,'w',encoding='utf-8').write(c)
# 4 黃底關鍵詞
f=R+'/bxl-hl.js';c=open(f,encoding='utf-8').read()
c=re.sub(r'"105-34":\[\[.*?\]\](?=,"|\})',lambda m:'"105-34":'+json.dumps(HL,ensure_ascii=False,separators=(',',':')),c,count=1);open(f,'w',encoding='utf-8').write(c)
for i,h in enumerate(HL):
    for w in h: assert w in EX[i],(i,w)
# 5 共用題庫
subprocess.run(['python3',R+'/tools/land_tq/mk_data.py'],check=True)
print('ok')
