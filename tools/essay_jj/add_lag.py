# -*- coding: utf-8 -*-
"""施工單第 8 項：進度分頁加「進度落後清單」。

目標寫在面板上（不是黑盒）：考前把每一樣至少做完 1 輪；
「每天要」＝剩餘量 ÷ 剩餘天數（無條件進位）。
資料一律取自 BXREP.status()（刷題／模擬卷／記憶工具／閱讀頁）與 bxj-es-log（申論），
不另外建表，也不動進度分頁既有的任何區塊。
可重複執行：以 <style id="lag-css"> … </script><!--/lag--> 為邊界整段換掉。
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
EXAM = '2026-11-14'

BLK = """<style id="lag-css">
#lagPanel{background:var(--surface,#fff);border:1.5px solid var(--line,#ddd);border-radius:12px;padding:14px 14px 12px;margin:0 0 14px}
#lagPanel h3{margin:0 0 2px;font-size:1.02rem;display:flex;align-items:center;gap:7px}
#lagPanel .lgoal{font-size:.82rem;color:var(--sub,#666);margin-bottom:10px}
#lagPanel .lgoal b{color:var(--ink,#222)}
#lagPanel table{width:100%;border-collapse:collapse;font-size:.85rem}
#lagPanel th,#lagPanel td{padding:7px 6px;border-bottom:1px solid var(--line,#eee);text-align:left;vertical-align:top}
#lagPanel th{font-size:.76rem;color:var(--sub,#666);font-weight:600}
#lagPanel td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#lagPanel td.d b{font-size:1.02rem;color:var(--pri,#2F5D50)}
#lagPanel .trk{height:6px;border-radius:3px;background:var(--line,#e6e6e6);margin-top:4px;overflow:hidden}
#lagPanel .trk i{display:block;height:100%;background:var(--pri,#2F5D50)}
#lagPanel .zero{margin-top:11px;padding-top:9px;border-top:1px dashed var(--line,#ddd);font-size:.82rem;color:var(--sub,#666)}
#lagPanel .zero b{color:var(--bad,#A8402B)}
#lagPanel .zero a{display:inline-block;border:1px solid var(--line,#ddd);border-radius:999px;padding:2px 9px;margin:4px 5px 0 0;
  background:var(--surface,#fff);color:var(--pri,#2F5D50);text-decoration:none;font-size:.78rem}
#lagPanel .zero a:hover{border-color:var(--pri,#2F5D50)}
@media(max-width:480px){#lagPanel th:nth-child(3),#lagPanel td:nth-child(3){display:none}}
</style>
<div id="lagPanel" hidden></div>
<script id="lag-js">
/* ⑧ 進度落後清單：考前把每一樣至少做完 1 輪；每天要＝剩餘÷剩餘天數 */
(function(){
var EXAM='__EXAM__';
function days(){var d=new Date(EXAM+'T00:00:00'),n=new Date();n.setHours(0,0,0,0);
  return Math.max(1,Math.ceil((d-n)/86400000))}
function esDone(){try{var D=JSON.parse(localStorage.getItem('bxj-es-log')||'{}'),c=0;
  Object.keys(D).forEach(function(k){if((D[k].n||0)>0)c++});return c}catch(e){return 0}}
function esTotal(){return document.querySelectorAll('details.essay-detail').length||68}
function draw(){
  var el=document.getElementById('lagPanel');
  if(!el||!window.BXREP||!BXREP.status){return}
  var G={};BXREP.status().forEach(function(g){G[g.g.split('（')[0]]=g.rows});
  var dr=G['刷題']||[],mk=G['模擬卷']||[],mm=G['記憶工具']||[],rd=G['閱讀頁']||[];
  var drill=dr.filter(function(r){return r.p.indexOf('刷題練習_')>=0});
  var sum=function(a,f){var t=0;a.forEach(function(x){t+=f(x)||0});return t};
  var ROWS=[
   {t:'選擇題（12 章題庫頁，含 2 題法源已廢止）',d:sum(drill,function(r){return r.done}),n:sum(drill,function(r){return r.total}),u:'題',
    zero:drill.filter(function(r){return !r.done})},
   {t:'申論卡（讀過 ≥1 輪）',d:esDone(),n:esTotal(),u:'題',zero:[]},
   {t:'閱讀整理頁（按 ＋ 或捲到底）',d:rd.filter(function(r){return (r.read||0)>0}).length,n:rd.length,u:'頁',
    zero:rd.filter(function(r){return !(r.read||0)})},
   {t:'模擬卷（交卷）',d:mk.filter(function(r){return r.total&&r.done}).length,n:mk.filter(function(r){return r.total}).length,u:'卷',
    zero:mk.filter(function(r){return r.total&&!r.done})},
   {t:'記憶工具（單字卡＋定義填空）',d:sum(mm,function(r){return r.done}),n:sum(mm,function(r){return r.total}),u:'張',
    zero:mm.filter(function(r){return !r.done})}
  ];
  var D=days(),h='<h3><span>📉</span>進度落後清單</h3>'
   +'<div class="lgoal">目標：<b>考前把每一樣至少做完 1 輪</b>。距離 '+EXAM+' 還有 <b>'+D+' 天</b>，'
   +'「每天要」＝還沒做的 ÷ '+D+' 天（無條件進位）。上面「日拱一築」算的是 518 題官方題，'
   +'這裡的 520 是題庫頁實際題數（多 2 題法源已廢止、只讀不計分）。</div>'
   +'<table><tr><th>項目</th><th>進度</th><th>還沒做</th><th>每天要</th></tr>';
  var zeros=[];
  ROWS.forEach(function(r){
    var left=Math.max(0,r.n-r.d),per=Math.ceil(left/D),pct=r.n?Math.round(r.d/r.n*100):0;
    h+='<tr><td>'+r.t+'<div class="trk"><i style="width:'+pct+'%"></i></div></td>'
      +'<td class="n">'+r.d+' / '+r.n+'<br><span style="font-size:.76rem;color:var(--sub,#666)">'+pct+'%</span></td>'
      +'<td class="n">'+left+' '+r.u+'</td>'
      +'<td class="n d">'+(left?('<b>'+per+'</b> '+r.u):'✓ 已完成')+'</td></tr>';
    (r.zero||[]).forEach(function(z){zeros.push(z)});
  });
  h+='</table>';
  if(zeros.length){
    h+='<div class="zero"><b>完全沒開始的有 '+zeros.length+' 項</b>——先從這裡挑一個：'
      +zeros.map(function(z){return '<a href="'+z.url+'">'+z.name+'</a>'}).join('')+'</div>';
  }else{
    h+='<div class="zero">每一樣都至少動過了，接著把上面「還沒做」的數字清掉。</div>';
  }
  el.innerHTML=h;el.hidden=false;
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',draw);else draw();
addEventListener('pageshow',draw);
})();
</script><!--/lag-->"""


def main():
    s = io.open(HUB, encoding='utf-8').read()
    blk = BLK.replace('__EXAM__', EXAM)
    m = re.search(r'<style id="lag-css">.*?<!--/lag-->', s, re.S)
    if m:
        s = s[:m.start()] + blk + s[m.end():]
        how = '已更新'
    else:
        # 放在「日拱一築」面板（hit-css … </script>）之後，不動進度分頁其他區塊
        i = s.index('<style id="hit-css">')
        j = s.index('</script>', i) + len('</script>')
        s = s[:j] + '\n' + blk + s[j:]
        how = '已插入'
    io.open(HUB, 'w', encoding='utf-8').write(s)
    print('%s 進度落後清單（%d 字；考試日 %s）' % (how, len(blk), EXAM))


if __name__ == '__main__':
    main()
