# -*- coding: utf-8 -*-
"""5 分鐘練習（經紀法規、民法 × 考場版、推理版）鍵盤操作（11-03 使用者要求）：
練習中 → 或空白鍵＝下一段／下一步（推理版還沒翻開時先翻開）；
存檔後回看本題：← 上一頁、→ 下一頁；空白鍵＝下一題。輸入框、下拉選單內不攔截。可重跑。"""
import os
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
JS = r'''<script id="sprint-keys">
/* 鍵盤：練習中 →／空白鍵＝下一段（推理版未翻開先翻開）；回看本題 ←／→ 翻頁；空白鍵＝下一題 */
document.addEventListener('keydown',function(e){
 if(e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;
 var t=e.target,tag=(t&&t.tagName)||'';if(/^(INPUT|SELECT|TEXTAREA)$/.test(tag)||(t&&t.isContentEditable))return;
 var k=e.key;if(k!=='ArrowRight'&&k!=='ArrowLeft'&&k!==' '&&k!=='Spacebar')return;
 var run=document.getElementById('run');if(!run||run.hidden)return;
 if(document.body.classList.contains('paused'))return;
 var rvP=document.getElementById('rvP'),rvN=document.getElementById('rvN'),nb=document.getElementById('nextBtn');
 function hit(b){if(b&&!b.disabled&&b.offsetParent!==null){e.preventDefault();b.click();return true}return false}
 if(rvP&&rvP.offsetParent!==null){            /* 存檔後：回看本題 */
  if(k==='ArrowLeft')return void hit(rvP);
  if(k==='ArrowRight')return void hit(rvN);
  return void hit(nb);                       /* 空白鍵＝下一題 */
 }
 if(k==='ArrowLeft')return;
 if(hit(document.getElementById('flip')))return;
 hit(nb);
});
</script>'''
for sub in ('essay_jj', 'essay_civ'):
    for fn in ('tpl.html', 'tpl_reason.html'):
        p = os.path.join(R, 'tools', sub, 'sprint', fn)
        if not os.path.exists(p): continue
        s = open(p, encoding='utf-8').read()
        import re
        s = re.sub(r'<script id="sprint-keys">.*?</script>\n?', '', s, flags=re.S)
        s = s.replace('</body>', JS + '\n</body>', 1)
        # 提示文字加上鍵盤說明（桌機才有用，放在模式說明之後不顯眼）
        open(p, 'w', encoding='utf-8').write(s); print('鍵盤操作', sub, fn)
