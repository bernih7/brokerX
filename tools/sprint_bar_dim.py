# -*- coding: utf-8 -*-
"""5 分鐘練習底部操作列（提示＋放棄這題＋下一段）整列淡出（11-03 使用者：「不是只有這四個字，是整行」）：
閱讀階段每段開始 4 秒後整列變淡（仍可按）；手指碰到或滑鼠移上去就恢復；⑤檢核與存檔後不淡出。
經紀法規、民法 × 衝刺、推理版共 4 份 tpl。可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CSS = ('.act{transition:opacity .8s}.act.dim{opacity:.22}.act.dim:hover,.act.dim:focus-within{opacity:1}'
       '.act .hint{font-size:.78rem;color:var(--sub);flex:1;min-width:0}')
JS = r'''<script id="sprint-bardim">
/* 底部操作列整列淡出：閱讀階段每段 4 秒後變淡；碰到就恢復 */
(function(){var a=document.getElementById('act'),t=null;if(!a)return;
 function reading(){return typeof st==='number'&&st<4}
 window.barWake=function(){a.classList.remove('dim');clearTimeout(t);if(reading())t=setTimeout(function(){if(reading())a.classList.add('dim')},4000)};
 a.addEventListener('pointerdown',function(){if(a.classList.contains('dim'))barWake()},true);
 setInterval(function(){if(!reading()&&a.classList.contains('dim'))a.classList.remove('dim')},500);
})();
</script>'''
for sub in ('essay_jj', 'essay_civ'):
    for fn in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', fn); s = open(p, encoding='utf-8').read()
        s = re.sub(r'<style id="sprint-bardim-css">.*?</style>', '', s, flags=re.S)
        s = s.replace('</style>', '</style><style id="sprint-bardim-css">%s</style>' % CSS, 1)
        # 原本只淡出提示文字的作法拿掉
        s = s.replace(".act .hint.gone{opacity:0}", "")
        s = re.sub(r"var _ht=null;function hintFade\(\)\{[^\n]*\n", "", s)
        s = s.replace("\n  hintFade();\n", "\n  if(window.barWake)barWake();\n")
        if 'barWake)barWake()' not in s:  # 民法版：在 paintAct／act 結尾加
            name = 'function paintAct(){' if 'function paintAct(){' in s else 'function act(){'
            i = s.find(name); k = s.find('{', i); d = 0
            while True:
                c = s[k]
                if c == '{': d += 1
                elif c == '}':
                    d -= 1
                    if d == 0: break
                k += 1
            s = s[:k] + '\n  if(window.barWake)barWake();\n' + s[k:]
        s = re.sub(r'<script id="sprint-bardim">.*?</script>\n?', '', s, flags=re.S)
        s = s.replace('</body>', JS + '\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(s); print('整列淡出', sub, fn, s.count('barWake'))
