# -*- coding: utf-8 -*-
"""民法指揮中心：申論分頁加兩個 5 分鐘練習入口；申論卡紀錄列顯示衝刺次數與分數（讀 bxm-es-sprint）；
回到此頁自動重讀 bxm-es-log／bxm-es-sprint；申論標題題數依實際卡片。可重跑（改自經紀法規 sprint/patch_hub.py）"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
f = os.path.join(R, '民法_備考指揮中心.html'); s = open(f, encoding='utf-8').read()
off = len(re.findall(r'data-lv="[ABC]" data-key=', s)); pr = s.count('data-lv="P" data-key='); mk = s.count('data-lv="M" data-key=')
s = re.sub(r'data-go2="ess"><i>\d+</i><div><b>申論 \d+ 題（[^<]*）</b>', 'data-go2="ess"><i>%d</i><div><b>申論 %d 題（官方%d＋預測%d＋模擬卷%d）</b>' % (off + pr + mk, off + pr + mk, off, pr, mk), s)
s = re.sub(r'<div class="section-title">申論（[^<]*）</div>', '<div class="section-title">申論（官方 %d 題＋預測 %d 題＋模擬卷 %d 題）</div>' % (off, pr, mk), s, count=1)
for lv, lab in (('A', 'A級'), ('B', 'B級'), ('C', 'C級')):
    s = re.sub(r'(<button data-f="%s"><span class="dot %s"></span>)%s \d+' % (lv, lv, lab), r'\g<1>%s %d' % (lab, s.count('data-lv="%s" data-key=' % lv)), s)
s = re.sub(r'<button data-f="all" class="on">全部 \d+</button>', '<button data-f="all" class="on">全部 %d</button>' % (off + pr + mk), s)
s = re.sub(r'<button data-f="P">預測 \d+</button>', '<button data-f="P">預測 %d</button>' % pr, s)
LINK = ('<a class="row" id="spLink" href="%E6%B0%91%E6%B3%95_%E7%94%B3%E8%AB%965%E5%88%86%E9%90%98%E8%A1%9D%E5%88%BA.html"><div class="n"><b>⏱ 申論 5 分鐘衝刺</b><small>一題 5 分鐘：讀題→先自己想→考場版→結論→關鍵檢核打分；沒做過的優先，再來不熟的；可 🎲 隨機出題</small></div><span class="b mid">練習</span></a>'
        '<a class="row" id="spLink2" href="%E6%B0%91%E6%B3%95_%E7%94%B3%E8%AB%965%E5%88%86%E9%90%98_%E6%8E%A8%E7%90%86%E7%89%88.html"><div class="n"><b>🧩 申論 5 分鐘・推理版</b><small>跟著推理鏈一步步自問自答→速寫骨架→失分點→關鍵詞檢核；秒數依題目內容分配</small></div><span class="b mid">練習</span></a>')
s = re.sub(r'<a class="row" id="spLink".*?</a><a class="row" id="spLink2".*?</a>', '', s, flags=re.S)
k = s.find('<a class="row" href="%E6%B0%91%E6%B3%95_%E7%94%B3%E8%AB%96115%E5%87%BA%E9%A1%8C%E9%A0%90%E6%B8%AC.html">'); assert k > 0
s = s[:k] + LINK + s[k:]
JS = '''<script id="sprint-sync">
/* 5 分鐘練習紀錄（bxm-es-sprint）顯示在每張申論卡紀錄列；bxm-es-log 由練習頁寫入時，回到此頁重讀輪數與自評 */
(function(){
function ld(k){try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return{}}}
function fmt(x){x=Math.round(x||0);return Math.floor(x/60)+':'+('0'+(x%60)).slice(-2)}
var VI={ok:'✅',mem:'📖',hard:'😵'};
function paint(){
  var S=ld('bxm-es-sprint'),L=ld('bxm-es-log');
  document.querySelectorAll('details.essay').forEach(function(d){
    var k=d.dataset.key,bar=d.querySelector('.esl'),x=L[k]||{},a=S[k]||[];
    if(bar){var sp=bar.querySelector('.elsp');if(!sp){sp=document.createElement('span');sp.className='elsp';bar.insertBefore(sp,bar.querySelector('button'))}
      var ar=a.filter(function(r){return r.f!=='r'}),rr=a.filter(function(r){return r.f==='r'});
      sp.innerHTML=(ar.length?'⏱ 衝刺 <b>'+ar.length+'</b> 次・最近 '+ar[0].sc+'／'+ar[0].mx:'')+(rr.length?(ar.length?'｜':'')+'🧩 推理 <b>'+rr.length+'</b> 次・最近 '+rr[0].sc+'／'+rr[0].mx:'');
      if(!d.open){var st=bar.querySelector('.eslst'),last=x.s&&x.s.length?x.s[x.s.length-1]:0;
        if(st)st.innerHTML=x.n?('看過 <b>'+x.n+'</b> 輪・累計 <b>'+fmt(x.tot)+'</b>'+(last?'・上一輪 '+fmt(last):'')):'還沒有完整看完一輪（展開讀滿 20 秒並捲到這裡＝一輪）'}
      bar.querySelectorAll('button[data-v]').forEach(function(b){b.classList.toggle('on',b.dataset.v===x.v)})}
    var et=d.querySelector('summary .et .eslv');if(et)et.textContent=x.v?VI[x.v]:'';
    if(x.n||a.length)d.classList.add('practiced');
  });
}
paint();
document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')paint()});
addEventListener('storage',function(e){if(e.key==='bxm-es-sprint'||e.key==='bxm-es-log')paint()});
addEventListener('pageshow',paint);
})();
</script>
<style id="sprint-css">.esl .elsp{font-size:.8rem;color:var(--sub)}.esl .elsp:empty{display:none}.esl .elsp b{color:var(--pri)}</style>
'''
s = re.sub(r'<script id="sprint-sync">.*?</script>\n<style id="sprint-css">.*?</style>\n', '', s, flags=re.S)
k = s.find('<script id="esl-js">'); k = s.find('</script>', k) + len('</script>')
s = s[:k] + '\n' + JS + s[k:]
open(f, 'w', encoding='utf-8').write(s); print('ok', off, pr, mk)
