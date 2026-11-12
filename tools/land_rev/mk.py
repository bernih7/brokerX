# -*- coding: utf-8 -*-
"""產生 土地法_反向申論練習.html（114-二 型）。可重跑。"""
import os, sys, html as H, re
sys.path.insert(0, os.path.dirname(__file__))
from data import DEMO, Q
R = os.path.join(os.path.dirname(__file__), '..', '..')
def t(s):
    s = H.escape(s)
    return re.sub(r'‖(.+?)‖', r'<mark>\1</mark>', s)
def rows(rs):
    return '<div class="map">' + ''.join('<div class="mr"><div class="mf">%s</div><div class="ma">→ %s</div></div>' % (t(a), t(b)) for a, b in rs) + '</div>'
cards = []
for i, x in enumerate(Q, 1):
    app = ''.join('<div class="ap"><b>%s</b><p>%s</p></div>' % (t(h), t(p)) for h, p in x['app'])
    cards.append(f'''<details class="card" id="{x['id']}"><summary><span class="no">反向 {i}</span><span class="tt">{t(x['t'])}</span><span class="lw">{t(x['law'])}</span></summary>
<div class="q"><b>題目</b>{t(x['q'])}</div>
<div class="step"><div class="sh">① 先讀題：題幹每個事實在考什麼</div>{rows(x['rows'])}</div>
<div class="step"><div class="sh">② 先自己想要件，再打開四段式對答案</div>
<details class="blk b1"><summary>一、定義</summary><p>{t(x['d'])}</p></details>
<details class="blk b2"><summary>二、法條</summary><p>{t(x['law_t'])}</p></details>
<details class="blk b3"><summary>三、涵攝分析（逐一要件對題目事實）</summary>{app}</details>
<details class="blk b4"><summary>四、結論</summary><p>{t(x['c'])}</p></details></div>
<div class="tr"><b>⚠️ 失分陷阱</b><ul>{''.join('<li>'+t(z)+'</li>' for z in x['traps'])}</ul></div>
</details>''')
page = f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"><script src="bx-vp.js"></script><title>土地法反向申論練習</title>
<script>(function(){{var s=null;try{{s=localStorage.getItem('bx-theme')}}catch(e){{}}if(s)document.documentElement.setAttribute('data-theme',s)}})();</script>
<style>
:root{{--pri:#2F5D50;--key:#8A5517;--onpri:#FFFFFF;--bg:#F5F1E6;--ink:#25302C;--card:#FFFEFA;--line:#DDD6C0;--muted:#66706A;--hl:#FFE58F;--b1:#EEF4EC;--b2:#EDF1F7;--b3:#FBF3E6;--b4:#FBECEC;--warn:#FFF1D6;color-scheme:light}}
@media(prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--pri:#84C2AE;--key:#E0B070;--onpri:#10201B;--bg:#161C19;--ink:#E7ECE6;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--hl:#6E5716;--b1:#1D2A22;--b2:#1C2430;--b3:#2C2619;--b4:#2E1E1E;--warn:#3A2E14;color-scheme:dark}}}}
:root[data-theme="dark"]{{--pri:#84C2AE;--key:#E0B070;--onpri:#10201B;--bg:#161C19;--ink:#E7ECE6;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--hl:#6E5716;--b1:#1D2A22;--b2:#1C2430;--b3:#2C2619;--b4:#2E1E1E;--warn:#3A2E14;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15.5px/1.8 "Noto Sans TC",system-ui,sans-serif;padding-inline:16px;padding-block:18px 96px}}
main{{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:14px}}
h1{{font-size:22px;margin:0;text-wrap:balance}}.sub{{color:var(--muted);font-size:14px}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.box h2{{font-size:17px;margin:0 0 6px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}}
.card>summary{{cursor:pointer;display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline;list-style:none}}
.card>summary::-webkit-details-marker{{display:none}}
.no{{font-size:12px;font-weight:700;color:var(--onpri);background:var(--pri);border-radius:99px;padding:1px 9px}}
.tt{{font-weight:700;font-size:16px}}.lw{{color:var(--muted);font-size:13px}}
.q{{margin:10px 0;padding:10px 12px;background:var(--b2);border-radius:8px}}.q b{{display:block;color:var(--key);font-size:13px}}
.sh{{font-weight:700;color:var(--key);margin:10px 0 6px}}
.map{{display:flex;flex-direction:column;gap:6px}}
.mr{{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);gap:10px;border-bottom:1px dashed var(--line);padding-bottom:6px}}
.mf{{font-weight:700}}.ma{{min-width:0}}
@media(max-width:600px){{.mr{{grid-template-columns:1fr;gap:0}}}}
.blk{{border-radius:10px;margin:6px 0;padding:6px 12px}}.blk>summary{{cursor:pointer;font-weight:700}}
.b1{{background:var(--b1)}}.b2{{background:var(--b2)}}.b3{{background:var(--b3)}}.b4{{background:var(--b4)}}
.ap{{margin:8px 0}}.ap b{{display:block;color:var(--key)}}.ap p,.blk p{{margin:2px 0}}
mark{{background:var(--hl);color:inherit;font-weight:700;padding:0 2px;border-radius:3px}}
.tr{{background:var(--warn);border-radius:8px;padding:8px 12px;margin-top:10px}}.tr ul{{margin:4px 0;padding-left:1.3em}}
.btn{{font:inherit;font-size:14px;padding:5px 14px;border-radius:99px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}}
a{{color:var(--pri)}}#hub{{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));width:46px;height:46px;border-radius:50%;background:var(--pri);color:var(--onpri);display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:20px}}
</style></head><body><main>
<h1>土地法 反向申論練習</h1>
<div class="sub">114-二 型：題目先給結果（「經告知得適用某條而免徵／按某稅率」），再在題幹埋幾個事實，要你倒推「必須具備哪些要件」。練的是<b>讀出每個事實在考哪個要件、哪個陷阱</b>。條文皆已對本站逐字條文庫。</div>
<div class="box"><h2>示範：官方 114-二 怎麼拆</h2><div class="q"><b>原題</b>{t(DEMO['q'])}</div>{rows(DEMO['rows'])}<p class="sub">完整答案：<a href="{DEMO['link']}">申論總覽 114-二 ›</a></p></div>
<div class="box"><b>練法</b>：每題先只看題目，自己列出「這句話在考什麼」→ 打開①對照 → 再自己想要件 → 打開②四段式。<button class="btn" id="all" type="button">全部展開</button></div>
{''.join(cards)}
</main><a id="hub" href="土地法_備考指揮中心.html" aria-label="回備考指揮中心">🏠</a>
<script>(function(){{var b=document.getElementById("all"),o=false;b.onclick=function(){{o=!o;document.querySelectorAll("details").forEach(function(d){{d.open=o}});b.textContent=o?"全部收合":"全部展開"}};if(location.hash){{var d=document.querySelector(location.hash);if(d&&d.tagName==="DETAILS")d.open=true}}}})();</script>
<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("/brokerX/sw.js",{{scope:"/brokerX/"}});</script>
</body></html>'''
open(os.path.join(R, '土地法_反向申論練習.html'), 'w', encoding='utf-8').write(page)
print('ok', len(Q))
