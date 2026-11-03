# -*- coding: utf-8 -*-
"""《估價_申論專練卷》限時申論套卷（比照民法／經紀法規申論專練卷：每題 25 分鐘，2 題＝50 分鐘）。
不新寫題目：題目一律取自《不動產估價概要_申論題實戰範文.html》現有申論卡（.q-box 原題），對答案＝iframe 嵌入《估價_申論卡.html#卡號》
（嵌入／接高度比照 tools/essay_val/patch_mock_pages.py：postMessage {bxvCard,h}）。
組卷規則（頁面「怎麼組卷」同步顯示，數字由本腳本算）：
  1. 偏計算＝該卡邏輯拆解為「一步一步算」（範文頁 lj-panel 的 .ljd）；其餘＝偏說明。
  2. 價值排序：A級＞B級＞C級＞補習班卷（M）；同級：官方＞115預測＞本站模擬卷＞補習班卷；官方題年份新者優先；再依範文頁順序。
  3. 計算題位：依價值排序挑 N 題；同級時，已用次數少的篇別優先（輪流）。
  4. 說明題位：先替「計算題沒蓋到的篇別」各挑一題（該篇別價值最高者），其餘依價值排序補滿（同級時篇別用得少的先）。
  5. 配卷：卷序＝計算題順序；每卷配價值最高、且與計算題不同篇別的說明題。
紀錄：交卷寫 bxv-es-log（與範文頁共用：n 輪數 +1、s 最近5輪秒數、tot、t、自評 v=ok/mem/hard）；本頁 bxv-es-drill（每卷完成次數、日期、自評）。
用法：python3 tools/essay_val/drill/build_drill.py      （可重跑；卡片新增或改等級後重跑即重新組卷）"""
import os, re, json, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
SRC = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html')
OUT = os.path.join(ROOT, '估價_申論專練卷.html')
TPL = os.path.join(H, 'tpl.html')
N = 7                       # 卷數（6～8）
LIMIT_MIN = 50              # 每卷分鐘（2 題 × 25 分鐘，比照民法／經紀法規專練卷 75 分鐘 3 題）
PRI_R = {'A': 0, 'B': 1, 'C': 2}
KIND = (('mk-c', 'mkc', '本站模擬卷', 2), ('mk-ls', 'mkls', '補習班模擬卷', 3), ('pred', 'pred', '115預測', 1))


def clean(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()


def div_end(s, a):
    d = 0
    for m in re.finditer(r'<(/?)div\b', s[a:]):
        d += -1 if m.group(1) else 1
        if d == 0:
            return s.find('>', a + m.end()) + 1
    raise SystemExit('div 不平衡')


def kind_of(cid):
    if re.match(r'e\d', cid): return 'off', '官方', 0
    for p, k, lab, r in KIND:
        if cid.startswith(p): return k, lab, r
    return 'other', '其他', 4


def load():
    s = open(SRC, encoding='utf-8').read()
    TN = {m.group(1): m.group(2).strip() for m in re.finditer(r'data-type="(\w+)"[^>]*onclick="setChip\(this,\'type\'\)">([^（<]+)', s)}
    TN.pop('all', None)
    ms = list(re.finditer(r'<div class="essay-card([^"]*)"[^>]*\bid="([^"]+)"[^>]*>', s))
    cards = []
    for n, m in enumerate(ms):
        cid, tag = m.group(2), m.group(0)
        c = s[m.start():div_end(s, m.start())]
        pri = (re.search(r'data-pri="([^"]*)"', tag) or [0, ''])[1]
        typ = (re.search(r'data-type="([^"]*)"', tag) or [0, ''])[1]
        k, klab, kr = kind_of(cid)
        qa = c.find('<div class="q-box">'); assert qa >= 0, cid
        q = c[qa + len('<div class="q-box">'):div_end(c, qa) - len('</div>')]
        q = re.sub(r'<div class="mk-src">.*?</div>', '', q, flags=re.S)
        q = re.sub(r'^\s*<strong>【[^】]*】</strong>', '', q)
        q = re.sub(r'<br\s*/?>', '\n', q)
        q = '\n'.join(re.sub(r'[ \t　]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', ln))).strip() for ln in q.split('\n'))
        q = re.sub(r'\n{2,}', '\n', q).strip()
        ym = re.search(r'<span class="card-year[^"]*">(.*?)</span>', c, re.S); seg = [x.strip() for x in clean(ym.group(1)).split('｜')] if ym else ['']
        no = seg[-1] if k == 'off' else (seg[0].replace('🔮', '').strip() if k == 'pred' else (seg[1] if len(seg) > 1 else seg[0]))
        no = re.sub(r'^[^\w（(]+', '', no)
        t = re.sub(r'^【[^】]*】\s*', '', clean(re.search(r'<div class="card-title">(.*?)</div>', c, re.S).group(1)))
        ljd = re.search(r'<p class="ljd">(.*?)</p>', c, re.S)
        calc = bool(ljd and '一步一步算' in ljd.group(1))
        yr = int(re.match(r'e(\d+)', cid).group(1)) if k == 'off' else 0
        cards.append(dict(id=cid, pri=pri, ty=typ, tn=TN.get(typ, typ), k=k, kl=klab, no=no, t=t, q=q, calc=calc,
                          key=(PRI_R.get(pri, 3), kr, -yr, n)))
    return cards, TN


