# -*- coding: utf-8 -*-
"""本站自擬模擬卷（卷④全真、卷⑤缺口補強、申論專練卷①）共 7 題申論收進指揮中心申論分頁（es-mk3～es-mk9）。
內容取自各卷頁面 D.E（完整四段式 parts、考場速寫 v、得分關鍵詞／失分點、口訣 m），一字不改。
之後依序跑：gen_lj.py（邏輯拆解）→ exam_ver/build_ev.py（考場版）→ split_sx_lists.py → sprint/*。
可重跑：先移除 es-mk3～es-mk9 與分組標籤再插入。"""
import io, json, os, re, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
M = json.load(open(os.path.join(H, 'mock2.json'), encoding='utf-8'))
PK = {'es-mk3': 'a', 'es-mk4': 'e', 'es-mk5': 'e', 'es-mk6': 'g', 'es-mk7': 'a', 'es-mk8': 'a', 'es-mk9': 'c'}
NUM = {'es-mk3': '模三', 'es-mk4': '模四', 'es-mk5': '模五', 'es-mk6': '模六', 'es-mk7': '模七', 'es-mk8': '模八', 'es-mk9': '模九'}
TITLE = {
 'es-mk3': '雙方代理未得書面同意、超收服務報酬與收取差價',
 'es-mk4': '區分所有權人屢違規約：管委會處理與強制出讓',
 'es-mk5': '漏水修繕：專有、共用與樓地板管線的責任與費用',
 'es-mk6': '斡旋金未告知要約書、預售屋先付定金才給審閱',
 'es-mk7': '不動產說明書簽章解說流程',
 'es-mk8': '公平交易法廣告查核分工原則（加盟店代銷）',
 'es-mk9': '115.1.13 不動產說明書修正',
}
def esc(t): return html.escape(t, quote=False)
def paras(t): return ''.join('<p>%s</p>' % esc(x) for x in t.split('\n') if x.strip())
def sk(parts): return '<div class="sk">' + ''.join('<h4>%s</h4>%s' % (esc(h), paras(t)) for h, t in parts) + '</div>'

def card(o):
    cid = o['eid']; pk = PK[cid]
    src = ('<p class="mksrc"><b>來源分類</b>　本站自擬模擬卷：<a href="%s" target="_blank" rel="noopener">%s</a>・%s。'
           '內容與該卷擬答相同（同一份資料）。</p>' % (o['src'], o['srclab'], esc(o['t'].split('｜')[0])))
    key = ('<div class="kw-box"><b>閱卷關鍵詞</b><div class="kws">' + ''.join('<span class="kw">%s</span>' % esc(w) for w in o['kws'])
           + '</div></div><div class="losebox"><b>常見失分點</b><ul>' + ''.join('<li>%s</li>' % esc(x) for x in o['lose']) + '</ul></div>'
           + ('<div class="kou"><b>口訣</b> %s <small>〔自編〕</small></div>' % esc(o['m']) if o['m'] else ''))
    chips = ''.join('<span class="kc">%s</span>' % esc(w) for w in o['kws'][:4])
    return ('<details id="%s" class="essay-detail mock pk-%s"><summary class="es-sum"><span class="es-top"><span class="essay-num">%s</span>'
            '<span class="es-t">模擬試題｜%s</span></span><span class="es-meta"><span class="es-lv mock">本站模擬卷</span>%s</span></summary>'
            '<div class="essay-body"><p class="essay-question"><b>【模擬試題（本站・%s・%s）】</b> %s</p>%s'
            '<div class="vtabs"><button type="button" class="vt on" data-v="1">考場速寫</button><button type="button" class="vt" data-v="0">完整四段式</button></div>'
            '<div class="vp" data-v="1">%s</div><div class="vp" data-v="2">%s</div><div class="vp" data-v="0" hidden>%s</div>'
            '</div><label class="esdone"><input type="checkbox" class="esrd"> 我已讀懂這題的邏輯</label></details>'
            % (cid, pk, NUM[cid], TITLE[cid], chips, o['srclab'], esc(o['t'].split('｜')[0]), esc(o['q']), src, sk(o['quick']), key, sk(o['full'])))

s = io.open(HUB, encoding='utf-8').read()
GL = '<div class="group-label">本站模擬卷（%d 題）</div>'
s = re.sub(r'<div class="group-label">本站模擬卷（\d+ 題）</div>', '', s)
for o in M:
    m = re.search(r'<details id="%s"[\s\S]*?(?=<div class="group-label">|<details id="es-|</div><div class="ess-panel"|</div>\s*</section>)' % o['eid'], s)
    if m: s = s[:m.start()] + s[m.end():]
by = {}
for o in M: by.setdefault(PK[o['eid']], []).append(o)
for k, lst in by.items():
    pm = re.search(r'<div class="ess-panel" data-k="%s"[^>]*>' % k, s); assert pm, k
    gm = re.search(r'<div class="group-label">預測題[^<]*</div>', s[pm.end():]); assert gm, k
    p = pm.end() + gm.start()
    s = s[:p] + GL % len(lst) + ''.join(card(o) for o in lst) + s[p:]
io.open(HUB, 'w', encoding='utf-8').write(s)
print('插入', sum(len(v) for v in by.values()), '張；篇別', {k: len(v) for k, v in by.items()})
