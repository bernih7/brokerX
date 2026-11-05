# -*- coding: utf-8 -*-
"""估價《定義填空練習》：施工單《定義填空整套_20261105》一～六節。可重跑。
- 第一節 鍵盤（空白／Enter 顯示一格、全部顯示後再按＝下一題、← →）＋可關提示（bxv-fill-kb）
- 第二節 隨機測驗全部顯示＝記 bxv-fill（頁面原本就有，這裡只保留）；換題捲到題目開頭
- 第五節 申論四段填空 S1～S7（ES_DATA，資料在 es_cards.py）＋「📝 申論隨機」頁籤（#essay）＋同型題 5 分鐘練習連結
- 出處條號連全國法規資料庫（技術規則 D0060077、地價調查估計規則 D0060005）
- 頁首題數：定義與申論四段分開計算（bxv-fill-total／bxv-fill-es-total）
第三、四節補卡直接寫在頁面 DATA（見 gap_cards.py）。"""
import json, os, re, sys, html
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, H)
from es_cards import S
P = os.path.join(ROOT, '估價_定義填空練習.html')
RS = open(os.path.join(ROOT, '估價_申論5分鐘_推理版.html'), encoding='utf-8').read()
SP = open(os.path.join(ROOT, '估價_申論5分鐘衝刺.html'), encoding='utf-8').read()
ES = open(os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html'), encoding='utf-8').read()
RID = set(re.findall(r'"id": ?"([^"]+)"', RS)); SID = set(re.findall(r'"id": ?"([^"]+)"', SP))
EID = set(re.findall(r'<div class="essay-card[^"]*"[^>]*\bid="([^"]+)"', ES))
CN = '一二三四五'
def lab(k):
    m = re.match(r'e(\d+)-(\d)$', k)
    if m: return '%s-%s' % (m.group(1), CN[int(m.group(2)) - 1])
    m = re.match(r'pred-(\d+)$', k)
    if m: return '預%s' % m.group(1)
    m = re.match(r'mk-c(\d)-(\d)$', k)
    if m: return '模擬卷%s-%s' % (CN[int(m.group(1)) - 1], m.group(2))
    m = re.match(r'mk-ls(\d)$', k)
    if m: return '來勝-%s' % m.group(1)
    raise ValueError(k)
L = [('e1', '問題定義'), ('e2', '法條定義'), ('e3', '問題核心'), ('e4', '結論'), ('e5', '結尾卓見')]
def build_card(x):
    parts = [re.sub(r'；(?![^\[]*\]\])', '；<br>', p) for p in x['parts']]
    secs = ''.join('<div class="esb %s"><span class="esl"%s>%s</span><div class="esc">%s</div></div>'
                   % (L[k][0], ' title="卓見為自編收尾句，非法條"' if k == 4 else '', L[k][1], parts[k]) for k in range(5))
    b = re.sub(r'\[\[(.+?)\]\]', '___', secs); a = re.sub(r'\[\[(.+?)\]\]', r'<span class="key">\1</span>', secs)
    for k in x['off'] + x['oth']:
        assert k in EID, ('申論頁沒有', k)
    es5 = [[lab(k), k if k in RID else '', k if k in SID else ''] for k in x['off'] + x['oth']]
    c = dict(term=x['term'], blank=b, answer=a, src=x['src'], mc=0, essay=len(x['off']),
             esx=[[lab(k), k] for k in x['off']], prl=[[lab(k), k] for k in x['oth']], es5=es5)
    if x['mn']: c['mn'] = x['mn']
    assert b.count('___') == a.count('class="key"'), x['term']
    return c
ESD = []
for n, (label, cards) in enumerate(S.items(), 1):
    ch = dict(id='S%d' % n, label=label, cards=[])
    for i, x in enumerate(cards, 1):
        c = build_card(x); c['cid'] = 'S%d-%02d' % (n, i); ch['cards'].append(c)
    ESD.append(ch)

s = open(P, encoding='utf-8').read()
def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, (s.count(old), old[:80])
    s = s.replace(old, new)

# ── ES_DATA 區塊（每次重寫）
blk = '/*ES_DATA*/const ES_DATA = ' + json.dumps(ESD, ensure_ascii=False, indent=0) + ';/*/ES_DATA*/'
if '/*ES_DATA*/' in s:
    s = re.sub(r'/\*ES_DATA\*/.*?/\*/ES_DATA\*/', lambda m: blk, s, flags=re.S)
else:
    i = s.find('const DATA'); j = s.find('\n];', i) + 3
    s = s[:j] + '\n' + blk + '\n' + s[j:]

if '/*fill-kit*/' not in s:
    # CSS：申論四段卡（配色同申論五分鐘推理版；色票照抄土地法填空頁，--card→--paper、--pri2→--primary）
    CSS = '''/*fill-kit*/
:root{--b1:#2F6B8C;--b1s:#E3EFF6;--b2:#7A5BA6;--b2s:#EEE8F6;--b3:#2F7A55;--b3s:#E1F1E8;--b4:#B8782E;--b4s:#F8EBD3;--hl:#FFE9A8}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--b1:#7DB6D8;--b1s:#1D2F3A;--b2:#B79BE0;--b2s:#2B2438;--b3:#7FCBA0;--b3s:#1D3226;--b4:#E0B070;--b4s:#3A3220;--hl:#5A4A18}}
:root[data-theme="dark"]{--b1:#7DB6D8;--b1s:#1D2F3A;--b2:#B79BE0;--b2s:#2B2438;--b3:#7FCBA0;--b3s:#1D3226;--b4:#E0B070;--b4s:#3A3220;--hl:#5A4A18}
:root[data-theme="light"]{--b1:#2F6B8C;--b1s:#E3EFF6;--b2:#7A5BA6;--b2s:#EEE8F6;--b3:#2F7A55;--b3s:#E1F1E8;--b4:#B8782E;--b4s:#F8EBD3;--hl:#FFE9A8}
.esb{display:grid;gap:4px;margin-top:12px;text-align:left;line-height:1.85;word-break:normal;overflow-wrap:anywhere}
.esb:first-child{margin-top:2px}
.esl{justify-self:start;font-size:.74rem;font-weight:700;border-radius:999px;padding:1px 10px;letter-spacing:.04em;line-height:1.7}
.esb.e1 .esl{background:var(--b2s);color:var(--b2)}
.esb.e2 .esl{background:var(--b1s);color:var(--b1)}
.esb.e3{border:1.5px solid var(--b4);border-radius:14px;padding:10px 14px;background:var(--paper)}
.esb.e3 .esl{background:none;padding:0;color:var(--b4)}
.esb.e4 .esl{background:var(--b3s);color:var(--b3)}
.esb.e5{background:var(--hl);border-radius:12px;padding:10px 14px}
.esb.e5 .esl{background:none;padding:0;color:var(--muted)}
.esb.e5 .esc{font-weight:700}
.esb .blank{line-height:1.6}
.es5{margin-top:10px;padding:10px 12px;border:1px dashed var(--line);border-radius:12px;font-size:13px;line-height:1.9}
.es5 b{display:block;font-size:12px;color:var(--muted);margin-bottom:2px}
.es5 .ch5{display:inline-flex;align-items:center;gap:6px;margin:2px 8px 2px 0;white-space:nowrap}
.es5 a.r{font-weight:700;color:var(--primary);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:1px 10px;background:var(--paper)}
.es5 a.s{font-size:12px;color:var(--muted)}
.es-mn{margin-top:8px;font-size:13px}.es-mn b{color:var(--mn);margin-right:6px}
.es-row{text-align:left;margin:2px 0}.es-row a{color:var(--blue)}
a.lawlk{color:inherit;text-decoration:underline dotted;text-underline-offset:3px}
.cp-sep{flex-basis:100%;font-size:12px;font-weight:700;color:var(--gold);margin:10px 0 2px;padding-top:8px;border-top:1px dashed currentColor;text-align:center}
.qc-kb{font-size:12px;color:var(--muted);text-align:center;margin:-4px 0 10px}
.qc-kb a{color:var(--blue);margin-left:6px}
'''
    rep('/* theme-fix: dark contrast */\n</style>', '/* theme-fix: dark contrast */\n' + CSS + '</style>')
    # 頁籤
    rep('<button class="mode-tab" id="tab-quiz" onclick="setMode(\'quiz\')">🎲 隨機測驗</button>',
        '<button class="mode-tab" id="tab-quiz" onclick="goDefQuiz()">🎲 隨機測驗</button>\n  <button class="mode-tab" id="tab-essay" onclick="goEssay()">📝 申論隨機</button>')
    rep('<div class="sub">章節練習 + 隨機測驗模式｜全科 <span id="fillTotal">116</span> 題</div>',
        '<div class="sub">章節練習 + 隨機測驗模式｜定義 <span id="fillTotal">116</span> 題＋申論四段 <span id="fillEsTotal">0</span> 題（另一分類）</div>')
    rep('<div class="fill-done" id="fillDone">已完成 0／116</div>', '<div class="fill-done" id="fillDone">已完成 0／116</div> <div class="fill-done" id="fillEsDone">申論四段 0／0</div>')
    # 排序：只排定義章；申論四段章接在後面、保留撰寫順序
    rep('DATA.sort((a,b)=>b._s-a._s);',
        "DATA.sort((a,b)=>b._s-a._s);\nES_DATA.forEach(ch=>{ch.cards.forEach(c=>{c._s=0;c._t=0;});ch._mc=0;ch._es=ch.cards.reduce((x,c)=>x+(c.essay||0),0);ch._s=0;ch._t=4;ch.es=1;DATA.push(ch);});")
    rep("const HEAT_CH={1:'★★★',2:'★★',3:'★',4:''},HEAT_CARD={1:'高頻',2:'常考',3:'一般'};",
        r"""const HEAT_CH={1:'★★★',2:'★★',3:'★',4:''},HEAT_CARD={1:'高頻',2:'常考',3:'一般'};
const LAWPC={'技術規則':'D0060077','地價調查估計規則':'D0060005','地價調查':'D0060005'};
const LAWKEYS=Object.keys(LAWPC).sort(function(a,b){return b.length-a.length});
// 出處條號連全國法規資料庫：本頁條號除另寫法名者外都是不動產估價技術規則（只處理 HTML 標籤以外的文字）
function srcHtml(t){var cur='D0060077',inA=false;return String(t).split(/(<[^>]+>)/).map(function(seg){if(seg.charAt(0)==='<'){if(/^<a\b/i.test(seg))inA=true;else if(/^<\/a>/i.test(seg))inA=false;return seg;}if(inA)return seg;
 return seg.replace(/([一-龥]*)§(\d+)(?:-(\d+))?/g,function(m,nm,no,sub){if(nm){var hit=null;for(var i=0;i<LAWKEYS.length;i++){if(nm.slice(-LAWKEYS[i].length)===LAWKEYS[i]){hit=LAWPC[LAWKEYS[i]];break}}if(hit)cur=hit;else if(/辦法|條例|土地法|細則/.test(nm))cur=null;}
 if(!cur)return m;var rg=sub&&(+sub>+no);if(rg){var z=sub;sub=null}return nm+'<a class="lawlk" target="_blank" rel="noopener" href="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode='+cur+'&flno='+no+(sub?'-'+sub:'')+'">§'+no+(sub?'-'+sub:'')+'</a>'+(rg?'-'+z:'')})}).join('')}
function isEs(c){return String(c.answer).indexOf('class="esb')>=0}
function es5Html(c){if(!c.es5||!c.es5.length)return'';return'<div class="es5"><b>⏱ 同型題・申論五分鐘練習</b>'+c.es5.map(function(e){var r=e[1]?'<a class="r" target="_blank" rel="noopener" href="估價_申論5分鐘_推理版.html#q='+encodeURIComponent(e[1])+'">'+e[0]+' 推理 ▸</a>':'<span>'+e[0]+'</span>';var s=e[2]?'<a class="s" target="_blank" rel="noopener" href="估價_申論5分鐘衝刺.html#q='+encodeURIComponent(e[2])+'">衝刺</a>':'';return'<span class="ch5">'+r+s+'</span>'}).join('')+'</div>'}
function esStat(c){var EP='不動產估價概要_申論題實戰範文.html#',r=[];
 if((c.esx||[]).length)r.push('<div class="es-row">官方申論考過 <strong>'+c.esx.length+'</strong> 次：'+c.esx.map(function(x){return '<a target="_blank" rel="noopener" href="'+EP+x[1]+'">'+x[0]+' ↗</a>'}).join('、')+'</div>');
 if((c.prl||[]).length)r.push('<div class="es-row">同型預測／模擬：'+c.prl.map(function(x){return '<a target="_blank" rel="noopener" href="'+EP+x[1]+'">'+x[0]+' ↗</a>'}).join('、')+'</div>');
 return r.length?r.join(''):'尚無官方申論紀錄'}
function esExtra(c){return (c.mn?'<div class="es-mn"><b>口訣</b>'+c.mn+'</div>':'')+es5Html(c)}""")
    # 章節選單：申論四段前加分隔標題；章首說明
    rep("DATA.forEach((ch,ci)=>{\n  const btn = document.createElement('button');\n  btn.className = 'nav-btn h'+ch._t",
        "DATA.forEach((ch,ci)=>{\n  if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（另一分類：定義→法條→核心→結論＋卓見）';nav.appendChild(sp);}\n  const btn = document.createElement('button');\n  btn.className = 'nav-btn h'+ch._t")
    rep("<div class=\"ch-heat\">歷屆：選擇 ${ch._mc} 題・申論 ${ch._es} 題（本頁已依考頻由高到低排列）</div>",
        "<div class=\"ch-heat\">${ch.es?'申論四段填空：①問題定義 ②法條定義 ③問題核心 ④結論＋結尾卓見；相似題型合併成一張卡，卡內列官方題與同型預測／模擬題（本章官方申論 '+ch._es+' 題）':'歷屆：選擇 '+ch._mc+' 題・申論 '+ch._es+' 題（本頁已依考頻由高到低排列）'}</div>")
    # 章節瀏覽卡片
    rep("const builtBlank = buildBlankLine(fmtAns(c.blank,true), c.answer, key);",
        "const builtBlank = buildBlankLine(isEs(c)?c.blank:fmtAns(c.blank,true), c.answer, key);")
    rep("const statHtml = statParts.length ? statParts.join('　｜　') : '尚無歷屆出題紀錄';\n    card.innerHTML",
        "const statHtml = isEs(c) ? esStat(c) : (statParts.length ? statParts.join('　｜　') : '尚無歷屆出題紀錄');\n    card.innerHTML")
    rep('<div class="term">${c.term}<span class="heat h${c._t}">${HEAT_CARD[c._t]}</span></div>',
        '<div class="term">${c.term}${HEAT_CARD[c._t]?`<span class="heat h${c._t}">${HEAT_CARD[c._t]}</span>`:\'\'}</div>')
    rep("""        <div class="key-note">${fmtAns(c.answer)}</div>
        <div class="src" style="margin-top:6px;font-size:12px;color:var(--muted)">📌 ${c.src}</div>
      </div>`;""",
        """        ${isEs(c)?'':`<div class="key-note">${fmtAns(c.answer)}</div>`}
        <div class="src" style="margin-top:6px;font-size:12px;color:var(--muted)">📌 ${srcHtml(c.src)}</div>
        ${isEs(c)?esExtra(c):''}
      </div>`;""")
    # 題數：定義與申論四段分開
    rep("const FILL_TOTAL = DATA.reduce((n,ch)=>n+ch.cards.length,0);",
        "const FILL_TOTAL = DATA.filter(ch=>!ch.es).reduce((n,ch)=>n+ch.cards.length,0), FILL_ES_TOTAL = DATA.filter(ch=>ch.es).reduce((n,ch)=>n+ch.cards.length,0);")
    rep("""  const n = Object.keys(cardDone).filter(k=>cardDone[k]).length;
  const el = document.getElementById('fillDone'); if(el) el.textContent = '已完成 '+n+'／'+FILL_TOTAL;
  const t = document.getElementById('fillTotal'); if(t) t.textContent = FILL_TOTAL;""",
        """  const ks = Object.keys(cardDone).filter(k=>cardDone[k]), ne = ks.filter(k=>k.charAt(0)==='S').length, n = ks.length-ne;
  const el = document.getElementById('fillDone'); if(el) el.textContent = '已完成 '+n+'／'+FILL_TOTAL;
  const t = document.getElementById('fillTotal'); if(t) t.textContent = FILL_TOTAL;
  const e2 = document.getElementById('fillEsDone'); if(e2) e2.textContent = '申論四段 '+ne+'／'+FILL_ES_TOTAL;
  const t2 = document.getElementById('fillEsTotal'); if(t2) t2.textContent = FILL_ES_TOTAL;""")
    rep("try{ localStorage.setItem('bxv-fill-total', String(FILL_TOTAL)); }catch(e){}",
        "try{ localStorage.setItem('bxv-fill-total', String(FILL_TOTAL)); localStorage.setItem('bxv-fill-es-total', String(FILL_ES_TOTAL)); }catch(e){}")
    # 模式切換：申論隨機
    rep("    tabB.classList.add('on'); tabQ.classList.remove('on');\n  } else {",
        "    tabB.classList.add('on'); tabQ.classList.remove('on'); document.getElementById('tab-essay').classList.remove('on');\n  } else {")
    rep("    tabB.classList.remove('on'); tabQ.classList.add('on');\n    initQuiz();",
        "    tabB.classList.remove('on'); tabQ.classList.add('on'); document.getElementById('tab-essay').classList.remove('on');\n    initQuiz();")
    rep("randAllBtn.onclick = () => setMode('quiz');", "randAllBtn.onclick = () => goDefQuiz();")
    # 題庫帶申論欄位
    rep("quizPool.push({ cid: c.cid, chN: ch.cards.length, chId: ch.id, chLabel: ch.label, term: c.term, blank: c.blank, answer: c.answer, src: c.src, mc: c.mc||0, essay: c.essay||0 });",
        "quizPool.push({ cid: c.cid, chN: ch.cards.length, chId: ch.id, chLabel: ch.label, term: c.term, blank: c.blank, answer: c.answer, src: c.src, mc: c.mc||0, essay: c.essay||0, esx: c.esx||[], prl: c.prl||[], es5: c.es5||[], mn: c.mn||'' });")
    rep("""    DATA.forEach(ch => {
      const btn = document.createElement('button');
      btn.className = 'qf-btn';""",
        """    DATA.forEach(ch => {
      if(ch.id==='S1'){const sp=document.createElement('div');sp.className='cp-sep';sp.textContent='📝 申論四段填空（「全部章節」不含，需另選）';filterEl.appendChild(sp);}
      const btn = document.createElement('button');
      btn.className = 'qf-btn';""")
    rep("  const pool = quizFilter.size === 0 ? quizPool : quizPool.filter(c => quizFilter.has(c.chId));",
        "  const pool = quizFilter.size === 0 ? quizPool.filter(c => c.chId.charAt(0) !== 'S') : quizPool.filter(c => quizFilter.has(c.chId));")
    rep("  if(!quizFilter.size)return '全部章節';", "  if(!quizFilter.size)return '全部章節';\n  const es=DATA.filter(c=>c.es).map(c=>c.id);if(es.length&&quizFilter.size===es.length&&es.every(id=>quizFilter.has(id)))return '申論四段（全部）';")
    # 跑完一輪：申論隨機不計入定義填空輪數
    rep("      var fc=parseInt(localStorage.getItem('bxe-fill')||'0')+1;\n      localStorage.setItem('bxe-fill',fc);",
        "      if(![...quizFilter].some(id=>id.charAt(0)==='S')){var fc=parseInt(localStorage.getItem('bxe-fill')||'0')+1;\n      localStorage.setItem('bxe-fill',fc);}")
    # 隨機測驗卡
    rep("  const builtBlank = fmtAns(c.blank,true).replace(/___/g, () => {",
        "  const builtBlank = (isEs(c)?c.blank:fmtAns(c.blank,true)).replace(/___/g, () => {")
    rep("""  const statHtml = statParts.length ? statParts.join('　｜　') : '尚無歷屆出題紀錄';

  area.innerHTML""", """  const statHtml = isEs(c) ? esStat(c) : (statParts.length ? statParts.join('　｜　') : '尚無歷屆出題紀錄');

  area.innerHTML""")
    rep("""      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      <div class="qc-btns">""", """      <div class="qc-blank" id="qblank-${qid}">${builtBlank}</div>
      ${kbHint ? '<div class="qc-kb">⌨ 空白／Enter 顯示｜← → 換題<a href="#" onclick="hideKb();return false">知道了</a></div>' : ''}
      <div class="qc-btns">""")
    rep("""        <div class="key-note">${fmtAns(c.answer)}</div>
        <div class="src">📌 ${c.src}</div>
      </div>""", """        ${isEs(c)?'':`<div class="key-note">${fmtAns(c.answer)}</div>`}
        <div class="src">📌 ${srcHtml(c.src)}</div>
        ${isEs(c)?esExtra(c):''}
      </div>""")
    # 換題不回頁首：捲到題目開頭
    rep("""function nextQuiz() {
  quizIdx++;
  renderQuizCard();
  window.scrollTo({top:0,behavior:'smooth'});
}""", """function quizScrollTop(){const el=document.getElementById('quiz-progress');if(!el)return;const y=el.getBoundingClientRect().top+window.scrollY-8;window.scrollTo({top:Math.max(0,y),behavior:'auto'})}
function nextQuiz() {
  quizIdx++;
  renderQuizCard();
  quizScrollTop();
}""")
    rep("""    quizIdx--;
    renderQuizCard();
    window.scrollTo({top:0,behavior:'smooth'});""", """    quizIdx--;
    renderQuizCard();
    quizScrollTop();""")
    # 鍵盤＋提示＋申論隨機＋#essay
    rep("// theme handled by themeToggle block below\n</script>", r"""// theme handled by themeToggle block below

// ===鍵盤提示（可關，bxv-fill-kb）===
let kbHint = true; try { kbHint = localStorage.getItem('bxv-fill-kb') !== '1'; } catch (e) {}
function hideKb() { kbHint = false; try { localStorage.setItem('bxv-fill-kb', '1'); } catch (e) {} document.querySelectorAll('.qc-kb').forEach(e => e.remove()); }

// ===申論隨機（只出 S 章）與定義隨機（不含 S 章）===
function qfSync(){
  document.querySelectorAll('.qf-btn').forEach(b=>{const q=b.dataset.q;b.classList.toggle('on',q==='ALL'?quizFilter.size===0:quizFilter.has(q));});
  const t=document.getElementById('qftog');if(t)t.innerHTML='📑 章節：<b>'+quizFilterLabel()+'</b> '+(document.getElementById('quiz-filter').classList.contains('open')?'▴':'▾');
}
function goEssay(){
  setMode('quiz'); quizFilter.clear(); DATA.forEach(c=>{if(c.es)quizFilter.add(c.id)}); qfSync(); startQuizRound();
  document.getElementById('tab-quiz').classList.remove('on'); document.getElementById('tab-essay').classList.add('on');
}
function goDefQuiz(){
  const wasEs=document.getElementById('tab-essay').classList.contains('on')||[...quizFilter].some(id=>id.charAt(0)==='S');
  setMode('quiz'); if(wasEs){quizFilter.clear();qfSync();startQuizRound();}
}
try{ if(location.hash==='#essay') setTimeout(goEssay,0); addEventListener('hashchange',()=>{if(location.hash==='#essay')goEssay()}); }catch(e){}

// ===隨機測驗鍵盤：空白鍵／Enter＝顯示一格（全部顯示後＝下一題；整輪做完＝再來一輪）、← 上一題、→ 下一題 ===
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
    if(quizIdx>=quizQueue.length){startQuizRound();quizScrollTop();return}
    var qid='q'+quizIdx;
    if(document.querySelectorAll('#qblank-'+qid+' .blank:not(.revealed)').length===0)nextQuiz();
    else revealOneQuizBlank(qid);
  }
  document.addEventListener('keydown',function(e){onKey(e,false)});
  document.addEventListener('keyup',function(e){if(e.key===' '||e.key==='Enter')onKey(e,true)});
})();
</script>""")

open(P, 'w', encoding='utf-8').write(s)
n = sum(len(c['cards']) for c in ESD)
print('申論四段', len(ESD), '章', n, '張；es5 連結', sum(len(c['es5']) for ch in ESD for c in ch['cards']))
cov = sorted(set(k for ch in ESD for c in ch['cards'] for _, k in c['esx']))
print('官方題涵蓋', len(cov), '/', len([e for e in EID if e.startswith('e')]), sorted(set(e for e in EID if e.startswith('e')) - set(cov)))
