# -*- coding: utf-8 -*-
"""《土地法_申論題分類總覽》每張申論卡加「📚 這題該讀哪幾頁」（施工單第 6 項，仿民法 mk_esrd.py）。
依卡片文字（題目＋必提重點）套關鍵詞規則，由具體到一般；先只看標題，標題沒命中才看題目全文；同一頁只留一節，每張最多 3 個連結；都沒命中時依主題分組給預設。
gen_full.py 重產後要再跑一次。可重複執行（先移除舊的 .esrd 再插）。產生時檢查每個連結的檔案與錨點都存在。"""
import io, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '土地法_申論題分類總覽.html')
SUM, PROC, TAX = '土地法_彩色重點速記.html', '土地法_程序總整理.html', '土地法_稅率總表.html'
R = [
 (r'一生一次|一生一屋|自用住宅用地', '土地法_一生一次一生一屋分析.html', '一生一次・一生一屋'),
 (r'申報移轉現值|審核標準|移轉現值', '土地法_土增稅申報時間點.html', '土增稅申報時間點'),
 (r'34-1|優先購買|優先承買|優先承購|§104|§107', '土地法_優先購買權_物權債權.html', '優先購買權（物權・債權）'),
 (r'外國人', SUM + '#bookA', '彩色速記 A1（外國人取得）'),
 (r'不得私有|地權', SUM + '#bookA', '彩色速記 A1（地權・不得私有）'),
 (r'稅負', '土地法_稅制與取得方式比較表.html#s1', '稅制比較表 ① 五稅並排'),
 (r'繼承|列冊管理|73-1', '土地法_繼承專區.html', '繼承專區'),
 (r'實價登錄|申報登錄|預售屋|紅單|47-3|47-4|81-2', '土地法_罰則總整理.html#sx', '罰則總整理・申報登錄與預售屋'),
 (r'區段徵收|抵價地', PROC + '#t3', '程序總整理 ④ 區段徵收・市地重劃'),
 (r'市地重劃|抵費地|重劃', PROC + '#t3', '程序總整理 ④ 區段徵收・市地重劃'),
 (r'收回權|撤銷徵收|廢止徵收|徵用', PROC + '#t4', '程序總整理 ⑤ 徵收之後'),
 (r'(?<!減半)(?<!免)徵收(?!率)', PROC + '#d1', '程序總整理 ③ 土地徵收'),
 (r'照價收買|空地|規定地價|申報地價|公告地價|荒地', PROC + '#t2', '程序總整理 ② 地價類'),
 (r'都市計畫|細部計畫|主要計畫|保留地|都計', PROC + '#t1', '程序總整理 ① 計畫類'),
 (r'區域計畫|非都市|國土計畫|開發許可|區計', '土地法_速查三表.html#s3', '速查三表 ③ 三計畫法比較'),
 (r'地價稅', TAX + '#landvalue', '稅務總表・地價稅'),
 (r'土地增值稅|土增稅', TAX + '#zeng', '稅務總表・土地增值稅'),
 (r'房屋稅', TAX + '#house', '稅務總表・房屋稅'),
 (r'契稅', TAX + '#deed', '稅務總表・契稅'),
 (r'房地合一', TAX + '#hehe', '稅務總表・房地合一'),
 (r'不課徵|免徵|減徵', '土地法_速查三表.html#s2', '速查三表 ② 免徵／不課徵／減徵'),
 (r'罰鍰|怠報金|滯納金|罰則', '土地法_罰則總整理.html', '罰則總整理'),
 (r'預告登記|限制登記|登記', SUM + '#bookA', '彩色速記 第一篇（土地法）'),
 (r'耕地|三七五|農地|農舍|農業用地', SUM + '#bookF', '彩色速記 第六～九篇'),
]
DEF = {'A': (PROC + '#t1', '程序總整理 ① 計畫類'), 'B': (PROC + '#d1', '程序總整理 ③ 土地徵收'), 'C': (PROC + '#t3', '程序總整理 ④ 區段徵收・市地重劃'),
       'D': (SUM + '#bookA', '彩色速記 第一篇（土地法）'), 'E': (TAX + '#landvalue', '稅務總表'), 'F': ('土地法_稅制與取得方式比較表.html#s1', '稅制比較表 ① 五稅並排'),
       'G': (SUM + '#bookA', '彩色速記 第一篇（土地法）')}
TAXES = ['地價稅', '土地增值稅|土增稅', '房屋稅', '契稅', '房地合一']
ids = {}
def has(href):
    f, _, a = href.partition('#'); p = os.path.join(ROOT, f)
    if not os.path.exists(p): return False
    if not a: return True
    if f not in ids: ids[f] = set(re.findall(r'id="([^"]+)"', io.open(p, encoding='utf-8').read()))
    return a in ids[f]
s = io.open(HUB, encoding='utf-8').read()
s = re.sub(r'<div class="esrd">.*?</div><!--esrd-->', '', s, flags=re.S)
grp = {}
for m in re.finditer(r'<details class="grp" id="cat-([A-Z])"', s): grp[m.start()] = m.group(1)
starts = sorted(grp)
out, last, nlink, tg = [], 0, 0, set()
for m in re.finditer(r'<details class="es[^"]*" id="([^"]+)"([^>]*)>', s):
    cid = m.group(1); tx = html.unescape(re.search(r'data-tx="([^"]*)"', m.group(2)).group(1) if 'data-tx' in m.group(2) else '')
    end = s.index('<label class="done">', m.end())
    title = re.sub(r'<[^>]+>', '', re.search(r'<b class="et">(.*?)</b>', s[m.end():end]).group(1))
    t = title + ' ' + tx
    cat = grp[max(x for x in starts if x < m.start())]
    L, pages = [], set()
    if sum(1 for k in TAXES if re.search(k, title)) >= 2:
        L.append(('土地法_稅制與取得方式比較表.html#s1', '稅制比較表 ① 五稅並排')); pages.add('土地法_稅制與取得方式比較表.html')
    for src in (title, t):   # 先只看標題；標題沒命中才看題目全文
        for pat, href, lab in R:
            if len(L) >= 3: break
            f = href.split('#')[0]
            if f in pages or not re.search(pat, src): continue
            L.append((href, lab)); pages.add(f)
        if L: break
    if not L: L.append(DEF[cat])
    for h, _ in L: assert has(h), (cid, h)
    nlink += len(L); tg.update(h for h, _ in L)
    blk = '<div class="esrd"><b>📚 這題該讀哪幾頁</b>' + ''.join('<a href="%s">%s ›</a>' % (h, lab) for h, lab in L) + '</div><!--esrd-->'
    out.append(s[last:end] + blk); last = end
s = ''.join(out) + s[last:]
css = '<style id="esrd-css">.esrd{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin:10px 0 4px;padding:8px 10px;border-radius:8px;background:var(--tint,#f4efe2);font-size:.82rem}.esrd b{font-size:.8rem}.esrd a{color:var(--pri,#2F5D50);font-weight:700;text-decoration:none;border-bottom:1px dotted currentColor}</style>'
s = re.sub(r'<style id="esrd-css">.*?</style>', '', s, flags=re.S)
s = s.replace('</head>', css + '</head>', 1)
io.open(HUB, 'w', encoding='utf-8').write(s)
print('cards', len(out), 'links', nlink, 'targets', len(tg))
