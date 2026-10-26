# 產生《民法_法條解析練習》。資料＝quiz_data.json（mkdata.py 產生）＋chapters.json；樣板＝tpl.html
import json,os,sys
H=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(H,'..','..')
tpl=open(os.path.join(H,'tpl.html'),encoding='utf-8').read()
data=open(os.path.join(H,'quiz_data.json'),encoding='utf-8').read().replace('</','<\\/')
chs=json.load(open(os.path.join(H,'chapters.json'),encoding='utf-8'))
HUB='%E6%B0%91%E6%B3%95_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'
out=tpl.replace('%DATA%',data).replace('%CHS%',json.dumps(chs,ensure_ascii=False,separators=(',',':'))).replace('%HUB%',HUB)
dst=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'民法_法條解析練習.html')
open(dst,'w',encoding='utf-8').write(out)
print('已產生',os.path.basename(dst),len(out)//1024,'KB')
