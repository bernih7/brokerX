# -*- coding: utf-8 -*-
"""估價「申論 5 分鐘衝刺」頁（改自經紀法規 tools/essay_jj/sprint/build_sprint.py）。內容一字不改，只換呈現方式。
用法：python3 tools/essay_val/sprint/build_sprint.py     （可重跑；卡數、題數一律從資料算）
資料來源（與經紀法規不同）：
- 卡片：《不動產估價概要_申論題實戰範文.html》的 <div class="essay-card…" id data-pri data-type>（題目 .q-box、考場速寫 .quick-ans、考場版 .exam-ver）
- 考場版四塊：範文頁內嵌 .exam-ver（由 tools/essay_val/exam/exam_ver.json 注入）；頁面沒有時改讀 exam_ver.json
- 關鍵檢核 checks／口訣 mnem／推理鏈 subs／得分關鍵詞 kw：tools/essay_val/lj_data.json
- 來源分類：e 開頭＝官方、pred＝預測、mk-c＝本站模擬卷、mk-ls＝補習班模擬卷；data-pri A＝必考，其餘＝參考
紀錄（估價自己的鍵）：bxv-es-log（輪數／秒數／自評 ok・mem・hard，與範文頁共用）＋ bxv-es-sprint（每次練習；推理版加 f:'r'）；
已讀 bx-essay-read（陣列）。缺邏輯拆解資料的卡（目前補習班卷 mk-ls1、mk-ls2）不列入，執行時會列出。"""
import os, re, json, html, sys
import sys as _s, os as _o; _s.path.insert(0, _o.path.normpath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), '..', '..'))); import sprint_hp as _hp  # 115 高／中機率排序（11-03）
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
PAGE = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html')
KINDS = (('mk-c', 'mkc', '本站模擬卷'), ('mk-ls', 'mkls', '補習班模擬卷'), ('pred', 'pred', '預測'))

def clean(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()
def md(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t, quote=False))
def kind_of(cid):
    if re.match(r'e\d', cid): return 'off', '官方'
    for p, k, lab in KINDS:
        if cid.startswith(p): return k, lab
    return 'other', '其他'

def div_body(s, start):
    """s[start] 是 '<div'；回傳 (內容, 結束位置)"""
    d = 0
    for m in re.finditer(r'<(/?)div\b[^>]*>', s[start:]):
        d += -1 if m.group(1) else 1
        if d == 0:
            o = s.find('>', start) + 1; return s[o:start + m.start()], start + m.end()
    raise ValueError('div 不平衡')

def ev_from_json(blocks):
    """exam_ver.json 的 [標題, 內文（<br> 分行）] → 與範文頁相同的 evb 呈現（逐點分行）"""
    out = []
    for h, body in blocks:
        lines = [x.strip() for x in body.split('<br>') if x.strip()]
        out.append('<span class="blk-l">%s</span><p>%s</p>' % (h, ''.join('<span class="evli">%s</span>' % x for x in lines) if len(lines) > 1 else body))
    return out

def load():
    page = open(PAGE, encoding='utf-8').read()
    LJ = {x['k']: x for x in json.load(open(os.path.join(ROOT, 'tools/essay_val/lj_data.json'), encoding='utf-8'))}
    EVJ = json.load(open(os.path.join(ROOT, 'tools/essay_val/exam/exam_ver.json'), encoding='utf-8'))
    TN = {m.group(1): m.group(2) for m in re.finditer(r'data-type="(\w+)"[^>]*onclick="setChip\(this,\'type\'\)">([^（<]+)', page)}
    ms = list(re.finditer(r'<div class="essay-card([^"]*)"[^>]*\bid="([^"]+)"[^>]*>', page))
    cards, skip = [], []
    for n, m in enumerate(ms):
        cid = m.group(2); tag = m.group(0)
        c = page[m.start():(ms[n + 1].start() if n + 1 < len(ms) else len(page))]
        pri = (re.search(r'data-pri="([^"]*)"', tag) or [None, ''])[1]; typ = (re.search(r'data-type="([^"]*)"', tag) or [None, ''])[1]
        k, klab = kind_of(cid)
        lj = LJ.get(cid)
        if not lj or not lj.get('checks') or not lj.get('subs'):
            skip.append((cid, '沒有邏輯拆解資料（lj_data.json）')); continue
        # 考場版
        b = []
        i = c.find('<div class="exam-ver">')
        if i >= 0:
            ev, _ = div_body(c, i)
            for bm in re.finditer(r'<div class="evb e\d">', ev):
                body, _ = div_body(ev, bm.start())
                hm = re.match(r'<b class="evh">(.*?)</b>', body, re.S)
                b.append('<span class="blk-l">%s</span>%s' % (hm.group(1), body[hm.end():]) if hm else body)
        elif cid in EVJ:
            b = ev_from_json(EVJ[cid])
        if len(b) != 4:
            skip.append((cid, '考場版不是四塊（%d）' % len(b))); continue
        # 題目（保留換行）
        qm = re.search(r'<div class="q-box">(.*?)</div>', c, re.S)
        q = qm.group(1) if qm else ''
        q = re.sub(r'<br\s*/?>', '\n', q)
        q = '\n'.join(re.sub(r'[ \t　]+', ' ', html.unescape(re.sub(r'<[^>]+>', '', ln))).strip() for ln in q.split('\n'))
        q = re.sub(r'\n{2,}', '\n', q).strip(); q = re.sub(r'^【[^】]*】\s*', '', q)
        ym = re.search(r'<span class="card-year[^"]*">(.*?)</span>', c, re.S); year = clean(ym.group(1)) if ym else ''
        seg = [x.strip() for x in year.split('｜')]  # 官方「🔴 A級｜105年第一題」、預測「🔮 115預測㉑｜B級」、模擬卷「📗 本站模擬卷｜綜合模擬卷一 申論一｜🔴 A級」
        no = seg[-1] if k == 'off' else (seg[0].replace('🔮', '').strip() if k == 'pred' else (seg[1] if len(seg) > 1 else seg[0]))
        t = clean(re.search(r'<div class="card-title">(.*?)</div>', c, re.S).group(1)); t = re.sub(r'^【[^】]*】\s*', '', t)
        tier = {'A': 0, 'B': 1, 'C': 2}.get(pri, 3)
        lv = klab + '・' + ('必考' if pri == 'A' else '參考') + ('（%s級）' % pri if pri in 'ABC' and pri else '')
        cards.append({'id': cid, 'no': no or cid, 't': t, 'lv': lv, 'k': k, 'tier': tier, 'g': TN.get(typ, typ), 'q': q,
                      'nq': len(lj['subs']) or 1, 'b': b, 'ck': [{'x': x['txt'], 'h': bool(x.get('hot'))} for x in lj['checks']],
                      'mn': lj.get('mnem', ''), '_c': c, '_lj': lj})
    return cards, skip

if __name__ == '__main__':
    cards, skip = load()
    SP = [{f: c[f] for f in ('id', 'no', 't', 'lv', 'k', 'tier', 'g', 'q', 'nq', 'b', 'ck', 'mn')} for c in cards]
    tpl = open(os.path.join(H, 'tpl.html'), encoding='utf-8').read()
    assert '/*__DATA__*/[]' in tpl
    open(os.path.join(ROOT, '估價_申論5分鐘衝刺.html'), 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/[]', json.dumps(_hp.tag(SP, 'val'), ensure_ascii=False)))
    from collections import Counter
    print('衝刺', len(SP), '張；檢核項', sum(len(c['ck']) for c in SP), dict(Counter(c['k'] for c in SP)))
    if skip: print('⚠ 未列入：', skip)
