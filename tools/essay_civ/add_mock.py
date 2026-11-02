# -*- coding: utf-8 -*-
"""民法模擬卷申論收進指揮中心申論分頁（施工單《申論統一_20261102》第一節；取代 add_mock_ls.py）。
- 來勝模擬(一) 2 題（來勝-一／二，補習班模擬卷）、申論專練卷 3 題（專練-一／二／三，本站模擬卷）。
- 本站模擬試題一、二的 4 題＝既有預測卡 預05、預08、預01、預06（題目相同），不重複建卡，模擬卷頁改嵌入那幾張。
- 完整四段式、考場速寫、得分關鍵詞、失分點、口訣＝卷頁原資料一字不改；專練卷的邏輯拆解＝卷頁原有 lj；來勝的邏輯拆解＝lj_mock_ls.json；
  考場版＝exam_ver/ev_*.json（之後跑 build_ev.py）。卡片 class 加 pred mock（虛線框）、data-lv="M"。
- 篩選「模擬卷 N」、各組標題、已讀計數、bxm-use.js 申論總數都依實際卡數。可重跑。"""
import io, json, os, re, html
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
HUB = os.path.join(R, '民法_備考指揮中心.html')
E = html.escape
s = io.open(HUB, encoding='utf-8').read()
def data(page):
    t = io.open(os.path.join(R, page), encoding='utf-8').read()
    return json.JSONDecoder().raw_decode(t[t.index('var D=') + 6:])[0]['E']
LAW = json.load(io.open(os.path.join(R, 'tools', 'civ_quiz', 'law.json'), encoding='utf-8'))
CIRC = dict(zip('ⅠⅡⅢⅣⅤⅥⅦ', '①②③④⑤⑥⑦'))
LS_META = json.load(io.open(os.path.join(H, 'ls_mock.json'), encoding='utf-8'))
LJ = {x['k']: x for x in json.load(io.open(os.path.join(H, 'lj_mock_ls.json'), encoding='utf-8'))}
LJF = os.path.join(H, 'lj_data.json'); LD = json.load(io.open(LJF, encoding='utf-8'))
LD = [x for x in LD if x['k'] not in LJ] + list(LJ.values())
io.open(LJF, 'w', encoding='utf-8').write(json.dumps(LD, ensure_ascii=False, indent=1))
gl = io.open(os.path.join(H, 'gen_lj.py'), encoding='utf-8').read()
ns = {'re': re, 'html': html, 'E': E}
exec(gl[gl.index('def rich('):gl.index('VT = ')], ns)
render = ns['render']

# (卡號, 卷頁, 第幾題, 類別, 組, 標題, 分類, chips, 卷名)
CARDS = [
 ('來勝-一', '民法_來勝模擬試題一.html', 0, 'cram', None, None, None, None, '來勝115模擬試題（一）'),
 ('來勝-二', '民法_來勝模擬試題一.html', 1, 'cram', None, None, None, None, '來勝115模擬試題（一）'),
 ('專練-一', '民法_申論專練卷.html', 0, 'site', 'g1', '共有：分管約定未登記與多數決出租、租金返還', 'D共有', ['§826-1', '§820', '§818', '§179'], '申論專練卷①'),
 ('專練-二', '民法_申論專練卷.html', 1, 'site', 'g5', '行為能力＋詐欺＋瑕疵擔保：未成年人用詐術購買泡水車', 'A行為能力＋C買賣', ['§77', '§83', '§92', '§360'], '申論專練卷①'),
 ('專練-三', '民法_申論專練卷.html', 2, 'site', 'g6', '贈與之任意撤銷＋歸扣與繼承人限定責任', 'C贈與＋E繼承', ['§408', '§1173', '§1148', '§1148-1'], '申論專練卷①'),
]
NO = '一二三'

def paras(t): return ''.join('<p>' + E(x) + '</p>' for x in t.split('\n') if x.strip())
def lawcard(a):
    if a not in LAW: return ''
    ps = []
    for line in LAW[a]['x'].split('\n'):
        line = line.strip()
        if line and line[0] in CIRC: line = CIRC[line[0]] + ' ' + line[1:].strip()
        if line: ps.append('<p>' + E(line) + '</p>')
    head = re.sub(r'\s+', '', re.sub(r'^[①-⑳]\s*', '', LAW[a]['x'].split('\n')[0]))
    return ('<details class="bt"><summary><b class="bn">§%s</b><span class="bti">%s</span><span class="bm">模擬卷用到</span></summary>'
            '<div class="btx">%s</div></details>') % (a, E(head[:16] + ('…' if len(head) > 16 else '')), ''.join(ps))
