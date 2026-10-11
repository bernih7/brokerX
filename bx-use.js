/* bx-use.js：全站共用——①自動記錄每頁開啟次數與停留時間 ②全站回報產生器 ③舊練習頁寫入共用作答紀錄。不連任何外部服務，資料只在本瀏覽器。 */
(function(){
var CH={"A1": ["A1A2", "A1 總則", 27], "A2": ["A1A2", "A2 土地登記", 54], "A3": ["A3A4A5", "A3 共有優先購買權", 20], "A4": ["A3A4A5", "A4 基地耕地優先購買權", 29], "A5": ["A3A4A5", "A5 公有土地", 13], "B1": ["B", "B1 區域計畫法／非都市土地管制", 37], "B2": ["B", "B2 都市計畫法", 40], "B3": ["B", "B3 國土計畫法", 3], "C1": ["C", "C1 規定地價", 9], "C2": ["C", "C2 市地重劃", 19], "C3": ["C", "C3 照價收買・空地稅・超額建地", 15], "C4": ["C", "C4 申報登錄・預售屋管理", 12], "D1": ["D", "D1 徵收程序與要件", 9], "D2": ["D", "D2 徵收補償標準", 27], "D3": ["D", "D3 區段徵收", 28], "D4": ["D", "D4 撤銷・廢止徵收與收回權", 14], "E1": ["E", "E1 地價稅", 37], "E2": ["E", "E2 土地增值稅", 46], "F1": ["FGHI", "F1 房屋稅", 29], "G1": ["FGHI", "G1 契稅", 29], "H1": ["FGHI", "H1 房地合一所得稅", 13], "I1": ["FGHI", "I1 耕地三七五減租", 8]},PAGES=[["LandLaw_A1A2_quiz", "題庫 A1A2"], ["LandLaw_A3A4A5_quiz", "題庫 A3A4A5"], ["LandLaw_B_quiz", "題庫 B"], ["LandLaw_C_quiz", "題庫 C"], ["LandLaw_D_quiz", "題庫 D"], ["LandLaw_E_quiz", "題庫 E"], ["LandLaw_FGHI_quiz", "題庫 FGHI"], ["土地法互動練習", "互動練習"], ["土地法解析版練習", "解析版練習"], ["土地法_診斷卷一", "診斷卷一"], ["土地法_來勝模擬試題一_土地法規", "來勝模擬(一)土地法規"], ["土地法_來勝模擬試題一_土地稅法", "來勝模擬(一)土地稅法"], ["土地法_考題小卡", "考題小卡"], ["土地法_互動單字卡", "互動單字卡"], ["土地法_定義填空練習", "定義填空練習"], ["土地法_罰則總整理", "罰則總整理"], ["土地法_稅率總表", "稅務總表"], ["土地法_稅制與取得方式比較表", "稅制與取得方式比較表"], ["土地法_速查三表", "速查三表"], ["土地法_優先購買權_物權債權", "優先購買權"], ["土地法_分數倍數數字分析", "分數倍數數字分析"], ["土地法_申論題分類總覽", "申論題分類總覽"], ["土地法_彩色重點速記", "彩色重點速記"], ["土地法_讀書攻略與備考指南", "讀書攻略"], ["土地法_備考指揮中心", "備考指揮中心"]],SUBJ="土地法";
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function pad(n){return n<10?"0"+n:""+n}
function now(){var d=new Date();return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())+" "+pad(d.getHours())+":"+pad(d.getMinutes())}
function pc(a,b){return b?Math.round(a/b*100):0}
function b64e(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))))}
var PAGE=decodeURIComponent((location.pathname.split("/").pop()||"index.html")).replace(/\.html$/,"");
/* ---- ① 使用追蹤 ---- */
var known=PAGES.some(function(p){return p[0]===PAGE});
if(known){var U=ld("bx-use",{});var u=U[PAGE]=U[PAGE]||{n:0,s:0,t:0};u.n++;u.t=Math.floor(Date.now()/1000);sv("bx-use",U);
 var act=Date.now(),acc=0;["pointerdown","keydown","scroll","touchstart"].forEach(function(ev){addEventListener(ev,function(){act=Date.now()},{passive:true})});
 var flush=function(){var U2=ld("bx-use",{}),x=U2[PAGE]=U2[PAGE]||{n:1,s:0,t:0};x.s=(x.s||0)+acc;x.t=Math.floor(Date.now()/1000);acc=0;sv("bx-use",U2)};
 setInterval(function(){if(document.visibilityState==="visible"&&Date.now()-act<60000)acc+=5;if(acc>=30)flush()},5000);
 document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden"&&acc>0)flush()});addEventListener("pagehide",function(){if(acc>0)flush()})}
/* ---- ③ 舊練習頁寫入共用作答紀錄（bx-q2） ---- */
function qid(q){return q.chapter+"-"+q.year+"-"+q.num}
function rec(q,chosen,ok){var DB=ld("bx-q2",{}),id=qid(q),r=DB[id]||{n:0,w:0,h:[]};r.c=chosen;r.ok=ok?1:0;r.g=0;r.k="";r.t=Math.floor(Date.now()/1000);r.n=(r.n||0)+1;if(!ok)r.w=(r.w||0)+1;(r.h=r.h||[]).push([r.t,r.ok,0]);if(r.h.length>10)r.h.shift();DB[id]=r;sv("bx-q2",DB)}
function tag(q,k){var DB=ld("bx-q2",{}),r=DB[qid(q)];if(!r)return;r.k=k;r.g=k==="D"?1:0;sv("bx-q2",DB)}
/* ---- ② 全站回報 ---- */
var KN={A:"A 法條混淆",B:"B 粗心",C:"C 不熟",D:"D 猜的"};
function build(){
 var DB=ld("bx-q2",{}),TGT=ld("bx-tgt",{p:60,g:70}),lastRep=ld("bx-lastrep",0),ids=Object.keys(DB),by={},tot={sure:0,gok:0,wr:0},cat={A:0,B:0,C:0,D:0,n:0},fresh=0;
 ids.forEach(function(id){var r=DB[id],ch=id.split("-")[0];var o=by[ch]=by[ch]||{sure:0,gok:0,wr:0};if(r.ok){if(r.k==="D"){o.gok++;tot.gok++;cat.D++}else{o.sure++;tot.sure++}}else{o.wr++;tot.wr++;if(r.k)cat[r.k]++;else cat.n++}if(r.t>lastRep)fresh++});
 var total=0,c;for(c in CH)total+=CH[c][2];var done=tot.sure+tot.gok+tot.wr,ok=tot.sure+tot.gok;
 var L=["【"+SUBJ+"學習回報】"+now(),"產生自："+(document.title||PAGE),"說明：同一瀏覽器所有頁面共用一份紀錄，任一頁產生的回報都涵蓋全部工具，不需每頁各貼；換裝置才另貼。","","══ 一、選擇題題庫（題庫七頁＋互動練習＋解析版練習 共用，共 "+total+" 題）══",
 "整體：已作答 "+done+"／"+total+"（達成 "+pc(done,total)+"%）｜答對 "+ok+"（確定 "+tot.sure+"、猜對 "+tot.gok+"）｜答錯 "+tot.wr+"｜正確率 "+(done?pc(ok,done)+"%":"-")+"｜及格線 "+TGT.p+"%・目標 "+TGT.g+"%","自上次回報新增：作答 "+fresh+" 題","","── 各頁（依題目章節歸入題庫頁；互動練習、解析版練習的作答也計入）──"];
 var pg={},order=[];for(c in CH){var p=CH[c][0];if(!pg[p]){pg[p]={t:0,d:0,o:0,w:0};order.push(p)}pg[p].t+=CH[c][2];var x=by[c];if(x){pg[p].d+=x.sure+x.gok+x.wr;pg[p].o+=x.sure+x.gok;pg[p].w+=x.wr}}
 order.forEach(function(p){var o=pg[p];L.push("LandLaw_"+p+"：已答 "+o.d+"／"+o.t+(o.d?"｜答對 "+o.o+"｜答錯 "+o.w+"｜"+pc(o.o,o.d)+"%":"｜未作答")+"（達成 "+pc(o.d,o.t)+"%）")});
 L.push("","── 各章 ──");for(c in CH){var o=by[c];if(!o){L.push(CH[c][1]+"：未作答（共 "+CH[c][2]+" 題）");continue}var d=o.sure+o.gok+o.wr;L.push(CH[c][1]+"：已答 "+d+"／"+CH[c][2]+"｜答對 "+(o.sure+o.gok)+"（猜對 "+o.gok+"）答錯 "+o.wr+"｜"+pc(o.sure+o.gok,d)+"%")}
 L.push("","── 錯題原因（A/B/C 只計答錯；D 含猜對）──","A 法條混淆 "+cat.A+"｜B 粗心 "+cat.B+"｜C 不熟 "+cat.C+"｜D 猜的 "+cat.D+"｜未分類 "+cat.n);
 var wr=ids.filter(function(i){return!DB[i].ok}).sort(function(a,b){return(DB[b].w||0)-(DB[a].w||0)||DB[b].t-DB[a].t}).slice(0,40);
 L.push("","── 答錯題（錯得多的在前，最多 40 題）──");wr.forEach(function(i){var r=DB[i];L.push(i+"　錯 "+(r.w||1)+" 次"+(r.k?"・"+KN[r.k]:"・未分類"))});
 var gu=ids.filter(function(i){return DB[i].ok&&DB[i].k==="D"}).slice(0,40);if(gu.length)L.push("","── 猜對（待加強）──",gu.join("、"));
 L.push("","══ 二、模擬卷／診斷卷 ══");
 [["landdiag1","診斷卷一"],["ll_a1","來勝模擬(一)土地法規"],["ll_b1","來勝模擬(一)土地稅法"]].forEach(function(m){var r=ld("bx_mock_"+m[0],null),er=ld("bx_mockerr_"+m[0],{});if(!r){L.push(m[1]+"：尚未作答");return}var ec={};Object.keys(er).forEach(function(k){ec[er[k]]=(ec[er[k]]||0)+1});var es=Object.keys(ec).sort().map(function(k){return k+" "+ec[k]}).join("・");
  L.push(m[1]+"：已答 "+r.a+"／"+r.n+"｜答對 "+r.c+"｜"+pc(r.c,r.a)+"%｜"+new Date(r.t).toLocaleString("zh-TW",{hour12:false})+(es?"｜錯題原因 "+es:""))});
 L.push("","══ 三、記憶工具 ══");
 var cnt=function(key,tt){var m=ld(key,{}),n=0,r=0;Object.keys(m).forEach(function(k){var s=typeof m[k]==="string"?m[k]:(m[k]&&m[k].status);if(s==="mastered")n++;else if(s==="review")r++});return"已掌握 "+n+"｜待複習 "+r+"｜未標記 "+Math.max(0,tt-n-r)};
 L.push("考題小卡（共 518 張）："+cnt("exam_mastery_land_v1",518));L.push("互動單字卡（共 104 張）："+cnt("land_flashcard_mastery_v1",104));
 var ff=ld("bx-fill",{}),fc={},fk=Object.keys(ff).length;Object.keys(ff).forEach(function(k){var c2=k.split("-")[0];fc[c2]=(fc[c2]||0)+1});
 L.push("定義填空練習：已確認 "+fk+" 張"+(fk?"（"+Object.keys(fc).sort().map(function(c2){return c2+" "+fc[c2]}).join("・")+"）":"（尚無紀錄；此功能 2026-10-12 起才開始記錄）"));
 var U=ld("bx-use",{}),hr=[],nv=[];
 PAGES.forEach(function(p){var x=U[p[0]];if(!x||!x.n){nv.push(p[1]);return}hr.push(p[1]+"｜開 "+x.n+" 次｜約 "+Math.round((x.s||0)/60)+" 分｜最近 "+new Date(x.t*1000).toLocaleDateString("zh-TW"))});
 L.push("","══ 四、頁面使用（自 2026-10-12 起記錄；開啟次數與約略停留分鐘）══");hr.forEach(function(s){L.push(s)});if(nv.length)L.push("尚未開過："+nv.join("、"));
 var ps=ld("ll_prog",null);if(ps&&(ps.e0||ps.e1||ps.e2))L.push("","指揮中心錯題本計數：A 混淆 "+(ps.e0||0)+"｜B 粗心 "+(ps.e1||0)+"｜C 不熟 "+(ps.e2||0));
 var data={};ids.forEach(function(i){var r=DB[i];data[i]=[r.c,r.ok,r.k==="D"?1:0,r.k||"",r.t,r.n||1,r.w||0]});
 L.push("","BXDATA1:"+b64e(data));return L.join("\n")}
function fillMark(key){var f=ld("bx-fill",{});f[key]=1;sv("bx-fill",f)}
window.BXREP={build:build,rec:rec,tag:tag,fillMark:fillMark,PAGE:PAGE};
})();
