# -*- coding: utf-8 -*-
"""《經紀法規_備考指揮中心》「日拱一築」面板（對應估價 v520）。

把「正確率」換算成「115 年預估會掉幾分、先打哪一章」。只讀 bxj-q2，不寫任何鍵。
可重複執行（以 <section id="hitPanel"> 為邊界整段換掉）。
"""
import io, json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
QD = json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))

CT = {"A1":"A1 總則：名詞定義與主管機關","A2":"A2 經紀業設立、保證金與營業處所",
 "A3":"A3 經紀人員：資格、證書與義務","A4":"A4 業務及責任（核心高頻）","A5":"A5 獎懲：行政罰與刑罰",
 "C1":"C1 說明書：土地應記載事項","C2":"C2 說明書：成屋應記載事項","C3":"C3 說明書：預售屋應記載事項",
 "C4":"C4 說明書：不得記載事項","D2":"D2 預售屋買賣定型化契約","D3":"D3 委託銷售定型化契約",
 "E1":"E1 公寓大廈：總則與定義","E2":"E2 公寓大廈：住戶權利義務","E3":"E3 公寓大廈：管理組織與決議",
 "E4":"E4 公寓大廈：規約","E5":"E5 公寓大廈：罰則","F2":"F2 規約範本之法律性質",
 "G1":"G1 公平交易法重要條文","G2":"G2 廣告查核分工原則","H1":"H1 定型化契約規範",
 "H2":"H2 特種交易","H3":"H3 損害賠償與罰則"}

# 章 → (刷題頁, 整理頁, 整理頁顯示名)
DRILL = {'A1':'經紀法規刷題練習_A1A2A3.html','A2':'經紀法規刷題練習_A1A2A3.html',
 'A3':'經紀法規刷題練習_A1A2A3.html','A4':'經紀法規刷題練習_A4.html','A5':'經紀法規刷題練習_A5.html',
 'E1':'經紀法規刷題練習_E1.html','E3':'經紀法規刷題練習_E3.html','G1':'經紀法規刷題練習_G1_1.html',
 'G2':'經紀法規刷題練習_G2.html','H1':'經紀法規刷題練習_H1.html','H3':'經紀法規刷題練習_H3_1.html'}
OTHER = '經紀法規刷題練習_其他小章節.html'
READ = {
 'A1':('經紀法規_定義填空練習.html','定義填空 A 篇'),
 'A2':('經紀法規_程序總整理.html#p1','程序總整理 ① 經紀業生命週期'),
 'A3':('經紀法規_程序總整理.html#p2','程序總整理 ② 經紀人員'),
 'A4':('經紀法規概要_彩色重點速記.html','彩色重點速記（業務與責任）'),
 'A5':('經紀法規_罰則總整理.html','罰則總整理'),
 'C1':('經紀法規_應記載不得記載總整理.html','應記載／不得記載總整理'),
 'C2':('經紀法規_應記載不得記載總整理.html','應記載／不得記載總整理'),
 'C3':('經紀法規_應記載不得記載總整理.html','應記載／不得記載總整理'),
 'C4':('經紀法規_應記載不得記載總整理.html','應記載／不得記載總整理'),
 'D2':('經紀法規_定型化契約專區.html','定型化契約專區'),
 'D3':('經紀法規_定型化契約專區.html','定型化契約專區'),
 'E1':('經紀法規_定義填空練習.html','定義填空 E 篇'),
 'E2':('經紀法規_程序總整理.html#p4','程序總整理 ④ 住戶違規階梯'),
 'E3':('經紀法規_程序總整理.html#p3','程序總整理 ③ 區分所有權人會議'),
 'E4':('經紀法規_應記載不得記載總整理.html','應記載／不得記載總整理（規約）'),
 'E5':('經紀法規_公寓大廈條例罰則整理.html','公寓大廈罰則整理'),
 'F2':('經紀法規_定義填空練習.html','定義填空 F 篇'),
 'G1':('經紀法規_公平法獨占聯合結合整理.html','公平法：獨占・聯合・結合'),
 'G2':('經紀法規_公平法獨占聯合結合整理.html','公平法：廣告與查核'),
 'H1':('經紀法規_定型化契約_無效vs不構成.html','定型化契約：無效 vs 不構成'),
 'H2':('經紀法規_定型化契約專區.html','定型化契約專區（特種交易）'),
 'H3':('經紀法規_公平法消保法罰則整理.html','公平法・消保法罰則整理'),
}

