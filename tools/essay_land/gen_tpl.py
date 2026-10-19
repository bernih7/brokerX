# 土地法申論「六型答題模板」頁產生器：題型骨架＋每型範例題（涵攝段首結論自動取自範文）
import re, json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
ESS = os.path.join(ROOT, '土地法_申論題分類總覽.html')
OUT = os.path.join(ROOT, '土地法申論題_六型答題模板.html')
URL = '土地法_申論題分類總覽.html'
s = open(ESS, encoding='utf-8').read()

def cards():
    res = {}
    for m in re.finditer(r'<details class="es[^"]*" id="([^"]+)" data-k="(off|pred)" data-pr="(\d)" data-lv="([^"]*)"', s):
        st = m.start(); en = s.find('<label class="done">', st)
        b = s[st:en]
        t = re.search(r'<b class="et">(.*?)</b>', b).group(1)
        ek = re.search(r'<span class="ek">(.*?)</span>', b).group(1)
        lv = re.search(r'<span class="lvp [^"]*">(.*?)</span>', b).group(1)
        oq = re.search(r'<div class="oq">(.*?)</div>', b, re.S).group(1)
        k3 = b.find('<details class="blk b3"'); k4 = b.find('<details class="blk b4"')
        ham = b[k3:k4]
        heads = [re.sub('<[^>]+>', '', h) for h in re.findall(r'<(?:summary|div class="sub1")><b>(（[一二三四五六七八九十]）[^<]*)</b>', ham)]
        concl = re.sub('<[^>]+>', '', re.search(r'<details class="blk b4"[^>]*><summary><h5>.*?</h5></summary><div class="fdb">(.*?)</div></details>', b, re.S).group(1)) if k4 > 0 else ''
        res[m.group(1)] = dict(id=m.group(1), k=m.group(2), t=t, ek=ek, lv=lv, oq=oq, heads=heads, concl=concl)
    return res
C = cards()
def ids(keys):
    out = []
    for k in keys:
        if k[0].isdigit(): out.append('q-' + k)
        elif k.startswith('X'): out.append('x-' + k[1:])
        else: out.append('pr-%02d' % int(k[1:]))
    return out