def arts(t):
    out = []
    for a, b in re.findall(r'第(\d+)條(?:之(\d+))?', t):
        k = a + ('-' + b if b else '')
        if k not in out: out.append(k)
    return out
def auto_sub(x):
    x = re.sub(r'^（[一二三四五]）', '', x.strip()); first = x.split('\n')[0]
    c = first.find('：')
    t = first[:c] if 0 < c <= 24 else ''
    rest = first[c + 1:] if t else first
    m = re.search(r'^.*?[。；]', rest); pt = m.group(0) if m else rest[:60]
    return t, pt

def card(key, page, qi, kind, g, et, ec, chips, title):
    d = data(page)[qi]; P = dict(d['parts']); no = NO[qi]
    if kind == 'cram':
        m = LS_META[key]; g, et, ec, chips = m['g'], m['et'], m['ec'], m['chips']
    pc = '補習班模擬卷・非官方' if kind == 'cram' else '本站模擬卷・自擬'
    summ = ('<summary><span class="eh"><span class="ck" aria-label="已讀">✓</span><b class="et">%s</b><span class="st"></span></span>'
            '<span class="em"><span class="ek">%s 申論%s</span><span class="ec">%s</span></span><span class="chips"><i class="pc">%s</i>%s</span></summary>') % (
        E(et), E(title), no, E(ec), pc, ''.join('<i>%s</i>' % E(c) for c in chips))
    src = '出題：高律、嶺律；非考選部官方試題' if kind == 'cram' else '本站自擬；非考選部官方試題'
    oq = ('<div class="oq"><b>【%s｜%s申論題%s，%s】</b>%s<br><a href="%s">%s →</a></div>') % (
        '補習班模擬卷' if kind == 'cram' else '本站模擬卷', E(title), no, src, E(d['q']), page,
        '老師版擬答與本站差異（模擬卷頁）' if kind == 'cram' else '到模擬卷頁限時作答')
    vt = '<div class="vt"><button class="on" data-v="3">邏輯拆解</button><button data-v="1">考場速寫</button><button data-v="0">完整四段式</button></div>'
    sub = [x for x in re.split(r'\n?(?=（[一二三四五]）)', P['三、涵攝分析'].strip()) if x.strip()]
    if kind == 'cram': st = list(zip(LS_META[key]['sub_titles'], LS_META[key]['sub_pts']))
    else: st = [(('（%s）' % '一二三四五'[i]) + (t + '：' if t else ''), pt) for i, (t, pt) in enumerate(auto_sub(x) for x in sub)]
    hs = ''.join('<details class="sub2"><summary><b>%s</b><span class="pt">%s</span></summary><div class="full">%s</div></details>'
                 % (E(t), E(pt), paras(re.sub(r'^（[一二三四五]）', '', x.strip()))) for (t, pt), x in zip(st, sub))
    concl = re.sub(r'(?<=。)(?=（[二三四]）)', '\n', P['四、結論'])
    skip = ('補習班模擬題', '【老師版與本站差異】', '【老師原文錯字】')
    warn = [x for x in d.get('warn', '').split('\n') if x.strip() and not x.startswith(skip)]
    al = [a for a in arts(P['二、法條']) if a in LAW]
    bt = '<div class="btw"><div class="bth">📌 這題要背的條文（%d 條）</div>%s</div>' % (len(al), ''.join(lawcard(a) for a in al)) if al else ''
    full = ('<div class="vp" data-v="0" hidden>'
            '<details class="blk b1 fd"><summary><h5>一、定義</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b2 fd"><summary><h5>二、法條</h5></summary><div class="fdb">%s%s</div></details>'
            '<details class="blk b3 fd"><summary><h5>三、涵攝分析</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b4 fd"><summary><h5>四、結論</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b5 fd"><summary><h5>考試陷阱・提醒</h5></summary><div class="fdb">%s%s</div></details></div>') % (
        paras(P['一、定義']), paras(P['二、法條']), bt, hs, paras(concl), paras(P.get('考試陷阱', '')), paras('\n'.join(warn)))
    V = {v['n']: v for v in d['v']}
    sx = V['考場速寫版']['parts']; sk = {x[0]: x[1] for x in V['得分關鍵與失分點']['parts']}
    quick = '<div class="vp" data-v="1" hidden>' + ''.join('<div class="blk b%d"><h5>%s</h5><p>%s</p></div>' % (i + 1, E(re.sub(r'^[一二三四]、', '', h)), E(t).replace('\n', '<br>')) for i, (h, t) in enumerate(sx))
    quick += '<div class="kou"><b>口訣〔自編〕</b>　%s</div>' % E(d['m'])
    quick += '<div class="sk2"><h5>得分關鍵詞</h5><div class="chips big">%s</div><h5>常見失分點</h5><ul>%s</ul>%s</div></div>' % (
        ''.join('<i>%s</i>' % E(x.strip()) for x in sk['得分關鍵詞'].split('｜')),
        ''.join('<li>%s</li>' % E(re.sub(r'^[①②③④⑤⑥]\s*', '', x)) for x in sk['常見失分點'].split('\n') if x.strip()),
        ('<h5>加分點</h5><p>%s</p>' % E(sk['加分點'])) if sk.get('加分點') else '')
    ljh = render(LJ[key]) if key in LJ else d['lj']
    ljv = '<div class="vp" data-v="3" data-lj-root="1">' + ljh + '</div>'
    return g, ('<details class="essay es p4 pred mock" data-lv="M" data-key="%s" data-yr="" data-g="%s">%s<div class="ebody">%s%s%s%s%s'
               '<label class="done"><input type="checkbox" class="rd" data-key="%s"> 我已讀過這題</label></div></details>\n') % (
        key, g, summ, oq, vt, full, quick, ljv, key)

