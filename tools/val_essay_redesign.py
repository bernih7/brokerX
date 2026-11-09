# -*- coding: utf-8 -*-
"""《不動產估價概要_申論題實戰範文》申論清單改版（比照民法 v775，使用者 11-09「好」）：
- 類別組依 115 預測期望題數排序（同頁「各類出題頻率」算法：16 年占比×0.6＋近 5 年占比×0.4，正規化×2）
- 組標頭：115 預估膠囊＋讀懂進度條
- 題目列：左側圓圈＝讀懂（同 bx-essay-read，呼叫原 toggleRead）、拿掉 A／B／C 級字樣、右側 5 分鐘鈕（未讀→推理版、已讀→衝刺）
- 展開卡底部：推理版／衝刺／單題頁
- 篩選列改：全部／官方／本站模擬／補習班／預測＋只看未讀＋搜尋＋全部展開／收合（原優先度／類別篩選收起不用）
可重跑（以 id 取代既有區塊）。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(R, '不動產估價概要_申論題實戰範文.html')
CSS = r'''<style id="vsx-css">
.filter-panel{display:none!important}
.usage-box{display:none!important}
#vsx-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;background:var(--paper2);border:1.5px solid var(--line);border-radius:12px;padding:10px 12px;margin:0 0 14px}
#vsx-bar button{font:inherit;font-size:.8rem;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:4px 11px;cursor:pointer}
#vsx-bar button[aria-pressed="true"]{background:var(--primary);border-color:var(--primary);color:#fff}
#vsx-bar input{flex:1;min-width:150px;font:inherit;font-size:.82rem;border:1px solid var(--line);border-radius:999px;padding:5px 12px;background:var(--paper);color:var(--ink)}
#vsx-bar .brk{flex-basis:100%;height:0}
.tgroup>summary{flex-wrap:wrap}
.vsx-gst{display:flex;flex-wrap:wrap;gap:8px;align-items:center;flex-basis:100%;padding-left:18px;font-size:.76rem;color:var(--muted)}
.vsx-pred{display:inline-flex;align-items:baseline;gap:3px;padding:1px 9px;border-radius:999px;background:rgba(0,0,0,.06);color:var(--muted)}
.vsx-pred b{color:var(--ink);font-size:.86rem}
.vsx-pred.hi{background:rgba(168,64,48,.12);color:var(--stamp)}.vsx-pred.hi b{color:var(--stamp)}
.vsx-pr{display:flex;align-items:center;gap:8px;flex:1;min-width:180px}
.vsx-tr{flex:1;max-width:260px;height:7px;border-radius:5px;background:rgba(0,0,0,.08);overflow:hidden}
.vsx-tr i{display:block;height:100%;background:var(--green)}
.vsx-pr b{color:var(--ink);font-variant-numeric:tabular-nums}
.essay-card .read-btn{display:none!important}
.card-header{gap:10px;padding:12px 14px}
.vsx-ck{flex:none;width:24px;height:24px;border-radius:50%;border:1.5px solid var(--line);background:var(--paper);color:transparent;font-size:13px;display:grid;place-items:center;cursor:pointer;padding:0;align-self:flex-start;margin-top:2px}
.essay-card.read .vsx-ck{background:var(--green);border-color:var(--green);color:#fff}
.essay-card.read .card-title{color:var(--muted)}
.essay-card.read:not(.open){opacity:1!important}
.vsx-go{flex:none;font-size:.76rem;color:var(--primary);text-decoration:none;white-space:nowrap;border:1px solid var(--line);border-radius:999px;padding:3px 10px;background:var(--paper)}
.vsx-act{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px;padding-top:10px;border-top:1px dashed var(--line)}
.vsx-act a{font-size:.8rem;border:1px solid var(--line);background:var(--paper);color:var(--primary);border-radius:999px;padding:4px 12px;text-decoration:none}
.essay-card .card-header .card-arrow{display:none}
@media(max-width:560px){.vsx-go{font-size:.7rem;padding:3px 8px}.vsx-gst{padding-left:0}}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .vsx-tr{background:rgba(255,255,255,.12)}:root:not([data-theme="light"]) .vsx-pred{background:rgba(255,255,255,.08)}}
:root[data-theme="dark"] .vsx-tr{background:rgba(255,255,255,.12)}:root[data-theme="dark"] .vsx-pred{background:rgba(255,255,255,.08)}
</style>'''
JS = r'''<script id="vsx-js">
(function(){
  var RK='bx-essay-read',RS='估價_申論5分鐘_推理版.html',SP='估價_申論5分鐘衝刺.html',CV='估價_申論卡.html';
  function rl(){try{return JSON.parse(localStorage.getItem(RK)||'[]')||[]}catch(e){return []}}
  var cards=[].slice.call(document.querySelectorAll('.essay-card[id]'));
  function kind(c){return /^e\d/.test(c.id)?'off':(c.id.indexOf('pred-')===0?'pred':(c.classList.contains('smock')?'smock':(c.classList.contains('mock')?'mock':'other')))}
  function yr(c){var m=c.id.match(/^e(\d+)-/);return m?+m[1]:0}
  document.querySelectorAll('header .sub').forEach(function(e){e.innerHTML=e.innerHTML.replace('（A/B/C三級）','（依 115 預估排序）')});
  /* 115 預估：同「各類出題頻率」算法 */
  var F={},tot=0,tr=0,W={},ws=0;
  cards.forEach(function(c){var y=c.getAttribute('data-type');F[y]=F[y]||{a:0,r:0};if(kind(c)!=='off')return;F[y].a++;tot++;if(yr(c)>=110){F[y].r++;tr++}});
  Object.keys(F).forEach(function(k){W[k]=0.6*F[k].a/(tot||1)+0.4*F[k].r/(tr||1);ws+=W[k]});
  var groups=[].slice.call(document.querySelectorAll('details.tgroup'));
  function gp(g){return 2*(W[g.getAttribute('data-g')]||0)/(ws||1)}
  if(groups.length){var par=groups[0].parentNode,anchor=groups[groups.length-1].nextSibling;
    groups.slice().sort(function(a,b){return gp(b)-gp(a)}).forEach(function(g){par.insertBefore(g,anchor)});}
  groups.forEach(function(g){var s=g.querySelector('summary');if(!s||s.querySelector('.vsx-gst'))return;
    var k=g.getAttribute('data-g'),p=gp(g),hi=p>=0.4,f=F[k]||{a:0,r:0};
    var d=document.createElement('span');d.className='vsx-gst';
    d.innerHTML='<span>16 年官方 '+f.a+'・近 5 年 '+f.r+'</span><span class="vsx-pred'+(hi?' hi':'')+'">115 預估<b>'+p.toFixed(2)+'</b>題'+(hi?'・優先':'')+'</span><span class="vsx-pr">讀懂<span class="vsx-tr"><i></i></span><b class="vsx-n"></b></span>';
    s.appendChild(d);});
  /* 題目列 */
  cards.forEach(function(c){var h=c.querySelector('.card-header');if(!h||h.querySelector('.vsx-ck'))return;
    var y=c.querySelector('.card-year');if(y)y.textContent=y.textContent.replace(/(?:🔴|🟡|🟢)\s*[ABC]\s*級\s*｜?/g,'').replace(/｜\s*$/,'').trim();
    var b=document.createElement('button');b.type='button';b.className='vsx-ck';b.textContent='✓';b.setAttribute('aria-label','切換讀懂');
    b.addEventListener('click',function(ev){ev.stopPropagation();toggleRead(c.id)});h.insertBefore(b,h.firstChild);
    var a=document.createElement('a');a.className='vsx-go';a.addEventListener('click',function(ev){ev.stopPropagation()});
    var arrow=h.querySelector('.card-arrow');h.insertBefore(a,arrow||null);
    var body=c.querySelector('.card-body');if(body&&!body.querySelector('.vsx-act')){var x=document.createElement('div');x.className='vsx-act';
      x.innerHTML='<a href="'+RS+'#q='+c.id+'">🧩 推理版 5 分鐘 ▸</a><a href="'+SP+'#q='+c.id+'">⏱ 考場版衝刺 ▸</a><a href="'+CV+'#'+c.id+'" target="_blank" rel="noopener">單題頁（另開）▸</a>';body.appendChild(x);}
  });
  function paint(){var r=rl();
    cards.forEach(function(c){var on=r.indexOf(c.id)>=0,a=c.querySelector('.vsx-go');if(a){a.href=(on?SP:RS)+'#q='+c.id;a.textContent=(on?'衝刺':'推理')+' 5 分鐘 ▸'}});
    groups.forEach(function(g){var cs=g.querySelectorAll('.essay-card[id]'),n=0;cs.forEach(function(c){if(r.indexOf(c.id)>=0)n++});
      var i=g.querySelector('.vsx-tr i'),b=g.querySelector('.vsx-n');if(i)i.style.width=(cs.length?Math.round(n/cs.length*100):0)+'%';if(b)b.textContent=n+'／'+cs.length;});
    apply();}
  /* 篩選列 */
  var cur='all',unread=false,q='';
  var fp=document.querySelector('.filter-panel');
  if(fp&&!document.getElementById('vsx-bar')){var n={all:cards.length,off:0,smock:0,mock:0,pred:0};cards.forEach(function(c){n[kind(c)]=(n[kind(c)]||0)+1});
    var bar=document.createElement('div');bar.id='vsx-bar';
    bar.innerHTML='<button data-f="all" aria-pressed="true">全部 '+n.all+'</button><button data-f="off" aria-pressed="false">官方 '+n.off+'</button>'+(n.smock?'<button data-f="smock" aria-pressed="false">本站模擬 '+n.smock+'</button>':'')+(n.mock?'<button data-f="mock" aria-pressed="false">補習班 '+n.mock+'</button>':'')+'<button data-f="pred" aria-pressed="false">預測 '+n.pred+'</button><button id="vsx-un" aria-pressed="false">只看未讀</button><span class="brk"></span><input id="vsx-q" type="search" placeholder="搜尋題目、題號或條號，例如 §81"><button id="vsx-all">全部展開</button><button id="vsx-none">全部收合</button>';
    fp.parentNode.insertBefore(bar,fp);
    bar.addEventListener('click',function(ev){var t=ev.target.closest('button');if(!t)return;
      if(t.dataset.f){cur=t.dataset.f;bar.querySelectorAll('[data-f]').forEach(function(x){x.setAttribute('aria-pressed',x===t)});apply();return}
      if(t.id==='vsx-un'){unread=!unread;t.setAttribute('aria-pressed',unread);apply();return}
      if(t.id==='vsx-all'||t.id==='vsx-none'){var o=t.id==='vsx-all';groups.forEach(function(g){g.open=o});return}});
    document.getElementById('vsx-q').addEventListener('input',function(){q=this.value.trim();if(q)groups.forEach(function(g){g.open=true});apply()});}
  function apply(){if(!document.getElementById('vsx-bar'))return;var r=rl();
    cards.forEach(function(c){var ok=(cur==='all'||kind(c)===cur)&&!(unread&&r.indexOf(c.id)>=0)&&(!q||(c.id+' '+c.textContent).indexOf(q)>=0);c.classList.toggle('hidden',!ok)});
    groups.forEach(function(g){g.style.display=g.querySelectorAll('.essay-card:not(.hidden)').length?'':'none'});}
  paint();
  var op=window.paintRead;if(typeof op==='function'){window.paintRead=function(){op.apply(this,arguments);paint()}}
  ['pageshow','visibilitychange','storage'].forEach(function(e){addEventListener(e,function(){if(typeof window.paintRead==='function')window.paintRead();else paint()})});
})();
</script>'''
s = open(P, encoding='utf-8').read()
def put(s, id_, block, before):
    pat = re.compile(r'<(style|script) id="%s">.*?</\1>' % id_, re.S)
    if pat.search(s): return pat.sub(lambda m: block, s, count=1)
    return s.replace(before, block + '\n' + before, 1)
s = put(s, 'vsx-css', CSS, '</head>')
s = put(s, 'vsx-js', JS, '</body>')
open(P, 'w', encoding='utf-8').write(s); print('ok')
