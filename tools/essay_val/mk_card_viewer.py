# -*- coding: utf-8 -*-
"""《估價_申論卡》單卡檢視頁：從《不動產估價概要_申論題實戰範文》抽出全部申論卡（<div class="essay-card" id="卡號">），
網址 #卡號（例 #pred-10、#mk-ls1，可逗號列多張）只顯示那幾張；?v=0 直接開「完整四段式」
（v 值比照經紀法規／民法：0＝完整四段式 1＝考場速寫 3＝邏輯拆解 4＝考場版；也接受 full／quick／lj／exam）。
模擬卷頁用 iframe 嵌入，讓卷內擬答與申論頁同一張卡，讀懂（bx-essay-read）、輪數與自評（bxv-es-log）同一份紀錄。
被嵌入時隱藏標題與題幹（保留「已讀」鈕）、用 postMessage {bxvCard, h} 回報內容高度（量 main，不量 scrollHeight，免得 iframe 只增不減）。
bx-essay-meta 只由申論頁寫（需要篩選列的類別名），本頁不寫。
卡片清單每次從申論頁動態讀取；申論卡新增或修改後重跑：python3 tools/essay_val/mk_card_viewer.py"""
import os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC, OUT = '不動產估價概要_申論題實戰範文.html', '估價_申論卡.html'
s = open(os.path.join(R, SRC), encoding='utf-8').read()
HE = s.find('</head>')
head = re.sub(r'<title>.*?</title>', '<title>估價｜申論卡</title>', s[:HE], count=1, flags=re.S)


def block(a, tag='div'):
    """從 s[a] 的 <tag 起，回傳配對結束位置（巢狀計數）。"""
    pat = re.compile(r'<(/?)%s\b' % tag)
    d = 0
    for m in pat.finditer(s, a):
        d += -1 if m.group(1) else 1
        if d == 0:
            return s.find('>', m.end()) + 1
    raise SystemExit('找不到配對的 </%s>（位置 %d）' % (tag, a))


cards, ids = [], []
for m in re.finditer(r'<div class="essay-card\b[^"]*"[^>]*\bid="([^"]+)"', s):
    a = m.start(); e = block(a)
    cards.append(s[a:e]); ids.append(m.group(1))
if not cards:
    sys.exit('申論頁沒有找到任何 essay-card')
assert len(set(ids)) == len(ids), '卡號重複'


def script(key):
    i = s.find(key, HE); assert i > 0, key
    a = s.rfind('<script', 0, i); b = s.find('</script>', i) + len('</script>')
    return s[a:b]


bstyles = re.findall(r'<style[^>]*>.*?</style>', s[HE:], re.S)
tpls = re.findall(r'<template id="[^"]+">.*?</template>', s[HE:], re.S)
eslog = script("var KEY='bxv-es-log'")
# 嵌入時「捲到卡片底部」要用父頁視窗判斷（iframe 本身等高，否則永遠算到底）
BOT = 'if(b.bottom<=innerHeight+80)'
assert eslog.count(BOT) == 1, 'bxv-es-log 腳本的到底判斷已變，請更新 mk_card_viewer.py'
eslog = eslog.replace(BOT, 'if(window.bxvEsBot?bxvEsBot(b):b.bottom<=innerHeight+80)')
keep = [script('var READ_KEY='),            # toggleCard／已讀 bx-essay-read
        script('// ── 計數器 ──'),            # bxvInc、主題
        '<script src="kf-fit.js"></script>',
        *tpls,
        script('id="depfig-js"'),
        eslog,                               # 輪數／自評 bxv-es-log
        script("var BY={"),                  # 這題該讀哪幾頁
        script('id="lj-js"')]                # setVer、邏輯拆解排法

