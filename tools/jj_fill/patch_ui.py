# -*- coding: utf-8 -*-
"""經紀法規《定義填空練習》介面：鍵盤、隨機記進度、申論隨機頁籤、申論四段卡版面、五分鐘練習連結、條號連全國法規、換題不回頁首。
比照土地法 v714～v723。只改 DATA 以外的程式；有 /*jjfill-v2*/ 標記就不再重複套用。"""
import os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(ROOT, '經紀法規_定義填空練習.html')
f = open(P, encoding='utf-8').read()
if '/*jjfill-v2*/' in f:
    print('已套用'); raise SystemExit
def rep(a, b, cnt=1):
    global f
    assert f.count(a) == cnt, (f.count(a), a[:80])
    f = f.replace(a, b)

CSS = '''/*jjfill-v2*/
/* 申論四段卡（配色同申論五分鐘推理版） */
:root{--b1:#2F6B8C;--b1s:#E3EFF6;--b2:#7A5BA6;--b2s:#EEE8F6;--b3:#2F7A55;--b3s:#E1F1E8;--b4:#B8782E;--b4s:#F8EBD3;--hl:#FFE9A8}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--b1:#7DB6D8;--b1s:#1D2F3A;--b2:#B79BE0;--b2s:#2B2438;--b3:#7FCBA0;--b3s:#1D3226;--b4:#E0B070;--b4s:#3A3220;--hl:#5A4A18}}
:root[data-theme="dark"]{--b1:#7DB6D8;--b1s:#1D2F3A;--b2:#B79BE0;--b2s:#2B2438;--b3:#7FCBA0;--b3s:#1D3226;--b4:#E0B070;--b4s:#3A3220;--hl:#5A4A18}
:root[data-theme="light"]{--b1:#2F6B8C;--b1s:#E3EFF6;--b2:#7A5BA6;--b2s:#EEE8F6;--b3:#2F7A55;--b3s:#E1F1E8;--b4:#B8782E;--b4s:#F8EBD3;--hl:#FFE9A8}
.esb{display:grid;gap:4px;margin-top:12px;text-align:left;line-height:1.85}
.esb:first-child{margin-top:2px}
.esl{justify-self:start;font-size:.74rem;font-weight:700;border-radius:999px;padding:1px 10px;letter-spacing:.04em}
.esb.e1 .esl{background:var(--b2s);color:var(--b2)}
.esb.e2 .esl{background:var(--b1s);color:var(--b1)}
.esb.e3{border:1.5px solid var(--b4);border-radius:14px;padding:10px 14px;background:var(--card)}
.esb.e3 .esl{background:none;padding:0;color:var(--b4)}
.esb.e4 .esl{background:var(--b3s);color:var(--b3)}
.esb.e5{background:var(--hl);border-radius:12px;padding:10px 14px}
.esb.e5 .esl{background:none;padding:0;color:var(--muted)}
.esb.e5 .esc{font-weight:700}
.es5{margin-top:10px;padding:10px 12px;border:1px dashed var(--line);border-radius:12px;font-size:13px;line-height:1.9}
.es5 b{display:block;font-size:12px;color:var(--muted);margin-bottom:2px}
.es5 .ch5{display:inline-flex;align-items:center;gap:6px;margin:2px 8px 2px 0;white-space:nowrap}
.es5 a.r{font-weight:700;color:var(--red);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:1px 10px;background:var(--card)}
.es5 a.s{font-size:12px;color:var(--muted)}
.cp-sep{flex-basis:100%;font-size:12px;font-weight:700;color:var(--b4);margin:8px 0 0;padding-top:8px;border-top:1px dashed var(--line)}
.qc-kb{font-size:12px;color:var(--muted);text-align:center;margin:6px 0}
.qc-kb a{margin-left:6px;color:var(--muted)}
a.lawlk{color:inherit;text-decoration:none;border-bottom:1px dotted currentColor}
.st-pred{color:var(--muted)}
</style>
<script src="bxj-use.js"></script>'''
rep('.section-hint{color:var(--muted)!important}</style>\n<script src="bxj-use.js"></script>', '.section-hint{color:var(--muted)!important}\n' + CSS)

rep('''  <button class="mode-tab on" id="tab-browse" onclick="setMode('browse')">章節瀏覽</button>
  <button class="mode-tab" id="tab-quiz" onclick="setMode('quiz')">隨機測驗</button>''',
'''  <button class="mode-tab on" id="tab-browse" onclick="setMode('browse')">📖 章節瀏覽</button>
  <button class="mode-tab" id="tab-quiz" onclick="goDefQuiz()">🎲 隨機測驗</button>
  <button class="mode-tab" id="tab-essay" onclick="goEssay()">📝 申論隨機</button>''')

