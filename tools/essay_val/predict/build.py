# 產生《估價_申論115出題預測.html》：歷屆申論主題網格＋主題預測等級＋63 張卡讀卡順序
# 資料（全部從站上檔案讀，數字不寫死）：
#   不動產估價概要_申論題實戰範文.html 的 .essay-card（id／data-type／card-title／card-meta 標籤／預測依據）
#   bxv-quiz-data.js（選擇題章別，只取 y>0 的官方題）
#   技術規則逐字檔（章節範圍；找不到時用 law_chapters.json 快取）
#   topic_map.json（卡號→主題的人工歸類；未列卡片依 § 標籤自動歸類）
# 用法：python3 tools/essay_val/predict/build.py [--law 逐字檔路徑]
import re, json, os, sys, html, subprocess, statistics, datetime
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = '不動產估價概要_申論題實戰範文.html'
OUT = os.path.join(ROOT, '估價_申論115出題預測.html')
HUB = '估價備考指揮中心.html'
TPL_PAGE = os.path.join(ROOT, '經紀法規_申論115出題預測.html')  # 只讀：借 bxfab 區塊
LAW_DEFAULT = '/tmp/claude-0/-home-claude/ac4bbd9f-3aea-5322-85d9-48ab97ee8f14/scratchpad/law_估價_技術規則_全文逐字_§1-§133_20261022.md'
EXAM_DAY = '2026-11-14'

# ---------- 規則參數（頁面上會照這裡寫出來）----------
FREQ_HI, FREQ_MID = 4, 2      # 歷屆出現 ≥4 次 +2；2–3 次 +1
LONG_GAP = 5                  # 已隔 ≥5 屆 +1
TIER_HI, TIER_MID = 3, 2      # 總分 ≥3 高；=2 中；≤1 低

# ---------- 主題定義（名稱／技術規則條號範圍／對應選擇題章別）----------
TOPICS = [
 ('T01', '建物折舊（定額・定率・償債基金）', '折舊', [(65, 69)], ['C2']),
 ('T02', '成本法：重建／重置成本、總成本與營造施工費', '總成本', [(48, 64)], ['C1']),
 ('T03', '土地開發分析法', '土開法', [(70, 82)], ['E1']),
 ('T04', '比較法：比較標的取捨、供需圈與調整', '比較法', [(18, 27)], ['B']),
 ('T05', '收益法：資本化率之決定', '資本化率', [(43, 43)], ['D2']),
 ('T06', '收益法：直接資本化、DCF、淨收益與殘餘法', '收益DCF', [(28, 42), (44, 47)], ['D1', 'D3']),
 ('T07', '租金估計', '租金', [(129, 133)], ['F1']),
 ('T08', '估價作業程序、資料蒐集、勘察與報告書', '程序報告', [(8, 13), (16, 17)], ['A4']),
 ('T09', '估價方法之選取與三大方法基礎', '方法選取', [(14, 15), (18, 18), (28, 28), (48, 48)], ['A4']),
 ('T10', '價格種類與影響價格因素', '價格因素', [(2, 2), (6, 6)], ['A2', 'A3']),
 ('T11', '估價原則（替代・變動・最有效使用等）', '估價原則', [], ['A1']),
 ('T12', '宗地估價：合併分割、特殊宗地與土地改良物', '宗地改良', [(83, 97), (107, 113)], ['H1H2', 'I2J1']),
 ('T13', '房地估價：區分所有、樓層效用與房地拆算', '房地估價', [(98, 106)], ['G1']),
 ('T14', '權利估價與都更權利變換', '權利估價', [(114, 128)], ['H3I1']),
]
TN = {t[0]: t for t in TOPICS}
TYPE_NAME = {'cost': '成本法', 'land': '土地開發', 'comp': '比較法', 'income': '收益法', 'rent': '租金', 'foundation': '基礎・程序', 'principle': '估價原則'}
CN = {'1': '一', '2': '二'}

