# -*- coding: utf-8 -*-
"""考題小卡（精選 4 頁）＋完整考題小卡（4 頁）答案依刷題 A～E 篇（QS，唯一來源）對齊：
- 多重給分／一律給分題加 ok 欄（可接受答案清單），頁面判分改 okOf(c)；單一答案題 correct 以刷題為準。
- 考題小卡題號標錯 3 題改正：D 101-26→102-26（古董花瓶）、E 103-34→104-34（教堂結婚）、E 105-19→106-19（結婚）。
可重跑。"""
import re, json, os
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
def span(s, start):
    i = s.index('[', start); d = 0; ins = False; esc = False
    for j in range(i, len(s)):
        c = s[j]
        if ins:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': ins = False
            continue
        if c == '"': ins = True
        elif c == '[': d += 1
        elif c == ']':
            d -= 1
            if d == 0: return i, j + 1
L = 'ABCD'; M = {}
for p in 'ABCDE':
    s = open(os.path.join(R, '民法刷題練習_%s篇.html' % p), encoding='utf-8').read(); a, b = span(s, s.index('const QS='))
    for q in json.loads(s[a:b]):
        acc = sorted(set((q['ans'] + (q.get('acc') or '')).replace(',', '').replace('、', '')))
        M[(q['year'], q['num'])] = [L.index(x) for x in acc] or [0, 1, 2, 3]   # 空＝一律給分
JS_HELP = 'function okOf(c){return c.ok||[c.correct]}\n'
n = 0
for f in ['民法A_完整考題小卡', '民法BC_完整考題小卡', '民法D_完整考題小卡', '民法E_完整考題小卡', '民法A_考題小卡', '民法BC_考題小卡', '民法D_考題小卡', '民法E_考題小卡']:
    fn = os.path.join(R, f + '.html'); s = open(fn, encoding='utf-8').read(); a, b = span(s, s.index('[{"id"'))
    C = json.loads(s[a:b]); assert json.dumps(C, ensure_ascii=False) == s[a:b]
    for c in C:
        for pg, wrong, right, kw in [('民法D_考題小卡', '101年第26題', '102年第26題', '古董花瓶'),
                                     ('民法E_考題小卡', '103年第34題', '104年第34題', '教堂'),
                                     ('民法E_考題小卡', '105年第19題', '106年第19題', '結婚')]:
            if f == pg and c['year'] == wrong and kw in c['q']: c['year'] = right; n += 1
        y, k = map(int, re.match(r'(\d+)年第(\d+)題', c['year']).groups()); ok = M[(y, k)]
        if len(ok) == 1:
            if c['correct'] != ok[0]: c['correct'] = ok[0]; n += 1
            if 'ok' in c: del c['ok']; n += 1
        else:
            if c.get('ok') != ok: c['ok'] = ok; n += 1
            if c['correct'] not in ok: c['correct'] = ok[0]; n += 1
    s = s[:a] + json.dumps(C, ensure_ascii=False) + s[b:]
    if 'function okOf(' not in s:
        if 'function selectOption(' in s: s = s.replace('function selectOption(', JS_HELP + 'function selectOption(', 1)
        else: s = s.replace('function pick(', JS_HELP + 'function pick(', 1)
        s = re.sub(r'\(i\s*===\s*c\.correct\)', '(okOf(c).includes(i))', s)
        s = s.replace('letters[c.correct]', "okOf(c).map(x=>letters[x]).join('、')").replace('L[c.correct]', "okOf(c).map(x=>L[x]).join('、')")
        s = re.sub(r'j\s*===\s*c\.correct', 'okOf(c).includes(j)', s)
    assert 'function okOf(' in s and s.count('[c.correct]') == 1, f
    open(fn, 'w', encoding='utf-8').write(s)
print('改動', n)
