# 產生 bxl-essay-meta.js：土地法申論總覽的卡片清單（id、題名、類別、級別），給備考指揮中心「進度落後」算分母與列未讀。
# 申論總覽（gen_full.py）重產後要再跑一次。
import re,json,os,html
R=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
t=open(R+'/土地法_申論題分類總覽.html',encoding='utf-8').read()
out=[]
for m in re.finditer(r'<details class="es[^"]*" id="([^"]+)" data-k="([^"]*)"(?: data-mk="[^"]*")? data-pr="([^"]*)" data-lv="([^"]*)"[^>]*><summary>(.*?)</summary>',t,re.S):
    et=re.search(r'<b class="et">(.*?)</b>',m.group(5),re.S); ek=re.search(r'<span class="ek">(.*?)</span>',m.group(5),re.S)
    out.append({"i":m.group(1),"k":m.group(2),"p":int(m.group(3) or 9),"lv":m.group(4),"t":html.unescape(re.sub('<[^>]+>','',et.group(1))) if et else m.group(1),"e":html.unescape(re.sub('<[^>]+>','',ek.group(1))) if ek else ''})
assert len(out)==t.count('<details class="es'),(len(out),t.count('<details class="es'))
open(R+'/bxl-essay-meta.js','w',encoding='utf-8').write('/* 土地法申論卡清單（由 tools/land_tq/mk_essay_meta.py 自申論總覽產生，不要手改） */\nwindow.BXL_ESSAY='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
import collections; print(len(out), collections.Counter(x['k'] for x in out))
