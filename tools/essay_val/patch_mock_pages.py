# -*- coding: utf-8 -*-
"""估價模擬卷頁的申論擬答改嵌入申論頁同一張卡（《估價_申論卡》iframe；比照 tools/essay_jj/mock2/patch_mock_pages.py）：
邏輯拆解｜考場速寫｜考場版｜完整四段式，讀懂（bx-essay-read）、輪數與自評（bxv-es-log）與《不動產估價概要_申論題實戰範文》同一份紀錄。
・綜合模擬卷一～五：「顯示擬答」展開後＝嵌入卡；卷頁原擬答架構原文收進 <details class="oldans">（備查，不刪）。
・來勝模擬試題一（補習班卷）：老師版原文照留；另加嵌入卡；原「本站擬答／本站補充」收進 <details class="oldans">。
iframe 等展開才載入（data-src），高度由卡頁 postMessage {bxvCard,h} 回報。可重跑（先拆掉上次插入的再插）。
用法：python3 tools/essay_val/patch_mock_pages.py [目錄]   （目錄預設＝站台根目錄；試跑時給副本目錄）"""
import os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else R
ESSAY, VIEW = '不動產估價概要_申論題實戰範文.html', '估價_申論卡.html'
MOCK = {'估價_綜合模擬卷一.html': ['mk-c1-1', 'mk-c1-2'], '估價_綜合模擬卷二.html': ['mk-c2-1', 'pred-10'],
        '估價_綜合模擬卷三.html': ['mk-c3-1', 'pred-2'], '估價_綜合模擬卷四.html': ['mk-c4-1', 'mk-c4-2'],
        '估價_綜合模擬卷五.html': ['mk-c5-1', 'pred-4']}
LS = {'估價_來勝模擬試題一.html': ['mk-ls1', 'mk-ls2']}
TABS = '邏輯拆解｜考場速寫｜考場版｜完整四段式'
HELP = r'''<script id="bxv-cardframe">
/* 申論擬答＝申論頁同一張卡（iframe 展開才載入、自動調高） */
function bxvCfLoad(root){if(!root)return;root.querySelectorAll('iframe.cf[data-src]').forEach(function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})}
addEventListener('message',function(ev){var d=ev.data;if(!d||!d.bxvCard)return;document.querySelectorAll('iframe.cf').forEach(function(f){if(f.contentWindow===ev.source)f.style.height=(d.h+4)+'px'})});
document.addEventListener('toggle',function(e){var t=e.target;if(t&&t.open&&t.classList&&t.classList.contains('cfd'))bxvCfLoad(t)},true);
</script>
<style id="bxv-cardframe-css">
.cfw{margin-top:4px}
.cfh{font-size:.8rem;color:var(--ink-soft,var(--muted,#66706A));margin-bottom:6px;line-height:1.6}
.cfh a{color:var(--pri-tx,var(--pri,#2F5D50));font-weight:700;white-space:nowrap}
iframe.cf{display:block;width:100%;height:600px;border:0;background:transparent;color-scheme:normal}
details.cfd{margin:0 0 8px}
details.cfd>summary,details.oldans>summary{cursor:pointer;font-weight:700}
details.oldans{margin-top:14px;border-top:1px dashed var(--rule,var(--line,#DDD6C0));padding-top:8px}
details.oldans>summary{font-size:.85rem;color:var(--ink-soft,var(--muted,#66706A))}
</style>'''


def match_end(t, a, tag):
    d = 0
    for m in re.finditer(r'<(/?)%s\b' % tag, t[a:]):
        d += -1 if m.group(1) else 1
        if d == 0:
            return t.find('>', a + m.end()) + 1
    raise SystemExit('找不到配對的 </%s>' % tag)


def frame(eid):
    return ('<!--bxv-cf--><div class="cfw" data-eid="%s"><div class="cfh">四種看法與申論範文頁同一張卡：%s（讀懂、輪數、自評同步）。'
            '<a href="%s#%s" target="_blank" rel="noopener">在申論範文頁開啟 ▸</a></div>'
            '<iframe class="cf" title="申論擬答" loading="lazy" data-src="%s#%s"></iframe></div><!--/bxv-cf-->') % (eid, TABS, ESSAY, eid, VIEW, eid)


