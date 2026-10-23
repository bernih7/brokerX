import re,sys,json,os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..')
s=open(os.path.join(ROOT,'經紀法規_備考指揮中心.html'),encoding='utf-8').read()
def blk(eid):
    i=s.find('<details id="%s"'%eid)
    j=s.find('<details id="es-',i+10)
    if j<0: j=len(s)
    return s[i:j]
for line in sys.argv[1:]:
    eid,pat=line.split('::',1)
    b=blk(eid); n=0
    for m in re.finditer(re.escape(pat),b):
        n+=1
        print(f'--- {eid} [{n}] ---')
        print(b[max(0,m.start()-200):m.start()+260].replace('\n',' '))
    if not n: print(f'!!! {eid} 找不到: {pat}')
    print()
