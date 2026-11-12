# 補習班模擬卷申論卡（mk-1、mk-2、mk-4）加「曾老師版」分頁，比照 mk-3（v815）；資料取自來勝原卷頁 E[].tch
import re,json,html
F='土地法_申論題分類總覽.html'
s=open(F,encoding='utf-8').read()
def tchs(f):
    t=open(f,encoding='utf-8').read(); out=[]; dec=json.JSONDecoder()
    for m in re.finditer(r'"tch"\s*:\s*',t):
        v,_=dec.raw_decode(t[m.end():]); out.append(v)
    return out
tax=tchs('土地法_來勝模擬試題一_土地稅法.html'); law=tchs('土地法_來勝模擬試題一_土地法規.html')
MAP={'mk-4':(tax[1],'土地法_來勝模擬試題一_土地稅法.html','來勝(一)土地稅法','申論二'),
     'mk-1':(law[0],'土地法_來勝模擬試題一_土地法規.html','來勝(一)土地法規','申論一'),
     'mk-2':(law[1],'土地法_來勝模擬試題一_土地法規.html','來勝(一)土地法規','申論二')}
def render(parts,href,name,q):
    h='<div class="vp" data-v="5" hidden><p class="note">曾老師版：依曾榮耀老師公布的解答要點整理（非逐字抄錄），條文已對照現行法；原卷頁在〈<a href="'+href+'">'+name+'</a>〉'+q+'「曾老師版」。</p>'
    for k,(tt,tx) in enumerate(parts):
        ps=''.join('<p>'+html.escape(x)+'</p>' for x in tx.split('\n') if x.strip())
        h+='<details class="blk b%d" open><summary><h5>%s</h5></summary><div class="fdb">%s</div></details>'%(k+1,html.escape(tt),ps)
    return h+'</div>'
n=0
for cid,(parts,href,name,q) in MAP.items():
    i=s.find('id="%s"'%cid); j=s.find('<details class="es',i+10)
    c=s[i:j]
    if 'data-v="5"' in c: continue
    assert len(parts)==4,cid
    c2=c.replace('<button type="button" data-v="0">完整四段式</button>','<button type="button" data-v="0">完整四段式</button><button type="button" data-v="5">曾老師版</button>',1)
    k=c2.find('<div class="esrd">'); assert k>0
    c2=c2[:k]+render(parts,href,name,q)+c2[k:]
    c2=c2.replace('逐字條文撰寫，非補習班解答原文。','逐字條文撰寫；老師解答要點見「曾老師版」分頁。',1)
    s=s[:i]+c2+s[j:]; n+=1
open(F,'w',encoding='utf-8').write(s); print('加分頁',n)
