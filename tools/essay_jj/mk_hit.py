# -*- coding: utf-8 -*-
"""《經紀法規_備考指揮中心》「掌握度・精準打擊」面板（對應估價 v500）。

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

CSS = '''<style id="hit-css">
#hitPanel{margin:0 0 18px}
#hitPanel .hp-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin:0 0 4px}
#hitPanel .hp-h h3{font-size:1.06rem;margin:0}
#hitPanel .hp-h .hp-tag{font-size:.72rem;background:var(--acc-soft);color:var(--acc-ink);
  border-radius:999px;padding:2px 9px;font-weight:700}
#hitPanel .hp-note{font-size:.78rem;color:var(--sub);margin:0 0 10px;line-height:1.6}
#hitPanel .hp-sum{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:11px 13px;margin:0 0 12px;box-shadow:var(--shadow)}
#hitPanel .hp-sum b{font-size:1.18rem;color:var(--bad)}
#hitPanel .hp-sum .hp-s2{font-size:.8rem;color:var(--sub);margin-top:3px}
#hitPanel .hp-row{background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--line);
  border-radius:10px;padding:10px 12px;margin:0 0 8px;box-shadow:var(--shadow)}
#hitPanel .hp-row.lv3{border-left-color:var(--bad)}
#hitPanel .hp-row.lv2{border-left-color:var(--acc)}
#hitPanel .hp-row.lv1{border-left-color:var(--ok)}
#hitPanel .hp-t{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline;justify-content:space-between}
#hitPanel .hp-t .nm{font-weight:700;font-size:.93rem;flex:1 1 60%;min-width:0}
#hitPanel .hp-t .ls{font-size:.86rem;font-weight:700;white-space:nowrap}
#hitPanel .lv3 .ls{color:var(--bad)}#hitPanel .lv2 .ls{color:var(--acc-ink)}#hitPanel .lv1 .ls{color:var(--ok)}
#hitPanel .hp-bar{height:6px;border-radius:4px;background:var(--line);margin:7px 0 6px;overflow:hidden}
#hitPanel .hp-bar i{display:block;height:100%;border-radius:4px}
#hitPanel .lv3 .hp-bar i{background:var(--bad)}#hitPanel .lv2 .hp-bar i{background:var(--acc)}
#hitPanel .lv1 .hp-bar i{background:var(--ok)}
#hitPanel .hp-d{font-size:.78rem;color:var(--sub);line-height:1.65}
#hitPanel .hp-d .wk{color:var(--bad);font-weight:700}
#hitPanel .hp-act{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
#hitPanel .hp-act a{flex:1 1 auto;text-align:center;font-size:.76rem;text-decoration:none;
  border:1px solid var(--line);border-radius:999px;padding:5px 10px;color:var(--ink);background:var(--bg)}
#hitPanel .hp-act a.p{background:var(--pri);color:var(--on);border-color:var(--pri)}
#hitPanel .hp-un{background:var(--warn);border:1px dashed var(--line);border-radius:10px;padding:10px 12px;margin:10px 0 0}
#hitPanel .hp-un h4{margin:0 0 5px;font-size:.88rem}
#hitPanel .hp-un .u{font-size:.8rem;color:var(--sub);line-height:1.8}
#hitPanel .hp-un .u a{color:var(--pri);text-decoration:none;font-weight:700}
#hitPanel .thin{font-size:.72rem;color:var(--acc-ink);font-weight:700}
@media(max-width:420px){#hitPanel .hp-act a{flex:1 1 100%}}
</style>'''

JS = '''<script id="hit-js">
(function(){
var CH=__CHJSON__;
var KN={A:'A 法條混淆',B:'B 粗心',C:'C 真的不熟',D:'D 猜的'};
var TIP={A:'把兩條並排看一次，再回來刷',B:'作答前先圈題幹的否定詞與主體',
 C:'先讀整理頁，不要硬刷',D:'猜對不算會，當成不會重讀'};
function ld(k,d){try{var v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}}
function esc(t){return String(t==null?'':t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function draw(){
  var box=document.getElementById('hitBody');if(!box)return;
  var DB=ld('bxj-q2',{});
  var st={};CH.forEach(function(x){st[x.c]={a:0,real:0,w:0,k:{}}});
  Object.keys(DB).forEach(function(id){
    var c=id.split('-')[0];if(!st[c])return;var r=DB[id]||{};if(!r.n)return;
    st[c].a++;
    if(r.ok&&!r.g)st[c].real++;
    if(!r.ok){st[c].w++;var k=r.k||'';if(k)st[c].k[k]=(st[c].k[k]||0)+1;else st[c].k['?']=(st[c].k['?']||0)+1}
  });
  var rows=[],un=[],lose=0,unq=0;
  CH.forEach(function(x){
    var s=st[x.c];
    if(!s.a){un.push(x);unq+=x.p;return}
    var rr=s.real/s.a, ls=x.p*(1-rr);
    lose+=ls;
    rows.push({x:x,s:s,rr:rr,ls:ls});
  });
  rows.sort(function(a,b){return b.ls-a.ls});
  var h='<div class="hp-sum"><div>預估總失分 <b>'+lose.toFixed(1)+' 題</b>'+
    ' ≈ <b>'+(lose*2).toFixed(0)+' 分</b><span style="font-size:.8rem;color:var(--sub)">（選擇題滿分 50）</span></div>';
  if(un.length)h+='<div class="hp-s2">另有 '+unq.toFixed(1)+' 題落在 '+un.length+' 個「還沒作答」的章節，下方獨立列出</div>';
  h+='</div>';
  rows.forEach(function(r){
    var x=r.x,s=r.s;
    var lv=r.ls>=1?3:(r.ls>=0.5?2:1);
    var thin=(s.a<8)||(s.a/x.n16<0.25);
    var kk='',kn=0;Object.keys(s.k).forEach(function(k){if(s.k[k]>kn){kn=s.k[k];kk=k}});
    var act;
    if(!s.w){act = s.real===s.a ? '維持，不用再花時間讀' : '答對的裡面有猜的，回頭確認一次為什麼對';}
    else if(kk==='?'){act='有 '+s.w+' 題錯了但<span class="wk">沒標錯誤類型</span>，先去標，否則判斷不出要補法條還是補觀念';}
    else {act='主要錯因 <span class="wk">'+esc(KN[kk]||kk)+'</span>（'+kn+' 題）→ '+TIP[kk];}
    h+='<div class="hp-row lv'+lv+'">'+
      '<div class="hp-t"><span class="nm">'+esc(x.nm)+'</span>'+
      '<span class="ls">預估失分 '+r.ls.toFixed(1)+' 題（'+(r.ls*2).toFixed(1)+' 分）</span></div>'+
      '<div class="hp-bar"><i style="width:'+Math.min(100,r.ls/1.5*100).toFixed(0)+'%"></i></div>'+
      '<div class="hp-d">115 預估出 <b>'+x.p.toFixed(1)+'</b> 題（16 年 '+x.n16+' 題・近 5 年 '+x.n5+' 題）'+
      '｜已答 '+s.a+'/'+x.n16+'｜真會率 <b>'+Math.round(r.rr*100)+'%</b>'+(s.w?'｜現在錯 '+s.w:'')+
      (thin?' <span class="thin">⚠ 作答太少，僅供參考</span>':'')+'<br>'+act+'</div>'+
      '<div class="hp-act">'+
      '<a class="p" href="'+x.d+'">去刷這章</a>'+
      '<a href="'+x.r+'">讀 '+esc(x.rn)+'</a>'+
      '<a href="經紀法規_法條解析練習.html#ch='+x.c+'">混合練這章</a>'+
      '</div></div>';
  });
  if(un.length){
    un.sort(function(a,b){return b.p-a.p});
    h+='<div class="hp-un"><h4>狀態未知（還沒作答，依官方出題量排起手順序）</h4><div class="u">';
    un.forEach(function(x,i){
      h+=(i?'　':'');
      h+='<a href="'+x.d+'">'+esc(x.c)+'</a>（預估 '+x.p.toFixed(1)+' 題）';
    });
    h+='</div></div>';
  }
  box.innerHTML=h;
}
draw();
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')draw()});
addEventListener('focus',draw);
/* #hit / #progress 直達進度分頁 */
function hitHash(){var hs=location.hash;if(hs==='#hit'||hs==='#progress'||hs==='#rev'){
  try{goTab('pProg')}catch(e){}
  if(hs==='#hit'){var el=document.getElementById('hitPanel');if(el)setTimeout(function(){el.scrollIntoView({behavior:'smooth',block:'start'})},120)}}}
if(location.hash)setTimeout(hitHash,180);
addEventListener('hashchange',hitHash);
})();
</script>'''.replace('__CHJSON__', json.dumps(CH, ensure_ascii=False))

BLOCK = CSS + '''
<section id="hitPanel">
  <div class="hp-h"><h3>掌握度・精準打擊</h3><span class="hp-tag">依你自己的作答推估</span></div>
  <p class="hp-note">把正確率換算成「<b>115 年大概會掉幾分</b>」，由高到低排出先打順序。<br>
  <b>預估題數</b>＝25 題 ×（該章 16 年占比×0.5 ＋ 近 5 年〔110–114〕占比×0.5），分母為 ''' + str(TOT) + ''' 題官方題（已排除多層次傳銷 2 題）。<br>
  <b>真會率</b>＝（答對且未標「D 猜的」）÷ 已作答——<b>猜對不算會</b>，這是和一般「正確率」最大的差別。<br>
  <b>預估失分</b>＝預估題數 ×（1－真會率），選擇題每題 2 分。這是依你的作答推估，<b>不是命中率預測</b>。</p>
  <div id="hitBody"></div>
</section>
''' + JS

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
