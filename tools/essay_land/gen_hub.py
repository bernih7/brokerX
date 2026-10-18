# 由申論頁產生指揮中心「申論」分頁（七主題列＋本週這題＋已讀）
import re, json, sys, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
ESS = os.path.join(ROOT, '土地法_申論題分類總覽.html')
HUB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '土地法_備考指揮中心.html')
OUT = sys.argv[2] if len(sys.argv) > 2 else HUB
URL = 'https://bernih7.github.io/brokerX/%E5%9C%9F%E5%9C%B0%E6%B3%95_%E7%94%B3%E8%AB%96%E9%A1%8C%E5%88%86%E9%A1%9E%E7%B8%BD%E8%A6%BD.html'
s = open(ESS, encoding='utf-8').read()
G = []
for m in re.finditer(r'<details class="grp" id="cat-(\w)" data-g="\w"><summary><span class="gl">\w</span><span class="gname">(.*?)</span><span class="gnum"><span><b>(\d+)</b>16年考</span><span><b>(\d+)</b>近5年</span><span><b class="p(.)">.</b>115預測</span></span>', s):
    g = m.group(1)
    st = m.end(); en = s.find('<details class="grp"', st)
    body = s[st:en if en > 0 else len(s)]
    cards = re.findall(r'<details class="es[^"]*" id="([^"]+)" data-k="(off|pred)" data-pr="(\d)" data-lv="([^"]*)"', body)
    titles = dict(re.findall(r'id="([^"]+)" data-k="[^"]+" data-pr="\d" data-lv="[^"]*"[^>]*><summary><span class="eh"><span class="rk"[^>]*>✓</span><b class="et">(.*?)</b>', body))
    eks = dict(re.findall(r'id="([^"]+)" data-k[^>]*>.*?<span class="ek">(.*?)</span>', body))
    G.append(dict(g=g, name=html.unescape(m.group(2)), tot=int(m.group(3)), r5=int(m.group(4)), p=m.group(5),
                  off=[c[0] for c in cards if c[1] == 'off'], pred=[c[0] for c in cards if c[1] == 'pred'],
                  cards=[dict(id=c[0], k=c[1], pr=int(c[2]), lv=c[3], t=html.unescape(re.sub('<[^>]+>', '', titles.get(c[0], ''))), ek=html.unescape(re.sub('<[^>]+>', '', eks.get(c[0], '')))) for c in cards]))
assert len(G) == 7, len(G)
SHORT = dict(A='都市計畫・公設保留地', B='土地徵收・區段徵收', C='市地重劃・空地・耕地', D='登記・優購・實價登錄', E='地價稅・土增稅', F='房屋稅・契稅・房地合一', G='地權總則・外國人・農地')
for x in G: x['name'] = SHORT[x['g']]
NOFF = sum(len(x['off']) for x in G); NPRE = sum(len(x['pred']) for x in G)
data = json.dumps([dict(g=x['g'], off=x['off'], pred=x['pred']) for x in G], ensure_ascii=False)
cards = json.dumps([c for x in G for c in x['cards']], ensure_ascii=False)
rows = ''.join(
    f'<a class="esr" href="{URL}#cat-{x["g"]}" target="_blank" rel="noopener" data-g="{x["g"]}">'
    f'<span class="esg">{x["g"]}</span><span class="esn"><b>{html.escape(x["name"])}</b><small class="esread">官方 {len(x["off"])}・預測 {len(x["pred"])}</small></span>'
    f'<span class="esv">{x["tot"]}</span><span class="esv">{x["r5"]}</span><span class="esv p{x["p"]}">{x["p"]}</span></a>'
    for x in G)
