import json,re
s=open('bxl-quiz-data.js').read();d=json.loads(s[s.index('{'):s.rindex('}')+1])
Q=d['q'];print(len(Q))
NEG=re.compile(r'錯誤|不正確|有誤|非|不得|不屬|不包括|不包含|不是|無須|不適用|不在|不能|不應|不可|不予|不需|不必|例外|無|不為|免|未')
def tail(st):
    m=None
    for mm in re.finditer(r'何者|何種|何項|何|哪|那',st):m=mm
    return st[m.start():] if m else st[-14:]
neg=0;amb=[]
for q in Q:
    t=tail(q['stem']);n=bool(NEG.search(t))
    neg+=n
    # check with exp of answer
    e=q['exp'][q['ans']]
    if n and re.search(r'正確[，。]|為正確',e) and not re.search(r'錯誤|不正確|非',e): amb.append((q['k'],t,e[:40]))
print('neg',neg);print(len(amb));[print(a) for a in amb[:40]]
