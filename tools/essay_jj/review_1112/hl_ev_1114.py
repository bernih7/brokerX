# -*- coding: utf-8 -*-
"""11-14 使用者：「我就說要參考其他科目了 怎沒黃底粗體重點」——經紀法規考場版比照民法／估價加 <mark> 黃底粗體。
規則（依全科日誌 v811 共識：期限、比例、金額、法律效果、主體義務）：每個涵攝小點、意義、結論各標 1～2 處；
只標正文（例／理由不標），不標條號。直接寫進 exam_ver/ev_*.json（之後跑 build_ev.py）。可重跑（已有 <mark> 的段落略過）。"""
import os, re, json, glob
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'exam_ver')
N = r'[\d,.一二三四五六七八九十百千萬兩]+'
PAT = [
    ('amt', re.compile(r'(?:新臺幣)?' + N + r'萬?元以上' + N + r'萬?元以下(?:之)?(?:罰鍰|罰金)?')),
    ('eff', re.compile(r'(?:應於加計利息後)?加倍返還(?:支付人)?|負連帶(?:損害)?賠償責任|連帶(?:損害)?賠償責任|其(?:定型化契約)?條款無效|條款無效|不生效力|仍構成契約之內容|不構成契約之內容|視為[^，。；：、（）]{2,14}|廢止其(?:許可|經紀人員證書或證明)|應予申誡|停止執行業務|停止營業處分|推定顯失公平|禁止其營業|限期令停止、改正')),
    ('per', re.compile(r'(?:於|自)?[^，。；：、（）]{0,8}?' + r'[\d一二三四五六七八九十]+\s*(?:個月|日|年|小時|名)(?:內|以上|以下|後|為限)?(?:[^，。；：（）]{0,40})')),
    ('frac', re.compile(r'[^，。；：、（）]{0,10}[一二三四五六七八九十]分之[一二三四五六七八九十](?:以上)?[^，。；：（）]{0,40}')),
    ('must', re.compile(r'(?:應經|須經|應由|不得|始得|應先)[^，。；：（）]{2,40}')),
    ('ext', re.compile(r'受償順序與第一順位抵押權同|得聲請法院拍賣|得訴請法院[^，。；：（）]{2,24}|得請求[^，。；：（）]{2,20}|應負[^，。；：（）]{0,10}責任|應即回收[^，。；：（）]{0,10}|[一二三五]倍以下|契約無效|得隨時以書面終止|連選得連任一次|至少應置[^，。；：（）]{2,14}|不列入[^，。；：（）]{0,12}|仍得認定[^，。；：（）]{0,12}|不適用|準用[^，。；：（）]{2,20}|與民事確定判決有同一之效力|免繳裁判費|週年利率百分之五|不含[^，。；：（）]{2,14}|不包括[^，。；：（）]{2,10}|屬第25條之顯失公平行為|違反第\d+條|應以書面[^，。；：（）]{2,20}|為公寓大廈之管理負責人|應予改善或回復原狀|應受該規約或決議之限制|應即[^，。；：（）]{2,16}|得報請[^，。；：（）]{2,16}|應置[^，。；：（）]{2,12}')),
]
FALL = re.compile(r'指([^，。；：（）]{4,28})')
def mark(text, k):
    if '<mark>' in text: return text
    # 只處理正文：切掉 例：／理由在於 之後
    m = re.search(r'(?:。|；|」)\s*(?:例：|理由在於)', text)
    body, tail = (text[:m.start() + 1], text[m.start() + 1:]) if m else (text, '')
    spans = []
    for kind, rx in PAT:
        for mm in rx.finditer(body):
            s, e = mm.span()
            if kind in ('per', 'frac'):   # 從所在子句開頭標起，不從字中間切
                s = max(body.rfind(c, 0, s) for c in '，。；：、（「') + 1
            seg = body[s:e].strip('，、 ')
            seg = re.sub(r'^(?:並|且|而|即|故|則)', '', seg)
            if len(seg) < 3 or len(seg) > 30 or (kind != 'ext' and re.search(r'第\s*\d+\s*條', seg)) or re.search(r'<|[①-⑳]', seg): continue
            s = body.find(seg, s)
            if any(not (e2 <= s or s + len(seg) <= s2) for s2, e2 in spans): continue
            spans.append((s, s + len(seg)))
            break
        if len(spans) >= k: break
    if not spans:   # 定義句：標「指」後的定義內容
        fm = FALL.search(body)
        if fm and not re.search(r'第\s*\d+\s*條|[①-⑳]', fm.group(1)): spans.append(fm.span(1))
    for s, e in sorted(spans, reverse=True):
        body = body[:s] + '<mark>' + body[s:e] + '</mark>' + body[e:]
    return body + tail
n = 0
for f in glob.glob(os.path.join(H, 'ev_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for cid, rows in d.items():
        for r in rows:
            h, p = r
            if h.startswith('三'):
                r[1] = '<br>'.join(mark(x, 2) if re.match(r'（[一二三四五六七八九十]+）', x.strip()) else x for x in p.split('<br>'))
            elif h.startswith('四'): r[1] = mark(p, 2)
            elif h.startswith('一'): r[1] = mark(p, 1)
            n += r[1].count('<mark>') - p.count('<mark>')
    out = '{\n' + ',\n'.join(json.dumps(k, ensure_ascii=False) + ': [\n' + ',\n'.join(json.dumps(r, ensure_ascii=False) for r in v) + '\n]' for k, v in d.items()) + '\n}\n'
    open(f, 'w', encoding='utf-8').write(out)
print('新增 mark', n)
