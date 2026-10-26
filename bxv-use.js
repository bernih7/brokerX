/* bxv-use.js：估價全站共用——①補上 window.storage（GitHub Pages 沒有，頁面原本存不住進度）②自動記錄每頁開啟次數與停留時間與每日刷題數 ③全站回報產生器 ④刷題頁寫入共用作答紀錄。不連任何外部服務，資料只在本瀏覽器。 */
(function(){
var SUBJ="估價";
/* CH：章節代碼 → [頁面key, 章名, 題數] */
var CH={
 "A1":["A1","A1 估價原則",44],
 "A2":["A2","A2 價格種類",31],
 "A3":["A3","A3 影響因素",44],
 "A4":["A4","A4 估價程序",44],
 "B": ["B", "B 比較法",65],
 "C1":["C1","C1 重建成本",57],
 "C2":["C2","C2 折舊計算",40],
 "D1":["D1","D1 直接資本化",42],
 "D2":["D2","D2 資本化率",29],
 "D3":["D3","D3 DCF",13],
 "E1":["E1","E1 土地開發",25],
 "F1":["F1","F1 租金估計",33],
 "G1":["G1","G1 樓層效用",15],
 "H1H2":["H1H2","H1H2 特殊宗地",21],
 "H3I1":["H3I1","H3I1 都更CAMA",17],
 "I2J1":["I2J1","I2J1 土地改良物・特殊宗地",20]
};
/* 113 真題頁不是獨立章節：它直接取用章節題庫的 113 年 25 題，作答記在各題自己的章節。
   （v512 前曾有 "113" 偽章節與 Q113_* 題號，已移除） */
/* PAGES：[頁面檔名（不含.html）, 顯示名稱] */
var PAGES=[
 ["估價刷題練習_A1","刷題 A1"],
 ["估價刷題練習_A2","刷題 A2"],
 ["估價刷題練習_A3","刷題 A3"],
 ["估價刷題練習_A4","刷題 A4"],
 ["估價刷題練習_B","刷題 B"],
 ["估價刷題練習_C1","刷題 C1"],
 ["估價刷題練習_C2","刷題 C2"],
 ["估價刷題練習_D1","刷題 D1"],
 ["估價刷題練習_D2","刷題 D2"],
 ["估價刷題練習_D3","刷題 D3"],
 ["估價刷題練習_E1","刷題 E1"],
 ["估價刷題練習_F1","刷題 F1"],
 ["估價刷題練習_G1","刷題 G1"],
 ["估價刷題練習_H1H2","刷題 H1H2"],
 ["估價刷題練習_H3I1","刷題 H3I1"],
 ["估價刷題練習_I2J1","刷題 I2J1"],
 ["估價刷題練習_113真題","刷題 113真題"],
 ["估價解析版練習","解析版練習（跨章）"],
 ["估價互動單字卡","互動單字卡"],
 ["估價_定義填空練習","定義填空練習"],
 ["估價_考題小卡","考題小卡"],
 ["估價彩色重點速記","彩色重點速記"],
 ["估價_程序流程記憶圖","程序流程記憶圖"],
 ["估價_八大程序速覽表","八大程序速覽"],
 ["估價_四大方法比較表","四大方法比較表"],
 ["估價_易混淆概念並排","易混淆概念並排"],
 ["估價四大方法系統攻略","四大方法系統攻略"],
 ["不動產估價概要_申論題實戰範文","申論題實戰範文"],
 ["估價_計算題攻略","計算題攻略"],
 ["估價_診斷卷一","診斷卷①"],
 ["估價_租金估計攻略表","租金估計攻略表"],
 ["估價_營造施工費四法","營造施工費四法"],
 ["估價_地價調查估計規則專欄","地價調查估計規則專欄"],
 ["估價_特殊標的總整理","特殊標的總整理"],
 ["估價_技術規則專欄","技術規則專欄"],
 ["估價_土開計算題組","土開計算題組"],
 ["估價_DCF計算題組","DCF計算題組"],
 ["估價_房地拆價計算題組","房地拆價計算題組"],
 ["估價_來勝模擬試題一","來勝模擬試題一"],
 ["估價_自編補強卷","自編補強卷"],
 ["估價_綜合模擬卷一","綜合模擬卷一"],
 ["估價_綜合模擬卷二","綜合模擬卷二"],
 ["估價_綜合模擬卷三","綜合模擬卷三"],
 ["估價_綜合模擬卷四","綜合模擬卷四"],
 ["估價_綜合模擬卷五","綜合模擬卷五"],
 ["估價備考指揮中心","備考指揮中心"]
];

function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function pad(n){return n<10?"0"+n:""+n}
function ymd(d){d=d||new Date();return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())}
function now(){var d=new Date();return ymd(d)+" "+pad(d.getHours())+":"+pad(d.getMinutes())}
function pc(a,b){return b?Math.round(a/b*100):0}
function b64e(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))))}
function day(f,n){var D=ld("bxv-day",{}),k=ymd(),x=D[k]=D[k]||{q:0,c:0};x[f]=(x[f]||0)+n;
 var ks=Object.keys(D).sort();while(ks.length>60)delete D[ks.shift()];sv("bxv-day",D)}

/* ---- ① window.storage 補強（Claude 預覽內建；GitHub Pages 沒有） ---- */
if(typeof window.storage==="undefined"){
 window.storage={
  get:function(k){return Promise.resolve().then(function(){var v=localStorage.getItem("bxv-st:"+k);return v==null?null:{key:k,value:v}})},
  set:function(k,v){return Promise.resolve().then(function(){
   var old=null,nw=null;
   try{old=JSON.parse(localStorage.getItem("bxv-st:"+k)||"null")}catch(e){}
   localStorage.setItem("bxv-st:"+k,v);
   try{nw=JSON.parse(v)}catch(e){}
   if(nw&&typeof nw==="object"){var n=0;Object.keys(nw).forEach(function(id){if(JSON.stringify((old||{})[id])!==JSON.stringify(nw[id]))n++});if(n)day("c",n)}
   return {key:k,value:v}})},
  delete:function(k){return Promise.resolve().then(function(){localStorage.removeItem("bxv-st:"+k);return {key:k,deleted:true}})}
 }
}

