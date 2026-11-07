# 土地法題庫：拿掉 PDF 換行殘留的「中文 中文」空格（題幹、選項、解析）。可重跑。
import re,glob,sys
pat=re.compile(r'(?<=[一-鿿，、。）」]) (?=[一-鿿（「])')
KEEP=['土地法概要 考題小卡','土地徵收條例 區段徵收']
files=['bxl-quiz-data.js','土地法_考題小卡.html','土地法解析版練習.html']+sorted(glob.glob('LandLaw_*quiz*.html'))
tot=0
for f in files:
    s=open(f).read()
    for i,k in enumerate(KEEP):s=s.replace(k,'\0%d\0'%i)
    s,n=pat.subn('',s)
    for i,k in enumerate(KEEP):s=s.replace('\0%d\0'%i,k)
    if n:open(f,'w').write(s)
    print(f,n);tot+=n
print('total',tot)
