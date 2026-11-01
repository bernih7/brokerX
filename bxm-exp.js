/* 民法刷題解析：每個選項「一句結論＋重點句」標色（v640 起）。
   正確敘述＝黃底粗體「對在」；錯誤敘述＝紅字粗體「錯在」；條號只用棕色字，不再自動畫黃。
   資料欄位：core[i]（一句結論）、key[i]（v641 起為關鍵字陣列，每個都是解析原文的逐字子字串）、tk[i]（'ok'｜'ng'）。
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
  +'.xpre{font-weight:700;margin-right:.45em}.xpre-ok{color:#2E7A45}.xpre-ng{color:#B3261E}'
  +'@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .xp-ok{background:#6E5B10;color:#FFEDA6}:root:not([data-theme="light"]) .xp-ng{background:#5A2420;color:#FFB4A8}:root:not([data-theme="light"]) mark.xk-ok{background:linear-gradient(transparent 40%,#6E5B10 40%)}:root:not([data-theme="light"]) mark.xk-ng{color:#FF8E7E}:root:not([data-theme="light"]) .xlaw{color:#E0B070}:root:not([data-theme="light"]) .xpre-ok{color:#8ED3A0}:root:not([data-theme="light"]) .xpre-ng{color:#FF8E7E}}'
  +':root[data-theme="dark"] .xp-ok{background:#6E5B10;color:#FFEDA6}:root[data-theme="dark"] .xp-ng{background:#5A2420;color:#FFB4A8}:root[data-theme="dark"] mark.xk-ok{background:linear-gradient(transparent 40%,#6E5B10 40%)}:root[data-theme="dark"] mark.xk-ng{color:#FF8E7E}:root[data-theme="dark"] .xlaw{color:#E0B070}:root[data-theme="dark"] .xpre-ok{color:#8ED3A0}:root[data-theme="dark"] .xpre-ng{color:#FF8E7E}';
  function addCss(){if(document.getElementById('bxm-exp-css'))return;var s=document.createElement('style');s.id='bxm-exp-css';s.textContent=CSS;(document.head||document.documentElement).appendChild(s)}
  addCss();
  function esc(t){return String(t==null?'':t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  var LAW=/(§\s*\d+(?:\s*[-之]\s*\d+)?(?:[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ]+)?(?:[①②③④⑤⑥⑦⑧⑨⑩]+)?(?:第[一二三四五六七八九十]+[項款])*(?:[～~]\s*§?\s*\d+(?:-\d+)?)?)/g;
  function law(h){return h.replace(LAW,'<span class="xlaw">$1</span>')}
  window.bxmExp=function(text,core,key,tk,pre){
    var t=String(text==null?'':text),h,i;
    tk=tk==='ok'?'ok':'ng';
    if(pre&&t.indexOf(pre)===0)t=t.slice(pre.length);
    /* key：關鍵字陣列（v641 起，每選項 1～3 個、各標第一次出現）；舊資料為單一字串也相容 */
    var ks=Array.isArray(key)?key:(key?[key]:[]),sp=[];
    ks.forEach(function(k){if(!k)return;var j=t.indexOf(k);if(j<0)return;
      for(var n=0;n<sp.length;n++){if(j<sp[n][1]&&j+k.length>sp[n][0])return}sp.push([j,j+k.length])});
    sp.sort(function(a,b){return a[0]-b[0]});
    h='';i=0;sp.forEach(function(r){h+=law(esc(t.slice(i,r[0])))+'<mark class="xk xk-'+tk+'">'+esc(t.slice(r[0],r[1]))+'</mark>';i=r[1]});
    h+=law(esc(t.slice(i)));
    var pr=pre?'<span class="xpre xpre-'+tk+'">'+esc(pre.trim().replace(/[.．]$/,''))+'</span>':'';
    var head;
    if(core)head='<span class="xc">'+pr+'<span class="xp xp-'+tk+'">'+(tk==='ok'?'對在':'錯在')+'</span>'+esc(core)+'</span>';
    else head=pr?pr+' ':'';
    return head+h;
  };
})();