/* 舊 window.storage key 遷移：valuation_practice_* → bxv-st:valuation_practice_* */
(function migrate(){
 var prefixes=["valuation_practice_a1_v2","valuation_practice_a2_v2","valuation_practice_a3_v2",
  "valuation_practice_a4_v2","valuation_practice_b_v2","valuation_practice_c1_v2",
  "valuation_practice_c2_v2","valuation_practice_d1_v2","valuation_practice_d2_v2",
  "valuation_practice_d3_v2","valuation_practice_e1_v2","valuation_practice_f1_v2",
  "valuation_practice_g1_v2","valuation_practice_h1h2_v2","valuation_practice_h3i1_v2",
  "val_prac_i2j1_v1","val_prac_113_v1"];
 prefixes.forEach(function(p){
  ["_answers","_errortags"].forEach(function(suf){
   var k=p+suf,nk="bxv-st:"+k;
   try{
    if(!localStorage.getItem(nk)&&localStorage.getItem(k)){
     localStorage.setItem(nk,localStorage.getItem(k));
    }
   }catch(e){}
  });
 });
})();

var PAGE=decodeURIComponent((location.pathname.split("/").pop()||"index.html")).replace(/\.html$/,"");

/* ---- 章節代碼統一：頁面題目的 cat（B1、H1、J1…）→ 指揮中心章節代碼（CH 的 key） ----
   刷題頁 rec() 用題目 cat 當前綴、sync() 用頁面傳入的 CH_KEY（＝第一題 cat），兩者對不上；
   113 真題的題目 cat 是 A1/B…，會被算進各章。統一規則：在刷題頁一律用該頁章節代碼；其他情況用別名表。 */
var ALIAS={"B1":"B","B2":"B","H1":"H1H2","H2":"H1H2","H3":"H3I1","I1":"H3I1","I2":"I2J1","J1":"I2J1"};
var PAGECH={};for(var _c in CH)PAGECH["估價刷題練習_"+CH[_c][0]]=_c;
function chOf(raw){return PAGECH[PAGE]||ALIAS[raw]||raw}
/* 一次性清理＋遷移 bxv-q2（每次載入檢查，冪等；只有有變動才寫回）：
   ①刪除 key 含 "undefined" 的壞紀錄（舊版來勝模擬試題一 rec 參數錯誤造成）
   ②舊前綴歸章：題號 Q113_* → 113；B1/B2→B、H1/H2→H1H2、H3/I1→H3I1、I2/J1→I2J1；同題重複時留較新的一筆 */
(function cleanQ2(){
 var DB=ld("bxv-q2",null);if(!DB||typeof DB!=="object")return;var ch=false;
 Object.keys(DB).forEach(function(k){
  if(k.indexOf("undefined")>=0){delete DB[k];ch=true;return}
  var a=k.split("-"),p=a[0],idp=a[a.length-1];
  /* v512：舊 113 真題頁的 Q113_* 是「改寫版題幹」的作答，不是官方題，直接刪除不保留
     （官方 113 年 25 題記在各章，id 為 V??_113_N；詳見 113 真題頁說明） */
  if(/^Q113_/.test(idp)||p==="113"){delete DB[k];ch=true;return}
  var np=ALIAS[p]||p;
  if(np===p)return;
  a[0]=np;var nk=a.join("-"),o=DB[nk],r=DB[k];
  if(!o||(r&&(r.t||0)>(o.t||0)))DB[nk]=r;
  delete DB[k];ch=true});
 if(ch)sv("bxv-q2",DB);
})();

/* ---- ② 使用追蹤 ---- */
var known=PAGES.some(function(p){return p[0]===PAGE});
if(known){
 var U=ld("bxv-use",{});var u=U[PAGE]=U[PAGE]||{n:0,s:0,t:0};u.n++;u.t=Math.floor(Date.now()/1000);sv("bxv-use",U);
 var act=Date.now(),acc=0;
 ["pointerdown","keydown","scroll","touchstart"].forEach(function(ev){addEventListener(ev,function(){act=Date.now()},{passive:true})});
 var flush=function(){var U2=ld("bxv-use",{}),x=U2[PAGE]=U2[PAGE]||{n:1,s:0,t:0};x.s=(x.s||0)+acc;x.t=Math.floor(Date.now()/1000);acc=0;sv("bxv-use",U2)};
 setInterval(function(){if(document.visibilityState==="visible"&&Date.now()-act<60000)acc+=5;if(acc>=30)flush()},5000);
 document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden"&&acc>0)flush()});
 addEventListener("pagehide",function(){if(acc>0)flush()});
}

/* ---- ④ 刷題頁寫入共用作答紀錄（bxv-q2；id = 章-年-題） ---- */
function qid(q){return chOf(q.chapter||q.cat)+"-"+(q.year||"obs")+"-"+(q.num||q.id)}
function rec(q,chosen,ok){
 var DB=ld("bxv-q2",{}),id=qid(q),r=DB[id]||{n:0,w:0,h:[]};
 r.c=chosen;r.ok=ok?1:0;r.g=0;r.k="";r.t=Math.floor(Date.now()/1000);
 r.n=(r.n||0)+1;if(!ok)r.w=(r.w||0)+1;
 (r.h=r.h||[]).push([r.t,r.ok,0]);if(r.h.length>10)r.h.shift();
 DB[id]=r;sv("bxv-q2",DB);day("q",1)
}
function tag(q,k){var DB=ld("bxv-q2",{}),r=DB[qid(q)];if(!r)return;r.k=k||"";r.g=k==="D"?1:0;sv("bxv-q2",DB)}
function drop(ch){ch=chOf(ch);var DB=ld("bxv-q2",{});Object.keys(DB).forEach(function(i){if(i.split("-")[0]===ch)delete DB[i]});sv("bxv-q2",DB)}

