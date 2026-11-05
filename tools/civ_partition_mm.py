# -*- coding: utf-8 -*-
"""民法 共有專區：分割判斷心智圖＋租金卡＋次序說明＋申論複習；定義填空補卡（使用者 11-05）。
可重跑：共有專區以 <!--mm:xxx--> 標記為邊界；填空同名不重加；補償金卡陷阱以標記句判斷。
條號皆對 tools/civ_quiz/law.json；「判決確定即取得」「付錢人＝抵押人才相遇」為推理，頁面已註明。
"""
import os, re, json
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CO = os.path.join(ROOT, '民法_共有專區.html')
FILL = os.path.join(ROOT, '民法_定義填空練習.html')

# ---------- 心智圖（顏色全用頁面 CSS 變數，跟深淺色） ----------
B = [('① 能不能分', 'main', [('原則：隨時可分', '§823Ⅰ', 0), ('例外：使用目的、約定不分割', '§823Ⅰ', 0), ('期限：5年，不動產管理約定30年', '§823Ⅱ', 1), ('再例外：重大事由仍可分', '§823Ⅲ', 0), ('公同共有：存續中不得分', '§829', 0), ('遺產：繼承人可隨時請求分割', '§1164', 1)]),
     ('② 怎麼分', 'main', [('先協議', '§824Ⅰ', 0), ('不能協議或時效拒履行→法院', '§824Ⅱ', 0), ('原物分配優先', '§824Ⅱ①', 1), ('困難才變賣', '§824Ⅱ②', 1), ('分不足→金錢補償', '§824Ⅲ', 1)]),
     ('③ 分割效力', 'main', [('取得時點', '', 2), ('協議：登記才生效', '§758', 1), ('裁判：判決確定即取得', '§824-1Ⅰ', 1), ('處分前須先登記', '§759', 1), ('互負出賣人擔保', '§825', 0), ('抵押權', '', 2), ('無但書：每筆土地都還在', '§824-1Ⅱ', 1), ('有但書：移存抵押人分得部分', '§824-1Ⅱ但', 1), ('有但書＋只分到錢：權利質權', '§824-1Ⅲ', 1), ('補償金抵押：分割時一併登記', '§824-1Ⅳ', 1), ('對移存者：補償金優先', '§824-1Ⅴ', 3), ('對本文者：依登記先後', '§865', 3)]),
     ('另案・租金', 'side', [('出租＝管理，雙過半', '§820Ⅰ', 0), ('過半：租金按持分分', '§818', 0), ('未過半：對他人不生效', '', 0), ('向承租人：返還全體', '§821', 1), ('向出租人：按持分請求不當得利', '§179', 1), ('費用按持分分擔', '§822', 0)])]


def w(s, sz): return sum(sz * 0.56 if ord(c) < 0x2000 else sz for c in s)