T = [
 dict(n='一', name='情境解說型', sub='經紀人向買方解說說明書', sig='題幹有「委託經紀人出售」「說明書之解說義務」「試就〇〇面向闡述」「應如何向丙解說」',
      ske=['定義：經紀人以不動產說明書向買方解說的義務（經紀條例§23、§24；居間人據實報告民法§567）', '法條：題目土地涉及的管制條文（都計§17、§50、§51、土徵§4、平均§59、重劃辦法§13…）', '涵攝：每一筆土地或每一個面向一段，段首寫「該地現況＋對買方的影響」，再寫法條要件、套到題目的 X 地／Y 地', '結論：分項列出說明書應載明的事項'],
      tip='題目通常有兩筆地或兩個面向（地用、地權），一定要分開寫，並把「對買方權益的影響」寫出來；只背條文不套到 X 地、Y 地會被扣分。',
      lose=['只寫法條，沒有套到題目的 X 地、Y 地', '漏寫但書（如都計§17Ⅱ「逾二年…或主要公共設施已興建完成」）', '說明義務的法源寫錯對象（經紀條例§23 是向相對人解說）'],
      off=['99-一', '112-一', '107-一', '114-一'], pred=['P01', 'P16', 'P19', 'P23']),
 dict(n='二', name='爭議判斷型', sub='「甲之主張有無理由／道理」', sig='題幹有「甲不服，主張…」「問甲之主張有無理由」「是否合理」',
      ske=['定義：先講清楚爭點所在的制度（稅基、查估方式、收回權…）', '法條：雙方主張各自的依據條文', '涵攝：①先寫結論「甲之主張有／無理由」；②法律依據；③套題目事實；④理由。主張型題目用「就情／就理／就法而言」三段論證，最後寫現行可用的救濟', '結論：一句話判斷＋理由，不要比條文說得更滿'],
      tip='結論要明確（有理由／無理由／不無道理），但「法無直接明文」不等於「於法無據」，用詞要準。',
      lose=['只描述制度，沒有回答「有無理由」', '結論說得太滿（例：把「依據薄弱」寫成「於法無據」）', '漏寫甲現行可用的救濟'],
      off=['99-二'], pred=['P34', 'X2']),
 dict(n='三', name='比較型', sub='兩種以上制度逐項比較', sig='題幹有「試比較」「有何差異」「何謂A？何謂B？」「區別」',
      ske=['定義：兩個（或三個）制度各給一句定義', '法條：各自的條號', '涵攝：每段一個比較基準（立法目的／要件／效力／機關／期限…），兩者都要寫到，段首直接寫出差異', '結論：一句話點出最核心的差異（通常是效力）'],
      tip='先在草稿列出比較基準再寫；效力欄（物權 vs 債權、相對無效 vs 停止新登記）最容易失分。',
      lose=['兩個制度分開各寫一大段，沒有逐項對照', '效力性質寫錯（§34-1Ⅳ 債權效力；§104、§107 物權效力）', '漏寫其中一方的要件'],
      off=['101-一', '103-一', '111-一'], pred=['P04', 'P06', 'P09', 'P11', 'P17', 'P31', 'X1']),
 dict(n='四', name='稅制結構型', sub='稅基・納稅義務人・稅率・課稅標的', sig='題幹有「稅基」「納稅義務人」「稅率為何」「課稅標的」「應負擔那些稅負」「如何計算」',
      ske=['定義：每個稅的性質（持有稅／交易稅）', '法條：各稅的稅基、義務人、稅率條文（土稅§3、§5、§15、§16、§31、房屋稅§4、§5、§11、契稅§2、§3、所得稅§4-4、§14-4…）', '涵攝：一個稅一段（或一個子問題一段），段首寫該稅的答案，再寫條文與例外（典權、信託、共有、代繳），題目有情境就套進去', '結論：用一句話把各稅並列'],
      tip='數字一個都不能錯（7公畝、10‰～55‰、6‰、2‰、20%～40%、1.2%～4.8%）；舊制（特種貨物及勞務稅、修法前房屋稅率）要標「考試年度官方答案」。',
      lose=['把納稅義務人寫成「所有權人」就結束，漏了典權人、管理人、受託人等例外', '免徵、不課徵、減徵、優惠稅率混用', '數字或級距寫錯'],
      off=['100-一', '102-二', '105-二', '108-二', '109-二', '111-二', '112-二', '113-二', '107-二'], pred=['P02', 'P22', 'P27', 'P29', 'P30', 'P32']),
 dict(n='五', name='要件效果型', sub='意義＋要件＋效果（含減免、限制、列舉）', sig='題幹有「何謂」「要件為何」「有何限制」「那些情形」「試列舉」「得予減徵之情形」',
      ske=['定義：制度意義一句話', '法條：主條文＋例外條文', '涵攝：一個要件或一個情形一段，段首寫要件本身，再寫條文用語、舉例（題目有事實就套），最後寫立法理由', '結論：要件或情形逐項收束'],
      tip='列舉型題目要寫滿條文所列款數（例：§14 十款、§17 七款、§19 八款），並注意修法後新增的款次。',
      lose=['列舉不完整', '把例外寫成原則（如「免徵＝永久不課」）', '條號、項款錯'],
      off=['103-二', '106-一', '110-一', '114-二', '104-一', '108-一', '109-一', '105-一', '110-二', '100-二', '102-一', '106-二'],
      pred=['P03', 'P07', 'P08', 'P10', 'P12', 'P13', 'P14', 'P15', 'P18', 'P20', 'P21', 'P24', 'P28', 'P33']),
 dict(n='六', name='程序型', sub='公告・通知・期限・異議・救濟', sig='題幹有「程序為何」「公告通知事項」「異議之時機與方式」「查定手續」「如何處理」',
      ske=['定義：程序的目的', '法條：每個程序階段的條文', '涵攝：依時間順序一個階段一段，段首寫「誰、在什麼時點、做什麼」，再寫期限（30日、15日、40日…）與不遵守的效果', '結論：把流程串成一句（公告→異議→調處→裁決）'],
      tip='時間軸不能顛倒；每個階段都要寫「期限」和「由誰處理」。',
      lose=['把兩個階段混在一起（如重劃計畫書公告與分配結果公告）', '期限寫錯', '漏寫救濟途徑'],
      off=['113-一', '101-二', '104-二'], pred=['P25', 'P26', 'X3']),
]
for t in T:
    t['ids_off'] = ids(t['off']); t['ids_pred'] = ids(t['pred'])
    for i in t['ids_off'] + t['ids_pred']:
        assert i in C, i
allo = [i for t in T for i in t['ids_off']]
assert len(allo) == 32 and len(set(allo)) == 32, len(allo)

