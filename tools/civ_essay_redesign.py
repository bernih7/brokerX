# -*- coding: utf-8 -*-
"""民法指揮中心「申論」分頁外層改版（使用者 11-08 看過 demo 後同意）：
- 分類依「115 預估題數」由高到低排序；標題列＝名稱＋16 年／近 5 年／115 預估（帶單位、≥0.4 標優先）＋常考＋讀懂進度條
- 題目列精簡：左邊圓圈＝讀懂（點了等同勾「我已讀懂這題的邏輯」）、條號灰字不加底、拿掉星等與左側色條
- 每題右邊 5 分鐘鈕：還沒讀懂→推理版、已讀懂→考場版衝刺（#q=卡號）
- 展開後底部動作列：推理版／衝刺／單題頁；考場版內文鋪滿寬度；完整四段式「全部收起／展開」
- 篩選：全部｜官方｜模擬卷｜預測｜只看未讀＋搜尋＋全部展開／收合（A／B／C 級鈕拿掉）；必背條一列＋「全部 N 條」
紀錄鍵（minfa_read、bxm-es-log、bxm-es-sprint）不變。可重跑：以 esx-css／esx-js 為邊界整段替換。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(R, '民法_備考指揮中心.html')

CSS = r'''<style id="esx-css">
/* 申論分頁外層改版（tools/civ_essay_redesign.py） */
.gcol{display:none!important}
#elist details.gdet{border:1px solid var(--line)!important;border-radius:12px;padding:0 12px}
#elist details.gdet>summary{padding:12px 2px}
#elist details.gdet>summary .grp{display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;column-gap:14px;row-gap:3px;align-items:center;max-width:none;margin:0}
#elist details.gdet>summary .grp>b{grid-column:1;grid-row:1;font-size:1.06rem;color:var(--ink)}
#elist details.gdet>summary .grp .gst{grid-column:2;grid-row:1;justify-self:end}
#elist details.gdet>summary .grp .gwd{grid-column:1/-1;grid-row:2;display:block;padding:0 0 0 1.15em;font:400 .8rem/1.55 "Noto Sans TC",sans-serif;color:var(--sub);text-align:left}
#elist details.gdet>summary .grp .gwd:before{content:"常考：";font-weight:700}
#elist details.gdet>summary .grp .sub{grid-column:1/-1;grid-row:3;margin:0 0 0 1.15em}
#elist details.gdet>summary .grp .gpr{grid-column:1/-1;grid-row:4;margin-left:1.15em}
#elist .gn{display:none!important}
.gst{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;font:400 .74rem "Noto Sans TC",sans-serif;color:var(--sub);white-space:nowrap}
.gst b{font-size:.95rem;color:var(--ink);margin-left:3px;font-variant-numeric:tabular-nums}
.gst .pv{padding:1px 9px;border-radius:999px;background:color-mix(in srgb,var(--ink) 7%,transparent)}
.gst .pv.hi{background:var(--bad-soft);color:var(--bad)}
.gst .pv.hi b{color:var(--bad)}
.gpr{display:flex;align-items:center;gap:8px;font:400 .74rem "Noto Sans TC",sans-serif;color:var(--sub)}
.gpr .tr{flex:1;max-width:300px;height:7px;border-radius:5px;background:color-mix(in srgb,var(--ink) 9%,transparent);overflow:hidden}
.gpr .tr i{display:block;height:100%;background:var(--ok)}
.gpr b{color:var(--ink);font-variant-numeric:tabular-nums}
.ginfo .gr a.ball{margin-left:auto;font-size:.78rem;color:var(--sub);text-decoration:none;border:0;cursor:pointer}
#elist details.essay.es{border:1px solid var(--line)!important;border-radius:10px;padding:2px 12px;margin:6px 0}
#elist details.essay.es.pred{border-style:dashed!important}
#elist details.essay.es[open]{border-color:var(--pri)!important}
#elist details.essay.es>summary{padding:9px 0}
#elist details.essay .eh{display:flex;gap:10px;align-items:flex-start}
#elist details.essay .st{display:none}
#elist details.essay .ck{display:inline-grid!important;place-items:center;flex:none;width:21px;height:21px;margin-top:1px;border-radius:50%;border:1.5px solid var(--line);background:var(--surface);color:transparent;font-size:12px;font-weight:900;cursor:pointer}
#elist details.essay.read .ck{background:var(--ok);border-color:var(--ok);color:#fff}
#elist details.essay.read .et{color:var(--sub)}
#elist details.essay .go5{flex:none;font:500 .74rem "Noto Sans TC",sans-serif;color:var(--pri);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:2px 10px;white-space:nowrap;align-self:center}
#elist details.essay .em,#elist details.essay .chips{margin-left:31px}
#elist details.essay .chips{gap:0;margin-top:2px}
#elist details.essay .chips i{background:none;border:0;padding:0;border-radius:0;font-size:.74rem;color:var(--sub)}
#elist details.essay .chips i+i:before{content:"・";color:var(--line)}
#elist details.essay .chips i:nth-child(n+6){display:none}
#elist details.essay .chips i.pc{background:var(--acc-soft);color:var(--acc-ink);border-radius:4px;padding:0 5px;margin-right:4px}
#elist details.essay .chips i.pc+i:before{content:none}
.ebody .evb p{max-width:none!important}
.ebody .eact{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.ebody .eact a{font-size:.8rem;border:1px solid var(--line);background:var(--surface);color:var(--pri);border-radius:999px;padding:3px 12px;text-decoration:none;font-weight:700}
.ebody label.done{display:inline-flex!important;padding:5px 14px;border-radius:999px;background:var(--pri);color:var(--on);font-weight:700;cursor:pointer}
.ebody label.done input{accent-color:var(--on)}
.ftool{display:flex;justify-content:flex-end;margin:2px 0 4px}
.ftool button{font:inherit;font-size:.8rem;font-weight:700;border:1px solid var(--line);background:var(--surface);color:var(--pri);border-radius:999px;padding:3px 12px;cursor:pointer}
#fl .brk{flex-basis:100%;height:0}
@media(max-width:560px){
 #elist details.gdet>summary .grp{grid-template-columns:minmax(0,1fr)!important}
 #elist details.gdet>summary .grp .gst{grid-column:1;grid-row:2;justify-self:start;margin-left:1.15em;white-space:normal}
 #elist details.gdet>summary .grp .gwd{grid-row:3}
 #elist details.gdet>summary .grp .sub{grid-row:4}
 #elist details.gdet>summary .grp .gpr{grid-row:5}
 #elist details.essay .em,#elist details.essay .chips{margin-left:31px}
}
</style>'''

JS = r'''<script id="esx-js">
/* 申論分頁外層改版（tools/civ_essay_redesign.py）：只讀 minfa_read，勾讀懂一律透過卡內原本的 checkbox */
(function(){
var L=document.getElementById('elist');if(!L)return;
var R={g1:[7,2,0.45],g2:[5,1,0.25],g3:[5,2,0.4],g4:[6,4,0.6],g5:[5,0,0.15],g6:[4,1,0.15]};
var REASON='民法_申論5分鐘_推理版.html',SPRINT='民法_申論5分鐘衝刺.html',CARD='民法_申論卡.html';
function rs(){try{return JSON.parse(localStorage.getItem('minfa_read')||'{}')||{}}catch(e){return{}}}
var G=[].slice.call(L.querySelectorAll(':scope>details.gdet'));
G.sort(function(a,b){return (R[b.dataset.g]||[0,0,0])[2]-(R[a.dataset.g]||[0,0,0])[2]}).forEach(function(d){L.appendChild(d)});
G.forEach(function(d){var r=R[d.dataset.g];if(!r)return;var gp=d.querySelector('summary .grp');if(!gp||gp.querySelector('.gst'))return;
  var s=document.createElement('span');s.className='gst';
  s.innerHTML='<span>16 年<b>'+r[0]+'</b></span><span>近 5 年<b>'+r[1]+'</b></span><span class="pv'+(r[2]>=0.4?' hi':'')+'">115 預估<b>'+r[2].toFixed(2)+'</b> 題'+(r[2]>=0.4?'・優先':'')+'</span>';
  gp.appendChild(s);var p=document.createElement('span');p.className='gpr';p.innerHTML='合計<span class="tr"><i></i></span><b></b>';gp.appendChild(p);
  var bt=d.querySelector('details.btg'),gr=d.querySelector('.ginfo .gr');
  if(bt&&gr&&!gr.querySelector('.ball')){var m=/（(\d+)\s*條）/.exec(bt.querySelector('summary').textContent);bt.hidden=true;
    var a=document.createElement('a');a.className='ball';a.href='#';a.textContent=(m?'全部 '+m[1]+' 條':'全部條文')+' ▸';gr.appendChild(a);
    a.addEventListener('click',function(ev){ev.preventDefault();bt.hidden=!bt.hidden;if(!bt.hidden){bt.open=true;a.textContent=a.textContent.replace('▸','▾')}else a.textContent=a.textContent.replace('▾','▸')})}});
var ES=[].slice.call(L.querySelectorAll('details.essay'));
ES.forEach(function(e){var k=e.dataset.key,eh=e.querySelector('summary .eh');if(!eh||eh.querySelector('.go5'))return;
  var ck=eh.querySelector('.ck');if(ck){eh.insertBefore(ck,eh.firstChild);ck.setAttribute('role','button');ck.setAttribute('tabindex','0');ck.title='讀懂（點一下切換）'}
  var g=document.createElement('a');g.className='go5';g.target='_blank';g.rel='noopener';eh.appendChild(g);
  var body=e.querySelector('.ebody'),dn=body&&body.querySelector('label.done');
  if(dn&&!body.querySelector('.eact')){var x=document.createElement('div');x.className='eact';var q='#q='+encodeURIComponent(k);
    x.innerHTML='<a target="_blank" rel="noopener" href="'+REASON+q+'">推理版 5 分鐘 ▸</a><a target="_blank" rel="noopener" href="'+SPRINT+q+'">考場版衝刺 ▸</a><a target="_blank" rel="noopener" href="'+CARD+'#'+encodeURIComponent(k)+'">單題頁（另開）▸</a>';
    dn.parentNode.insertBefore(x,dn)}
  var f=body&&body.querySelector('.vp[data-v="0"]');
  if(f&&!f.querySelector('.ftool')){var t=document.createElement('div');t.className='ftool';t.innerHTML='<button type="button">全部收起</button>';f.insertBefore(t,f.firstChild);
    t.firstChild.addEventListener('click',function(){var ds=[].slice.call(f.querySelectorAll('details.fd')),op=ds.some(function(z){return z.open});ds.forEach(function(z){z.open=!op});this.textContent=op?'全部展開':'全部收起'})}});
function paint(){var S=rs();
  ES.forEach(function(e){var k=e.dataset.key,g=e.querySelector('.go5');if(!g)return;var rd=!!S[k];
    g.textContent=rd?'衝刺 5 分鐘 ▸':'推理 5 分鐘 ▸';g.href=(rd?SPRINT:REASON)+'#q='+encodeURIComponent(k);g.title=rd?'已讀懂：用考場版衝刺驗收':'還沒讀懂：先用推理版走一遍邏輯'});
  G.forEach(function(d){var es=ES.filter(function(e){return e.dataset.g===d.dataset.g}),n=es.filter(function(e){return S[e.dataset.key]}).length,p=d.querySelector('.gpr');
    if(p){p.querySelector('i').style.width=(es.length?Math.round(n/es.length*100):0)+'%';p.querySelector('b').textContent=n+'／'+es.length}})}
L.addEventListener('click',function(ev){var c=ev.target.closest('summary .ck');if(c){ev.preventDefault();ev.stopPropagation();var e=c.closest('details.essay'),i=e&&e.querySelector('label.done input');if(i)i.click();setTimeout(paint,0);return}
  if(ev.target.closest('summary .go5'))ev.stopPropagation()},true);
L.addEventListener('keydown',function(ev){var c=ev.target.closest&&ev.target.closest('summary .ck');if(c&&(ev.key==='Enter'||ev.key===' ')){ev.preventDefault();c.click()}});
L.addEventListener('change',function(){setTimeout(paint,0)});
addEventListener('pageshow',paint);document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')paint()});
addEventListener('storage',function(e){if(e.key==='minfa_read')paint()});
paint();
})();
</script>'''

s = open(P, encoding='utf-8').read()
# 篩選鈕：A／B／C 級 → 官方；未讀 → 只看未讀；搜尋與展開收合換到第二排
nOff = len(re.findall(r'<details class="essay(?![^"]*\bpred\b)[^"]*"', s))
fl_a = s.index('<div class="filters" id="fl">'); fl_b = s.index('</div>', fl_a) + 6
FL = ('<div class="filters" id="fl">\n    <button data-f="all" class="on">全部 86</button>\n'
      '    <button data-f="O">官方 %d</button>\n    <button data-f="M">模擬卷 5</button>\n    <button data-f="P">預測 49</button>\n'
      '    <button data-f="unread">只看未讀</button>\n    <span class="brk"></span>\n'
      '    <input type="search" id="sq" placeholder="搜尋題目、年度或條號，例如 §824-1">\n'
      '    <button id="ex">全部展開</button><button id="co">全部收合</button>\n    <span class="sub" id="rcount"></span>\n  </div>') % nOff
s = s[:fl_a] + FL + s[fl_b:]
old = "if(curF==='A'||curF==='B'||curF==='C'||curF==='P'||curF==='M')ok=e.dataset.lv===curF;else if(curF==='unread')"
new = "if(curF==='A'||curF==='B'||curF==='C'||curF==='P'||curF==='M')ok=e.dataset.lv===curF;else if(curF==='O')ok=!e.classList.contains('pred');else if(curF==='unread')"
if new not in s:
    assert s.count(old) == 1; s = s.replace(old, new)
s = s.replace('色條＝篇別（綠 A總則・藍 B債總・金 C債分・紫 D物權・紅 E親屬繼承）；★★★／★★／★＝A／B／C 級；虛線色條＝預測題（自擬非官方）；✓＝已讀。',
              '標題前小圓點＝篇別（綠 A總則・藍 B債總・金 C債分・紫 D物權・紅 E親屬繼承）；虛線框＝預測題與模擬卷（非官方）；左邊圓圈打勾＝已讀懂（點圓圈可切換）。分類依「115 預估」由高到低排列。')
def put(s, tag, block, where):
    a = s.find('<%s id="%s">' % (('style' if 'css' in tag else 'script'), tag))
    if a >= 0:
        b = s.index('</style>' if 'css' in tag else '</script>', a) + (8 if 'css' in tag else 9)
        return s[:a] + block + s[b:]
    i = s.rindex(where); return s[:i] + block + '\n' + s[i:]
s = put(s, 'esx-css', CSS, '</head>')
s = put(s, 'esx-js', JS, '</body>')
open(P, 'w', encoding='utf-8').write(s)
print('OK 官方', nOff)