def svg():
    RH, GAP, BX, BW, TX = 21, 22, 41, 88, 133
    PX = BX + BW / 2; XL = {0: 139, 2: 139, 1: 154, 3: 169}
    G, LN = 'var(--green)', 'var(--ink-soft)'
    out, txt, y, groups = [], [], 60, []
    for name, kind, ls in B:
        rows = []
        for t, law, ind in ls:
            cy = y + RH / 2; x = XL[ind]
            assert x + w(t, 12) + 5 + w(law, 11) <= 376, t
            rows.append((x, cy, t, law, ind)); y += RH
        groups.append((name, kind, rows)); y += GAP
    H = y - GAP + 12
    out.append(f'<rect x="{BX}" y="10" width="{BW}" height="30" rx="15" style="fill:{G}"/><text x="{PX}" y="30" text-anchor="middle" font-size="14" font-weight="700" style="fill:var(--onc)">共有物分割</text>')
    prevb = 40
    for name, kind, rows in groups:
        pc = rows[0][1]
        if kind == 'main':
            out.append(f'<line x1="{PX}" y1="{prevb+1}" x2="{PX}" y2="{pc-16}" marker-end="url(#mmar)" style="stroke:{G};stroke-width:1.8"/>')
            out.append(f'<rect x="{BX}" y="{pc-14}" width="{BW}" height="28" rx="14" style="fill:var(--surf);stroke:{G};stroke-width:1.2"/><text x="{PX}" y="{pc+5}" text-anchor="middle" font-size="14" font-weight="700" style="fill:{G}">{name}</text>')
            prevb = pc + 14; col = G
        else:
            out.append(f'<path d="M{BX} 25 L22 25 L22 {pc} L{BX-2} {pc}" fill="none" stroke-dasharray="4 3" marker-end="url(#mmar)" style="stroke:{LN};stroke-width:1.2"/>')
            out.append(f'<a href="#s2"><rect x="{BX}" y="{pc-14}" width="{BW}" height="28" rx="14" stroke-dasharray="4 3" style="fill:none;stroke:{LN};stroke-width:1.2"/><text x="{PX}" y="{pc+5}" text-anchor="middle" font-size="14" font-weight="700" style="fill:var(--ink-soft)">{name}</text></a>')
            col = LN
        tops = [r for r in rows if r[4] in (0, 2)]
        out.append(f'<path d="M{BX+BW} {pc} L{TX} {pc} L{TX} {tops[-1][1]}" fill="none" style="stroke:{col};stroke-width:1.2"/>')
        for r in tops: out.append(f'<line x1="{TX}" y1="{r[1]}" x2="{TX+4}" y2="{r[1]}" style="stroke:{col};stroke-width:1.2"/>')
        last = {0: None, 1: None}
        for x, cy, t, law, ind in rows:
            if ind in (0, 2): last[0] = cy
            elif ind == 1:
                out.append(f'<path d="M145 {last[0]+7} L145 {cy} L151 {cy}" fill="none" style="stroke:{LN};stroke-width:1"/>'); last[1] = cy
            else:
                out.append(f'<path d="M160 {last[1]+7} L160 {cy} L166 {cy}" fill="none" style="stroke:{LN};stroke-width:1"/>')
            if ind == 2:
                txt.append(f'<text x="{x}" y="{cy+4}" font-size="12" font-weight="700" style="fill:var(--ink)">{t}</text>'); continue
            s = f'<text x="{x}" y="{cy+4}" font-size="12" style="fill:var(--ink)">{t}'
            if law: s += f'<tspan dx="5" font-size="11" style="fill:var(--ink-soft)">{law}</tspan>'
            txt.append(s + '</text>')
    return (f'<svg viewBox="0 0 380 {H}" role="img" aria-label="共有物分割判斷心智圖"><title>共有物分割判斷心智圖</title>'
            '<defs><marker id="mmar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
            + ''.join(out + txt) + '</svg>')


ESS = lambda k: '民法_備考指揮中心.html#essay=' + __import__('urllib.parse').parse.quote(k)
SPR = lambda f, k: f + '#q=' + __import__('urllib.parse').parse.quote(k)

FIG = ('<!--mm:fig--><figure class="mmap">' + svg() + '<figcaption>判斷順序：主幹 ①→②→③ 由上往下讀，縮排是上一行的細節；'
       '虛線「另案・租金」是獨立請求，不是分割的前提（點它看 ②）。「判決確定即取得」由§824-1Ⅰ「分割之效力發生時」及§759 推得。</figcaption></figure><!--mm:/fig-->')

ORDER = ('<!--mm:order--><p class="side"><b>補償金抵押權與原抵押權誰先？</b>§824-1Ⅴ只說補償金抵押權優先於「Ⅱ但書移存」的抵押權。'
         '①依本文（無但書三款）：原抵押權仍在每一筆，包括補償義務人分得的那筆 → 兩者在同一筆相遇，依<b class="an">§865</b>登記先後，原抵押權在先（<a class="el" href="'
         + ESS('預02') + '">預02</a>）。②依但書移存：原抵押權只在抵押人分得那筆 → 只有「付錢的人＝抵押人」時才會在同一筆相遇，此時補償金抵押權優先（Ⅴ）。（推理整理，非條文原句）</p><!--mm:/order-->')

ESSAY = ('<!--mm:essay--><div class="card mmes"><h4>申論複習：分割與抵押權（四段式）</h4><ol>'
         '<li><b>定義</b>：分割後，應有部分上的抵押權落在哪裡；未受分配者的補償金怎麼擔保。</li>'
         '<li><b>法條</b>：<b class="an">§824Ⅲ</b> 金錢補償；<b class="an">§824-1Ⅱ</b> 本文不受影響、但書三款移存；Ⅲ 只分到錢準用<b class="an">§881</b>Ⅰ、Ⅱ；Ⅳ 補償金抵押權；Ⅴ 一併登記、優先於但書抵押權；<b class="an">§865</b> 登記先後。</li>'
         '<li><b>涵攝</b>：題目有沒有寫權利人同意、參加或經告知未參加 → 決定原抵押權在哪幾筆 → 補償金抵押權在補償義務人那筆 → 同一筆相遇才排次序（本文看§865；移存看Ⅴ）。</li>'
         '<li><b>結論</b>：題目沒寫但書三款 → 依本文，原抵押權在先；寫了但書且付錢人＝抵押人 → 補償金抵押權在先。</li></ol>'
         '<p class="mmgo"><a class="go" href="' + SPR('民法_申論5分鐘_推理版.html', '預02') + '">推理版練預02 ▸</a>'
         '<a class="go" href="' + SPR('民法_申論5分鐘衝刺.html', '預02') + '">考場版衝刺 ▸</a>'
         '<a class="go" href="' + ESS('103-二') + '">103-二 範文 ▸</a><a class="go" href="' + ESS('110-一') + '">110-一 範文 ▸</a></p></div><!--mm:/essay-->')

