/* 定義填空：「只看未完成」— 四科共用。網址加 #todo 直接進入。申論四段填空（S1…）另計，不列入。 */
(function(){
  if(typeof DATA==='undefined'||typeof cardDone==='undefined')return;
  var main=document.getElementById('main');if(!main)return;
  var ES=/^S\d/;
  var st=document.createElement('style');
  st.textContent='body.bxtd #main .chapter{display:block!important}body.bxtd #main .chapter.bxtd-x,body.bxtd #main .card.bxtd-d{display:none!important}body.bxtd #main .chapter+.chapter{margin-top:22px}'+
  '#bxtdBar{max-width:860px;margin:10px auto 0;padding:0 16px;box-sizing:border-box}'+
  '#bxtdBar .in{display:flex;flex-wrap:wrap;align-items:center;gap:8px;border:1px solid var(--line,#ddd);border-radius:10px;padding:8px 12px;background:var(--card,transparent);font-size:13px;color:var(--ink,inherit)}'+
  '#bxtdBar .tx{flex:1 1 220px;min-width:0;line-height:1.6}#bxtdBar .tx small{display:block;color:var(--muted,#888);font-size:12px}'+
  '#bxtdBar button{font:inherit;font-size:12.5px;font-weight:700;padding:5px 12px;border-radius:99px;border:1.5px solid var(--red,#a33);background:transparent;color:var(--red,#a33);cursor:pointer;white-space:nowrap}'+
  '#bxtdBar button.on{background:var(--red,#a33);color:var(--card,#fff)}';
  document.head.appendChild(st);
  var bar=document.createElement('div');bar.id='bxtdBar';main.parentNode.insertBefore(bar,main);
  function chOf(k){return k.replace(/-[^-]*$/,'')}
  function left(){
    var by={},n=0,order=[];
    DATA.forEach(function(ch){if(ES.test(ch.id))return;var c=0;Object.keys(cardDone).forEach(function(k){if(chOf(k)===ch.id&&!cardDone[k])c++});if(c){by[ch.id]=c;order.push(ch.id);n+=c}});
    return{n:n,by:by,order:order};
  }
  var on=false;
  function paint(){
    var L=left(),list=L.order.map(function(id){return id+' '+L.by[id]}).join('・');
    if(!L.n){bar.innerHTML='<div class="in"><span class="tx">🎉 選擇題攻略全部完成</span>'+(on?'<button type="button" class="on" data-a="off">顯示全部</button>':'')+'</div>';return}
    bar.innerHTML='<div class="in"><span class="tx">'+(on?'🔍 只顯示未完成：剩 <b>'+L.n+'</b> 張':'還沒完成 <b>'+L.n+'</b> 張')+'<small>'+list+'（不含申論四段填空）</small></span>'+
      (on?'<button type="button" class="on" data-a="off">顯示全部</button>':'<button type="button" data-a="on">只看未完成</button>')+'</div>';
  }
  function apply(){
    Object.keys(cardDone).forEach(function(k){var c=document.getElementById('card-'+k);if(c)c.classList.toggle('bxtd-d',!!cardDone[k])});
    DATA.forEach(function(ch){var d=document.getElementById('ch-'+ch.id);if(!d)return;var any=!ES.test(ch.id)&&Object.keys(cardDone).some(function(k){return chOf(k)===ch.id&&!cardDone[k]});d.classList.toggle('bxtd-x',!any)});
  }
  function goOn(){try{if(typeof setMode==='function')setMode('browse')}catch(e){}apply();on=true;document.body.classList.add('bxtd');paint()}
  function goOff(){on=false;document.body.classList.remove('bxtd');paint()}
  bar.addEventListener('click',function(e){var b=e.target.closest('button[data-a]');if(!b)return;b.dataset.a==='on'?goOn():goOff()});
  document.addEventListener('click',function(e){if(!bar.contains(e.target))setTimeout(paint,60)});
  paint();
  function hs(){if(location.hash==='#todo')setTimeout(goOn,0)}
  hs();addEventListener('hashchange',hs);
})();
