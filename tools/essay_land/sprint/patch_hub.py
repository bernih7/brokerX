# 土地法指揮中心：申論分頁加「5 分鐘衝刺」「5 分鐘・推理版」入口；申論總覽題數更新。可重跑
import os, re, json
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
f = os.path.join(R, '土地法_備考指揮中心.html'); s = open(f, encoding='utf-8').read()
n = len(re.findall(r'<details class="es[^"]*" id="', open(os.path.join(R, '土地法_申論題分類總覽.html'), encoding='utf-8').read()))
s = re.sub(r'申論總覽（全部 \d+ 題）', '申論總覽（全部 %d 題）' % n, s)
LINK = ('<a class="tool-link" id="spLink" href="土地法_申論5分鐘衝刺.html" target="_blank" rel="noopener"><div><div class="name">⏱ 申論 5 分鐘衝刺</div><div class="tag">一題 5 分鐘：讀題→先自己想→考場版→結論→關鍵檢核打分；115 高機率且沒做過的優先，再來不熟的；紀錄與申論總覽同步</div></div><span class="badge gold">開啟</span></a>\n'
        '   <a class="tool-link" id="spLink2" href="土地法_申論5分鐘_推理版.html" target="_blank" rel="noopener"><div><div class="name">🧩 申論 5 分鐘・推理版</div><div class="tag">跟著推理鏈一步步自問自答→速寫骨架→失分點→關鍵詞檢核；同一題可與衝刺版互換</div></div><span class="badge">開啟</span></a>\n   ')
if 'id="spLink"' not in s:
    k = s.find('<a class="tool-link" href="https://bernih7.github.io/brokerX/%E5%9C%9F%E5%9C%B0%E6%B3%95_%E7%94%B3%E8%AB%96115'); assert k > 0
    s = s[:k] + LINK + s[k:]
open(f, 'w', encoding='utf-8').write(s); print('ok', n)
