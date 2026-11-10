# -*- coding: utf-8 -*-
"""11-10 使用者：推理版「看條文原文」也要能用 →／空白鍵打開。
練習中按 →／空白：①未翻開先翻開 ②本步有收著的「看條文原文／看公式內容／看內容」先打開 ③再下一步。四科 tpl＋已產生頁面。可重跑。"""
import glob, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
O = " if(hit(document.getElementById('flip')))return;\n hit(nb);"
N = (" if(hit(document.getElementById('flip')))return;\n"
     " var lx=Array.prototype.find.call(run.querySelectorAll('details.lawx'),function(d){return !d.open&&d.offsetParent!==null});\n"
     " if(lx){e.preventDefault();lx.open=true;return;}   /* 有收著的條文原文：先打開 */\n"
     " hit(nb);")
fs = glob.glob(os.path.join(ROOT, 'tools', 'essay_*', 'sprint', 'tpl_reason.html')) + glob.glob(os.path.join(ROOT, '*_申論5分鐘_推理版.html'))
for f in fs:
    s = open(f, encoding='utf-8').read()
    if N in s: continue
    if s.count(O) == 1: open(f, 'w', encoding='utf-8').write(s.replace(O, N)); print('改', os.path.relpath(f, ROOT))
    else: print('找不到', os.path.relpath(f, ROOT), s.count(O))
