import re, json, glob, html, sys, os
from collections import Counter, OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, 'data') + '/'
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'src.html')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', '..', '土地法_申論題分類總覽.html')
s = open(SRC, encoding='utf-8').read()

def block_at(j):
    depth = 0
    for m in re.finditer(r'<details|</details>', s[j:]):
        depth += 1 if m.group() == '<details' else -1
        if depth == 0:
            return s[j:j + m.end()]

def top_items(container_id):
    a = s.index(f'id="{container_id}"')
    # end of container: matching div
    st = s.index('>', a) + 1; depth = 1
    for mm in re.finditer(r'<div\b|</div>', s[st:]):
        depth += 1 if mm.group().startswith('<div') else -1
        if depth == 0:
            end = st + mm.start(); break
    res = []; i = st
    while True:
        k = s.find('<details class="it"', i, end)
        if k < 0: break
        b = block_at(k); res.append(b); i = k + len(b)
    return res

def inner(b, v):
    m = re.search(r'<div class="vp" data-v="%s"[^>]*>' % v, b)
    st = m.end(); depth = 1
    for mm in re.finditer(r'<div\b|</div>', b[st:]):
        depth += 1 if mm.group().startswith('<div') else -1
        if depth == 0:
            return b[st:st + mm.start()]

def parse(b):
    d = {}
    d['nm'] = re.search(r'<span class="nm">(.*?)</span>', b).group(1)
    ch = re.search(r'<span class="chips">(.*?)</span>', b)
    d['chips'] = re.findall(r'<i>(.*?)</i>', ch.group(1)) if ch else []
    d['oq'] = re.search(r'<p class="oq">(.*?)</p>', b, re.S).group(1)
    sm = re.search(r'<p class="src">(.*?)</p>', b, re.S)
    d['src'] = sm.group(1) if sm else ''
    v0 = inner(b, '0')
    fm = re.search(r'<details class="full"><summary>看完整範文</summary>(.*?)</details>', v0, re.S)
    full = fm.group(1)
    d['sec'] = re.findall(r'<h4>(.*?)</h4>(.*?)(?=<h4>|$)', full, re.S)
    why = re.search(r'<h4>為什麼列進來</h4>(<ul>.*?</ul>)', v0[:fm.start()], re.S)
    d['why'] = why.group(1) if why else ''
    after = v0[fm.end():]
    d['tail'] = after.strip()
    d['v1'] = inner(b, '1'); d['v2'] = inner(b, '2')
    return d

# ---------- data ----------
E = json.load(open(W + 'essays.json'))
M = {}
for f in sorted(glob.glob(W + 'M*_out.json')):
    for r in json.load(open(f)): M[r['key']] = r
LAW = {}
for f in sorted(glob.glob(W + 'F*_law.json')):
    LAW.update(json.load(open(f)))

# map blocks
offb = {}
for r in E:
    if r['kind'] == 'off':
        k = s.find(f'id="{r["idv"]}"'); offb[r['key']] = block_at(s.rfind('<details', 0, k))
predb = top_items('predlist'); topb = top_items('toplist')
def nm_of(b): return re.search(r'<span class="nm">(.*?)</span>', b).group(1)
pmap = {}
for r in E:
    if r['kind'] in ('pred', 'mock'):
        cand = [b for b in predb if html.unescape(re.sub('<[^>]+>', '', nm_of(b))).startswith(r['nm'][:20])]
        assert len(cand) == 1, (r['key'], len(cand))
        pmap[r['key']] = cand[0]
    if r['kind'] == 'topic':
        cand = [b for b in topb if html.unescape(re.sub('<[^>]+>', '', nm_of(b))).startswith(r['nm'][:15])]
        assert len(cand) == 1, (r['key'], len(cand))
        pmap[r['key']] = cand[0]

