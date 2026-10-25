/* 考古題面板：讀共用紀錄 bxv-q2（只讀、不寫），依章篩選 A/B/C/D。
   用法：<div class="bxv-tq" data-chs="B,C1,C2" data-title="比較法・成本法"></div> ＋ <script src="bxv-topic-q.js"></script>
   題庫來自 bxv-quiz-data.js（由 tools/quiz_val/gen_data.py 自章節頁產生）。 */
(function(){
var css=".bxv-tq{margin:18px 0;border:1px solid var(--line,#ddd);border-radius:12px;background:var(--paper,#fff);color:var(--fg,#222);overflow:hidden;font-size:14px}"+
".bxv-tq *{box-sizing:border-box}.bxv-tq .th{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid var(--line,#ddd)}"+
".bxv-tq .th b{font-size:15px}.bxv-tq .th a{color:var(--primary,#2F5D50);font-weight:700;text-decoration:none;font-size:13px}"+
".bxv-tq .sm{padding:10px 14px;color:var(--muted,#777);font-size:13px;line-height:1.7}.bxv-tq .chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px}"+
".bxv-tq .chip{border:1px solid var(--line,#ccc);background:transparent;color:inherit;border-radius:999px;padding:4px 11px;font-size:12.5px;cursor:pointer;font-family:inherit}"+
".bxv-tq .chip.on{background:var(--primary,#2F5D50);border-color:var(--primary,#2F5D50);color:#fff}"+
".bxv-tq .ls{max-height:520px;overflow:auto;border-top:1px solid var(--line,#ddd)}.bxv-tq details{border-bottom:1px solid var(--line,#ddd)}"+
".bxv-tq summary{cursor:pointer;padding:9px 14px;display:flex;gap:8px;align-items:baseline;list-style:none}.bxv-tq summary::-webkit-details-marker{display:none}"+
".bxv-tq .yr{flex:none;color:var(--muted,#777);font-size:12px;min-width:62px}.bxv-tq .st{flex:none;font-size:12px;font-weight:700;min-width:34px}"+
".bxv-tq .st.x{color:#B33A2A}.bxv-tq .st.o{color:#2F7A4A}.bxv-tq .st.u{color:var(--muted,#999)}.bxv-tq .qt{min-width:0;line-height:1.55}"+
".bxv-tq .bd{padding:2px 14px 12px 14px;line-height:1.7}.bxv-tq .op{padding:2px 0}.bxv-tq .op.ok{color:#2F7A4A;font-weight:700}"+
".bxv-tq .nt{margin-top:6px;padding:7px 10px;border-radius:8px;background:var(--paper2,#f3f3f3);font-size:13px}.bxv-tq .em{padding:16px 14px;color:var(--muted,#777)}";
var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function esc(s){return String(s).replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c]})}
function init(){
 var Q=window.BXV_QUIZ;if(!Q)return;
 var wclr=+(function(){try{return localStorage.getItem("bxv-wclr")||0}catch(e){return 0}})()||0;
 document.querySelectorAll(".bxv-tq").forEach(function(box){
  var chs=(box.getAttribute("data-chs")||"").split(",").filter(Boolean),title=box.getAttribute("data-title")||chs.join("、");
  var items=Q.items.filter(function(q){return chs.indexOf(q.ch)>=0}).sort(function(a,b){return b.y-a.y||a.n-b.n});
  var D=ld("bxv-q2",{}),F="all";
  items.forEach(function(q){var r=D[q.ch+"-"+q.year+"-"+q.id];q._r=r||null;
   q._s=!r?"u":(r.ok===1?"o":"x");q._wrong=!!(r&&r.ok===0&&(r.t||0)>wclr);q._k=r?(r.k||""):""});
  var cnt={all:items.length,u:0,x:0,A:0,B:0,C:0,D:0,N:0};
  items.forEach(function(q){if(q._s==="u")cnt.u++;if(q._wrong){cnt.x++;if(q._k)cnt[q._k]++;else cnt.N++}else if(q._k==="D")cnt.D++});
  var done=items.length-cnt.u;
  var h='<div class="th"><b>🎯 考古題・'+esc(title)+'</b><a href="估價解析版練習.html#ch='+chs.join(",")+'">開始練這幾章 →</a></div>'+
   '<div class="sm">共 '+items.length+' 題，已練 '+done+' 題；目前錯題 '+cnt.x+'（A 法條混淆 '+cnt.A+'・B 粗心 '+cnt.B+'・C 不熟 '+cnt.C+'・D 猜對 '+cnt.D+'・未標 '+cnt.N+'）。紀錄與各刷題頁共用，此處只讀不寫。</div>'+
   '<div class="chips">'+[["all","全部"],["x","目前錯題"],["A","A 混淆"],["B","B 粗心"],["C","C 不熟"],["D","D 猜對"],["N","錯題未標"],["u","未練"]].map(function(a){return '<button class="chip'+(a[0]==="all"?" on":"")+'" data-f="'+a[0]+'">'+a[1]+' '+cnt[a[0]]+'</button>'}).join("")+'</div><div class="ls"></div>';
  box.innerHTML=h;
  var ls=box.querySelector(".ls");
  function match(q){return F==="all"||(F==="u"&&q._s==="u")||(F==="x"&&q._wrong)||(F==="N"&&q._wrong&&!q._k)||((F==="A"||F==="B"||F==="C")&&q._wrong&&q._k===F)||(F==="D"&&q._k==="D")}
  function draw(){
   var a=items.filter(match);
   if(!a.length){ls.innerHTML='<div class="em">這個條件下沒有題目。</div>';return}
   ls.innerHTML=a.map(function(q,i){
    var sl=q._s==="u"?"未練":(q._wrong?"✗"+(q._k&&q._k!=="D"?q._k:""):(q._k==="D"?"猜對":"✓"));
    var cls=q._s==="u"?"u":(q._wrong?"x":"o");
    var ops=q.opts.map(function(o,j){return '<div class="op'+(j===q.correct?' ok':'')+'">'+"ABCD"[j]+'. '+esc(o)+(j===q.correct?' ✔':'')+'</div>'}).join("");
    var ex=q.exps&&q.exps[q.correct]?'<div class="nt">解析：'+esc(q.exps[q.correct])+'</div>':'';
    var nt=q.note?'<div class="nt">⚠️ '+esc(q.note)+'</div>':'';
    return '<details><summary><span class="yr">'+esc(q.year)+'</span><span class="st '+cls+'">'+sl+'</span><span class="qt">'+esc(q.q)+'</span></summary><div class="bd">'+ops+ex+nt+'</div></details>'}).join("");
  }
  box.querySelector(".chips").addEventListener("click",function(e){var b=e.target.closest(".chip");if(!b)return;F=b.getAttribute("data-f");
   box.querySelectorAll(".chip").forEach(function(x){x.classList.toggle("on",x===b)});draw()});
  draw();
 });
}
if(window.BXV_QUIZ)init();else{var s=document.createElement("script");s.src="bxv-quiz-data.js";s.onload=init;document.head.appendChild(s)}
})();
