# 三科（民法・估價・經紀法規）5 分鐘衝刺／推理版：首頁最上方類別篩選（11-05，比照土地法 essay_land/sprint/patch_filter.py；可重跑）
import os, re, sys, json, importlib.util
T = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pf', os.path.join(T, 'essay_land', 'sprint', 'patch_filter.py'))
src = open(os.path.join(T, 'essay_land', 'sprint', 'patch_filter.py'), encoding='utf-8').read()
CSS = re.search(r"CSS='''(.*?)'''", src, re.S).group(1)
JS0 = re.search(r"JS='''(.*?)'''", src, re.S).group(1)
CFG = {'essay_civ': ('bxm-sprint-flt', '預測'), 'essay_val': ('bxv-sprint-flt', '預測'), 'essay_jj': ('bxj-sprint-flt', '預測')}
for d, (key, plab) in CFG.items():
    js = JS0.replace("'bx-land-sprint-flt'", "'%s'" % key)
    js = re.sub(r"var GS=\{[^}]*\};", "var GS={};", js)
    js = js.replace("if(FLT.k&&c.k!==FLT.k)return false;", "if(FLT.k&&(FLT.k==='mock'?(c.k==='off'||c.k==='pred'):c.k!==FLT.k))return false;")
    js = js.replace("['pred','預測・專題']", "['pred','%s']" % plab)
    for fn in ['tpl.html', 'tpl_reason.html']:
        p = os.path.join(T, d, 'sprint', fn)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        if '/*flt*/' in s: print(d, fn, '已有'); continue
        s = s.replace('</style>', CSS + '</style>', 1)
        s = re.sub(r'(<p class="lead">.*?</p>)', lambda m: m.group(1) + '\n    <div class="flt" id="flt"></div>', s, count=1, flags=re.S)
        s = s.replace("var arr=CARDS.map(function(c,i){var s=stat(c.id);return {c:c,s:s,i:i}});", "var arr=CARDS.map(function(c,i){var s=stat(c.id);return {c:c,s:s,i:i}}).filter(function(x){return fpass(x.c,x.s)});", 1)
        s = s.replace("var arr=CARDS.map(function(c,i){return {c:c,s:stat(c.id),i:i}});", "var arr=CARDS.map(function(c,i){return {c:c,s:stat(c.id),i:i}}).filter(function(x){return fpass(x.c,x.s)});", 1)
        s = s.replace("function randPick(ex){var a=CARDS.filter(function(c){return c.id!==ex});", "function randPick(ex){var a=fpool().filter(function(c){return c.id!==ex});if(!a.length)a=CARDS.filter(function(c){return c.id!==ex});", 1)
        s = s.replace("$('startBtn').onclick=function(){pick='order';start(order()[0].c.id)};", "$('startBtn').onclick=function(){pick='order';var o=order();if(!o.length){alert0();return}start(o[0].c.id)};\nfunction alert0(){var f=$('flt');if(f){f.scrollIntoView({block:'start'});f.style.outline='2px solid var(--bad)';setTimeout(function(){f.style.outline=''},1200)}}", 1)
        s = s.replace("var showAll=false;", "var showAll=false;\n" + js, 1)
        s = s.replace("function home(){\n  swGo('');", "function home(){\n  swGo('');fdraw();", 1)
        assert s.count('fpass(') >= 3 and 'fdraw();' in s and 'id="flt"' in s and 'alert0()' in s, (d, fn)
        open(p, 'w', encoding='utf-8').write(s); print(d, fn, 'ok')