/* 舊作答補寫進共用紀錄（window.storage key → bxv-q2） */
function sync(ch,QS,S,gk){
 var DB=ld("bxv-q2",{}),changed=false,M={a:"A",b:"B",c:"C",d:"D"};ch=chOf(ch);
 QS.forEach(function(q){
  var g=gk(q);if(g&&typeof g==="object")g=g.id; /* 各頁傳 k=>k，拿到的是題目物件本身，改取 id */
  var s=S[g];if(!s)return;
  var id=ch+"-"+(q.year||"obs")+"-"+(q.num||q.id);
  if(DB[id]){if(s.et&&DB[id].k!==M[s.et]){DB[id].k=M[s.et];DB[id].g=s.et==="d"?1:0;changed=true}return}
  DB[id]={c:s.ch||s.selected,ok:s.ok||s.correct?1:0,g:s.et==="d"?1:0,k:s.et?M[s.et]:"",t:Math.floor(Date.now()/1000),n:1,w:(s.ok||s.correct)?0:1,h:[]};changed=true
 });
 if(changed)sv("bxv-q2",DB)
}

function fillMark(key){var f=ld("bxv-fill",{});if(!f[key]){f[key]=1;sv("bxv-fill",f);day("c",1)}}
function fillUnmark(keys){var f=ld("bxv-fill",{});(keys||[]).forEach(function(k){delete f[k]});sv("bxv-fill",f)}
/* 定義填空每張卡 id＝章節代碼-兩位序號（例 A1-01）；"fill" 是舊版「跑完一輪」標記，不算張數 */
var FILL_RE=/^(A1|A2|A3|A4|B|C|D|E|G|H|I2|J|K|I)-\d{2}$/;
function fillDone(){var f=ld("bxv-fill",{}),n=0;Object.keys(f).forEach(function(k){if(f[k]&&FILL_RE.test(k))n++});return n}
/* 模擬卷題目不屬題庫：只計入今日作答數，不寫 bxv-q2 */
function countQ(n){day("q",n||1)}

/* 純閱讀頁 計次（+1 / -1 / 讀取） */
function readInc(id,delta){
 var R=ld("bxv-read",{});R[id]=R[id]||{n:0,t:0};
 R[id].n=Math.max(0,(R[id].n||0)+(delta||1));
 if(R[id].n>0)R[id].t=Math.floor(Date.now()/1000);
 sv("bxv-read",R);return R[id].n
}
function readGet(id){var R=ld("bxv-read",{});return R[id]||{n:0,t:0}}

/* ---- ③ 全站回報 ---- */
var KN={A:"A 法條混淆",B:"B 粗心",C:"C 不熟",D:"D 猜的"};
function build(){
 var DB=ld("bxv-q2",{}),TGT=ld("bxv-tgt",{p:60,g:70}),lastRep=ld("bxv-lastrep",0);
 var ids=Object.keys(DB),by={},tot={sure:0,gok:0,wr:0},cat={A:0,B:0,C:0,D:0,n:0},fresh=0;
 ids.forEach(function(id){
  var r=DB[id],ch=id.split("-")[0];
  var o=by[ch]=by[ch]||{sure:0,gok:0,wr:0};
  if(r.ok){if(r.k==="D"){o.gok++;tot.gok++;cat.D++}else{o.sure++;tot.sure++}}
  else{o.wr++;tot.wr++;if(r.k)cat[r.k]++;else cat.n++}
  if(r.t>lastRep)fresh++
 });

 var total=0;for(var c in CH)total+=CH[c][2];
 var done=tot.sure+tot.gok+tot.wr,ok=tot.sure+tot.gok;
 var DY=ld("bxv-day",{}),td=DY[ymd()]||{q:0,c:0},wk=0,wc=0,i;
 for(i=0;i<7;i++){var dd=new Date();dd.setDate(dd.getDate()-i);var x=DY[ymd(dd)];if(x){wk+=x.q||0;wc+=x.c||0}}

 var L=["【估價學習回報】"+now(),"產生自："+(document.title||PAGE),
  "說明：同一瀏覽器所有頁面共用一份紀錄，任一頁產生的回報都涵蓋全部工具，不需每頁各貼；換裝置才另貼。","",
  "今日：刷題作答 "+td.q+" 題｜卡片與填空操作 "+td.c+" 次；近 7 日：刷題 "+wk+" 題｜卡片與填空 "+wc+" 次（自 2026-10-13 起記錄）","",
  "══ 一、選擇題題庫（A1～I2J1 共 16 章，共 "+total+" 題；含 113 年官方 25 題）══",
  "整體：已作答 "+done+"／"+total+"（達成 "+pc(done,total)+"%）｜答對 "+ok+"（確定 "+tot.sure+"、猜對 "+tot.gok+"）｜答錯 "+tot.wr+"｜正確率 "+(done?pc(ok,done)+"%":"-")+"｜及格線 "+TGT.p+"%・目標 "+TGT.g+"%",
  "自上次回報新增：作答 "+fresh+" 題","","── 各章 ──"];

 for(c in CH){
  var o=by[c];if(!o){L.push(CH[c][0]+"（"+CH[c][1]+"）：尚未開過（共 "+CH[c][2]+" 題）");continue}
  var d=o.sure+o.gok+o.wr;
  L.push(CH[c][0]+"（"+CH[c][1]+"）：已答 "+d+"／"+CH[c][2]+"｜答對 "+(o.sure+o.gok)+"（猜對 "+o.gok+"）答錯 "+o.wr+"｜正確率 "+pc(o.sure+o.gok,d)+"%｜達成 "+pc(d,CH[c][2])+"%")
 }

 L.push("","── 錯題原因（A/B/C 只計答錯；D 含猜對）──","A 法條混淆 "+cat.A+"｜B 粗心 "+cat.B+"｜C 不熟 "+cat.C+"｜D 猜的 "+cat.D+"｜未分類 "+cat.n);
 var wr=ids.filter(function(i){return!DB[i].ok}).sort(function(a,b){return(DB[b].w||0)-(DB[a].w||0)||DB[b].t-DB[a].t}).slice(0,40);
 L.push("","── 答錯題（錯得多的在前，最多 40 題；格式 章-年-題）──");
 wr.forEach(function(i){var r=DB[i];L.push(i+"　錯 "+(r.w||1)+" 次"+(r.k?"・"+KN[r.k]:"・未分類"))});
 var gu=ids.filter(function(i){return DB[i].ok&&DB[i].k==="D"}).slice(0,40);
 if(gu.length)L.push("","── 猜對（待加強）──",gu.join("、"));

 L.push("","══ 二、診斷卷 ══");
 var H=ld("bxv-mock",{});
 if(!Object.keys(H).length)L.push("尚未開過");
 else Object.keys(H).forEach(function(id){var r=H[id];L.push("診斷卷 "+id+"｜得分 "+r.score+"｜"+new Date(r.t*1000).toLocaleDateString("zh-TW"))});

 L.push("","══ 三、記憶工具 ══");
 var fk=fillDone();
 L.push("定義填空練習：已確認 "+fk+" 張"+(fk?"":"（尚無紀錄；此功能 2026-10-13 起才開始記錄）"));

 var R=ld("bxv-read",{});
 var readItems=[
  {id:"card",label:"互動單字卡"},
  {id:"kcard",label:"考題小卡"},
  {id:"color",label:"彩色重點速記"},
  {id:"flow",label:"程序流程記憶圖"},
  {id:"proc",label:"八大程序速覽表"},
  {id:"method",label:"四大方法比較表"},
  {id:"special",label:"特殊標的總整理"},
  {id:"mix1",label:"易混淆概念並排"},
  {id:"sys",label:"四大方法系統攻略"},
  {id:"essay",label:"申論題實戰範文"},
  {id:"calc",label:"計算題攻略"}
 ];
 readItems.forEach(function(it){
  var r=R[it.id]||{n:0,t:0};
  if(r.n>0)L.push(it.label+"：讀了 "+r.n+" 次，最近 "+new Date(r.t*1000).toLocaleDateString("zh-TW"));
  else L.push(it.label+"：尚未開過");
 });

 var U=ld("bxv-use",{}),hr=[],nv=[];
 PAGES.forEach(function(p){
  var x=U[p[0]];
  if(!x||!x.n){nv.push(p[1]);return}
  hr.push(p[1]+"｜開 "+x.n+" 次｜約 "+Math.round((x.s||0)/60)+" 分｜最近 "+new Date(x.t*1000).toLocaleDateString("zh-TW"))
 });
 L.push("","══ 四、頁面使用（自 2026-10-13 起記錄；開啟次數與約略停留分鐘）══");
 hr.forEach(function(s){L.push(s)});
 if(nv.length)L.push("尚未開過："+nv.join("、"));

 /* 更新 lastRep 時間戳 */
 try{localStorage.setItem("bxv-lastrep",Math.floor(Date.now()/1000))}catch(e){}

 var data={};ids.forEach(function(i){var r=DB[i];data[i]=[r.c,r.ok,r.k==="D"?1:0,r.k||"",r.t,r.n||1,r.w||0]});
 L.push("","BXDATA1:"+b64e(data));
 return L.join("\n")
}