RENT = ('<!--mm:rent--><div class="card"><h4>未過半私自出租：租金怎麼要回來</h4><p>例：甲 1/2、乙丙各 1/4，甲未經同意把整筆地出租，一年收 120 萬。<br>'
        '對承租人：租約只在甲與承租人間有效，對乙丙<b class="k">不生效力</b> → 乙丙得依<b class="an">§821</b>但書請求返還<b class="k">全體</b>共有人。<br>'
        '對甲：各共有人按應有部分使用收益（<b class="an">§818</b>），甲收取逾其應有部分之租金 → 乙丙依<b class="an">§179</b>按<b class="k">應有部分</b>請求返還（各 30 萬），甲自己的 60 萬不用吐；甲墊付的稅費可依<b class="an">§822</b>Ⅱ請求償還。<br>'
        '金額以實際租金或相當租金計，實務見解不一（待查）。</p>'
        '<p class="mmgo"><a class="go" href="' + SPR('民法_申論5分鐘_推理版.html', '106-一') + '">推理版練106-一 ▸</a><a class="go" href="' + ESS('106-一') + '">106-一 範文 ▸</a></p></div><!--mm:/rent-->')

CSS = ('<style id="mm-css">.mmap{margin:12px auto 8px;max-width:560px}.mmap svg{display:block;width:100%;height:auto}'
       '.mmap a{cursor:pointer}.mmap figcaption{font-size:12.5px;color:var(--ink-soft);margin-top:4px;line-height:1.6}'
       '.mmes{margin-top:12px}.mmes ol{padding-left:1.3em;font-size:14px}.mmes li{margin:3px 0}'
       '.mmgo{margin-top:6px;display:flex;flex-wrap:wrap;gap:6px}.mmgo .go{margin:0}</style>')


def put(s, tag, block, anchor_fn):
    a, b = f'<!--mm:{tag}-->', f'<!--mm:/{tag}-->'
    if a in s:
        i = s.index(a); j = s.index(b) + len(b); return s[:i] + block + s[j:]
    p = anchor_fn(s); return s[:p] + block + s[p:]


s = open(CO, encoding='utf-8').read()
if 'id="mm-css"' in s:
    i = s.index('<style id="mm-css">'); j = s.index('</style>', i) + 8; s = s[:i] + CSS + s[j:]
else:
    i = s.index('</head>'); s = s[:i] + CSS + s[i:]
S5 = s.index('id="s5"')
s = put(s, 'fig', FIG, lambda s: s.index('</p>', s.index('<p class="lead">', s.index('id="s5"'))) + 4)
s = put(s, 'order', ORDER, lambda s: s.index('</table></div>', s.index('續存 vs 移存')) + len('</table></div>'))
s = put(s, 'essay', ESSAY, lambda s: s.index('<details class="law">', s.index('id="s5"')))
s = put(s, 'rent', RENT, lambda s: s.index('<div class="card"><h4><b class="an">§820</b> Ⅱ～Ⅳ'))
open(CO, 'w', encoding='utf-8').write(s)
print('共有專區 OK')

# ---------- 定義填空 D1 補卡 ----------
f = open(FILL, encoding='utf-8').read()
i = f.find('const DATA = ') + 13; D, e = json.JSONDecoder().raw_decode(f[i:])


def cv(t): return re.sub(r'\[\[(.+?)\]\]', '___', t), re.sub(r'\[\[(.+?)\]\]', r'<span class="key">\1</span>', t)


def card(term, t, src, p, m, tr, es=()):
    b, a = cv(t); x = {'term': term, 'blank': b, 'answer': a, 'src': src, 'mc': 0, 'p': p, 'm': m, 't': tr}
    if es: x['es'] = list(es)
    return x


