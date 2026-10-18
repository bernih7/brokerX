/* 考古題代號（如 104-34）→ 點一下顯示「104年第34題」題幹與官方答案。資料：bxm-exams-data.js（民法 99–114 年 520 題） */
(function(){
  var css='.xq{cursor:pointer;border-bottom:1px dotted currentColor;white-space:nowrap}.xq:hover{opacity:.75}'+
  '#xqp{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);width:min(92vw,440px);max-height:60vh;overflow:auto;z-index:99999;border:1px solid rgba(128,128,128,.4);border-radius:12px;padding:12px 14px 14px;box-shadow:0 6px 24px rgba(0,0,0,.25);font-size:.9rem;line-height:1.65;display:none}'+
  '#xqp .xh{font-weight:700;margin-bottom:4px;display:flex;justify-content:space-between;gap:8px}#xqp .xc{cursor:pointer;opacity:.6;padding:0 4px}'+
  '#xqp .xa{margin-top:8px;padding-top:6px;border-top:1px dashed rgba(128,128,128,.4)}#xqp .xa b{font-weight:700}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  var RE=/(?<![\d§\-.\/])((?:9\d|1[01]\d)-\d{1,2})(?![\d\-])/g;
  var loaded=false,loading=false,pend=null;
  function load(cb){
    if(window.BXQ){loaded=true;cb();return}
    if(loading){return}
    loading=true;var s=document.createElement('script');s.src='bxm-exams-data.js';
    s.onload=function(){loaded=true;cb()};document.head.appendChild(s);
  }
  function wrap(root){
    if(!window.BXQ)return;
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      var p=n.parentNode;if(!p||!n.nodeValue||n.nodeValue.indexOf('-')<0)return 3;
      if(/^(SCRIPT|STYLE|TEXTAREA|INPUT|OPTION)$/.test(p.nodeName)||(p.closest&&p.closest('.xq,#xqp')))return 3;
      RE.lastIndex=0;return RE.test(n.nodeValue)?1:3}});
    var list=[],n;while(n=w.nextNode())list.push(n);
    list.forEach(function(t){
      var v=t.nodeValue,frag=document.createDocumentFragment(),last=0,m,any=false;RE.lastIndex=0;
      while(m=RE.exec(v)){
        if(!window.BXQ[m[1]])continue;
        any=true;frag.appendChild(document.createTextNode(v.slice(last,m.index)));
        var sp=document.createElement('span');sp.className='xq';sp.setAttribute('data-xq',m[1]);sp.textContent=m[1];
        frag.appendChild(sp);last=m.index+m[0].length;
      }
      if(!any)return;
      frag.appendChild(document.createTextNode(v.slice(last)));t.parentNode.replaceChild(frag,t);
    });
  }
  var pop;
  function show(code){
    var d=window.BXQ[code];if(!d)return;
    if(!pop){pop=document.createElement('div');pop.id='xqp';document.body.appendChild(pop)}
    var cs=getComputedStyle(document.body),bg=cs.backgroundColor;
    if(!bg||bg==='rgba(0, 0, 0, 0)')bg='#fff';
    pop.style.background=bg;pop.style.color=cs.color;
    var y=code.split('-')[0],n=code.split('-')[1];
    pop.innerHTML='<div class="xh"><span></span><span class="xc">✕</span></div><div class="xs"></div><div class="xa"></div>';
    pop.querySelector('.xh span').textContent='民法概要 '+y+' 年第 '+n+' 題';
    pop.querySelector('.xs').textContent=d[0];
    pop.querySelector('.xa').innerHTML='<b>官方答案</b>　'+(d[1]?'':'（依考選部公告一律給分／多重給分）');
    if(d[1]){var a=pop.querySelector('.xa');a.appendChild(document.createTextNode(d[1]))}
    pop.style.display='block';
  }
  document.addEventListener('click',function(e){
    var t=e.target.closest&&e.target.closest('.xq');
    if(t){e.preventDefault();e.stopPropagation();show(t.getAttribute('data-xq'));return}
    if(pop&&pop.style.display==='block'&&(!e.target.closest('#xqp')||e.target.closest('.xc')))pop.style.display='none';
  },true);
  var tm=null;
  function run(){wrap(document.body)}
  function schedule(){clearTimeout(tm);tm=setTimeout(function(){load(run)},350)}
  function start(){
    schedule();
    new MutationObserver(function(ms){
      for(var i=0;i<ms.length;i++){var t=ms[i].target;if(t&&t.closest&&t.closest('#xqp'))continue;schedule();break}
    }).observe(document.body,{childList:true,subtree:true});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
