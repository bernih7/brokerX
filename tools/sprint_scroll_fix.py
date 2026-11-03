# -*- coding: utf-8 -*-
"""5 分鐘衝刺／推理版（11-04 使用者手機截圖）：
① 進到下一段（推理版含下一步）時自動捲到內容開頭（計時列下方），不用手動往下滑；第①讀題仍停在最上面。
② 進度條修正：每段開始時，前面各段補滿、後面各段歸零——原本只更新「目前這段」，上一題或放棄的那次留下的長度會殘留。
三科（民法、經紀法規、估價）× 衝刺、推理版共 6 份模板，可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
HELP = ("function toBody(){var b=$('body');if(!b||st<1||st>4)return;var bar=document.querySelector('.bar');"
        "var y=Math.max(0,b.getBoundingClientRect().top+scrollY-(bar?bar.offsetHeight:0)-8);scrollTo({top:y,behavior:'smooth'})}\n"
        "function segFix(){[].forEach.call($('segs').children,function(g,i){if(i===st)return;var b=g.querySelector('b');if(b)b.style.width=i<st?'100%':'0%';if(i>st)g.classList.remove('over')})}\n")
for sub in ('essay_civ', 'essay_jj', 'essay_val'):
    for fn in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', fn)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        if 'function segFix(' in s: print('skip', p); continue
        a = 'function next(){'; assert s.count(a) == 1, p
        s = s.replace(a, HELP + a, 1)
        i = s.find('function next(){'); j = s.find('\n}', i)
        body = s[i:j]; n = body.count('scrollTo(0,0)'); assert n >= 1, p
        s = s[:i] + body.replace('scrollTo(0,0)', 'toBody()') + s[j:]
        a = 'function tick(first){'; assert s.count(a) == 1, p
        s = s.replace(a, a + 'if(first)segFix();', 1)
        a = "if(!v)scrollTo(0,0)}"; assert s.count(a) == 1, p
        s = s.replace(a, "if(!v){if(cur&&st>=1&&st<=4)toBody();else scrollTo(0,0)}}", 1)
        open(p, 'w', encoding='utf-8').write(s); print('ok', p, 'next 內換', n)
# ③ 推理版：plan(cur) 依本題重算各段秒數後，第①段 left 要重取（原本取到上一題的秒數）
for sub in ('essay_civ', 'essay_jj', 'essay_val'):
    p = os.path.join(R, 'tools', sub, 'sprint', 'tpl_reason.html')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if 'plan(cur);left=STG[0].s;' in s: continue
    s = s.replace("  plan(cur);\n", "  plan(cur);left=STG[0].s;  /* 11-04：plan 依本題重算秒數後才取第①段秒數（原本取到上一題的） */\n", 1)
    open(p, 'w', encoding='utf-8').write(s); print('ok left', p)
