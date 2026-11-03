# -*- coding: utf-8 -*-
"""5 分鐘推理版「③ 速寫骨架」法條塊：只有條號時，補上該條在本題的名稱（取自同一張卡邏輯拆解的條文標題 lawh），
並一條一行（使用者 11-03：「數字和定義放在一起比較好記」）。不新增內容：名稱只取本卡 lawh，找不到就不補。
民法 tools/essay_civ/sprint/build_sprint.py、經紀法規 tools/essay_jj/sprint/build_reason.py 共用。"""
import re
TOK = re.compile(r'(§\s*\d+(?:之\d+|-\d+)?(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)?(?:[①-⑳]+)?(?:前段|中段|後段|但書|本文)?)')
def base(t): return re.match(r'§\s*(\d+(?:之\d+|-\d+)?)', t).group(1).replace('之', '-')
def titles(steps):
    m = {}
    for st in steps:
        h = (st.get('lawh') or '').strip()
        mm = re.match(r'^(§\s*\d+(?:之\d+|-\d+)?\S*)\s+(.+)$', h)
        if not mm: continue
        tok, name = mm.group(1), re.sub(r'[（(].*?[）)]$', '', mm.group(2)).strip()
        name = re.sub(r'（已核對）|^[^｜]*｜', '', name); name = re.sub(r'^(本文|但書|前段|中段|後段)[\s、]*', '', name).strip()
        if len(name) < 3 or re.match(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ①-⑳（(]|[一二三四五六七八九十]款', name): continue
        if not name or re.search(r'§|第\s*\d+\s*條', name): continue
        m.setdefault(tok, name)
        b = m.setdefault('#' + base(tok), [])
        if name not in b: b.append(name)
    return m
def annotate(body, steps, extra=None):
    """body：法條塊 HTML（可能只有「§4、§22Ⅰ、§22Ⅱ。」）。回傳新 HTML 與補了幾條。"""
    M = titles(steps); n = 0; out = []
    X = {}  # 本卡 lawh 沒有名稱時的後備（民法 sx_law_names.json；經紀法規取 law.json 條文標題）
    for k, v in (extra or {}).items():
        if k not in M: M[k] = v
        if not re.search(r'[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ①-⑳]', k): X[base(k)] = v
    plain = re.sub(r'<[^>]+>', '', body)
    toks = TOK.findall(plain)
    if not toks: return body, 0
    # 每個條號後面若已有說明（緊接「（」或中文字），不補
    def rep(m):
        nonlocal n
        t = m.group(1); after = plain_after.get(m.start(), '')
        if after[:1] in ('（', '(') or re.match(r'[一-鿿]', after[:1] or ' '): return t
        name = M.get(t)
        if not name: name = X.get(base(t))
        if not name:
            b = M.get('#' + base(t)) or []
            name = '、'.join(b[:2]) if b else None
        if not name: return t
        name = name.replace('（已核對）', '').strip()
        n += 1; return '%s<span class="lawn">（%s）</span>' % (t, name)
    plain_after = {}
    for m in TOK.finditer(body): plain_after[m.start()] = re.sub(r'<[^>]+>', '', body[m.end():m.end() + 12]).lstrip(' ')
    nb = TOK.sub(rep, body)
    # 只有條號、頓號分隔的清單 → 一條一行
    core = re.sub(r'<span class="lawn">.*?</span>', '', re.sub(r'<(?!/?span)[^>]+>', '', nb))
    if len(toks) >= 2 and re.fullmatch(r'[\s§\dⅠ-Ⅹ①-⑳之\-、，；。前中後段但書本文]+', re.sub(r'</?span[^>]*>', '', core)):
        inner = re.sub(r'^<p>|</p>$', '', nb.strip())
        parts = []
        for p in re.split(r'[、，；](?![^<]*</span>)', inner):
            p = p.strip(' 。')
            if not p: continue
            if parts and not p.startswith('§'): parts[-1] += '、' + p  # 「§22Ⅰ、Ⅱ」的 Ⅱ 接回上一條
            else: parts.append(p)
        def tail(p):  # 名稱移到該行最後（「§10Ⅰ Ⅱ（名稱）」而不是「§10（名稱） Ⅰ Ⅱ」）
            ns = re.findall(r'<span class="lawn">.*?</span>', p)
            return re.sub(r'\s*<span class="lawn">.*?</span>', '', p).strip() + ''.join(ns[:1])
        parts = [tail(p) for p in parts]
        nb = '<p>' + ''.join('<span class="sxli">%s</span>' % p for p in parts) + '</p>'
    return nb, n
