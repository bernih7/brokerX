# -*- coding: utf-8 -*-
"""從 lawfull.json 抽出「數字 → 屬於哪一條」的反向索引資料。
用途：經紀法規的數字密度是四科最高，而考題套路就是同一個數字屬於哪一條
（例：3萬～15萬 出現在 8 條、6萬～30萬 的主體一個是建商一個是經紀業）。
只產資料，不產頁面；頁面要不要做由使用者決定。
"""
import collections, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(io.open(os.path.join(HERE, 'law', 'lawfull.json'), encoding='utf-8'))
CN = '零一二三四五六七八九十百千萬億'
DIG = {c: i for i, c in enumerate('零一二三四五六七八九')}


def cn(s):
    units = {'十': 10, '百': 100, '千': 1000}
    tot = cur = big = 0
    for c in s:
        if c in DIG:
            cur = DIG[c]
        elif c in units:
            cur = cur or 1
            tot += cur * units[c]
            cur = 0
        elif c == '萬':
            big += (tot + cur or 1) * 10000
            tot = cur = 0
        elif c == '億':
            big += (tot + cur or 1) * 100000000
            tot = cur = 0
    return big + tot + cur


def fmt(n):
    n = int(n)
    if n >= 10000:
        return '%d萬' % (n // 10000) if n % 10000 == 0 else '%g萬' % (n / 10000)
    return str(n)


money, period, ratio = (collections.defaultdict(list) for _ in range(3))
for k, v in L.items():
    t = v.get('text', '')
    for m in re.finditer(r'新臺幣([%s]+)元以上([%s]+)元以下罰(鍰|金)' % (CN, CN), t):
        money['%s～%s' % (fmt(cn(m.group(1))), fmt(cn(m.group(2))))].append(
            {'art': k, 'kind': '罰' + m.group(3)})
    for m in re.finditer(r'([%s]+)(日|個月|年|小時|工作日)' % CN, t):
        n = cn(m.group(1))
        if 0 < n <= 120:
            period['%d%s' % (n, m.group(2))].append(k)
    for m in re.finditer(r'([%s]+)分之([%s]+)' % (CN, CN), t):
        ratio['%d分之%d' % (cn(m.group(1)), cn(m.group(2)))].append(k)

out = {
    '罰鍰罰金級距': {k: v for k, v in sorted(money.items(), key=lambda x: -len(x[1]))},
    '期間': {k: sorted(set(v)) for k, v in sorted(period.items(), key=lambda x: -len(set(x[1])))},
    '比例': {k: sorted(set(v)) for k, v in sorted(ratio.items(), key=lambda x: -len(set(x[1])))},
}
dst = os.path.join(HERE, 'numindex.json')
json.dump(out, io.open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

dup = [(k, v) for k, v in out['罰鍰罰金級距'].items()
       if len(set(x['art'] for x in v)) >= 2]
print('金額級距 %d 組，其中 %d 組跨兩條以上（這些就是最會混的）'
      % (len(out['罰鍰罰金級距']), len(dup)))
for k, v in dup:
    print('  %-12s %s' % (k, '、'.join(sorted(set(x['art'] for x in v)))))
print('期間 %d 種、比例 %d 種' % (len(out['期間']), len(out['比例'])))
