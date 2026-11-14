# -*- coding: utf-8 -*-
"""11-14：模一～模九「完整四段式」從舊的 div.sk 壓縮段落，改成與其他 66 張相同的四色塊（定義／法條／涵攝／結論＋考試陷阱）。
定義段一律引條文（逐字對 lawfull.json）；涵攝、結論取自已審過的邏輯拆解 lj_data.json（每問：條文→本題→小結）；
考試陷阱取 lj 檢核中標「hot」的項目。原本的「這題要背的條文」移進法條塊。可重跑（已是 blk 版者略過）。"""
import os, re, json, html
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
H = os.path.join(R, '經紀法規_備考指揮中心.html'); hub = open(H, encoding='utf-8').read()
LJ = {x['k']: x for x in json.load(open(os.path.join(R, 'tools/essay_jj/lj_data.json'), encoding='utf-8'))}
LAW = json.load(open(os.path.join(R, 'tools/essay_jj/law/lawfull.json'), encoding='utf-8'))
def law(k, n=None):
    t = LAW[k]['text']
    if n is None: return t
    m = re.search(r'(?m)^%s、(.+)$' % n, t); assert m, (k, n); return m.group(1)

DEF = {
 'es-mk1': [('仲介業務', '經紀業條例§4⑤', law('經紀業條例 §4', '五').replace('︰', '：')),
            ('經紀業', '經紀業條例§4④', law('經紀業條例 §4', '四').replace('︰', '：')),
            ('經紀人員', '經紀業條例§4⑦', law('經紀業條例 §4', '七').replace('︰', '：')),
            ('經營經紀業之許可', '經紀業條例§5Ⅰ', '經營經紀業者，應向主管機關申請許可後，依法辦理公司或商業登記。')],
 'es-mk2': [('定型化契約條款', '消保法§2⑦', law('消保法 §2', '七')),
            ('定型化契約', '消保法§2⑨', law('消保法 §2', '九'))],
 'es-mk3': [('差價', '經紀業條例§4⑨', law('經紀業條例 §4', '九').replace('︰', '：')),
            ('雙方代理', '經紀業條例§24之2本文', '經營仲介業務者經買賣或租賃雙方當事人之書面同意，得同時接受雙方之委託。'),
            ('禁收差價', '經紀業條例§19Ⅰ前段', '經紀業或經紀人員不得收取差價或其他報酬。')],
 'es-mk4': [('住戶', '公寓大廈§3⑧', law('公寓大廈 §3', '八')),
            ('區分所有', '公寓大廈§3②', law('公寓大廈 §3', '二'))],
 'es-mk5': [('專有部分', '公寓大廈§3③', law('公寓大廈 §3', '三')),
            ('共用部分', '公寓大廈§3④', law('公寓大廈 §3', '四'))],
 'es-mk6': [('事業', '公平法§2Ⅰ', '公司、獨資或合夥之工商行號、其他提供商品或服務從事交易之人或團體。'),
            ('欺罔或顯失公平', '公平法§25', LAW['公平法 §25']['text'])],
 'es-mk7': [('不動產說明書之簽章', '經紀業條例§22Ⅰ⑤', '不動產之買賣、互易、租賃或代理銷售，如委由經紀業仲介或代銷者，不動產說明書應由經紀業指派經紀人簽章。'),
            ('解說義務', '經紀業條例§23Ⅰ', LAW['經紀業條例 §23']['text'].split('\n')[0]),
            ('應記載及不得記載事項', '經紀業條例§22Ⅲ', '第一項第五款之不動產說明書應記載及不得記載事項，由中央主管機關定之。')],
 'es-mk8': [('廣告', '不動產經紀業廣告處理原則第二點', LAW['廣告處理原則 §2點']['text'].split('\n')[-1].lstrip('二、').replace('本處理原則所稱廣告，指', ''))],
 'es-mk9': [('不動產說明書之簽章', '經紀業條例§22Ⅰ⑤', '不動產之買賣、互易、租賃或代理銷售，如委由經紀業仲介或代銷者，不動產說明書應由經紀業指派經紀人簽章。'),
            ('應記載及不得記載事項', '經紀業條例§22Ⅲ', '第一項第五款之不動產說明書應記載及不得記載事項，由中央主管機關定之。')],
}
CN = '一二三四五六七八'
def md(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html.escape(t or '', quote=False))
def build(cid, lawwrap):
    x = LJ[cid]
    b1 = '<div class="blk b1"><span class="blk-l">定義</span>' + ''.join(
        '<p><b>%s</b>：%s（%s）</p>' % (html.escape(n), html.escape(re.sub(r'^' + re.escape(n) + r'[：︰]', '', t).rstrip('。')) + '。', html.escape(src)) for n, src, t in DEF[cid]) + '</div>'
    laws = []
    for s in x['subs']:
        for st in s['steps']:
            h = (st.get('lawh') or '').strip()
            if h and h not in laws: laws.append(h)
    b2 = '<div class="blk b2"><span class="blk-l">法條</span><p><b>法條：</b>%s。</p>%s</div>' % ('；'.join(html.escape(l) for l in laws), lawwrap)
    b3 = '<div class="blk b3"><span class="blk-l">涵攝分析</span>'
    b4 = '<div class="blk b4"><span class="blk-l">結論</span>'
    for i, s in enumerate(x['subs']):
        tag = '問%s' % CN[i] if len(x['subs']) > 1 else '本題'
        b3 += '<p><b>%s　%s</b></p>' % (tag, html.escape(s['q']))
        if s.get('pre'): b3 += '<p>%s</p>' % md(s['pre'])
        b3 += '<ol>'
        for st in s['steps']:
            parts = []
            if st.get('lawh'): parts.append('依<b>%s</b>：%s' % (html.escape(st['lawh']), md(st.get('law'))))
            elif st.get('law'): parts.append(md(st['law']))
            if st.get('fact'): parts.append('本題%s' % md(st['fact']))
            if st.get('res'): parts.append('故%s' % md(st['res']))
            b3 += '<li>%s</li>' % '<br>'.join(parts)
        b3 += '</ol>'
        b4 += '<p>%s%s</p>' % ('（%s）' % CN[i] if len(x['subs']) > 1 else '', md(s['ans']))
    b3 += '</div>'; b4 += '</div>'
    hot = [c['txt'] for c in x.get('checks', []) if c.get('hot')]
    b5 = ('<div class="blk b5"><span class="blk-l">考試陷阱</span><ul>%s</ul></div>' % ''.join('<li>%s</li>' % md(t) for t in hot)) if hot else ''
    return '<div class="vp" data-v="0" hidden>' + b1 + b2 + b3 + b4 + b5 + '</div>'