/* ---- ⑤ 各工具完成度＋讀過輪數（指揮中心「進度」頁顯示，不需回報） ---- */
var BASE="https://bernih7.github.io/brokerX/";
function U8(p){return BASE+encodeURIComponent(p)+".html"}
/* 頁面 → 讀過計數 RID（bxv-read）；有 RID 的頁面在指揮中心顯示「讀過 N 輪」 */
var RIDS={"估價互動單字卡":"card","估價_考題小卡":"kcard","估價_定義填空練習":"fill","估價彩色重點速記":"color","估價四大方法系統攻略":"sys","估價_四大方法比較表":"method","估價_程序流程記憶圖":"flow","估價_八大程序速覽表":"proc","估價_租金估計攻略表":"rent","估價_營造施工費四法":"cost4","估價_地價調查估計規則專欄":"dijia","估價_特殊標的總整理":"special","估價_計算題攻略":"calc","估價_易混淆概念並排":"mix1","估價_技術規則專欄":"rule","不動產估價概要_申論題實戰範文":"essay"};
/* 頁面本身沒有 header 計數元件、由本檔在右下自動補「＋／讀過 N 輪／－」的頁面 */
var READ_INJ={"估價_技術規則專欄":1,"估價_定義填空練習":1};
/* 各刷題頁自己的作答存檔（window.storage → localStorage "bxv-st:"+key） */
var ANS={"A1":"valuation_practice_a1_v2","A2":"valuation_practice_a2_v2","A3":"valuation_practice_a3_v2","A4":"valuation_practice_a4_v2","B":"valuation_practice_b_v2","C1":"valuation_practice_c1_v2","C2":"valuation_practice_c2_v2","D1":"valuation_practice_d1_v2","D2":"valuation_practice_d2_v2","D3":"valuation_practice_d3_v2","E1":"valuation_practice_e1_v2","F1":"valuation_practice_f1_v2","G1":"valuation_practice_g1_v2","H1H2":"valuation_practice_h1h2_v2","H3I1":"valuation_practice_h3i1_v2","I2J1":"val_prac_i2j1_v1"};
var TOT={fill:116,card:95,kcard:533,essay:53,v_hs1:25,e1dev:8,dcf:8,split:6};
function md(t){if(!t)return"";var d=new Date(t*1000);return(d.getMonth()+1)+"/"+d.getDate()}
function status(){
 var UU=ld("bxv-use",{}),G=[];
 function row(p,name,done,total,txt,t2){var u=UU[p]||{},rid=RIDS[p],rd=rid?readGet(rid):{n:0,t:0};
  return{p:p,url:U8(p),name:name,done:done,total:total,pct:total?Math.min(100,Math.round(done/total*100)):null,txt:txt,read:rid?(rd.n||0):null,open:u.n||0,last:Math.max(u.t||0,rd.t||0,t2||0)}}
 /* 刷題：讀各頁自己的作答存檔 */
 var R1=[];["A1","A2","A3","A4","B","C1","C2","D1","D2","D3","E1","F1","G1","H1H2","H3I1","I2J1"].forEach(function(c){var a=ld("bxv-st:"+ANS[c]+"_answers",null)||ld(ANS[c]+"_answers",{})||{},ks=Object.keys(a),d=Math.min(ks.length,CH[c][2]),ok=0,known=0;
  ks.forEach(function(k){var v=a[k];if(v&&typeof v==="object"&&"correct" in v){known++;if(v.correct)ok++}});
  R1.push(row("估價刷題練習_"+CH[c][0],"刷題 "+CH[c][1],d,CH[c][2],"已作答 "+d+"／"+CH[c][2]+(known?"・正確率 "+pc(ok,known)+"%・錯 "+(known-ok):"")))});
 /* 113 年官方 25 題：記在各章，這一列只是把它們挑出來看進度（不是獨立章節，不另計總題數） */
 (function(){var D3=ld("bxv-q2",{}),n=0,k3=0;Object.keys(D3).forEach(function(k){if(k.indexOf("-113年")>0){n++;if(D3[k].ok)k3++}});
  R1.push(row("估價刷題練習_113真題","113年官方真題（25題・已計入各章）",Math.min(n,25),25,"已作答 "+Math.min(n,25)+"／25"+(n?"・正確率 "+pc(k3,n)+"%":"")))})();
 var AT=ld("bxv-anal-time",[]);
 R1.unshift(row("估價解析版練習","解析版練習（跨章節・智慧配題・計時）",0,0,AT.length?"已計時練習 "+AT.length+" 輪（近 10 輪）・最近一輪 "+Math.round(AT[0].s/60*10)/10+" 分、每題約 "+Math.round(AT[0].s/Math.max(1,AT[0].n))+" 秒":"尚未練習（作答自動寫入下方各章進度）",AT.length?Math.floor(AT[0].d/1000):0));
 G.push({g:"刷題（作答後自動記錄）",rows:R1});
 /* 模擬卷 */
 var R2=[],hs=ld("v_hs1_answers",{}),hn=Math.min(Object.keys(hs).length,TOT.v_hs1);
 R2.push(row("估價_來勝模擬試題一","來勝模擬試題一",hn,TOT.v_hs1,"選擇題已作答 "+hn+"／"+TOT.v_hs1));
 [["估價_自編補強卷","自編補強卷（原模擬試題二～四的獨有 24 題）","bx_mockx_1","mockx1"],
  ["估價_綜合模擬卷一","綜合模擬卷一","bx_mockc_1","mockc1"],["估價_綜合模擬卷二","綜合模擬卷二","bx_mockc_2","mockc2"],["估價_綜合模擬卷三","綜合模擬卷三","bx_mockc_3","mockc3"],["估價_綜合模擬卷四","綜合模擬卷四","bx_mockc_4","mockc4"],["估價_綜合模擬卷五","綜合模擬卷五","bx_mockc_5","mockc5"],
  ["估價_診斷卷一","診斷卷一","bx_mock_1","diag1"]].forEach(function(m){
  var r=ld(m[2],null)||ld("bxv-mock:"+m[3],null),tt=(r&&r.total)||25,ts=r&&r.ts?Math.floor(r.ts/1000):0;
  R2.push(row(m[0],m[1],r?tt:0,tt,r?"已交卷・答對 "+r.score+"／"+tt+"（"+(r.pct!=null?r.pct:pc(r.score,tt))+"%）":"尚未交卷",ts))});
 var cv=row("估價_模擬卷覆蓋分析","模擬卷覆蓋分析",0,0,"分析頁，不記錄開啟");cv.open=null;R2.push(cv);
 G.push({g:"模擬卷（交卷後自動記錄）",rows:R2});
 /* 計算題組 */
 var R3=[];[["估價_土開計算題組","土開計算題組","bx-e1dev-done",TOT.e1dev],["估價_DCF計算題組","DCF計算題組","bx-dcfcalc-done",TOT.dcf],["估價_房地拆價計算題組","房地拆價計算題組","bx-split-done",TOT.split]].forEach(function(x){
  var dn=ld(x[2],[]);dn=Array.isArray(dn)?Math.min(dn.length,x[3]):0;R3.push(row(x[0],x[1],dn,x[3],"答對 "+dn+"／"+x[3]+" 題"))});
 G.push({g:"計算題組（核對答對自動記錄）",rows:R3});
 /* 記憶工具 */
 var R4=[],fm=ld("bxv-st:valuation_flashcard_mastery",{})||{},fmm=0,fmr=0;Object.keys(fm).forEach(function(k){if(fm[k]==="mastered")fmm++;else if(fm[k])fmr++});
 fmm=Math.min(fmm,TOT.card);R4.push(row("估價互動單字卡","互動單字卡",fmm,TOT.card,"已掌握 "+fmm+"／"+TOT.card+" 張"+(fmr?"・待複習 "+fmr:"")));
 var kc=ld("bxe-card-v2",{})||{},kcm=0,kcr=0;Object.keys(kc).forEach(function(k){var s=kc[k]&&typeof kc[k]==="object"?kc[k].status:kc[k];if(s==="mastered")kcm++;else if(s==="review")kcr++});
 kcm=Math.min(kcm,TOT.kcard);R4.push(row("估價_考題小卡","考題小卡",kcm,TOT.kcard,"已掌握 "+kcm+"／"+TOT.kcard+" 張"+(kcr?"・待複習 "+kcr:"")));
 var fr=parseInt(ld("bxe-fill",0),10)||0,ft=parseInt(ld("bxv-fill-total",TOT.fill),10)||TOT.fill,fd=Math.min(fillDone(),ft);
 R4.push(row("估價_定義填空練習","定義填空練習",fd,ft,"已完成 "+fd+"／"+ft+" 張"+(fr?"・隨機測驗跑完 "+fr+" 輪":"")));
 G.push({g:"記憶工具（已掌握＝自己標記）",rows:R4});
 /* 申論 */
 var er=ld("bx-essay-read",[]),en=0;if(Array.isArray(er))er.forEach(function(id){if(/^(e\d+-[12]|pred-\d+)$/.test(id))en++});en=Math.min(en,TOT.essay);
 G.push({g:"申論",rows:[row("不動產估價概要_申論題實戰範文","申論題實戰範文",en,TOT.essay,"已讀 "+en+"／"+TOT.essay+" 題（官方 32＋預測 21）")]});
 /* 閱讀頁 */
 var R6=[];[["估價彩色重點速記","彩色重點速記"],["估價四大方法系統攻略","四大方法系統攻略"],["估價_四大方法比較表","四大方法比較表"],["估價_程序流程記憶圖","程序流程記憶圖"],["估價_八大程序速覽表","八大程序速覽表"],["估價_租金估計攻略表","租金估計攻略表"],["估價_營造施工費四法","營造施工費四法"],["估價_地價調查估計規則專欄","地價調查估計規則專欄"],["估價_特殊標的總整理","特殊標的總整理"],["估價_計算題攻略","計算題攻略"],["估價_易混淆概念並排","易混淆概念並排"],["估價_技術規則專欄","技術規則專欄"]].forEach(function(a){R6.push(row(a[0],a[1],0,0,""))});
 G.push({g:"閱讀頁（讀完一輪在該頁按＋）",rows:R6});
 return G}

