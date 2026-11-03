# -*- coding: utf-8 -*-
"""申論進度口徑統一（11-03）：指揮中心申論分頁的「已讀」改稱「讀懂」（＝自己勾的），另加一行
「看過一輪或做過 5 分鐘練習 n／N｜進度表的已讀（三種任一）m／N」，與「進度落後在哪」、工具完成度表同口徑；
回到頁面（返回鍵、切回分頁、別頁存檔）自動重算。民法、經紀法規兩個指揮中心，可重跑。"""
import os
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
def js(sel, read, log, spr, anchor):
    return ('<script id="es-any">/* 申論進度：讀懂（勾）／練過（讀過一輪或 5 分鐘練習）／任一（＝進度表已讀） */\n(function(){\n'
            "function ld(k){try{return JSON.parse(localStorage.getItem(k)||'{}')||{}}catch(e){return{}}}\n"
            "var ES=[].slice.call(document.querySelectorAll('%s'));if(!ES.length)return;\n"
            "function key(d){return d.dataset.key||d.id}\n"
            "function paint(){var R=ld('%s'),L=ld('%s'),S=ld('%s'),p=0,a=0;\n"
            " ES.forEach(function(d){var k=key(d),pr=(L[k]&&L[k].n>0)||(S[k]&&S[k].length>0);if(pr)p++;if(pr||R[k])a++});\n"
            " var el=document.getElementById('esAny');if(!el){var an=%s;if(!an)return;el=document.createElement('p');el.id='esAny';an.parentNode.insertBefore(el,an.nextSibling)}\n"
            " el.innerHTML='看過一輪或做過 5 分鐘練習 <b>'+p+'</b>／'+ES.length+'｜進度表的「已讀」（勾讀懂、看過一輪、5 分鐘練習任一）<b>'+a+'</b>／'+ES.length}\n"
            "paint();document.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')paint()});\n"
            "addEventListener('pageshow',paint);addEventListener('storage',function(e){if(e.key==='%s'||e.key==='%s'||e.key==='%s')paint()});\n"
            "document.addEventListener('change',function(e){if(e.target&&e.target.closest&&e.target.closest('%s'))setTimeout(paint,0)});\n"
            "})();</script>\n<style id=\"es-any-css\">#esAny{font-size:.82rem;color:var(--sub);margin:4px 0 8px;line-height:1.7}#esAny b{color:var(--ink)}</style>\n"
            ) % (sel, read, log, spr, anchor, read, log, spr, sel)
CFG = [
    ('民法_備考指揮中心.html', 'details.essay', 'minfa_read', 'bxm-es-log', 'bxm-es-sprint',
     "document.getElementById('eslSum')||document.getElementById('rcount')",
     [("sb.textContent='已讀　官方 '", "sb.textContent='讀懂　官方 '"), ("textContent='顯示 '+n+' 題｜已讀 '", "textContent='顯示 '+n+' 題｜讀懂 '"),
      ("sv(L);st.sec=0;paint(e);sum()} setInterval", None)],
     ("\nsum();\n})();", "\nsum();\ndocument.addEventListener('visibilitychange',function(){if(document.visibilityState==='visible')sum()});addEventListener('pageshow',sum);\n})();")),
    ('經紀法規_備考指揮中心.html', '.essay-detail[id^=es-]', 'bxj-es-read', 'bxj-es-log', 'bxj-es-sprint',
     "(document.getElementById('esPrgI')||{}).parentNode",
     [("<span class=\"esn\">已讀 '", "<span class=\"esn\">讀懂 '"),
      ("'在申論卡勾「我已讀懂這題的邏輯」'", "'勾讀懂、看完一輪或做過 5 分鐘練習都算'"),
      ("ES.forEach(function(d){if(RD[d.id]||(LG[d.id]&&(LG[d.id].n||0)>0))esRead++});",
       "var SPX={};try{SPX=JSON.parse(localStorage.getItem('bxj-es-sprint')||'{}')||{}}catch(e){}   ES.forEach(function(d){if(RD[d.id]||(LG[d.id]&&(LG[d.id].n||0)>0)||(SPX[d.id]&&SPX[d.id].length))esRead++});")], None),
]
for fn, sel, rd, lg, sp, anchor, reps, sumfix in CFG:
    p = os.path.join(R, fn); s = open(p, encoding='utf-8').read()
    for a, b in reps:
        if b is None: continue
        if b in s: continue
        assert s.count(a) == 1, (fn, a); s = s.replace(a, b, 1)
    if sumfix and sumfix[1] not in s:
        a = sumfix[0]; i = s.find('<script id="esl-js">'); j = s.find('</script>', i); seg = s[i:j]
        assert seg.count(a) == 1, fn; s = s[:i] + seg.replace(a, sumfix[1]) + s[j:]
    import re
    s = re.sub(r'<script id="es-any">.*?</script>\n<style id="es-any-css">.*?</style>\n', '', s, flags=re.S)
    k = s.rfind('</body>'); s = s[:k] + js(sel, rd, lg, sp, anchor) + s[k:]
    open(p, 'w', encoding='utf-8').write(s); print('ok', fn)
