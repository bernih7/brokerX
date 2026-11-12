# -*- coding: utf-8 -*-
"""11-12 經紀法規申論 75 張重審：套用審稿修正（我逐項核過、排除者列在 SKIP）。
v0＝指揮中心完整四段式（直接改 HTML，容許引文中夾 <b> 等標籤）；v4＝exam_ver/ev_*.json（之後跑 build_ev.py）。
同一句若也出現在考場速寫、essays.json、mock2.json，一併替換（逐字相符才換）。
evidence 內「」引文須逐字見於 lawfull.json 對應條文，否則不套用、列出人工看。"""
import os, re, json, glob, sys, html
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
REV = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-claude/db4af835-7730-5160-a7cd-81cabbdf283a/scratchpad/jjrev'
LAW = json.load(open(os.path.join(R, 'tools/essay_jj/law/lawfull.json'), encoding='utf-8'))
SKIP = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skip.json'), encoding='utf-8'))) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skip.json')) else set()
OVR = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'override.json'), encoding='utf-8')) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'override.json')) else {}
items = []
for f in sorted(glob.glob(os.path.join(REV, 'out*.json'))):
    b = re.search(r'out(\d+)', f).group(1)
    for i, x in enumerate(json.load(open(f, encoding='utf-8'))):
        x['_k'] = '%s-%d' % (b, i); items.append(x)

def ev_ok(x):
    ev = x.get('evidence', '') or ''
    for seg in re.split(r'；(?=[^「]*?§)', ev):
        m = re.match(r'\s*(.+? §[^：:「]+?)\s*[：:]\s*「(.+?)」', seg)
        if not m: continue
        key, q = re.sub(r'(第[0-9一二三四五六七八九十]+[項款]|[①-⑳]|[一二三四五六七八九十]+$|（[一二三四五六七八九十]+）)+$', '', m.group(1).strip()).strip(), m.group(2)
        key = re.split(r'、', key)[0]
        txt = re.sub(r'\s', '', (LAW.get(key) or {}).get('text', ''))
        if not txt: return 'nokey:' + key
        for part in re.split(r'…|\.\.\.', q):
            p = re.sub(r'\s', '', part)
            if p and p not in txt: return 'mismatch:' + key + ':' + part[:30]
    return ''

def fuzzy(q):
    q = re.sub(r'^[一二三四]、(意義|法條|涵攝|結論)', '', q.strip())
    lab = ''
    for L in ('意義', '理由', '例'):
        if q.startswith(L) and not q.startswith(L + '如'):
            lab = L; break
    body = q[len(lab):] if lab else q
    parts = [re.escape(ch) for ch in body]
    rx = r'(?:<[^>]+>|\s)*'.join(parts)
    pre = {'理由': r'理由(?:在於)?', '例': r'例[：:]?', '意義': r''}.get(lab, '')
    return re.compile(pre + r'(?:<[^>]+>|\s)*' + rx if lab else rx), lab

H = os.path.join(R, '經紀法規_備考指揮中心.html'); hub = open(H, encoding='utf-8').read()
EVF = {}
for f in glob.glob(os.path.join(R, 'tools/essay_jj/exam_ver/ev_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for k in d: EVF[k] = f
EVD = {f: json.load(open(f, encoding='utf-8')) for f in set(EVF.values())}
side = {p: open(os.path.join(R, p), encoding='utf-8').read() for p in ['tools/essay_jj/essays.json', 'tools/essay_jj/mock2/mock2.json', 'tools/essay_jj/lj_data.json']}

def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()
    return len(s)

def keep_tags(matched):
    st, orphan = [], []
    for t in re.findall(r'<[^>]+>', matched):
        if t.startswith('</'):
            nm = t[2:-1].split()[0]
            if st and st[-1][0] == nm: st.pop()
            else: orphan.append(t)
        elif not t.endswith('/>') and not t.lower().startswith('<br'):
            st.append((re.match(r'<(\w+)', t).group(1), t))
    return ''.join(orphan), ''.join(o for _, o in st)

def seg(cid):
    i = hub.find('<details id="%s"' % cid); j = hub.find('<details id="es-', i + 10); return i, (j if j > 0 else len(hub))

done, fail, bad_ev, skipped = [], [], [], []
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
for x in items:
    if ONLY is not None and x['_k'] not in ONLY: continue
    if x['_k'] in SKIP or x.get('severity') == '未核實': skipped.append(x['_k']); continue
    fix = x.get('fix', '').strip() or '（刪除）'
    m_alt = re.match(r'^（刪除，或改為：(.+)）$', fix)
    if m_alt: fix = m_alt.group(1)
    elif fix.startswith('（刪除，'): fix = '（刪除）'
    if x['_k'] in OVR: fix = OVR[x['_k']]
    fix = re.sub(r'^[一二三四]、(意義|法條|涵攝|結論)', '', fix)
    e = ev_ok(x)
    if e: bad_ev.append((x['_k'], x['id'], e)); continue
    delete = fix in ('（刪除）', '刪除', '(刪除)')
    q = x['quote']; rx, lab = fuzzy(q)
    new = '' if delete else (fix[len(lab):] if lab and fix.startswith(lab) else fix)
    where = x.get('where', '')
    ok = False
    if where.startswith('v4'):
        f = EVF.get(x['id'])
        rows = EVD[f][x['id']] if f else []
        for r in rows:
            m = rx.search(r[1])
            if m:
                rep = (m.group(0)[:m.group(0).find(new[:0]) or 0] if False else '')
                keep = re.match(r'(理由在於|理由|例：|例)', m.group(0)) if lab else None
                r[1] = r[1][:m.start()] + ((keep.group(0) if keep and not delete else '') + new) + r[1][m.end():]
                ok = True; break
    else:
        i, j = seg(x['id']); s = hub[i:j]
        a = s.find('<div class="vp" data-v="0"'); b2 = div_end(s, a)
        m = rx.search(s, a, b2)
        if m:
            pre, post = keep_tags(m.group(0))
            s = s[:m.start()] + pre + new + post + s[m.end():]; hub = hub[:i] + s + hub[j:]; ok = True
    if ok:
        done.append((x['_k'], x['id'], where))
        # 速寫與資料源同句
        i, j = seg(x['id']); s = hub[i:j]
        if q in s and not delete: hub = hub[:i] + s.replace(q, new) + hub[j:]
        for p in side:
            if q in side[p]: side[p] = side[p].replace(q, new)
    else:
        fail.append((x['_k'], x['id'], where, q[:50]))
open(H, 'w', encoding='utf-8').write(hub)
for f, d in EVD.items():
    out = '{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': [\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in v) + '\n]' for k, v in d.items()) + '\n}\n'
    open(f, 'w', encoding='utf-8').write(out)
for p, s in side.items(): open(os.path.join(R, p), 'w', encoding='utf-8').write(s)
print('套用', len(done), '找不到原句', len(fail), '依據不符', len(bad_ev), '略過', len(skipped))
json.dump({'done': done, 'fail': fail, 'bad_ev': bad_ev, 'skipped': skipped}, open(os.path.join(REV, 'apply_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
