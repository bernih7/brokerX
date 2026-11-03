# -*- coding: utf-8 -*-
"""民法「申論 5 分鐘衝刺」＋「5 分鐘・推理版」：從指揮中心申論卡產生（改自經紀法規 tools/essay_jj/sprint/）。內容一字不改，只換呈現方式。
用法：python3 tools/essay_civ/sprint/build_sprint.py
- 衝刺（考場版）：卡片考場版四塊＋ lj_data.json 的關鍵檢核 checks（模擬卷卡的邏輯拆解只有 HTML，從 HTML 讀回）。
- 推理版：邏輯拆解推理鏈＋考場速寫（四段、口訣、得分關鍵詞、失分點）；得分關鍵詞是條號者用 kw_cn.json 的中文代表（程式發現仍有條號就中止）。
紀錄與指揮中心同步：bxm-es-log（輪數／秒數／自評，與申論卡共用）＋ bxm-es-sprint（每次衝刺；推理版加 f:'r'）。"""
import os, re, json, html, sys
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
from sprint_sx_law import annotate  # 速寫法條塊：條號＋本題名稱（11-03）
_f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sx_law_names.json'); SXN = json.load(open(_f, encoding='utf-8')) if os.path.exists(_f) else {}
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
hub = open(os.path.join(ROOT, '民法_備考指揮中心.html'), encoding='utf-8').read()
LJ = {x['k']: x for x in json.load(open(os.path.join(ROOT, 'tools/essay_civ/lj_data.json'), encoding='utf-8'))}
GN = {'g1': '共有・分管・區分所有', 'g2': '抵押權・地上權・物權順序', 'g3': '無權處分・善意取得・登記', 'g4': '居間・委任・買賣・租賃', 'g5': '意思表示・行為能力・債總', 'g6': '時效・相鄰・親屬繼承'}
HIGH = {'預01', '預02', '預03', '預05', '預07', '預15', '預20', '預21', '預22', '預24', '預25', '預26', '預29', '預38', '預40'}
def clean(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
def md(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t, quote=False))

def lj_from_html(h):
    """模擬卷卡：邏輯拆解只有 HTML（gen_lj render 的輸出），讀回 subs／checks／mnem。"""
    A = h[h.find('<div class="ljp" data-lj="A">'):h.find('<div class="ljp" data-lj="B"')]
    C = h[h.find('<div class="ljp" data-lj="C"'):]
    keys = [clean(x) for x in re.findall(r'<li><span class="ljno">\d+</span>(.*?)</li>', C)]
    subs = []; n = 0
    for part in re.split(r'(?=<div class="ljq">)', A)[1:]:
        q = clean(re.search(r'<span class="ljqt">(.*?)</span>', part).group(1))
        pre = re.search(r'<div class="ljar ljpre">(.*?)</div>', part)
        steps = []
        for m in re.finditer(r'<div class="ljst">(.*?)</div>(?:<div class="ljar">(.*?)</div>)?', part, re.S):
            b, link = m.group(1), m.group(2) or ''
            ask = clean(re.sub(r'<span class="ljno">\d+</span>', '', re.search(r'<div class="ljsq">(.*?)$', b, re.S).group(1).split('</div>')[0]))
            law = re.search(r'<span class="ljt tl">條文</span><b>(.*?)</b>：(.*?)</p>', b, re.S)
            fact = re.search(r'<span class="ljt tf">本題</span>(.*?)</p>', b, re.S)
            res = re.search(r'<span class="ljt ta">小結</span>(.*?)</p>', b, re.S)
            steps.append({'ask': ask, 'key': keys[n] if n < len(keys) else '', 'lawh': clean(law.group(1)) if law else '', 'law': clean(law.group(2)) if law else '',
                          'facth': '', 'fact': clean(fact.group(1)) if fact else '', 'res': clean(res.group(1)) if res else '', 'link': clean(re.sub(r'^↓\s*', '', clean(link)))})
            n += 1
        ans = re.search(r'<div class="ljans"><b>答[一二三四五]?：</b>(.*?)</div>', part, re.S)
        subs.append({'q': q, 'pre': clean(pre.group(1)) if pre else '', 'steps': steps, 'ans_html': ans.group(1) if ans else ''})
    checks = []
    for m in re.finditer(r'<li><label><input type="checkbox"><span class="ljt (\w+)">[^<]*</span>(.*?)</label>', C, re.S):
        t = m.group(2); checks.append({'txt': clean(re.sub(r'<span class="ljhot">.*?</span>', '', t)), 'hot': 'ljhot' in t})
    mn = re.search(r'<div class="kou"><b>口訣</b>\s*(.*?)</div>', A, re.S)
    return {'subs': subs, 'checks': checks, 'mnem': clean(mn.group(1)) if mn else ''}

def seg(c, a_mark, enders):
    a = c.find(a_mark); e = min([x for x in (c.find(t, a + 10) for t in enders) if x > 0] or [len(c)]); return c[a:e]