def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()

def plain(h):
    h = re.sub(r'<div class="lawwrap">.*?</details></div>', '', h, flags=re.S)
    h = re.sub(r'<span class="blk-l">([^<]+)</span>', r'\n【\1】\n', h)
    h = re.sub(r'</(p|li)>', '\n', h); h = h.replace('<br>', '\n')
    return re.sub(r'\n+', '\n', html.unescape(re.sub(r'<[^>]+>', '', h))).strip()

E = os.path.join(R, 'tools/essay_jj/essays.json'); ES = json.load(open(E, encoding='utf-8'))
done = []
for n in range(1, 10):
    cid = 'es-mk%d' % n
    i = hub.find('<details id="%s"' % cid); a = hub.find('<div class="vp" data-v="0"', i); b = div_end(hub, a)
    old = hub[a:b]
    if 'class="sk"' not in old: continue
    lw = re.search(r'<div class="lawwrap">.*</details></div>', old, re.S)
    new = build(cid, lw.group(0) if lw else '')
    hub = hub[:a] + new + hub[b:]; done.append(cid)
    for e in (ES if isinstance(ES, list) else ES.values()):
        if isinstance(e, dict) and e.get('eid') == cid:
            if 'full' in e: e['full'] = plain(new)
open(H, 'w', encoding='utf-8').write(hub)
open(E, 'w', encoding='utf-8').write(json.dumps(ES, ensure_ascii=False, indent=1) + ('\n' if open(E, encoding='utf-8').read().endswith('\n') else ''))
print('改', done)
