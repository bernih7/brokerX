# -*- coding: utf-8 -*-
"""經紀法規定義填空：隨機測驗章節篩選改為可收合（預設收起，顯示目前選擇；選完自動收起）。比照估價／土地法／民法。可重跑。"""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '經紀法規_定義填空練習.html')
s = open(P, encoding='utf-8').read()
if 'id="qf-wrap"' not in s:
    def rep(a, b):
        global s
        assert s.count(a) == 1, a[:50]; s = s.replace(a, b)
    rep('  <div class="quiz-filter" id="quiz-filter"></div>',
        '  <details class="qf-wrap" id="qf-wrap"><summary id="qf-sum">📑 章節：<b>全部章節（不含申論四段）</b> ▾</summary><div class="quiz-filter" id="quiz-filter"></div></details>')
    rep('.quiz-filter{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}',
        '.quiz-filter{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px}\n'
        'details.qf-wrap{margin-bottom:12px;text-align:center}\n'
        'details.qf-wrap>summary{display:inline-block;cursor:pointer;list-style:none;font-size:13.5px;font-weight:700;padding:6px 18px;border-radius:99px;border:1.5px solid var(--green);color:var(--green);max-width:100%}\n'
        'details.qf-wrap>summary::-webkit-details-marker{display:none}\n'
        'details.qf-wrap>summary b{color:var(--ink,inherit)}\n'
        'details.qf-wrap .quiz-filter{margin-top:10px;text-align:left}')
    rep("""  btn.classList.add('on');
  startQuizRound();
}""", """  btn.classList.add('on');
  const sm=document.getElementById('qf-sum'); if(sm) sm.innerHTML='📑 章節：<b>'+btn.textContent+'</b> ▾';
  const fw=document.getElementById('qf-wrap'); if(fw) fw.open=false;
  startQuizRound();
}""")
    open(P, 'w', encoding='utf-8').write(s); print('ok')
else: print('已有')
