# -*- coding: utf-8 -*-
"""民法《定義填空練習》介面（比照土地法 v714～v723、經紀法規 v726）：鍵盤、隨機記進度、申論隨機頁籤、申論四段卡版面、
五分鐘練習連結、條號連全國法規、換題不回頁首、載入還原進度。只改 DATA 以外程式；有 /*civfill-v2*/ 標記就不重複套用。"""
import os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
P = os.path.join(ROOT, '民法_定義填空練習.html')
f = open(P, encoding='utf-8').read()
if '/*civfill-v2*/' in f:
    print('已套用'); raise SystemExit
def rep(a, b, cnt=1):
    global f
    assert f.count(a) == cnt, (f.count(a), a[:90])
    f = f.replace(a, b)
CSS = open(os.path.join(H, 'css.txt'), encoding='utf-8').read()
rep('</style>\n<script src="bxm-use.js"></script>', CSS + '\n</style>\n<script src="bxm-use.js"></script>')

rep('''  <button class="mode-tab on" id="tab-browse" onclick="setMode('browse')">📖 章節瀏覽</button>
  <button class="mode-tab" id="tab-quiz" onclick="setMode('quiz')">🎲 隨機測驗</button>''',
'''  <button class="mode-tab on" id="tab-browse" onclick="setMode('browse')">📖 章節瀏覽</button>
  <button class="mode-tab" id="tab-quiz" onclick="goDefQuiz()">🎲 隨機測驗</button>
  <button class="mode-tab" id="tab-essay" onclick="goEssay()">📝 申論隨機</button>''')

# 解析面板：申論四段卡不重複印答案；條號連結；五分鐘練習
rep('''function ansHtml(c){
  let h='<div class="an-full">'+c.answer+'</div>';''', '''function isEs(c){return String(c.answer).indexOf('class="esb')>=0}
function es5Html(c){if(!c.es5||!c.es5.length)return'';return'<div class="es5"><b>⏱ 同型題・申論五分鐘練習</b>'+c.es5.map(function(e){var r=e[1]?'<a class="r" target="_blank" rel="noopener" href="民法_申論5分鐘_推理版.html#q='+encodeURIComponent(e[1])+'">'+e[0]+' 推理 ▸</a>':'<span>'+e[0]+'</span>';var s=e[2]?'<a class="s" target="_blank" rel="noopener" href="民法_申論5分鐘衝刺.html#q='+encodeURIComponent(e[2])+'">衝刺</a>':'';return'<span class="ch5">'+r+s+'</span>'}).join('')+'</div>'}
const LAWPC={'民法':'B0000001','土地法':'D0060001','租賃住宅條例':'D0060125'};
function srcHtml(t){var cur='B0000001';return String(t).replace(/([一-龥]*)§(\\d+)(?:-(\\d+))?/g,function(m,nm,no,sub){if(nm){var k=Object.keys(LAWPC).find(function(x){return nm.slice(-x.length)===x});cur=k?LAWPC[k]:null}if(!cur)return m;return nm+'<a class="lawlk" target="_blank" rel="noopener" href="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode='+cur+'&flno='+no+(sub?'-'+sub:'')+'">§'+no+(sub?'-'+sub:'')+'</a>'})}
function ansHtml(c){
  let h=isEs(c)?'':'<div class="an-full">'+c.answer+'</div>';''')
rep("  h+='<div class=\"src\">📌 '+c.src+'</div>';\n  return h;", "  h+='<div class=\"src\">📌 '+srcHtml(c.src)+'</div>'+es5Html(c);\n  return h;")

rep("randAllBtn.onclick = () => setMode('quiz');", "randAllBtn.onclick = () => goDefQuiz();")
rep('''DATA.forEach((ch,ci)=>{
  const btn = document.createElement('button');
  btn.className = 'nav-btn' + (ci===0?' on':'');''', '''DATA.forEach((ch,ci)=>{
  if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（另一分類：定義→法條→核心→結論＋卓見）';nav.appendChild(sp)}
  const btn = document.createElement('button');
  btn.className = 'nav-btn' + (ci===0?' on':''); btn.dataset.id = ch.id;''')
rep("  [...document.querySelectorAll('.nav-btn')].find(b=>b.textContent.startsWith(id)).classList.add('on');",
    "  const nb=document.querySelector('.nav-btn[data-id=\"'+id+'\"]'); if(nb) nb.classList.add('on');")
# 載入還原已確認（章節瀏覽與隨機測驗共用 bxm-fill）
rep('''function toggleBlank(el) {''', '''(function(){
  var fl={};try{fl=JSON.parse(localStorage.getItem('bxm-fill')||'{}')||{}}catch(e){}
  Object.keys(fl).forEach(function(k){if(!(k in cardDone))return;cardDone[k]=true;var b=document.getElementById('rb-'+k);if(b){b.textContent='✓ 完成';b.classList.add('done')}});
  DATA.forEach(function(ch){var n=ch.cards.filter(function(_,i){return cardDone[ch.id+'-'+i]}).length,t=ch.cards.length;var pf=document.getElementById('pf-'+ch.id),pt=document.getElementById('pt-'+ch.id);if(pf)pf.style.width=Math.round(n/t*100)+'%';if(pt)pt.textContent=n+' / '+t});
})();
function toggleBlank(el) {''')

rep('''    tabB.classList.add('on'); tabQ.classList.remove('on');
  } else {''', '''    tabB.classList.add('on'); tabQ.classList.remove('on'); document.getElementById('tab-essay').classList.remove('on');
  } else {''')
rep('''    tabB.classList.remove('on'); tabQ.classList.add('on');
    initQuiz();''', '''    tabB.classList.remove('on'); tabQ.classList.add('on'); document.getElementById('tab-essay').classList.remove('on');
    initQuiz();''')
