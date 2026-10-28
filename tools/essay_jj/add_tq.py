# -*- coding: utf-8 -*-
"""把「可作答的考古題面板」(bxj-topic-q.js) 插進經紀法規各整理頁。

題號對應關係是現成的——頁面上每一節旁邊就寫著考過哪幾題，所以直接從該節的
**文字**抓題號，不用關鍵詞猜。可重複執行（先移除舊面板再重插）。

⚠️ 條號會被當成題號（估價 v552 的坑）。四道防線：
  ① 只看文字節點（先把標籤挖掉）② 年份限 99～119 ＋ 1～2 位題號
  ③ 前面是 § 、數字或「-」一律跳過 ④ 題庫裡找不到就不要
"""
import io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
BANK = {}
for x in json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))['q']:
    if x.get('sr') != 'mock':
        BANK[x['k']] = x

QPAT = re.compile(r'(?<![0-9§\-])((?:99|1[0-1][0-9]))-([0-9]{1,2})(?![0-9])')
MIN = 2            # 一節少於 2 題就不放面板

# 頁面 → (節容器 class 關鍵字, 節 id 樣式)
# (檔名, 節容器 class, 節 id 樣式, gr→節id 規則, 不放「本頁全部」)
PAGES = [
    ('經紀法規_應記載不得記載總整理.html', 'sc',  r'^s\d+$',      None,            False),
    ('經紀法規_公平法消保法罰則整理.html', 'sc',  r'^s\d+$',      None,            False),
    ('經紀法規_罰則總整理.html',           'sc',  r'^s\d+$',      None,            False),
    # 這兩頁自己有一套考古題（但**不寫 bxj-q2**），所以只在各步驟補可計分的面板，
    # 不另加「本頁全部」，避免和頁尾那一區重複。
    ('經紀法規_程序總整理.html',           'sec', r'^p\d+$',      lambda g: g.replace('P', 'p'), True),
    ('經紀法規_定型化契約專區.html',       'sec', r'^d\d+$',      None,            True),
    ('經紀法規_公寓大廈條例罰則整理.html', 'sec', r'^p\d+$',      None,            False),
    ('經紀法規_定型化契約_無效vs不構成.html', 'sc', r'^t\d+$',    None,            False),
]


def close_of(s, i):
    """從 <details …> 的起點往後找配對的 </details>（巢狀要算）。"""
    d, k = 0, i
    while True:
        a, b = s.find('<details', k), s.find('</details>', k)
        if b < 0:
            raise SystemExit('找不到 </details>')
        if 0 <= a < b:
            d += 1; k = a + 8
        else:
            if d == 0:
                return b
            d -= 1; k = b + 10


def title_of(seg):
    """取節標題：優先用 <h2>，並剔除編號 span、副標 <small>、題數膠囊。"""
    m = re.search(r'<summary[^>]*>(.*?)</summary>', seg, re.S)
    t = m.group(1) if m else seg[:400]
    for cls in ('n2', 'dat', 'tg2', 'ar', 'cnt'):
        t = re.sub(r'<span class="%s"[^>]*>.*?</span>' % cls, '', t, flags=re.S)
    t = re.sub(r'<small>.*?</small>', '', t, flags=re.S)
    h = re.search(r'<h[23][^>]*>(.*?)</h[23]>', t, re.S)
    if h:
        t = h.group(1)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'^[⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫]\s*', '', t)
    return (t[:24] or '本節').strip()


def qd_groups(s):
    """頁內自帶的 var QD=[…]（程序總整理、定型化契約專區）：依 gr 分組取題號。"""
    m = re.search(r'var QD=(\[.*?\]);', s, re.S)
    if not m:
        return {}
    try:
        arr = json.loads(m.group(1))
    except Exception:
        return {}
    g = {}
    for x in arr:
        if x.get('gr') and x.get('k') in BANK:
            g.setdefault(x['gr'], []).append(x['k'])
    return g


def qs_in(seg):
    txt = re.sub(r'<[^>]+>', ' ', seg)
    out, seen = [], set()
    for m in QPAT.finditer(txt):
        k = m.group(0)
        if k in BANK and k not in seen:
            seen.add(k); out.append(k)
    out.sort(key=lambda k: (-int(k.split('-')[0]), int(k.split('-')[1])))
    return out


def run(dry=False):
    tot = 0
    for fn, cls, idpat, grmap, noall in PAGES:
        p = os.path.join(ROOT, fn)
        s = io.open(p, encoding='utf-8').read()
        # 先移除舊面板與舊 script，確保可重複執行
        s = re.sub(r'<div class="bxj-tq"[^>]*></div>', '', s)
        s = s.replace('<script src="bxj-topic-q.js" defer></script>\n', '')
        GR = {}
        if grmap:
            for g, ks in qd_groups(s).items():
                GR[grmap(g)] = ks
        secs = []
        for m in re.finditer(r'<details([^>]*)>', s):
            at = m.group(1)
            c = (re.search(r'class="([^"]*)"', at) or [None, ''])[1]
            i = (re.search(r'id="([^"]*)"', at) or [None, ''])[1]
            if cls not in c.split() or not re.match(idpat, i):
                continue
            secs.append((m.start(), m.end(), i))
        rep, pageqs, pageseen = [], [], set()
        for st, sten, sid in secs:
            en = close_of(s, sten)
            seg = s[sten:en]
            qs = GR.get(sid) or qs_in(seg)
            for k in qs:
                if k not in pageseen:
                    pageseen.add(k); pageqs.append(k)
            if len(qs) < MIN:
                rep.append((sid, title_of(seg), 0, en, None))
                continue
            rep.append((sid, title_of(seg), len(qs), en, qs))
        # 「本頁全部」掛在標題含「考古題」的那一節，否則掛最後一節
        allsec = None
        if not noall:
            for r in rep:
                if '考古' in r[1]:
                    allsec = r[0]; break
            if allsec is None and rep:
                allsec = rep[0][0]
        print('── %s（%d 節／全頁 %d 題不重複）' % (fn, len(rep), len(pageqs)))
        ins = []
        for sid, ti, n, en, qs in rep:
            blks = []
            if qs:
                blks.append('<div class="bxj-tq" data-title="%s" data-qs="%s"></div>' % (ti, ','.join(qs)))
            if sid == allsec and len(pageqs) >= 12:
                blks.append('<div class="bxj-tq" data-title="本頁全部" data-qs="%s"></div>' % ','.join(pageqs))
            print('     %-5s %-24s %3d 題%s' % (sid, ti, n, '　＋本頁全部' if (sid == allsec and len(pageqs) >= 12) else ''))
            if blks:
                ins.append((en, ''.join(blks)))
        if dry:
            continue
        for en, blk in sorted(ins, reverse=True):
            at = en - 6 if s[en - 6:en] == '</div>' else en
            s = s[:at] + blk + s[at:]
        if '<script src="bxj-topic-q.js"' not in s:
            s = s.replace('</body>', '<script src="bxj-topic-q.js" defer></script>\n</body>')
        io.open(p, 'w', encoding='utf-8').write(s)
        tot += sum(1 for _, b in ins for _ in [0])
    print('完成，共寫入 %d 頁' % len(PAGES))


run('--dry' in sys.argv)
