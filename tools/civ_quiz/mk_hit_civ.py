# -*- coding: utf-8 -*-
"""《民法_備考指揮中心》「日拱一築」面板（移植自 tools/essay_jj/mk_hit.py 的 v532 覆蓋率版）。

覆蓋率三段：🌟穩穩收下＝est×cov×rate、🌱還能追回＝est×cov×(1-rate)、🌰等待發芽＝est×(1-cov)，三段相加恆為 50 分。
真會率分子＝答對且 !(k==='D' || g===1 || sh===1)。只讀 bxm-q2（id＝刷題篇別-年-題，經 IDM 對到 28 小類），
另寫 bxm-hit-pal（色卡）。可重複執行（以 <style id="hit-css">～<script id="hit-js"> 為邊界整段換掉）。
預估題數由 quiz_data.json 計算：25×(16年占比×0.5＋近5年〔110–114〕占比×0.5)，四捨五入殘差補到最大章。
"""
import io, json, os, collections, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '民法_備考指揮中心.html')
QD = json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))
CT = json.load(io.open(os.path.join(HERE, 'chapters.json'), encoding='utf-8'))
U = lambda n: urllib.parse.quote(n + '.html')
DRILL = {L: U('民法刷題練習_%s篇' % L) for L in 'ABCDE'}
A, BC, D_, E = U('民法A_彩色重點速記'), U('民法BC_彩色重點速記'), U('民法D_彩色重點速記'), U('民法E_彩色重點速記')
BCF = U('民法BC_完整考題小卡')
DB = U('民法_債之發生與移轉')
# 章 → 整理頁（2026-10-27 使用者確認的 28 列）
READ = {
 'A1': (A + '#sec-a1', 'A 速記・自然人'), 'A2': (A + '#sec-a2', 'A 速記・法人'),
 'A3': (A + '#sec-a3', 'A 速記・物'), 'A4': (A + '#sec-a4', 'A 速記・法律行為效力'),
 'A5': (A + '#sec-a5', 'A 速記・意思表示瑕疵'), 'A6': (A + '#sec-a6', 'A 速記・代理'),
 'A7': (U('民法_數字期間速查') + '#s4', '數字期間速查 ④ 時效・除斥期間並排'),
 'B1': (BC + '#sec-b', 'BC 速記・債編總則'), 'B2': (BC + '#sec-b', 'BC 速記・債務不履行三型態'),
 'B3': (BC + '#sec-c', 'BC 速記・保證（連帶債務著墨少）'),
 'B4': (DB + '#s2', '債之發生與移轉 ② 不當得利'), 'B5': (DB + '#s1', '債之發生與移轉 ① 無因管理'),
 'B6': (DB + '#s4', '債之發生與移轉 ③④ 侵權行為'),
 'C1': (BC + '#sec-c', 'BC 速記・買賣'), 'C2': (BC + '#sec-c', 'BC 速記・租賃'),
 'C3': (BC + '#sec-c', 'BC 速記・委任居間承攬比較'),
 'C4': (U('民法_法律效果總整理') + '#s7', '法律效果總整理・契約與物權的效果'),
 'C5': (DB + '#s5', '債之發生與移轉 ⑤ 債權讓與'),
 'D1': (A + '#sec-a3', 'A 速記・物（與 A3 同主題）'),
 'D2': (U('民法_共有專區'), '共有專區（登記另見物權變動與登記）'),
 'D3': (D_ + '#sec-d1', 'D 速記・物權通則與所有權'), 'D4': (D_ + '#sec-d1', 'D 速記・物權通則與所有權'),
 'D5': (D_ + '#sec-d3', 'D 速記・地上權與農育權'), 'D6': (U('民法_抵押權總整理'), '抵押權總整理'),
 'E1': (E + '#sec-e2', 'E 速記・婚姻'), 'E2': (E + '#sec-e5', 'E 速記・夫妻財產制'),
 'E3': (E + '#sec-e4', 'E 速記・父母子女'), 'E4': (U('民法_繼承專區'), '繼承專區'),
}
assert set(READ) == set(CT)
OFF = [q for q in QD['q'] if not q.get('oos')]
TOT = len(OFF)
REC = [q for q in OFF if q['y'] >= 110]
TOTR = len(REC)
c16 = collections.Counter(q['ch'] for q in OFF)
c5 = collections.Counter(q['ch'] for q in REC)
PRED = {c: round(25 * (c16[c] / TOT * 0.5 + c5[c] / TOTR * 0.5), 2) for c in CT}
s = sum(PRED.values())
if abs(s - 25) > 0.001:
    big = max(PRED, key=lambda k: PRED[k])
    PRED[big] = round(PRED[big] + 25 - s, 2)
IDM = {'%s-%d-%d' % (q['p'], q['y'], q['n']): q['ch'] for q in OFF}
assert len(IDM) == TOT
CH = [{'c': c, 'nm': CT[c], 'n16': c16[c], 'n5': c5[c], 'p': PRED[c], 'bank': c16[c],
       'd': DRILL[c[0]], 'r': READ[c][0], 'rn': READ[c][1]} for c in sorted(CT)]

