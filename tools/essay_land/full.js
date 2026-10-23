
(function(){
var KEY="bx-es-read",R={};try{R=JSON.parse(localStorage.getItem(KEY)||"{}")||{}}catch(e){R={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(R))}catch(e){}}
var ES=[].slice.call(document.querySelectorAll(".es")),G=[].slice.call(document.querySelectorAll(".grp"));
var F={k:"",p:"",s:""};
// view tabs
document.addEventListener("click",function(e){var b=e.target.closest(".vtab button");if(!b)return;var body=b.closest(".ebody");body.querySelectorAll(":scope>.vtab button").forEach(function(x){x.classList.toggle("on",x===b)});body.querySelectorAll(":scope>.vp").forEach(function(p){p.hidden=p.dataset.v!==b.dataset.v})});
// read state
ES.forEach(function(es){var c=es.querySelector(".rd");c.checked=!!R[es.id];es.classList.toggle("read",c.checked);
 c.addEventListener("change",function(){if(c.checked)R[es.id]=1;else delete R[es.id];save();es.classList.toggle("read",c.checked);upd();if(F.k==="unread")apply()})});
function cnt(list){var o=0,oa=0,p=0,pa=0;list.forEach(function(es){var r=!!R[es.id];if(es.dataset.k==="pred"){pa++;if(r)p++}else{oa++;if(r)o++}});return{o:o,oa:oa,p:p,pa:pa}}
function pick(){var o=[["off","3"],["off","2"],["off","1"],["pred","3"],["pred","2"],["pred","1"]];for(var i=0;i<o.length;i++){var f=ES.filter(function(d){return d.dataset.k===o[i][0]&&d.dataset.pr===o[i][1]&&!R[d.id]})[0];if(f)return f}return null}
function upd(){G.forEach(function(g){var c=cnt([].slice.call(g.querySelectorAll(".es")));g.querySelector(".gread").textContent="已讀　官方 "+c.o+"／"+c.oa+(c.pa?"　預測／模擬 "+c.p+"／"+c.pa:"")});
 var A=ES.filter(function(d){return d.dataset.lv==="A"}),a=A.filter(function(d){return R[d.id]}).length,c=cnt(ES);
 document.getElementById("prgi").style.width=(A.length?a/A.length*100:0)+"%";
 document.getElementById("prgt").textContent="必考 "+a+"／"+A.length+"　官方 "+c.o+"／"+c.oa+"　預測／模擬 "+c.p+"／"+c.pa;
 var f=pick(),n=document.getElementById("now");
 if(!f){n.innerHTML="<small>下一題</small><b>全部題目都讀過了</b><small>可取消勾選重讀。</small>";return}
 var lv=f.querySelector(".lvp").textContent,ek=f.querySelector(".ek").textContent;
 n.innerHTML="<small>本週這題（每週一題，官方必考→高機率→參考→預測）</small><b>"+lv+"・"+ek+"　"+f.querySelector(".et").textContent+"</b><button type=\"button\" data-q=\""+f.id+"\">去讀這題</button>"}
// filters
function press(id,v){document.querySelectorAll("#"+id+" .fc").forEach(function(x){x.setAttribute("aria-pressed",x.dataset.f===v?"true":"false")})}
function apply(){press("fk",F.k);press("fp",F.p);var vis=0;
 ES.forEach(function(es){var h=(F.k==="off"&&es.dataset.k!=="off")||(F.k==="pred"&&(es.dataset.k!=="pred"||es.dataset.mk))||(F.k==="mock"&&!es.dataset.mk)||(F.k==="unread"&&!!R[es.id])||(F.p&&es.dataset.pr!==F.p)||(F.s&&es.dataset.tx.indexOf(F.s)<0);es.hidden=h;if(!h)vis++});
 var act=!!(F.k||F.p||F.s);
 G.forEach(function(g){var any=!!g.querySelector(".es:not([hidden])");g.hidden=!any;
  g.querySelectorAll(".sec").forEach(function(sc){var n=sc.nextElementSibling,ok=false;while(n&&!n.classList.contains("sec")){if(n.classList.contains("es")&&!n.hidden){ok=true;break}n=n.nextElementSibling}sc.hidden=!ok});
  var tp=g.querySelector(".topic");if(tp)tp.hidden=!g.querySelector(".es[id^='x-']:not([hidden])");
  if(act&&any)g.open=true});
 document.getElementById("nores").hidden=vis>0;
 document.getElementById("cnt").textContent=act?"符合 "+vis+" 題":"共 "+ES.length+" 題"}
document.getElementById("fk").addEventListener("click",function(e){var b=e.target.closest(".fc");if(b){F.k=b.dataset.f;apply()}});
document.getElementById("fp").addEventListener("click",function(e){var b=e.target.closest(".fc");if(b){F.p=b.dataset.f;apply()}});
document.getElementById("esq").addEventListener("input",function(){F.s=this.value.replace(/\s+/g,"").toLowerCase();apply();if(F.s)ES.forEach(function(d){if(!d.hidden)d.open=false})});
function reset(){F.k="";F.p="";F.s="";document.getElementById("esq").value="";apply()}
function go(el,open){if(!el)return;var g=el.closest(".grp");if(g)g.open=true;if(open)el.open=true;setTimeout(function(){el.scrollIntoView({behavior:"smooth",block:"start"});if(el.classList.contains("es")){el.classList.add("flash");setTimeout(function(){el.classList.remove("flash")},1500)}},60)}
document.addEventListener("click",function(e){
 var q=e.target.closest("[data-q]");if(q){var d=document.getElementById(q.dataset.q);if(!d)return;if(d.hidden)reset();go(d,true);return}
 var k=e.target.closest(".hk");if(k){go(document.getElementById("cat-"+k.dataset.cat),false);return}
 var t=e.target.closest("#tg button");if(t){var g=document.getElementById("cat-"+t.dataset.g);if(g.hidden)reset();go(g,false);return}
 var a=e.target.closest("[data-all]");if(a){var op=a.dataset.all==="open";G.forEach(function(g){g.open=op});if(!op)ES.forEach(function(d){d.open=false})}});
function gh(){var h=(location.hash||"").slice(1);if(!h)return;try{h=decodeURIComponent(h)}catch(e){}
 if(h==="off"||h==="pred"||h==="mock"){F.k=h;apply();return}
 if(h==="topic"){reset();go(document.getElementById("topic"),false);return}
 var d=document.getElementById(h);if(!d)return;if(d.hidden)reset();go(d,d.tagName==="DETAILS")}
upd();apply();gh();window.addEventListener("hashchange",gh);
})();
function ub(t){var b=document.getElementById("theme-btn");if(b)b.textContent=t==="dark"?"🌙":"☀️"}
function toggleTheme(){var h=document.documentElement,c=h.getAttribute("data-theme")||"light",n=c==="dark"?"light":"dark";h.setAttribute("data-theme",n);ub(n);try{localStorage.setItem("bx-theme",n)}catch(e){}}
ub(document.documentElement.getAttribute("data-theme")||"light");

/* lj-start */
(function(){var K="bx-land-ljv";function set(v,save){document.querySelectorAll(".ljseg button").forEach(function(b){b.classList.toggle("on",b.dataset.lj===v)});document.querySelectorAll(".ljp").forEach(function(p){p.hidden=p.dataset.lj!==v});if(save){try{localStorage.setItem(K,v)}catch(e){}}}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".ljseg button");if(b)set(b.dataset.lj,true)});
try{var v=localStorage.getItem(K);if(v&&/^[ABC]$/.test(v))set(v,false)}catch(e){}})();
/* lj-end */
