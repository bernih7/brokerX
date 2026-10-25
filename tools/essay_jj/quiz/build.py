# 產生《經紀法規_法條解析練習》。資料＝quiz_data.json（520題＋相關法條）＋chapters.json
import json,os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..','..')
tpl=open(os.path.join(HERE,'tpl.html'),encoding='utf-8').read()
data=open(os.path.join(HERE,'..','quiz_data.json'),encoding='utf-8').read()
chs=open(os.path.join(HERE,'..','chapters.json'),encoding='utf-8').read()
HUB='https://bernih7.github.io/brokerX/%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'
out=tpl.replace('%DATA%',data).replace('%CHS%',json.dumps(json.loads(chs),ensure_ascii=False,separators=(',',':'))).replace('%HUB%',HUB)
dst=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'經紀法規_法條解析練習.html')
open(dst,'w',encoding='utf-8').write(out)
print('已產生',os.path.basename(dst),len(out)//1024,'KB')