ADD = [
    card('分割的方法（§824）',
         '共有物之分割，依共有人[[協議]]之方法行之（§824Ⅰ）。<br>分割之方法不能協議決定，或於協議決定後因[[消滅時效]]完成經共有人拒絕履行者，法院得因任何共有人之請求，以[[原物]]分配於各共有人；原物分配顯有困難時，得[[變賣]]共有物，以價金分配於各共有人（§824Ⅱ）。<br>以原物為分配時，如共有人中有未受分配，或不能按其應有部分受分配者，得以[[金錢補償]]之（§824Ⅲ）。',
         '民法§824Ⅰ～Ⅲ', '先自己談；談不成，或談好了對方用時效拒絕履行，才找法院。法院先分地，分地太難才賣掉分錢；分到的地不夠的人，用錢補。',
         '先協議、後法院；原物先、變賣後、不足補錢〔自編〕',
         '協議後對方以時效抗辯拒絕履行，也可以請求法院分割；原物分配可只分給部分共有人（§824Ⅱ①但書），一部分也可維持共有（§824Ⅳ）；變賣時共有人有優先承買權（§824Ⅶ）。',
         ('110-一', '103-二', '預02')),
    card('分割後何時取得所有權★陷阱',
         '共有人自共有物分割之[[效力發生]]時起，取得分得部分之所有權（§824-1Ⅰ）。<br>協議分割屬依法律行為取得不動產物權，非經[[登記]]，不生效力（§758Ⅰ）。<br>因法院之判決於登記前已取得不動產物權者，應經登記，始得[[處分]]其物權（§759）。',
         '民法§824-1Ⅰ、§758Ⅰ、§759', '協議分割要登記才拿到；法院判決分割，判決確定就拿到，只是要賣或設定負擔前得先登記。',
         '協議靠登記、判決確定就取得、處分前先登記〔自編〕',
         '「裁判分割要登記才取得」錯（113-14、102-14）；「協議達成時即取得」錯（99-24）。判決確定時取得是由§759「法院之判決」推得，§824-1Ⅰ條文只寫「分割之效力發生時」。'),
    card('未過半私自出租的租金★陷阱',
         '共有物之管理（如出租），應以共有人過半數及其應有部分合計過半數之同意行之（§820Ⅰ）；未達多數決之租約，對不同意之共有人[[不生效力]]。<br>各共有人按其[[應有部分]]，對於共有物之全部，有使用收益之權（§818）；出租人收取逾其應有部分之租金，他共有人得依[[不當得利]]請求返還（§179）。<br>回復共有物之請求，僅得為[[共有人全體]]之利益為之（§821但書）。',
         '民法§818、§820Ⅰ、§821、§179', '甲 1/2、乙丙各 1/4，甲私自出租收 120 萬：乙丙各可向甲要 30 萬；向承租人只能請求把地還給全體。',
         '租約對外有效、對他人不生效；超收的按持分吐出來〔自編〕',
         '不是「租約無效、租金全部退給承租人」；他共有人只能請求自己應有部分比例的租金；出租人墊付的稅費可依§822Ⅱ請求償還；金額以實際租金或相當租金計，實務見解不一。',
         ('106-一', '102-一')),
]
MARK = 'Ⅴ只優先於但書「移存」的抵押權'
added = 0
for ch in D:
    if ch['id'] != 'D1': continue
    for c in ADD:
        if not any(x['term'] == c['term'] for x in ch['cards']):
            assert c['blank'].count('___') == c['answer'].count('class="key"'); ch['cards'].append(c); added += 1
    for x in ch['cards']:
        if x['term'] == '補償金抵押權（申論高頻）' and MARK not in x.get('t', ''):
            x['t'] = x.get('t', '') + '　' + MARK + '；依本文時原抵押權仍在每一筆（含補償義務人分得者），依§865登記先後，原抵押權在先。移存抵押權只在抵押人分得那筆，所以「付錢的人＝抵押人」時才會與補償金抵押權相遇（推理整理）。'
f = f[:i] + json.dumps(D, ensure_ascii=False, indent=1) + f[i + e:]
open(FILL, 'w', encoding='utf-8').write(f)
print('填空新增', added)

# ---------- 題數同步（定義卡＝非 S 章合計） ----------
n = sum(len(ch['cards']) for ch in D if not ch['id'].startswith('S'))
f = open(FILL, encoding='utf-8').read()
f = re.sub(r'定義 \d+ 題＋申論四段', '定義 %d 題＋申論四段' % n, f, count=1); open(FILL, 'w', encoding='utf-8').write(f)
U = os.path.join(ROOT, 'bxm-use.js'); u = open(U, encoding='utf-8').read()
u = re.sub(r'fill:\d+,', 'fill:%d,' % n, u, count=1); open(U, 'w', encoding='utf-8').write(u)
print('定義卡', n)

# ---------- 申論卡：只同步「這題該讀哪幾頁」對照（先跑 tools/civ_quiz/mk_esrd.py） ----------
H = open(os.path.join(ROOT, '民法_備考指揮中心.html'), encoding='utf-8').read()
CP = os.path.join(ROOT, '民法_申論卡.html'); C = open(CP, encoding='utf-8').read()
def _b(x): a = x.index('<script id="esrd-js">'); return a, x.index('</script>', a) + 9
a, b = _b(H); blk = H[a:b]; a, b = _b(C); C = C[:a] + blk + C[b:]
open(CP, 'w', encoding='utf-8').write(C); print('申論卡對照已同步')
