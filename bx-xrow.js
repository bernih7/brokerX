/* 逐選項解析列（土地法／估價解析版練習共用，2026-11-07，比照民法法條解析練習）
   每列＝字母＋〔本題答案〕＋對在／錯在＋一句重點（有寫才顯示）＋解析（關鍵字黃底／紅字）＋你選的。
   對在／錯在＝這個選項的敘述對不對：題幹問「錯誤／非／不得／不屬…」時，答案那項是「錯在」、其餘「對在」；其他題型相反。
   依賴 bxm-exp.js（bxmExp）。 */
(function(){
  var NEG=/錯誤|不正確|有誤|非(?!公共設施|都市)|不得(?!超過|少於|小於|多於|低於|逾)|不屬|不包括|不包含|不是|不適用(?!.{0,14}之規定)|無(?!理由|間斷)|沒有|不在(?!此限)|不需|不必|不宜|不符|不應|不可|不能|最不/;
  function tail(st){st=String(st||'');var r=/何者|何種|何項|何|哪|那|多少|幾/g,m,last=-1;while((m=r.exec(st)))last=m.index;if(last<0)last=Math.max(0,st.length-14);var t=st.slice(last),q=t.search(/[？?]/);return {t:q>=0?t.slice(0,q):t,i:last}}
  window.bxNegStem=function(stem){
    stem=String(stem||'');try{stem=stem.normalize('NFKC')}catch(e){}  /* PDF 來的相容字（如 U+F967 不）先正規化 */
    var tt=tail(stem),t=tt.t,pre=stem.slice(0,tt.i);
    var n=NEG.test(t.replace(/（[^）]*）|\([^)]*\)/g,''));
    if(/(?:不包含|不包括|不屬於?|不是|非屬)(?:下列)?$/.test(pre))n=true;
    if(/非因(?:下列)?$/.test(pre))n=!n;   /* 「非因下列何種情形，不得…」雙重否定 */
    return n};
  if(!document.getElementById('bx-xrow-css')){var s=document.createElement('style');s.id='bx-xrow-css';s.textContent=
    '.xrs{border:1px solid rgba(120,110,95,.28);border-radius:10px;overflow:hidden;background:var(--card,#FFFEFA)}'+
    '.xrw{display:flex;gap:10px;padding:9px 12px;border-top:1px dashed rgba(120,110,95,.3);line-height:1.7;font-size:.9rem}'+
    '.xrw:first-child{border-top:0}.xrw .xL{flex:none;width:1.5em;font-weight:700;color:#B3261E}.xrw.ok .xL{color:#2E7A45}'+
    '.xrw.ok{background:#EAF3EA}.xrw .xB{flex:1;min-width:0}.xrw .xme{display:inline-block;font-size:.72rem;background:#FBE9D2;color:#8A5517;border-radius:4px;padding:0 6px;margin-left:6px;white-space:nowrap}'+
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .xrw.ok{background:#22302A}:root:not([data-theme="light"]) .xrw .xL{color:#FF8E7E}:root:not([data-theme="light"]) .xrw.ok .xL{color:#8ED3A0}:root:not([data-theme="light"]) .xrw .xme{background:#3A2E1C;color:#E0B070}:root:not([data-theme="light"]) .xrs{background:var(--card,#1F2723)}}'+
    ':root[data-theme="dark"] .xrw.ok{background:#22302A}:root[data-theme="dark"] .xrw .xL{color:#FF8E7E}:root[data-theme="dark"] .xrw.ok .xL{color:#8ED3A0}:root[data-theme="dark"] .xrw .xme{background:#3A2E1C;color:#E0B070}:root[data-theme="dark"] .xrs{background:var(--card,#1F2723)}'+
    /* 11-14 使用者「顏色分配太雜亂」：列內只留兩種顏色——綠＝本題答案、黃底＝關鍵詞（對、錯選項同一種黃底）；對在／錯在、字母、你選的一律中性灰 */
    '.xrs .xrw .xL{color:#8A8378}.xrs .xrw.ok .xL{color:#2E7A45}'+
    '.xrs .xp,.xrs .xp-ok,.xrs .xp-ng{background:transparent;color:#6F685E;border:1px solid rgba(120,110,95,.4);font-weight:600}'+
    '.xrs mark.xk-ng,.xrs mark.xk-ok{color:inherit;background:linear-gradient(transparent 40%,#FBE277 40%)}'+
    '.xrs .xrw .xme{background:transparent;color:#6F685E;border:1px solid rgba(120,110,95,.4)}'+
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .xrs .xrw .xL{color:#9E978D}:root:not([data-theme="light"]) .xrs .xrw.ok .xL{color:#8ED3A0}:root:not([data-theme="light"]) .xrs .xp{color:#B5AEA3;border-color:rgba(200,190,175,.35);background:transparent}:root:not([data-theme="light"]) .xrs mark.xk-ng,:root:not([data-theme="light"]) .xrs mark.xk-ok{color:inherit;background:linear-gradient(transparent 40%,#6E5B10 40%)}:root:not([data-theme="light"]) .xrs .xrw .xme{color:#B5AEA3;border-color:rgba(200,190,175,.35);background:transparent}}'+
    ':root[data-theme="dark"] .xrs .xrw .xL{color:#9E978D}:root[data-theme="dark"] .xrs .xrw.ok .xL{color:#8ED3A0}:root[data-theme="dark"] .xrs .xp{color:#B5AEA3;border-color:rgba(200,190,175,.35);background:transparent}:root[data-theme="dark"] .xrs mark.xk-ng,:root[data-theme="dark"] .xrs mark.xk-ok{color:inherit;background:linear-gradient(transparent 40%,#6E5B10 40%)}:root[data-theme="dark"] .xrs .xrw .xme{color:#B5AEA3;border-color:rgba(200,190,175,.35);background:transparent}';
    (document.head||document.documentElement).appendChild(s)}
  function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  /* o={stem,exps:[4],ans:0-3,pick:0-3,core:[4]|null,keys:[[...]x4]|null} */
  /* 11-14：作答後在題目選項上把「錯的字」標紅（依 bx-wrong.js）。btns＝四個選項元素，o 同 bxXRows */
  window.bxMarkOpts=function(btns,o){if(!window.bxWrong)return;var neg=bxNegStem(o.stem);
    [].forEach.call(btns,function(el,i){if((i===o.ans)!==neg||el.querySelector('mark.bxw'))return;
      var ph=bxWrong(o.opts[i],(o.exps||[])[i]);if(!ph.length)return;
      var tw=document.createTreeWalker(el,4),n,ns=[];while((n=tw.nextNode()))ns.push(n);
      ph.forEach(function(p){for(var k=0;k<ns.length;k++){var t=ns[k],j=t.nodeValue.indexOf(p);if(j<0)continue;
        var r=t.splitText(j);r.splitText(p.length);var m=document.createElement('mark');m.className='bxw';r.parentNode.replaceChild(m,r);m.appendChild(r);ns.splice(k+1,0,m.nextSibling);break}})})};
  window.bxXRows=function(o){
    var neg=bxNegStem(o.stem),h='<div class="xrs">';
    /* 組合題（選項都是 ①②③…）：答案組合就是「對在」 */
    if(o.opts&&o.opts.length&&o.opts.every(function(x){return /^[\s①-⑳、，,與及和]+$/.test(String(x))}))neg=false;
    (o.exps||[]).forEach(function(t,i){
      var ok=i===o.ans,tk=(ok!==neg)?'ok':'ng',core=o.core&&o.core[i],keys=o.keys&&o.keys[i]||[];
      var raw=String(t||'（本選項解析待補）').replace(/^[✓✔✗✘❌✅]\s*/,''),tags=[];
      /* 解析內少數 <b>／<br>／<sup>／<sub> 保留（先換成記號，標色後還原） */
      raw=raw.replace(/<\/?(?:b|strong|br|sup|sub|i|em)\s*\/?>/gi,function(m){tags.push(m);return '\u0001'+(tags.length-1)+'\u0002'});
      var body=window.bxmExp?bxmExp(raw,null,keys,tk):esc(raw);
      body=body.replace(/\u0001(\d+)\u0002/g,function(_,n){return tags[+n]});
      if(tk==='ng'&&window.bxWrongExp)body=bxWrongExp(body);
      var head='<span class="xc">'+(ok?'<span class="xans">本題答案</span>':'')+'<span class="xp xp-'+tk+'">'+(tk==='ok'?'對在':'錯在')+'</span>'+(core?esc(core):'')+'</span>';
      h+='<div class="xrw'+(ok?' ok':'')+'"><span class="xL">'+'ABCD'[i]+'</span><div class="xB">'+head+body+(i===o.pick&&!ok?'<span class="xme">你選的</span>':'')+'</div></div>';
    });
    return h+'</div>';
  };
})();