def ex(i):
    c = C[i]
    heads = ''.join(f'<li>{html.escape(h)}</li>' for h in c['heads'])
    return (f'<details class="ex"><summary><span class="exk">{c["ek"]}</span><b>{c["t"]}</b><span class="exl">{c["lv"]}</span></summary>'
            f'<div class="exb"><div class="oq">{c["oq"]}</div><p class="exh">涵攝骨架（每段先寫結論）</p><ol class="hd">{heads}</ol>'
            f'<a class="go" href="{URL}#{i}">看完整範文 ›</a></div></details>')

body = ''
for t in T:
    no = len(t['ids_off']); npd = len(t['ids_pred'])
    body += (f'<details class="ty" id="t{t["n"]}" data-t="{t["n"]}"><summary><span class="tn">{t["n"]}</span><span class="tt"><b>{t["name"]}</b><small>{t["sub"]}</small></span>'
             f'<span class="tc"><b>{no}</b>官方</span><span class="tc"><b>{npd}</b>預測</span></summary><div class="tb">'
             f'<p class="sig"><b>判型訊號</b>{t["sig"]}</p>'
             f'<div class="ske"><p class="h">四段骨架</p><ol>' + ''.join(f'<li>{x}</li>' for x in t['ske']) + '</ol></div>'
             f'<p class="tip"><b>寫法重點</b>{t["tip"]}</p>'
             f'<div class="lose"><p class="h">常見失分</p><ul>' + ''.join(f'<li>{x}</li>' for x in t['lose']) + '</ul></div>'
             f'<p class="h">官方歷屆（{no} 題）</p>' + ''.join(ex(i) for i in t['ids_off']) +
             f'<p class="h">預測題（{npd} 題）</p>' + ''.join(ex(i) for i in t['ids_pred']) +
             f'<label class="got"><input type="checkbox" class="gk"> 我已掌握這一型</label></div></details>')
