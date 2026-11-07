/* 逐選項解析列（土地法／估價解析版練習共用，2026-11-07，比照民法法條解析練習）
   每列＝字母＋〔本題答案〕＋對在／錯在＋一句重點（有寫才顯示）＋解析（關鍵字黃底／紅字）＋你選的。
   對在／錯在＝這個選項的敘述對不對：題幹問「錯誤／非／不得／不屬…」時，答案那項是「錯在」、其餘「對在」；其他題型相反。
   依賴 bxm-exp.js（bxmExp）。 */
(function(){
  var NEG=/錯誤|不正確|有誤|非|不得|不屬|不包括|不包含|不是|不適用|無(?!理由)|不在(?!此限)/;
  function tail(st){st=String(st||'');var r=/何者|何種|何項|何|哪|那/g,m,last=-1;while((m=r.exec(st)))last=m.index;return last>=0?st.slice(last):st.slice(-14)}
  window.bxNegStem=function(stem){return NEG.test(tail(stem))};
  if(!document.getElementById('bx-xrow-css')){var s=document.createElement('style');s.id='bx-xrow-css';s.textContent=
    '.xrs{border:1px solid rgba(120,110,95,.28);border-radius:10px;overflow:hidden;background:var(--card,#FFFEFA)}'+
    '.xrw{display:flex;gap:10px;padding:9px 12px;border-top:1px dashed rgba(120,110,95,.3);line-height:1.7;font-size:.9rem}'+
    '.xrw:first-child{border-top:0}.xrw .xL{flex:none;width:1.5em;font-weight:700;color:#B3261E}.xrw.ok .xL{color:#2E7A45}'+
    '.xrw.ok{background:#EAF3EA}.xrw .xB{flex:1;min-width:0}.xrw .xme{display:inline-block;font-size:.72rem;background:#FBE9D2;color:#8A5517;border-radius:4px;padding:0 6px;margin-left:6px;white-space:nowrap}'+
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .xrw.ok{background:#22302A}:root:not([data-theme="light"]) .xrw .xL{color:#FF8E7E}:root:not([data-theme="light"]) .xrw.ok .xL{color:#8ED3A0}:root:not([data-theme="light"]) .xrw .xme{background:#3A2E1C;color:#E0B070}:root:not([data-theme="light"]) .xrs{background:var(--card,#1F2723)}}'+
    ':root[data-theme="dark"] .xrw.ok{background:#22302A}:root[data-theme="dark"] .xrw .xL{color:#FF8E7E}:root[data-theme="dark"] .xrw.ok .xL{color:#8ED3A0}:root[data-theme="dark"] .xrw .xme{background:#3A2E1C;color:#E0B070}:root[data-theme="dark"] .xrs{background:var(--card,#1F2723)}';
    (document.head||document.documentElement).appendChild(s)}
  function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  /* o={stem,exps:[4],ans:0-3,pick:0-3,core:[4]|null,keys:[[...]x4]|null} */
  window.bxXRows=function(o){
    var neg=bxNegStem(o.stem),h='<div class="xrs">';
    (o.exps||[]).forEach(function(t,i){
      var ok=i===o.ans,tk=(ok!==neg)?'ok':'ng',core=o.core&&o.core[i],keys=o.keys&&o.keys[i]||[];
      var body=window.bxmExp?bxmExp(String(t||'（本選項解析待補）').replace(/^[✓✔✗✘❌✅]\s*/,''),null,keys,tk):esc(t);
      var head='<span class="xc">'+(ok?'<span class="xans">本題答案</span>':'')+'<span class="xp xp-'+tk+'">'+(tk==='ok'?'對在':'錯在')+'</span>'+(core?esc(core):'')+'</span>';
      h+='<div class="xrw'+(ok?' ok':'')+'"><span class="xL">'+'ABCD'[i]+'</span><div class="xB">'+head+body+(i===o.pick&&!ok?'<span class="xme">你選的</span>':'')+'</div></div>';
    });
    return h+'</div>';
  };
})();
