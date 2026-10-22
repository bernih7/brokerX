/* bxm-use.js：民法全站共用——①補上 window.storage（GitHub Pages 沒有，13 頁原本存不下進度）②自動記錄每頁開啟次數與停留時間與每日刷題數 ③全站回報產生器 ④刷題頁寫入共用作答紀錄。不連任何外部服務，資料只在本瀏覽器。 */
(function(){
var SUBJ="民法";
var CH={"A":["A","A 民法總則",107],"B":["B","B 債編總論",85],"C":["C","C 債編分則",77],"D":["D","D 物權",134],"E":["E","E 親屬與繼承",117]};
var PAGES=[["民法_數字期間速查","數字期間速查"],["民法_用詞分類與申論必背","用詞分類・申論必背"],["民法刷題練習_A篇","刷題 A 篇"],["民法刷題練習_B篇","刷題 B 篇"],["民法刷題練習_C篇","刷題 C 篇"],["民法刷題練習_D篇","刷題 D 篇"],["民法刷題練習_E篇","刷題 E 篇"],["民法概要_25題模擬測驗","25題模擬測驗"],["民法A_考題小卡","A 精選小卡"],["民法BC_考題小卡","BC 精選小卡"],["民法D_考題小卡","D 精選小卡"],["民法E_考題小卡","E 精選小卡"],["民法A_完整考題小卡","A 完整小卡"],["民法BC_完整考題小卡","BC 完整小卡"],["民法D_完整考題小卡","D 完整小卡"],["民法E_完整考題小卡","E 完整小卡"],["民法A_互動單字卡","A 單字卡"],["民法BC_互動單字卡","BC 單字卡"],["民法D_互動單字卡","D 單字卡"],["民法E_互動單字卡","E 單字卡"],["民法A_彩色重點速記","A 彩色速記"],["民法BC_彩色重點速記","BC 彩色速記"],["民法D_彩色重點速記","D 彩色速記"],["民法E_彩色重點速記","E 彩色速記"],["民法_定義填空練習","定義填空練習"],["民法_模擬試題一","自擬模擬卷①"],["民法_模擬試題二","自擬模擬卷②"],["民法_申論115出題預測","申論115預測"],["民法_申論專練卷","申論專練卷①"],["民法_來勝模擬試題一","來勝模擬(一)"],["民法_法律效果總整理","法律效果總整理"],["民法申論題_五型答題模板","申論五型模板"],["民法_備考指揮中心","備考指揮中心"]];
var TOT={fill:147,sel:74,full:520,word:172};
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function pad(n){return n<10?"0"+n:""+n}
function ymd(d){d=d||new Date();return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())}
function now(){var d=new Date();return ymd(d)+" "+pad(d.getHours())+":"+pad(d.getMinutes())}
function pc(a,b){return b?Math.round(a/b*100):0}
function b64e(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))))}
function day(f,n){var D=ld("bxm-day",{}),k=ymd(),x=D[k]=D[k]||{q:0,c:0};x[f]=(x[f]||0)+n;
 var ks=Object.keys(D).sort();while(ks.length>60)delete D[ks.shift()];sv("bxm-day",D)}
/* ---- ① window.storage 補強（Claude 預覽內建；GitHub Pages 沒有） ---- */
if(typeof window.storage==="undefined"){
 window.storage={
  get:function(k){return Promise.resolve().then(function(){var v=localStorage.getItem("bxm-st:"+k);return v==null?null:{key:k,value:v}})},
  set:function(k,v){return Promise.resolve().then(function(){var old=null,nw=null;try{old=JSON.parse(localStorage.getItem("bxm-st:"+k)||"null")}catch(e){}
   localStorage.setItem("bxm-st:"+k,v);
   try{nw=JSON.parse(v)}catch(e){}
   if(nw&&typeof nw==="object"){var n=0;Object.keys(nw).forEach(function(id){if(JSON.stringify((old||{})[id])!==JSON.stringify(nw[id]))n++});if(n)day("c",n)}
   return {key:k,value:v}})},
  delete:function(k){return Promise.resolve().then(function(){localStorage.removeItem("bxm-st:"+k);return {key:k,deleted:true}})}
 }}
