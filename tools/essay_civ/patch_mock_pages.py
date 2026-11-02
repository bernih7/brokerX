# -*- coding: utf-8 -*-
"""民法模擬卷頁的申論擬答改嵌入指揮中心同一張申論卡（《民法_申論卡》iframe，改自經紀法規 mock2/patch_mock_pages.py）：
邏輯拆解｜考場速寫｜考場版｜完整四段式，內容與紀錄和指揮中心一致。模擬試題一、二的 4 題＝預05、預08、預01、預06（題目相同）。
來勝模擬(一) 另保留老師版與對照。可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PAGES = {'民法_模擬試題一.html': ['預05', '預08'], '民法_模擬試題二.html': ['預01', '預06'],
         '民法_申論專練卷.html': ['專練-一', '專練-二', '專練-三'], '民法_來勝模擬試題一.html': ['來勝-一', '來勝-二']}
HELP = r'''<script id="bxm-cardframe">
/* 申論擬答＝指揮中心同一張卡（iframe 自動調高） */
function bxmCardFrame(eid){var w=document.createElement('div');w.className='cfw';
 w.innerHTML='<div class="cfh">四種看法與指揮中心同一張卡：邏輯拆解｜考場速寫｜考場版｜完整四段式（讀懂、輪數、自評同步）。<a href="民法_備考指揮中心.html#'+eid+'" target="_blank" rel="noopener">在指揮中心開啟 ▸</a></div>'
  +'<iframe class="cf" title="申論擬答" loading="lazy" src="民法_申論卡.html#'+eid+'"></iframe>';return w}
function bxmTeacher(x){var ts=(x.v||[]).filter(function(v){return v.n.indexOf('老師')>=0});if(!ts.length)return null;
 var w=document.createElement('div');var e=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')};
 ts.forEach(function(t){var d=document.createElement('details');d.className='tch';
 d.innerHTML='<summary>'+e(t.n)+'</summary>'+(t.src?'<p class="tsrc">'+e(t.src)+'</p>':'')+t.parts.map(function(p){return '<h4>'+e(p[0])+'</h4>'+String(p[1]).split('\n').map(function(l){return '<p>'+e(l)+'</p>'}).join('')}).join('');w.appendChild(d)});return w}
addEventListener('message',function(ev){var d=ev.data;if(!d||!d.bxmCard)return;document.querySelectorAll('iframe.cf').forEach(function(f){if(f.contentWindow===ev.source)f.style.height=(d.h+4)+'px'})});
</script>
<style id="bxm-cardframe-css">
.cfw{margin-top:10px}
.cfh{font-size:.8rem;color:var(--sub,#5F6B63);margin-bottom:6px;line-height:1.6}
.cfh a{color:var(--pri,#2F5D50);font-weight:700;white-space:nowrap}
iframe.cf{display:block;width:100%;height:600px;border:0;background:transparent}
details.tch{margin-top:12px;border-top:1px dashed var(--line,#DAD6C3);padding-top:8px}
details.tch summary{cursor:pointer;font-weight:700}
details.tch h4{margin:10px 0 2px}details.tch p{margin:2px 0;line-height:1.8}.tch .tsrc{font-size:.8rem;color:var(--sub,#5F6B63)}
</style>'''
for f, ids in PAGES.items():
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<script id="bxm-cardframe">.*?</style>', '', s, flags=re.S)
    s = s.replace('</head>', HELP + '\n</head>', 1)
    s = re.sub(r'var BXM_EIDS=\[[^\]]*\];', '', s)
    s = s.replace('<script>', '<script>var BXM_EIDS=%s;' % ('[' + ','.join('"%s"' % i for i in ids) + ']'), 1) if 'var BXM_EIDS=' not in s else s
    n0 = s.count('renderVers(a,x);')
    s = s.replace('D.E.forEach(function(x){', 'D.E.forEach(function(x,xi){')
    s = s.replace('renderVers(a,x);', 'a.appendChild(bxmCardFrame(BXM_EIDS[xi]));var _t=bxmTeacher(x);if(_t)a.appendChild(_t);')
    for a, b in [('展開擬答（3 個版本）對照', '展開擬答對照'), ('展開擬答（3 個版本）', '展開擬答（邏輯拆解｜考場速寫｜考場版｜完整四段式）'),
                 ('展開擬答（4 個版本）', '展開擬答（邏輯拆解｜考場速寫｜考場版｜完整四段式）'),
                 ('展開擬答（5 個版本，含來勝老師版與對照）', '展開擬答（邏輯拆解｜考場速寫｜考場版｜完整四段式＋老師版）')]:
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    print(f, '改寫', n0, '處；剩', s.count('renderVers(a,x);'))