OFF = [q for q in QD['q'] if q.get('sr') != 'mock' and not q.get('oos')]
TOT = len(OFF)
REC = [q for q in OFF if q['y'] >= 110]          # 近 5 年 110–114
TOTR = len(REC)
c16 = collections.Counter(q['ch'] for q in OFF)
c5 = collections.Counter(q['ch'] for q in REC)

PRED = {}
for c in CT:
    PRED[c] = round(25 * (c16[c] / TOT * 0.5 + c5[c] / TOTR * 0.5), 2)
s = sum(PRED.values())
# 四捨五入誤差補到題數最多的章
if abs(s - 25) > 0.001:
    big = max(PRED, key=lambda k: PRED[k])
    PRED[big] = round(PRED[big] + 25 - s, 2)

CH = []
for c in sorted(CT):
    CH.append({'c': c, 'nm': CT[c], 'n16': c16[c], 'n5': c5[c], 'p': PRED[c],
               'd': DRILL.get(c, OTHER), 'r': READ[c][0], 'rn': READ[c][1]})

CSS = """<style id="hit-css">
/* 日拱一築（對應估價 v520）；五組貓系色卡由 #hitPanel[data-pal] 切換，存 bxj-hit-pal */
#hitPanel{margin:0 0 18px}
#hitPanel, #hitPanel[data-pal="p1"]{
  --cp-got:#4E5F4A;--cp-got-t:#ECD9B9;--cp-pick:#8FA083;--cp-pick-t:#28331F;
  --cp-unk:#ECD9B9;--cp-unk-t:#4E5F4A;--cp-accent:#4E5F4A;--cp-accent-t:#ECD9B9;
  --cp-card:#FFFDF7;--cp-milk:#F6F1E4;--cp-line:#DCD3C0;--cp-ink:#2F3A2C;--cp-soft:#6E7A68;--cp-track:#E6DECB;}
#hitPanel[data-pal="p2"]{--cp-got:#4A3028;--cp-got-t:#FFF1D0;--cp-pick:#F28C28;--cp-pick-t:#4A3028;
  --cp-unk:#FFF1D0;--cp-unk-t:#4A3028;--cp-accent:#F28C28;--cp-accent-t:#4A3028;
  --cp-card:#FFFBF2;--cp-milk:#FFF1D0;--cp-line:#E7D8BC;--cp-ink:#3A2720;--cp-soft:#8A6F5E;--cp-track:#F3E4C9;}
#hitPanel[data-pal="p3"]{--cp-got:#4B5D6B;--cp-got-t:#E8EFF7;--cp-pick:#7F8FA6;--cp-pick-t:#1F2A33;
  --cp-unk:#C7D3E3;--cp-unk-t:#3A4753;--cp-accent:#4B5D6B;--cp-accent-t:#E8EFF7;
  --cp-card:#FBFCFE;--cp-milk:#EEF3F9;--cp-line:#CFDAE7;--cp-ink:#273039;--cp-soft:#6B7A8A;--cp-track:#DEE6F0;}
#hitPanel[data-pal="p4"]{--cp-got:#030303;--cp-got-t:#FFFFFF;--cp-pick:#F58220;--cp-pick-t:#1A0C00;
  --cp-unk:#ECECEC;--cp-unk-t:#333333;--cp-accent:#F58220;--cp-accent-t:#1A0C00;
  --cp-card:#FFFFFF;--cp-milk:#F6F6F6;--cp-line:#DCDCDC;--cp-ink:#1A1A1A;--cp-soft:#6E6E6E;--cp-track:#ECECEC;}
#hitPanel[data-pal="p5"]{--cp-got:#3A3A3A;--cp-got-t:#EFE8DE;--cp-pick:#A89B8A;--cp-pick-t:#2A251F;
  --cp-unk:#D6C8B6;--cp-unk-t:#4A423A;--cp-accent:#3A3A3A;--cp-accent-t:#EFE8DE;
  --cp-card:#FDFBF7;--cp-milk:#F2ECE3;--cp-line:#DED4C6;--cp-ink:#2F2B26;--cp-soft:#7A7167;--cp-track:#E6DCCE;}
[data-theme="dark"] #hitPanel{--cp-card:#1F2723;--cp-milk:#263029;--cp-line:#33403A;--cp-ink:#E7ECE6;--cp-soft:#A5B1A8;--cp-track:#2C3832;--cp-accent:#8FA083;--cp-accent-t:#28331F}
[data-theme="dark"] #hitPanel[data-pal="p2"]{--cp-accent:#F28C28;--cp-accent-t:#4A3028;--cp-card:#2A211C;--cp-milk:#352A22;--cp-line:#45372C;--cp-ink:#F2E4D0;--cp-soft:#B59B84;--cp-track:#3C2F26}
[data-theme="dark"] #hitPanel[data-pal="p3"]{--cp-accent:#7F8FA6;--cp-accent-t:#1F2A33;--cp-card:#1F262C;--cp-milk:#273038;--cp-line:#333F49;--cp-ink:#E4ECF4;--cp-soft:#90A0B0;--cp-track:#2C353E}
[data-theme="dark"] #hitPanel[data-pal="p4"]{--cp-accent:#F58220;--cp-accent-t:#1A0C00;--cp-card:#171717;--cp-milk:#202020;--cp-line:#303030;--cp-ink:#F2F2F2;--cp-soft:#9A9A9A;--cp-track:#272727}
[data-theme="dark"] #hitPanel[data-pal="p5"]{--cp-accent:#A89B8A;--cp-accent-t:#2A251F;--cp-card:#232120;--cp-milk:#2C2926;--cp-line:#3A3531;--cp-ink:#EFE8DE;--cp-soft:#A3978A;--cp-track:#302C28}
#hitPanel .score{background:var(--cp-card);border:1.5px solid var(--cp-line);border-radius:12px;padding:15px 15px 13px;margin-bottom:11px;color:var(--cp-ink)}
#hitPanel .score h3{margin:0 0 2px;font-size:1.06rem;display:flex;align-items:center;gap:7px;position:relative;padding-right:34px;letter-spacing:.04em}
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
#hitPanel .today{background:var(--cp-card);border:1.5px solid var(--cp-line);border-left:6px solid var(--cp-accent);border-radius:12px;padding:14px 15px;margin-bottom:11px;color:var(--cp-ink)}
#hitPanel .today .tag{font-size:.73rem;font-weight:800;letter-spacing:.05em;color:var(--cp-accent);margin-bottom:4px}
#hitPanel .today h4{margin:0;font-size:1.1rem;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap}
#hitPanel .today .gain{background:var(--cp-accent);color:var(--cp-accent-t);font-size:.8rem;font-weight:800;padding:3px 10px;border-radius:999px;font-variant-numeric:tabular-nums;margin-left:auto}
#hitPanel .today p{margin:9px 0 11px;font-size:.84rem;line-height:1.7}
#hitPanel .today p b{color:var(--cp-accent)}
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
</style>"""

