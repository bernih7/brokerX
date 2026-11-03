# -*- coding: utf-8 -*-
"""《民法_申論卡》單卡檢視頁：從指揮中心抽出全部申論卡，網址 #卡號（例 #預05、#專練-一，可逗號列多張）只顯示那幾張。
模擬卷頁用 iframe 嵌入，讓卷內擬答與指揮中心同一張卡（邏輯拆解｜考場速寫｜考場版｜完整四段式），讀懂、輪數、自評同一份紀錄
（minfa_read、bxm-es-log）。被嵌入時隱藏標題與題幹、用 postMessage 回報高度。
指揮中心申論卡改了要重跑：python3 tools/essay_civ/mk_card_viewer.py（比照經紀法規 mk_card_viewer.py）"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
s = open(os.path.join(R, '民法_備考指揮中心.html'), encoding='utf-8').read()
head = s[:s.find('</head>')]
head = re.sub(r'<title>.*?</title>', '<title>民法｜申論卡</title>', head)
cards = []
for m in re.finditer(r'<details class="essay[^"]*" data-lv="\w" data-key="([^"]+)"', s):
    a = m.start(); k = m.group(1)
    e = s.find('</details>', s.find('<input type="checkbox" class="rd" data-key="%s">' % k, a)) + len('</details>')
    cards.append(s[a:e])
def script(sid):
    i = s.find('<script id="%s"' % sid); return s[i:s.find('</script>', i) + len('</script>')]
bstyles = re.findall(r'<style[^>]*>.*?</style>', s[s.find('</head>'):], re.S)
keep = [script('esl-js'), script('esrd-js'), script('lj-js')]
body = '\n'.join(bstyles) + '''
<style>
body{background:var(--bg)}
.cv{max-width:820px;margin:0 auto;padding-block:8px 24px;padding-left:max(12px,env(safe-area-inset-left,0px));padding-right:max(12px,env(safe-area-inset-right,0px))}
.cv details.essay{display:none}
.cv details.essay.show{display:block}
.cv .cvmsg{color:var(--sub);font-size:.9rem;padding:16px 0}
html.embed .cv{padding:0}
html.embed body{background:transparent}
html.embed .cvmsg{display:none}
html.embed .cv details.essay>summary{display:none}
html.embed .cv details.essay{border:0!important;background:transparent;padding:0;margin:0}
html.embed .cv .oq{display:none}
</style>
</head>
<body>
<main class="cv" id="pEss"><div id="elist"><p class="cvmsg" id="cvmsg"><a href="民法_備考指揮中心.html">← 指揮中心</a></p>
''' + '\n'.join(cards) + '''
</div></main>
<script>
(function(){
var emb=window.self!==window.top; if(emb)document.documentElement.classList.add('embed');
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.vt button');if(!b)return;var box=b.closest('.ebody');
 box.querySelectorAll('.vt button').forEach(function(x){x.classList.toggle('on',x===b)});box.querySelectorAll('.vp').forEach(function(p){p.hidden=p.dataset.v!==b.dataset.v})});
var R={};try{R=JSON.parse(localStorage.getItem('minfa_read')||'{}')}catch(e){}
document.querySelectorAll('.cv details.essay').forEach(function(d){var k=d.dataset.key,cb=d.querySelector('.rd');if(R[k]){d.classList.add('read');if(cb)cb.checked=true}
 if(cb)cb.addEventListener('change',function(){try{R=JSON.parse(localStorage.getItem('minfa_read')||'{}')}catch(e){R={}}R[k]=cb.checked;if(!cb.checked)delete R[k];d.classList.toggle('read',cb.checked);try{localStorage.setItem('minfa_read',JSON.stringify(R))}catch(e){}})});
function show(){var ids=decodeURIComponent(location.hash||'').replace('#','').split(',').filter(Boolean),n=0;
 document.querySelectorAll('.cv details.essay').forEach(function(d){var on=ids.indexOf(d.dataset.key)>=0;d.classList.toggle('show',on);if(on){d.open=true;n++}});
 if(!n&&!document.getElementById('cvnf'))document.getElementById('cvmsg').insertAdjacentHTML('beforeend','<span id="cvnf">　找不到這張申論卡。</span>')}
show();addEventListener('hashchange',show);
function tabv(){var m=/[?&]v=([0-9])/.exec(location.search);if(!m)return;document.querySelectorAll('.cv details.show').forEach(function(d){var b=d.querySelector('.vt[data-v="'+m[1]+'"],.vt button[data-v="'+m[1]+'"]');if(b)b.click()})}
tabv();addEventListener('hashchange',tabv);
if(emb){var post=function(){try{parent.postMessage({bxmCard:location.hash,h:document.documentElement.scrollHeight},'*')}catch(e){}};
 new ResizeObserver(post).observe(document.body);addEventListener('load',post);document.addEventListener('click',function(){setTimeout(post,30)});document.addEventListener('toggle',function(){setTimeout(post,30)},true)}
})();
</script>
''' + '\n'.join(keep) + '\n</body>\n</html>\n'
open(os.path.join(R, '民法_申論卡.html'), 'w', encoding='utf-8').write(head + body)
print('申論卡', len(cards), '張')