cards = []
ms = list(re.finditer(r'<details class="essay[^"]*" data-lv="(\w)" data-key="([^"]+)" data-yr="[^"]*" data-g="(g\d)"', hub))
for n, m in enumerate(ms):
    lv, k, g = m.groups()
    c = hub[m.start():(ms[n + 1].start() if n + 1 < len(ms) else len(hub))]
    a = c.find('<div class="vp ev" data-v="4" hidden>'); b = c.find('<!--/ev-->', a)
    if a < 0: sys.exit('缺考場版 ' + k)
    ev = c[a + len('<div class="vp ev" data-v="4" hidden>'):b]; ev = ev[:ev.rfind('</div>')]
    blocks = re.findall(r'<div class="evb e(\d)"><b class="evh">(.*?)</b>(.*?)</div>(?=<div class="evb e\d">|$)', ev, re.S)
    assert len(blocks) == 4, (k, len(blocks))
    blk = ['<span class="blk-l">%s</span>%s' % (h, body.replace('class="evph"', 'class="evh"')) for _, h, body in blocks]
    oq = re.search(r'<div class="oq">(.*?)</div>', c, re.S); q = re.sub(r'^【[^】]*】\s*', '', clean(re.sub(r'<br>.*$', '', oq.group(1), flags=re.S)))
    lj = LJ.get(k)
    if not lj:
        lh = seg(c, '<div class="vp" data-v="3"', ['<label class="done">']); lj = lj_from_html(lh)
    kind = 'off' if lv in 'ABC' else ('mock' if lv == 'M' else 'pred')
    tier = {'A': 0, 'B': 1, 'C': 2}.get(lv, 0 if k in HIGH else (1 if lv == 'P' else 2))
    no = clean(re.search(r'<span class="ek">(.*?)</span>', c).group(1))
    sx = seg(c, '<div class="vp" data-v="1"', ['<div class="vp" data-v="3"', '<div class="vp" data-v="0"', '<label class="done">'])
    sxb = [('b%d' % int(x[0]), clean(x[1]), x[2]) for x in re.findall(r'<div class="blk b(\d)"><h5>(.*?)</h5>(.*?)</div>(?=<div class="blk|<div class="kou|<div class="sk2)', sx, re.S)]
    kou = re.search(r'<div class="kou"><b>口訣[^<]*</b>(.*?)</div>', sx, re.S)
    sk2 = sx[sx.find('<div class="sk2">'):]
    kws = [clean(x) for x in re.findall(r'<i>(.*?)</i>', sk2[:sk2.find('</div>')])] if '<div class="sk2">' in sx else []
    lose = [clean(x) for x in re.findall(r'<li>(.*?)</li>', sk2)]
    subs = []
    for s_ in lj['subs']:
        subs.append({'q': s_['q'], 'pre': s_.get('pre', ''), 'ans': s_['ans_html'] if 'ans_html' in s_ else md(s_.get('ans', '')),
                     'st': [{f: st.get(f, '') for f in ('ask', 'key', 'lawh', 'law', 'facth', 'fact', 'res', 'link')} for st in s_['steps']]})
    cards.append({'id': k, 'no': no, 't': clean(re.search(r'<b class="et">(.*?)</b>', c).group(1)), 'lv': '', 'k': kind, 'tier': tier, 'g': GN.get(g, ''),
                  'q': q, 'nq': len(subs) or 1, 'b': blk, 'ck': [{'x': x['txt'], 'h': bool(x.get('hot'))} for x in lj.get('checks', [])],
                  'mn': lj.get('mnem', ''), 'subs': subs, 'sx': [[x[0], x[1], annotate(x[2], [st for s_ in subs for st in s_['st']], SXN)[0] if x[1].strip() == '法條' else x[2]] for x in sxb], 'kou': clean(kou.group(1)) if kou else '', 'kws': kws, 'lose': lose,
                  'href': '民法_備考指揮中心.html#essay=' + k})
miss = [c['id'] for c in cards if not c['ck'] or not c['subs'] or not c['sx'] or not c['kws']]
assert not miss, ('資料不全', miss)

KWCN = json.load(open(os.path.join(H, 'kw_cn.json'), encoding='utf-8')) if os.path.exists(os.path.join(H, 'kw_cn.json')) else {}
ART = re.compile(r'§|第\s*\d+\s*條')
todo = {}
for c in cards:
    m = KWCN.get(c['id'], {}); out = []
    for kw in c['kws']:
        if kw in m:
            if m[kw] is None: continue
            out.append({'c': m[kw], 'a': kw})
        else: out.append({'c': kw, 'a': ''})
    bad = [x['c'] for x in out if ART.search(x['c'])]
    if bad: todo[c['id']] = bad
    c['kwr'] = out
json.dump(todo, open(os.path.join(H, 'kw_todo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

SP = [{f: c[f] for f in ('id', 'no', 't', 'lv', 'k', 'tier', 'g', 'q', 'nq', 'b', 'ck', 'mn')} for c in cards]
tpl = open(os.path.join(H, 'tpl.html'), encoding='utf-8').read()
open(os.path.join(ROOT, '民法_申論5分鐘衝刺.html'), 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/[]', json.dumps(SP, ensure_ascii=False)))
print('衝刺', len(SP), '張；檢核項', sum(len(c['ck']) for c in SP))
if todo:
    print('⚠ 關鍵詞仍是條號、尚無中文代表（寫入 kw_todo.json）：', sum(len(v) for v in todo.values()), '項／', len(todo), '張；推理版未產生'); sys.exit(1)
RS = [{'id': c['id'], 'no': c['no'], 't': c['t'], 'g': c['g'], 'q': c['q'], 'subs': c['subs'], 'sx': c['sx'], 'kou': c['kou'], 'kws': c['kwr'], 'lose': c['lose'], 'k': c['k'], 'tier': c['tier']} for c in cards]
tr = open(os.path.join(H, 'tpl_reason.html'), encoding='utf-8').read()
open(os.path.join(ROOT, '民法_申論5分鐘_推理版.html'), 'w', encoding='utf-8').write(tr.replace('/*__DATA__*/[]', json.dumps(RS, ensure_ascii=False)).replace('/*__DEMO__*/false', 'false').replace('__ROOT__', ''))
print('推理版', len(RS), '張')
