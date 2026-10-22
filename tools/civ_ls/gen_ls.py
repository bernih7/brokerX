# 產生《民法_來勝模擬試題一.html》：以 民法_模擬試題一.html 為外殼（作答／申論／結果三分頁、可計時 90 分鐘）
import json, os, re, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..','..')
sys.path.insert(0,HERE)
from ls_q import Q
from ls_e import E
assert len(Q)==25 and [x['n'] for x in Q]==list(range(1,26))
KEY="CBADBCADBCADBCDABDBCADBCA"
assert ''.join(x['ans'] for x in Q)==KEY, ''.join(x['ans'] for x in Q)
src=open(os.path.join(ROOT,'民法_模擬試題一.html'),encoding='utf-8').read()
j=src.find('var D='); d,end=json.JSONDecoder().raw_decode(src[j+6:])
page=src[:j]+'var D='+json.dumps({"Q":Q,"E":E,"timer":True},ensure_ascii=False)+src[j+6+end:]
def rep(a,b,n=1):
    global page
    assert page.count(a)==n,(a[:60],page.count(a)); page=page.replace(a,b)
page=re.sub(r'<title>[^<]*</title>','<title>民法來勝115模擬試題（一）</title>',page,count=1)
page=re.sub(r'<h1>[^<]*</h1>','<h1>來勝115模擬試題（一）｜民法概要</h1>',page,count=1)
page=re.sub(r'<div class="sub">.*?</div></div></header>','<div class="sub">補習班模擬卷（出題：高律、嶺律；非考選部官方試題）：申論 2 題（每題 25 分）＋單選 25 題（每題 2 分），可計時 90 分鐘。題幹依題目卷逐字轉錄；選擇題答案＝老師公布解答，本站另行獨立作答 25 題全部一致，逐選項解析依現行條文撰寫。申論附「來勝老師版」要點與差異說明｜答錯可歸類 A 法條混淆／B 粗心／C 真的不熟</div></div></header>',page,count=1,flags=re.S)
rep('},ID="civ1";','},ID="civls1";')
rep('var ID="civ1";','var ID="civls1";')
rep('申論兩題共 50 分。建議先自己寫在紙上，再展開擬答（3 個版本）對照。','申論兩題共 50 分。先自己寫在紙上，再展開本站擬答；版本列最後一個是「來勝老師版」，並寫明與本站的差異。')
rep('展開擬答（3 個版本）','展開擬答（4 個版本，含來勝老師版）')
open(os.path.join(ROOT,'民法_來勝模擬試題一.html'),'w',encoding='utf-8').write(page)
print('ok',len(page))
