# -*- coding: utf-8 -*-
"""模擬卷頁的申論擬答改嵌入指揮中心同一張申論卡（《經紀法規_申論卡》iframe）：
邏輯拆解｜考場速寫｜考場版｜完整四段式，內容與紀錄和指揮中心一致。來勝模擬(一) 另保留老師版。可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
PAGES = {'經紀法規_全真模擬卷四.html': ['es-mk3', 'es-mk4'], '經紀法規_缺口補強卷五.html': ['es-mk5', 'es-mk6'],
         '經紀法規_申論專練卷.html': ['es-mk7', 'es-mk8', 'es-mk9'], '經紀法規_模擬試題一_曾榮耀.html': ['es-mk1', 'es-mk2']}
HELP = r'''<script id="bxj-cardframe">
/* 申論擬答＝指揮中心同一張卡（iframe 自動調高） */
function bxjCardFrame(eid){var w=document.createElement('div');w.className='cfw';
 w.innerHTML='<div class="cfh">四種看法與指揮中心同一張卡：邏輯拆解｜考場速寫｜考場版｜完整四段式（讀懂、輪數、自評同步）。<a href="經紀法規_備考指揮中心.html#'+eid+'" target="_blank" rel="noopener">在指揮中心開啟 ▸</a></div>'
  +'<iframe class="cf" title="申論擬答" loading="lazy" src="經紀法規_申論卡.html#'+eid+'"></iframe>';return w}
function bxjTeacher(x){var t=(x.v||[]).filter(function(v){return v.n==='老師版'})[0];if(!t)return null;
 var d=document.createElement('details');d.className='tch';var e=function(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')};
 d.innerHTML='<summary>老師版擬答（補習班解答原文）</summary>'+(t.src?'<p class="tsrc">'+e(t.src)+'</p>':'')+t.parts.map(function(p){return '<h4>'+e(p[0])+'</h4>'+String(p[1]).split('\n').map(function(l){return '<p>'+e(l)+'</p>'}).join('')}).join('');return d}
addEventListener('message',function(ev){var d=ev.data;if(!d||!d.bxjCard)return;document.querySelectorAll('iframe.cf').forEach(function(f){if(f.contentWindow===ev.source)f.style.height=(d.h+4)+'px'})});
</script>
<style id="bxj-cardframe-css">
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
    s = re.sub(r'<script id="bxj-cardframe">.*?</style>', '', s, flags=re.S)
    s = s.replace('</body>', HELP + '\n</body>', 1)
    s = re.sub(r'var BXJ_EIDS=\[[^\]]*\];', '', s)
    s = s.replace('<script>', '<script>var BXJ_EIDS=%s;' % ('[' + ','.join('"%s"' % i for i in ids) + ']'), 1) if 'var BXJ_EIDS=' not in s else s
    n0 = s.count('renderVers(a,x);')
    s = s.replace('D.E.forEach(function(x){', 'D.E.forEach(function(x,xi){')
    s = s.replace('renderVers(a,x);', 'a.appendChild(bxjCardFrame(BXJ_EIDS[xi]));var _t=bxjTeacher(x);if(_t)a.appendChild(_t);')
    s = s.replace('展開擬答（3 個版本）', '展開擬答（邏輯拆解｜考場速寫｜考場版｜完整四段式）').replace('展開擬答（含老師版）', '展開擬答（邏輯拆解｜考場速寫｜考場版｜完整四段式＋老師版）')
    s = s.replace('再展開擬答（3 個版本）對照', '再展開擬答對照').replace('每題擬答都附「考場速寫版」與「得分關鍵與失分點」。', '擬答與指揮中心申論卡同一張（四種看法）。')
    open(p, 'w', encoding='utf-8').write(s)
    print(f, '改寫', n0, '處；剩', s.count('renderVers(a,x);'))
