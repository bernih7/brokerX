# -*- coding: utf-8 -*-
"""深淺色方案 A 的收尾兩件：

① 估價備考指揮中心.html 在 <html> 標籤裡寫死 data-theme="light"（不是 JS 寫的），拿掉。
② 民法_數字期間速查、民法_用詞分類與申論必背 的深色色票只寫在 [data-theme=dark]，
   沒有 @media (prefers-color-scheme:dark)，所以拿掉屬性後接不到深色。
   作法：把既有的 [data-theme=dark] 規則「原值鏡像」一份到 media query 內，
   選擇器改成 :root:not([data-theme=light])。不新增任何顏色值。

可重複執行（已加過的 <style id="sysdark-css"> 會先移除再重建）。
"""
import io, re, sys

def blk(s, start):
    k = s.find('{', start); d = 0; i = k
    while i < len(s):
        if s[i] == '{': d += 1
        elif s[i] == '}':
            d -= 1
            if d == 0: return k, i
        i += 1
    return k, len(s)

def fix_html_attr(p='估價備考指揮中心.html'):
    s = io.open(p, encoding='utf-8').read()
    new = re.sub(r'(<html[^>]*?)\s+data-theme\s*=\s*["\']light["\']', r'\1', s, count=1)
    if new == s:
        print('  %s：沒有寫死的 data-theme（可能已改過）' % p); return 0
    io.open(p, 'w', encoding='utf-8').write(new)
    print('  %s：已拿掉 <html> 的 data-theme="light"' % p); return 1

SEL = re.compile(r'(?:^|[\s,};])(\[data-theme\s*=\s*["\']?dark["\']?\][^{,}]*)\s*\{')

def mirror(p):
    s = io.open(p, encoding='utf-8').read()
    s = re.sub(r'<style id="sysdark-css">.*?</style>', '', s, flags=re.S)
    rules = []
    for m in SEL.finditer(s):
        sel = m.group(1).strip()
        a, b = blk(s, m.end() - 1)
        body = s[a + 1:b].strip()
        if not body: continue
        newsel = re.sub(r'^\[data-theme\s*=\s*["\']?dark["\']?\]',
                        ':root:not([data-theme=light])', sel)
        rules.append('%s{%s}' % (newsel, body))
    if not rules:
        print('  %s：找不到 [data-theme=dark] 規則' % p); return 0
    css = ('<style id="sysdark-css">/* 系統深色：鏡像既有 [data-theme=dark] 的值，未新增顏色 */\n'
           '@media (prefers-color-scheme:dark){\n' + '\n'.join(rules) + '\n}</style>')
    # 放在 </head> 之前，確保在原 <style> 之後（同權重時後者勝，但這裡選擇器更specific）
    i = s.lower().rfind('</head>')
    if i < 0:
        print('  %s：找不到 </head>' % p); return 0
    s = s[:i] + css + '\n' + s[i:]
    io.open(p, 'w', encoding='utf-8').write(s)
    print('  %s：鏡像 %d 條規則進 media query' % (p, len(rules))); return 1

if __name__ == '__main__':
    n = fix_html_attr()
    for p in ('民法_數字期間速查.html', '民法_用詞分類與申論必背.html'):
        n += mirror(p)
    print('共處理 %d 處' % n)