JS = r"""<script id="hit-js">
(function(){
var CH=__CHJSON__;
var KN={A:['法條混淆','兩條記混了。去讀整理頁把兩條並排看，不要只重刷題。'],
 B:['粗心','會但看錯。作答時先圈題幹的「錯誤／不正確／不包括」再看選項。'],
 C:['真的不熟','還沒讀懂。先讀整理頁再回來刷，直接刷只是重複猜。'],
 D:['用猜的','等於還沒會。把猜對的也當錯題處理。']};
var PALS=[['p1','Forest Paws','#4E5F4A','#8FA083','#ECD9B9'],
 ['p2','Orange Cat','#4A3028','#F28C28','#FFF1D0'],
 ['p3','Blue-Eyed Kitty','#4B5D6B','#7F8FA6','#C7D3E3'],
 ['p4','Garfield','#030303','#F58220','#ECECEC'],
 ['p5','Muzzle Taupe','#3A3A3A','#A89B8A','#D6C8B6']];
function pal(){try{return localStorage.getItem('bxj-hit-pal')||'p1'}catch(e){return 'p1'}}
function esc(t){return String(t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function draw(){
  var box=document.getElementById('hitBody'); if(!box) return;
  var panel=document.getElementById('hitPanel'); panel.setAttribute('data-pal',pal());
  var openPal=!!(box.querySelector('.palrow')&&!box.querySelector('.palrow').hidden);
  var openAll=!!(box.querySelector('#hitAll')&&!box.querySelector('#hitAll').hidden);
  var raw={}; try{raw=JSON.parse(localStorage.getItem('bxj-q2')||'{}')}catch(e){}
  var by={};
  Object.keys(raw).forEach(function(id){
    var r=raw[id]; if(!r||typeof r!=='object') return;
    var c=id.split('-')[0];
    var o=by[c]=by[c]||{a:0,sure:0,w:0,g:0,k:{A:0,B:0,C:0,D:0,'':0}};
    o.a++;
    if(r.ok){ if(r.k==='D'||r.g===1){o.g++}else{o.sure++} }
    else { o.w++; o.k[r.k||'']=(o.k[r.k||'']||0)+1 }
  });
  var rows=[],un=[],estAns=0,lossT=0,doneT=0,bankT=0,unEst=0;
  CH.forEach(function(x){
    var s=by[x.c]; bankT+=x.n16;
    if(!s||!s.a){ un.push(x); unEst+=x.p; return }
    estAns+=x.p; doneT+=Math.min(s.a,x.n16||s.a);
    var rr=s.sure/s.a, ls=x.p*(1-rr); lossT+=ls;
    var kk='',kn=0; ['A','B','C','D'].forEach(function(t){ if((s.k[t]||0)>kn){kn=s.k[t];kk=t} });
    rows.push({x:x,a:s.a,w:s.w,g:s.g,rr:rr,ls:ls,kk:kk,kn:kn,thin:(s.a<8||(x.n16&&s.a/x.n16<0.25))});
  });
  rows.sort(function(a,b){return b.ls-a.ls||b.x.p-a.x.p});
  un.sort(function(a,b){return b.p-a.p});
  var gotP=(estAns-lossT)*2, pickP=lossT*2, unkP=unEst*2;
  var maxL=rows.length?rows[0].ls:1;
  function why(r){
    if(r.w===0&&r.g===0) return '這章目前全對、也沒有用猜的。<b>先放著</b>，考前再刷一輪確認就好。';
    if(r.kk) return '卡在：<b>'+KN[r.kk][0]+'</b>（'+r.kn+' 題）。'+KN[r.kk][1];
    if(r.w>0) return '有 <b>'+r.w+'</b> 題答錯但還沒標錯誤類型。先去錯題本標 A／B／C／D，才知道要補法條還是補觀念。';
    return '答對的裡面有 <b>'+r.g+'</b> 題是猜的，等於還沒會。先讀整理頁再回來刷。';
  }
  function gain(r){return (r.ls*2).toFixed(1)}
  var h='<div class="score"><h3><span>🐾</span>日拱一築'
    +'<button class="palbtn'+(openPal?' on':'')+'" id="hitPalBtn" title="換色卡" aria-label="換色卡">🎨</button></h3>'
    +'<div class="palrow"'+(openPal?'':' hidden')+'>色卡：'+PALS.map(function(x){
      return '<button data-hpal="'+x[0]+'"'+(pal()===x[0]?' class="on"':'')+' title="'+x[1]+'">'
        +'<i style="background:'+x[2]+'"></i><i style="background:'+x[3]+'"></i><i style="background:'+x[4]+'"></i></button>'}).join('')
    +'<span id="hitPalName">'+((PALS.filter(function(x){return x[0]===pal()})[0]||PALS[0])[1])+'</span></div>'
    +'<div class="motto">藏分於日 —— 今天拿回來的分，考場上就是你的</div>';
  if(!rows.length){
    h+='<div class="ssub">還沒有作答紀錄，先去任一章刷題，這裡就會算出你的 50 分現在長什麼樣，並挑出今天從哪一章開始。</div></div>';
  }else{
    h+='<div class="ssub">你的選擇題 50 分現在長這樣，依已經作答的題推估。申論另外 50 分不在這張圖裡。</div>'
      +'<div class="sbar">'
      +(gotP>0?'<div class="got" style="flex:'+gotP+'">'+Math.round(gotP)+'</div>':'')
      +(pickP>0?'<div class="pick" style="flex:'+pickP+'">'+Math.round(pickP)+'</div>':'')
      +(unkP>0?'<div class="unk" style="flex:'+unkP+'">'+Math.round(unkP)+'</div>':'')
      +'</div><div class="skey">'
      +'<span><i style="background:var(--cp-got)"></i>🌟 穩穩收下 <b>'+Math.round(gotP)+' 分</b></span>'
      +'<span><i style="background:var(--cp-pick)"></i>🌱 還能追回 <b>'+Math.round(pickP)+' 分</b>　<small>答錯或用猜的，補起來就是你的</small></span>'
      +(unkP>0?'<span><i style="background:var(--cp-unk)"></i>🎁 等待開箱 <b>'+Math.round(unkP)+' 分</b>　<small>'+un.length+' 章完全沒作答，實力未知</small></span>':'')
      +'</div><button class="howbtn" id="hitHow">這三個數字怎麼算出來的？</button>'
      +'<div class="defs2" id="hitDefs" hidden><b>每章 115 年預估出幾題</b>＝25 題×（16 年占比×0.5＋近 5 年〔1105114〕占比×0.5）。'
      +'<b>真會率</b>＝答對且沒標「猜的」÷ 已作答（猜對不算會）。<b>🌟 穩穩收下</b>＝預估題數×真會率；'
      +'<b>🌱 還能追回</b>＝其餘；完全沒作答的章整章算 <b>🎁 等待開箱</b>。每題 2 分，已作答 '+doneT+'／'+bankT+' 題。'
      +'<br>這是依你自己的作答推估，不是命中率預測；某章作答愈少，推估愈不準。</div></div>';
    var t=rows[0];
    h+='<div class="today"><div class="tag">今天從這章開始</div>'
      +'<h4>'+esc(t.x.nm)+'<span class="gain">還能追回 '+gain(t)+' 分</span></h4>'
      +'<p>'+why(t)+'<br>目前已答 '+t.a+'/'+t.x.n16+' 題，真會率 '+Math.round(t.rr*100)+'%。'
      +(t.thin?'<br><span style="color:var(--cp-accent)">⚠ 這章作答還少，推估僅供參考。</span>':'')+'</p>'
      +'<div class="acts"><a class="go" href="'+t.x.d+'">去刷這章 ▸</a>'
      +'<a href="'+t.x.r+'">讀 '+esc(t.x.rn)+' ▸</a>'
      +'<a href="經紀法規_法條解析練習.html#ch='+t.x.c+'">混合練這章 ▸</a></div></div>';
    var nx='';
    if(rows[1]) nx+='練完接著：<b>'+esc(rows[1].x.nm)+'</b>（'+gain(rows[1])+' 分）';
    if(rows[2]) nx+='、<b>'+esc(rows[2].x.nm)+'</b>（'+gain(rows[2])+' 分）';
    if(nx) nx+='。';
    if(un.length&&un[0].p>0) nx+='<br>那 '+Math.round(unkP)+' 分等待開箱的，從 <b>'+esc(un[0].nm)+'</b>（預估出 '+un[0].p.toFixed(1)+' 題）開始最劃算。';
    if(nx) h+='<p class="nextup">'+nx+'</p>';
  }
  h+='<button class="more" id="hitMore">'+(openAll?'收起 ▴':'看全部 '+(rows.length+un.length)+' 章 ▾')+'</button>'
    +'<div id="hitAll"'+(openAll?'':' hidden')+' style="margin-top:10px"><div class="slim">';
  rows.forEach(function(r){
    h+='<details><summary><span class="sl-dot'+(r.ls>=0.5?' hi':'')+'"></span>'
      +'<span class="sl-name">'+esc(r.x.c)+'</span>'
      +'<span class="sl-mini"><i style="width:'+Math.max(3,Math.round(r.ls/(maxL||1)*100))+'%"></i></span>'
      +'<span class="sl-num">可追回 <b>'+gain(r)+' 分</b>・會 <b>'+Math.round(r.rr*100)+'%</b></span></summary>'
      +'<div class="sl-body"><b>'+esc(r.x.nm)+'</b><br>'+why(r)
      +'<div class="acts" style="margin-top:8px"><a class="go" href="'+r.x.d+'">去刷這章 ▸</a>'
      +'<a href="'+r.x.r+'">讀 '+esc(r.x.rn)+' ▸</a>'
      +'<a href="經紀法規_法條解析練習.html#ch='+r.x.c+'">混合練 ▸</a></div></div></details>';
  });
  un.forEach(function(x){
    h+='<details><summary><span class="sl-dot un"></span><span class="sl-name">'+esc(x.c)+'</span>'
      +'<span class="sl-mini"></span>'
      +'<span class="sl-num">等待開箱・值 <b>'+(x.p*2).toFixed(1)+' 分</b></span></summary>'
      +'<div class="sl-body"><b>'+esc(x.nm)+'</b><br>這章完全沒作答，先刷一輪就知道實力落在哪（16 年 '+x.n16+' 題）。'
      +'<div class="acts" style="margin-top:8px"><a class="go" href="'+x.d+'">去刷這章 ▸</a>'
      +'<a href="'+x.r+'">讀 '+esc(x.rn)+' ▸</a></div></div></details>';
  });
  h+='</div></div>';
  box.innerHTML=h;
}
draw();
document.addEventListener('click',function(e){
  var box=document.getElementById('hitPanel'); if(!box||!box.contains(e.target)) return;
  var pb=e.target.closest('.palrow [data-hpal]');
  if(pb){
    var v=pb.getAttribute('data-hpal');
    try{localStorage.setItem('bxj-hit-pal',v)}catch(err){}
    box.setAttribute('data-pal',v);
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
</script>""".replace('__CHJSON__', json.dumps(CH, ensure_ascii=False))

BLOCK = CSS + """
<section id="hitPanel">
  <div id="hitBody"></div>
</section>
""" + JS

s = io.open(HUB, encoding='utf-8').read()
import re
if 'id="hit-css"' in s:
    a = s.index('<style id="hit-css">')
    b = s.index('</script>', s.index('<script id="hit-js">')) + len('</script>')
    s = s[:a] + BLOCK + s[b:]
else:
    anchor = '<section class="tab" id="pProg">\n'
    assert s.count(anchor) == 1
    s = s.replace(anchor, anchor + BLOCK + '\n')
io.open(HUB, 'w', encoding='utf-8').write(s)
print('面板已寫入｜官方題 %d（近5年 %d）｜22 章預估合計 %.2f 題' % (TOT, TOTR, sum(PRED.values())))
for c in sorted(PRED, key=lambda k: -PRED[k])[:6]:
    print('   %s 預估 %.2f 題（16年 %d／近5年 %d）' % (c, PRED[c], c16[c], c5[c]))
