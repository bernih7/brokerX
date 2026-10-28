# -*- coding: utf-8 -*-
"""施工單第 5 項：申論卡「看了幾輪・每輪多久・看完自評」。

鍵：bxj-es-log = {卡片id:{n:輪數, s:[最近5輪秒數], tot:總秒數, v:自評, t:最後時間}}
    bxj-es-read（原本的「我已讀懂」）完全不動。
計時規則（與估價 v527／本科 v573 的「捲到底」一致）：
  - 只有卡片展開時才計時；分頁切到背景或閒置 2 分鐘不計。
  - 該輪 ≥20 秒且曾捲到這張卡的底部 → 輪數 +1（同一次展開只加一次）。
可重複執行：以 <style id="eslog-css"> … </script><!--/eslog--> 為邊界整段換掉。
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')

CSS = """<style id="eslog-css">
.eslog{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:8px 0 2px;padding-top:8px;border-top:1px dashed var(--line);font-size:.8rem;color:var(--sub)}
.eslog .elst{font-variant-numeric:tabular-nums}
.eslog .elst b{color:var(--pri);font-size:.95rem}
.eslog .elv{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.eslog .elb{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:3px 10px;font-size:.78rem;cursor:pointer;font-family:inherit;line-height:1.5}
.eslog .elb:hover{border-color:var(--pri)}
.eslog .elb.on{background:var(--pri);color:var(--on);border-color:var(--pri);font-weight:700}
.eslog .elb.on[data-v="2"]{background:var(--acc);border-color:var(--acc)}
.eslog .elb.on[data-v="3"]{background:var(--bad);border-color:var(--bad)}
@media(max-width:480px){.eslog .elv{margin-left:0;width:100%}}
</style>"""

JS = """<script id="eslog-js">
/* ⑤ 申論卡：看了幾輪・每輪多久・看完自評（bxj-es-log）。bxj-es-read 不動。 */
(function(){
var KEY='bxj-es-log', MINSEC=20, IDLE=120000;
function ld(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return{}}}
function sv(o){try{localStorage.setItem(KEY,JSON.stringify(o))}catch(e){}}
var VN={1:'✅ 熟',2:'📖 還沒背起來',3:'😵 太難'};
function mins(s){return s<60?s+' 秒':Math.round(s/60)+' 分'}
function txt(r){
  if(!r||!r.n)return '還沒讀過一輪';
  var avg=r.n?Math.round((r.tot||0)/r.n):0;
  return '讀過 <b>'+r.n+'</b> 輪・共 '+mins(r.tot||0)+(r.n>1?'・平均 '+mins(avg):'')
    +(r.s&&r.s.length>1?'（最近：'+r.s.slice(0,3).map(mins).join('、')+'）':'');
}
var act=Date.now();
['pointerdown','keydown','scroll','touchstart','wheel'].forEach(function(ev){
  addEventListener(ev,function(){act=Date.now()},{passive:true})});

document.querySelectorAll('details.essay-detail').forEach(function(d){
  var id=d.id; if(!id) return;
  var host=d.querySelector('.esdone');
  var bar=document.createElement('div'); bar.className='eslog';
  var st=document.createElement('span'); st.className='elst';
  var vb=document.createElement('span'); vb.className='elv';
  [1,2,3].forEach(function(v){
    var b=document.createElement('button'); b.type='button'; b.className='elb';
    b.setAttribute('data-v',v); b.textContent=VN[v];
    b.onclick=function(){var D=ld(),r=D[id]=D[id]||{n:0,s:[],tot:0};
      r.v=(r.v===v)?0:v; r.t=Math.floor(Date.now()/1000); sv(D); paint()};
    vb.appendChild(b);
  });
  bar.appendChild(st); bar.appendChild(vb);
  if(host&&host.parentNode) host.parentNode.insertBefore(bar,host.nextSibling); else d.appendChild(bar);

  function paint(){var r=ld()[id]; st.innerHTML=txt(r)+(sec>=4?'　<span style="color:var(--acc)">本輪 '+mins(sec)+'</span>':'');
    vb.querySelectorAll('.elb').forEach(function(b){
      b.classList.toggle('on', !!r && r.v===+b.getAttribute('data-v'))})}
  /* 計時：展開才跑；背景或閒置 2 分鐘不累計 */
  var sec=0, bottomSeen=false, counted=false, iv=null;
  paint();
  function atBottom(){var q=d.getBoundingClientRect();
    return q.bottom<=innerHeight+40 && q.bottom>0}
  function stop(){ if(iv){clearInterval(iv);iv=null} sec=0; bottomSeen=false; counted=false; paint(); }
  function tickOne(){
    if(document.visibilityState!=='visible'||Date.now()-act>IDLE) return;
    sec+=2; if(atBottom())bottomSeen=true;
    var D=ld(), r=D[id]=D[id]||{n:0,s:[],tot:0};
    r.tot=(r.tot||0)+2;                       /* 秒數即時累計，不等關卡片才寫 */
    if(!counted&&sec>=MINSEC&&bottomSeen){counted=true;
      r.n=(r.n||0)+1; r.s=[sec].concat(r.s||[]).slice(0,5)}
    else if(counted&&r.s&&r.s.length){r.s[0]=sec}
    r.t=Math.floor(Date.now()/1000); sv(D); paint();
  }
  d.addEventListener('toggle',function(){
    if(iv){clearInterval(iv);iv=null}            /* 防 toggle 重複觸發造成雙計時 */
    if(d.open){sec=0;bottomSeen=false;counted=false;iv=setInterval(tickOne,2000)}
    else stop();
  });
  addEventListener('pagehide',function(){if(d.open)stop()});
  document.addEventListener('visibilitychange',function(){
    if(document.visibilityState==='hidden'&&d.open&&sec>0)stop()});
});
})();
</script><!--/eslog-->"""


def main():
    s = io.open(HUB, encoding='utf-8').read()
    blk = CSS + JS
    m = re.search(r'<style id="eslog-css">.*?<!--/eslog-->', s, re.S)
    if m:
        s = s[:m.start()] + blk + s[m.end():]
        how = '已更新'
    else:
        i = s.rindex('</body>')
        s = s[:i] + blk + '\n' + s[i:]
        how = '已插入'
    io.open(HUB, 'w', encoding='utf-8').write(s)
    print('%s 申論輪數／用時／自評區塊（%d 字）' % (how, len(blk)))


if __name__ == '__main__':
    main()
