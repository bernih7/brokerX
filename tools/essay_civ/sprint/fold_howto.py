# -*- coding: utf-8 -*-
"""5 分鐘練習兩頁（民法＋經紀法規共四份模板）：首頁「流程與時間分配」與模式說明收進可展開區，平常只留模式按鈕與開始鈕。
展開狀態記在 bx-sprint-howto（四頁共用）。可重跑。改完要重跑各科 build。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
CSS = ('.howto{margin:12px 0 0;border:1px solid var(--line);border-radius:12px;background:var(--surface)}'
       '.howto>summary{cursor:pointer;list-style:none;padding:9px 14px;font-size:.9rem;color:var(--sub);display:flex;justify-content:space-between;gap:8px}'
       '.howto>summary::-webkit-details-marker{display:none}.howto>summary::after{content:"點開 ▾";font-size:.8rem}.howto[open]>summary::after{content:"收起 ▴"}'
       '.howto>summary:focus-visible{outline:2px solid var(--pri);outline-offset:2px}.howto .hb{padding:0 14px 12px}.howto .hb>*:first-child{margin-top:0}'
       '.modes .mode small{display:none}.howto[open]~.modes .mode small{display:block}')
JS = ('<script id="howto-js">(function(){var d=document.getElementById("howto");if(!d)return;'
      'try{if(localStorage.getItem("bx-sprint-howto")==="1")d.open=true}catch(e){}'
      'd.addEventListener("toggle",function(){try{localStorage.setItem("bx-sprint-howto",d.open?"1":"0")}catch(e){}})})();</script>')
SUM = '<details class="howto" id="howto"><summary>流程、時間怎麼分、兩種模式說明</summary><div class="hb">%s</div></details>\n    '
for sub in ('essay_civ', 'essay_jj', 'essay_val'):
    for t in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', t); s = open(p, encoding='utf-8').read()
        if 'id="howto"' not in s:
            if t == 'tpl.html':
                m = re.search(r'\n    <ul class="flow">.*?</ul>', s); body = m.group(0).strip()
                s = s.replace(m.group(0), '', 1)
            else:
                m = re.search(r'\n    <p class="lead" style="margin:0 0 6px">.*?</p>\n    <div class="plan">.*?\n    </div>', s, re.S); body = m.group(0).strip()
                s = s.replace(m.group(0), '', 1)
            k = s.index('<div class="modes"')
            s = s[:k] + SUM % body + s[k:]
            s = s.replace('</style>', CSS + '\n</style>', 1)
            s = s.replace('</body>', JS + '\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(s); print(sub, t, 'ok')