CSS = """<style id="hit-css">
/* 日拱一築（民法版）；五組貓系色卡由 body[data-pal] 切換（頁首色帶與面板共用），存 bxm-hit-pal */
#hitPanel{margin:0 0 18px}
body, body[data-pal="p1"]{
  --cp-got:#4E5F4A;--cp-got-t:#ECD9B9;--cp-pick:#8FA083;--cp-pick-t:#28331F;
  --cp-unk:#ECD9B9;--cp-unk-t:#4E5F4A;--cp-accent:#4E5F4A;--cp-accent-t:#ECD9B9;
  --cp-card:#FFFDF7;--cp-milk:#F6F1E4;--cp-line:#DCD3C0;--cp-ink:#2F3A2C;--cp-soft:#6E7A68;--cp-track:#E6DECB;}
body[data-pal="p2"]{--cp-got:#4A3028;--cp-got-t:#FFF1D0;--cp-pick:#F28C28;--cp-pick-t:#4A3028;
  --cp-unk:#FFF1D0;--cp-unk-t:#4A3028;--cp-accent:#F28C28;--cp-accent-t:#4A3028;
  --cp-card:#FFFBF2;--cp-milk:#FFF1D0;--cp-line:#E7D8BC;--cp-ink:#3A2720;--cp-soft:#8A6F5E;--cp-track:#F3E4C9;}
body[data-pal="p3"]{--cp-got:#4B5D6B;--cp-got-t:#E8EFF7;--cp-pick:#7F8FA6;--cp-pick-t:#1F2A33;
  --cp-unk:#C7D3E3;--cp-unk-t:#3A4753;--cp-accent:#4B5D6B;--cp-accent-t:#E8EFF7;
  --cp-card:#FBFCFE;--cp-milk:#EEF3F9;--cp-line:#CFDAE7;--cp-ink:#273039;--cp-soft:#6B7A8A;--cp-track:#DEE6F0;}
body[data-pal="p4"]{--cp-got:#030303;--cp-got-t:#FFFFFF;--cp-pick:#F58220;--cp-pick-t:#1A0C00;
  --cp-unk:#ECECEC;--cp-unk-t:#333333;--cp-accent:#F58220;--cp-accent-t:#1A0C00;
  --cp-card:#FFFFFF;--cp-milk:#F6F6F6;--cp-line:#DCDCDC;--cp-ink:#1A1A1A;--cp-soft:#6E6E6E;--cp-track:#ECECEC;}
body[data-pal="p5"]{--cp-got:#3A3A3A;--cp-got-t:#EFE8DE;--cp-pick:#A89B8A;--cp-pick-t:#2A251F;
  --cp-unk:#D6C8B6;--cp-unk-t:#4A423A;--cp-accent:#3A3A3A;--cp-accent-t:#EFE8DE;
  --cp-card:#FDFBF7;--cp-milk:#F2ECE3;--cp-line:#DED4C6;--cp-ink:#2F2B26;--cp-soft:#7A7167;--cp-track:#E6DCCE;}
[data-theme="dark"] body{--cp-card:#1F2723;--cp-milk:#263029;--cp-line:#33403A;--cp-ink:#E7ECE6;--cp-soft:#A5B1A8;--cp-track:#2C3832;--cp-accent:#8FA083;--cp-accent-t:#1A2214}
[data-theme="dark"] body[data-pal="p2"]{--cp-accent:#F28C28;--cp-accent-t:#4A3028;--cp-card:#2A211C;--cp-milk:#352A22;--cp-line:#45372C;--cp-ink:#F2E4D0;--cp-soft:#B59B84;--cp-track:#3C2F26}
[data-theme="dark"] body[data-pal="p3"]{--cp-accent:#7F8FA6;--cp-accent-t:#0E141A;--cp-card:#1F262C;--cp-milk:#273038;--cp-line:#333F49;--cp-ink:#E4ECF4;--cp-soft:#90A0B0;--cp-track:#2C353E}
[data-theme="dark"] body[data-pal="p4"]{--cp-accent:#F58220;--cp-accent-t:#1A0C00;--cp-card:#171717;--cp-milk:#202020;--cp-line:#303030;--cp-ink:#F2F2F2;--cp-soft:#9A9A9A;--cp-track:#272727}
[data-theme="dark"] body[data-pal="p5"]{--cp-accent:#A89B8A;--cp-accent-t:#2A251F;--cp-card:#232120;--cp-milk:#2C2926;--cp-line:#3A3531;--cp-ink:#EFE8DE;--cp-soft:#A3978A;--cp-track:#302C28}
#hitPanel .hscore{background:var(--cp-card);border:1.5px solid var(--cp-line);border-radius:12px;padding:15px 15px 13px;margin-bottom:11px;color:var(--cp-ink)}
#hitPanel .hscore h3{margin:0 0 2px;font-size:1.06rem;display:flex;align-items:center;gap:7px;position:relative;padding-right:34px;letter-spacing:.04em}
#hitPanel .motto{font-size:.8rem;color:var(--cp-accent);font-weight:700;margin:1px 0 7px}
#hitPanel .ssub{font-size:.76rem;color:var(--cp-soft);margin-bottom:12px;line-height:1.6}
#hitPanel .palbtn{position:absolute;right:-2px;top:-3px;width:28px;height:28px;border-radius:50%;cursor:pointer;border:1.5px solid var(--cp-line);background:var(--cp-milk);font-size:.85rem;line-height:1;display:grid;place-items:center;padding:0;color:var(--cp-soft)}
#hitPanel .palbtn.on{background:var(--cp-accent);border-color:var(--cp-accent);color:var(--cp-accent-t)}
#hitPanel .palrow{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-bottom:11px;font-size:.76rem;color:var(--cp-soft);background:var(--cp-milk);border:1.5px solid var(--cp-line);border-radius:10px;padding:9px 11px}
#hitPanel .palrow[hidden]{display:none!important}
#hitPanel .palrow button{display:flex;align-items:center;padding:3px;border-radius:999px;cursor:pointer;border:2px solid var(--cp-line);background:var(--cp-card)}
#hitPanel .palrow button.on{border-color:var(--cp-ink)}
#hitPanel .palrow button i{display:block;width:17px;height:17px;border-radius:50%;margin-left:-5px;border:1.5px solid var(--cp-card)}
#hitPanel .palrow button i:first-child{margin-left:0}
#hitPanel .sbar{display:flex;height:34px;border-radius:9px;overflow:hidden;background:var(--cp-track);margin-bottom:10px}
#hitPanel .sbar div{display:grid;place-items:center;font-size:.82rem;font-weight:800;min-width:0;font-variant-numeric:tabular-nums}
#hitPanel .sbar .got{background:var(--cp-got);color:var(--cp-got-t)}
#hitPanel .sbar .pick{background:var(--cp-pick);color:var(--cp-pick-t)}
#hitPanel .sbar .unk{background:var(--cp-unk);color:var(--cp-unk-t)}
#hitPanel .skey{display:grid;gap:5px;font-size:.81rem;line-height:1.5}
#hitPanel .skey span{display:flex;align-items:center;gap:8px}
#hitPanel .skey i{width:11px;height:11px;border-radius:3px;flex:none}
#hitPanel .skey b{font-variant-numeric:tabular-nums;font-size:.88rem}
#hitPanel .skey small{color:var(--cp-soft);font-size:.75rem}
#hitPanel .howbtn{width:100%;font:inherit;font-size:.76rem;font-weight:700;padding:7px;border-radius:8px;cursor:pointer;background:transparent;color:var(--cp-soft);border:1.5px dashed var(--cp-line);margin-top:10px}
#hitPanel .defs2{font-size:.76rem;color:var(--cp-soft);line-height:1.75;background:var(--cp-milk);border-radius:8px;padding:9px 11px;margin-top:9px}
#hitPanel .htoday{background:var(--cp-card);border:1.5px solid var(--cp-line);border-left:6px solid var(--cp-accent);border-radius:12px;padding:14px 15px;margin-bottom:11px;color:var(--cp-ink)}
#hitPanel .htoday .htag{font-size:.73rem;font-weight:800;letter-spacing:.05em;color:var(--cp-accent);margin-bottom:4px}
#hitPanel .htoday h4{margin:0;font-size:1.1rem;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
#hitPanel .htoday .gain{background:var(--cp-accent);color:var(--cp-accent-t);font-size:.8rem;font-weight:800;padding:3px 10px;border-radius:999px;font-variant-numeric:tabular-nums;margin-left:auto}
#hitPanel .htoday p{margin:9px 0 11px;font-size:.84rem;line-height:1.7}
#hitPanel .htoday p b{color:var(--cp-accent)}
#hitPanel .acts{display:flex;gap:7px;flex-wrap:wrap}
#hitPanel .acts a{font-size:.78rem;font-weight:700;text-decoration:none;padding:7px 13px;border-radius:999px;border:1.5px solid var(--cp-line);color:var(--cp-ink);background:var(--cp-milk)}
#hitPanel .acts a.go{background:var(--cp-got);border-color:var(--cp-got);color:var(--cp-got-t)}
#hitPanel .nextup{font-size:.79rem;color:var(--cp-soft);margin:0 0 12px;line-height:1.8;padding:0 3px}
#hitPanel .nextup b{color:var(--cp-ink)}
#hitPanel .more{width:100%;font:inherit;font-size:.8rem;font-weight:700;padding:10px;border-radius:9px;cursor:pointer;background:var(--cp-milk);color:var(--cp-soft);border:1.5px solid var(--cp-line)}
#hitPanel .slim{background:var(--cp-card);border:1.5px solid var(--cp-line);border-radius:10px;overflow:hidden}
#hitPanel .slim details{border-top:1px solid var(--cp-line)}
#hitPanel .slim details:first-child{border-top:0}
#hitPanel .slim summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:9px 11px;font-size:.82rem;color:var(--cp-ink)}
#hitPanel .slim summary::-webkit-details-marker{display:none}
#hitPanel .slim summary:hover{background:var(--cp-milk)}
#hitPanel .sl-dot{width:7px;height:7px;border-radius:50%;flex:none;background:var(--cp-got)}
#hitPanel .sl-dot.hi{background:var(--cp-pick)}
#hitPanel .sl-dot.un{background:var(--cp-unk)}
#hitPanel .sl-name{font-weight:700;flex:none}
#hitPanel .sl-mini{flex:1;height:6px;border-radius:4px;background:var(--cp-track);overflow:hidden;min-width:24px}
#hitPanel .sl-mini i{display:block;height:100%;background:var(--cp-pick)}
#hitPanel .sl-num{font-size:.78rem;color:var(--cp-soft);font-variant-numeric:tabular-nums;flex:none}
#hitPanel .sl-num b{color:var(--cp-ink)}
#hitPanel .sl-body{padding:0 11px 11px;font-size:.79rem;line-height:1.7;color:var(--cp-ink)}
/* A 版全章表：章節｜115 出題｜測過多少｜還沒到手｜先做什麼（沒有「真會率」欄） */
#hitPanel .atb{width:100%;border-collapse:collapse;font-size:.8rem;color:var(--cp-ink);background:var(--cp-card);
  border:1.5px solid var(--cp-line);border-radius:10px;overflow:hidden}
#hitPanel .atb th{background:var(--cp-milk);color:var(--cp-soft);font-size:.74rem;font-weight:700;
  text-align:left;padding:8px 9px;border-bottom:1.5px solid var(--cp-line);white-space:nowrap}
#hitPanel .atb td{padding:9px;border-bottom:1px solid var(--cp-line);vertical-align:top;line-height:1.6}
#hitPanel .atb tr:last-child td{border-bottom:0}
#hitPanel .atb .cc{font-weight:800}
#hitPanel .atb .hcn{display:block;color:var(--cp-soft);font-size:.74rem;font-weight:400}
#hitPanel .atb .num{font-variant-numeric:tabular-nums;white-space:nowrap}
#hitPanel .atb .left b{font-size:.92rem}
#hitPanel .atb .mini{display:flex;height:9px;border-radius:5px;overflow:hidden;background:var(--cp-track);min-width:56px}
#hitPanel .atb .mini i{display:block;height:100%}
#hitPanel .atb .mini .g{background:var(--cp-got)}
#hitPanel .atb .mini .p{background:var(--cp-pick)}
#hitPanel .atb .mini .s{background:var(--cp-unk)}
#hitPanel .atb .cov{display:block;color:var(--cp-soft);font-size:.73rem;margin-top:3px;font-variant-numeric:tabular-nums}
#hitPanel .atb .do b{display:block}
#hitPanel .atb .do small{color:var(--cp-soft);font-size:.74rem;line-height:1.55;display:block;margin-top:2px}
#hitPanel .atb .lk{display:inline-block;margin-top:5px;margin-right:6px;font-size:.74rem;font-weight:700;
  text-decoration:none;color:var(--cp-ink);background:var(--cp-milk);border:1.5px solid var(--cp-line);
  border-radius:999px;padding:3px 9px}
@media(max-width:620px){
  #hitPanel .atb,#hitPanel .atb tbody,#hitPanel .atb tr,#hitPanel .atb td{display:block;width:100%}
  #hitPanel .atb thead{display:none}
  #hitPanel .atb tr{border-bottom:1.5px solid var(--cp-line);padding:3px 0}
  #hitPanel .atb tr:last-child{border-bottom:0}
  #hitPanel .atb td{border-bottom:0;padding:4px 10px;display:flex;gap:9px;align-items:flex-start}
  #hitPanel .atb td:first-child{padding-top:10px}
  #hitPanel .atb td:last-child{padding-bottom:11px;flex-direction:column;gap:0}
  #hitPanel .atb td::before{content:attr(data-l);flex:none;width:68px;color:var(--cp-soft);font-size:.73rem;padding-top:1px}
  #hitPanel .atb td:last-child::before{width:auto;margin-bottom:2px}
  #hitPanel .atb .mini{flex:1}
}
</style>"""