def strip(s):
    s = re.sub(r'<script id="bxv-cardframe">.*?</style>\n?', '', s, flags=re.S)
    return re.sub(r'\n?[ ]*<!--bxv-cf-->.*?<!--/bxv-cf-->', '', s, flags=re.S)


def cards(s):
    return [m.start() for m in re.finditer(r'<div class="essay-card">', s)]


have = set(re.findall(r'<div class="essay-card\b[^"]*"[^>]*\bid="([^"]+)"', open(os.path.join(R, ESSAY), encoding='utf-8').read()))
miss = [i for v in list(MOCK.values()) + list(LS.values()) for i in v if i not in have]
if miss:
    print('⚠ 申論頁尚無這些卡（嵌入會顯示「找不到」，補卡後重跑 mk_card_viewer.py 即可，不必重跑本腳本）：', '、'.join(miss))

for f, ids in MOCK.items():
    p = os.path.join(D, f); s = strip(open(p, encoding='utf-8').read())
    pos = cards(s); assert len(pos) == len(ids), (f, len(pos))
    for k in range(len(ids) - 1, -1, -1):                     # 由後往前改，位置不位移
        a = pos[k]; e = match_end(s, a, 'div'); c = s[a:e]
        i = c.find('<div class="essay-ans">'); assert i > 0, f
        j = match_end(c, i, 'div'); o = i + len('<div class="essay-ans">'); inner = c[o:j - len('</div>')]
        if '<details class="oldans">' not in inner:
            inner = '\n<details class="oldans"><summary>本卷原附擬答架構（備查）</summary>' + inner + '</details>\n'
        c = c[:o] + frame(ids[k]) + inner + '</div>' + c[j:]
        s = s[:a] + c + s[e:]
    s = s.replace('▼ 顯示擬答架構', '▼ 顯示擬答（%s）' % TABS).replace('▲ 收起擬答架構', '▲ 收起擬答')
    T = "const open=ans.classList.toggle('open');"
    if 'bxvCfLoad(ans)' not in s:
        assert s.count(T) == 1, f; s = s.replace(T, T + "if(open)bxvCfLoad(ans);")
    s = s.replace('</head>', HELP + '\n</head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print(f, '嵌入', s.count('<!--bxv-cf-->'), '題；原擬答備查', s.count('<details class="oldans">'), '份')

for f, ids in LS.items():
    p = os.path.join(D, f); s = strip(open(p, encoding='utf-8').read())
    pos = cards(s); assert len(pos) == len(ids), (f, len(pos))
    for k in range(len(ids) - 1, -1, -1):
        a = pos[k]; e = match_end(s, a, 'div'); c = s[a:e]
        q = match_end(c, c.find('<div class="essay-q">'), 'div')
        emb = ('<!--bxv-cf--><details class="cfd"><summary>✍️ 本站擬答（與申論範文頁同一張卡：%s）</summary>' % TABS
               + frame(ids[k]).replace('<!--bxv-cf-->', '').replace('<!--/bxv-cf-->', '') + '</details><!--/bxv-cf-->')
        c = c[:q] + '\n    ' + emb + c[q:]
        if '<details class="oldans">' not in c:
            i = c.find('<details style="margin-top:8px">\n      <summary>✍️ 本站擬答'); assert i > 0, f
            j = match_end(c, i, 'details')
            if c[j:].lstrip().startswith('<details style="margin-top:8px">\n      <summary>🔧 本站補充'):
                j = match_end(c, c.find('<details', j), 'details')
            c = c[:i] + '<details class="oldans"><summary>本卷原附本站擬答與補充（備查；現行版本見上方申論卡）</summary>' + c[i:j] + '</details>' + c[j:]
        s = s[:a] + c + s[e:]
    s = s.replace('</head>', HELP + '\n</head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    print(f, '嵌入', s.count('<!--bxv-cf-->'), '題；老師版', s.count('老師版擬答（來勝解答，照抄）'), '份；舊擬答備查', s.count('<details class="oldans">'), '份')
