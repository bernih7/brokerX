/* bx-quiz-core.js — 土地法題庫頁共用程式（七頁共用；題目資料由各頁以 window.BX_CARDS 提供） */
(function(){
"use strict";
function bxTax(sec,so,all){var S={E1:["landvalue","地價稅"],E2:["zeng","土地增值稅"],F1:["house","房屋稅"],G1:["deed","契稅"],H1:["hehe","房地合一"],C3:["landvalue","地價稅（空地稅）"]},l=[];
 if(S[sec])l.push([S[sec][1],S[sec][0]]);
 [["地價稅|空地稅|累進起點","landvalue","地價稅"],["土地增值稅|土增稅|漲價總數額","zeng","土地增值稅"],["房屋稅","house","房屋稅"],["契稅","deed","契稅"],["房地合一","hehe","房地合一"]].forEach(function(a){if(new RegExp(a[0]).test(so)&&!l.some(function(x){return x[1]===a[1]}))l.push([a[2],a[1]])});
 if(l.length||/稅/.test(so))[["自用住宅","selfuse","自用住宅・一生一屋一生一次"],["免徵|減徵|不課徵|減半|免稅","relief","免徵・減徵・不課徵"],["滯納|怠報|匿報|短報|罰鍰","penalty","罰則"],["納稅義務人|申報|期限|繳納","payer","義務人・期限・稽徵機關"]].forEach(function(a){if(new RegExp(a[0]).test(all)&&!l.some(function(x){return x[1]===a[1]}))l.push([a[2],a[1]])});
 if(!l.length)return "";
 return '<div class="bxtl" style="margin-top:8px">'+l.slice(0,3).map(function(a){return '<a target="_blank" rel="noopener" href="土地法_稅率總表.html#'+a[1]+'" style="display:inline-block;margin:2px 6px 2px 0;padding:2px 11px;border:1px solid #B8782E;border-radius:99px;color:#8A5517;background:#FBF1D9;text-decoration:none;font-size:13px;font-weight:700">💰 稅務總表：'+a[0]+' →</a>'}).join("")+'</div>'}


var CARDS=window.BX_CARDS||[],ALL=window.BX_ALL||[];
CARDS.forEach(function(c){if(!c.chName){c.chName=c.ch;c.ch=String(c.ch).slice(0,2)}c.id=c.ch+"-"+c.year+"-"+c.num});
function g(id){return document.getElementById(id)}
function ld(k,d){try{var v=localStorage.getItem(k);return v==null?d:JSON.parse(v)}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true}catch(e){return false}}
var DB=ld("bx-q2",{}),TGT=ld("bx-tgt",{p:60,g:70}),STF="all";
Object.keys(DB).forEach(function(i){var r=DB[i];if(r){if(r.g&&!r.k)r.k="D";r.g=r.k==="D"?1:0}});
function save(){sv("bx-q2",DB)}
var KN={A:"A 法條混淆",B:"B 粗心",C:"C 不熟",D:"D 猜的"};
var CHS=[];CARDS.forEach(function(c){if(CHS.indexOf(c.chName)<0)CHS.push(c.chName)});
var sel={};CHS.forEach(function(c){sel[c]=1});
var ans={};
/* ---------- 章節篩選 ---------- */
function renderPills(){var p=g("pills");p.innerHTML="";CHS.forEach(function(ch){var b=document.createElement("button");b.className="pill"+(sel[ch]?" on":"");b.textContent=ch;b.onclick=function(){sel[ch]=sel[ch]?0:1;renderPills();renderList()};p.appendChild(b)})}
function selAll(){Object.keys(sel).forEach(function(k){sel[k]=1});renderPills();renderList()}
function selNone(){Object.keys(sel).forEach(function(k){sel[k]=0});renderPills();renderList()}
function resetAll(){if(!confirm("只清掉「這一次」的作答畫面，累積紀錄不會刪。確定？"))return;ans={};renderList()}
/* ---------- 順序 ---------- */
var BXO="new";try{BXO=localStorage.getItem("bx-ord")||"new"}catch(e){}
var BXR=new Map();function bxShuffle(){BXR=new Map();CARDS.forEach(function(c){BXR.set(c,Math.random())})}bxShuffle();
function bxOrd(v){if(BXO==="new")return v.slice().sort(function(a,b){return(+b.year)-(+a.year)||(+a.num)-(+b.num)});if(BXO==="rand")return v.slice().sort(function(a,b){return BXR.get(a)-BXR.get(b)});return v}
/* ---------- 狀態篩選 ---------- */
function stOk(c){var r=DB[c.id];switch(STF){case"new":return!r;case"wrong":return!!r&&!r.ok;case"D":return!!r&&r.k==="D";case"A":case"B":case"C":return!!r&&!r.ok&&r.k===STF;case"nocat":return!!r&&!r.ok&&!r.k;default:return true}}
function bxBar(){var L=g("list");if(!L||g("ords"))return;
 L.insertAdjacentHTML("beforebegin",'<div class="ords" id="stf">狀態<button data-s="all">全部</button><button data-s="new">未作答</button><button data-s="wrong">答錯</button><button data-s="A">A 混淆</button><button data-s="B">B 粗心</button><button data-s="C">C 不熟</button><button data-s="D">D 猜的</button><button data-s="nocat">未分類</button></div><div class="ords" id="ords">題目順序<button data-o="new">年份新→舊</button><button data-o="rand">隨機</button><button data-o="ch">章節順序</button><button class="sh" id="shuf">重新洗牌</button></div>');
 function mark(){[].forEach.call(document.querySelectorAll("#ords button[data-o]"),function(b){b.className=b.dataset.o===BXO?"on":""});g("shuf").style.display=BXO==="rand"?"":"none";[].forEach.call(document.querySelectorAll("#stf button[data-s]"),function(b){b.className=b.dataset.s===STF?"on":""})}
 [].forEach.call(document.querySelectorAll("#ords button[data-o]"),function(b){b.onclick=function(){BXO=b.dataset.o;try{localStorage.setItem("bx-ord",BXO)}catch(e){}if(BXO==="rand")bxShuffle();mark();renderList();window.scrollTo({top:0})}});
 [].forEach.call(document.querySelectorAll("#stf button[data-s]"),function(b){b.onclick=function(){STF=b.dataset.s;mark();renderList();window.scrollTo({top:0})}});
 g("shuf").onclick=function(){bxShuffle();renderList();window.scrollTo({top:0})};mark();window.__bxMark=mark}
/* ---------- 清單與題卡 ---------- */
function renderList(){bxBar();if(window.__bxMark)window.__bxMark();var list=g("list");list.innerHTML="";
 var vis=bxOrd(CARDS.filter(function(c){return sel[c.chName]&&stOk(c)})),last="";
 if(!vis.length)list.innerHTML='<div class="empty">這個條件下沒有題目。</div>';
 vis.forEach(function(card){var idx=CARDS.indexOf(card);var hk=BXO==="rand"?"":(BXO==="ch"?card.chName:card.year+" 年");
  if(hk&&hk!==last){var h=document.createElement("div");h.className=BXO==="ch"?"ch-header":"yr-header";h.textContent=hk;list.appendChild(h);last=hk}
  list.appendChild(makeCard(card,idx))});
 updateProg()}
function histTxt(card){var r=DB[card.id];if(!r)return"";return r.ok?(r.k==="D"?"上次猜對":"上次答對"):("上次答錯"+(r.k?"・"+KN[r.k]:""))}
function clsHtml(card){var r=DB[card.id]||{};var ks=r.ok?["D"]:["A","B","C","D"];return '<span class="cl">'+(r.ok?"答對了，如果是亂猜的":"這題錯在")+'</span>'+ks.map(function(k){return '<button type="button" data-k="'+k+'" class="'+(r.k===k?"on":"")+'">'+KN[k]+"</button>"}).join("")}
function makeCard(card,idx){var a=ans[idx],ht=histTxt(card);var div=document.createElement("div");div.className="qcard"+(a?(a.ok?" answered-ok":" answered-ng"):"");div.id="c"+idx;
 div.innerHTML='<div class="qmeta"><span>【'+card.year+"年第"+card.num+"題】"+(ht?'<em class="hist">'+ht+"</em>":"")+'</span><span class="qtag">'+card.chName+'</span></div><div class="qtext">'+card.q+"</div>";
 var opts=document.createElement("div");opts.className="opts";
 ["A","B","C","D"].forEach(function(l,i){var b=document.createElement("button");b.className="opt";b.innerHTML='<span class="ltr">'+l+"</span><span>"+card.opts[i]+"</span>";
  if(a){b.disabled=true;if(i===card.ans)b.classList.add("show-correct");if(i===a.chosen&&!a.ok)b.classList.add("ng")}else b.onclick=function(){pick(idx,i)};opts.appendChild(b)});
 div.appendChild(opts);
 var eb=document.createElement("div");eb.className="expbox"+(a?" show":"");eb.id="e"+idx;eb.innerHTML='<div class="exph">&#128218; 逐選項解析</div><div class="expb" id="eb'+idx+'">'+(a?buildExp(card,a.chosen,a.ok):"")+"</div>";div.appendChild(eb);
 if(a&&!a.ok)div.insertAdjacentHTML("beforeend",'<div class="cls">'+clsHtml(card)+"</div>");
 if(a&&a.ok)div.insertAdjacentHTML("beforeend",'<div class="cls">'+clsHtml(card)+"</div>");
 return div}
function buildExp(card,chosen,ok){var h='<div style="margin-bottom:7px;"><span class="verdict '+(ok?"ok":"ng")+'">'+(ok?"答對了":"答錯了")+"</span></div>";
 ["A","B","C","D"].forEach(function(l,i){var ec=i===card.ans?"ok":(i===chosen&&!ok?"ng":"no");h+='<div class="ei"><span class="el '+ec+'">'+l+"</span><span>"+(card.exps[i]||"")+"</span></div>"});return h}
function pick(idx,chosen){var card=CARDS[idx],ok=chosen===card.ans;ans[idx]={chosen:chosen,ok:ok};
 var r=DB[card.id]||{n:0,w:0,h:[]};r.c=chosen;r.ok=ok?1:0;r.g=0;r.k="";r.t=Math.floor(Date.now()/1000);r.n=(r.n||0)+1;if(!ok)r.w=(r.w||0)+1;(r.h=r.h||[]).push([r.t,r.ok,0]);if(r.h.length>10)r.h.shift();DB[card.id]=r;save();
 var div=g("c"+idx);div.className="qcard"+(ok?" answered-ok":" answered-ng");
 div.querySelectorAll(".opt").forEach(function(b,i){b.disabled=true;b.onclick=null;if(i===card.ans)b.classList.add("show-correct");if(i===chosen&&!ok)b.classList.add("ng")});
 g("eb"+idx).innerHTML=buildExp(card,chosen,ok);g("e"+idx).classList.add("show");
 div.insertAdjacentHTML("beforeend",'<div class="cls">'+clsHtml(card)+"</div>");
 updateProg()}
/* ---------- 進度面板 ---------- */
function stat(list){var s={t:list.length,sure:0,gok:0,wr:0};list.forEach(function(c){var r=DB[c.id];if(!r)return;if(r.ok){r.k==="D"?s.gok++:s.sure++}else s.wr++});s.done=s.sure+s.gok+s.wr;s.ok=s.sure+s.gok;return s}
function pc(a,b){return b?Math.round(a/b*100):0}
function updateProg(){var vis=CARDS.filter(function(c){return sel[c.chName]}),s=stat(vis),T=s.t||1;
 g("pbS").style.width=s.sure/T*100+"%";g("pbG").style.width=s.gok/T*100+"%";g("pbN").style.width=s.wr/T*100+"%";
 g("lnP").style.left=TGT.p+"%";g("lnG").style.left=TGT.g+"%";g("lnP").dataset.v=TGT.p;g("lnG").dataset.v=TGT.g;
 var acc=s.done?pc(s.ok,s.done)+"%":"-";
 var need=function(p){return Math.max(0,Math.ceil(s.t*p/100)-s.ok)};
 g("ptxt").innerHTML='累積 <b>'+s.done+"</b>/<b>"+s.t+"</b> 題・目前正確率 <b>"+acc+"</b>"+(s.done?"（答對 "+s.ok+"，其中猜對 "+s.gok+"；答錯 "+s.wr+"）":"")+
  '<div class="pgoal">及格線 '+TGT.p+"%："+(need(TGT.p)?"還差 <b>"+need(TGT.p)+"</b> 題答對":"已達")+"　目標 "+TGT.g+"%："+(need(TGT.g)?"還差 <b>"+need(TGT.g)+"</b> 題答對":"已達")+"</div>";
 var rows=CHS.filter(function(c){return sel[c]}).map(function(ch){var cs=stat(CARDS.filter(function(c){return c.chName===ch})),a=cs.done?pc(cs.ok,cs.done):null,cl=a==null?"":(a<TGT.p?"lo":(a<TGT.g?"mid":"hi"));
  return '<div class="pch"><span class="n">'+ch+'</span><span class="v '+cl+'">'+(a==null?"未作答":a+"%")+'</span><span class="d">'+cs.ok+"/"+cs.done+" 答對・共 "+cs.t+" 題</span></div>"});
 g("pchs").innerHTML=rows.join("");
 var cat={A:0,B:0,C:0,D:0,n:0};vis.forEach(function(c){var r=DB[c.id];if(!r)return;if(r.k==="D")cat.D++;else if(!r.ok){if(r.k)cat[r.k]++;else cat.n++}});
 g("pcat").textContent=(s.wr||cat.D?"原因　A 混淆 "+cat.A+"・B 粗心 "+cat.B+"・C 不熟 "+cat.C+"・D 猜的 "+cat.D+(cat.n?"・未分類 "+cat.n:""):"")}
/* ---------- 回報與匯入 ---------- */
function b64e(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))))}
function b64d(s){return JSON.parse(decodeURIComponent(escape(atob(s))))}
function pad(n){return n<10?"0"+n:""+n}
function now(){var d=new Date();return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())+" "+pad(d.getHours())+":"+pad(d.getMinutes())}
function report(){if(window.BXREP)return BXREP.build();
 var ids=Object.keys(DB),by={},tot={sure:0,gok:0,wr:0},cat={A:0,B:0,C:0,D:0,n:0},lastRep=ld("bx-lastrep",0),fresh=0;
 ids.forEach(function(id){var r=DB[id],ch=id.split("-")[0];var o=by[ch]=by[ch]||{sure:0,gok:0,wr:0};if(r.ok){r.k==="D"?(o.gok++,tot.gok++,cat.D++):(o.sure++,tot.sure++)}else{o.wr++;tot.wr++;if(r.k)cat[r.k]++;else cat.n++}if(r.t>lastRep)fresh++});
 var total=ALL.reduce(function(a,c){return a+c.total},0),done=tot.sure+tot.gok+tot.wr,ok=tot.sure+tot.gok;
 var L=["【土地法練習回報】"+now(),"整體：已作答 "+done+"／共 "+total+" 題｜答對 "+ok+"（確定 "+tot.sure+"、猜對 "+tot.gok+"）｜答錯 "+tot.wr+"｜正確率 "+(done?pc(ok,done)+"%":"-")+"｜及格線 "+TGT.p+"%・目標 "+TGT.g+"%","自上次回報新增：作答 "+fresh+" 題","範圍：土地法題庫七頁（A1A2／A3A4A5／B／C／D／E／FGHI）合併，共 "+total+" 題；同一裝置同一瀏覽器七頁共用一份紀錄，所以不論從哪一頁按「複製練習回報」，內容都涵蓋七頁，不需要每頁各貼一份。","未涵蓋：「土地法互動練習」「土地法解析版練習」目前沒有紀錄功能。","按回報的頁面："+(document.title||location.pathname),"","── 各頁 ──"];
 var PG=[],pm={};ALL.forEach(function(c){var o=pm[c.page];if(!o){o=pm[c.page]={page:c.page,total:0,done:0,ok:0,wr:0};PG.push(o)}o.total+=c.total;var x=by[c.ch];if(x){o.done+=x.sure+x.gok+x.wr;o.ok+=x.sure+x.gok;o.wr+=x.wr}});
 PG.forEach(function(o){L.push("LandLaw_"+o.page+"：已答 "+o.done+"／"+o.total+(o.done?"｜答對 "+o.ok+"｜答錯 "+o.wr+"｜"+pc(o.ok,o.done)+"%":"｜未作答")+"（達成 "+pc(o.done,o.total)+"%）")});L.push("","── 各章 ──");
 ALL.forEach(function(c){var o=by[c.ch];if(!o){L.push(c.name+"：未作答（共 "+c.total+" 題）");return}var d=o.sure+o.gok+o.wr;L.push(c.name+"：已答 "+d+"／"+c.total+"｜答對 "+(o.sure+o.gok)+"（猜對 "+o.gok+"）答錯 "+o.wr+"｜"+pc(o.sure+o.gok,d)+"%")});
 L.push("","── 錯題原因 ──","A 法條混淆 "+cat.A+"｜B 粗心 "+cat.B+"｜C 不熟 "+cat.C+"｜D 猜的 "+cat.D+"｜未分類 "+cat.n);
 var wr=ids.filter(function(i){return!DB[i].ok}).sort(function(a,b){return(DB[b].w||0)-(DB[a].w||0)||DB[b].t-DB[a].t}).slice(0,40);
 L.push("","── 答錯題（錯得多的在前，最多 40 題）──");wr.forEach(function(i){var r=DB[i];L.push(i+"　錯 "+(r.w||1)+" 次"+(r.k?"・"+KN[r.k]:"・未分類"))});
 var gu=ids.filter(function(i){return DB[i].ok&&DB[i].k==="D"}).slice(0,40);if(gu.length){L.push("","── 猜對（待加強）──",gu.join("、"))}
 var data={};ids.forEach(function(i){var r=DB[i];data[i]=[r.c,r.ok,r.k==="D"?1:0,r.k||"",r.t,r.n||1,r.w||0]});
 L.push("","BXDATA1:"+b64e(data));return L.join("\n")}
