# 申論專練卷①：加上「邏輯拆解」版本（資料 zl_lj.json），可重複執行。
# gen_zl.py 重產頁面後，要再跑本檔。
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)
from zl_data import E
from lj_render import render, CSS
P = os.path.join(ROOT, '民法_申論專練卷.html')
s = open(P, encoding='utf-8').read()
LJ = json.load(open(os.path.join(HERE, 'zl_lj.json'), encoding='utf-8'))
assert len(LJ) == len(E) == 3
E2 = []
for x, d in zip(E, LJ):
    y = dict(x); y['lj'] = render(d); E2.append(y)
i = s.index('var D=') + 6
D, end = json.JSONDecoder().raw_decode(s[i:])
D['E'] = E2
s = s[:i] + json.dumps(D, ensure_ascii=False) + s[i + end:]
def rep(a, b, n=1):
    global s
    if b in s and a not in s: return
    assert s.count(a) == n, (a[:50], s.count(a)); s = s.replace(a, b)
rep('var vs=[{n:"完整四段式",parts:x.parts}].concat(x.v||[]);',
    'var vs=(x.lj?[{n:"邏輯拆解",lj:x.lj}]:[]).concat([{n:"完整四段式",parts:x.parts}]).concat(x.v||[]);')
rep('  vs[i].parts.forEach(function(p,k){',
    '  if(vs[i].lj){var lw=document.createElement("div");lw.className="lj";lw.innerHTML=vs[i].lj;body.appendChild(lw);xb.style.display="none";if(window.ljApply)ljApply(lw);return}xb.style.display="";\n  vs[i].parts.forEach(function(p,k){')
rep('展開擬答（3 個版本）', '展開擬答（4 個版本）', 2)
rep('版本：完整版＝寫滿時用；', '版本：邏輯拆解＝一步一步推、寫完逐項勾採分點；完整版＝寫滿時用；')
VARS = ('<style id="zl-ljvar">:root{--b2:#7A4F8A;--b3:#35693F;--b4:#B8782E}'
        ':root[data-theme="dark"]{--b2:#C3A0D4;--b3:#7FC18A;--b4:#D9A863}'
        '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--b2:#C3A0D4;--b3:#7FC18A;--b4:#D9A863}}'
        '.lj .kou{margin-top:10px;border:1.5px solid var(--ok);background:var(--ok-soft);border-radius:10px;padding:7px 11px;font-size:.88rem}</style>')
JS = ('<script id="lj-js">(function(){var K="bxm-ljv";function set(v,save,root){(root||document).querySelectorAll(".ljseg button").forEach(function(b){b.classList.toggle("on",b.dataset.lj===v)});'
      '(root||document).querySelectorAll(".ljp").forEach(function(p){p.hidden=p.dataset.lj!==v});if(save){try{localStorage.setItem(K,v)}catch(e){}}}'
      'window.ljApply=function(root){try{var v=localStorage.getItem(K);if(v&&/^[ABC]$/.test(v))set(v,false,root)}catch(e){}};'
      'document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".ljseg button");if(b)set(b.dataset.lj,true)})})();</script>')
s = re.sub(r'<style id="lj-css">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<style id="zl-ljvar">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="lj-js">.*?</script>', '', s, flags=re.S)
s = s.replace('</head>', VARS + CSS + '</head>', 1)
s = s.replace('</body>', JS + '</body>', 1)
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s))
