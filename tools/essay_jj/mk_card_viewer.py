# -*- coding: utf-8 -*-
"""《經紀法規_申論卡》：從指揮中心抽出全部申論卡，網址 #es-xxx 只顯示那一張（可逗號列多張）。
模擬卷頁用 iframe 嵌入，讓卷內擬答與指揮中心同一張卡（邏輯拆解｜考場速寫｜考場版｜完整四段式），紀錄同步。
指揮中心申論卡改了要重跑：python3 tools/essay_jj/mk_card_viewer.py"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
s = open(os.path.join(R, '經紀法規_備考指揮中心.html'), encoding='utf-8').read()
head = s[:s.find('</head>')]
head = re.sub(r'<title>.*?</title>', '<title>經紀法規｜申論卡</title>', head)
cards = []
for m in re.finditer(r'<details id="(es-[^"]+)" class="essay-detail', s):
    a = m.start(); e = s.find('</details>', s.find('<label class="esdone"', a)) + len('</details>')
    cards.append(s[a:e])
def script(key):
    i = s.find(key); a = s.rfind('<script', 0, i); b = s.find('</script>', i) + len('</script>')
    return s[a:b]
bstyles = re.findall(r'<style[^>]*>.*?</style>', s[s.find('</head>'):], re.S)
keep = [script('申論已讀 bxj-es-read'), script('id="eslog-js"'), script('id="sprint-sync"'), script('id="lj-js"')]
body = '\n'.join(bstyles) + '''
<style>
body{background:var(--bg)}
.cv{max-width:820px;margin:0 auto;padding-block:8px 24px;padding-left:max(12px,env(safe-area-inset-left,0px));padding-right:max(12px,env(safe-area-inset-right,0px))}
.cv details.essay-detail{display:none}
.cv details.essay-detail.show{display:block}
.cv .cvmsg{color:var(--sub);font-size:.9rem;padding:16px 0}
html.embed .cv{padding:0}
html.embed body{background:transparent}
html.embed .cvmsg{display:none}
html.embed .cv details.essay-detail>summary{display:none}
html.embed .cv details.essay-detail{border:0;background:transparent;padding:0;margin:0}
html.embed .cv .essay-question,html.embed .cv .mksrc{display:none}
</style>
</head>
<body>
<main class="cv" id="cv"><p class="cvmsg" id="cvmsg"><a href="經紀法規_備考指揮中心.html">← 指揮中心</a></p>
''' + ''.join(cards) + '''
</main>
<script>
(function(){
var emb=window.self!==window.top; if(emb)document.documentElement.classList.add('embed');
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.vt');if(!b)return;var body=b.closest('.essay-body');
 body.querySelectorAll('.vt').forEach(function(x){x.classList.toggle('on',x===b)});body.querySelectorAll('.vp').forEach(function(p){p.hidden=p.dataset.v!==b.dataset.v})});
function show(){var ids=(location.hash||'').replace('#','').split(',').filter(Boolean),n=0;
 document.querySelectorAll('.cv details.essay-detail').forEach(function(d){var on=ids.indexOf(d.id)>=0;d.classList.toggle('show',on);if(on){d.open=true;n++}});
 if(!n)document.getElementById('cvmsg').insertAdjacentHTML('beforeend','　找不到這張申論卡。')}
show();addEventListener('hashchange',show);
if(emb){var post=function(){try{parent.postMessage({bxjCard:location.hash,h:document.documentElement.scrollHeight},'*')}catch(e){}};
 new ResizeObserver(post).observe(document.body);addEventListener('load',post);document.addEventListener('click',function(){setTimeout(post,30)})}
})();
</script>
''' + '\n'.join(keep) + '\n</body>\n</html>\n'
open(os.path.join(R, '經紀法規_申論卡.html'), 'w', encoding='utf-8').write(head + body)
print('申論卡', len(cards), '張')