function importText(t){var m=/BXDATA1:([A-Za-z0-9+\/=]+)/.exec(t);if(!m)return"找不到 BXDATA1 資料，請把整段回報貼上。";var d;try{d=b64d(m[1])}catch(e){return"資料格式錯誤，無法讀取。"}var n=0,u=0;
 Object.keys(d).forEach(function(id){var a=d[id],o=DB[id];var rec={c:a[0],ok:a[1],g:a[2],k:a[3]||(a[2]?"D":""),t:a[4],n:a[5],w:a[6],h:(o&&o.h)||[]};if(!o||rec.t>o.t){if(o){rec.n=Math.max(rec.n,o.n||0);rec.w=Math.max(rec.w,o.w||0)}DB[id]=rec;u++}n++});save();renderList();return"已讀入 "+n+" 題紀錄，其中 "+u+" 題比本機新而更新。"}
/* ---------- 對話框 ---------- */
function modal(title,txt,okLabel,onok,link){var m=g("bxm");g("bxlink").style.display=link?"":"none";g("bxmt").textContent=title;var ta=g("bxta");ta.value=txt||"";g("bxok").textContent=okLabel||"";g("bxok").style.display=okLabel?"":"none";g("bxmsg").textContent="";m.classList.add("on");g("bxok").onclick=function(){onok&&onok(ta.value)};setTimeout(function(){ta.focus();if(txt)ta.select()},30)}
function copyReport(){var t=report();var done=function(ok){modal(ok?"已複製到剪貼簿，貼到【總控】對話裡即可":"請全選後自行複製，再貼到【總控】對話",t,"",null,true);try{sv("bx-lastrep",Math.floor(Date.now()/1000))}catch(e){}};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){done(true)},function(){done(false)})}else done(false)}
function bindTools(){g("bSelAll").onclick=selAll;g("bSelNone").onclick=selNone;g("bReset").onclick=resetAll;
 g("bRep").onclick=copyReport;
 g("bImp").onclick=function(){modal("匯入：把練習回報整段貼上","","匯入",function(v){g("bxmsg").textContent=importText(v)})};
 g("bTgt").onclick=function(){var p=prompt("及格線（%）",TGT.p);if(p===null)return;var q=prompt("目標（%，要比及格線高一點）",TGT.g);if(q===null)return;p=+p;q=+q;if(p>0&&p<=100&&q>0&&q<=100){TGT={p:p,g:q};sv("bx-tgt",TGT);updateProg()}};
 g("bClr").onclick=function(){if(confirm("要清除這台裝置上「全部」累積紀錄嗎？無法復原。（若要保留，請先按「複製練習回報」）")){DB={};save();ans={};renderList()}};
 g("bxcl").onclick=function(){g("bxm").classList.remove("on")};
 document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("button[data-k]");if(!b)return;var q=b.closest(".qcard");if(!q)return;var card=CARDS[+q.id.slice(1)],r=DB[card.id];if(!r)return;r.k=r.k===b.dataset.k?"":b.dataset.k;r.g=r.k==="D"?1:0;save();[].forEach.call(q.querySelectorAll("button[data-k]"),function(x){x.classList.toggle("on",x.dataset.k===r.k)});updateProg()})}