window.BXREP={build:build,rec:rec,tag:tag,drop:drop,sync:sync,fillMark:fillMark,fillUnmark:fillUnmark,fillDone:fillDone,countQ:countQ,chOf:chOf,CH:CH,readInc:readInc,readGet:readGet,status:status,READ_INJ:READ_INJ,RIDS:RIDS,PAGE:PAGE,today:function(){return ld("bxv-day",{})[ymd()]||{q:0,c:0}}};
})();

/* ── 浮動鈕（全站標準 #bxfab）：左下回頂端（進度環）＋右下回備考指揮中心；沒有深淺色切換鈕的頁面補 🌙 ── */
(function(){
 var HUB=/備考指揮中心/.test(decodeURIComponent(location.pathname));
 var HUBURL="%E4%BC%B0%E5%83%B9%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html";
 var RE_TOP=/回頂|回到頂|回到最上|頂端|↑|⇧|▲|totop|to-top|backtop|back-top|fab-top|scrolltop|scroll-top|gotop|go-top|\btop\b|upbtn|navup/i;
 var RE_HOME=/hub|home|指揮中心|備考中心|回首頁|⌂|🏠/i;
 var RE_THEME=/深色|淺色|亮\/暗|深淺|🌙|☀|theme/i;
 function sig(e){var t=[e.id,typeof e.className==="string"?e.className:"",e.title,e.getAttribute("aria-label"),e.getAttribute("href"),e.getAttribute("onclick"),(e.textContent||"").trim().slice(0,12)];
  var k=e.querySelectorAll("[id],[class],[title],[href]");for(var i=0;i<k.length&&i<12;i++){var c=k[i];t.push(c.id,typeof c.className==="string"?c.className:"",c.title,c.getAttribute("href"))}return t.join(" ")}
 function vis(e){return e.getClientRects().length>0&&getComputedStyle(e).visibility!=="hidden"}
 function isTheme(e){var g=[e.id,typeof e.className==="string"?e.className:"",e.title,e.getAttribute("aria-label"),(e.textContent||"").trim().slice(0,8)].join(" ");return RE_THEME.test(g)}
 function css(){
  var st=document.createElement("style");st.id="bxv-fab-css";
  st.textContent=
   ".bxv-hide{display:none!important}"+
   "#bxfab{--fp:#2F5D50;--fs:#FFFEFA;--fo:#FFFFFF;--fl:#DDD6C0;position:fixed;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom,0px));padding:0 max(12px,env(safe-area-inset-right,0px)) 0 max(12px,env(safe-area-inset-left,0px));display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none;z-index:60}"+
   "#bxfab>*{pointer-events:auto}"+
   "#bxfab .bx-up{position:relative;width:40px;height:40px;border-radius:50%;border:0;background:var(--fs);color:var(--fp);padding:0;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.22);cursor:pointer;opacity:.4;transition:opacity .25s}"+
   "#bxfab .bx-up.act{opacity:1}#bxfab .bx-up .rg{position:absolute;inset:0;width:100%;height:100%}#bxfab .bx-up .rg circle{fill:none;stroke-width:3}"+
   "#bxfab .bx-up .rg .t{stroke:var(--fl)}#bxfab .bx-up .rg .p{stroke:var(--fp);stroke-linecap:round;transform:rotate(-90deg);transform-origin:center;transition:stroke-dashoffset .1s}"+
   "#bxfab svg.ic{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;position:relative}"+
   "#bxfab .bx-hub{width:40px;height:40px;border-radius:50%;background:var(--fp);color:var(--fo);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.25);text-decoration:none}"+
   "#bxfab .bx-hub svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}"+
   "@media (prefers-color-scheme: dark){:root:not([data-theme=\"light\"]) #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}}"+
   ":root[data-theme=\"dark\"] #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}"+
   "#bxv-theme{position:fixed;top:calc(14px + env(safe-area-inset-top,0px));right:max(14px,env(safe-area-inset-right,0px));z-index:999;width:36px;height:36px;border-radius:50%;border:1.5px solid var(--line,var(--rule,#DDD6C0));background:var(--paper,var(--card,#FFFEFA));color:var(--ink,var(--fg,#25302C));font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:0;font-family:inherit}";
  document.head.appendChild(st)}
 function build(){
  var w=document.createElement("div");w.id="bxfab";
  w.innerHTML='<button class="bx-up" aria-label="回到最上方" title="回到最上方"><svg class="rg" viewBox="0 0 44 44"><circle class="t" cx="22" cy="22" r="19"/><circle class="p" cx="22" cy="22" r="19" stroke-dasharray="119.4" stroke-dashoffset="119.4"/></svg><svg class="ic" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>'+
   (HUB?'':'<a class="bx-hub" href="'+HUBURL+'" aria-label="回備考指揮中心" title="回備考指揮中心"><svg viewBox="0 0 24 24"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/></svg></a>');
  document.body.appendChild(w);
  var b=w.querySelector(".bx-up"),p=b.querySelector(".p");
  b.onclick=function(){scrollTo({top:0,behavior:"smooth"})};
  function f(){var h=document.documentElement,m=h.scrollHeight-innerHeight,y=scrollY||0,r=m>0?Math.min(1,y/m):0;p.setAttribute("stroke-dashoffset",(119.4*(1-r)).toFixed(1));b.classList.toggle("act",y>160)}
  addEventListener("scroll",f,{passive:true});addEventListener("resize",f);f();
  var vv=window.visualViewport;function z(){if(!vv)return;var s=vv.scale;if(s<=1.02){w.style.transform="";return}var lh=document.documentElement.clientHeight;w.style.transformOrigin="left bottom";w.style.transform="translate("+vv.offsetLeft+"px,"+(vv.offsetTop+vv.height-lh)+"px) scale("+(1/s)+")"}
  if(vv){vv.addEventListener("resize",z);vv.addEventListener("scroll",z)}
  return w}
 function themeBtn(){
  var c=document.querySelectorAll("button,a,[role=button],[onclick]");
  for(var i=0;i<c.length;i++){if(isTheme(c[i])&&vis(c[i]))return}
  var root=document.documentElement;
  function dark(){var t=root.getAttribute("data-theme");return t==="dark"||(!t&&matchMedia("(prefers-color-scheme: dark)").matches)}
  try{var s=localStorage.getItem("bx-theme")||localStorage.getItem("bxr-theme");if(s&&!root.getAttribute("data-theme"))root.setAttribute("data-theme",s)}catch(e){}
  var t=document.createElement("button");t.id="bxv-theme";t.title="切換深淺色";t.setAttribute("aria-label","切換深淺色");
  function ic(){t.textContent=dark()?"☀️":"🌙"}ic();
  t.onclick=function(){var n=dark()?"light":"dark";root.setAttribute("data-theme",n);try{localStorage.setItem("bx-theme",n);localStorage.setItem("bxr-theme",n)}catch(e){}
   var pb=document.getElementById("theme-btn");if(pb&&!/[🌙☀]/.test(pb.textContent))pb.textContent=n==="dark"?"淺色":"深色";ic()};
  document.body.appendChild(t)}
 function run(){
  try{
   css();
   var w=document.getElementById("bxfab")||build();
   if(HUB){var hh=w.querySelector(".bx-hub");if(hh)hh.classList.add("bxv-hide")}
   /* 收掉頁面自帶的舊版回頂／回中心鈕，只留 #bxfab */
   var all=document.body.getElementsByTagName("*"),barTop=innerHeight,leftTop=innerHeight;
   for(var i=0;i<all.length;i++){var e=all[i];
    if(e===w||w.contains(e)||e.id==="bxv-theme")continue;
    var cs=getComputedStyle(e);if(cs.position!=="fixed")continue;
    if(e.parentElement&&e.parentElement.closest&&e.parentElement.closest(".bxv-hide"))continue;
    var r=e.getBoundingClientRect(),v=vis(e);
    if(v&&r.width>innerWidth*0.8){if(r.bottom>=innerHeight-6)barTop=Math.min(barTop,r.top);continue}
    if(isTheme(e))continue;
    var small=v?(r.width<=130&&r.height<=170):((e.textContent||"").trim().length<=16);
    if(!small)continue;
    var g=sig(e);
    if(RE_TOP.test(g)||RE_HOME.test(g)){e.classList.add("bxv-hide");continue}
    if(v&&r.left+r.width/2<innerWidth/2&&r.bottom>innerHeight-220)leftTop=Math.min(leftTop,r.top)}
   /* 底部有固定列（導覽列、計分列）就把按鈕墊到列的上方 */
   if(barTop<innerHeight)w.style.bottom="calc("+Math.round(innerHeight-barTop+10)+"px)";
   var up=w.querySelector(".bx-up"),wb=w.getBoundingClientRect().bottom;
   if(leftTop<innerHeight&&up)up.style.marginBottom=Math.max(0,Math.round(wb-leftTop+10))+"px";
   themeBtn();
   readWidget(w);
  }catch(e){}
 }
 /* 沒有 header 計數元件的閱讀／記憶頁：右下直式「＋／讀過 N 輪／－」，放在回指揮中心圓鈕正上方（沿用 bxv-read） */
 function readWidget(w){
  var R=window.BXREP;if(!R||!R.READ_INJ||!R.READ_INJ[R.PAGE]||document.getElementById("bxv-n")||document.getElementById("bxvRead"))return;
  var rid=R.RIDS[R.PAGE];if(!rid)return;
  var cs=document.createElement("style");cs.textContent=
   "#bxvRead{--rp:#2F5D50;--rs:#FFFEFA;--ri:#25302C;--rl:#DDD6C0;position:fixed;right:max(12px,env(safe-area-inset-right,0px));bottom:calc(64px + env(safe-area-inset-bottom,0px));z-index:59;width:40px;display:flex;flex-direction:column;align-items:center;gap:2px;background:var(--rs);color:var(--ri);border:1px solid var(--rl);border-radius:20px;padding:3px 0;box-shadow:0 2px 8px rgba(0,0,0,.18);font:11px/1.15 system-ui,-apple-system,'Noto Sans TC',sans-serif;text-align:center}"+
   "#bxvRead button{width:32px;height:32px;border:0;border-radius:50%;background:transparent;color:var(--rp);font-size:18px;line-height:1;cursor:pointer;font-family:inherit;padding:0}#bxvRead button.p{background:var(--rp);color:var(--rs)}#bxvRead .t{display:block;padding:1px 0}#bxvRead b{display:block;font-size:15px;color:var(--rp)}"+
   "@media (prefers-color-scheme: dark){:root:not([data-theme=\"light\"]) #bxvRead{--rp:#84C2AE;--rs:#1F2723;--ri:#E7ECE6;--rl:#34403A}}:root[data-theme=\"dark\"] #bxvRead{--rp:#84C2AE;--rs:#1F2723;--ri:#E7ECE6;--rl:#34403A}";
  document.head.appendChild(cs);
  var b=document.createElement("div");b.id="bxvRead";b.title="讀完一輪按＋，按錯按－；輪數顯示在指揮中心「進度」";
  b.innerHTML='<button type="button" class="p" aria-label="讀完一輪，加一">＋</button><span class="t">讀過<b>0</b>輪</span><button type="button" aria-label="減一輪">－</button>';
  var bs=b.querySelectorAll("button"),n=b.querySelector("b");function up(){n.textContent=R.readGet(rid).n||0}
  bs[0].onclick=function(){R.readInc(rid,1);up()};bs[1].onclick=function(){R.readInc(rid,-1);up()};
  document.body.appendChild(b);up();
  /* 跟著 #bxfab 的高度（底部有固定列時 #bxfab 會被墊高） */
  var hub=w&&w.querySelector(".bx-hub");if(hub&&hub.getClientRects().length){var top=hub.getBoundingClientRect().top;b.style.bottom=Math.round(innerHeight-top+10)+"px"}
 }
 if(document.readyState==="complete")setTimeout(run,300);else addEventListener("load",function(){setTimeout(run,500)});
})();