def assemble(cards, TN):
    calc = sorted([c for c in cards if c['calc']], key=lambda c: c['key'])
    expl = sorted([c for c in cards if not c['calc']], key=lambda c: c['key'])
    use = {}
    def pick(pool, n):
        out = []
        for _ in range(n):
            c = min((c for c in pool if c not in out), key=lambda c: (c['key'][0], use.get(c['ty'], 0)) + c['key'][1:])
            out.append(c); use[c['ty']] = use.get(c['ty'], 0) + 1
        return out
    C = pick(calc, N)
    miss = [t for t in TN if t not in {c['ty'] for c in C}]
    E = [min((c for c in expl if c['ty'] == t), key=lambda c: c['key']) for t in miss if any(c['ty'] == t for c in expl)]
    for c in E: use[c['ty']] = use.get(c['ty'], 0) + 1
    assert len(E) <= N, '計算題沒蓋到的篇別比卷數多'
    E += pick([c for c in expl if c not in E], N - len(E))
    E.sort(key=lambda c: c['key'])
    papers, left = [], list(E)
    for c in C:
        e = next((x for x in left if x['ty'] != c['ty']), None)
        if e is None:                       # 剩下的都同篇別：和前面的卷交換
            e = left[0]
            for p in papers:
                if p[1]['ty'] != c['ty'] and e['ty'] != p[0]['ty']:
                    p[1], e = e, p[1]; left.remove(p[1]); left.append(e); break
        left.remove(e); papers.append([c, e])
    cov = {x['ty'] for p in papers for x in p}
    assert cov == set(TN), ('篇別未全涵蓋', set(TN) - cov)
    return papers


def main():
    cards, TN = load()
    papers = assemble(cards, TN)
    used = {x['id'] for p in papers for x in p}
    D = {c['id']: {k: c[k] for k in ('pri', 'ty', 'tn', 'k', 'kl', 'no', 't', 'q', 'calc')} for c in cards if c['id'] in used}
    P = [{'id': '+'.join(x['id'] for x in p), 'q': [x['id'] for x in p]} for p in papers]
    nc = sum(c['calc'] for c in cards)
    stat = '範文頁現有 %d 張卡（官方 %d、115預測 %d、本站模擬卷 %d、補習班卷 %d）；偏計算 %d 張、偏說明 %d 張；篇別 %d 個（%s）。' % (
        len(cards), sum(c['k'] == 'off' for c in cards), sum(c['k'] == 'pred' for c in cards), sum(c['k'] == 'mkc' for c in cards),
        sum(c['k'] == 'mkls' for c in cards), nc, len(cards) - nc, len(TN), '、'.join(TN.values()))
    t = open(TPL, encoding='utf-8').read()
    js = lambda o: json.dumps(o, ensure_ascii=False).replace('</', '<\\/')
    t = t.replace('/*__CARDS__*/{}', js(D)).replace('/*__PAPERS__*/[]', js(P)).replace('/*__LIMIT__*/3000', str(LIMIT_MIN * 60))
    t = t.replace('__STAT__', html.escape(stat)).replace('__N__', str(N)).replace('__MIN__', str(LIMIT_MIN)).replace('__HALF__', str(LIMIT_MIN // 2))
    assert '__' not in re.sub(r'<script[\s\S]*?</script>', '', t).replace('__proto__', ''), '模板有未替換的佔位'
    open(OUT, 'w', encoding='utf-8').write(t)
    print(os.path.basename(OUT), '：%d 卷，每卷 %d 分鐘' % (len(P), LIMIT_MIN))
    print(stat)
    for i, p in enumerate(papers):
        print('卷%d' % (i + 1), '｜'.join('%s %s %s級 %s %s' % ('算' if x['calc'] else '說', x['tn'], x['pri'], x['id'], x['t'][:24]) for x in p))


if __name__ == '__main__':
    main()
