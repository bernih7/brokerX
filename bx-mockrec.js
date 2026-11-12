/* bx-mockrec.js — 四科模擬卷共用：每題熟練度＋每份卷歷次紀錄＋錯題複習卷連結
   熟練度（localStorage bx_drill_<科>）：{題號:{c:答對次數,w:答錯次數,s:最近連續答對,h:"10110",t:時間}}
   放過：從沒錯過且答對 1 次；或錯過後連續答對 3 次。
   每份卷：bx_att_<卷>＝本次作答 {題號:[對錯,歸類]}；bx_atth_<卷>＝歷次紀錄（最多 20 次）。 */
(function(){
var SUBJ={land:"土地法",civ:"民法",jj:"經紀法規",val:"估價"};
var DRILL={land:"土地法_錯題複習卷.html",civ:"民法_錯題複習卷.html",jj:"經紀法規_錯題複習卷.html",val:"估價_錯題複習卷.html"};
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function done(r){return !!r&&(r.w?r.s>=3:r.c>=1)}
function state(r){return !r?"new":done(r)?"done":"todo"}
var mounts=[];
var B={
 done:done,state:state,SUBJ:SUBJ,DRILL:DRILL,
 all:function(S){return ld("bx_drill_"+S,{})},
 get:function(S,id){return B.all(S)[id]},
 /* 記一題：S 科目、id 題目代碼、ok 對錯 */
 rec:function(S,id,ok){var a=B.all(S),r=a[id]||{c:0,w:0,s:0,h:""};
  if(ok){r.c++;r.s++}else{r.w++;r.s=0}r.h=(r.h+(ok?"1":"0")).slice(-12);r.t=Date.now();a[id]=r;sv("bx_drill_"+S,a);return r},
 /* 模擬卷作答：pid 卷代碼、n 題號 */
 ans:function(S,pid,n,ok,cls){B.rec(S,pid+"-"+n,ok);var c=ld("bx_att_"+pid,{});c[n]=[ok?1:0,cls||""];c._t=Date.now();sv("bx_att_"+pid,c);B.paint()},
 cls:function(pid,n,k){var c=ld("bx_att_"+pid,{});if(c[n]){c[n][1]=k;sv("bx_att_"+pid,c)}},
 hist:function(pid){return ld("bx_atth_"+pid,[])},
 /* 把本次作答存進歷次紀錄並清空 */
 reset:function(pid,N){var c=ld("bx_att_"+pid,null);try{localStorage.removeItem("bx_att_"+pid)}catch(e){}
  if(!c)return;var a=0,ok=0,w=[];Object.keys(c).forEach(function(k){if(k==="_t")return;a++;if(c[k][0])ok++;else w.push([+k||k,c[k][1]||""])});
  if(!a)return;var h=B.hist(pid);h.push({t:c._t||Date.now(),a:a,c:ok,n:N||a,w:w});sv("bx_atth_"+pid,h.slice(-20));B.paint()},
 /* 開頁：上次沒按重做就離開的作答，先存成一次紀錄 */
 boot:function(pid,N){B.reset(pid,N)},
 /* 在 host 放「歷次紀錄」卡；secOf(n) 回傳題目小標 */
 mount:function(S,pid,host,N,secOf,onReset){if(!host)return;var d=document.createElement("div");d.className="bxd-card";host.appendChild(d);
  mounts.push({S:S,pid:pid,el:d,N:N,secOf:secOf,onReset:onReset});B.css();B.paint()},
 paint:function(){mounts.forEach(function(m){if(!document.body.contains(m.el))return;var H=B.hist(m.pid),cur=ld("bx_att_"+m.pid,{}),a=B.all(m.S);
  var st={done:0,todo:0,"new":0};for(var i=1;i<=(m.N||0);i++)st[state(a[m.pid+"-"+i])]++;
  var h='<div class="bxd-h">本卷歷次紀錄</div><div class="bxd-s">本卷 '+m.N+' 題：<b class="ok">放過 '+st.done+'</b>｜<b class="ng">還要練 '+st.todo+'</b>｜沒做過 '+st["new"]+
   '<span class="bxd-rule">（第一次就答對＝放過；答錯過的要連續答對 3 次）</span></div>'+
   '<a class="bxd-go" href="'+DRILL[m.S]+'">▶ 去'+SUBJ[m.S]+'錯題複習卷（錯題＋新題混合）</a>'+(m.onReset?' <button class="bxd-go bxd-rs" type="button">↺ 重做本卷（這次存入紀錄）</button>':'');
  if(!H.length)h+='<div class="bxd-s">還沒有完成的紀錄。按「重做」或下次再開本卷時，這次作答會自動存成一筆。</div>';
  H.slice().reverse().forEach(function(r,i){var t=new Date(r.t);
   h+='<div class="bxd-r"><b>第'+(H.length-i)+'次｜'+(t.getMonth()+1)+'/'+t.getDate()+'｜答對 '+r.c+'/'+r.n+(r.a<r.n?'（只答 '+r.a+' 題）':'')+(r.note?'｜'+r.note:'')+'</b>';
   r.w.slice().sort(function(x,y){return x[0]-y[0]}).forEach(function(x){var q=a[m.pid+"-"+x[0]],nowc=cur[x[0]];
    h+='<div class="bxd-w">第'+x[0]+'題'+(m.secOf?'｜'+(m.secOf(x[0])||''):'')+(x[1]?'｜'+x[1]+'型':'')+
     (nowc?(nowc[0]?'｜<span class="ok">✅ 這次答對</span>':'｜<span class="ng">❌ 這次又錯</span>'):'')+
     (q?(done(q)?'｜<span class="ok">已放過</span>':'｜連對 '+q.s+'/3'):'')+'</div>'});
   h+='</div>'});
  m.el.innerHTML=h;var rb=m.el.querySelector('.bxd-rs');if(rb)rb.onclick=function(){B.reset(m.pid,m.N);m.onReset()}})},
 css:function(){if(document.getElementById("bxd-css"))return;var s=document.createElement("style");s.id="bxd-css";
  s.textContent=".bxd-card{margin:14px 0;padding:14px 16px;border:1px solid rgba(128,128,128,.35);border-radius:12px;background:var(--card,var(--paper,transparent));line-height:1.7}"+
  ".bxd-h{font-weight:700;font-size:1.05em;margin-bottom:4px}.bxd-s{font-size:.92em;opacity:.85;margin:4px 0}.bxd-rule{display:block;font-size:.88em;opacity:.8}"+
  ".bxd-go{display:inline-block;background:none;font:inherit;cursor:pointer;margin:8px 0 4px;padding:6px 12px;border-radius:8px;border:1px solid currentColor;text-decoration:none;font-weight:700;color:inherit}"+
  ".bxd-r{margin:10px 0 0;padding-top:8px;border-top:1px dashed rgba(128,128,128,.35)}.bxd-w{font-size:.92em;margin:2px 0 0 4px;opacity:.9}"+
  ".bxd-card .ok{color:#3d7a4a}.bxd-card .ng{color:#b0402e}@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .bxd-card .ok{color:#8fcf9b}:root:not([data-theme=light]) .bxd-card .ng{color:#f0957f}}:root[data-theme=dark] .bxd-card .ok{color:#8fcf9b}:root[data-theme=dark] .bxd-card .ng{color:#f0957f}";
  document.head.appendChild(s)}
};
window.BXMR=B;
})();