CAT = dict(P01='A', P02='E', P03='D', P04='D', P06='C', P07='E', P08='D', P09='D', P10='G', P11='B', P12='B', P13='G', P14='G', P15='G', P16='G', P17='G', P18='D', P19='D', P20='D', P21='G', P22='F', P23='D', P24='C', P25='C', P26='D', P27='F', P28='G', P29='E', P30='F', P31='A', P32='F', P33='G', X1='B', X2='B', X3='B', P34='A', K1='D', K2='B', K3='E', K4='F')
rows = []
for r in E:
    if r['key'] == 'P05': continue
    r = dict(r)
    if r['kind'] == 'off':
        r['b'] = offb[r['key']]; r['id'] = r['idv']
    else:
        r['b'] = pmap[r['key']]; r['cat'] = CAT[r['key']]
        r['id'] = r['idv'] or ('pr-%02d' % int(r['key'][1:]) if r['key'].startswith('P') else 'x-' + r['key'][1:])
    r['d'] = parse(r['b'])
    r['m'] = M[r['key']]
    rows.append(r)
assert len(set(r['id'] for r in rows)) == len(rows)

# group headers from old page
GH = {}
for m in re.finditer(r'<section class="cat" data-cat="(\w)" id="cat-\w"><div class="ch"><h3><span class="ck" data-g="\w">\w</span>(.*?)<small>.*?</small></h3><p class="rule">(.*?)</p><p class="how">(.*?)</p><p class="ys2">(.*?)</p>', s, re.S):
    GH[m.group(1)] = dict(name=m.group(2), rule=m.group(3), how=m.group(4), ys=m.group(5))
assert len(GH) == 7
SHORT = dict(A='都市計畫・公設保留地', B='土地徵收・區段徵收', C='市地重劃・空地・耕地', D='登記・優購・實價登錄', E='地價稅・土增稅', F='房屋稅・契稅・房地合一', G='地權總則・外國人・農地')
GSUB = dict(A='說明書解說、保留地使用限制', B='失效、要件、抵價地、撤銷廢止', C='重劃程序、空地稅、照價收買', D='預告登記、§34-1、實價登錄', E='稅基、納稅義務人、減免', F='課稅標的、房屋稅2.0', G='§14、外國人、農舍、國土')
ORDER = ['E', 'A', 'F', 'D', 'G', 'B', 'C']
TOT = dict(E=8, A=5, F=5, D=4, G=4, B=3, C=3)
R5 = dict(A=2, B=0, C=2, D=1, E=2, F=2, G=1)
P115 = dict(E='高', A='高', F='高', D='高', G='中', B='中', C='中')
for g in ORDER:
    n = sum(1 for r in rows if r['cat'] == g and r['kind'] == 'off')
    assert n == TOT[g], (g, n)
    y = [int(r['key'].split('-')[0]) for r in rows if r['cat'] == g and r['kind'] == 'off']
    assert sum(1 for v in y if v >= 110) == R5[g], (g, y)

# citations count
offc = Counter(); prec = Counter()
for r in rows:
    for a in r['m']['cite']:
        (offc if r['kind'] == 'off' else prec)[a] += 1

def stars(n): return '★★★' if n >= 3 else '★★' if n == 2 else '★' if n == 1 else ''
def cnt_txt(o, q):
    a = [f'歷屆申論考過 {o} 題' if o else '歷屆申論沒考過']
    if q: a.append(f'預測題用到 {q} 題')
    return '・'.join(a)

def law_body(a):
    L = LAW.get(a)
    if not L or not L.get('p'):
        return '<p class="lnil">⚠️ 條文全文尚未取得逐字原文，請對照紙本法條。</p>'
    out = ''
    for p in L['p']:
        parts = re.split(r'(?<=[：。；])(?=[一二三四五六七八九十]{1,3}、)', p)
        out += f'<p>{html.escape(parts[0])}</p>' + ''.join(f'<p class="k">{html.escape(x)}</p>' for x in parts[1:])
    note = L.get('note', '')
    if note: out += f'<p class="lnote">註：{html.escape(note)}</p>'
    return out

