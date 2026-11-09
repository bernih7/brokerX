# -*- coding: utf-8 -*-
"""11-10 使用者截圖 110-一 衝刺③／推理版②：§23 十三款分類擠在一起被①②切行切壞（「⑪人為哄抬；交易關係類有③…」「動機（／①②⑨⑪）」），並問「口訣呢？」。
①考場版（一）改為五類各一行＋口訣；②切行規則：圈號後面緊接圈號或「）」（如「（①②⑨⑪）」）不切（render_ev.lst、四科推理版 rt()）。可重跑。"""
import json, os, re, glob
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
OLD = "（一）§23所列情況：交易動機類有<mark>①急買急賣或急出租急承租、②期待因素影響</mark>、⑨受迷信影響、⑪人為哄抬；交易關係類有③債權債務、④親友關係人間；交易標的類有⑤畸零地或合併使用、⑥地上物處理糾紛、⑩包含公共設施用地、⑫與法定用途不符；交易程序類有⑦拍賣、⑧公有土地標售讓售；⑬其他特殊交易為概括規定。例：拍賣屬非自願、限制多。"
NEW = ("（一）§23所列情況：十三款依交易性質分五類記，口訣：<b>急期債親，畸糾拍公，迷設哄符他</b>（依款次①～⑬）。"
       "<br><span class=\"evcat\"><b>交易動機</b>：<mark>①急買急賣或急出租急承租、②期待因素影響</mark>、⑨受迷信影響、⑪人為哄抬</span>"
       "<br><span class=\"evcat\"><b>交易關係</b>：③債權債務、④親友關係人間</span>"
       "<br><span class=\"evcat\"><b>交易標的</b>：⑤畸零地或有合併使用、⑥地上物處理有糾紛、⑩包含公共設施用地、⑫與法定用途不符</span>"
       "<br><span class=\"evcat\"><b>交易程序</b>：⑦拍賣、⑧公有土地標售、讓售</span>。例：拍賣屬非自願、限制多。"
       "<br><span class=\"evcat\"><b>概括規定</b>：⑬其他特殊交易</span>")
fs = [os.path.join(H, 'exam', 'exam_ver.json')] + glob.glob(os.path.join(H, 'exam', 'out_*.json'))
for f in fs:
    d = json.load(open(f, encoding='utf-8'))
    if 'e110-1' not in d: continue
    ch = False
    for blk in d['e110-1']:
        if OLD in blk[1]: blk[1] = blk[1].replace(OLD, NEW); ch = True
    if ch:
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=f.endswith('exam_ver.json')); print('改', os.path.basename(f))
# 切行規則：圈號後面緊接圈號或「）」不切
R = os.path.join(H, 'exam', 'render_ev.py'); s = open(R, encoding='utf-8').read()
o = "and depth == 0 and (prev == '' or prev in PUN) and not"
n = "and depth == 0 and (prev == '' or prev in PUN) and not re.match(r'[①-⑳）)]', t[m.end():m.end() + 1] or '）') and not"
if n not in s: assert s.count(o) == 1; open(R, 'w', encoding='utf-8').write(s.replace(o, n)); print('render_ev 規則')
o2 = "'　 ，；：、。（→'.indexOf(h[m.index-1])>=0))c.push(m.index)"
n2 = "'　 ，；：、。（→'.indexOf(h[m.index-1])>=0)&&!/[\\u2460-\\u2473）)]/.test(h.charAt(m.index+1)||'）'))c.push(m.index)"
for f in glob.glob(os.path.join(ROOT, 'tools', 'essay_*', 'sprint', 'tpl_reason.html')) + glob.glob(os.path.join(ROOT, '*_申論5分鐘_推理版.html')):
    s = open(f, encoding='utf-8').read()
    if o2 in s: open(f, 'w', encoding='utf-8').write(s.replace(o2, n2)); print('rt', os.path.relpath(f, ROOT))
# ③ 推理版／邏輯拆解：小結補口訣（lj_data 與申論頁 lj 面板同一句）
OR = '十三款依動機、關係、標的、程序分類記。'
NR = '十三款依動機、關係、標的、程序、概括分類記；口訣：急期債親，畸糾拍公，迷設哄符他（依款次①～⑬）。'
LJ = os.path.join(H, 'lj_data.json'); d = json.load(open(LJ, encoding='utf-8'))
for c in d:
    if c['k'] == 'e110-1':
        for sb in c['subs']:
            for st in sb['steps']:
                if st.get('res') == OR: st['res'] = NR; print('lj_data res')
json.dump(d, open(LJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
EP = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html'); s = open(EP, encoding='utf-8').read()
if OR in s: open(EP, 'w', encoding='utf-8').write(s.replace(OR, NR)); print('申論頁 lj')