bindTools();renderPills();renderList();
(function(){
var EX="D";try{EX=localStorage.getItem("bx-ex2")||"D"}catch(e){}
function applyOpen(cc){[].forEach.call(cc.querySelectorAll(".opt"),function(o){o.classList.toggle("open",EX==="C"&&(o.classList.contains("ok")||o.classList.contains("show-correct")||o.classList.contains("ng")))})}
function setEx(m){EX=m;document.body.dataset.ex=m;[].forEach.call(document.querySelectorAll(".qcard.done"),applyOpen);try{localStorage.setItem("bx-ex2",m)}catch(e){}[].forEach.call(document.querySelectorAll(".exs button[data-m]"),function(b){b.className=b.dataset.m===m?"on":""})}
function dec(div){if(div.dataset.dec||!/answered-(ok|ng)/.test(div.className))return;var m=(div.id||"").match(/(\d+)$/);if(!m||typeof CARDS==="undefined")return;var c=CARDS[+m[1]];if(!c)return;
 div.dataset.dec="1";div.classList.add("done");var ok=div.classList.contains("answered-ok"),L="ABCD",chosen=-1;
 var os=div.querySelectorAll(".opt");[].forEach.call(os,function(o,i){if(o.classList.contains("ng"))chosen=i});
 [].forEach.call(os,function(o,i){var tx=o.children[1];if(!tx)return;tx.className="ob";tx.insertAdjacentHTML("beforeend",'<span class="bg a">正解</span><span class="bg p">你選的</span><span class="arr">▾</span><div class="nt"></div>');tx.querySelector(".nt").innerHTML=(c.exps&&c.exps[i])||"";
  o.addEventListener("click",function(){if(div.classList.contains("done")&&(EX==="C"||EX==="D"))o.classList.toggle("open")})});
 var ob=div.querySelector(".opts");ob.insertAdjacentHTML("beforebegin",'<div class="res'+(ok?" ok":"")+'">'+(ok?"答對了":"答錯了")+"　正解 "+L[c.ans]+(ok||chosen<0?"":"（你選 "+L[chosen]+"）")+'</div><div class="hn">點每個選項可展開／收合說明；上方「全部展開」一次看完</div>');
 var so=(c.q||"")+(c.opts||[]).join("");var tl=typeof bxTax==="function"?bxTax(String(c.ch||"").slice(0,2),so,so+(c.exps||[]).join("")):"";if(tl)div.insertAdjacentHTML("beforeend",'<div class="tl">'+tl+"</div>");
 applyOpen(div)}
function scan(){[].forEach.call(document.querySelectorAll(".qcard"),dec)}
function init(){var L=document.getElementById("list")||document.getElementById("questionList");if(!L)return;
 L.insertAdjacentHTML("beforebegin",'<div class="exs">解析樣式<button data-m="B">分離式</button><button data-m="C">摺疊式</button><button data-m="D">結論優先</button><button class="ea" id="ea">全部展開</button></div>');
 [].forEach.call(document.querySelectorAll(".exs button[data-m]"),function(b){b.onclick=function(){setEx(b.dataset.m)}});
 document.getElementById("ea").onclick=function(){var on=document.body.classList.toggle("allopen");this.textContent=on?"全部收合":"全部展開"};
 setEx(EX);new MutationObserver(scan).observe(L,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});scan()}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init()})();

})();
