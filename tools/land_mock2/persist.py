# -*- coding: utf-8 -*-
"""模擬卷（診斷卷版型）作答紀錄保存：
- 本次作答（選項、對錯、A/B/C 歸類）存 bx_mockcur_ID，重新整理不會不見。
- 按「重做」先把本次存進 bx_mockhist_ID（歷次紀錄），再清空。
- bx_mockerr_ID＝最近一次的錯題→歸類（指揮中心讀）。
- 結果分頁加「歷次紀錄」與「上次也錯」標記。
用法：python3 persist.py 檔案...（可重跑，已改過的檔會略過）"""
import sys

PAIRS = [
 # 1 狀態變數
 ('var L="ABCD",st={},cl={},cur=0,',
  'var L="ABCD",st={},cl={},pk={},CARDS={},cur=0,'),
 # 2 save 也存本次作答＋錯題
 ('localStorage.setItem("bx_mock_"+ID,JSON.stringify({a:a,c:c,n:D.Q.length,t:Date.now()}))}catch(e){}}',
  'localStorage.setItem("bx_mock_"+ID,JSON.stringify({a:a,c:c,n:D.Q.length,t:Date.now()}));'
  'localStorage.setItem("bx_mockcur_"+ID,JSON.stringify({st:st,cl:cl,pk:pk,t:Date.now()}));'
  'var er={};for(var k2 in st){if(st[k2]===false)er[k2]=cl[k2]||"未歸類"}localStorage.setItem("bx_mockerr_"+ID,JSON.stringify(er))}catch(e){}}\n'
  'function hist(){try{return JSON.parse(localStorage.getItem("bx_mockhist_"+ID)||"[]")}catch(e){return []}}\n'
  'function archive(){var a=0,c=0,w=[];for(var k in st){a++;if(st[k])c++;else w.push([+k,cl[k]||""])}if(!a)return;'
  'var h=hist();h.push({t:Date.now(),a:a,c:c,n:D.Q.length,w:w});try{localStorage.setItem("bx_mockhist_"+ID,JSON.stringify(h.slice(-20)));localStorage.removeItem("bx_mockcur_"+ID)}catch(e){}}'),
 # 3 記住選了哪個
 ('cc.classList.add("done");var ok=(L[ii]===qq.ans);st[qq.n]=ok;',
  'cc.classList.add("done");var ok=(L[ii]===qq.ans);st[qq.n]=ok;pk[qq.n]=ii;'),
 # 4 卡片參照
 ('  var c=document.createElement("div");c.className="card";\n  c.innerHTML=\'<div class="qn">第\'+q.n+\'題',
  '  var c=document.createElement("div");c.className="card";CARDS[q.n]=c;\n  c.innerHTML=\'<div class="qn">第\'+q.n+\'題'),
 # 5 歸類後也存
 ('b.onclick=(function(qq,k,bb,cc){return function(){cl[qq.n]=k;cc.querySelectorAll(".cls button").forEach(function(x){x.className=""});bb.className="sel"}})(q,t[0],b,c);',
  'b.onclick=(function(qq,k,bb,cc){return function(){cl[qq.n]=k;cc.querySelectorAll(".cls button").forEach(function(x){x.className=""});bb.className="sel";save()}})(q,t[0],b,c);b.dataset.k=t[0];'),
 # 6 重做前先存進歷次紀錄
 ('qHost.querySelector("#rs").onclick=function(){st={};cl={};',
  'qHost.querySelector("#rs").onclick=function(){archive();st={};cl={};pk={};'),
 # 7 開頁時還原本次作答
 ('mkQ(qHost);go(0);',
  'var _cur=null;try{_cur=JSON.parse(localStorage.getItem("bx_mockcur_"+ID)||"null")}catch(e){}mkQ(qHost);(function(){try{var s=_cur;if(!s||!s.pk)return;'
  'D.Q.forEach(function(q){var i=s.pk[q.n];if(i===undefined||!CARDS[q.n])return;var b=CARDS[q.n].querySelectorAll(".opt")[i];if(b)b.onclick.call(b);'
  'var k=(s.cl||{})[q.n];if(k){var x=CARDS[q.n].querySelector(\'.cls button[data-k="\'+k+\'"]\');if(x)x.onclick()}})}catch(e){}})();go(0);'),
 # 8 結果頁：上次也錯＋歷次紀錄
 ('wr.forEach(function(q){var p=document.createElement("div");p.className="row";p.style.margin="6px 0";\n'
  '  p.textContent="第"+q.n+"題｜"+q.sec+"｜"+(cl[q.n]?cl[q.n]+"型":"未歸類");ls.appendChild(p)});\n host.appendChild(d);',
  'var H=hist(),last=H.length?H[H.length-1]:null,lw={};if(last)last.w.forEach(function(x){lw[x[0]]=1});\n'
  ' wr.forEach(function(q){var p=document.createElement("div");p.className="row";p.style.margin="6px 0";\n'
  '  p.textContent="第"+q.n+"題｜"+q.sec+"｜"+(cl[q.n]?cl[q.n]+"型":"未歸類")+(lw[q.n]?"｜⚠️ 上次也錯":"");ls.appendChild(p)});\n host.appendChild(d);\n'
  ' if(H.length){var hc=document.createElement("div");hc.className="card";hc.innerHTML=\'<div class="qn">歷次紀錄（按「重做」時自動保存）</div><div class="ls"></div>\';var hl=hc.querySelector(".ls"),SEC={};D.Q.forEach(function(q){SEC[q.n]=q.sec});\n'
  '  H.slice().reverse().forEach(function(r,i){var t=new Date(r.t),dd=document.createElement("div");dd.style.margin="10px 0";\n'
  '   var hd=document.createElement("div");hd.style.fontWeight="700";hd.textContent="第"+(H.length-i)+"次｜"+(t.getMonth()+1)+"/"+t.getDate()+"｜答對 "+r.c+"/"+r.n+(r.a<r.n?"（只答 "+r.a+" 題）":"")+"｜選擇題 "+(r.c*2)+" 分"+(r.note?"｜"+r.note:"");dd.appendChild(hd);\n'
  '   r.w.slice().sort(function(a,b){return a[0]-b[0]}).forEach(function(x){var p=document.createElement("div");p.className="note";p.style.margin="2px 0";p.textContent="第"+x[0]+"題｜"+(SEC[x[0]]||"")+"｜"+(x[1]?x[1]+"型":"未歸類")+(st[x[0]]===true?"｜✅ 這次答對":st[x[0]]===false?"｜❌ 這次又錯":"");dd.appendChild(p)});\n'
  '   hl.appendChild(dd)});host.appendChild(hc)}'),
]
SEED_ANCHOR = 'var _cur=null;try{_cur=JSON.parse(localStorage.getItem("bx_mockcur_"+ID)'
SEED = ('(function(){try{if(localStorage.getItem("bx_mockseed1_"+ID))return;localStorage.setItem("bx_mockseed1_"+ID,"1");if(hist().length)return;'
        'localStorage.setItem("bx_mockhist_"+ID,JSON.stringify([{t:new Date(2026,10,12,11,53).getTime(),a:25,c:16,n:25,note:"依 11/12 截圖補登",'
        'w:[[3,"A"],[6,"C"],[8,"C"],[9,"B"],[12,"C"],[14,"A"],[18,"C"],[22,"B"],[24,"B"]]}]))}catch(e){}})();\n')

for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'bx_mockcur_' in s:
        print('skip(已改)', f); continue
    miss = [i for i, (a, b) in enumerate(PAIRS, 1) if s.count(a) != 1]
    if miss:
        print('skip(版型不同)', f, miss); continue
    for a, b in PAIRS:
        s = s.replace(a, b)
    if 'ID="landdiag1"' in s:   # 只有土地法診斷卷①有使用者截圖的第 1 次紀錄
        s = s.replace(SEED_ANCHOR, SEED + SEED_ANCHOR, 1)
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', f)
