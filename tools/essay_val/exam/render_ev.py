# -*- coding: utf-8 -*-
"""估價考場版排版（施工單《申論統一》第三節＋第八節 v702 定案）：
- 涵攝每一點：「（一）小標」獨立一行粗體 → 本文 → 「例」「理由」各自一行、前加灰色小膠囊
- 同一行兩個以上 ①②③：每項一行（懸掛縮排）；只在句讀「　，；：、。（→」之後切，不在 <b>/<sup>/<mark> 內切，款號（§4⑤）不切
- 法條塊一條一行；只有條號沒有說明時補本卡邏輯拆解（lawh）的名稱；條號灰色一般字
內容一字不改，只加標記。"""
import re, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from sprint_sx_law import titles as _titles
LJD = {x['k']: x for x in json.load(open(os.path.join(H, '..', 'lj_data.json'), encoding='utf-8'))}
ART = re.compile(r'(§\s*\d+(?:之\d+|-\d+)?(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)?(?:[①-⑳]+)?|第\s*\d+\s*條(?:之\d+)?(?:第\s*\d+\s*[項款])*)')
PT = re.compile(r'^（[一二三四五六七八九十]+）')
PUN = set('　，；：、。（→ ')
def _outside(t, f):
    """只對標籤外的文字套 f"""
    return ''.join(p if p.startswith('<') else f(p) for p in re.split(r'(<[^>]+>)', t))
def art(t): return _outside(t, lambda x: ART.sub(lambda m: '<span class="art">%s</span>' % m.group(1), x))
def lst(t):
    """同一行兩個以上 ①②：在合格位置前切行"""
    if len(re.findall('[①-⑳]', re.sub(r'<[^>]+>', '', t))) < 2: return t
    cuts = []; depth = 0; i = 0; prev = ''
    for m in re.finditer(r'<[^>]+>|.', t, re.S):
        tok = m.group(0)
        if tok.startswith('<') and len(tok) > 1:
            if re.match(r'<(b|sup|mark|strong)\b', tok): depth += 1
            elif re.match(r'</(b|sup|mark|strong)>', tok): depth -= 1
            continue
        if re.match('[①-⑳]', tok) and depth == 0 and (prev == '' or prev in PUN) and not re.search(r'§\s*\d+[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]*$', re.sub(r'<[^>]+>', '', t[:m.start()])):
            cuts.append(m.start())
        prev = tok
    if len(cuts) < 2: return t
    parts = [t[:cuts[0]]] + [t[a:b] for a, b in zip(cuts, cuts[1:] + [len(t)])]
    head = parts[0]
    return head + ''.join('<span class="evli">%s</span>' % p for p in parts[1:] if p.strip())
def fmt(t): return art(lst(t.strip()))
def _split_ex(line):
    """一行拆成 本文／例／理由"""
    m = re.search(r'(?:(?<=[。；」）])\s*|^)例：', line); r = re.search(r'(?:(?<=[。；」）])\s*|^)理由在於', line)
    cut = [x for x in (m, r) if x]
    main = line[:min(x.start() for x in cut)] if cut else line
    ex = why = ''
    if m: ex = line[m.end():(r.start() if r and r.start() > m.start() else len(line))]
    if r: why = line[r.end():(m.start() if m and m.start() > r.start() else len(line))]
    return main, ex, why
def _line(line):
    main, ex, why = _split_ex(line)
    o = '<p>%s</p>' % fmt(main) if main.strip() else ''
    if ex.strip(): o += '<p class="evx"><span class="evt">例</span><span>%s</span></p>' % fmt(ex)
    if why.strip(): o += '<p class="evx"><span class="evt">理由</span><span>理由在於%s</span></p>' % fmt(why)
    return o
def subsume(text):
    lines = [x for x in re.split(r'<br\s*/?>', text) if x.strip()]
    out = []; cur = None
    for ln in lines:
        s = ln.strip(); hm = PT.match(re.sub(r'^<b>', '', s))
        if hm:
            if cur is not None: out.append(cur + '</div>')
            plain = s
            # 小標：（一）＋到第一個「：」為止（≤22 字），否則（一）＋整個短句
            body = plain[len(hm.group(0)):] if plain.startswith(hm.group(0)) else plain
            c = body.find('：')
            if 0 < c <= 22 and '<' not in body[:c]: h, rest = hm.group(0) + body[:c], body[c + 1:]
            elif len(re.sub(r'<[^>]+>', '', body)) <= 26: h, rest = hm.group(0) + body, ''
            else: h, rest = hm.group(0), body
            cur = '<div class="evp"><p class="evh">%s</p>%s' % (art(h), _line(rest) if rest.strip() else '')
        else:
            if cur is None: out.append(_line(s))
            else: cur += _line(s)
    if cur is not None: out.append(cur + '</div>')
    return ''.join(out)
TOKS = re.compile(r'(§\s*\d+(?:之\d+|-\d+)?(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)?)')
def law_block(cid, text):
    M = _titles([st for sb in LJD.get(cid, {}).get('subs', []) for st in sb['steps']])
    rows = []
    for ln in re.split(r'<br\s*/?>', text):
        ln = ln.strip()
        if not ln: continue
        # 同一行擠兩條以上「§N：…。§M：…」→ 拆開
        for seg in re.split(r'(?<=[。；])\s*(?=§\s*\d)', ln):
            seg = seg.strip()
            if not seg: continue
            plain = re.sub(r'<[^>]+>', '', seg)
            if re.fullmatch(r'[\s§\dⅠ-Ⅹ①-⑳之\-、，。]+', plain):  # 只有條號
                toks = TOKS.findall(plain)
                for t in toks:
                    nm = M.get(t.replace(' ', '')) or (M.get('#' + re.match(r'§\s*(\d+(?:之\d+|-\d+)?)', t).group(1).replace('之', '-')) or [None])[0]
                    rows.append(art(t) + ('<span class="lawn">（%s）</span>' % nm if nm else ''))
            else:
                rows.append(fmt(seg))
    if len(rows) < 2: return '<p>%s</p>' % (rows[0] if rows else fmt(text))
    return '<p>' + ''.join('<span class="evli">%s</span>' % r for r in rows) + '</p>'
def body(h, t, cid):
    if h.startswith('二'): return law_block(cid, t)
    if h.startswith('三'): return subsume(t)
    return ''.join('<p>%s</p>' % fmt(x) for x in re.split(r'<br\s*/?>', t) if x.strip())
CSS = ('.exam-ver .evb p{margin:4px 0 0;line-height:1.85;max-width:44em}.exam-ver .evb>p:first-of-type{margin-top:0}'
       '.exam-ver .art{color:var(--evsub);font-weight:400}.exam-ver .evp{margin-top:12px}.exam-ver .evp:first-of-type{margin-top:4px}'
       '.exam-ver .evp .evh{font-weight:700;margin-top:0}.exam-ver .evx{display:flex;gap:8px;align-items:baseline}'
       '.exam-ver .lawn{color:var(--evink);font-weight:500;margin-left:2px}'
       '.exam-ver .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}'
       '.exam-ver .evt{flex:none;font-size:.74em;line-height:1.6;padding:0 7px;border-radius:999px;background:color-mix(in srgb,var(--evink) 9%,transparent);color:var(--evsub);font-weight:600}')
