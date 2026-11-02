# -*- coding: utf-8 -*-
"""民法條文覆蓋盤點補漏（比照土地法 v562「考過補漏」框）。
官方 520 題 law 欄考過 ≥2 題、但 13 支整理頁都沒寫到條號的條文 → 依章節放進四份《彩色重點速記》對應段落末尾。
條文逐字取自 tools/civ_quiz/law.json（兩網站比對），不另寫解說；題號連到《民法_法條解析練習》#q= 直接作答。
可重跑：先拿掉舊的 <!--cov-->…<!--/cov--> 再掃描、插入。"""
import io, json, os, re, html, collections
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
E = html.escape
qs = json.load(io.open(os.path.join(H, 'quiz_data.json'), encoding='utf-8'))['q']
LAW = json.load(io.open(os.path.join(H, 'law.json'), encoding='utf-8'))
cnt = collections.defaultdict(list); chs = collections.defaultdict(collections.Counter)
for q in qs:
    for a in q.get('law') or []: cnt[a].append(q['k']); chs[a][q['ch']] += 1
PAGES = ['民法A_彩色重點速記', '民法BC_彩色重點速記', '民法D_彩色重點速記', '民法E_彩色重點速記', '民法_債之發生與移轉', '民法_共有專區', '民法_抵押權總整理',
         '民法_數字期間速查', '民法_法律效果總整理', '民法_物權變動與登記', '民法_繼承專區', '民法_用詞分類與申論必背', '民法_定義填空練習']
COVRX = re.compile(r'\n?<!--cov-->.*?<!--/cov-->', re.S)
SRC = {p: COVRX.sub('', io.open(os.path.join(R, p + '.html'), encoding='utf-8').read()) for p in PAGES}
def base(a): return int(a.split('-')[0])
have = set()
NUM = r'(\d{1,4})(?:\s*(?:-|之)\s*(\d{1,2}))?'
PAT = [re.compile(r'§\s*' + NUM + r'(?:\s*[～~至]\s*§?\s*' + NUM + ')?'),
       re.compile(r'第\s*' + NUM.replace('(?:-|之)', '之') + r'\s*條(?:\s*[～~至]\s*第?\s*' + NUM + r'\s*條)?'),
       re.compile(r'(?<![\d.§])' + NUM + r'(?:\s*[～~至]\s*' + NUM + r')?\s*條')]
for p, s in SRC.items():
    t = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)))
    for rx in PAT:
        for m in rx.finditer(t):
            g = m.groups(); a1, s1 = g[0], g[1]; a2 = g[2] if len(g) > 2 else None
            have.add(a1 + ('-' + s1 if s1 else ''))
            if s1 and int(s1) > int(a1) and base(a1) < 100:  # 「69-70條」＝區間
                have.update(str(x) for x in range(int(a1), int(s1) + 1))
            if a2 and 0 <= int(a2) - int(a1) < 40: have.update(str(x) for x in range(int(a1), int(a2) + 1))
miss = [a for a in cnt if a not in have and len(cnt[a]) >= 2 and a in LAW]

def section(a):
    n = base(a); ch = chs[a].most_common(1)[0][0]
    if ch[0] == 'A': return '民法A_彩色重點速記', 'sec-a' + ch[1]
    if ch[0] in 'BC': return '民法BC_彩色重點速記', 'sec-' + ch[0].lower()
    if ch[0] == 'D':
        for lo, hi, sid in [(757, 816, 'd1'), (817, 831, 'd2'), (832, 850, 'd3'), (851, 859, 'd4'), (860, 883, 'd5'), (884, 910, 'd6'), (911, 927, 'd7'), (940, 966, 'd8')]:
            if lo <= n <= hi: return '民法D_彩色重點速記', 'sec-' + sid
        return '民法D_彩色重點速記', 'sec-d1'
    for lo, hi, sid in [(967, 971, 'e1'), (972, 1003, 'e2'), (1004, 1048, 'e5'), (1049, 1058, 'e3'), (1059, 1137, 'e4'), (1138, 1185, 'e6'), (1186, 1225, 'e7')]:
        if lo <= n <= hi: return '民法E_彩色重點速記', 'sec-' + sid
    return '民法E_彩色重點速記', 'sec-e1'