def law_title(a):
    L = LAW.get(a); return html.escape(L['t']) if L and L.get('t') else ''

def lawdet(a, who=None):
    n = offc[a]
    c = f'<div class="btc">本組用到：{"・".join(who)}</div>' if who else ''
    return (f'<details class="bt"><summary><b class="bn">{a}</b><span class="bti">{law_title(a)}</span>'
            f'<span class="bm">{stars(n)}<small>{cnt_txt(n, prec[a])}</small></span></summary><div class="btx">{c}{law_body(a)}</div></details>')

NUMS = '一二三四五六七八九十'
def split_ham(p):
    txt = p.strip()
    txt = re.sub(r'^<p>|</p>$', '', txt)
    paras = [x.strip() for x in re.split(r'</p>\s*<p>', txt)]
    if len(paras) > 1:
        if not any(re.match(r'（[一二三四五六七八九十]）', x) for x in paras): return p
        parts = ['']
        for x in paras:
            if re.match(r'（[一二三四五六七八九十]）', x): parts.append(x)
            elif len(parts) == 1: parts[0] += x
            else: parts[-1] += '<br>' + x
    else:
        parts = re.split(r'(?<![第依])(?=（[一二三四五六七八九十]）)', txt)
    if len(parts) == 1:
        segs = re.split(r'(?<=。)(?=就)', txt)
        if len(segs) > 1:
            parts = [''] + [f'（{NUMS[i]}）' + x for i, x in enumerate(segs)]
        else:
            return p
    out = ''
    lead = parts[0].strip()
    if lead: out += f'<p>{lead}</p>'
    for q in parts[1:]:
        m = re.match(r'（([一二三四五六七八九十])）(.*)', q, re.S)
        body = m.group(2).strip()
        plain = re.sub(r'<[^>]+>', '', body)
        fs = re.split(r'(?<=[。；])', plain, maxsplit=1)[0]
        head = re.match(r'([^：:。]{2,40}?)[：:]', plain) or re.match(r'就(.{2,16}?)(?:而言|部分)', plain)
        hd = head.group(1) if head else ''
        if head and fs.startswith(head.group(0)): fs = fs[len(head.group(0)):]
        fs = re.sub(r'^[，,]', '', fs)
        rest = plain[len(head.group(0)):] if head else plain
        if len(rest) <= 60:
            out += f'<div class="sub1"><b>（{m.group(1)}）{hd}</b>{"：" if hd else ""}{rest}</div>'
            continue
        if len(fs) > 46:
            cut = [i for i, ch in enumerate(fs) if ch in '，；、' and 14 <= i <= 46]
            fs = fs[:cut[-1]] + '…' if cut else fs[:44] + '…'
        out += (f'<details class="sub2"><summary><b>（{m.group(1)}）{hd}</b><span class="pt">{fs}</span>'
                f'<span class="more">看全文</span></summary><div class="full2"><p>{body}</p></div></details>')
    return out

LVL = {'A': ('必考', 'lA', 3), 'B': ('高機率', 'lB', 2), 'C': ('參考', 'lC', 1), '高': ('預測・高', 'pH', 3), '中': ('預測・中', 'pM', 2), '低': ('預測・低', 'pL', 1), '': ('自編專題', 'pM', 2), '模': ('模擬試題', 'pM', 2)}
TAGC = {'定義': 'm1', '法條': 'm2', '涵攝': 'm3', '結論': 'm4'}

def clean_tx(x): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', '', x))).lower()

