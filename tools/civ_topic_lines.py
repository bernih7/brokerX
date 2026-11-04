# -*- coding: utf-8 -*-
"""民法五個專區頁線條減量（11-04 使用者截圖《抵押權總整理》：「線條太多不好看」）：
拿掉 details.sec／.intro／.tr／.rc tr 的左側色條、.rc td 的虛線分隔；條號 .ar 改灰色一般字（設計規範）。
流程圖 ol.flow 的細灰連接線保留。可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PAGES = ['民法_抵押權總整理.html', '民法_共有專區.html', '民法_繼承專區.html', '民法_物權變動與登記.html', '民法_債之發生與移轉.html']
SEL = re.compile(r'(details\.sec|\.intro|\.tr|\.rc tr|\.rc td)\{([^}]*)\}')
def fix(m):
    sel, body = m.group(1), m.group(2)
    body = re.sub(r'border-left:[^;}]*;?', '', body)
    if sel == '.rc td': body = body.replace('border-bottom:1px dashed var(--rule)', 'border-bottom:0')
    return sel + '{' + body.rstrip(';') + '}'
for fn in PAGES:
    p = os.path.join(R, fn); s = open(p, encoding='utf-8').read(); n = SEL.sub(fix, s)
    n = re.sub(r'\.ar\{font-weight:700;color:var\(--brown\);', '.ar{font-weight:400;color:var(--ink-soft);', n)
    if n != s: open(p, 'w', encoding='utf-8').write(n); print('ok', fn, s.count('border-left') - n.count('border-left'), s.count('dashed') - n.count('dashed'))