# 申論四段卡輔助函式、條號連結
rep("const QZ='", r'''/* 申論四段卡：全部顯示後附同型題的兩種五分鐘練習 */
function es5Html(c){if(!c.es5||!c.es5.length)return'';return'<div class="es5"><b>⏱ 同型題・申論五分鐘練習</b>'+c.es5.map(function(e){var r=e[1]?'<a class="r" target="_blank" rel="noopener" href="經紀法規_申論5分鐘_推理版.html#q='+encodeURIComponent(e[1])+'">'+e[0]+' 推理 ▸</a>':'<span>'+e[0]+'</span>';var s=e[2]?'<a class="s" target="_blank" rel="noopener" href="經紀法規_申論5分鐘衝刺.html#q='+encodeURIComponent(e[2])+'">衝刺</a>':'';return'<span class="ch5">'+r+s+'</span>'}).join('')+'</div>'}
function isEs(c){return String(c.answer).indexOf('class="esb')>=0}
/* 條號連到全國法規資料庫；「條例／細則」依章節判斷是經紀業還是公寓大廈 */
const LAWPC={'不動產經紀業管理條例':'D0060066','經紀業條例':'D0060066','管理條例':'D0060066','施行細則':'D0060068','細則':'D0060068','條例':'D0060066','公寓大廈管理條例':'D0070118','公寓大廈施行細則':'D0070119','公寓大廈':'D0070118','公寓':'D0070118','公平交易法':'J0150002','公平法':'J0150002','消費者保護法':'J0170001','消保法':'J0170001','平均地權條例':'D0060009','民法':'B0000001'};
const LAWKEYS=Object.keys(LAWPC).sort(function(a,b){return b.length-a.length});
function srcHtml(t,chId){var ef=/^[EF]/.test(chId||'');var cur=null;return String(t).replace(/([一-龥]*)§(\d+)(?:(-|之)(\d+))?/g,function(m,nm,no,sp,sub){if(nm){cur=null;for(var i=0;i<LAWKEYS.length;i++){var k=LAWKEYS[i];if(nm.slice(-k.length)===k){cur=LAWPC[k];if(ef&&(k==='條例'||k==='管理條例'))cur='D0070118';if(ef&&(k==='施行細則'||k==='細則'))cur='D0070119';break}}}
if(!cur)return m;var fl=no,tail='';if(sub){if(sp==='-'&&+sub>+no){tail='-'+sub}else fl=no+'-'+sub}return nm+'<a class="lawlk" target="_blank" rel="noopener" href="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode='+cur+'&flno='+fl+'">§'+no+(sub&&!tail?sp+sub:'')+'</a>'+tail})}
const QZ='''+"'")

# statOf：申論四段卡沒有官方題時的說明
rep("  if(!a.length) a.push('<span class=\"st-none\">歷屆選擇題未直接考過</span>');",
    "  if(!a.length) a.push((c.es5&&c.es5.length)?'<span class=\"st-pred\">本型為預測／模擬題（下方可開五分鐘練習）</span>':'<span class=\"st-none\">歷屆選擇題未直接考過</span>');")

# 章節選單：S1 前加分隔標題；按鈕帶 data-id
rep('''DATA.forEach((ch,ci)=>{
  const btn = document.createElement('button');
  btn.className = 'nav-btn' + (ci===0?' on':'');
  btn.textContent = ch.label;''', '''DATA.forEach((ch,ci)=>{
  if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（另一分類：定義→法條→核心→結論＋卓見）';nav.appendChild(sp)}
  const btn = document.createElement('button');
  btn.className = 'nav-btn' + (ci===0?' on':''); btn.dataset.id = ch.id;
  btn.textContent = ch.label;''')
rep('''        <div class="key-note">${c.answer}</div>
        ${pmtHtml(c)}
        <div class="src" style="margin-top:6px;font-size:12px;color:var(--muted)">📌 ${c.src}</div>
      </div>`;''', '''        ${isEs(c)?'':`<div class="key-note">${c.answer}</div>`}
        ${pmtHtml(c)}
        <div class="src" style="margin-top:6px;font-size:12px;color:var(--muted)">📌 ${srcHtml(c.src,ch.id)}</div>
        ${es5Html(c)}
      </div>`;''')
rep("  [...document.querySelectorAll('.nav-btn')].find(b=>b.textContent.startsWith(id)).classList.add('on');",
    "  const nb=document.querySelector('.nav-btn[data-id=\"'+id+'\"]'); if(nb) nb.classList.add('on');")

# 模式切換：三個頁籤
rep('''    tabB.classList.add('on'); tabQ.classList.remove('on');
  } else {''', '''    tabB.classList.add('on'); tabQ.classList.remove('on'); document.getElementById('tab-essay').classList.remove('on');
  } else {''')
