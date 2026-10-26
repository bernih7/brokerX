# 由經紀法規 quiz/tpl.html 改出民法版 tpl.html（一次性；之後直接改 tpl.html 即可）
import re,os,shutil
H=os.path.dirname(os.path.abspath(__file__))
src=os.path.join(H,'..','essay_jj','quiz','tpl.html')
s=open(src,encoding='utf-8').read()
def R(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n>=1,('MISSING',a[:60])
    if cnt==1: assert n==1,('MULTI',n,a[:60])
    s=s.replace(a,b)
R('<title>經紀法規｜法條解析練習</title>','<title>民法｜法條解析練習</title>')
s=re.sub(r'--cA:#2F5D50;--cAs:#DDEBE5;.*?--cHs:#E1F1E8;','--cA:#2F5D50;--cAs:#DDEBE5;--cB:#3A5A7A;--cBs:#E3EBF3;--cC:#8A5517;--cCs:#F7E6CC;--cD:#7A5BA6;--cDs:#EBE3F6;--cE:#A8402B;--cEs:#F8E1DC;',s,count=1,flags=re.S)
s=re.sub(r'--cA:#84C2AE;--cAs:#22362F;.*?--cHs:#1E3024;','--cA:#84C2AE;--cAs:#22362F;--cB:#8DB0CE;--cBs:#1E2A36;--cC:#D9A863;--cCs:#3A2F1C;--cD:#B9A3DC;--cDs:#2B2338;--cE:#E8806A;--cEs:#3A221D;',s,flags=re.S)
R('.cat{border-radius:11px;padding:9px 11px;margin-bottom:9px;border-left:5px solid}','.cat{border-radius:11px;padding:9px 11px;margin-bottom:9px;border:1px solid var(--line)}\n.tip{background:var(--acc-soft);border:1px solid var(--acc);border-radius:10px;padding:8px 11px;font-size:.86rem;line-height:1.7;margin-top:8px}\n.tip b{color:var(--acc-ink)}\n.tip p{margin:2px 0}\n.lawb a{color:var(--pri);font-size:.74rem;margin-left:6px}')
R('<h1>經紀法規｜法條解析練習</h1>','<h1>民法｜法條解析練習</h1>')
R('<div class="sub">99–114 年官方試題 518 題（另 2 題法源已廢止，不列入）・可選補習班模擬卷 25 題・逐選項解析・本題相關法條・錯誤類型 A/B/C/D</div>','<div class="sub">99–114 年官方試題 520 題・28 小類・逐選項解析・本題相關法條・錯誤類型 A/B/C/D・與刷題 A～E 篇共用作答紀錄</div>')
R('''    <div class="row" style="margin-bottom:9px;align-items:center">
      <button class="btn" id="mkToggle">加入補習班模擬卷 25 題</button>
      <span class="nv" id="mkHint"></span>
    </div>
''','')
R('<p class="hint">讀共用作答紀錄的「最近一次答錯」。題庫 12 頁與本頁共用，<b>在任何一頁答對就會移出</b>。</p>','<p class="hint">讀共用作答紀錄的「最近一次答錯」。刷題 A～E 篇、25 題模擬測驗與本頁共用，<b>在任何一頁答對就會移出</b>。</p>')
R('''      <button class="btn" id="onlyMock">只練補習班模擬卷 25 題</button>
''','')
R('<div id="memBox"></div>','<div id="memBox"></div><div id="tipBox"></div>')
R('<script src="bxj-use.js"></script>','<script src="bxm-use.js"></script>')
R("var CAT={A:'A 不動產經紀業管理條例',C:'C 不動產說明書',D:'D 定型化契約',E:'E 公寓大廈管理條例',F:'F 規約範本',G:'G 公平交易法',H:'H 消費者保護法'};",
  "var CAT={A:'A 民法總則',B:'B 債編總論',C:'C 債編分則',D:'D 物權',E:'E 親屬與繼承'};")
R("function qid(q){return q.ch+'-'+q.y+'-'+q.n}  /* 模擬題 y=0，id 與官方不會相撞 */","function qid(q){return q.p+'-'+q.y+'-'+q.n}  /* 共用紀錄 bxm-q2 的 id＝刷題篇別-年-題（小類 ch 只用來分組） */")
R("function db(){return ld('bxj-q2',{})}","function db(){return ld('bxm-q2',{})}")
R("/* 作答寫入：優先用 bxj-use.js 的 BXREP，格式才會與題庫 12 頁一致 */","/* 作答寫入：優先用 bxm-use.js 的 BXREP，格式才會與刷題 A～E 篇一致 */")
R("if(window.BXREP&&BXREP.rec){try{BXREP.rec({chapter:q.ch,year:q.y,qnum:q.n},chosen,ok);return}catch(e){}}","if(window.BXREP&&BXREP.rec){try{BXREP.rec({chapter:q.p,year:q.y,num:q.n},chosen,ok);return}catch(e){}}")
R("DB[id]=r;sv('bxj-q2',DB);","DB[id]=r;sv('bxm-q2',DB);")
R("if(window.BXREP&&BXREP.tag){try{BXREP.tag({chapter:q.ch,year:q.y,qnum:q.n},k);return}catch(e){}}","if(window.BXREP&&BXREP.tag){try{BXREP.tag({chapter:q.p,year:q.y,num:q.n},k);return}catch(e){}}")
R("r.k=k;r.g=(k==='D')?1:0;sv('bxj-q2',DB);","r.k=k;r.g=(k==='D')?1:0;sv('bxm-q2',DB);")
R("var HL_K=/無效|不構成契約之內容|視為|推定|連帶|撤銷|廢止|準用/g;","var HL_K=/無效|得撤銷|效力未定|不得對抗|視為|推定|連帶|準用/g;")
R("var HLL_K=/得連續處罰|按次連續處罰|按次處罰|應令其限期改正|得令其限期改善|令其限期改善|經制止而不遵從|屆期未改正|屆期不改善|屆期仍不|勒令停業|停止營業|應廢止|得廢止|視為|無效|不得規避、妨礙或拒絕/g;",
  "var HLL_K=/非經登記，不生效力|不得對抗|不生效力|視為|推定|無效|連帶|準用/g;")
R("function accept(q){return q.dis?q.dis.acc:[q.ans]}","function accept(q){return q.free?['A','B','C','D']:q.acc}")
R("function isFree(q){return !!(q.sp||isOos(q)||(q.dis&&q.dis.kind==='free'))}","function isFree(q){return !!q.free}")
R("function isMock(q){return q.sr==='mock'}","function isMock(q){return false}")
R("var sel=new Set(Object.keys(CT)), ord=ld('bxj-ord','new'), num=30, useTm=false;\nvar useMock=ld('bxj-mock',0)?1:0;","var sel=new Set(Object.keys(CT)), ord=ld('bxm-anal-ord','new'), num=30, useTm=false;\nvar useMock=0;")
R("var WCLR=ld('bxj-wclr',0);","var WCLR=ld('bxm-wclr',0);")
a=s.index('function renderMk(){');b=s.index("document.getElementById('selAll')")
s=s[:a]+'function renderMk(){}\n'+s[b:]
a=s.index("document.getElementById('onlyMock').onclick");b=s.index("document.getElementById('clrWrong')")
s=s[:a]+s[b:]
R("sel=new Set(a.map(function(x){return x[0]}));renderCats();","sel=new Set(a.filter(function(x){return x[1]>0}).map(function(x){return x[0]}));if(!sel.size){alert('目前還沒有錯題紀錄');sel=new Set(Object.keys(CT))}renderCats();")
R("ord=b.dataset.ord;sv('bxj-ord',ord);renderOrd()","ord=b.dataset.ord;sv('bxm-anal-ord',ord);renderOrd()")
R("WCLR=Math.floor(Date.now()/1000);sv('bxj-wclr',WCLR);","WCLR=Math.floor(Date.now()/1000);sv('bxm-wclr',WCLR);")
R("""  h+='<tr><td><b>補習班模擬卷合計</b></td><td>'+sm.tot+'</td><td>'+sm.a+'</td><td>'+sm.ok+'</td><td>'+sm.w+'</td><td>'+(sm.a?Math.round(sm.ok/sm.a*100)+'%':'—')+'</td></tr>';
""","")
R("<td><b>官方歷屆合計</b>","<td><b>合計</b>")
s=s.replace("'bxj-anal-log'","'bxm-anal-log'")
R("""(isMock(q)?'<span class="srcmk">補習班模擬卷</span><span>曾榮耀模擬試題一 第 '+q.n+' 題</span>'
             :'<span>'+q.y+' 年 第 '+q.n+' 題</span>')+""","""'<span>'+q.y+' 年 第 '+q.n+' 題</span><span class="nv">'+esc(CT[q.ch]||'')+'</span>'+""")
R("""  if(q.dis) dbh+='<div class="dis"><b>'+(q.dis.kind==='free'?'考選部一律給分':(q.dis.kind==='dual'?'爭議題：官方答案與條文衝突，兩解皆判對':'爭議題：維持官方答案'))+
    '</b><br>'+rich(q.dis.why)+'</div>';""","""  if(q.note) dbh+='<div class="dis"><b>提醒</b><br>'+hl(q.note,1)+'</div>';""")
a=s.index("  var lb=document.getElementById('lawBox');");b=s.index("  var mb=document.getElementById('memBox');")
s=s[:a]+"""  var lb=document.getElementById('lawBox');
  if(q.law&&q.law.length){
    var lh='';
    q.law.forEach(function(k){var L=LAW[k];if(!L)return;
      lh+='<h5>民法 §'+esc(k)+'<a href="https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=B0000001&flno='+encodeURIComponent(k)+'" target="_blank" rel="noopener">全國法規資料庫 ↗</a></h5>'+
          L.x.split('\\n').map(function(p){return '<p>'+hlLaw(p)+'</p>'}).join('')+
          (L.n?'<p class="nv">⚠ '+esc(L.n)+'</p>':'')});
    lb.innerHTML='<details class="law"><summary>本題相關法條（'+q.law.length+' 條）</summary><div class="lawb">'+lh+
      '<p class="nv" style="margin-top:7px">條文取自《民法_現行條文核實表》與補遺；條號依本題題目、選項、解析出現者挑選。</p></div></details>';
  } else lb.innerHTML='';
"""+s[b:]
R("""  } else mb.innerHTML='';
""","""  } else mb.innerHTML='';
  document.getElementById('tipBox').innerHTML=q.tip&&q.tip.length?'<div class="tip"><b>重點</b>'+q.tip.map(function(t){return '<p>'+hl(t,1)+'</p>'}).join('')+'</div>':'';
""")
assert 'bxj' not in s, [m.start() for m in re.finditer('bxj',s)]
open(os.path.join(H,'tpl.html'),'w',encoding='utf-8').write(s)
print('tpl ok')
