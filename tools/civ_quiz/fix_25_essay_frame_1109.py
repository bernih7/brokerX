# -*- coding: utf-8 -*-
"""《民法概要_25題模擬測驗》申論「對照範文」改嵌入指揮中心同一張卡（民法_申論卡.html#年-題），
原 ESSAY[].m 舊範文（16 題中 10 題結論與指揮中心不同）刪除。可重跑。"""
import json, os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
fn = os.path.join(R, '民法概要_25題模擬測驗.html'); s = open(fn, encoding='utf-8').read()
i = s.index('const ESSAY=') + 12; E, e = json.JSONDecoder().raw_decode(s[i:])
for y in E:
    for x in E[y]: x.pop('m', None)
s = s[:i] + json.dumps(E, ensure_ascii=False) + s[i + e:]
old = '<details><summary>對照範文（四段式）</summary><div class="es-model">${e.m}</div></details>'
new = ('<details class="es-cfd"><summary>對照擬答（與指揮中心同一張卡）</summary><div class="cfw"><div class="cfh">四種看法：邏輯拆解｜考場速寫｜考場版｜完整四段式（讀懂、輪數同步）。'
       '<a href="民法_備考指揮中心.html#${curYear}-${e.no}" target="_blank" rel="noopener">在指揮中心開啟 ▸</a></div>'
       '<iframe class="cf" title="申論擬答" loading="lazy" src="民法_申論卡.html#${curYear}-${e.no}"></iframe></div></details>')
if old in s: s = s.replace(old, new)
assert new in s
if 'id="bxm-cardframe-css"' not in s:
    css = ('<style id="bxm-cardframe-css">.cfw{margin-top:10px}.cfh{font-size:.8rem;color:var(--sub,#5F6B63);margin-bottom:6px;line-height:1.6}'
           '.cfh a{color:var(--pri,#2F5D50);font-weight:700;white-space:nowrap}iframe.cf{display:block;width:100%;height:600px;border:0;background:transparent}</style>\n'
           '<script id="bxm-cardframe">addEventListener("message",function(ev){var d=ev.data;if(!d||!d.bxmCard)return;'
           'document.querySelectorAll("iframe.cf").forEach(function(f){if(f.contentWindow===ev.source)f.style.height=(d.h+4)+"px"})});</script>\n')
    s = s.replace('</head>', css + '</head>', 1)
open(fn, 'w', encoding='utf-8').write(s); print('ok')