var PAGE=decodeURIComponent((location.pathname.split("/").pop()||"index.html")).replace(/\.html$/,"");
/* ---- ② 使用追蹤 ---- */
var known=PAGES.some(function(p){return p[0]===PAGE});
if(known){var U=ld("bxm-use",{});var u=U[PAGE]=U[PAGE]||{n:0,s:0,t:0};u.n++;u.t=Math.floor(Date.now()/1000);sv("bxm-use",U);
 var act=Date.now(),acc=0;["pointerdown","keydown","scroll","touchstart"].forEach(function(ev){addEventListener(ev,function(){act=Date.now()},{passive:true})});
 var flush=function(){var U2=ld("bxm-use",{}),x=U2[PAGE]=U2[PAGE]||{n:1,s:0,t:0};x.s=(x.s||0)+acc;x.t=Math.floor(Date.now()/1000);acc=0;sv("bxm-use",U2)};
 setInterval(function(){if(document.visibilityState==="visible"&&Date.now()-act<60000)acc+=5;if(acc>=30)flush()},5000);
 document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden"&&acc>0)flush()});addEventListener("pagehide",function(){if(acc>0)flush()})}
/* ---- ④ 刷題頁寫入共用作答紀錄（bxm-q2；id = 篇-年-題） ---- */
function qid(q){return q.chapter+"-"+q.year+"-"+q.num}
function rec(q,chosen,ok){var DB=ld("bxm-q2",{}),id=qid(q),r=DB[id]||{n:0,w:0,h:[]};r.c=chosen;r.ok=ok?1:0;r.g=0;r.k="";r.t=Math.floor(Date.now()/1000);r.n=(r.n||0)+1;if(!ok)r.w=(r.w||0)+1;(r.h=r.h||[]).push([r.t,r.ok,0]);if(r.h.length>10)r.h.shift();DB[id]=r;sv("bxm-q2",DB);day("q",1)}
function tag(q,k){var DB=ld("bxm-q2",{}),r=DB[qid(q)];if(!r)return;r.k=k||"";r.g=k==="D"?1:0;sv("bxm-q2",DB)}
function drop(ch){var DB=ld("bxm-q2",{});Object.keys(DB).forEach(function(i){if(i.split("-")[0]===ch)delete DB[i]});sv("bxm-q2",DB)}
/* 舊作答（頁面自己的存檔）補寫一次進共用紀錄 */
function sync(ch,QS,S,gk){var DB=ld("bxm-q2",{}),ch2=false,M={a:"A",b:"B",c:"C",d:"D"};QS.forEach(function(q){var s=S[gk(q)];if(!s)return;var id=ch+"-"+q.year+"-"+q.num;if(DB[id]){if(s.et&&DB[id].k!==M[s.et]){DB[id].k=M[s.et];DB[id].g=s.et==="d"?1:0;ch2=true}return}
 DB[id]={c:s.ch,ok:s.ok?1:0,g:s.et==="d"?1:0,k:s.et?M[s.et]:"",t:Math.floor(Date.now()/1000),n:1,w:s.ok?0:1,h:[]};ch2=true});if(ch2)sv("bxm-q2",DB)}
function fillMark(key){var f=ld("bxm-fill",{});if(!f[key]){f[key]=1;sv("bxm-fill",f);day("c",1)}}
/* ---- ③ 全站回報 ---- */
var KN={A:"A 法條混淆",B:"B 粗心",C:"C 不熟",D:"D 猜的"};
function st(k){var m=ld("bxm-st:"+k,{});return m}
function build(){
 var DB=ld("bxm-q2",{}),TGT=ld("bxm-tgt",{p:60,g:70}),lastRep=ld("bxm-lastrep",0),ids=Object.keys(DB),by={},tot={sure:0,gok:0,wr:0},cat={A:0,B:0,C:0,D:0,n:0},fresh=0;
 ids.forEach(function(id){var r=DB[id],ch=id.split("-")[0];var o=by[ch]=by[ch]||{sure:0,gok:0,wr:0};if(r.ok){if(r.k==="D"){o.gok++;tot.gok++;cat.D++}else{o.sure++;tot.sure++}}else{o.wr++;tot.wr++;if(r.k)cat[r.k]++;else cat.n++}if(r.t>lastRep)fresh++});
 var total=0,c;for(c in CH)total+=CH[c][2];var done=tot.sure+tot.gok+tot.wr,ok=tot.sure+tot.gok;
 var DY=ld("bxm-day",{}),td=DY[ymd()]||{q:0,c:0},wk=0,wc=0,i;for(i=0;i<7;i++){var dd=new Date();dd.setDate(dd.getDate()-i);var x=DY[ymd(dd)];if(x){wk+=x.q||0;wc+=x.c||0}}
 var L=["【"+SUBJ+"學習回報】"+now(),"產生自："+(document.title||PAGE),"說明：同一瀏覽器所有頁面共用一份紀錄，任一頁產生的回報都涵蓋全部工具，不需每頁各貼；換裝置才另貼。","",
 "今日：刷題作答 "+td.q+" 題｜卡片與填空操作 "+td.c+" 次；近 7 日：刷題 "+wk+" 題｜卡片與填空 "+wc+" 次（自 "+"2026-10-12 起記錄）","",
 "══ 一、選擇題題庫（刷題 A～E 五篇，共 "+total+" 題）══",
 "整體：已作答 "+done+"／"+total+"（達成 "+pc(done,total)+"%）｜答對 "+ok+"（確定 "+tot.sure+"、猜對 "+tot.gok+"）｜答錯 "+tot.wr+"｜正確率 "+(done?pc(ok,done)+"%":"-")+"｜及格線 "+TGT.p+"%・目標 "+TGT.g+"%","自上次回報新增：作答 "+fresh+" 題","","── 各篇 ──"];
 for(c in CH){var o=by[c];if(!o){L.push("民法刷題練習_"+c+"篇（"+CH[c][1]+"）：未作答（共 "+CH[c][2]+" 題）");continue}var d=o.sure+o.gok+o.wr;L.push("民法刷題練習_"+c+"篇（"+CH[c][1]+"）：已答 "+d+"／"+CH[c][2]+"｜答對 "+(o.sure+o.gok)+"（猜對 "+o.gok+"）答錯 "+o.wr+"｜"+pc(o.sure+o.gok,d)+"%｜達成 "+pc(d,CH[c][2])+"%")}
 L.push("","── 各篇刷到哪些年份（年份＝作答題數；99–114 共 16 年）──");
 for(c in CH){var yc={};ids.forEach(function(id){var q=id.split("-");if(q[0]===c)yc[q[1]]=(yc[q[1]]||0)+1});var ys=Object.keys(yc).sort(function(a,b){return b-a}),miss=[];for(i=99;i<=114;i++)if(!yc[i])miss.push(i);
  L.push(c+" 篇："+(ys.length?ys.map(function(y){return y+"("+yc[y]+")"}).join("、"):"尚未作答")+(ys.length?"｜完全沒碰："+(miss.length?miss.join("、"):"無"):""))}
 L.push("","── 錯題原因（A/B/C 只計答錯；D 含猜對）──","A 法條混淆 "+cat.A+"｜B 粗心 "+cat.B+"｜C 不熟 "+cat.C+"｜D 猜的 "+cat.D+"｜未分類 "+cat.n);
 var wr=ids.filter(function(i){return!DB[i].ok}).sort(function(a,b){return(DB[b].w||0)-(DB[a].w||0)||DB[b].t-DB[a].t}).slice(0,40);
 L.push("","── 答錯題（錯得多的在前，最多 40 題；格式 篇-年-題）──");wr.forEach(function(i){var r=DB[i];L.push(i+"　錯 "+(r.w||1)+" 次"+(r.k?"・"+KN[r.k]:"・未分類"))});
 var gu=ids.filter(function(i){return DB[i].ok&&DB[i].k==="D"}).slice(0,40);if(gu.length)L.push("","── 猜對（待加強）──",gu.join("、"));
 L.push("","══ 二、25題模擬測驗 ══");
 var H=ld("bx_mock_civ_sim",[]);if(!H.length)L.push("尚未作答");else{L.push("共 "+H.length+" 次；最近 "+Math.min(5,H.length)+" 次（新→舊）：");H.slice(-5).reverse().forEach(function(r){L.push("民國 "+r.y+" 年卷｜選擇題 "+r.correct+"／25 對｜"+r.score+" 分"+(r.total!=null?"｜含申論合計 "+r.total:"")+"｜"+new Date(r.t).toLocaleString("zh-TW",{hour12:false}))})}
 ["civ1","civ2"].forEach(function(id,i){var r=ld("bx_mock_"+id,null);L.push("自擬模擬卷"+(i+1)+"："+(r&&r.n?"最近已答 "+r.a+"／"+r.n+"，答對 "+r.c+"（選擇題 "+(r.c*2)+"／50）":"尚未作答"))});
 L.push("","══ 三、記憶工具 ══");
 var cnt=function(keys,tt){var n=0,r=0;keys.forEach(function(key){var m=st(key);Object.keys(m).forEach(function(k){var s=typeof m[k]==="string"?m[k]:(m[k]&&m[k].status);if(s==="mastered")n++;else if(s==="review")r++})});return"已掌握 "+n+"｜待複習 "+r+"｜未標記 "+Math.max(0,tt-n-r)+"（共 "+tt+"）"};
 L.push("精選考題小卡：",cnt(["exam_mastery_data","exam_mastery_data_a","exam_mastery_data_d","exam_mastery_data_e"],TOT.sel));
 L.push("完整考題小卡（520 張，與題庫同題）："+cnt(["exam_mastery_a_full_v1","exam_mastery_bc_full_v1","exam_mastery_d_full_v1","exam_mastery_e_full_v1"],TOT.full));
 L.push("互動單字卡："+cnt(["mastery_data","mastery_data_a","mastery_data_d","mastery_data_e"],TOT.word));
 var ff=ld("bxm-fill",{}),fc={},fk=Object.keys(ff).length;Object.keys(ff).forEach(function(k){var c2=k.split("-")[0];fc[c2]=(fc[c2]||0)+1});
 L.push("定義填空練習：已確認 "+fk+"／"+TOT.fill+" 張"+(fk?"（"+Object.keys(fc).sort().map(function(c2){return c2+" "+fc[c2]}).join("・")+"）":"（尚無紀錄；此功能 2026-10-12 起才開始記錄）"));
 var es=ld("civlaw_essay_template_mastery_v2",{}),er=0,em=0;Object.keys(es).forEach(function(k){if(es[k]==="mastered")em++;else if(es[k]==="read")er++});L.push("申論五型模板：已讀 "+er+"｜已熟 "+em);
 var U=ld("bxm-use",{}),hr=[],nv=[];
 PAGES.forEach(function(p){var x=U[p[0]];if(!x||!x.n){nv.push(p[1]);return}hr.push(p[1]+"｜開 "+x.n+" 次｜約 "+Math.round((x.s||0)/60)+" 分｜最近 "+new Date(x.t*1000).toLocaleDateString("zh-TW"))});
 L.push("","══ 四、頁面使用（自 2026-10-12 起記錄；開啟次數與約略停留分鐘）══");hr.forEach(function(s){L.push(s)});if(nv.length)L.push("尚未開過："+nv.join("、"));
 var data={};ids.forEach(function(i){var r=DB[i];data[i]=[r.c,r.ok,r.k==="D"?1:0,r.k||"",r.t,r.n||1,r.w||0]});
 L.push("","BXDATA1:"+b64e(data));return L.join("\n")}
window.BXREP={build:build,rec:rec,tag:tag,drop:drop,sync:sync,fillMark:fillMark,PAGE:PAGE,today:function(){return ld("bxm-day",{})[ymd()]||{q:0,c:0}}};
})();
