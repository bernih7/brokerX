# -*- coding: utf-8 -*-
"""《民法_備考指揮中心》申論卡：看了幾輪、每輪多久、看完自評（施工單第 5 項，移植估價 v527～v528）。

新鍵 bxm-es-log = {題號: {n:輪數, s:[最近5輪秒數], tot:總秒數, v:'ok'|'mem'|'hard', t}}；minfa_read 不動。
- 卡片（details.essay）展開才計時；切到背景或閒置 2 分鐘不算。
- 一輪＝本次展開累計 ≥20 秒，且捲到該卡底部（「我已讀懂這題的邏輯」那列進入畫面）；每次展開最多記一輪。
- 自評三類：✅ 熟／📖 還沒背起來／😵 太難，再按一次取消。
可重複執行（以 <style id="esl-css">～<script id="esl-js"> 為邊界整段換掉）。
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
HUB = os.path.normpath(os.path.join(HERE, '..', '..', '民法_備考指揮中心.html'))

BLOCK = r'''<style id="esl-css">
.esl{display:flex;flex-wrap:wrap;gap:6px 8px;align-items:center;margin-top:8px;padding-top:8px;border-top:1px dashed var(--line);font-size:.8rem;color:var(--sub)}
.esl .eslst{font-variant-numeric:tabular-nums;margin-right:auto}
.esl .eslst b{color:var(--ink)}
.esl button{font:inherit;font-size:.76rem;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:3px 10px;cursor:pointer}
.esl button.on[data-v="ok"]{background:var(--ok);border-color:var(--ok);color:var(--surface);font-weight:700}
.esl button.on[data-v="mem"]{background:var(--acc);border-color:var(--acc);color:var(--surface);font-weight:700}
.esl button.on[data-v="hard"]{background:var(--bad);border-color:var(--bad);color:var(--surface);font-weight:700}
.eslv{font-style:normal;font-size:.72rem;margin-left:4px}
#eslSum{font-size:.78rem;color:var(--sub);margin:4px 0 0}
</style>
<script id="esl-js">
(function(){
var KEY='bxm-es-log',VN={ok:'✅ 熟',mem:'📖 還沒背起來',hard:'😵 太難'},VI={ok:'✅',mem:'📖',hard:'😵'};
function ld(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}}
function sv(L){try{localStorage.setItem(KEY,JSON.stringify(L))}catch(e){}}
function fmt(x){x=Math.round(x||0);return Math.floor(x/60)+':'+('0'+(x%60)).slice(-2)}
var essays=[].slice.call(document.querySelectorAll('details.essay'));if(!essays.length)return;
var act=Date.now();['pointerdown','keydown','scroll','touchstart'].forEach(function(ev){addEventListener(ev,function(){act=Date.now()},{passive:true})});
var S={}; /* 每張卡本次展開的狀態 {sec, counted} */
function row(e){
  var k=e.dataset.key,body=e.querySelector('.ebody');if(!body)return null;
  var r=body.querySelector('.esl');if(r)return r;
  r=document.createElement('div');r.className='esl';
  r.innerHTML='<span class="eslst"></span><button type="button" data-v="ok">'+VN.ok+'</button><button type="button" data-v="mem">'+VN.mem+'</button><button type="button" data-v="hard">'+VN.hard+'</button>';
  body.appendChild(r);
  r.addEventListener('click',function(ev){var b=ev.target.closest('button[data-v]');if(!b)return;
    var L=ld(),x=L[k]=L[k]||{n:0,s:[],tot:0};x.v=(x.v===b.dataset.v)?'':b.dataset.v;if(!x.v)delete x.v;x.t=Math.floor(Date.now()/1000);sv(L);paint(e);sum()});
  return r;
}
function paint(e){
  var k=e.dataset.key,x=ld()[k]||{},r=row(e);if(!r)return;
  var last=x.s&&x.s.length?x.s[x.s.length-1]:0;
  r.querySelector('.eslst').innerHTML=x.n?('看過 <b>'+x.n+'</b> 輪・累計 <b>'+fmt(x.tot)+'</b>'+(last?'・上一輪 '+fmt(last):'')):'還沒有完整看完一輪（展開讀滿 20 秒並捲到這裡＝一輪）';
  [].forEach.call(r.querySelectorAll('button[data-v]'),function(b){b.classList.toggle('on',b.dataset.v===x.v)});
  var et=e.querySelector('summary .et');if(et){var i=et.querySelector('.eslv');if(!i){i=document.createElement('i');i.className='eslv';et.appendChild(i)}i.textContent=x.v?VI[x.v]:''}
}
function sum(){
  var L=ld(),n=0,rd=0,tot=0,c={ok:0,mem:0,hard:0};
  essays.forEach(function(e){var x=L[e.dataset.key];if(!x)return;if(x.n){n++;rd+=x.n;tot+=x.tot||0}if(x.v)c[x.v]++});
  var el=document.getElementById('eslSum');
  if(!el){var rc=document.getElementById('rcount');if(!rc)return;el=document.createElement('p');el.id='eslSum';rc.parentNode.insertBefore(el,rc.nextSibling)}
  el.textContent='看過至少一輪 '+n+'／'+essays.length+' 題・累計 '+rd+' 輪、'+Math.round(tot/60)+' 分鐘｜自評：✅ '+c.ok+'　📖 '+c.mem+'　😵 '+c.hard;
}
function bottomSeen(e){var d=e.querySelector('label.done')||e.querySelector('.esl');if(!d)return false;var b=d.getBoundingClientRect();return b.top<innerHeight&&b.bottom>0}
essays.forEach(function(e){paint(e);if(e.open)S[e.dataset.key]={sec:0,counted:false};e.addEventListener('toggle',function(){if(e.open){if(!S[e.dataset.key])S[e.dataset.key]={sec:0,counted:false}}else{flush(e);delete S[e.dataset.key]}})});
function flush(e){var st=S[e.dataset.key];if(!st||!st.sec)return;var L=ld(),x=L[e.dataset.key]=L[e.dataset.key]||{n:0,s:[],tot:0};x.tot=(x.tot||0)+st.sec;
  if(st.counted){x.s=(x.s||[]).concat([st.sec]).slice(-5)}x.t=Math.floor(Date.now()/1000);sv(L);st.sec=0;paint(e);sum()}
setInterval(function(){
  if(document.visibilityState!=='visible'||Date.now()-act>120000)return;
  essays.forEach(function(e){if(e.open&&!S[e.dataset.key])S[e.dataset.key]={sec:0,counted:false};var st=S[e.dataset.key];if(!st||!e.open||!e.offsetParent)return;st.sec+=1;st.all=(st.all||0)+1;
    if(!st.counted&&st.all>=20&&bottomSeen(e)){st.counted=true;var L=ld(),x=L[e.dataset.key]=L[e.dataset.key]||{n:0,s:[],tot:0};x.n=(x.n||0)+1;sv(L);flush(e)}});
},1000);
addEventListener('pagehide',function(){essays.forEach(function(e){if(e.open)flush(e)})});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='hidden')essays.forEach(function(e){if(e.open)flush(e)})});
sum();
})();
</script>'''

s = io.open(HUB, encoding='utf-8').read()
if 'id="esl-css"' in s:
    a = s.index('<style id="esl-css">'); b = s.index('</script>', s.index('<script id="esl-js">')) + len('</script>')
    s = s[:a] + BLOCK + s[b:]
else:
    i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i:]
io.open(HUB, 'w', encoding='utf-8').write(s)
print('申論輪數／用時／自評已寫入')
