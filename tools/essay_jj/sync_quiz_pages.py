# -*- coding: utf-8 -*-
"""把 quiz_data.json 的 exp／ref 同步到 12 支刷題練習_*.html 內嵌的 QUESTIONS。

這些頁面各自帶一份 const QUESTIONS = [...]（key 為 year/qnum/explains{A..D}/ref），
是 quiz_data.json 的副本。本腳本就地解析該 JSON 陣列，照 (year,qnum) 覆寫
explains 與 ref，其餘欄位（stem/options/answer/id/chapter）完全不動。
可重複執行；找不到對應題目會列出但不中止（模擬題可能不在 quiz_data 裡）。
"""
import io, json, os, glob, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
D = json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))
SRC = {}
for q in D['q']:
    exp = q.get('exp') or []
    SRC[(q['y'], q['n'])] = {
        'explains': {'ABCD'[i]: exp[i] for i in range(min(len(exp), 4))},
        'ref': q.get('ref') or '',
        'stem': q.get('stem') or '',
        'options': list(q.get('opt') or []),
    }

def arr_end(s, i):
    """i 指向 '['，回傳對應 ']' 的 index+1（JSON 字串感知）。"""
    d, k, instr, esc = 0, i, False, False
    while k < len(s):
        c = s[k]
        if instr:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c in '[{': d += 1
            elif c in ']}':
                d -= 1
                if d == 0: return k + 1
        k += 1
    raise ValueError('找不到陣列結尾')

# 本次確定要連題幹／選項一起覆寫的題（依考選部官方試題更正者）
ALLOW = {(106, 33)}

tot_pages = tot_q = tot_exp = tot_ref = tot_stem = tot_opt = 0
miss = []
drift = []
for p in sorted(glob.glob(os.path.join(ROOT, '經紀法規刷題練習_*.html'))):
    s = io.open(p, encoding='utf-8').read()
    m = re.search(r'const QUESTIONS\s*=\s*', s)
    if not m:
        print('  ⚠ %s 找不到 QUESTIONS，跳過' % os.path.basename(p)); continue
    a = s.index('[', m.end()); b = arr_end(s, a)
    try:
        qs = json.loads(s[a:b])
    except Exception as e:
        print('  ✗ %s JSON 解析失敗：%s' % (os.path.basename(p), e)); sys.exit(1)
    ce = cr = cs = co = 0
    for item in qs:
        key = (item.get('year'), item.get('qnum'))
        src = SRC.get(key)
        if src is None:
            miss.append('%s：%s-%s' % (os.path.basename(p), key[0], key[1])); continue
        old = item.get('explains') or {}
        new = dict(old)
        for L, v in src['explains'].items():
            if L in old and old[L] != v:
                new[L] = v; ce += 1
            elif L not in old:
                new[L] = v; ce += 1
        item['explains'] = new
        if src['ref'] and item.get('ref') != src['ref']:
            item['ref'] = src['ref']; cr += 1
        # 題幹與選項只在 ALLOW 名單內才覆寫。頁面副本過去做過人工清理
        # （101-14 的「→」、113-9 的引號間距等），全量同步會把它們改壞。
        if src['stem'] and item.get('stem') != src['stem']:
            if key in ALLOW:
                item['stem'] = src['stem']; cs += 1
            else:
                drift.append('%s：%s-%s 題幹不同（未改）' % (os.path.basename(p), key[0], key[1]))
        if src['options'] and item.get('options') != src['options']:
            if key in ALLOW and len(src['options']) == len(item.get('options') or []):
                item['options'] = src['options']; co += 1
            else:
                drift.append('%s：%s-%s 選項不同（未改）' % (os.path.basename(p), key[0], key[1]))
    out = s[:a] + json.dumps(qs, ensure_ascii=False) + s[b:]
    if out != s:
        io.open(p, 'w', encoding='utf-8').write(out)
    tot_pages += 1; tot_q += len(qs); tot_exp += ce; tot_ref += cr
    tot_stem += cs; tot_opt += co
    print('  %-34s %3d 題　解析 %3d　ref %3d　題幹 %d　選項 %d'
          % (os.path.basename(p), len(qs), ce, cr, cs, co))

print('\n共 %d 頁 / %d 題；解析 %d 處、ref %d 處、題幹 %d 處、選項 %d 處'
      % (tot_pages, tot_q, tot_exp, tot_ref, tot_stem, tot_opt))
if miss:
    print('quiz_data 內找不到的題（未改）：%d 筆' % len(miss))
    for x in miss[:12]: print('   ', x)
if drift:
    print('題幹／選項與 quiz_data 不同但不在 ALLOW 名單，未改：%d 筆' % len(drift))
    for x in drift[:12]: print('   ', x)
