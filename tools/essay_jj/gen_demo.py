# 產生「邏輯拆解」demo 頁（獨立檔，給使用者確認版面與寫法）
import json, os, sys, re, html
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from lj_render import render, CSS, JS
ROOT=os.path.join(HERE,'..','..')
ES={x['eid']:x for x in json.load(open(os.path.join(HERE,'essays.json'),encoding='utf-8'))}
D=json.load(open(os.path.join(HERE,'lj_demo.json'),encoding='utf-8'))
E=html.escape
# 從指揮中心抓原卡的 速寫 / 得分關鍵，示範「考場速寫（併得分關鍵・失分點）」
hub=open(os.path.join(ROOT,'經紀法規_備考指揮中心.html'),encoding='utf-8').read()
def vp(eid,v):
    i=hub.find('<details id="%s"'%eid); b=hub.find('<div class="vp" data-v="%d"'%v,i)
    e=hub.find('<div class="vp" data-v="',b+5)
    if e<0: e=hub.find('</details>',b)
    seg=hub[b:e]
    seg=re.sub(r'^<div class="vp" data-v="\d"[^>]*>','',seg)
    return seg[:seg.rindex('</div>')] if '</div>' in seg else seg
TOK='''--bg:#F5F1E6;--surface:#FFFEFA;--ink:#25302C;--sub:#5F6B63;--line:#DAD6C3;--pri:#2F5D50;--on:#FFFFFF;--pri-soft:#DDEBE5;--acc:#B8782E;--bad:#A8402B;--bad-soft:#F8E1DC;--hl:#FFF3CF;--b1:#2F6B8C;--b1s:#E3EFF6;--b2:#7A5BA6;--b2s:#EEE8F6;--b3:#2F7A55;--b3s:#E1F1E8;--b4:#B8782E;--b4s:#F8EBD3;--b5:#8A5517;--b5s:#F6EBDD'''
TOKD='''--bg:#161C19;--surface:#1F2723;--ink:#E7ECE6;--sub:#A5B1A8;--line:#33403A;--pri:#84C2AE;--on:#10201B;--pri-soft:#24362F;--acc:#E0B070;--bad:#F08A7E;--bad-soft:#3A2420;--hl:#3B3venue;--b1:#7DB6D8;--b1s:#1D2F3A;--b2:#B79BE0;--b2s:#2B2438;--b3:#7FCBA0;--b3s:#1D3226;--b4:#E0B070;--b4s:#3A3220;--b5:#E6C06E;--b5s:#3A3220'''.replace('#3B3venue','#3A3220')
cards=[]
for d in D:
    x=ES[d['k']]
    sk=vp(d['k'],1); kz=vp(d['k'],2)
    cards.append(f'''<section class="card">
<div class="chead"><span class="cn">{E(x['num'])}</span><span class="ct">{E(x['title'])}</span></div>
<p class="q"><b>【原題】</b>{E(x['question'].replace('【原題】','').strip())}</p>
<div class="vtabs"><button class="vt on" data-v="3">邏輯拆解</button><button class="vt" data-v="1">考場速寫</button><button class="vt" data-v="0">完整四段式</button></div>
<div class="vp" data-v="3">{render(d)}</div>
<div class="vp" data-v="1" hidden>{sk}<div class="sk2">{kz}</div></div>
<div class="vp" data-v="0" hidden><p class="note">（demo 不重貼全文；正式頁這裡就是現在的「完整四段式」，內容不動，只改成第三個分頁。）</p></div>
</section>''')
# 取指揮中心既有的 blk/kou/kw 等樣式片段
m=re.search(r'<style>(.*?)</style>',hub,re.S); hubcss=m.group(1)
want=[r'\.blk\{[^}]*\}',r'\.blk\.b\d\{[^}]*\}',r'\.blk-l\{[^}]*\}',r'\.kou\{[^}]*\}',r'\.kwbox\{[^}]*\}',r'\.kws\{[^}]*\}',r'\.kw\{[^}]*\}',r'\.losebox\{[^}]*\}',r'\.losebox[^{]*\{[^}]*\}',r'mark\.hl\{[^}]*\}',r'\.vtabs\{[^}]*\}',r'\.vt\{[^}]*\}',r'\.vt\.on\{[^}]*\}',r'\.vp\[hidden\]\{[^}]*\}']
pick=[]
for w in want: pick+=re.findall(w,hubcss)
pick=list(dict.fromkeys(pick))
PAGE=f'''<meta name="claude:viewport-fit-sides" content="cover">
<title>邏輯拆解 Demo</title>
<style>
:root{{{TOK};color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{{TOKD};color-scheme:dark}}}}
:root[data-theme="dark"]{{{TOKD};color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 "Noto Sans TC",system-ui,-apple-system,"PingFang TC","Microsoft JhengHei",sans-serif;padding-block:18px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));overflow-x:hidden}}
main{{max-width:880px;margin:0 auto;display:flex;flex-direction:column;gap:16px}}
h1{{font-size:1.25rem;margin:0;color:var(--pri)}}
.lead{{font-size:.88rem;color:var(--sub);margin:0;line-height:1.75}}
.lead b{{color:var(--ink)}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 15px}}
.chead{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;margin-bottom:4px}}
.cn{{font-weight:700;color:var(--pri);font-size:.86rem;background:var(--pri-soft);border-radius:6px;padding:1px 8px}}
.ct{{font-weight:700;font-size:.98rem;line-height:1.5}}
.q{{font-size:.9rem;line-height:1.75;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:9px 12px;margin:8px 0}}
.note{{font-size:.86rem;color:var(--sub)}}
.ask{{background:var(--hl);border-radius:12px;padding:12px 14px;font-size:.9rem;line-height:1.8}}
.ask b{{display:block;margin-bottom:4px}}
.ask ol{{margin:6px 0 0;padding-left:20px}}
.sk2{{margin-top:12px;border:1px solid var(--line);border-radius:10px;padding:4px 12px 8px}}
{chr(10).join(pick)}
{CSS}
</style>
<main>
<h1>邏輯拆解 demo（經紀法規申論卡）</h1>
<p class="lead">照民法 v395 的做法改：每題分頁變成 <b>邏輯拆解 → 考場速寫（併得分關鍵・失分點）→ 完整四段式</b>，打開預設停在邏輯拆解。<br>
邏輯拆解裡有三種排法可切換，資料同一份：<b>① 推理鏈</b>（第一次讀懂）、<b>② 條文｜本題</b>（對答案）、<b>③ 地圖＋勾選</b>（考前複習）。選哪種會記住。<br>
下面兩張卡是真的內容：<b>範文06</b> 是案例題（三問、有罰則），<b>範文01</b> 是說明題（沒有案例事實，「本題」欄改成「舉例」；行政命令標「要點整理」）。</p>
{''.join(cards)}
<div class="ask"><b>要你回覆的三件事</b>
<ol><li>三種排法都留，還是只留其中一兩種？</li><li>分頁順序「邏輯拆解 → 考場速寫 → 完整四段式」可以嗎？預設停在邏輯拆解可以嗎？</li><li>說明題用「舉例」欄（看範文01）這樣處理清楚嗎？</li></ol>
說可以，我就把 65 題全部改成這樣。</div>
</main>
<script>{JS}</script>
<script>document.addEventListener('click',function(e){{var b=e.target.closest&&e.target.closest('.vt');if(!b)return;var c=b.closest('.card');c.querySelectorAll('.vt').forEach(function(x){{x.classList.toggle('on',x===b)}});c.querySelectorAll('.vp').forEach(function(p){{p.hidden=p.dataset.v!==b.dataset.v}})}});</script>'''
open(os.path.join(HERE,'demo_lj.html'),'w',encoding='utf-8').write(PAGE)
print('ok',len(PAGE))