def card(r):
    d = r['d']; m = r['m']; key = r['key']; kind = r['kind']
    cite = m['cite']
    secs = ''
    for i, (h, p) in enumerate(d['sec']):
        cls = 'b%d' % (min(i, 3) + 1)
        if i == 1:
            p += (f'<div class="btw"><div class="bth">這題要背的條文（{len(cite)} 條）<small>★＝歷屆官方申論考過幾題（★★★ 3 題以上、★★ 2 題、★ 1 題），點開看全文</small></div>'
                  + ''.join(lawdet(a) for a in cite) + '</div>')
        if i == 2: p = split_ham(p)
        secs += f'<details class="blk {cls}"{" open" if i == 0 else ""}><summary><h5>{h}</h5></summary><div class="fdb">{p}</div></details>'
    must = ''.join(f'<li class="{TAGC[t]}"><span class="mt">{t}</span><span>{html.escape(x)}</span></li>' for t, x in m['must'])
    lab, lc, pr = LVL[r['lv']]
    if kind == 'off':
        y, n = key.split('-'); ek = f'{y}年 第{n}題'
    elif kind == 'mock':
        ek = '補習班模擬卷'
    elif kind == 'pred':
        ek = '模擬題・網路來源' if d['src'] else '預測題・自擬'
    else:
        ek = '自擬・含解答'
    why = f'<div class="why"><b>為什麼列進來</b>{d["why"]}</div>' if d['why'] else ''
    tail = d['tail']
    tail = tail.replace('<p class="warn">', '<p class="note warn">')
    hasw = '⚠️' in (''.join(p for _, p in d['sec']) + tail)
    v1 = d['v1'].replace('速寫版由上方完整範文濃縮，未新增法條事實；⚠️待核處同完整版。', '速寫版由上方完整範文濃縮；⚠️待核處同完整版。' if hasw else '速寫版由上方完整範文濃縮。')
    tx = clean_tx(d['nm'] + ' '.join(d['chips']) + key + d['oq'] + ' '.join(cite) + ' '.join(x for _, x in m['must']))
    oq = d['oq']
    return (f'<details class="es{" pred" if kind != "off" else ""}" id="{r["id"]}" data-k="{"off" if kind == "off" else "pred"}"{" data-mk=\"1\"" if kind == "mock" else ""} data-pr="{pr}" data-lv="{r["lv"]}" data-tx="{html.escape(tx)}">'
            f'<summary><span class="eh"><span class="rk" aria-hidden="true">✓</span><b class="et">{d["nm"]}</b></span>'
            f'<span class="em"><span class="lvp {lc}">{lab}</span><span class="ek">{ek}</span></span>'
            f'<span class="chips">{"".join(f"<i>{c}</i>" for c in d["chips"][:5])}</span></summary>'
            f'<div class="ebody"><div class="oq">{oq}</div>{"<p class=srcl>" + d["src"] + "</p>" if d["src"] else ""}{why}'
            f'<div class="vtab" role="tablist"><button type="button" class="on" data-v="0">完整四段式</button><button type="button" data-v="1">考場速寫版</button><button type="button" data-v="2">得分關鍵・失分點</button><button type="button" data-v="3">必提重點</button></div>'
            f'<div class="vp" data-v="0">{secs}{tail}</div><div class="vp" data-v="1" hidden>{v1}</div><div class="vp" data-v="2" hidden>{d["v2"]}</div>'
            f'<div class="vp" data-v="3" hidden><p class="mh">一定要寫到的 {len(m["must"])} 個採分點（照答題順序，寫完逐項打勾自查）</p><ul class="must">{must}</ul>'
            f'<div class="mc"><b>結論必寫</b>{html.escape(m["mc"])}</div><div class="mtrap"><b>最容易漏</b>{html.escape(m["mt"])}</div></div>'
            f'<label class="done"><input type="checkbox" class="rd"> 我已讀懂這題的邏輯</label></div></details>')

def sortkey(r):
    if r['kind'] == 'off':
        return (0, 'ABC'.index(r['lv']), -int(r['key'].split('-')[0]), r['key'])
    if r['kind'] == 'mock':
        return (1, -1, int(r['key'][1:]), '')
    if r['kind'] == 'pred':
        return (1, '高中低'.index(r['lv']), int(r['key'][1:]), '')
    return (2, 0, int(r['key'][1:]), '')

