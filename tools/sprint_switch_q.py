# -*- coding: utf-8 -*-
"""5 分鐘衝刺／推理版：題目下方加「同一題切到另一版」，以 #q=卡號 開啟另一頁並直接開始該題（使用者 11-03）。
右上角「切到…版」做題中也帶當前題號。四份模板（民法、經紀法規 × 衝刺、推理版）可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CSS = ('.swq{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin:10px 2px 0;font-size:.86rem;color:var(--sub)}'
       '.swq a{font-weight:600;white-space:nowrap}')
for sub in ('essay_jj', 'essay_civ'):
    for fn in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', fn); s = open(p, encoding='utf-8').read()
        if 'id="swq"' in s: print('skip', p); continue
        m = re.search(r'<a href="([^"]*)">(切到(推理版|考場版)) ▸</a>', s); href, lab, ver = m.group(1), m.group(2), m.group(3)
        s = s.replace(m.group(0), '<a id="swTop" href="%s">%s ▸</a>' % (href, lab), 1)
        a = '<div class="qbox" id="qbox"></div>'; assert s.count(a) == 1
        s = s.replace(a, a + '<div class="swq" id="swq"></div>', 1)
        s = s.replace('</style>', CSS + '\n</style>', 1)
        js = ('''var SWU='%s';
function swGo(id){var u=SWU+(id?'#q='+encodeURIComponent(id):'');$('swTop').href=u;var w=$('swq');if(w)w.innerHTML=id?'<span>同一題換個練法</span><a href="'+u+'">這題改用%s ▸</a>':''}
''' % (href, ver))
        a = 'function start(id){'; assert s.count(a) == 1
        s = s.replace(a, js + a, 1)
        # start 末尾設定連結：在 start 內第一行後插入
        s = s.replace(a + '\n', a + '\n  swGo(id);\n', 1)
        a = '\nhome();\n'; assert s.count(a) == 1
        s = s.replace(a, '''
(function(){var m=/^#q=(.+)$/.exec(location.hash||''),id=m?decodeURIComponent(m[1]):'';
  if(id&&CARDS.some(function(c){return c.id===id})){try{history.replaceState(null,'',location.pathname+location.search)}catch(e){}start(id)}else home()})();
''', 1)
        # 回首頁時右上連結還原
        s = s.replace("$('home').hidden=false;home();scrollTo(0,0)};", "$('home').hidden=false;swGo('');home();scrollTo(0,0)};", 1)
        open(p, 'w', encoding='utf-8').write(s); print('ok', p, ver)
