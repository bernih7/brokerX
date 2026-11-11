# -*- coding: utf-8 -*-
"""11-11 使用者：推理版作答完（存檔後回看本題）按 → 不會打開「看條文原文」。
回看時 →：本頁有收著的條文原文先打開，全開了才翻下一頁。四科 tpl＋已產生頁面。可重跑。"""
import glob, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
O = "  if(k==='ArrowRight')return void hit(rvN);"
N = ("  if(k==='ArrowRight'){var lr=Array.prototype.find.call(run.querySelectorAll('details.lawx'),function(d){return !d.open&&d.offsetParent!==null});\n"
     "   if(lr){e.preventDefault();lr.open=true;return;}   /* 回看：本頁條文原文先打開 */\n"
     "   return void hit(rvN);}")
fs = glob.glob(os.path.join(ROOT, 'tools', 'essay_*', 'sprint', 'tpl_reason.html')) + glob.glob(os.path.join(ROOT, '*_申論5分鐘_推理版.html'))
for f in fs:
    s = open(f, encoding='utf-8').read()
    if N in s: print('已改', os.path.relpath(f, ROOT)); continue
    if s.count(O) == 1: open(f, 'w', encoding='utf-8').write(s.replace(O, N)); print('改', os.path.relpath(f, ROOT))
    else: print('找不到', os.path.relpath(f, ROOT), s.count(O))