sec = f'''<section class="tab" id="t4">
   <div class="section-title">申論（官方 {NOFF} 題＋預測 {NPRE} 題）</div>
   <p class="hint">四段式：定義→法條→涵攝→結論。7 個主題依 16 年出題數排序；預測題（自擬或網路來源，不是考選部試題）放在各主題內。點主題直接開到該組。</p>
   <div class="esnow" id="esNow"></div>
   <div class="esprg"><div class="esbar"><i id="esBar"></i></div><small id="esPrg"></small></div>
   <div class="eshead"><span></span><span>主題（點開進入）</span><span>16年考</span><span>近5年</span><span>115預測</span></div>
   <div class="eslist">{rows}</div>
   <a class="tool-link" href="{URL}" target="_blank" rel="noopener"><div><div class="name">申論總覽（全部 {NOFF + NPRE} 題）</div><div class="tag">搜尋・熱度地圖・篩選官方／預測／未讀・每題必提重點與條文全文</div></div><span class="badge gold">開啟</span></a>
   <style>
   #t4 .esnow{{background:var(--pri);color:var(--on,#fff);border-radius:14px;padding:12px 14px;margin:6px 0 8px}}
   #t4 .esnow small{{opacity:.85;font-size:.78rem}}#t4 .esnow b{{display:block;font-family:"Noto Serif TC",serif;font-size:1rem;margin:3px 0 8px;line-height:1.45}}
   #t4 .esnow a{{display:inline-block;font-weight:700;font-size:.85rem;border-radius:99px;padding:5px 14px;background:var(--surface);color:var(--pri);text-decoration:none}}
   #t4 .esprg{{margin:0 2px 12px}}#t4 .esbar{{height:6px;background:var(--line);border-radius:9px;overflow:hidden}}#t4 .esbar i{{display:block;height:100%;width:0;background:var(--acc,#B8782E)}}
   #t4 .esprg small{{color:var(--sub);font-size:.78rem;font-variant-numeric:tabular-nums}}
   #t4 .eshead,#t4 .esr{{display:grid;grid-template-columns:1fr 3.4em 3.4em 3.8em;align-items:center;gap:4px}}
   #t4 .eshead{{font-size:.72rem;color:var(--sub);padding:0 12px 4px 46px}}#t4 .eshead span{{white-space:nowrap;text-align:center}}#t4 .eshead span:nth-child(2){{text-align:left}}
   #t4 .eslist{{display:flex;flex-direction:column;gap:8px}}
   #t4 .esr{{grid-template-columns:28px 1fr 2.9em 2.9em 3.6em;gap:4px 8px;text-decoration:none;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 12px}}
   #t4 .esg{{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:8px;background:var(--pri);color:var(--on,#fff);font-weight:700;font-size:.85rem}}
   #t4 .esn{{min-width:0}}#t4 .esn b{{display:block;font-family:"Noto Serif TC",serif;font-size:.92rem;color:var(--pri);line-height:1.35}}#t4 .esn small{{white-space:nowrap;font-size:.72rem;color:var(--sub);font-variant-numeric:tabular-nums}}
   #t4 .esv{{text-align:center;font-family:"Noto Serif TC",serif;font-weight:700;font-size:1.05rem;font-variant-numeric:tabular-nums}}#t4 .esv.p高{{color:var(--bad,#A8402B)}}#t4 .esv.p中{{color:var(--acc,#B8782E)}}
   #t4 .eshead{{grid-template-columns:28px 1fr 2.9em 2.9em 3.6em;gap:4px 8px;padding:0 12px 4px}}
   </style>
   <script>(function(){{var D={data},C={cards},U="{URL}",R={{}};try{{R=JSON.parse(localStorage.getItem("bx-es-read")||"{{}}")||{{}}}}catch(e){{}}
   var to=0,ro=0,tp=0,rp=0,ta=0,ra=0;D.forEach(function(g){{var o=g.off.filter(function(i){{return R[i]}}).length,p=g.pred.filter(function(i){{return R[i]}}).length;to+=g.off.length;ro+=o;tp+=g.pred.length;rp+=p;var el=document.querySelector('#t4 .esr[data-g="'+g.g+'"] .esread');if(el)el.textContent="已讀 官方 "+o+"/"+g.off.length+"・預測 "+p+"/"+g.pred.length}});
   C.forEach(function(c){{if(c.lv==="A"){{ta++;if(R[c.id])ra++}}}});
   document.getElementById("esBar").style.width=(ta?ra/ta*100:0)+"%";document.getElementById("esPrg").textContent="必考 "+ra+"／"+ta+"　官方 "+ro+"／"+to+"　預測 "+rp+"／"+tp;
   var ord=[["off",3],["off",2],["off",1],["pred",3],["pred",2],["pred",1]],f=null;for(var i=0;i<ord.length&&!f;i++)f=C.filter(function(c){{return c.k===ord[i][0]&&c.pr===ord[i][1]&&!R[c.id]}})[0];
   var n=document.getElementById("esNow");n.innerHTML=f?"<small>本週這題（每週一題，官方必考→高機率→參考→預測）</small><b>"+f.ek+"　"+f.t+"</b><a href=\\""+U+"#"+encodeURIComponent(f.id)+"\\" target=\\"_blank\\" rel=\\"noopener\\">去讀這題</a>":"<small>下一題</small><b>全部題目都讀過了</b>"}})();</script>
 </section>'''
h = open(HUB, encoding='utf-8').read()
a = h.index('<section class="tab" id="t4">'); b = h.index('</section>', a) + len('</section>')
h = h[:a] + sec + h[b:]
open(OUT, 'w', encoding='utf-8').write(h)
print('groups', [(x['g'], len(x['off']), len(x['pred'])) for x in G])