JS = r"""<script id="hit-js">
(function(){
var CH=__CHJSON__;
var IDM=__IDMJSON__;
var KN={A:['法條混淆','兩條記混了。去讀整理頁把兩條並排看，不要只重刷題。'],
 B:['粗心','會但看錯。作答時先圈題幹的「錯誤／不正確／不包括」再看選項。'],
 C:['真的不熟','還沒讀懂。先讀整理頁再回來刷，直接刷只是重複猜。'],
 D:['用猜的','等於還沒會。把猜對的也當錯題處理。']};
var PALS=[['p1','Forest Paws','#4E5F4A','#8FA083','#ECD9B9'],
 ['p2','Orange Cat','#4A3028','#F28C28','#FFF1D0'],
 ['p3','Blue-Eyed Kitty','#4B5D6B','#7F8FA6','#C7D3E3'],
 ['p4','Garfield','#030303','#F58220','#ECECEC'],
 ['p5','Muzzle Taupe','#3A3A3A','#A89B8A','#D6C8B6']];
function pal(){try{return localStorage.getItem('bxm-hit-pal')||'p1'}catch(e){return 'p1'}}
function esc(t){return String(t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function fx(n){return (Math.round(n*10)/10).toFixed(1)}
function pc(n){return Math.round(n*100)}
function draw(){
  var box=document.getElementById('hitBody'); if(!box) return;
  document.body.setAttribute('data-pal',pal());
  var openPal=!!(box.querySelector('.palrow')&&!box.querySelector('.palrow').hidden);
  var openAll=!!(box.querySelector('#hitAll')&&!box.querySelector('#hitAll').hidden);
  var raw={}; try{raw=JSON.parse(localStorage.getItem('bxm-q2')||'{}')}catch(e){}
  var by={};
  Object.keys(raw).forEach(function(id){
    var r=raw[id]; if(!r||typeof r!=='object') return;
    var c=IDM[id]; if(!c) return;      /* bxm-q2 的 id＝刷題篇別-年-題，換成 28 小類 */
    var o=by[c]=by[c]||{a:0,sure:0,w:0,soft:0,k:{A:0,B:0,C:0,D:0,'':0}};
    o.a++;
    /* 真會率的分子：答對、且沒標「D 猜的」、沒按 🎲（g=1）、也沒按 🤔 對了但不熟（sh=1） */
    if(r.ok){ if(r.k==='D'||r.g===1||r.sh===1){o.soft++}else{o.sure++} }
    else { o.w++; o.k[r.k||'']=(o.k[r.k||'']||0)+1 }
  });
  var rows=[],okT=0,needT=0,seedT=0,doneT=0,bankT=0,anyAns=false;
  CH.forEach(function(x){
    var s=by[x.c]||{a:0,sure:0,w:0,soft:0,k:{}};
    var bank=x.bank||x.n16||0;
    var done=bank?Math.min(s.a,bank):s.a;
    var cov=bank?done/bank:0;              /* 覆蓋率：這章題庫測過幾成 */
    var rate=s.a?s.sure/s.a:0;             /* 真會率：測過的裡面真的會幾成 */
    var ok=x.p*cov*rate, need=x.p*cov*(1-rate), seed=x.p*(1-cov);
    okT+=ok; needT+=need; seedT+=seed; doneT+=done; bankT+=bank;
    if(s.a)anyAns=true;
    var kk='',kn=0; ['A','B','C','D'].forEach(function(t){ if((s.k[t]||0)>kn){kn=s.k[t];kk=t} });
    rows.push({x:x,bank:bank,done:done,cov:cov,rate:rate,ok:ok,need:need,seed:seed,
               left:need+seed,a:s.a,w:s.w,soft:s.soft,kk:kk,kn:kn});
  });
  rows.sort(function(a,b){return b.left-a.left||b.x.p-a.x.p});   /* 依「還沒到手」排 */
  var gotP=okT*2, pickP=needT*2, unkP=seedT*2;
  /* 先做什麼：嚴格版——只有測過七成以上、且全對又沒有不確定，才准說「維持就好」 */
  function todo(r){
    if(r.cov>=0.7&&r.w===0&&r.soft===0&&r.a>0)
      return ['維持就好','已經測過 '+pc(r.cov)+'%，全對、也沒有不確定的。考前再刷一輪確認就好。'];
    if(r.cov<0.3)
      return [r.a?'先刷一輪':'還沒開始','只測了 '+pc(r.cov)+'%（'+r.done+'/'+r.bank+' 題），現在的數字還不準。先刷一輪把底掀開。'];
    if(r.kk) return ['補「'+KN[r.kk][0]+'」',KN[r.kk][1]+'（'+r.kn+' 題）'];
    if(r.w>0) return ['先標錯題類型','有 '+r.w+' 題答錯還沒標 A／B／C／D，標了才知道要補法條還是補觀念。'];
    if(r.soft>0) return ['回頭確認 '+r.soft+' 題','這些是「對了但不熟」或用猜的，等於還沒會。先讀整理頁再回來刷。'];
    return ['把剩下的刷完','測過 '+pc(r.cov)+'%，目前都站得住，繼續把這章刷滿。'];
  }
  var h='<div class="hscore"><h3><span>🐾</span>日拱一築'
    +'<button class="palbtn'+(openPal?' on':'')+'" id="hitPalBtn" title="換色卡" aria-label="換色卡">🎨</button></h3>'
    +'<div class="palrow"'+(openPal?'':' hidden')+'>色卡：'+PALS.map(function(x){
      return '<button data-hpal="'+x[0]+'"'+(pal()===x[0]?' class="on"':'')+' title="'+x[1]+'">'
        +'<i style="background:'+x[2]+'"></i><i style="background:'+x[3]+'"></i><i style="background:'+x[4]+'"></i></button>'}).join('')
    +'<span id="hitPalName">'+((PALS.filter(function(x){return x[0]===pal()})[0]||PALS[0])[1])+'</span></div>'
    +'<div class="motto">藏分於日 —— 今天拿回來的分，考場上就是你的</div>';
  if(!anyAns){
    h+='<div class="ssub">還沒有作答紀錄。整個 50 分現在都是 <b>🌰 等待發芽</b>——不是「會」也不是「不會」，是還沒測過。'
      +'先去任一章刷一輪，這張圖就會長出來。</div>';
  }else{
    h+='<div class="ssub">你的選擇題 50 分現在長這樣。<b>沒測過的題一律算「等待發芽」，不會被當成你會</b>。申論另外 50 分不在這張圖裡。</div>'
      +'<div class="sbar">'
      +(gotP>0.5?'<div class="got" style="flex:'+gotP+'">'+Math.round(gotP)+'</div>':'')
      +(pickP>0.5?'<div class="pick" style="flex:'+pickP+'">'+Math.round(pickP)+'</div>':'')
      +(unkP>0.5?'<div class="unk" style="flex:'+unkP+'">'+Math.round(unkP)+'</div>':'')
      +'</div>';
  }
  h+='<div class="skey">'
    +'<span><i style="background:var(--cp-got)"></i>🌟 穩穩收下 <b>'+fx(gotP)+' 分</b>　<small>測過而且真的會</small></span>'
    +'<span><i style="background:var(--cp-pick)"></i>🌱 還能追回 <b>'+fx(pickP)+' 分</b>　<small>測過但答錯、用猜的或不熟</small></span>'
    +'<span><i style="background:var(--cp-unk)"></i>🌰 等待發芽 <b>'+fx(unkP)+' 分</b>　<small>還沒測過的題，實力未知</small></span>'
    +'</div><button class="howbtn" id="hitHow">這三個數字怎麼算出來的？</button>'
    +'<div class="defs2" id="hitDefs" hidden>每章先算 <b>115 年預估出幾題</b>＝25 題×（16 年占比×0.5＋近 5 年〔110–114〕占比×0.5），28 章合計 25 題。'
    +'再用兩個比率把它切三段：<b>覆蓋率</b>＝這章題庫你測過幾成、<b>真會率</b>＝測過的裡面答對且沒標「不熟／猜的」占幾成。'
    +'<br>🌟 ＝ 預估題數 × 覆蓋率 × 真會率；🌱 ＝ 預估題數 × 覆蓋率 ×（1－真會率）；🌰 ＝ 預估題數 ×（1－覆蓋率）。每題 2 分，三段相加恆為 50 分。'
    +'<br>目前全科測過 <b>'+doneT+'／'+bankT+'</b> 題（'+pc(bankT?doneT/bankT:0)+'%）。這是依你自己的作答推估，不是命中率預測。</div></div>';
  if(anyAns||rows.length){
    var t=rows[0],td=todo(t);
    h+='<div class="htoday"><div class="htag">今天從這章開始</div>'
      +'<h4>'+esc(t.x.nm)+'<span class="gain">還沒到手 '+fx(t.left*2)+' 分</span></h4>'
      +'<p><b>'+esc(td[0])+'</b>　'+td[1]+'<br>這章 115 年預估出 '+fx(t.x.p)+' 題，題庫 '+t.bank+' 題、你測過 '+t.done+' 題（'+pc(t.cov)+'%）。</p>'
      +'<div class="acts"><a class="go" href="'+t.x.d+'">去刷這章 ▸</a>'
      +'<a href="'+t.x.r+'">讀 '+esc(t.x.rn)+' ▸</a>'
      +'<a href="民法_法條解析練習.html#ch='+t.x.c+'">混合練這章 ▸</a></div></div>';
    var nx='';
    if(rows[1]) nx+='練完接著：<b>'+esc(rows[1].x.nm)+'</b>（'+fx(rows[1].left*2)+' 分）';
    if(rows[2]) nx+='、<b>'+esc(rows[2].x.nm)+'</b>（'+fx(rows[2].left*2)+' 分）';
    if(nx) h+='<p class="nextup">'+nx+'。前三章就占 '+fx((rows[0].left+(rows[1]?rows[1].left:0)+(rows[2]?rows[2].left:0))*2)+' 分。</p>';
  }
  h+='<button class="more" id="hitMore">'+(openAll?'收起 ▴':'看全部 '+rows.length+' 章 ▾')+'</button>'
    +'<div id="hitAll"'+(openAll?'':' hidden')+' style="margin-top:10px">'
    +'<table class="atb"><thead><tr><th>章節</th><th>115 出題</th><th>測過多少</th><th>還沒到手</th><th>先做什麼</th></tr></thead><tbody>';
  rows.forEach(function(r){
    var td=todo(r),tot=r.x.p||1;
    h+='<tr>'
      +'<td data-l="章節"><span><span class="cc">'+esc(r.x.c)+'</span><span class="hcn">'+esc(r.x.nm.replace(/^\S+\s*/,''))+'</span></span></td>'
      +'<td data-l="115 出題" class="num">'+fx(r.x.p)+' 題</td>'
      +'<td data-l="測過多少"><span style="flex:1;min-width:0"><span class="mini">'
        +'<i class="g" style="flex:'+(r.ok/tot)+'"></i><i class="p" style="flex:'+(r.need/tot)+'"></i><i class="s" style="flex:'+(r.seed/tot)+'"></i>'
        +'</span><span class="cov">'+r.done+'/'+r.bank+' 題・'+pc(r.cov)+'%</span></span></td>'
      +'<td data-l="還沒到手" class="num left"><b>'+fx(r.left*2)+' 分</b></td>'
      +'<td data-l="先做什麼" class="do"><b>'+esc(td[0])+'</b><small>'+td[1]+'</small>'
        +'<span><a class="lk" href="'+r.x.d+'">去刷 ▸</a>'
        +'<a class="lk" href="'+r.x.r+'">讀整理頁 ▸</a>'
        +'<a class="lk" href="民法_法條解析練習.html#ch='+r.x.c+'">混合練 ▸</a></span></td>'
      +'</tr>';
  });
  h+='</tbody></table></div>';
  box.innerHTML=h;
}
draw();
document.addEventListener('click',function(e){
  var box=document.getElementById('hitPanel'); if(!box||!box.contains(e.target)) return;
  var pb=e.target.closest('.palrow [data-hpal]');
  if(pb){
    var v=pb.getAttribute('data-hpal');
    try{localStorage.setItem('bxm-hit-pal',v)}catch(err){}
    document.body.setAttribute('data-pal',v);
    box.querySelectorAll('.palrow [data-hpal]').forEach(function(x){x.classList.toggle('on',x.getAttribute('data-hpal')===v)});
    var n=document.getElementById('hitPalName');
    if(n){var f=PALS.filter(function(x){return x[0]===v})[0]; if(f)n.textContent=f[1]}
    return;
  }
  if(e.target.id==='hitPalBtn'){var row=box.querySelector('.palrow');row.hidden=!row.hidden;e.target.classList.toggle('on',!row.hidden);return}
  if(e.target.id==='hitHow'){var d=document.getElementById('hitDefs');d.hidden=!d.hidden;e.target.textContent=d.hidden?'這三個數字怎麼算出來的？':'收起說明 ▴';return}
  if(e.target.id==='hitMore'){var a=document.getElementById('hitAll');a.hidden=!a.hidden;e.target.textContent=a.hidden?'看全部 '+CH.length+' 章 ▾':'收起 ▴';return}
});
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')draw()});
addEventListener('focus',draw);
function hitHash(){var hs=location.hash;if(hs==='#hit'||hs==='#progress'||hs==='#rev'){
  try{goTab('pProg')}catch(e){}
  if(hs==='#hit'){var el=document.getElementById('hitPanel');if(el)setTimeout(function(){el.scrollIntoView({behavior:'smooth',block:'start'})},120)}}}
if(location.hash)setTimeout(hitHash,180);
addEventListener('hashchange',hitHash);
})();
</script>""".replace('__CHJSON__', json.dumps(CH, ensure_ascii=False)).replace('__IDMJSON__', json.dumps(IDM, ensure_ascii=False, separators=(',',':')))

