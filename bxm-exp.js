/* 民法刷題解析：每個選項「一句結論＋重點句」標色（v640 起）。
   正確敘述＝黃底粗體「對在」；錯誤敘述＝紅字粗體「錯在」；條號只用棕色字，不再自動畫黃。
   資料欄位：core[i]（一句結論）、key[i]（解析原文中的重點句，逐字子字串）、tk[i]（'ok'｜'ng'）。
   用法：el.innerHTML = bxmExp(解析文字, core, key, tk[, 前綴]) */
(function(){
  var CSS=''
  +'.xc{display:block;font-weight:700;line-height:1.55;margin:0 0 3px}'
  +'.xp{display:inline-block;font-size:.76em;font-weight:700;border-radius:99px;padding:0 .6em;margin-right:.45em;vertical-align:.08em;white-space:nowrap}'
  +'.xp-ok{background:#F7DC5C;color:#4A3800}.xp-ng{background:#F9D6CF;color:#B3261E}'
  +'mark.xk{background:none;color:inherit;font-weight:700;padding:0 1px;border-radius:2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}'
  +'mark.xk-ok{background:linear-gradient(transparent 40%,#FBE277 40%)}'
  +'mark.xk-ng{color:#C0392B}'
  +'.xlaw{color:#8A5517;font-weight:600}'
  +'.xpre{font-weight:700;margin-right:.3em}'
  +'@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .xp-ok{background:#6E5B10;color:#FFEDA6}:root:not([data-theme="light"]) .xp-ng{background:#5A2420;color:#FFB4A8}:root:not([data-theme="light"]) mark.xk-ok{background:linear-gradient(transparent 40%,#6E5B10 40%)}:root:not([data-theme="light"]) mark.xk-ng{color:#FF8E7E}:root:not([data-theme="light"]) .xlaw{color:#E0B070}}'
  +':root[data-theme="dark"] .xp-ok{background:#6E5B10;color:#FFEDA6}:root[data-theme="dark"] .xp-ng{background:#5A2420;color:#FFB4A8}:root[data-theme="dark"] mark.xk-ok{background:linear-gradient(transparent 40%,#6E5B10 40%)}:root[data-theme="dark"] mark.xk-ng{color:#FF8E7E}:root[data-theme="dark"] .xlaw{color:#E0B070}';
  function addCss(){if(document.getElementById('bxm-exp-css'))return;var s=document.createElement('style');s.id='bxm-exp-css';s.textContent=CSS;(document.head||document.documentElement).appendChild(s)}
  addCss();
  function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  var LAW=/(§\s*\d+(?:\s*[-之]\s*\d+)?(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)?(?:[①②③④⑤⑥⑦⑧⑨⑩]+)?(?:第[一二三四五六七八九十]+[項款])*(?:[～~]\s*§?\s*\d+(?:-\d+)?)?)/g;
  function law(h){return h.replace(LAW,'<span class="xlaw">$1</span>')}
  window.bxmExp=function(text,core,key,tk,pre){
    var t=String(text==null?'':text),h,i;
    tk=tk==='ok'?'ok':'ng';
    if(pre&&t.indexOf(pre)===0)t=t.slice(pre.length);
    if(key&&(i=t.indexOf(key))>=0){
      h=law(esc(t.slice(0,i)))+'<mark class="xk xk-'+tk+'">'+esc(key)+'</mark>'+law(esc(t.slice(i+key.length)));
    }else h=law(esc(t));
    var head=pre?'<span class="xpre">'+esc(pre.trim())+'</span>':'';
    if(core)head+='<span class="xc"><span class="xp xp-'+tk+'">'+(tk==='ok'?'對在':'錯在')+'</span>'+esc(core)+'</span>';
    else if(pre)head+=' ';
    return head+h;
  };
})();
