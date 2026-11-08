# -*- coding: utf-8 -*-
"""民法指揮中心「進度落後在哪」：每列可點開看還沒完成的項目（比照土地法 v654～v668），
並依篇別考題占比（D 26%＞E 24%＞A 21.5%＞B 14.5%＞C 14%，同頁攻略表①；BC 合冊頁算 28.5%）排序（使用者 11-08）。
CSS 直接沿用土地法 lag-css（兩頁色票變數同名）。可重跑：整段替換 <script id="lag-js"> 與 <style id="lag-css">。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
P = os.path.join(R, '民法_備考指揮中心.html')
LAND = os.path.join(R, '土地法_備考指揮中心.html')

JS = r'''<script id="lag-js">
/* 進度落後清單：目標＝考前把每一樣至少做完 1 輪；每天要＝剩餘量÷剩餘天數。只讀，不寫任何鍵。
   每一列可點開，列出還沒完成的項目與連結；依篇別考題占比排序（2026-11-08，tools/civ_lag_detail.py）。 */
(function(){
var OPEN={};
var W={D:26,E:24,A:21.5,B:14.5,C:14,BC:28.5},WN={D:'物權',E:'親屬繼承',A:'總則',B:'債總',C:'債各',BC:'債編'};
function esc(x){return String(x==null?'':x).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
/* 依頁面檔名判斷篇別；跨篇的整理頁算 0（排在有篇別的後面） */
function pian(p){p=p||'';var m=/民法(A|BC|D|E)_/.exec(p)||/刷題練習_([A-E])篇/.exec(p);if(m)return m[1];
  if(/繼承專區/.test(p))return 'E';if(/共有專區|物權變動|抵押權/.test(p))return 'D';if(/債之發生/.test(p))return 'B';return ''}
function wt(k){return W[k]||0}
function tag(k){if(!k)return '';return '<span class="wt">'+(k==='BC'?'B・C':k)+' '+WN[k]+' '+W[k]+'%</span>'}
function lk(u,t,sub,k){return '<li><a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(t)+' ▸</a>'+tag(k)+(sub?'<small>'+sub+'</small>':'')+'</li>'}
function byW(a,b){return wt(b.k)-wt(a.k)}
function lagBuild(){
  var box=document.getElementById('lagPanel'); if(!box) return;
  if(typeof BXREP==='undefined'||!BXREP.status){box.innerHTML='';return;}
  var exam=new Date('2026-11-14T09:00:00+08:00');
  var days=Math.max(1,Math.ceil((exam-new Date())/86400000));
  var G=BXREP.status();
  function grp(n){for(var i=0;i<G.length;i++)if(G[i].g.indexOf(n)===0)return G[i];return null}
  function rows(g){return g?g.rows:[]}
  function url(r){return r.url||(r.p?r.p+'.html':'#')}
  var drill=grp('刷題'),mock=grp('模擬卷'),read=grp('閱讀頁'),mem=grp('記憶工具');
  var dRows=rows(drill).filter(function(r){return r.total>0&&r.name.indexOf('刷題 ')===0});
  dRows.forEach(function(r){r.k=pian(r.p)});
  var dDone=0,dTot=0;dRows.forEach(function(r){dDone+=r.done;dTot+=r.total});
  /* 申論：按已讀、看完一輪或做過 5 分鐘練習都算讀過 */
  var EL=[].slice.call(document.querySelectorAll('details.essay')),esTot=EL.length||86,eUn=[];
  try{var M=JSON.parse(localStorage.getItem('minfa_read')||'{}'),LG=JSON.parse(localStorage.getItem('bxm-es-log')||'{}'),SPR=JSON.parse(localStorage.getItem('bxm-es-sprint')||'{}');
    EL.forEach(function(d){var k=d.dataset.key;if(M[k]||(LG[k]&&LG[k].n)||(SPR[k]&&SPR[k].length))return;
      var ec=d.querySelector('.ec'),et=d.querySelector('.et'),c=ec?ec.textContent.trim():'';
      eUn.push({i:k,t:et?et.textContent.trim():k,c:c,k:/^[A-E]/.test(c)?c.charAt(0):'',off:/^\d/.test(k),lv:d.dataset.lv||'Z'})})}catch(e){}
  var esRead=esTot-eUn.length;
  var rRows=rows(read);rRows.forEach(function(r){r.k=pian(r.p)});
  var rTot=rRows.length,rDone=rRows.filter(function(r){return (r.read||0)>0}).length;
  var mRows=rows(mock).filter(function(r){return r.total>0}),mTot=0,mDone=0;
  /* 歷屆整卷一列＝8 卷（done／total 就是卷數）；其餘每列 1 份，答完才算 */
  mRows.forEach(function(r){if(r.p==='民法概要_25題模擬測驗'){mTot+=r.total;mDone+=Math.min(r.done,r.total)}else{mTot++;if(r.done>=r.total)mDone++}});
  var kRows=rows(mem).filter(function(r){return r.total>0&&r.p.indexOf('考題小卡')<0}),kDone=0,kTot=0;kRows.forEach(function(r){r.k=pian(r.p);kDone+=Math.min(r.done,r.total);kTot+=r.total});
  function per(rem){return rem<=0?'已完成':(Math.ceil(rem/days)+' / 天')}
  function bar(d,t){var p=t?Math.min(100,Math.round(d/t*100)):0;return '<span class="pb"><i style="width:'+p+'%"></i></span>'}
  function row(k,nm,d,t,u,note,det){var rem=Math.max(0,t-d),op=!!OPEN[k];
    return '<tr class="lgr'+(op?' on':'')+'" data-k="'+k+'" tabindex="0" role="button" aria-expanded="'+op+'"><td><span class="tw">'+(op?'▾':'▸')+'</span>'+nm+'</td><td class="n" data-l="目前">'+d+'／'+t+' '+u+'</td><td data-l="完成度">'+bar(d,t)+'</td>'
      +'<td class="n '+(rem?'need':'zero')+'" data-l="每天要">'+per(rem)+'</td><td class="zero" data-l="備註">'+(note||'')+'</td></tr>'
      +'<tr class="lgx" data-k="'+k+'"'+(op?'':' hidden')+'><td colspan="5"><div class="lgd">'+det+'</div></td></tr>'}
  var SORT='<p class="lh">依篇別考題占比排序：D 物權 26%＞E 親屬繼承 24%＞A 總則 21.5%＞B 債總 14.5%＞C 債各 14%（520 題分篇統計；B・C 合冊的頁面算 28.5%）。</p>';
  /* 選擇題：先占比、再剩餘題數 */
  var dDet=dRows.filter(function(r){return r.done<r.total}).sort(function(a,b){return byW(a,b)||(b.total-b.done)-(a.total-a.done)}).map(function(r){var rem=r.total-r.done;
      return lk(url(r),r.name,'還沒做 '+rem+' 題（'+r.done+'／'+r.total+'）',r.k)}).join('');
  dDet=dDet?SORT+'<ul>'+dDet+'</ul><p class="lh">題庫頁可用「未作答」只出沒做過的；也可到 <a href="民法_法條解析練習.html" target="_blank" rel="noopener">法條解析練習 ▸</a> 用智慧配題混合練。</p>':'<p class="lh">五篇都做完一輪了。</p>';
  /* 申論：占比 → 官方先 → 星等 */
  var eDet;
  if(!EL.length)eDet='<p class="lh">申論清單沒有載入，請到申論分頁看未讀。</p>';
  else if(!eUn.length)eDet='<p class="lh">'+esTot+' 題都讀過了。</p>';
  else{eUn.sort(function(a,b){return byW(a,b)||(b.off-a.off)||(a.lv<b.lv?-1:a.lv>b.lv?1:0)});
    var nOff=eUn.filter(function(x){return x.off}).length;
    eDet=SORT.replace('</p>','；同篇內官方題先、再依星等。</p>')+'<p class="lh">還沒讀的 '+eUn.length+' 題（官方 '+nOff+'、預測／模擬 '+(eUn.length-nOff)+'）。點了開單題頁。</p><ul class="sc">'
      +eUn.map(function(x){return lk('民法_申論卡.html#'+encodeURIComponent(x.i),x.t,(x.off?'官方 ':'')+esc(x.i)+'・'+esc(x.c),x.k)}).join('')+'</ul>'}
  var rUn=rRows.filter(function(r){return !(r.read>0)}).sort(byW);
  var rDet=rUn.length?SORT+'<p class="lh">還沒讀完一輪的 '+rUn.length+' 頁（讀完在頁面右下按＋，或捲到最底自動記一輪）；跨篇的整理頁排最後。</p><ul>'
    +rUn.map(function(r){return lk(url(r),r.name,r.open?'開過 '+r.open+' 次':'沒開過',r.k)}).join('')+'</ul>':'<p class="lh">每一頁都至少讀完一輪了。</p>';
  var mUn=mRows.filter(function(r){return r.done<r.total});
  var mDet=mUn.length?'<p class="lh">模擬卷跨篇，不分占比。</p><ul>'+mUn.map(function(r){return lk(url(r),r.name,r.done?'已答 '+r.done+'／'+r.total+'，還差 '+(r.total-r.done)+(r.p==='民法概要_25題模擬測驗'?' 卷':' 題'):'還沒開始')}).join('')+'</ul>':'<p class="lh">模擬卷都答完了。</p>';
  var kUn=kRows.filter(function(r){return r.done<r.total}).sort(function(a,b){return byW(a,b)||(b.total-b.done)-(a.total-a.done)});
  var kDet=kUn.length?SORT+'<ul>'+kUn.map(function(r){return lk(url(r)+(/單字卡/.test(r.p)?'#unseen':/定義填空/.test(r.p)?'#todo':''),r.name,'還差 '+(r.total-r.done)+'（'+esc(r.txt||'')+'）',r.k)}).join('')+'</ul>':'<p class="lh">記憶工具都完成了。</p>';
  var h='<div class="lg"><h3><span>⏳</span>進度落後在哪<span class="d">剩 '+days+' 天</span></h3>'
    +'<div class="goal">目標：<b>考前把每一樣至少做完 1 輪</b>。「每天要」＝剩下的量 ÷ 剩下的天數。<b>點任一列</b>看還沒完成的項目（依篇別考題占比排序），點連結直接過去。</div>'
    +'<table><thead><tr><th>項目</th><th class="n">目前</th><th>完成度</th><th class="n">每天要</th><th>備註</th></tr></thead><tbody>'
    +row('d','選擇題（A～E 篇）',dDone,dTot,'題','法條解析練習的作答也算在這裡',dDet)
    +row('e','申論 '+esTot+' 題',esRead,esTot,'題','按「已讀」、看完一輪或做過 5 分鐘練習都算',eDet)
    +row('r','閱讀／整理頁',rDone,rTot,'頁','讀完一輪＝按＋，或捲到該頁最底',rDet)
    +row('m','模擬卷',mDone,mTot,'份','歷屆整卷 8 卷＋自擬 2 份＋來勝 1 份',mDet)
    +row('k','記憶工具',kDone,kTot,'張','單字卡翻過背面就算看過（或在單字卡頁按右下「讀過＋」＝整輪看完）；定義填空按完成（精選／完整考題小卡與題庫是同一批題目，不重複計）',kDet)
    +'</tbody></table>';
  var zero=[];
  dRows.forEach(function(r){if(r.done===0)zero.push({n:r.name,u:url(r),k:r.k})});
  rUn.forEach(function(r){zero.push({n:r.name,u:url(r),k:r.k})});
  mRows.forEach(function(r){if(!r.done)zero.push({n:r.name,u:url(r),k:''})});
  zero.sort(byW);
  if(zero.length){
    h+='<div class="names"><span class="lab">完全沒開始的 '+zero.length+' 項（占比高的在前）</span>'
      +zero.map(function(z){return '<a href="'+esc(z.u)+'" target="_blank" rel="noopener">'+esc(z.n)+'</a>'}).join('、')+'</div>';
  }else h+='<div class="names"><span class="lab">每一項都已經開始</span>接下來看「每天要」那一欄，把量補上就好。</div>';
  /*PLAN*/
  box.innerHTML=h+'</div>';
}
document.addEventListener('click',function(e){var tr=e.target.closest&&e.target.closest('#lagPanel tr.lgr');if(!tr||e.target.closest('a'))return;var k=tr.getAttribute('data-k');OPEN[k]=!OPEN[k];lagBuild()});
document.addEventListener('keydown',function(e){if(e.key!=='Enter'&&e.key!==' ')return;var tr=e.target.closest&&e.target.closest('#lagPanel tr.lgr');if(!tr)return;e.preventDefault();var k=tr.getAttribute('data-k');OPEN[k]=!OPEN[k];lagBuild();var n=document.querySelector('#lagPanel tr.lgr[data-k="'+k+'"]');if(n)n.focus()});
lagBuild();
addEventListener('pageshow',lagBuild);
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')lagBuild()});
addEventListener('focus',lagBuild);
})();
</script>'''

s = open(P, encoding='utf-8').read()
a = s.index('<script id="lag-js">'); b = s.index('</script>', a) + 9
old = s[a:b]
# 保留原「考前補進度排程」區塊（從 /* 考前補進度排程 到 box.innerHTML 之前）
if '/*PLAN*/' in JS and '考前補進度排程' in old:
    pa = old.index('  /* 考前補進度排程'); pb = old.index('  box.innerHTML=h+', pa)
    plan = old[pa:pb]
else:
    pa = old.find('  /* 考前補進度排程'); plan = ''
js = JS.replace('  /*PLAN*/\n', plan)
s = s[:a] + js + s[b:]
L = open(LAND, encoding='utf-8').read()
la = L.index('<style id="lag-css">'); lb = L.index('</style>', la) + 8
css = L[la:lb].replace('</style>', '#lagPanel .wt{display:inline-block;margin-left:6px;padding:0 7px;border-radius:999px;background:var(--cp-milk);color:var(--cp-soft);font-size:.68rem;font-weight:700;vertical-align:1px}\n</style>')
ca = s.index('<style id="lag-css">'); cb = s.index('</style>', ca) + 8
s = s[:ca] + css + s[cb:]
open(P, 'w', encoding='utf-8').write(s)
print('OK', '保留排程' if plan else '無排程')
