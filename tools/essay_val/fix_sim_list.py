# -*- coding: utf-8 -*-
"""11-09 使用者：「模擬卷為什麼不放上面分類，理由是什麼」——頁尾「模擬卷裡的申論題」是 v705 收編前的舊說明
（寫「不算進上面的題數」），實際上 12 題早已在上面各類：本站綜合卷 7 題＝mk-c*、另 3 題與預測卡同題（pred-10、pred-2、pred-4）、
補習班 2 題＝mk-ls1／mk-ls2。改為「在哪一類」對照：每題連到上面那張卡（#卡號，自動展開類別）＋卷頁試題。可重跑。"""
import os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '不動產估價概要_申論題實戰範文.html')
s = open(P, encoding='utf-8').read()
CN = '一二三四五'
M = [('綜合模擬卷一', 1, 'mk-c1-1'), ('綜合模擬卷一', 2, 'mk-c1-2'), ('綜合模擬卷二', 1, 'mk-c2-1'), ('綜合模擬卷二', 2, 'pred-10'),
     ('綜合模擬卷三', 1, 'mk-c3-1'), ('綜合模擬卷三', 2, 'pred-2'), ('綜合模擬卷四', 1, 'mk-c4-1'), ('綜合模擬卷四', 2, 'mk-c4-2'),
     ('綜合模擬卷五', 1, 'mk-c5-1'), ('綜合模擬卷五', 2, 'pred-4'), ('來勝115（一）', 1, 'mk-ls1'), ('來勝115（一）', 2, 'mk-ls2')]
PAGE = {'綜合模擬卷%s' % c: '估價_綜合模擬卷%s.html' % c for c in CN}; PAGE['來勝115（一）'] = '估價_來勝模擬試題一.html'
gs = [(m.start(), m.group(1)) for m in re.finditer(r'<details class="tgroup"[^>]*data-g="([^"]+)"', s)]
def where(cid):
    i = s.find('id="%s"' % cid); assert i > 0, cid
    g = [x for x in gs if x[0] < i][-1][0]
    gt = re.search(r'class="g-title">(.*?)</div>', s[g:g + 600]).group(1)
    t = re.search(r'class="card-title">(.*?)</div>', s[i:i + 4000], re.S).group(1)
    t = re.sub(r'<[^>]+>', '', re.sub(r'^【[^】]*】', '', t.strip()))
    return gt, t
li = []
for paper, k, cid in M:
    gt, t = where(cid)
    note = '（與預測題同題，收在預測卡）' if cid.startswith('pred') else ''
    li.append('<li><span class="sm-s">%s・申論%s</span><span class="sm-t">%s<span class="sm-g">→ %s%s</span></span>'
              '<span class="sm-a"><a href="#%s">看卡 ▸</a><a href="%s">試題 ↗</a></span></li>' % (paper, CN[k - 1], t, gt, note, cid, PAGE[paper]))
SEC = ('<section class="sim-list" id="sim">\n  <h2>📝 模擬卷申論在哪一類</h2>\n'
       '  <p class="sim-n">本站綜合模擬卷 10 題、補習班卷 2 題<b>都已收進上面各類</b>（虛線框卡片，算在各類題數裡）；其中 3 題與預測題同題，就收在那張預測卡。點「看卡」直接跳到上面那張卡。</p>\n'
       '  <details class="sim-d"><summary>展開 12 題對照 ▸</summary><ul class="sim-ul">' + ''.join(li) + '</ul></details>\n</section>')
s = re.sub(r'<section class="sim-list" id="sim">.*?</section>', lambda m: SEC, s, flags=re.S)
CSS = '<style id="sim2-css">.sm-g{display:block;font-size:.78rem;color:var(--muted)}.sm-a{display:flex;gap:10px;white-space:nowrap}.sim-d>summary{cursor:pointer;color:var(--primary);font-size:.88rem;font-weight:700;margin-top:6px}</style>'
s = re.sub(r'<style id="sim2-css">.*?</style>\n?', '', s, flags=re.S); s = s.replace('</head>', CSS + '\n</head>', 1)
open(P, 'w', encoding='utf-8').write(s); print('ok', len(li))
