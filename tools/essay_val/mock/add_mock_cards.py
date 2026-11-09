# -*- coding: utf-8 -*-
"""施工單《申論統一》第一節：綜合模擬卷一～五尚未收的 7 題申論收進《不動產估價概要_申論題實戰範文》。
- 位置：各篇「官方題」之後、「補習班模擬卷／預測題」之前；虛線框；膠囊「本站模擬卷」
- 完整四段式＝卷頁擬答原文（src_*.json 的 ans_html，一字不改）；邏輯拆解／考場速寫／考場版取自 out_*.json
- 計數全部改由頁面實際卡片計算（kind() 加 smock；頁首、頁尾總數改成 JS 填）；bxv-use.js TOT.essay 依頁面卡數重寫
可重跑：已存在的新卡先整張移除再插入。之後依序跑 exam/inject.py、split_sx_lists.py。"""
import json, os, re, sys, glob, html
H = os.path.dirname(os.path.abspath(__file__)); EV = os.path.dirname(H); ROOT = os.path.normpath(os.path.join(EV, '..', '..'))
sys.path.insert(0, EV)
import gen_lj
PAGE = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html')
LJ = os.path.join(EV, 'lj_data.json'); EXV = os.path.join(EV, 'exam', 'exam_ver.json'); USE = os.path.join(ROOT, 'bxv-use.js')
CN = '一二三四五'
def div_end(s, i):
    d = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        d += 1 if m.group(0).startswith('<div') else -1
        if d == 0: return i + m.end()
    raise ValueError('div 不平衡')
PRI = {'A': ('tier-a', '🔴 A級'), 'B': ('tier-b', '🟡 B級'), 'C': ('tier-c', '🟢 C級')}
def card(src, out):
    cid = src['id']; n = CN.index(re.search(r'模擬卷(.)', src['src']).group(1)); k = src['idx']
    lab = '綜合模擬卷%s 申論%s' % (CN[n], '一二'[k])
    tags = ''.join('<span class="tag">%s</span>' % html.escape(t) for t in out['tags'][:5])
    q = re.sub(r'^\s*[一二]、', '', src['q_html'].strip())
    return ('<div class="essay-card smock" id="%s" data-pri="%s" data-type="%s" data-src="%s">\n'
            '  <div class="card-header" onclick="toggleCard(this)">\n    <div class="card-header-left">\n'
            '      <div><span class="card-year tier-s">📗 本站模擬卷｜%s｜%s</span></div>\n'
            '      <div class="card-title">%s</div>\n      <div class="card-meta">%s<span class="tag tag-smock">本站模擬卷</span></div>\n    </div>\n'
            '    <button class="read-btn" id="rbtn-%s" onclick="event.stopPropagation();toggleRead(\'%s\')">☐ 已讀</button>\n'
            '    <span class="card-arrow">▼</span>\n  </div>\n'
            '  <div class="card-body"><div class="q-box"><strong>【%s】</strong> %s</div>'
            '<div class="quick-ans">%s</div><div class="detail-content"><div class="smock-ans">%s</div></div></div>\n</div>\n'
            ) % (cid, out['pri'], src['group'], src['src'], lab, PRI[out['pri']][1], html.escape(out['title']), tags,
                 cid, cid, lab, q, out['quick_html'], src['ans_html'])