TOPIC_TABLE = re.search(r'(<div class="pn"><h2>自編專題：徵收後讓土地回來的四條路</h2>.*?</div>)\s*<div id="toplist"', s, re.S).group(1)
TOPIC_TABLE = TOPIC_TABLE.replace('<div class="pn">', '<div class="topic" id="topic">', 1).replace('<h2>', '<h5 class="sec2">', 1).replace('</h2>', '</h5>', 1).replace('<p class="warn" style="margin:8px 0 0">', '<p class="note warn">')

groups = ''
for g in ORDER:
    gr = sorted([r for r in rows if r['cat'] == g], key=sortkey)
    off = [r for r in gr if r['kind'] == 'off']; mk = [r for r in gr if r['kind'] == 'mock']; pre = [r for r in gr if r['kind'] == 'pred']; top = [r for r in gr if r['kind'] == 'topic']
    arts = OrderedDict()
    for r in gr:
        for a in r['m']['cite']:
            arts.setdefault(a, []).append(r['key'] if r['kind'] == 'off' else ('預' + r['key'] if r['kind'] == 'pred' else '模' + r['key'] if r['kind'] == 'mock' else '專' + r['key']))
    al = sorted(arts, key=lambda a: (-offc[a], -sum(1 for k in arts[a] if not k.startswith(('預', '專', '模'))), -len(arts[a]), a))
    h = GH[g]
    ptag = P115[g]
    body = (f'<div class="gnote"><p>{h["rule"]}</p><p class="how"><b>答法</b>{h["how"]}</p></div>'
            f'<details class="btg"><summary>本組要背的條文（{len(al)} 條）<small>依官方申論引用次數排序・點條文看全文</small></summary>'
            f'<div class="btgb"><p class="btl">★★★＝歷屆官方申論考過 3 題以上　★★＝2 題　★＝1 題　沒有星＝歷屆沒考過、只在預測題出現。</p>{"".join(lawdet(a, arts[a]) for a in al)}</div></details>')
    body += f'<h5 class="sec">官方歷屆（{len(off)} 題）<small>{h["ys"].replace("出現：", "")}</small></h5>' + ''.join(card(r) for r in off)
    if mk:
        body += f'<h5 class="sec">補習班模擬卷（{len(mk)} 題）<small>非考選部；本站依現行條文撰寫範文</small></h5>' + ''.join(card(r) for r in mk)
    if pre:
        body += f'<h5 class="sec">預測題（自擬或網路來源・非考選部）{len(pre)} 題</h5>' + ''.join(card(r) for r in pre)
    if top:
        body += f'<h5 class="sec">自編專題：撤銷・廢止・收回（{len(top)} 題）</h5>' + TOPIC_TABLE + ''.join(card(r) for r in top)
    groups += (f'<details class="grp" id="cat-{g}" data-g="{g}"><summary><span class="gl">{g}</span><span class="gname">{h["name"]}</span>'
               f'<span class="gnum"><span><b>{TOT[g]}</b>16年考</span><span><b>{R5[g]}</b>近5年</span><span><b class="p{ptag}">{ptag}</b>115預測</span></span>'
               f'<span class="gread">官方 {len(off)}・預測 {len(pre) + len(top)}{"・模擬 " + str(len(mk)) if mk else ""}</span></summary><div class="gbody">{body}</div></details>')

# heat map: reuse old
HM = re.search(r'(<details class="pn hmd">.*?</details>)', s, re.S).group(1)
HM = HM.replace('虛線格＝預測會考見「預測」分頁', '預測題放在各主題內，虛線框卡片')
HM = HM.replace('<details class="pn hmd">', '<details class="hmd">')