rep('''    tabB.classList.remove('on'); tabQ.classList.add('on');
    initQuiz();''', '''    tabB.classList.remove('on'); tabQ.classList.add('on'); document.getElementById('tab-essay').classList.remove('on');
    initQuiz();''')
rep("quizPool.push({ key: ch.id+'-'+ci, chId: ch.id, chLabel: ch.label, term: c.term, blank: c.blank, answer: c.answer, src: c.src, essay: c.essay||0, hot: c.hot||0, chStat: ch.stat, p: c.p||'', m: c.m||'', t: c.t||'', qk: c.qk||[], qkind: c.qkind||'', esl: c.esl||[] });",
    "quizPool.push({ key: ch.id+'-'+ci, chId: ch.id, chLabel: ch.label, term: c.term, blank: c.blank, answer: c.answer, src: c.src, essay: c.essay||0, hot: c.hot||0, chStat: ch.stat, p: c.p||'', m: c.m||'', t: c.t||'', qk: c.qk||[], qkind: c.qkind||'', esl: c.esl||[], es5: c.es5||[] });")
rep('''    allBtn.textContent = '全部章節';''', '''    allBtn.textContent = '全部章節（不含申論四段）';''')
rep('''    DATA.forEach(ch => {
      const btn = document.createElement('button');
      btn.className = 'qf-btn';''', '''    DATA.forEach(ch => {
      if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（「全部章節」不含，需另選或按「申論隨機」）';filterEl.appendChild(sp);
        const eb=document.createElement('button');eb.className='qf-btn qf-es';eb.dataset.id='ES';eb.textContent='申論四段全部';eb.onclick=()=>setQuizFilter('ES',eb);filterEl.appendChild(eb)}
      const btn = document.createElement('button');
      btn.className = 'qf-btn'; btn.dataset.id = ch.id;''')
rep('''  const pool = quizFilter === 'ALL' ? quizPool : quizPool.filter(c => c.chId === quizFilter);''',
    '''  const pool = quizFilter === 'ALL' ? quizPool.filter(c => c.chId[0] !== 'S') : quizFilter === 'ES' ? quizPool.filter(c => c.chId[0] === 'S') : quizPool.filter(c => c.chId === quizFilter);''')
rep('''function startQuizRound() {''', '''function goEssay(){setMode('quiz');const eb=document.querySelector('.qf-btn[data-id="ES"]');if(eb)setQuizFilter('ES',eb);document.getElementById('tab-quiz').classList.remove('on');document.getElementById('tab-essay').classList.add('on')}
function goDefQuiz(){const wasEs=document.getElementById('tab-essay').classList.contains('on');setMode('quiz');if(wasEs||quizFilter==='ES'||(quizFilter[0]==='S'&&quizFilter!=='ALL')){const ab=document.querySelector('.qf-btn.qf-all');if(ab)setQuizFilter('ALL',ab)}}
try{if(location.hash==='#essay')setTimeout(goEssay,0);addEventListener('hashchange',()=>{if(location.hash==='#essay')goEssay()})}catch(e){}
let kbHint = true; try { kbHint = localStorage.getItem('bxj-fill-kb') !== '1'; } catch (e) {}
function hideKb() { kbHint = false; try { localStorage.setItem('bxj-fill-kb', '1'); } catch (e) {} document.querySelectorAll('.qc-kb').forEach(e => e.remove()); }
function startQuizRound() {''')

# 題卡：提示列、申論四段卡不重複印答案、條號連結、五分鐘練習
rep('''      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      <div class="qc-btns">''', '''      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      ${kbHint ? '<div class="qc-kb">⌨ 空白／Enter 顯示｜← → 換題<a href="#" onclick="hideKb();return false">知道了</a></div>' : ''}
      <div class="qc-btns">''')
rep('''        <div>${c.answer}</div>
        ${pmtHtml(c)}
        <div class="src">📌 ${c.src}</div>''', '''        ${isEs(c)?'':`<div>${c.answer}</div>`}
        ${pmtHtml(c)}
        <div class="src">📌 ${srcHtml(c.src,c.chId)}</div>
        ${es5Html(c)}''')
