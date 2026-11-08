# -*- coding: utf-8 -*-
"""114-18 解析★行寫清楚（§955 只規定善意）；民法D彩色重點速記 D8 善意 vs 惡意占有人表補「有益費用」列與考題連結（使用者 11-08）。可重跑。"""
import os
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OLD = '有益費用惡意不得請求（§955）。'
NEW = '有益費用只有§955規定善意占有人得請求，惡意占有人法無規定，不得請求。'
for f in ['民法刷題練習_D篇.html', '民法_法條解析練習.html', '民法D_完整考題小卡.html', '民法概要_25題模擬測驗.html', 'tools/civ_quiz/quiz_data.json']:
    p = os.path.join(R, f); s = open(p, encoding='utf-8').read()
    n = s.count(OLD); s = s.replace(OLD, NEW); open(p, 'w', encoding='utf-8').write(s); print(f, n)
p = os.path.join(R, '民法D_彩色重點速記.html'); s = open(p, encoding='utf-8').read()
a = '<td>依<b>無因管理</b>規定請求償還（957條）</td></tr>'
b = ('<td>得依<b>無因管理</b>規定請求償還（957條）——<b>不是不得請求</b></td></tr>\n'
     '      <tr><td>有益費用</td><td>於<b>現存增加價值限度內</b>得請求償還（955條）</td><td>法無規定，<b>不得請求</b>（955條只規定善意占有人）</td></tr>')
if '<tr><td>有益費用</td>' not in s:
    assert s.count(a) == 1; s = s.replace(a, b)
q = '<p class="psq" style="font-size:.85rem;margin:6px 0 0">考過：<a target="_blank" rel="noopener" href="%E6%B0%91%E6%B3%95_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html#q=114-18">114-18 ↗</a></p>'
anc = '<td>得依<b>無因管理</b>'
if 'class="psq"' not in s:
    i = s.index('</table>', s.index(anc)); j = s.index('</div>', i) + 6; s = s[:j] + '\n  ' + q + s[j:]
open(p, 'w', encoding='utf-8').write(s); print('D彩色 OK')
