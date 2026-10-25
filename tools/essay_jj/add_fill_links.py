# -*- coding: utf-8 -*-
"""《經紀法規_定義填空練習》補三件事（使用者回報）：

1. **申論跳轉**：卡片只寫「申論 N 次」卻連不過去。改成可點的題號，直接跳到
   《備考指揮中心》對應的申論卡（錨點 es-xxx）。
2. **考次統計算到這張卡自己頭上**：原本只顯示整章的「H篇歷屆 117 題（22.5%）」，
   那是章別統計，對單張卡沒意義。改成以這張卡的**條號**去比對 quiz_data 的
   「本題相關法條」，算出「本條考過 N 題」，並附一鍵練這幾題的連結。
3. **黃底重點**：白話／口訣／陷阱沿用法條解析練習的 hl()，條號、數字量詞、
   分數、法律效果詞自動加半高黃底粗體。

可重複執行。
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, '經紀法規_定義填空練習.html')
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
QD = json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))

HUBURL = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'
QZURL = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html'

# ── 申論卡：年-題 → 錨點 ──
hs = io.open(HUB, encoding='utf-8').read()
ESMAP = {}
for m in re.finditer(r'id="(es-[a-z0-9]+)"', hs):
    seg = re.sub(r'<[^>]+>', '', hs[m.end():m.end() + 220])
    seg = re.sub(r'範文\s*\d{2}', '', seg, count=1)      # 「範文08」會和後面的年份黏成 0899
    y = re.search(r'(?<!\d)(\d{2,3})\s*年申論([一二三四])', seg)
    if y:
        ESMAP.setdefault('%s-%s' % (y.group(1), y.group(2)), m.group(1))

# ── 章別 → 裸 § 預設法規 ──
BARE = {'A': '經紀業條例', 'B': '施行細則', 'E': '公寓大廈',
        'F': '公寓大廈施行細則', 'G': '公平法', 'H': '消保法'}
NAMED = [
    ('公寓大廈施行細則', '公寓大廈施行細則'), ('公寓大廈管理服務人辦法', '公寓大廈管理服務人辦法'),
    ('消保法施行細則', '消保法施行細則'), ('公寓大廈管理條例', '公寓大廈'), ('公寓大廈', '公寓大廈'),
    ('平均地權條例', '平均地權條例'), ('申報登錄備查辦法', '備查辦法'), ('備查辦法', '備查辦法'),
    ('不動產經紀業管理條例', '經紀業條例'), ('經紀業條例', '經紀業條例'), ('條例', None),
    ('公平法', '公平法'), ('公平交易法', '公平法'),
    ('消保法', '消保法'), ('消費者保護法', '消保法'),
    ('施行細則', None), ('細則', None),
]


def arts(src, ch):
    """從 src 抽出條號，回傳 lawfull.json 格式的 key 集合。"""
    out = set()
    # 以法規名切段，段內的 §N 都歸該法規
    toks = list(re.finditer(r'(%s)' % '|'.join(re.escape(a) for a, _ in NAMED), src))
    spans = []
    for i, t in enumerate(toks):
        end = toks[i + 1].start() if i + 1 < len(toks) else len(src)
        name = next(b for a, b in NAMED if a == t.group(1))
        if name is None:  # 「條例」「細則」是簡稱，依章別決定
            name = BARE.get(ch)
            if t.group(1) in ('施行細則', '細則'):
                name = {'A': '施行細則', 'B': '施行細則'}.get(ch, '公寓大廈施行細則')
        spans.append((t.start(), end, name))
    if not spans:
        spans = [(0, len(src), BARE.get(ch))]
    for st, en, name in spans:
        if not name:
            continue
        seg = src[st:en]
        # 範圍寫法 §47-50 / §47～§50 展開成逐條
        for m in re.finditer(r'§\s*(\d+)\s*[-–~～]\s*§?\s*(\d+)', seg):
            a, b = int(m.group(1)), int(m.group(2))
            if 0 < b - a <= 12:
                for v in range(a, b + 1):
                    out.add('%s §%d' % (name, v))
        for m in re.finditer(r'§\s*(\d+)(?:\s*之\s*(\d+))?', seg):
            a = '§%s' % m.group(1) + ('之%s' % m.group(2) if m.group(2) else '')
            out.add('%s %s' % (name, a))
    return out


# ── 官方題（排除模擬卷與已廢止）依條號建索引 ──
BYLAW = {}
for q in QD['q']:
    if q.get('sr') == 'mock' or q.get('oos'):
        continue
    for L in (q.get('law') or []):
        BYLAW.setdefault(L, []).append(q['k'])



# ── 條號對不到的卡：用人工指定的關鍵詞補位（AND 條件，精度約八成，
#    所以標籤用「相關考古題」而不是「本條考過」） ──
KW = {
 'B-3': [['經紀人', '換證'], ['經紀人證書', '有效期限']],
 'B-5': [['業務', '紀錄'], ['查詢', '取閱']],
 'C-0': [['不得記載', '說明書']],
 'C-3': [['水災'], ['淹水']],
 'C-4': [['氯離子'], ['放射性']],
 'C-5': [['使用分區'], ['建蔽率'], ['容積率']],
 'C-6': [['建物型態'], ['區分所有建物']],
 'D-3': [['審閱期'], ['審閱期間']],
 'D-4': [['利息', '百分之']],
 'D-6': [['預售屋', '違約']],
 'D-7': [['履約擔保'], ['價金信託'], ['不動產開發信託']],
 'D-10': [['使用執照', '交屋'], ['移轉登記', '個月']],
 'D-11': [['成交行情'], ['要約書', '轉交']],
 'D-12': [['斡旋金']],
 'D-13': [['定金', '沒收', '受託人']],
 'D-15': [['土地增值稅', '契稅']],
 'E-16': [['罰鍰', '公寓大廈']],
 'F-0': [['公共基金', '工程造價'], ['千分之']],
 'F-1': [['召集人', '推選'], ['互推']],
 'F-4': [['會計憑證'], ['日記帳'], ['財務報表']],
 'G-5': [['加盟']],
}
TXT = {q['k']: (q['stem'] + '｜' + '｜'.join(q['opt']))
       for q in QD['q'] if q.get('sr') != 'mock' and not q.get('oos')}

def ykey(k):
    y, n = k.split('-')
    return (-int(y), int(n))


# ── 取出 DATA ──
s = io.open(PAGE, encoding='utf-8').read()
st = s.index('[', s.index('DATA'))
d, k = 0, st
while True:
    if s[k] == '[':
        d += 1
    elif s[k] == ']':
        d -= 1
        if d == 0:
            break
    k += 1
D = json.loads(s[st:k + 1])

nq = nes = 0
miss_es = []
for ch in D:
    for i, c in enumerate(ch['cards']):
        cid = '%s-%d' % (ch['id'], i)
        # ① 以條號比對「本題相關法條」——精確
        ks = set()
        for L in arts(c.get('src', ''), ch['id']):
            ks.update(BYLAW.get(L, []))
        c['qk'] = sorted(ks, key=ykey)[:14]
        c['qkind'] = 'art' if ks else ''
        # ② 條號對不到時，用人工關鍵詞補位——較寬鬆
        if not ks and cid in KW:
            hit = set()
            for grp in KW[cid]:
                for qk, t in TXT.items():
                    if all(w in t for w in grp):
                        hit.add(qk)
            if hit:
                c['qk'] = sorted(hit, key=ykey)[:14]
                c['qkind'] = 'kw'
        if c['qk']:
            nq += 1
        # ② 申論題號 → 錨點
        es, seen = [], set()
        # 「（申論105年一、113年一）」第二個以後沒有「申論」前綴，整段抓出來再逐一解析
        for blk in re.findall(r'申論[^）)]*', c.get('src', '')):
            for y, no in re.findall(r'(\d{2,3})\s*年\s*([一二三四])', blk):
                lab = '%s-%s' % (y, no)
                if lab in seen:
                    continue
                seen.add(lab)
                if lab in ESMAP:
                    es.append([lab, ESMAP[lab]])
                else:
                    miss_es.append(lab)
        c['esl'] = es
        if es:
            nes += 1

new = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
s = s[:st] + new + s[k + 1:]
io.open(PAGE, 'w', encoding='utf-8').write(s)

tot = sum(len(ch['cards']) for ch in D)
art=sum(1 for ch in D for c in ch['cards'] if c.get('qkind')=='art')
kw=sum(1 for ch in D for c in ch['cards'] if c.get('qkind')=='kw')
print('卡片 %d 張｜有考古題連結 %d 張（條號命中 %d、關鍵詞補位 %d）｜申論跳轉 %d 張'
      % (tot, nq, art, kw, nes))
if miss_es:
    print('⚠ 指揮中心找不到對應申論卡：', sorted(set(miss_es)))
noq = [('%s-%d' % (ch['id'], i), c['src'][:46])
       for ch in D for i, c in enumerate(ch['cards']) if not c['qk']]
print('沒有對到任何考古題的 %d 張（多半是公告類，條文庫無對應條號）：' % len(noq))
for x in noq:
    print('   ', x)
