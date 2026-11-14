# -*- coding: utf-8 -*-
"""由 tpl_drill.html 產生四科《○○_錯題複習卷.html》。可重跑。"""
import os
R = os.path.join(os.path.dirname(__file__), '..', '..')
T = open(os.path.join(os.path.dirname(__file__), 'tpl_drill.html'), encoding='utf-8').read()
HUB = {'land': '土地法_備考指揮中心.html', 'civ': '民法_備考指揮中心.html', 'jj': '經紀法規_備考指揮中心.html', 'val': '估價備考指揮中心.html'}
RATIO = ('land', 'jj')  # 11-14 使用者：只改土地法、經紀法規（民法、估價已考完）
NAME = {'land': '土地法', 'civ': '民法', 'jj': '經紀法規', 'val': '估價'}
for S in NAME:
    assert os.path.exists(os.path.join(R, HUB[S])), HUB[S]
    s = T.replace('@@NAME@@', NAME[S]).replace('@@POOL@@', 'bx-pool-%s.js' % S).replace('@@HUB@@', HUB[S]).replace('@@RATIO@@', '1' if S in RATIO else '0').replace('@@RATIO_TXT@@', '新題先把模擬卷全部做完（依 107–114 年歷屆各章比例挑），模擬卷做完後，歷屆題同樣依各章比例出題。' if S in RATIO else '')
    open(os.path.join(R, '%s_錯題複習卷.html' % NAME[S]), 'w', encoding='utf-8').write(s)
    print('ok', NAME[S])