/* ---- 答案鍵修正後的一次性重算（v495）：舊作答若依錯誤答案鍵判分，這裡依新答案鍵重判 ---- */
(function(){try{
 var FLAG="bxv-keyfix",VER="v495";if(localStorage.getItem(FLAG)===VER)return;
 var PFX={A1:"valuation_practice_a1_v2",A2:"valuation_practice_a2_v2",A3:"valuation_practice_a3_v2",A4:"valuation_practice_a4_v2",B:"valuation_practice_b_v2",C1:"valuation_practice_c1_v2",C2:"valuation_practice_c2_v2",D1:"valuation_practice_d1_v2",D2:"valuation_practice_d2_v2",D3:"valuation_practice_d3_v2",E1:"valuation_practice_e1_v2",F1:"valuation_practice_f1_v2",G1:"valuation_practice_g1_v2",H1H2:"valuation_practice_h1h2_v2",H3I1:"valuation_practice_h3i1_v2",I2J1:"val_prac_i2j1_v1"};
 /* [章, 年第N題, 題id, 新正解index, 類型] 類型：k＝依新答案重判；f＝一律給分；d＝題幹選項已換成原卷，舊紀錄作廢；r＝選項重排（103-15） */
 var FIX=[["A2","105年第7題","VA2_105_7",3,"k"],["B","107年第17題","VB1_107_17",0,"k"],["C1","102年第33題","VC1_102_33",3,"k"],["D1","102年第12題","VD1_102_12",3,"k"],["H1H2","102年第19題","VH1_102_19",1,"d"],["H1H2","105年第28題","VH2_105_28",1,"d"],["A4","103年第14題","VA4_103_14",1,"k"],["H1H2","103年第15題","VH2_103_15",2,"r"],["F1","104年第33題","VF1_104_33",2,"k"],["A3","100年第2題","VA3_100_2",2,"k"],["A3","100年第5題","VA3_100_5",1,"k"],["B","100年第21題","VB1_100_21",1,"k"],["D2","99年第9題","VD2_99_9",1,"f"],["D1","104年第15題","VD1_104_15",1,"f"],["B","106年第28題","VB1_106_28",0,"f"],["D1","108年第11題","VD1_108_11",0,"f"],["B","108年第18題","VB1_108_18",3,"f"],["C1","101年第17題","VC1_101_17",0,"f"]];
 var rd=function(k,d){try{return JSON.parse(localStorage.getItem(k)||"")||d}catch(e){return d}};
 var DB=rd("bxv-q2",{}),chg=false,ST={};
 FIX.forEach(function(f){
  var ch=f[0],qid=ch+"-"+f[1]+"-"+f[2],type=f[4],ok;
  var fn=function(c){if(type==="f")return 1;return c===f[3]?1:0};
  var r=DB[qid];
  if(r){
   if(type==="d"){delete DB[qid];chg=true}
   else if(typeof r.c==="number"||type==="f"){var c=r.c;if(type==="r"&&typeof c==="number"){c=c===3?2:(c===2?-1:c);r.c=c}ok=fn(r.c);if(r.ok!==ok){r.ok=ok;chg=true}if(r.h&&r.h.length)r.h[r.h.length-1][1]=ok}
  }
  var p=PFX[ch];if(!p)return;var k="bxv-st:"+p+"_answers";var A=ST[k]||(ST[k]=rd(k,null));
  if(A&&A[f[2]]){
   if(type==="d"){delete A[f[2]];ST[k+"#"]=1}
   else{var a=A[f[2]],c2=a.selected;if(type==="r"&&typeof c2==="number"){c2=c2===3?2:(c2===2?-1:c2);a.selected=c2}var o=type==="f"?true:(c2===f[3]);if(a.correct!==o){a.correct=o}ST[k+"#"]=1}
  }
 });
 if(chg)localStorage.setItem("bxv-q2",JSON.stringify(DB));
 Object.keys(ST).forEach(function(k){if(k.slice(-1)!=="#"&&ST[k+"#"])localStorage.setItem(k,JSON.stringify(ST[k]))});
 localStorage.setItem(FLAG,VER)
}catch(e){}})();