def law_chapters(path):
    cache = os.path.join(HERE, 'law_chapters.json')
    if path and os.path.exists(path):
        heads, cur = [], None
        for line in open(path, encoding='utf-8'):
            m = re.match(r'##\s+(.+)', line)
            if m: cur = m.group(1).strip().replace('　', ' '); continue
            m = re.match(r'\*\*第\s*(\d+)\s*條', line)
            if m and cur:
                n = int(m.group(1))
                if heads and heads[-1][0] == cur: heads[-1][2] = n
                else: heads.append([cur, n, n])
        # 「第二節 收益法」這類節名補上章名
        chap = ''
        for h in heads:
            m = re.match(r'(第.章\s*\S+)', h[0]);
            if m and '第' in h[0][:1]: chap = m.group(1)
            if h[0].startswith('第二節') or h[0].startswith('第三節') or h[0].startswith('第四節'):
                h[0] = chap + ' ' + h[0]
        json.dump(heads, open(cache, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
        return heads, os.path.basename(path)
    return json.load(open(cache, encoding='utf-8')), 'law_chapters.json（快取）'

def chap_of(n, heads):
    for name, a, b in heads:
        if a <= n <= b: return name
    return None

def secs(tags):
    out = []
    for t in tags:
        for a, b in re.findall(r'§(\d+)(?:[-之]\d+)?(?:\s*[–～~]\s*§?(\d+))?', t):
            out.append(int(a))
    return out

def main():
    lawp = LAW_DEFAULT
    if '--law' in sys.argv: lawp = sys.argv[sys.argv.index('--law') + 1]
    heads, law_src = law_chapters(lawp)
    # ---------- 卡片 ----------
    soup = BeautifulSoup(open(os.path.join(ROOT, SRC), encoding='utf-8').read(), 'html.parser')
    tmap = json.load(open(os.path.join(HERE, 'topic_map.json'), encoding='utf-8'))
    cards, warn = [], []
    for c in soup.select('div.essay-card[id]'):
        cid = c['id']
        title = c.select_one('.card-title').get_text(' ', strip=True)
        tags = [t.get_text(strip=True) for t in c.select('.card-meta .tag') if 'tag-smock' not in (t.get('class') or [])]
        pi = c.select_one('.pred-info')
        basis = re.sub(r'^🔮\s*預測依據：\s*', '', pi.get_text(' ', strip=True)) if pi else ''
        m = re.match(r'e(\d+)-(\d)$', cid)
        if m: kind, y, no = 'off', int(m.group(1)), CN[m.group(2)]
        elif cid.startswith('pred-'): kind, y, no = 'pred', None, None
        elif cid.startswith('mk-ls'): kind, y, no = 'ls', None, None
        elif cid.startswith('mk-'): kind, y, no = 'site', None, None
        else: kind, y, no = 'other', None, None
        yr = c.select_one('.card-year')
        lab = yr.get_text(' ', strip=True) if yr else ''
        if kind == 'off': label = f'{y}-{no}'
        elif kind == 'pred': label = '預測' + re.search(r'【115預測(.)】', title).group(1) if '【115預測' in title else cid
        else:
            mm = re.search(r'｜(.+?申論.)', lab); label = mm.group(1).replace(' ', '') if mm else cid
        title_clean = re.sub(r'^【115預測.】', '', title)
        if cid in tmap: tp, auto = tmap[cid], False
        else:
            s = secs(tags); tp = []
            for n in s:
                for t in TOPICS:
                    if any(a <= n <= b for a, b in t[3]): tp = [t[0]]; break
                if tp: break
            tp = tp or ['T09']; auto = True; warn.append(f'{cid} 未在 topic_map.json，依 § 自動歸 {tp[0]}')
        # 條號是否落在主題範圍（只提示，不改歸類）
        rng = [r for t in tp for r in TN[t][3]]
        s = secs(tags)
        if rng and s and not any(a <= n <= b for n in s for a, b in rng):
            warn.append(f'{cid} 標籤條號 {s} 不在 {tp} 範圍內（人工歸類，保留）')
        cards.append(dict(id=cid, kind=kind, y=y, no=no, label=label, t=title_clean, tags=tags,
                          type=c.get('data-type', ''), basis=basis, tp=tp, auto=auto))
    off = [c for c in cards if c['kind'] == 'off']
    LAST = max(c['y'] for c in off); FIRST = min(c['y'] for c in off)
    years = list(range(FIRST, LAST + 1))
    nyears = len(years)
    # ---------- 選擇題 ----------
    js = subprocess.run(['node', '-e', 'global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.BXV_QUIZ.items.map(x=>[x.ch,x.y])))',
                         os.path.join(ROOT, 'bxv-quiz-data.js')], capture_output=True, text=True, check=True).stdout
    items = json.loads(js)
    q_all = [x for x in items if x[1]]
    R5 = LAST - 4
    q5 = [x for x in q_all if x[1] >= R5]
    # ---------- 主題指標 ----------
    T = []
    for code, name, short, rng, qch in TOPICS:
        qs = [c for c in off if code in c['tp']]
        ys = sorted({c['y'] for c in qs})
        n = len(qs)
        last = max(ys) if ys else None
        since = (LAST - last) if ys else None
        avg = round((ys[-1] - ys[0]) / (len(ys) - 1), 1) if len(ys) >= 2 else None
        m_all = sum(1 for x in q_all if x[0] in qch); m5 = sum(1 for x in q5 if x[0] in qch)
        rng_txt = '、'.join(f'§{a}' if a == b else f'§{a}–§{b}' for a, b in rng) or '技術規則多未明文（學理）'
        chs = []
        for a, b in rng:
            for k in (a, b):
                ch = chap_of(k, heads)
                if ch and ch not in chs: chs.append(ch)
        T.append(dict(code=code, name=name, short=short, rng=rng_txt, chs=chs, qch=qch, n=n, years=ys, last=last,
                      since=since, avg=avg, m_all=m_all, m5=m5,
                      cards=[c['id'] for c in cards if c['tp'][0] == code],
                      sec=[c['id'] for c in cards if code in c['tp'][1:]]))
    med = statistics.median([t['m5'] for t in T])
    for t in T:
        pts = []
        f = 2 if t['n'] >= FREQ_HI else (1 if t['n'] >= FREQ_MID else 0)
        pts.append(['歷屆考過 %d 次' % t['n'], f])
        if t['avg'] is not None and t['since'] >= t['avg']:
            pts.append(['已隔 %d 屆 ≥ 平均間隔 %s 年（到期）' % (t['since'], t['avg']), 1])
        if t['since'] is not None and t['since'] >= LONG_GAP:
            pts.append(['已隔 %d 屆（≥%d，久未考）' % (t['since'], LONG_GAP), 1])
        if t['since'] == 0:
            pts.append(['%d 年剛考過' % LAST, -1])
        if t['m5'] >= med:
            pts.append(['近 5 年選擇題 %d 題 ≥ 中位數 %s' % (t['m5'], ('%g' % med)), 1])
        else:
            pts.append(['近 5 年選擇題 %d 題 < 中位數 %s' % (t['m5'], ('%g' % med)), 0])
        t['pts'] = pts
        t['score'] = sum(p[1] for p in pts)
        t['tier'] = '高' if t['score'] >= TIER_HI else ('中' if t['score'] >= TIER_MID else '低')
    TO = {'高': 0, '中': 1, '低': 2}
    T.sort(key=lambda t: (TO[t['tier']], -t['score'], -t['n'], -(t['since'] if t['since'] is not None else -1), t['code']))
    # 每主題卡片排序：官方（新→舊）→ 本站預測 → 本站模擬卷 → 補習班
    KO = {'off': 0, 'pred': 1, 'site': 2, 'ls': 3, 'other': 4}
    CB = {c['id']: c for c in cards}
    def ck(cid):
        c = CB[cid]; return (KO[c['kind']], -(c['y'] or 0), int(re.sub(r'\D', '', cid) or 0))
    for t in T:
        t['cards'].sort(key=ck); t['sec'].sort(key=ck)
    tier_cards = {k: sum(len(t['cards']) for t in T if t['tier'] == k) for k in '高中低'}
    tier_topics = {k: sum(1 for t in T if t['tier'] == k) for k in '高中低'}
    # ---------- 網格 ----------
    grid = []
    for t in T:
        row = {}
        for c in off:
            if t['code'] in c['tp']:
                row.setdefault(str(c['y']), []).append([c['id'], c['no'], 0 if c['tp'][0] == t['code'] else 1, c['t']])
        grid.append(row)
    D = dict(years=years, last=LAST, r5=R5, med=med, topics=T, grid=grid, exam=EXAM_DAY,
             cards={c['id']: dict(k=c['kind'], l=c['label'], t=c['t'], y=c['y'], no=c['no'], ty=c['type'], b=c['basis'], tp=c['tp'], tags=c['tags'], auto=c['auto']) for c in cards},
             nq=len(q_all), nq5=len(q5), nyears=nyears)
    cnt = {k: sum(1 for c in cards if c['kind'] == k) for k in ('off', 'pred', 'site', 'ls')}
    # 篇別統計（官方）
    ty_all = {}; ty5 = {}
    for c in off:
        ty_all[c['type']] = ty_all.get(c['type'], 0) + 1
        if c['y'] >= R5: ty5[c['type']] = ty5.get(c['type'], 0) + 1
    ty_line = '、'.join(f'{TYPE_NAME.get(k, k)} <span class="num">{v}</span>' for k, v in sorted(ty_all.items(), key=lambda kv: -kv[1]))
    ty5_line = '、'.join(f'{TYPE_NAME.get(k, k)} <span class="num">{ty5.get(k, 0)}</span>' for k, v in sorted(ty_all.items(), key=lambda kv: -kv[1]))
    zero = [t for t in T if t['n'] == 0]
    hi = [t for t in T if t['tier'] == '高']
    # ---------- 輸出 ----------
    fab = ''
    if os.path.exists(TPL_PAGE):
        s = open(TPL_PAGE, encoding='utf-8').read()
        if '<!--bxfab-->' in s:
            fab = s[s.index('<!--bxfab-->'):s.index('<!--/bxfab-->') + len('<!--/bxfab-->')]
            fab = fab.replace('%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html',
                              '%E4%BC%B0%E5%83%B9%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html')
            assert '%E4%BC%B0%E5%83%B9' in fab
    page = open(os.path.join(HERE, 'page_tpl.html'), encoding='utf-8').read()
    def chip(i, t): return f'<a class="nchip" href="#t-{t["code"]}">{"①②③④⑤⑥"[i]} {html.escape(t["short"])}</a>'
    rep = {
        '%%NCARDS%%': str(len(cards)), '%%NOFF%%': str(cnt['off']), '%%NPRED%%': str(cnt['pred']),
        '%%NSITE%%': str(cnt['site']), '%%NLS%%': str(cnt['ls']), '%%NQ%%': str(len(q_all)), '%%NQ5%%': str(len(q5)),
        '%%FIRST%%': str(FIRST), '%%LAST%%': str(LAST), '%%R5%%': str(R5), '%%NY%%': str(nyears),
        '%%NT%%': str(len(T)), '%%NHI%%': str(tier_topics['高']), '%%NMID%%': str(tier_topics['中']), '%%NLO%%': str(tier_topics['低']),
        '%%CHI%%': str(tier_cards['高']), '%%CMID%%': str(tier_cards['中']), '%%CLO%%': str(tier_cards['低']),
        '%%CHIPS%%': ''.join(chip(i, t) for i, t in enumerate(hi[:3])),
        '%%TYLINE%%': ty_line, '%%TY5LINE%%': ty5_line,
        '%%ZERO%%': '、'.join(html.escape(t['short']) for t in zero) or '無',
        '%%NZERO%%': str(len(zero)),
        '%%MED%%': '%g' % med, '%%FREQ_HI%%': str(FREQ_HI), '%%FREQ_HI1%%': str(FREQ_HI - 1), '%%FREQ_MID%%': str(FREQ_MID), '%%LONG%%': str(LONG_GAP),
        '%%TIER_HI%%': str(TIER_HI), '%%TIER_MID%%': str(TIER_MID),
        '%%LAWSRC%%': html.escape(law_src), '%%BUILT%%': datetime.date.today().isoformat(),
        '%%DATA%%': json.dumps(D, ensure_ascii=False).replace('</', '<\\/'), '%%FAB%%': fab,
    }
    for k, v in rep.items(): page = page.replace(k, v)
    assert '%%' not in page, re.findall(r'%%\w+%%', page)
    open(OUT, 'w', encoding='utf-8').write(page)
    # ---------- 報告 ----------
    print(f'卡片 {len(cards)}（官方 {cnt["off"]}／預測 {cnt["pred"]}／本站卷 {cnt["site"]}／補習班 {cnt["ls"]}）；選擇題官方 {len(q_all)}、近5年 {len(q5)}；中位數 {med}')
    for t in T:
        print(f"{t['tier']} {t['score']:>2} {t['code']} {t['short']:<8} n={t['n']} yrs={t['years']} since={t['since']} avg={t['avg']} m5={t['m5']} cards={len(t['cards'])}")
    print('各等級主題', tier_topics, '卡片（主歸類）', tier_cards)
    for w in warn: print('提示：', w)
    assert len(off) == 2 * nyears, f'官方題數 {len(off)} 與年數不符'
    print('寫出', OUT)

if __name__ == '__main__':
    main()
