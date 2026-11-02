# 指揮中心：申論分頁加「5 分鐘衝刺」入口；申論卡紀錄列顯示衝刺次數與分數（讀 bxj-es-sprint，與衝刺頁同步）。可重跑
import os
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
f=os.path.join(R,'經紀法規_備考指揮中心.html'); s=open(f,encoding='utf-8').read()
s=s.replace('17 主題・考過幾次','16 主題・考過幾次')
LINK='''<a class="tool-link" id="spLink" href="經紀法規_申論5分鐘衝刺.html" target="_blank" rel="noopener"><div><div class="name">⏱ 申論 5 分鐘衝刺</div><div class="tag">一題 5 分鐘：讀題→先自己想→考場版→結論→關鍵檢核打分；沒做過的優先，再來不熟的</div></div><span class="badge gold">練習</span></a>
    '''
if 'id="spLink"' not in s:
    k=s.find('<a class="tool-link" href="https://bernih7.github.io/brokerX/%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F%E7%94%B3%E8%AB%96%E9%A1%8C_%E7%AF%87%E7%AB%A0')
    assert k>0; s=s[:k]+LINK+s[k:]
JS='''<script id="sprint-sync">
/* 5 分鐘衝刺紀錄（bxj-es-sprint）顯示在每張申論卡的紀錄列；回到此頁時重讀，與衝刺頁同步 */
(function(){
function ld(k){try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return{}}}
function mins(s){return s<60?s+' 秒':Math.round(s/60)+' 分'}
function txt(r){if(!r||!r.n)return '還沒讀過一輪';var avg=Math.round((r.tot||0)/r.n);return '讀過 <b>'+r.n+'</b> 輪・共 '+mins(r.tot||0)+(r.n>1?'・平均 '+mins(avg):'')+(r.s&&r.s.length>1?'（最近：'+r.s.slice(0,3).map(mins).join('、')+'）':'')}
function paint(){
  var S=ld('bxj-es-sprint'),L=ld('bxj-es-log');
  document.querySelectorAll('details.essay-detail').forEach(function(d){
    var bar=d.querySelector('.eslog'); if(!bar)return;
    var sp=bar.querySelector('.elsp'); if(!sp){sp=document.createElement('span');sp.className='elsp';bar.insertBefore(sp,bar.querySelector('.elv'))}
    var a=S[d.id]||[], r=L[d.id]||{};
    sp.innerHTML=a.length?'⏱ 衝刺 <b>'+a.length+'</b> 次・最近 '+a[0].sc+'／'+a[0].mx:'';
    var st=bar.querySelector('.elst'); if(st&&!d.open)st.innerHTML=txt(r);
    bar.querySelectorAll('.elb').forEach(function(b){b.classList.toggle('on',!!r.v&&r.v===+b.getAttribute('data-v'))});
  });
}
paint();
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')paint()});
addEventListener('storage',function(e){if(e.key==='bxj-es-sprint'||e.key==='bxj-es-log')paint()});
addEventListener('pageshow',paint);
})();
</script>
<style id="sprint-css">.eslog .elsp{font-size:.8rem;color:var(--sub)}.eslog .elsp:empty{display:none}.eslog .elsp b{color:var(--pri)}</style>
'''
if 'id="sprint-sync"' not in s:
    k=s.find('<script id="eslog-js">'); k=s.find('</script>',k)+len('</script>')
    s=s[:k]+'\n'+JS+s[k:]
open(f,'w',encoding='utf-8').write(s); print('ok')