for c in CARDS:
    key = c[0]
    i = s.find('<details class="essay es p4 pred mock" data-lv="M" data-key="%s"' % key)
    if i >= 0:
        e = s.index('</details>\n', s.index('<label class="done"><input type="checkbox" class="rd" data-key="%s">' % key, i)) + len('</details>\n')
        s = s[:i] + s[e:]
for c in CARDS:
    g, html_ = card(*c)
    a = re.search(r'<details class="essay[^"]*\bpred\b(?![^"]*mock)[^"]*" data-lv="P" data-key="[^"]+" data-yr="[^"]*" data-g="%s"' % g, s)
    s = s[:a.start()] + html_ + s[a.start():]
NM = s.count('data-lv="M"')
s = re.sub(r'<button data-f="M">[^<]*</button>', '<button data-f="M">模擬卷 %d</button>' % NM, s)
JSR = [
 ("h3.textContent='補習班模擬卷（非官方）'+nm+' 題'", "h3.textContent='模擬卷（補習班／本站自擬，非官方）'+nm+' 題'"),
 ("'　補習班 '+em.filter", "'　模擬卷 '+em.filter"),
 ("+'＋補習班 '+essays.filter(function(e){return e.classList.contains('mock')}).length", "+'＋模擬卷 '+essays.filter(function(e){return e.classList.contains('mock')}).length"),
]
for a, b in JSR:
    if b in s: continue
    assert s.count(a) == 1, a[:50]; s = s.replace(a, b)
io.open(HUB, 'w', encoding='utf-8').write(s)
N = s.count('class="essay')
gl2 = re.sub(r'assert done == \d+, done.*', 'assert done == %d, done  # 含模擬卷卡' % N, gl)
gl2 = gl2.replace("    if k not in D: sys.exit('缺資料 ' + k)", "    if k not in D:\n        if 'data-lv=\"M\"' in s[i:i + 300]: done += 1; continue  # 模擬卷卡的邏輯拆解來自卷頁\n        sys.exit('缺資料 ' + k)")
if gl2 != gl: io.open(os.path.join(H, 'gen_lj.py'), 'w', encoding='utf-8').write(gl2)
U = os.path.join(R, 'bxm-use.js'); u = io.open(U, encoding='utf-8').read()
u2 = re.sub(r'name:"申論 \d+ 題（[^"]*）",done:rn,total:\d+,pct:Math.round\(rn/\d+\*100\),txt:"已讀 "\+rn\+"／\d+"',
            'name:"申論 %d 題（官方32＋模擬卷%d＋預測49）",done:rn,total:%d,pct:Math.round(rn/%d*100),txt:"已讀 "+rn+"／%d"' % (N, NM, N, N, N), u)
if u2 != u: io.open(U, 'w', encoding='utf-8').write(u2)
print('卡數', N, '模擬卷', NM)