BY = collections.defaultdict(list)
for a in miss: BY[section(a)].append(a)
CIRC = dict(zip('ⅠⅡⅢⅣⅤⅥⅦ', '①②③④⑤⑥⑦'))
QA = '%E6%B0%91%E6%B3%95_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html#q='
def item(a):
    ks = sorted(cnt[a], key=lambda k: (-int(k.split('-')[0]), int(k.split('-')[1])))
    lines = []
    for ln in LAW[a]['x'].split('\n'):
        ln = ln.strip()
        if ln and ln[0] in CIRC: ln = CIRC[ln[0]] + ' ' + ln[1:].strip()
        if ln: lines.append(ln)
    head = re.sub(r'\s+', '', lines[0])[:22] + ('…' if len(re.sub(r'\s+', '', lines[0])) > 22 else '')
    return ('<details class="covi"><summary><span class="covart">§%s</span><span class="covh">%s</span><span class="covn">考過 %d 題</span></summary>'
            '<div class="covb">%s<p class="covq">%s<a class="covall" target="_blank" rel="noopener" href="%s%s">一起練這 %d 題 →</a></p></div></details>') % (
        a, E(head), len(ks), ''.join('<p>%s</p>' % E(x) for x in lines),
        ''.join('<a target="_blank" rel="noopener" href="%s%s">%s</a>' % (QA, k, k) for k in ks), QA, ','.join(ks), len(ks))
CSS = ('<style id="cov-css">.cov{margin:14px 0}.cov .covd{font-size:.82rem;color:var(--ink-soft);margin:4px 0 6px}'
       '.covi{border-top:1px dashed var(--rule);padding:4px 0}.covi>summary{cursor:pointer;display:flex;flex-wrap:wrap;gap:4px 8px;align-items:baseline;list-style:none;padding:3px 0}'
       '.covi>summary::-webkit-details-marker{display:none}.covi>summary::before{content:"＋";color:var(--ink-soft);font-size:.8rem}.covi[open]>summary::before{content:"－"}'
       '.covart{color:var(--ink-soft);font-weight:400}.covh{flex:1;min-width:0}.covn{font-size:.76rem;font-weight:700;color:var(--gold);white-space:nowrap}'
       '.covb p{margin:4px 0;line-height:1.75}.covq{display:flex;flex-wrap:wrap;gap:4px 6px;font-size:.8rem}'
       '.covq a{border:1px solid var(--rule);border-radius:99px;padding:0 8px;text-decoration:none;color:var(--ink)}.covq a.covall{border-color:var(--gold);color:var(--gold);font-weight:700}</style>')
out = collections.Counter()
for p in ['民法A_彩色重點速記', '民法BC_彩色重點速記', '民法D_彩色重點速記', '民法E_彩色重點速記']:
    s = SRC[p]
    s = re.sub(r'<style id="cov-css">.*?</style>', '', s, flags=re.S)
    for (pp, sid), arts in sorted(BY.items()):
        if pp != p: continue
        arts.sort(key=lambda a: (base(a), a))
        i = s.index('id="%s"' % sid)
        j = s.find('<div class="section-div"', i + 10)
        if j < 0: j = s.index('<!-- ================= 紅色地雷清單', i)
        c = s.rfind('<!-- =', i, j)
        if c > 0: j = c
        box = ('<!--cov--><div class="note note-orange cov"><span class="tag">🟠 考過補漏</span>'
               '<p class="covd">歷屆選擇題考過 2 題以上、本站整理頁原本沒寫到的條文（%d 條）。條文逐字取自條文庫；題號點了另開分頁直接作答。</p>%s</div><!--/cov-->\n') % (len(arts), ''.join(item(a) for a in arts))
        s = s[:j] + box + s[j:]; out[p] += len(arts)
    s = s.replace('</head>', CSS + '</head>', 1)
    io.open(os.path.join(R, p + '.html'), 'w', encoding='utf-8').write(s)
print('補漏條文', len(miss), dict(out))
print({k: v for k, v in sorted((('%s#%s' % k, len(v)) for k, v in BY.items()))})
