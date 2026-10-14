/* bx-use.js：經紀法規全站共用——①自動記錄每頁開啟次數與停留時間 ②全站回報產生器 ③舊練習頁寫入共用作答紀錄。不連任何外部服務，資料只在本瀏覽器。 */
(function(){
var CH={"A1": ["A1A2A3", "A1 總則：名詞定義與主管機關", 6], "A2": ["A1A2A3", "A2 經紀業設立、保證金與營業處所", 20], "A3": ["A1A2A3", "A3 經紀人員：資格、證書與義務", 21], "A4": ["A4", "A4 業務及責任（核心高頻）", 51], "A5": ["A5", "A5 獎懲：行政罰與刑罰", 38], "C1": ["其他小章節", "C1 說明書：土地應記載事項", 1], "C2": ["其他小章節", "C2 說明書：成屋應記載事項", 4], "C3": ["其他小章節", "C3 說明書：預售屋應記載事項", 1], "C4": ["其他小章節", "C4 說明書：不得記載事項", 7], "D2": ["其他小章節", "D2 預售屋買賣定型化契約", 5], "D3": ["其他小章節", "D3 委託銷售定型化契約", 9], "E1": ["E1", "E1 公寓大廈：總則與定義", 39], "E2": ["其他小章節", "E2 公寓大廈：住戶權利義務", 6], "E3": ["E3", "E3 公寓大廈：管理組織與決議", 66], "E4": ["其他小章節", "E4 公寓大廈：規約", 3], "E5": ["其他小章節", "E5 公寓大廈：罰則", 6], "F2": ["其他小章節", "F2 規約範本之法律性質", 1], "G1": ["G1", "G1 公平交易法重要條文", 110], "G2": ["G2", "G2 廣告查核分工原則", 9], "H1": ["H1", "H1 定型化契約規範", 23], "H2": ["其他小章節", "H2 特種交易", 6], "H3": ["H3", "H3 損害賠償與罰則", 88]},PAGES=[["經紀法規刷題練習_A1A2A3", "題庫 A1A2A3"], ["經紀法規刷題練習_A4", "題庫 A4"], ["經紀法規刷題練習_A5", "題庫 A5"], ["經紀法規刷題練習_E1", "題庫 E1"], ["經紀法規刷題練習_E3", "題庫 E3"], ["經紀法規刷題練習_G1_1", "題庫 G1-1"], ["經紀法規刷題練習_G1_2", "題庫 G1-2"], ["經紀法規刷題練習_G2", "題庫 G2"], ["經紀法規刷題練習_H1", "題庫 H1"], ["經紀法規刷題練習_H3_1", "題庫 H3-1"], ["經紀法規刷題練習_H3_2", "題庫 H3-2"], ["經紀法規刷題練習_其他小章節", "題庫 其他小章節"], ["經紀法規概要_互動練習", "互動練習"], ["經紀法規_診斷卷一", "診斷卷一"], ["經紀法規_高頻考點卷二", "高頻考點卷二"], ["經紀法規_混淆對比卷三", "混淆對比卷三"], ["經紀法規_全真模擬卷四", "全真模擬卷四"], ["經紀法規_模擬試題一_曾榮耀", "來勝模擬(一)"], ["經紀法規概要_互動單字卡", "互動單字卡"], ["經紀法規_定義填空練習", "定義填空練習"], ["經紀法規申論題_篇章主題答題模板", "申論答題模板"], ["經紀法規_罰則總整理", "罰則總整理"], ["經紀法規概要_彩色重點速記", "彩色重點速記"], ["經紀法規_易混淆概念並排", "易混淆概念並排"], ["經紀法規_讀書攻略與備考指南", "讀書攻略"], ["經紀法規_備考指揮中心", "備考指揮中心"]],SUBJ="經紀法規";
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function pad(n){return n<10?"0"+n:""+n}
function now(){var d=new Date();return d.getFullYear()+"-"+pad(d.getMonth()+1)+"-"+pad(d.getDate())+" "+pad(d.getHours())+":"+pad(d.getMinutes())}
function pc(a,b){return b?Math.round(a/b*100):0}
function b64e(o){return btoa(unescape(encodeURIComponent(JSON.stringify(o))))}
var PAGE=decodeURIComponent((location.pathname.split("/").pop()||"index.html")).replace(/\.html$/,"");
/* ---- ① 使用追蹤 ---- */
var known=PAGES.some(function(p){return p[0]===PAGE});
if(known){var U=ld("bxj-use",{});var u=U[PAGE]=U[PAGE]||{n:0,s:0,t:0};u.n++;u.t=Math.floor(Date.now()/1000);sv("bxj-use",U);
 var act=Date.now(),acc=0;["pointerdown","keydown","scroll","touchstart"].forEach(function(ev){addEventListener(ev,function(){act=Date.now()},{passive:true})});
 var flush=function(){var U2=ld("bxj-use",{}),x=U2[PAGE]=U2[PAGE]||{n:1,s:0,t:0};x.s=(x.s||0)+acc;x.t=Math.floor(Date.now()/1000);acc=0;sv("bxj-use",U2)};
 setInterval(function(){if(document.visibilityState==="visible"&&Date.now()-act<60000)acc+=5;if(acc>=30)flush()},5000);
 document.addEventListener("visibilitychange",function(){if(document.visibilityState==="hidden"&&acc>0)flush()});addEventListener("pagehide",function(){if(acc>0)flush()})}
/* ---- ③ 舊練習頁寫入共用作答紀錄（bx-q2） ---- */
function qid(q){return q.chapter+"-"+q.year+"-"+(q.num||q.qnum)}
function rec(q,chosen,ok){var DB=ld("bxj-q2",{}),id=qid(q),r=DB[id]||{n:0,w:0,h:[]};r.c=chosen;r.ok=ok?1:0;r.g=0;r.k="";r.t=Math.floor(Date.now()/1000);r.n=(r.n||0)+1;if(!ok)r.w=(r.w||0)+1;(r.h=r.h||[]).push([r.t,r.ok,0]);if(r.h.length>10)r.h.shift();DB[id]=r;sv("bxj-q2",DB)}
function tag(q,k){var DB=ld("bxj-q2",{}),r=DB[qid(q)];if(!r)return;r.k=k;r.g=k==="D"?1:0;sv("bxj-q2",DB)}
/* ---- ② 全站回報 ---- */
var KN={A:"A 法條混淆",B:"B 粗心",C:"C 不熟",D:"D 猜的"};
function build(){
 var DB=ld("bxj-q2",{}),TGT=ld("bxj-tgt",{p:60,g:70}),lastRep=ld("bxj-lastrep",0),ids=Object.keys(DB),by={},tot={sure:0,gok:0,wr:0},cat={A:0,B:0,C:0,D:0,n:0},fresh=0;
 ids.forEach(function(id){var r=DB[id],ch=id.split("-")[0];var o=by[ch]=by[ch]||{sure:0,gok:0,wr:0};if(r.ok){if(r.k==="D"){o.gok++;tot.gok++;cat.D++}else{o.sure++;tot.sure++}}else{o.wr++;tot.wr++;if(r.k)cat[r.k]++;else cat.n++}if(r.t>lastRep)fresh++});
 var total=0,c;for(c in CH)total+=CH[c][2];var done=tot.sure+tot.gok+tot.wr,ok=tot.sure+tot.gok;
 var L=["【"+SUBJ+"學習回報】"+now(),"產生自："+(document.title||PAGE),"說明：同一瀏覽器所有頁面共用一份紀錄，任一頁產生的回報都涵蓋全部工具，不需每頁各貼；換裝置才另貼。","","══ 一、選擇題題庫（章節題庫十二頁＋互動練習 共用，共 "+total+" 題）══",
 "整體：已作答 "+done+"／"+total+"（達成 "+pc(done,total)+"%）｜答對 "+ok+"（確定 "+tot.sure+"、猜對 "+tot.gok+"）｜答錯 "+tot.wr+"｜正確率 "+(done?pc(ok,done)+"%":"-")+"｜及格線 "+TGT.p+"%・目標 "+TGT.g+"%","自上次回報新增：作答 "+fresh+" 題","","── 各頁（依題目章節歸入題庫頁；互動練習的作答也計入）──"];
 var pg={},order=[];for(c in CH){var p=CH[c][0];if(!pg[p]){pg[p]={t:0,d:0,o:0,w:0};order.push(p)}pg[p].t+=CH[c][2];var x=by[c];if(x){pg[p].d+=x.sure+x.gok+x.wr;pg[p].o+=x.sure+x.gok;pg[p].w+=x.wr}}
 order.forEach(function(p){var o=pg[p];L.push("題庫 "+p+"：已答 "+o.d+"／"+o.t+(o.d?"｜答對 "+o.o+"｜答錯 "+o.w+"｜"+pc(o.o,o.d)+"%":"｜未作答")+"（達成 "+pc(o.d,o.t)+"%）")});
 L.push("","── 各章 ──");for(c in CH){var o=by[c];if(!o){L.push(CH[c][1]+"：未作答（共 "+CH[c][2]+" 題）");continue}var d=o.sure+o.gok+o.wr;L.push(CH[c][1]+"：已答 "+d+"／"+CH[c][2]+"｜答對 "+(o.sure+o.gok)+"（猜對 "+o.gok+"）答錯 "+o.wr+"｜"+pc(o.sure+o.gok,d)+"%")}
 L.push("","── 錯題原因（A/B/C 只計答錯；D 含猜對）──","A 法條混淆 "+cat.A+"｜B 粗心 "+cat.B+"｜C 不熟 "+cat.C+"｜D 猜的 "+cat.D+"｜未分類 "+cat.n);
 var wr=ids.filter(function(i){return!DB[i].ok}).sort(function(a,b){return(DB[b].w||0)-(DB[a].w||0)||DB[b].t-DB[a].t}).slice(0,40);
 L.push("","── 答錯題（錯得多的在前，最多 40 題）──");wr.forEach(function(i){var r=DB[i];L.push(i+"　錯 "+(r.w||1)+" 次"+(r.k?"・"+KN[r.k]:"・未分類"))});
 var gu=ids.filter(function(i){return DB[i].ok&&DB[i].k==="D"}).slice(0,40);if(gu.length)L.push("","── 猜對（待加強）──",gu.join("、"));
 L.push("","══ 二、模擬卷／診斷卷 ══");
 [["diag1","診斷卷一"],["hi2","高頻考點卷二"],["cf3","混淆對比卷三"],["full4","全真模擬卷四"],["tch1","來勝模擬(一)"]].forEach(function(m){var r=ld("bx_mock_"+m[0],null),er=ld("bx_mockerr_"+m[0],{});if(!r){L.push(m[1]+"：尚未作答");return}var ec={};Object.keys(er).forEach(function(k){ec[er[k]]=(ec[er[k]]||0)+1});var es=Object.keys(ec).sort().map(function(k){return k+" "+ec[k]}).join("・");
  L.push(m[1]+"：已答 "+r.a+"／"+r.n+"｜答對 "+r.c+"｜"+pc(r.c,r.a)+"%｜"+new Date(r.t).toLocaleString("zh-TW",{hour12:false})+(es?"｜錯題原因 "+es:""))});
 L.push("","══ 三、記憶工具 ══");
 var cnt=function(key,tt,yes,no){var m=ld(key,{}),n=0,r=0,t=0;Object.keys(m).forEach(function(k){var s=typeof m[k]==="string"?m[k]:(m[k]&&m[k].status);t++;if(s===yes)n++;else if(s===no)r++});return"已掌握 "+n+"｜待加強 "+r+"｜其他已標記 "+(t-n-r)+"｜未標記 "+Math.max(0,tt-t)};
 L.push("互動單字卡（共 113 張；掌握／不熟／普通）："+cnt("jingji_flashcard_mastery",113,"yes","no"));var em=ld("brokerlaw_essay_template_mastery_v2",{}),e1=0,e2=0;Object.keys(em).forEach(function(k){if(em[k]==="mastered")e1++;else e2++});L.push("申論答題模板：已掌握 "+e1+" 題範例｜僅讀過 "+e2+" 題範例");
 var ff=ld("bxj-fill",{}),fc={},fk=Object.keys(ff).length;Object.keys(ff).forEach(function(k){var c2=k.split("-")[0];fc[c2]=(fc[c2]||0)+1});
 L.push("定義填空練習（共 95 張）：已確認 "+fk+" 張"+(fk?"（"+Object.keys(fc).sort().map(function(c2){return c2+" "+fc[c2]}).join("・")+"）":"（尚無紀錄；此功能 2026-10-12 起才開始記錄）"));
 var U=ld("bxj-use",{}),hr=[],nv=[];
 PAGES.forEach(function(p){var x=U[p[0]];if(!x||!x.n){nv.push(p[1]);return}hr.push(p[1]+"｜開 "+x.n+" 次｜約 "+Math.round((x.s||0)/60)+" 分｜最近 "+new Date(x.t*1000).toLocaleDateString("zh-TW"))});
 L.push("","══ 四、頁面使用（自 2026-10-12 起記錄；開啟次數與約略停留分鐘）══");hr.forEach(function(s){L.push(s)});if(nv.length)L.push("尚未開過："+nv.join("、"));
 var ps=ld("jj_prog",null);if(ps&&(ps.e0||ps.e1||ps.e2))L.push("","指揮中心錯題本計數：A 混淆 "+(ps.e0||0)+"｜B 粗心 "+(ps.e1||0)+"｜C 不熟 "+(ps.e2||0));
 var data={};ids.forEach(function(i){var r=DB[i];data[i]=[r.c,r.ok,r.k==="D"?1:0,r.k||"",r.t,r.n||1,r.w||0]});
 L.push("","BXDATA1:"+b64e(data));return L.join("\n")}
function fillMark(key){var f=ld("bxj-fill",{});f[key]=1;sv("bxj-fill",f)}
window.BXREP={build:build,rec:rec,tag:tag,fillMark:fillMark,PAGE:PAGE};
})();