# 逐格點完也算全部顯示
rep('''    val.style.display = ''; mask.style.display = 'none';
    el.classList.add('revealed');
  }
}''', '''    val.style.display = ''; mask.style.display = 'none';
    el.classList.add('revealed');
    if (!document.querySelector('#quiz-card-area .blank:not(.revealed)')) revealAllQuizBlanks('q' + quizIdx);
  }
}''')
# 記進度抽成 quizMarkDone()
rep('''  // 隨機測驗也要計入完成（與章節瀏覽共用 bxj-fill）
      try{
        var _c = quizQueue[quizIdx];
        if(_c && _c.key && !cardDone[_c.key]){
          cardDone[_c.key] = true;
          window.BXREP && BXREP.fillMark(_c.key);
          var _b = document.getElementById('rb-'+_c.key);
          if(_b){ _b.textContent='✓ 完成'; _b.classList.add('done'); }
          updProg(_c.chId);
        }
      }catch(e){}
    }''', '''  quizMarkDone();
}
/* 隨機測驗：這題空格全部顯示＝記為「已確認」（key＝章節id-序號，與章節瀏覽共用 bxj-fill） */
function quizMarkDone() {
  const c = quizQueue[quizIdx];
  if (!c || !c.key) return;
  try { window.BXREP && BXREP.fillMark(c.key); } catch (e) {}
  if (!cardDone[c.key]) {
    cardDone[c.key] = true;
    const b = document.getElementById('rb-' + c.key);
    if (b) { b.textContent = '✓ 完成'; b.classList.add('done'); }
    updProg(c.chId);
  }
}''')
# 換題捲到題目開頭
rep('''function nextQuiz() {
  quizIdx++;
  renderQuizCard();
  window.scrollTo({top:0,behavior:'smooth'});
}''', '''function quizScrollTop(){const el=document.getElementById('quiz-progress');if(!el)return;const y=el.getBoundingClientRect().top+window.scrollY-8;window.scrollTo({top:Math.max(0,y),behavior:'auto'})}
function nextQuiz() {
  quizIdx++;
  renderQuizCard();
  quizScrollTop();
}''')
rep('''    quizIdx--;
    renderQuizCard();
    window.scrollTo({top:0,behavior:'smooth'});''', '''    quizIdx--;
    renderQuizCard();
    quizScrollTop();''')
# 鍵盤
rep('''// ===主題切換===''', '''// ===隨機測驗鍵盤：空白鍵／Enter＝顯示一個（全部顯示後＝下一題；整輪做完＝再來一輪）、← 上一題、→ 下一題===
(function(){
  function active(){var q=document.getElementById('quiz-mode');return q&&q.classList.contains('active')}
  function onKey(e,up){
    if(!active()||e.ctrlKey||e.metaKey||e.altKey)return;
    var k=e.key,t=e.target,tag=t&&t.tagName;
    if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||(t&&t.isContentEditable))return;
    if(k!==' '&&k!=='Enter'&&k!=='ArrowLeft'&&k!=='ArrowRight')return;
    e.preventDefault();
    if(up||e.repeat)return;
    if(document.activeElement&&document.activeElement!==document.body&&document.activeElement.blur)document.activeElement.blur();
    if(k==='ArrowLeft'){prevQuiz();return}
    if(k==='ArrowRight'){if(quizIdx<quizQueue.length)nextQuiz();return}
    if(quizIdx>=quizQueue.length){startQuizRound();return}
    var qid='q'+quizIdx;
    if(document.querySelectorAll('#qblank-'+qid+' .blank:not(.revealed)').length===0)nextQuiz();
    else revealOneQuizBlank(qid);
  }
  document.addEventListener('keydown',function(e){onKey(e,false)});
  document.addEventListener('keyup',function(e){if(e.key===' '||e.key==='Enter')onKey(e,true)});
})();

// ===主題切換===''')
rep("    updateThemeBtn(saved || 'light');", "    updateThemeBtn(saved || ((window.matchMedia && matchMedia('(prefers-color-scheme:dark)').matches) ? 'dark' : 'light'));")
rep("randAllBtn.onclick = () => setMode('quiz');", "randAllBtn.onclick = () => goDefQuiz();")
rep("""  const all = DATA.reduce((n,c)=>n+c.cards.length,0);
  const allDone = DATA.reduce((n,c)=>n+c.cards.filter((_,i)=>cardDone[c.id+'-'+i]).length,0);
  const tt = document.getElementById('fillTotal');
  if(tt) tt.textContent = '全部已完成 '+allDone+' / '+all+' 張（'+Math.round(allDone/all*100)+'%）';""", """  const DF = DATA.filter(c=>c.id[0]!=='S'), DS = DATA.filter(c=>c.id[0]==='S');
  const cntA = a=>a.reduce((n,c)=>n+c.cards.length,0), cntD = a=>a.reduce((n,c)=>n+c.cards.filter((_,i)=>cardDone[c.id+'-'+i]).length,0);
  const all = cntA(DF), allDone = cntD(DF), es = cntA(DS), esDone = cntD(DS);
  const tt = document.getElementById('fillTotal');
  if(tt) tt.textContent = '定義填空已完成 '+allDone+' / '+all+' 張（'+Math.round(allDone/all*100)+'%）｜申論四段 '+esDone+' / '+es+' 張';""")
open(P, 'w', encoding='utf-8').write(f)
print('ok')