dist = ''.join(f'<div class="dr"><span>{t["n"]}　{t["name"]}</span><i style="--w:{len(t["ids_off"])/12*100:.0f}%"></i><b>{len(t["ids_off"])}</b></div>' for t in T)
head = s[:s.index('<style>')].replace('<title>土地法申論題分類總覽</title>', '<title>土地法申論六型模板</title>')
css = open(os.path.join(HERE, 'full.css'), encoding='utf-8').read()
css += '''
.intro{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px;font-size:14px}.intro ol{margin:6px 0 0;padding-left:1.3em}.intro li{margin:2px 0}
.prg2{display:flex;gap:14px;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}.prg2 b{color:var(--pri);font-size:16px}
.dist{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:10px 14px}.dist .h{margin:0 0 6px}
.dr{display:grid;grid-template-columns:9.5em 1fr 2em;gap:8px;align-items:center;font-size:13px;margin:3px 0}.dr i{display:block;height:10px;border-radius:5px;background:var(--pri);width:var(--w)}.dr b{text-align:right;font-variant-numeric:tabular-nums}
.ty{background:var(--card);border:1px solid var(--line);border-radius:14px}
.ty>summary{display:grid;grid-template-columns:30px 1fr auto auto;gap:4px 12px;align-items:center;padding:12px 14px}
.tn{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--pri);color:var(--onpri);font:700 15px "Noto Serif TC",serif}
.ty.got .tn{background:var(--green)}
.tt b{display:block;font:700 16px "Noto Serif TC",serif;color:var(--pri)}.tt small{color:var(--muted);font-size:12.5px}
.tc{text-align:center;font-size:11px;color:var(--muted);line-height:1.2}.tc b{display:block;font:700 17px "Noto Serif TC",serif;color:var(--ink)}
.ty[open]>summary{border-bottom:1px solid var(--line)}
.tb{padding:10px 14px 14px;display:flex;flex-direction:column;gap:8px;font-size:14px}
.h{font-size:13px;font-weight:700;color:var(--muted);margin:6px 0 2px}
.sig,.tip{margin:0;padding:8px 12px;border-radius:9px;border:1px solid var(--b2l);background:var(--b2s)}.tip{border-color:var(--b3l);background:var(--b3s)}.sig b,.tip b{display:block;font-size:12.5px;color:var(--b2)}.tip b{color:var(--b3)}
.ske{border:1px solid var(--b1l);background:var(--b1s);border-radius:9px;padding:6px 12px}.ske ol{margin:2px 0;padding-left:1.3em}.ske li{margin:3px 0}
.lose{border:1px solid var(--b4l);background:var(--b4s);border-radius:9px;padding:6px 12px}.lose ul{margin:2px 0;padding-left:1.2em}
.ex{border:1px solid var(--line);border-radius:10px;background:var(--bg)}.ex>summary{display:flex;gap:8px;align-items:baseline;padding:8px 10px;flex-wrap:wrap}
.exk{font-size:12px;color:var(--key);white-space:nowrap}.ex b{flex:1;min-width:10em;font-size:14px}.exl{font-size:11.5px;color:var(--muted)}
.exb{padding:0 10px 10px}.exh{font-size:12.5px;font-weight:700;color:var(--b3);margin:6px 0 2px}.hd{margin:0;padding-left:0;list-style:none}.hd li{margin:4px 0;padding:5px 9px;border:1px solid var(--b3l);background:var(--b3s);border-radius:7px;font-size:13.5px}
.go{display:inline-block;margin-top:8px;font-size:13px;font-weight:700;color:var(--pri)}
.got{display:flex;gap:8px;align-items:center;font-weight:700;color:var(--pri);margin-top:6px}.got input{width:18px;height:18px;accent-color:var(--green)}
'''
js = '''(function(){var K="bx-land-tpl",R={};try{R=JSON.parse(localStorage.getItem(K)||"{}")||{}}catch(e){}
var E={};try{E=JSON.parse(localStorage.getItem("bx-es-read")||"{}")||{}}catch(e){}
var T=[].slice.call(document.querySelectorAll(".ty"));
function upd(){var g=0;T.forEach(function(t){var on=!!R[t.dataset.t];t.classList.toggle("got",on);t.querySelector(".gk").checked=on;if(on)g++});document.getElementById("gotN").textContent=g;
var ex=[].slice.call(document.querySelectorAll(".ex .go")),r=ex.filter(function(a){return E[decodeURIComponent(a.getAttribute("href").split("#")[1])]}).length;document.getElementById("readN").textContent=r+"／"+ex.length}
T.forEach(function(t){t.querySelector(".gk").addEventListener("change",function(){if(this.checked)R[t.dataset.t]=1;else delete R[t.dataset.t];try{localStorage.setItem(K,JSON.stringify(R))}catch(e){}upd()})});
document.querySelectorAll("[data-all]").forEach(function(b){b.onclick=function(){var o=b.dataset.all==="open";T.forEach(function(t){t.open=o})}});
upd();var h=(location.hash||"").slice(1);if(h){var d=document.getElementById(h);if(d){d.open=true;d.scrollIntoView()}}})();
function ub(t){var b=document.getElementById("theme-btn");if(b)b.textContent=t==="dark"?"🌙":"☀️"}
function toggleTheme(){var h=document.documentElement,c=h.getAttribute("data-theme")||"light",n=c==="dark"?"light":"dark";h.setAttribute("data-theme",n);ub(n);try{localStorage.setItem("bx-theme",n)}catch(e){}}
ub(document.documentElement.getAttribute("data-theme")||"light");'''
FAB = s[s.index('<!--bxfab-->'):s.index('<!--/bxfab-->') + len('<!--/bxfab-->')]
page = (head + '<style>' + css + '</style></head><body><button id="theme-btn" onclick="toggleTheme()" title="切換深淺色" aria-label="切換深淺色">☀️</button><main>'
        '<header><h1>土地法｜申論六型答題模板</h1><p class="sub">看到題目先判型，骨架就出來了。官方 32 題全部歸型，每題附「涵攝骨架」（範文每段開頭的結論句），點進去看完整範文。</p></header>'
        '<div class="prg2"><span>已掌握 <b id="gotN">0</b>／6 型</span><span>範例已讀 <b id="readN">0</b></span></div>'
        '<div class="intro"><b>考場 60 秒 SOP</b><ol><li>先讀題目最後的問句，框出到底問幾個子問題。</li><li>用下方「判型訊號」決定是哪一型。</li><li>在題目空白處列（一）（二）（三）大綱，每個子問題一段，不能漏。</li><li>每段先寫結論，再寫法條、套題目事實、寫理由。</li><li>四段式不變：定義→法條→涵攝→結論。</li></ol></div>'
        f'<div class="dist"><p class="h">官方 32 題的題型分布</p>{dist}</div>'
        '<div class="ctl"><button class="mini" data-all="open">全部展開</button><button class="mini" data-all="close">全部收合</button></div>'
        + body +
        '<p class="note warn">題型是我依題目問法歸類的備考分類，不是考選部分類；範例的涵攝骨架自動取自申論頁現行範文。</p>'
        '</main><script>' + js + '</script>' + FAB + '\n<script src="bx-use.js"></script>\n</body></html>')
open(OUT, 'w', encoding='utf-8').write(page)
print('ok', len(page), [(t['name'], len(t['ids_off']), len(t['ids_pred'])) for t in T])
