# -*- coding: utf-8 -*-
"""民法條文覆蓋盤點：官方 520 題 law 欄被考過的條文 vs 整理頁（不含題庫、小卡、模擬卷）有沒有提到。輸出 cov_scan.json。"""
import json, re, collections, html, os, io
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
qs = json.load(open(os.path.join(H, 'quiz_data.json'), encoding='utf-8'))['q']
cnt = collections.defaultdict(list)
for q in qs:
    for a in q.get('law') or []: cnt[a].append(q['k'])
PAGES = ['民法A_彩色重點速記', '民法BC_彩色重點速記', '民法D_彩色重點速記', '民法E_彩色重點速記', '民法_債之發生與移轉', '民法_共有專區', '民法_抵押權總整理',
         '民法_數字期間速查', '民法_法律效果總整理', '民法_物權變動與登記', '民法_繼承專區', '民法_用詞分類與申論必背', '民法_定義填空練習']
def base(a): return int(a.split('-')[0])
have = collections.defaultdict(set)
NUM = r'(\d{1,4})(?:\s*(?:-|之)\s*(\d{1,2}))?'
PAT = [re.compile(r'§\s*' + NUM + r'(?:\s*[～~至]\s*§?\s*' + NUM + ')?'),
       re.compile(r'第\s*' + NUM.replace('(?:-|之)', '之') + r'\s*條(?:\s*[～~至]\s*第?\s*' + NUM + r'\s*條)?'),
       re.compile(r'(?<![\d.§])' + NUM + r'(?:\s*[～~至]\s*' + NUM + r')?\s*條')]
for p in PAGES:
    s = io.open(os.path.join(R, p + '.html'), encoding='utf-8').read()
    t = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)))
    for rx in PAT:
        for m in rx.finditer(t):
            g = m.groups(); a1, s1 = g[0], g[1]
            a2 = g[2] if len(g) > 2 else None
            have[a1 + ('-' + s1 if s1 else '')].add(p)
            if s1 and int(s1) > int(a1) % 100 + 1 and int(s1) < 100 and base(a1) < 100:  # 「69-70條」＝區間
                for x in range(int(a1), int(s1) + 1): have[str(x)].add(p)
            if a2 and int(a2) >= int(a1) and int(a2) - int(a1) < 40:
                for x in range(int(a1), int(a2) + 1): have[str(x)].add(p)
miss = sorted(((a, v) for a, v in cnt.items() if a not in have), key=lambda x: (-len(x[1]), base(x[0])))
json.dump({'tested': len(cnt), 'miss': miss}, io.open(os.path.join(H, 'cov_scan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('考過條文', len(cnt), '整理頁沒提到', len(miss), '其中考過 ≥2 題', sum(1 for a, v in miss if len(v) >= 2))