CSS = '''<style id="smock-css">
.essay-card.smock{border:1.5px dashed var(--found)!important}
.tier-s{background:color-mix(in srgb,var(--found) 18%,transparent);color:var(--found);border:1px solid var(--found)}
.tag.tag-smock{background:transparent;border:1px dashed var(--found);color:var(--found)}
:is(.essay-card.mock,.essay-card.smock) .ans-block{background:var(--paper2);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-top:8px;font-size:.92rem;line-height:1.9}
:is(.essay-card.mock,.essay-card.smock) .ans-block h4{color:var(--primary);margin:12px 0 4px;font-size:.95rem}
:is(.essay-card.mock,.essay-card.smock) .ans-block h4:first-child{margin-top:0}
:is(.essay-card.mock,.essay-card.smock) .ans-block p{margin:4px 0}
:is(.essay-card.mock,.essay-card.smock) .cbox{display:flex;flex-direction:column;gap:6px;border-left-width:1px}
:is(.essay-card.mock,.essay-card.smock) .cbox .kf-eq{display:flex;flex-wrap:nowrap;align-items:center;gap:6px 8px;overflow-x:auto}
:is(.essay-card.mock,.essay-card.smock) .cbox .kf-eq>*{flex:0 0 auto}
</style>'''
def main():
    s = open(PAGE, encoding='utf-8').read()
    srcs = {json.load(open(p, encoding='utf-8'))['id']: json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(H, 'src_*.json')))}
    outs = {}
    for cid in srcs:
        p = os.path.join(H, 'out_%s.json' % cid)
        if not os.path.exists(p): sys.exit('缺 ' + p)
        outs[cid] = json.load(open(p, encoding='utf-8'))
    # 移除舊的新卡
    for cid in srcs:
        a = s.find('<div class="essay-card smock" id="%s"' % cid)
        if a >= 0: s = s[:a] + s[div_end(s, a):].lstrip('\n')
    # 插入
    for cid, src in srcs.items():
        g = s.find('<details class="tgroup" data-g="%s"' % src['group']); assert g >= 0, src['group']
        ge = s.find('</details>', g)
        cands = [x for x in (s.find('<div class="essay-card" data-v="lj" id="pred-', g), s.find('<div class="essay-card mock"', g)) if 0 <= x < ge]
        # 同篇已插入的本站模擬卷排在一起（依卷號）
        sm = [m.start() for m in re.finditer(r'<div class="essay-card smock[^"]*"[^>]*id="([^"]+)"', s[g:ge])]
        later = [g + p for p in sm if re.search(r'id="([^"]+)"', s[g + p:g + p + 200]).group(1) > cid]
        at = min(later + cands) if (later + cands) else s.rfind('</div>', g, ge)
        blk = gen_lj.convert(card(src, outs[cid]), outs[cid]['lj'])
        s = s[:at] + blk + s[at:]
    if 'id="smock-css"' in s: s = re.sub(r'<style id="smock-css">.*?</style>', CSS, s, flags=re.S)
    else: s = s.replace('</head>', CSS + '\n</head>', 1)
    # 計數：kind() 分出 smock；頁首／頁尾總數改 JS 填
    s = s.replace("(c.classList.contains('mock')?'mock':'other')", "(c.classList.contains('smock')?'smock':(c.classList.contains('mock')?'mock':'other'))")
    s = s.replace("var n={all:cards.length,off:0,pred:0,mock:0}", "var n={all:cards.length,off:0,pred:0,mock:0,smock:0}")
    s = s.replace("set('s-mock',n.mock);", "set('s-mock',n.mock);set('s-smock',n.smock);document.querySelectorAll('.h-tot').forEach(function(e){e.textContent='官方'+n.off+'題＋本站模擬'+n.smock+'題＋補習班模擬'+n.mock+'題＋預測'+n.pred+'題'});")
    s = s.replace("var cs=g.querySelectorAll('.essay-card[id]'),pr=0,mk=0;cs.forEach(function(c){var k=kind(c);if(k==='pred')pr++;if(k==='mock')mk++;});",
                  "var cs=g.querySelectorAll('.essay-card[id]'),pr=0,mk=0,sm=0;cs.forEach(function(c){var k=kind(c);if(k==='pred')pr++;if(k==='mock')mk++;if(k==='smock')sm++;});")
    s = s.replace("var x=[];if(pr)x.push('預測'+pr);if(mk)x.push('補習班'+mk);", "var x=[];if(sm)x.push('本站模擬'+sm);if(mk)x.push('補習班'+mk);if(pr)x.push('預測'+pr);")
    s = re.sub(r'官方\d+題＋(?:本站模擬\d+題＋)?補習班模擬\d+題＋預測\d+題', lambda m: m.group(0), s)
    s = re.sub(r'(?<!class="h-tot">)官方\d+題＋(?:本站模擬\d+題＋)?補習班模擬\d+題＋預測\d+題', lambda m: '<span class="h-tot">%s</span>' % m.group(0), s)
    if 'id="s-smock"' not in s:
        s = s.replace('<span class="stat-chip">補習班 <strong id="s-mock">', '<span class="stat-chip">本站模擬卷 <strong id="s-smock">0</strong></span>\n  <span class="stat-chip">補習班 <strong id="s-mock">', 1)
    # 靜態數字也先依實際卡片寫好（JS 失效時仍正確）
    ids = re.findall(r'<div class="essay-card([^"]*)"[^>]*\bid="([^"]+)"', s)
    off = sum(1 for c, i in ids if re.match(r'e\d', i)); pred = sum(1 for c, i in ids if i.startswith('pred-'))
    sm = sum(1 for c, i in ids if 'smock' in c); mk = sum(1 for c, i in ids if 'mock' in c.split() and 'smock' not in c)
    tot = len(ids); txt = '官方%d題＋本站模擬%d題＋補習班模擬%d題＋預測%d題' % (off, sm, mk, pred)
    s = re.sub(r'<span class="h-tot">[^<]*</span>', '<span class="h-tot">%s</span>' % txt, s)
    s = re.sub(r'(id="s-total">)\d+', r'\g<1>%d' % tot, s); s = re.sub(r'(id="s-smock">)\d+', r'\g<1>%d' % sm, s)
    open(PAGE, 'w', encoding='utf-8').write(s)
    # lj_data／exam_ver 也收錄（給 5 分鐘練習、單卡檢視用）
    d = json.load(open(LJ, encoding='utf-8')); d = [x for x in d if x['k'] not in srcs] + [outs[c]['lj'] for c in srcs]
    json.dump(d, open(LJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ev = json.load(open(EXV, encoding='utf-8'))
    for c in srcs: ev[c] = outs[c]['exam']
    json.dump(ev, open(EXV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    u = open(USE, encoding='utf-8').read()
    u = re.sub(r'essay:\d+', 'essay:%d' % tot, u, count=1)
    u = re.sub(r'（官方 ?\d+ ?＋[^）]*預測 ?\d+）', '（官方 %d＋本站模擬 %d＋補習班模擬 %d＋預測 %d）' % (off, sm, mk, pred), u, count=1)
    open(USE, 'w', encoding='utf-8').write(u)
    print('插入', len(srcs), '張；總數', tot, txt)
if __name__ == '__main__': main()