rep('''      ch.cards.forEach(c => {
        quizPool.push(Object.assign({ chId: ch.id, chLabel: ch.label }, c));''', '''      ch.cards.forEach((c, ci) => {
        quizPool.push(Object.assign({ key: ch.id + '-' + ci, chId: ch.id, chLabel: ch.label }, c));''')
rep("    allBtn.textContent = '全部章節';", "    allBtn.textContent = '全部章節（不含申論四段）';")
rep('''    DATA.forEach(ch => {
      const btn = document.createElement('button');
      btn.className = 'qf-btn';''', '''    DATA.forEach(ch => {
      if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（「全部章節」不含，需另選或按「申論隨機」）';filterEl.appendChild(sp);
        const eb=document.createElement('button');eb.className='qf-btn qf-es';eb.dataset.id='ES';eb.textContent='申論四段全部';eb.onclick=()=>setQuizFilter('ES',eb);filterEl.appendChild(eb)}
      const btn = document.createElement('button');
      btn.className = 'qf-btn'; btn.dataset.id = ch.id;''')
rep("  const pool = quizFilter === 'ALL' ? quizPool : quizPool.filter(c => c.chId === quizFilter);",
    "  const pool = quizFilter === 'ALL' ? quizPool.filter(c => c.chId[0] !== 'S') : quizFilter === 'ES' ? quizPool.filter(c => c.chId[0] === 'S') : quizPool.filter(c => c.chId === quizFilter);")
rep("    if (quizQueue.length === quizPool.length) {", "    if (quizFilter === 'ALL') {")
rep("全部 ' + quizPool.length + ' 題做完才會自動記一輪", "全部 ' + quizPool.filter(c => c.chId[0] !== 'S').length + ' 題定義填空做完才會自動記一輪")
rep('''function startQuizRound() {''', '''function goEssay(){setMode('quiz');const eb=document.querySelector('.qf-btn[data-id="ES"]');if(eb)setQuizFilter('ES',eb);document.getElementById('tab-quiz').classList.remove('on');document.getElementById('tab-essay').classList.add('on')}
function goDefQuiz(){const wasEs=document.getElementById('tab-essay').classList.contains('on');setMode('quiz');if(wasEs||quizFilter==='ES'||(quizFilter[0]==='S'&&quizFilter!=='ALL')){const ab=document.querySelector('.qf-btn.qf-all');if(ab)setQuizFilter('ALL',ab)}}
try{if(location.hash==='#essay')setTimeout(goEssay,0);addEventListener('hashchange',()=>{if(location.hash==='#essay')goEssay()})}catch(e){}
let kbHint = true; try { kbHint = localStorage.getItem('bxm-fill-kb') !== '1'; } catch (e) {}
function hideKb() { kbHint = false; try { localStorage.setItem('bxm-fill-kb', '1'); } catch (e) {} document.querySelectorAll('.qc-kb').forEach(e => e.remove()); }
function startQuizRound() {''')
rep('''      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      ${esRow(c)}''', '''      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      ${kbHint ? '<div class="qc-kb">⌨ 空白／Enter 顯示｜← → 換題<a href="#" onclick="hideKb();return false">知道了</a></div>' : ''}
      ${esRow(c)}''')
rep('''    val.style.display = ''; mask.style.display = 'none';
    el.classList.add('revealed');
  }
}''', '''    val.style.display = ''; mask.style.display = 'none';
    el.classList.add('revealed');
    if (!document.querySelector('#quiz-card-area .blank:not(.revealed)')) revealAllQuizBlanks('q' + quizIdx);
  }
}''')
rep('''  const stat = document.getElementById('qstat-' + qid);
  if (stat) stat.classList.add('show');
}''', '''  const stat = document.getElementById('qstat-' + qid);
  if (stat) stat.classList.add('show');
  quizMarkDone();
}
/* 隨機測驗：這題空格全部顯示＝記為「已確認」（key＝章節id-序號，與章節瀏覽共用 bxm-fill） */
function quizMarkDone() {
  const c = quizQueue[quizIdx];
  if (!c || !c.key) return;
  try { window.BXREP && BXREP.fillMark(c.key); } catch (e) {}
  if (!cardDone[c.key]) {
    cardDone[c.key] = true;
    const b = document.getElementById('rb-' + c.key);
    if (b) { b.textContent = '✓ 完成'; b.classList.add('done'); }
    const ch = DATA.find(x => x.id === c.chId), t = ch.cards.length, n = ch.cards.filter((_, i) => cardDone[c.chId + '-' + i]).length;
    const pf = document.getElementById('pf-' + c.chId), pt = document.getElementById('pt-' + c.chId);
    if (pf) pf.style.width = Math.round(n / t * 100) + '%'; if (pt) pt.textContent = n + ' / ' + t;
  }
}''')
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
rep('''// ===主題切換===''', '''// ===隨機測驗鍵盤：空白鍵／Enter＝顯示一個（全部顯示後＝下一題；整輪做完＝再來一輪）、← 上一題、→ 下一題===
(function(){
  function active(){var q=document.getElementById('quiz-mode');return q&&q.classList.contains('active')}
  function onKey(e,up){
    if(!active()||e.ctrlKey||e.metaKey||e.altKey)return;
    var k=e.key,t=e.target,tag=t&&t.tagName;
    if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT'||(t&&t.isContentEditable))return;
    if(k!==' '&&k!=='Enter'&&k!=='ArrowLeft'&&k!=='ArrowRight')return;
    if(t&&t.closest&&t.closest('summary'))return;
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
open(P, 'w', encoding='utf-8').write(f)
print('ok')
