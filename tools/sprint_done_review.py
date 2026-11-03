# -*- coding: utf-8 -*-
"""5 分鐘衝刺／推理版「已存檔」畫面加：🔁 再練一次、📖 看完整解說（另開《申論卡》完整四段式）、
回看本題（上一頁／下一頁／下拉跳頁，沒有計時）。使用者 11-03。四份模板（民法、經紀法規 × 衝刺、推理版）可重跑。
另：兩科 mk_card_viewer.py 支援 ?v=0 直接打開完整四段式分頁。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CSS = ('.dnb{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.dnb .btn{text-decoration:none;display:inline-flex;align-items:center}'
       '.rv{margin-top:16px;border-top:1px solid var(--line);padding-top:12px}.rvh{font-weight:700;margin-bottom:8px}'
       '.rvnav{display:flex;gap:8px;align-items:center}.rvnav select{flex:1;min-width:0;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:10px;padding:7px 8px;font:inherit;font-size:.88rem}'
       '.rvnav .btn{white-space:nowrap;padding:7px 12px}.rvnav .btn:disabled{opacity:.4}#rvB{margin-top:12px}'
       '.rvq{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;line-height:1.85}'
       '.ck label.miss{opacity:.75}.ck label .mk{font-weight:700;min-width:1.2em}.ck label.on .mk{color:var(--ok)}.kw.miss{opacity:.6}'
       '@media(max-width:480px){.rvnav .btn{padding:7px 10px}}')
COMMON = r'''
/* ---- 存檔後：再練一次／看完整解說／回看本題（11-03） ---- */
function doneExtra(revPages){
  var id=cur.id,b=$('body');
  b.insertAdjacentHTML('beforeend','<div class="dnb"><button type="button" class="btn" id="againBtn">🔁 再練一次</button><a class="btn" href="'+CARDU+'?v=0#'+encodeURIComponent(id)+'" target="_blank" rel="noopener">📖 看完整解說（另開）</a></div>'
    +'<div class="rv"><div class="rvh">回看本題（不計時）</div><div class="rvnav"><button type="button" class="btn" id="rvP">◀ 上一頁</button><select id="rvS" aria-label="跳到哪一頁"></select><button type="button" class="btn" id="rvN">下一頁 ▶</button></div><div id="rvB"></div></div>');
  $('againBtn').onclick=function(){$('nextBtn').onclick=next;$('quitBtn').textContent='放棄這題';start(id)};
  var P=revPages(),i=0;
  $('rvS').innerHTML=P.map(function(p,k){return '<option value="'+k+'">'+(k+1)+'／'+P.length+'　'+esc(p[0])+'</option>'}).join('');
  function go(k){i=Math.max(0,Math.min(P.length-1,k));$('rvS').value=String(i);$('rvB').innerHTML=P[i][1];$('rvP').disabled=i===0;$('rvN').disabled=i===P.length-1}
  $('rvP').onclick=function(){go(i-1)};$('rvN').onclick=function(){go(i+1)};$('rvS').onchange=function(){go(+this.value)};
  go(0);
}
'''
SPRINT_REV = r'''function sprintPages(){
  var rc='<div class="recall"><b>先不看答案，在心裡或紙上列出：</b><ol><li>會用哪幾條（條號）</li><li>要分幾點（照題目幾問）</li><li>結論一句話怎麼答</li></ol></div>'+(cur.mn?'<div class="mn">口訣：<b>'+esc(cur.mn)+'</b></div>':'');
  var ck='<div class="ck">'+cur.ck.map(function(c,i){var g=!!cur.got[i];return '<label class="'+(g?'on':'miss')+'"><span class="mk">'+(g?'✓':'✗')+'</span>'+(c.h?'<span class="must">必寫</span>':'')+'<span>'+esc(c.x)+'</span></label>'}).join('')+'</div>';
  return [[STG[0].n,'<div class="rvq">'+esc(cur.q)+'</div>'],[STG[1].n,rc],[STG[2].n,evHTML([0,1,2],[],[])],[STG[3].n,evHTML([3],[],[])],[STG[4].n+'（✓ 有勾／✗ 漏掉）',ck],['考場版全文',evHTML([0,1,2,3],[],[])]];
}
'''
REASON_REV = r'''function reasonPages(){
  var P=[[STG[0].n,'<div class="rvq">'+esc(cur.q)+'<ul class="subs">'+cur.subs.map(function(s,a){return '<li><b>問題'+CN[a]+'</b><span>'+esc(s.q)+'</span></li>'}).join('')+'</ul></div>']];
  var si0=si,sh0=shown;
  steps.forEach(function(p,k){si=k;shown=true;var a=p.x.ask||'';P.push([STG[1].n+' '+(k+1)+'／'+steps.length+'：'+(a.length>16?a.slice(0,16)+'…':a),stepHTML()])});
  si=si0;shown=sh0;
  P.push([STG[2].n,cur.sx.map(function(x){return '<div class="blk '+x[0]+'"><span class="blk-l">'+esc(x[1])+'</span>'+x[2]+'</div>'}).join('')+(cur.kou?'<div class="kou"><b>口訣</b>'+esc(cur.kou)+'</div>':'')]);
  P.push([STG[3].n,'<div class="lose">'+cur.lose.map(function(t){return '<div><b>⚠</b><span>'+esc(t)+'</span></div>'}).join('')+'</div>']);
  P.push([STG[4].n+'（綠＝有點到）','<div class="kws">'+cur.kws.map(function(k,i){return '<span class="kw'+(got[i]?' on':' miss')+'">'+(got[i]?'✓ ':'')+esc(k.c)+(k.a?'<small class="ka">'+esc(k.a)+'</small>':'')+'</span>'}).join('')+'</div>']);
  return P;
}
'''
for sub, card in (('essay_jj', '經紀法規_申論卡.html'), ('essay_civ', '民法_申論卡.html'), ('essay_val', '估價_申論卡.html')):
    for fn in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', fn); s = open(p, encoding='utf-8').read()
        if 'function doneExtra(' in s: print('skip', p); continue
        reason = fn == 'tpl_reason.html'
        cu = ('__ROOT__' if reason else '') + card
        js = "var CARDU='%s';\n" % cu + COMMON + (REASON_REV if reason else SPRINT_REV)
        a = 'function start(id){'; assert s.count(a) == 1
        s = s.replace(a, js + a, 1)
        if reason:
            a = "  st=5;$('stg').innerHTML='完成"; assert s.count(a) == 1
            s = s.replace(a, "  if(!DEMO)doneExtra(reasonPages);\n" + a, 1)
        else:
            a = "  $('stg').innerHTML='完成<small>這題的紀錄已同步</small>';"; assert s.count(a) == 1
            s = s.replace(a, "  doneExtra(sprintPages);\n" + a, 1)
        s = s.replace('</style>', CSS + '\n</style>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('ok', p)
# 申論卡 ?v=0 → 打開指定分頁
TAB = "show();addEventListener('hashchange',show);"
ADD = TAB + "\nfunction tabv(){var m=/[?&]v=([0-9])/.exec(location.search);if(!m)return;document.querySelectorAll('.cv details.show').forEach(function(d){var b=d.querySelector('.vt[data-v=\"'+m[1]+'\"],.vt button[data-v=\"'+m[1]+'\"]');if(b)b.click()})}\ntabv();addEventListener('hashchange',tabv);"
for sub in ('essay_jj', 'essay_civ'):
    p = os.path.join(R, 'tools', sub, 'mk_card_viewer.py'); s = open(p, encoding='utf-8').read()
    if 'function tabv(' in s: print('skip', p); continue
    assert s.count(TAB) == 1; s = s.replace(TAB, ADD, 1); open(p, 'w', encoding='utf-8').write(s); print('ok', p)
