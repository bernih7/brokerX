# -*- coding: utf-8 -*-
"""刷題頁拿掉左側色條（11-04 使用者截圖民法 C 篇：「刷題旁太多線條」）。
對象：民法／經紀法規／估價刷題頁、bx-quiz.css（土地法刷題共用）。只刪 border-left 宣告，其餘樣式不動。可重跑。"""
import os, re, glob
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SEL = re.compile(r'(\.yr-header|\.res|\.opt\.(?:correct|wrong) \.nt|\.qcard\.answered[\w.-]*|\.note-box)\{([^}]*)\}')
def fix(m):
    body = re.sub(r'border-left:[^;}]*;?', '', m.group(2))
    if m.group(1) == '.yr-header': body = re.sub(r'padding-left:\d+px;?', '', body)
    return m.group(1) + '{' + body.rstrip(';') + '}'
files = sorted(glob.glob(os.path.join(R, '民法刷題練習_*.html')) + glob.glob(os.path.join(R, '經紀法規刷題練習_*.html')) + glob.glob(os.path.join(R, '估價刷題練習_*.html')) + [os.path.join(R, 'bx-quiz.css')])
for p in files:
    s = open(p, encoding='utf-8').read(); n = SEL.sub(fix, s)
    if n != s: open(p, 'w', encoding='utf-8').write(n); print('ok', os.path.basename(p), len(re.findall('border-left', s)) - len(re.findall('border-left', n)))