# ── 進度落後清單（施工單第 8 項，移植估價 v527）：放在 #hitPanel 內，共用同一張色卡 ──
LAG_CSS = """<style id="lag-css">
#lagPanel{margin:14px 0 0}
#lagPanel .lg{background:var(--cp-card);border:1.5px solid var(--cp-line);border-radius:12px;padding:14px 15px;color:var(--cp-ink)}
#lagPanel h3{margin:0 0 3px;font-size:1.04rem;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
#lagPanel h3 .d{margin-left:auto;background:var(--cp-accent);color:var(--cp-accent-t);font-size:.76rem;font-weight:800;border-radius:999px;padding:2px 10px;font-variant-numeric:tabular-nums}
#lagPanel .goal{font-size:.76rem;color:var(--cp-soft);margin-bottom:10px;line-height:1.6}
#lagPanel table{border-collapse:collapse;width:100%;font-size:.81rem;font-variant-numeric:tabular-nums}
#lagPanel th,#lagPanel td{padding:7px 8px;text-align:left;border-top:1px solid var(--cp-line)}
#lagPanel thead th{border-top:0;background:var(--cp-milk);font-size:.72rem;color:var(--cp-soft);letter-spacing:.04em;font-weight:800;white-space:nowrap}
#lagPanel td.n{text-align:right;white-space:nowrap}
#lagPanel .pb{display:inline-flex;height:8px;width:100%;min-width:50px;max-width:110px;border-radius:5px;overflow:hidden;background:var(--cp-track);vertical-align:middle}
#lagPanel .pb i{display:block;height:100%;background:var(--cp-got)}
#lagPanel .need{font-weight:800;color:var(--cp-accent)}
#lagPanel .zero{color:var(--cp-soft)}
#lagPanel .names{margin:11px 0 0;padding:10px 12px;border-radius:9px;background:var(--cp-milk);font-size:.79rem;line-height:1.85}
#lagPanel .names a{color:var(--cp-ink);font-weight:700;text-decoration:none;border-bottom:1.5px solid var(--cp-pick)}
#lagPanel .names .lab{font-weight:800;color:var(--cp-accent);display:block;font-size:.73rem;letter-spacing:.05em;margin-bottom:3px}
@media(max-width:560px){
  #lagPanel table,#lagPanel tbody,#lagPanel tr,#lagPanel td{display:block;width:100%}
  #lagPanel thead{display:none}
  #lagPanel tr{border-top:1px solid var(--cp-line);padding:6px 0}
  #lagPanel td{border:0;padding:2px 2px;display:flex;gap:8px;align-items:center}
  #lagPanel td.n{text-align:left}
  #lagPanel td::before{content:attr(data-l);flex:none;width:60px;color:var(--cp-soft);font-size:.72rem}
  #lagPanel td:first-child{font-weight:800}
  #lagPanel td:first-child::before{display:none}
  #lagPanel td:empty{display:none}
}
</style>"""
LAG_JS = r"""<script id="lag-js">
/* 進度落後清單：目標＝考前把每一樣至少做完 1 輪；每天要＝剩餘量÷剩餘天數。只讀，不寫任何鍵。 */
(function(){
function lagBuild(){
  var box=document.getElementById('lagPanel'); if(!box) return;
  if(typeof BXREP==='undefined'||!BXREP.status){box.innerHTML='';return;}
  var exam=new Date('2026-11-14T09:00:00+08:00');
  var days=Math.max(1,Math.ceil((exam-new Date())/86400000));
  var G=BXREP.status();
  function grp(n){for(var i=0;i<G.length;i++)if(G[i].g.indexOf(n)===0)return G[i];return null}
  function rows(g){return g?g.rows:[]}
  var drill=grp('刷題'),mock=grp('模擬卷'),read=grp('閱讀頁'),mem=grp('記憶工具');
  var dDone=0,dTot=0;rows(drill).forEach(function(r){if(r.total>0&&r.name.indexOf('刷題 ')===0){dDone+=r.done;dTot+=r.total}});
  var esRead=0;try{var M=JSON.parse(localStorage.getItem('minfa_read')||'{}');Object.keys(M).forEach(function(k){if(M[k])esRead++})}catch(e){}
  var rTot=rows(read).length,rDone=rows(read).filter(function(r){return (r.read||0)>0}).length;
  var mRows=rows(mock).filter(function(r){return r.total>0}),mTot=0,mDone=0;
  /* 歷屆整卷一列＝8 卷（done／total 就是卷數）；其餘每列 1 份，答完才算 */
  mRows.forEach(function(r){if(r.p==='民法概要_25題模擬測驗'){mTot+=r.total;mDone+=Math.min(r.done,r.total)}else{mTot++;if(r.done>=r.total)mDone++}});
  var kRows=rows(mem).filter(function(r){return r.total>0}),kDone=0,kTot=0;kRows.forEach(function(r){kDone+=Math.min(r.done,r.total);kTot+=r.total});
  function per(rem){return rem<=0?'已完成':(Math.ceil(rem/days)+' / 天')}
  function bar(d,t){var p=t?Math.min(100,Math.round(d/t*100)):0;return '<span class="pb"><i style="width:'+p+'%"></i></span>'}
  function row(nm,d,t,u,note){var rem=Math.max(0,t-d);
    return '<tr><td>'+nm+'</td><td class="n" data-l="目前">'+d+'／'+t+' '+u+'</td><td data-l="完成度">'+bar(d,t)+'</td>'
      +'<td class="n '+(rem?'need':'zero')+'" data-l="每天要">'+per(rem)+'</td><td class="zero" data-l="備註">'+(note||'')+'</td></tr>'}
  var h='<div class="lg"><h3><span>⏳</span>進度落後在哪<span class="d">剩 '+days+' 天</span></h3>'
    +'<div class="goal">目標：<b>考前把每一樣至少做完 1 輪</b>。「每天要」＝剩下的量 ÷ 剩下的天數，沒有另外訂讀書表。</div>'
    +'<table><thead><tr><th>項目</th><th class="n">目前</th><th>完成度</th><th class="n">每天要</th><th>備註</th></tr></thead><tbody>'
    +row('選擇題（A～E 篇）',dDone,dTot,'題','法條解析練習的作答也算在這裡')
    +row('申論 73 題',esRead,73,'題','在申論卡按「已讀」')
    +row('閱讀／整理頁',rDone,rTot,'頁','讀完一輪＝按＋，或捲到該頁最底')
    +row('模擬卷',mDone,mTot,'份','歷屆整卷 8 卷＋自擬 2 份＋來勝 1 份')
    +row('記憶工具（已掌握）',kDone,kTot,'張','小卡、單字卡自己標「已掌握」；填空按完成')
    +'</tbody></table>';
  var zero=[];
  rows(drill).forEach(function(r){if(r.total>0&&r.name.indexOf('刷題 ')===0&&r.done===0)zero.push({n:r.name,u:r.url})});
  rows(read).forEach(function(r){if(!r.read)zero.push({n:r.name,u:r.url})});
  mRows.forEach(function(r){if(!r.done)zero.push({n:r.name,u:r.url})});
  if(zero.length){
    h+='<div class="names"><span class="lab">完全沒開始的 '+zero.length+' 項</span>'
      +zero.slice(0,14).map(function(z){return '<a href="'+z.u+'" target="_blank" rel="noopener">'+z.n+'</a>'}).join('、')
      +(zero.length>14?'　…另 '+(zero.length-14)+' 項':'')+'</div>';
  }else h+='<div class="names"><span class="lab">每一項都已經開始</span>接下來看「每天要」那一欄，把量補上就好。</div>';
  box.innerHTML=h+'</div>';
}
lagBuild();
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')lagBuild()});
addEventListener('focus',lagBuild);
})();
</script>"""

BLOCK = CSS + LAG_CSS + """
<section id="hitPanel">
  <div id="hitBody"></div>
  <div id="lagPanel"></div>
</section>
""" + JS + LAG_JS

s = io.open(HUB, encoding='utf-8').read()
if 'id="hit-css"' in s:
    a = s.index('<style id="hit-css">')
    end = '<script id="lag-js">' if '<script id="lag-js">' in s else '<script id="hit-js">'
    b = s.index('</script>', s.index(end)) + len('</script>')
    s = s[:a] + BLOCK + s[b:]
else:
    anchor = '<section class="tab" id="pProg">\n'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + BLOCK + '\n')
io.open(HUB, 'w', encoding='utf-8').write(s)
print('面板已寫入｜官方題 %d（近5年 %d）｜28 章預估合計 %.2f 題' % (TOT, TOTR, sum(PRED.values())))
for c in sorted(PRED, key=lambda k: -PRED[k]):
    print('   %s %.2f（16年 %d／近5年 %d）' % (c, PRED[c], c16[c], c5[c]))
