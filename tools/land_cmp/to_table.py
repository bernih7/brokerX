# -*- coding: utf-8 -*-
"""《土地法_稅制與取得方式比較表》：把「每個項目一個摺疊框＋每欄一張小卡（重複法條名）」改成一張比較表：
欄＝比較對象（表頭只寫一次）、列＝比較項目。手機（≤640px）改成逐項堆疊，每格前面標小字欄名。內容一字不改。可重跑（已轉過就跳過）。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
f = os.path.join(R, '土地法_稅制與取得方式比較表.html'); s = open(f, encoding='utf-8').read()
CELL = re.compile(r'<div class="cell" style="--a:(var\(--c\d\))"><div class="ch">(.*?)</div><div class="cb">(.*?)</div></div>(?=<div class="cell"|</div></details>)', re.S)
def conv(m):
    wid, body = m.group(1), m.group(2)
    rows = re.findall(r'<details class="gd"[^>]*><summary><span class="gt">(.*?)</span>.*?</summary><div class="cg">(.*?)</div></details>', body, re.S)
    assert rows, wid
    heads = None; trs = []
    for gt, cg in rows:
        cells = CELL.findall(cg + '</div></details>')
        h = [(a, ch) for a, ch, _ in cells]
        if heads is None: heads = h
        assert [x[1] for x in h] == [x[1] for x in heads], (wid, gt)
        trs.append('<tr><th class="rh" scope="row">%s</th>%s</tr>' % (gt, ''.join('<td class="cell" style="--a:%s" data-l="%s"><div class="cb">%s</div></td>' % (a, re.sub(r'<[^>]+>', '', ch), cb) for a, ch, cb in cells)))
    th = ''.join('<th scope="col" style="--a:%s">%s</th>' % (a, ch) for a, ch in heads)
    return '<div class="tw" id="%s"><table class="cmp n%d"><thead><tr><th class="rh">比較項目</th>%s</tr></thead><tbody>%s</tbody></table></div>' % (wid, len(heads), th, ''.join(trs))
n = 0
def rep(m):
    global n; n += 1; return conv(m)
s2 = re.sub(r'<div class="gdwrap" id="(\w+)">(.*?)</details></div>(?=</section>|<)', lambda m: rep(m) if True else m.group(0), s, flags=re.S)
CSS = '''<style id="cmp-css">
.tw{overflow-x:auto;margin:12px 0 4px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
table.cmp{border-collapse:collapse;width:100%;font-size:14px;line-height:1.7}
table.cmp.n5{min-width:860px}table.cmp.n4{min-width:720px}
table.cmp th,table.cmp td{padding:10px 12px;vertical-align:top;text-align:left;border-bottom:1px solid var(--line)}
table.cmp tbody tr:last-child>*{border-bottom:0}
table.cmp thead th{font-family:"Noto Serif TC",serif;font-size:14.5px;font-weight:700;color:var(--a,var(--muted));border-bottom:2px solid var(--a,var(--line));background:color-mix(in srgb,var(--a,var(--line)) 7%,var(--card));white-space:nowrap}
table.cmp th.rh{width:7.5em;font-family:"Noto Serif TC",serif;font-weight:700;color:var(--ink,inherit);background:color-mix(in srgb,var(--line) 35%,var(--card));position:sticky;left:0;z-index:1}
table.cmp thead th.rh{color:var(--muted);font-size:12.5px}
table.cmp td{border-left:1px solid color-mix(in srgb,var(--line) 60%,transparent)}
table.cmp td.cell{background:none;border-top:0;border-right:0;border-radius:0;padding:10px 12px;font-size:14px}
table.cmp td b{color:var(--a)}
table.cmp tbody tr:hover td{background:color-mix(in srgb,var(--line) 18%,transparent)}
#allBtn{display:none}
@media (max-width:640px){
 .tw{border:0;background:none;overflow:visible}
 table.cmp,table.cmp tbody,table.cmp tr,table.cmp th,table.cmp td{display:block;min-width:0!important;width:auto}
 table.cmp thead{display:none}
 table.cmp tr{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:0 0 10px;overflow:hidden}
 table.cmp th.rh{position:static;width:auto;padding:8px 12px;border-bottom:1px solid var(--line)}
 table.cmp td{border-left:0;padding:8px 12px}
 table.cmp td::before{content:attr(data-l);display:block;font-family:"Noto Serif TC",serif;font-weight:700;font-size:12.5px;color:var(--a)}
 table.cmp tbody tr:hover td{background:none}
}
</style>'''
if n and 'id="cmp-css"' not in s2: s2 = s2.replace('</head>', CSS + '</head>', 1)
open(f, 'w', encoding='utf-8').write(s2); print('converted', n)