body = '\n'.join(bstyles) + '''
<style id="cv-css">
body{background:var(--paper)}
.cv{max-width:860px;margin:0 auto;padding-block:8px 24px;padding-left:max(12px,env(safe-area-inset-left,0px));padding-right:max(12px,env(safe-area-inset-right,0px))}
.cv .essay-card{display:none}
.cv .essay-card.show{display:block}
.cv .cvmsg{color:var(--muted,#66706A);font-size:.9rem;padding:16px 0}
.cv .cvmsg a{color:var(--primary,#2F5D50);font-weight:700}
#esSum{display:none}
html.embed body{background:transparent;padding:0}
html.embed .cv{padding:0;max-width:none}
html.embed .cvmsg,html.embed #bxfab,html.embed #bxv-theme{display:none!important}
html.embed .cv .essay-card{border:0!important;background:transparent;margin:0;border-radius:0;overflow:visible}
html.embed .cv .card-header{cursor:default;padding:0 0 8px;border-bottom:0;justify-content:flex-end;gap:8px;background:transparent}
html.embed .cv .card-header:hover{background:transparent}
html.embed .cv .card-header-left,html.embed .cv .card-arrow,html.embed .cv .q-box{display:none}
html.embed .cv .card-body{padding:0 0 4px}
</style>
</head>
<body>
<main class="cv" id="cv"><p class="cvmsg" id="cvmsg"><a href="''' + SRC + '''">← 申論題實戰範文</a></p>
''' + '\n'.join(cards) + '''
</main>
<script id="cv-js">
(function(){
var emb=window.self!==window.top; if(emb)document.documentElement.classList.add('embed');
function show(go){var ids=decodeURIComponent(location.hash||'').replace('#','').split(',').filter(Boolean),n=0;
 document.querySelectorAll('.cv .essay-card[id]').forEach(function(c){var on=ids.indexOf(c.id)>=0;c.classList.toggle('show',on);
  if(on)n++;if(!go)return;if(on)c.classList.add('open');else c.classList.remove('open')});
 var nf=document.getElementById('cvnf');if(n&&nf)nf.remove();
 if(!n&&!nf)document.getElementById('cvmsg').insertAdjacentHTML('beforeend','<span id="cvnf">　找不到這張申論卡。</span>');
 if(!emb){var c=document.querySelector('.cv .essay-card.show .card-title');document.title=(c?c.textContent.trim()+'｜':'')+'估價申論卡'}}
var VM={'0':'full','1':'quick','3':'lj','4':'exam',full:'full',quick:'quick',lj:'lj',exam:'exam'};
function tabv(){var m=/[?&]v=(\\w+)/.exec(location.search),v=m&&VM[m[1]];if(!v)return;
 document.querySelectorAll('.cv .essay-card.show').forEach(function(c){if(typeof setVer==='function')setVer(c,v)})}
show(false);
/* 「展開」要等輪數腳本掛好監看（它看 class open 的變化）才加 */
window.addEventListener('DOMContentLoaded',function(){setTimeout(function(){show(true);tabv()},0)});
addEventListener('hashchange',function(){show(true);tabv()});
addEventListener('storage',function(e){if(e.key==='bx-theme'&&e.newValue&&typeof applyTheme==='function')applyTheme(e.newValue==='dark')});
if(emb){
 window.toggleCard=function(){};
 /* 深淺色跟父頁走 */
 var syncTheme=function(){try{var t=parent.document.documentElement.getAttribute('data-theme');if(t&&typeof applyTheme==='function')applyTheme(t==='dark')}catch(e){}};
 addEventListener('DOMContentLoaded',function(){syncTheme();try{new MutationObserver(syncTheme).observe(parent.document.documentElement,{attributes:true,attributeFilter:['data-theme']})}catch(e){}});
 var fe=null;try{fe=window.frameElement}catch(e){}
 /* 輪數：卡片底部是否進入父頁視窗；父頁捲動／點擊也算「有在看」 */
 window.bxvEsBot=function(b){try{if(!fe)return true;var r=fe.getBoundingClientRect();if(!r.width)return false;return r.top+b.bottom<=parent.innerHeight+80}catch(e){return true}};
 try{['scroll','pointerdown','keydown','touchstart'].forEach(function(ev){parent.addEventListener(ev,function(){if(fe&&fe.getClientRects().length)window.dispatchEvent(new Event('pointerdown'))},{passive:true})})}catch(e){}
 var post=function(){try{var m=document.getElementById('cv');parent.postMessage({bxvCard:location.hash,h:Math.ceil(m.getBoundingClientRect().bottom+scrollY)},'*')}catch(e){}};
 new ResizeObserver(post).observe(document.body);addEventListener('load',post);
 document.addEventListener('click',function(){setTimeout(post,30)});document.addEventListener('toggle',function(){setTimeout(post,30)},true);
}
})();
</script>
''' + '\n'.join(keep) + '''
</body>
</html>
'''
open(os.path.join(R, OUT), 'w', encoding='utf-8').write(head + body)
print('%s：申論卡 %d 張' % (OUT, len(cards)))