NOFF = sum(1 for r in rows if r['kind'] == 'off'); NPRE = sum(1 for r in rows if r['kind'] == 'pred'); NTOP = sum(1 for r in rows if r['kind'] == 'topic'); NMK = sum(1 for r in rows if r['kind'] == 'mock')
NA = sum(1 for r in rows if r['lv'] == 'A'); NB = sum(1 for r in rows if r['lv'] == 'B'); NC = sum(1 for r in rows if r['lv'] == 'C')
tg = ''.join(f'<button type="button" data-g="{g}"><b>{g}　{SHORT[g]}</b><em>官方 {TOT[g]}・預測 {sum(1 for r in rows if r["cat"] == g and r["kind"] in ("pred", "topic"))}{"・模擬 " + str(sum(1 for r in rows if r["cat"] == g and r["kind"] == "mock")) if any(r["cat"] == g and r["kind"] == "mock" for r in rows) else ""}</em><small>{GSUB[g]}</small></button>' for g in ORDER)

css = open(os.path.join(os.path.dirname(__file__), 'full.css'), encoding='utf-8').read()
js = open(os.path.join(os.path.dirname(__file__), 'full.js'), encoding='utf-8').read()
head = s[:s.index('<style>')]
FAB = s[s.index('<!--bxfab-->'):s.index('<!--/bxfab-->') + len('<!--/bxfab-->')]
page = (head + '<style>' + css + '</style></head><body><button id="theme-btn" onclick="toggleTheme()" title="切換深淺色" aria-label="切換深淺色">☀️</button><main>'
        f'<header><h1>土地法｜申論題</h1><p class="sub">官方 {NOFF} 題＋補習班模擬卷 {NMK} 題＋預測 {NPRE} 題＋自編專題 {NTOP} 題，依 7 大主題分組（依 16 年出題數排序）；每題四段式、速寫、失分點、必提重點與條文全文　<a href="土地法申論題_六型答題模板.html">先判型：六型答題模板 ›</a>　<a href="土地法_申論115出題預測.html">115 出題預測 ›</a></p></header>'
        f'<div id="start"><input id="esq" class="esq" type="search" placeholder="搜尋：預告登記、累進起點、§34-1、說明書" aria-label="搜尋申論題"><div class="now" id="now"></div>'
        f'<div class="prg"><div class="prgb"><i id="prgi"></i></div><small id="prgt"></small></div></div>'
        f'<div class="fbar" id="fbar"><div class="fl" id="fk"><button class="fc" aria-pressed="true" data-f="">全部 {len(rows)}</button><button class="fc" aria-pressed="false" data-f="off">官方 {NOFF}</button><button class="fc" aria-pressed="false" data-f="mock">模擬卷 {NMK}</button><button class="fc" aria-pressed="false" data-f="pred">預測 {NPRE + NTOP}</button><button class="fc" aria-pressed="false" data-f="unread">未讀</button></div>'
        f'<div class="fl" id="fp"><button class="fc" aria-pressed="true" data-f="">所有級別</button><button class="fc" aria-pressed="false" data-f="3">必考／預測高</button><button class="fc" aria-pressed="false" data-f="2">高機率／預測中</button><button class="fc" aria-pressed="false" data-f="1">參考／預測低</button></div></div>'
        f'<p class="l2">依主題進入</p><div class="tg" id="tg">{tg}</div>'
        + HM +
        '<div class="ctl"><button class="mini" data-all="open">全部主題展開</button><button class="mini" data-all="close">全部收合</button><span class="cnt" id="cnt"></span></div>'
        f'<div id="glist">{groups}</div><p class="noresult" id="nores" hidden>沒有符合的題目。</p>'
        '<p class="note warn">四段式是我依官方答案與現行條文寫的範文，不是考選部標準答案；補習班模擬卷為補習班題目、範文由本站撰寫；預測題與自編專題皆為自擬。條文全文取自 6laws／LawPlayer／臺北市法規查詢逐字引文，考前仍以紙本法條為準。</p>'
        '</main><script>' + js + '</script>' + FAB + '\n<script src="bx-use.js"></script>\n</body></html>')
open(OUT, 'w', encoding='utf-8').write(page)
missing = sorted(set(a for r in rows for a in r['m']['cite'] if not (LAW.get(a) and LAW[a].get('p'))))
print('rows', len(rows), 'law have', len(LAW), 'missing', len(missing), missing[:60])
print('size', len(page))
