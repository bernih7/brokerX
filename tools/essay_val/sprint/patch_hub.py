# -*- coding: utf-8 -*-
"""估價指揮中心：申論分頁加兩個 5 分鐘練習入口＋「各題紀錄」列（⏱ 衝刺 N 次・最近 a／b｜🧩 推理 N 次・最近 a／b，
讀範文頁的 bxv-es-log 輪數／自評與 bxv-es-sprint）；回到此頁（返回鍵、切回分頁、別頁存檔）自動重讀。
「進度落後在哪」申論：分母＝範文頁實際卡數（bx-essay-meta，範文頁每次開啟時寫入；沒有就用 bxv-essay-meta.js），
勾已讀、看過一輪、做過 5 分鐘練習任一都算讀過（只算範文頁現有的卡）。
改自經紀法規 tools/essay_jj/sprint/patch_hub.py 與 tools/essay_progress_unify.py（估價指揮中心沒有逐卡清單，所以紀錄列放在入口下方）。
可重跑：python3 tools/essay_val/sprint/patch_hub.py"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
f = os.path.join(R, '估價備考指揮中心.html'); s = open(f, encoding='utf-8').read()

BOX = '''<!--sp-box--><div class="esh-box sp-box" id="spBox">
    <div class="esh-bt">5 分鐘申論練習（紀錄與範文頁同步）</div>
    <a class="sp-a" id="spLink" href="%E4%BC%B0%E5%83%B9_%E7%94%B3%E8%AB%965%E5%88%86%E9%90%98%E8%A1%9D%E5%88%BA.html"><span class="sp-n"><b>⏱ 申論 5 分鐘衝刺</b><small>一題 5 分鐘：讀題→先自己想→考場版→結論→關鍵檢核打分；沒做過的優先，再來不熟的；可 🎲 隨機出題</small></span><span class="sp-g">練習 ▸</span></a>
    <a class="sp-a" id="spLink2" href="%E4%BC%B0%E5%83%B9_%E7%94%B3%E8%AB%965%E5%88%86%E9%90%98_%E6%8E%A8%E7%90%86%E7%89%88.html"><span class="sp-n"><b>🧩 申論 5 分鐘・推理版</b><small>跟著推理鏈一步步自問自答→速寫骨架→失分點→關鍵詞檢核；秒數依題目內容分配</small></span><span class="sp-g">練習 ▸</span></a>
    <p class="sp-any" id="esAny"></p>
    <details class="sp-log" id="spLog"><summary>各題紀錄 <span id="spLogN"></span></summary><div class="sp-rows" id="spRows"></div></details>
  </div><!--/sp-box-->
'''
CSS = '''<style id="sprint-css">
.sp-a{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:10px;padding:9px 12px;margin-top:6px;text-decoration:none;color:var(--ink);background:var(--paper2,var(--paper))}
.sp-a:hover{border-color:var(--primary)}
.sp-n{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.sp-n b{font-size:.92rem}.sp-n small{font-size:.74rem;color:var(--muted);line-height:1.5}
.sp-g{flex:none;font-size:.76rem;font-weight:700;color:var(--primary);white-space:nowrap}
.sp-any{font-size:.8rem;color:var(--muted);margin:8px 0 2px;line-height:1.7}.sp-any b{color:var(--ink)}
.sp-log{margin-top:6px}.sp-log>summary{cursor:pointer;font-size:.82rem;font-weight:700;color:var(--primary);padding:4px 0}
.sp-rows{display:flex;flex-direction:column;gap:4px;margin-top:4px}
.sp-r{display:grid;grid-template-columns:1fr auto;gap:2px 8px;align-items:center;border-top:1px dashed var(--line);padding:6px 2px;font-size:.8rem}
.sp-r .t{min-width:0;color:var(--ink);line-height:1.5}.sp-r .t small{color:var(--muted);margin-right:4px}
.sp-r a{font-size:.76rem;font-weight:700;color:var(--primary);text-decoration:none;white-space:nowrap}
.sp-r .l{grid-column:1/3;color:var(--muted);font-size:.76rem;display:flex;flex-wrap:wrap;gap:2px 10px}.sp-r .l b{color:var(--primary)}
.sp-r .l:empty{display:none}.sp-r.none .t{opacity:.7}
</style>
'''
JS = '''<script id="sprint-sync">
/* 5 分鐘練習紀錄（bxv-es-sprint；推理版 f:'r'）＋範文頁輪數／自評（bxv-es-log）顯示在申論分頁「各題紀錄」；回到此頁時重讀 */
(function(){
var SU='%E4%BC%B0%E5%83%B9_%E7%94%B3%E8%AB%965%E5%88%86%E9%90%98%E8%A1%9D%E5%88%BA.html';
function ld(k,d){try{var v=JSON.parse(localStorage.getItem(k)||'null');return v==null?d:v}catch(e){return d}}
function meta(){var M=ld('bx-essay-meta',null);return (M&&M.ids)?M:(window.BXV_ESSAY_META||null)}
function fmt(x){x=Math.round(x||0);return Math.floor(x/60)+':'+('0'+(x%60)).slice(-2)}
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
var VI={ok:'✅ 熟',mem:'📖 還沒背起來',hard:'😵 太難'};
function paint(){
  var M=meta(),S=ld('bxv-es-sprint',{})||{},L=ld('bxv-es-log',{})||{},RD=ld('bx-essay-read',[]);if(!Array.isArray(RD))RD=[];
  var box=document.getElementById('spRows');if(!M||!box)return;
  var ids=(M.order&&M.order.length?M.order:Object.keys(M.ids)).filter(function(k){return M.ids[k]}),p=0,a=0,h='';
  ids.forEach(function(k){
    var x=L[k]||{},sp=S[k]||[],ar=sp.filter(function(r){return r.f!=='r'}),rr=sp.filter(function(r){return r.f==='r'});
    var pr=(x.n>0)||sp.length>0;if(pr)p++;if(pr||RD.indexOf(k)>=0)a++;
    var lg=(ar.length?'<span>⏱ 衝刺 <b>'+ar.length+'</b> 次・最近 '+ar[0].sc+'／'+ar[0].mx+'</span>':'')
      +(rr.length?'<span>🧩 推理 <b>'+rr.length+'</b> 次・最近 '+rr[0].sc+'／'+rr[0].mx+'</span>':'')
      +(x.n?'<span>讀過 <b>'+x.n+'</b> 輪・累計 '+fmt(x.tot)+'</span>':'')+(x.v&&VI[x.v]?'<span>'+VI[x.v]+'</span>':'');
    var m=M.ids[k]||[];
    h+='<div class="sp-r'+(lg?'':' none')+'" data-id="'+esc(k)+'"><span class="t">'+esc(m[3]||k)+'</span><a href="'+SU+'#q='+encodeURIComponent(k)+'">練這題 ▸</a><span class="l">'+lg+'</span></div>';
  });
  box.innerHTML=h;
  var n=document.getElementById('spLogN');if(n)n.textContent='（練過 '+p+'／'+ids.length+'）';
  var el=document.getElementById('esAny');if(el)el.innerHTML='看過一輪或做過 5 分鐘練習 <b>'+p+'</b>／'+ids.length+'｜「進度落後在哪」的已讀（勾已讀、看過一輪、5 分鐘練習任一）<b>'+a+'</b>／'+ids.length;
}
function all(){paint();if(typeof lagBuild==='function')lagBuild()}
var d=document.getElementById('spLog');
if(d){try{if(localStorage.getItem('bxv-sp-log-open')==='1')d.open=true}catch(e){}d.addEventListener('toggle',function(){try{localStorage.setItem('bxv-sp-log-open',d.open?'1':'0')}catch(e){}})}
paint();
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')paint()});
addEventListener('focus',paint);
addEventListener('storage',function(e){if(e.key==='bxv-es-sprint'||e.key==='bxv-es-log'||e.key==='bx-essay-read'||e.key==='bx-essay-meta')all()});
addEventListener('pageshow',function(e){if(e.persisted)all();else paint()});
})();
</script>
'''
# 1) 入口＋紀錄列（申論分頁、分級膠囊下方）
s = re.sub(r'(<div class="esh-lv" id="esh-lv"></div>\n)\s*<!--sp-box-->.*?<!--/sp-box-->\n', r'\1', s, flags=re.S)
a = '<div class="esh-lv" id="esh-lv"></div>\n'; assert s.count(a) == 1, '找不到 esh-lv'
s = s.replace(a, a + '\n  ' + BOX, 1)
# 2) CSS／JS
s = re.sub(r'<style id="sprint-css">.*?</style>\n', '', s, flags=re.S)
s = re.sub(r'<script id="sprint-sync">.*?</script>\n', '', s, flags=re.S)
s = s.replace('</head>', CSS + '</head>', 1)
k = s.rfind('</body>'); s = s[:k] + JS + s[k:]
# 3) 進度落後在哪：申論口徑（分母＝範文頁實際卡數；勾已讀／看過一輪／5 分鐘練習任一＝讀過）
OLD = """  try{var L=JSON.parse(localStorage.getItem('bxv-es-log')||'{}');
    Object.keys(L).forEach(function(k){var r=L[k];if(!r)return;
      if(r.n){esCards++;esRounds+=r.n;esSec+=r.tot||0;}
      if(r.v&&esV[r.v]!=null)esV[r.v]++;});}catch(e){}
  if(!esCards){try{esCards=(JSON.parse(localStorage.getItem('bx-es-read')||'[]')||[]).length;}catch(e){}}"""
NEW = """  /*es-any*/var esSp=0;
  try{var L=JSON.parse(localStorage.getItem('bxv-es-log')||'{}')||{},SPX=JSON.parse(localStorage.getItem('bxv-es-sprint')||'{}')||{},RDX=JSON.parse(localStorage.getItem('bx-essay-read')||'[]')||[],MX=null,seen={};
    try{MX=JSON.parse(localStorage.getItem('bx-essay-meta')||'null')}catch(e){} if(!(MX&&MX.ids))MX=window.BXV_ESSAY_META||null;
    function inPage(k){return !(MX&&MX.ids)||!!MX.ids[k]}
    Object.keys(L).forEach(function(k){var r=L[k];if(!r||!inPage(k))return;
      if(r.n){seen[k]=1;esRounds+=r.n;esSec+=r.tot||0;}
      if(r.v&&esV[r.v]!=null)esV[r.v]++;});
    Object.keys(SPX).forEach(function(k){if(inPage(k)&&SPX[k]&&SPX[k].length){seen[k]=1;esSp+=SPX[k].length;}});
    (Array.isArray(RDX)?RDX:[]).forEach(function(k){if(inPage(k))seen[k]=1});
    esCards=Object.keys(seen).length;}catch(e){}"""
if '/*es-any*/' not in s:
    assert s.count(OLD) == 1, '進度落後在哪：申論區段已被改動，請手動比對'
    s = s.replace(OLD, NEW, 1)
OLD2 = "       (esRounds?('累計 '+esRounds+' 輪・共 '+Math.round(esSec/60)+' 分鐘'):'還沒有計時紀錄')"
NEW2 = "       (esRounds?('累計 '+esRounds+' 輪・共 '+Math.round(esSec/60)+' 分鐘'):'還沒有計時紀錄')+(esSp?('・5 分鐘練習 '+esSp+' 次'):'')"
if NEW2 not in s:
    assert s.count(OLD2) == 1, '進度落後在哪：申論備註已被改動'
    s = s.replace(OLD2, NEW2, 1)
open(f, 'w', encoding='utf-8').write(s); print('ok 指揮中心')
