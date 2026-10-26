/* bx-theme.js：全站統一「預設淺色＋右上深淺切換」（記在 localStorage bx-theme）。
   <script src="bx-theme.js" data-auto="1"> ＝ 本頁沒有自己的深色樣式，由本檔自動把淺底轉深底、深字轉淺字。
   沒有 data-auto ＝ 本頁已有 [data-theme="dark"] 深色樣式，本檔只負責預設值與切換鈕。 */
(function(){
  var D=document,H=D.documentElement,me=D.currentScript,AUTO=me&&me.getAttribute('data-auto')==='1';
  var t=null;try{t=localStorage.getItem('bx-theme')}catch(e){}
  H.setAttribute('data-theme',t==='dark'?'dark':'light');
  function lum(c){return (0.2126*c[0]+0.7152*c[1]+0.0722*c[2])/255}
  function parse(s){var m=s&&s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);if(!m)return null;var a=m[4]===undefined?1:+m[4];return a<0.05?null:[+m[1],+m[2],+m[3],a]}
  function chroma(c){return (Math.max(c[0],c[1],c[2])-Math.min(c[0],c[1],c[2]))/255}
  function rgb(c){return 'rgb('+c.map(function(x){return Math.round(x)}).slice(0,3).join(',')+')'}
  var BASE=[31,39,35],BODY=[22,28,25],INK=[231,236,230];
  function fixEl(el){
    if(el.nodeType!==1||el.dataset.bxdk)return;var cs=getComputedStyle(el);
    var bg=parse(cs.backgroundColor),fg=parse(cs.color),bc=parse(cs.borderTopColor),o={};
    if(bg){var L=lum(bg);if(L>0.8){o.b=el.style.backgroundColor;el.style.backgroundColor=rgb(el===D.body?BODY:(chroma(bg)>0.06?bg.map(function(x,i){return i<3?x*0.22+BASE[i]*0.78:x}):BASE))}
      else if(L>0.55){o.b=el.style.backgroundColor;el.style.backgroundColor=rgb(bg.map(function(x,i){return i<3?x*0.35+BASE[i]*0.65:x}))}}
    if(fg){var Lf=lum(fg);if(Lf<0.45){o.c=el.style.color;el.style.color=rgb(chroma(fg)>0.18?fg.map(function(x,i){return i<3?x*0.55+255*0.45:x}):INK)}}
    if(bc&&lum(bc)>0.7&&parseFloat(cs.borderTopWidth)>0){o.d=el.style.borderColor;el.style.borderColor='#3A463F'}
    if(o.b!==undefined||o.c!==undefined||o.d!==undefined){el.dataset.bxdk=JSON.stringify(o)}else el.dataset.bxdk='{}';
  }
  function walk(root){fixEl(root);var all=root.querySelectorAll?root.querySelectorAll('*'):[];for(var i=0;i<all.length;i++)fixEl(all[i])}
  function undo(){[].forEach.call(D.querySelectorAll('[data-bxdk]'),function(el){try{var o=JSON.parse(el.dataset.bxdk);if('b'in o)el.style.backgroundColor=o.b;if('c'in o)el.style.color=o.c;if('d'in o)el.style.borderColor=o.d}catch(e){}delete el.dataset.bxdk})}
  var mo=null;
  function apply(){
    var dark=H.getAttribute('data-theme')==='dark';H.style.colorScheme=dark?'dark':'light';
    if(!AUTO)return;
    if(dark){walk(D.body);if(!mo){mo=new MutationObserver(function(ms){ms.forEach(function(m){m.addedNodes.forEach(function(n){if(n.nodeType===1)walk(n)});if(m.type==='attributes'&&m.target.nodeType===1&&m.target.dataset.bxdk){delete m.target.dataset.bxdk;fixEl(m.target)}})});mo.observe(D.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class']})}}
    else{if(mo){mo.disconnect();mo=null}undo()}
  }
  function btnSync(b){b.textContent=H.getAttribute('data-theme')==='dark'?'🌙':'☀️'}
  function init(){
    var ex=D.querySelector('#theme-btn,#themeBtn,#themeToggle,button.theme,[onclick*="toggleTheme"],[data-bx-theme],button#theme');
    if(!ex){var b=D.createElement('button');b.id='bx-theme-btn';b.type='button';b.setAttribute('aria-label','切換深淺色');b.title='切換深淺色';
      b.style.cssText='position:fixed;top:calc(10px + env(safe-area-inset-top,0px));right:10px;z-index:9999;width:38px;height:38px;border-radius:50%;border:1px solid rgba(128,128,128,.4);background:rgba(255,255,255,.85);font-size:18px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15)';
      btnSync(b);b.onclick=function(){var n=H.getAttribute('data-theme')==='dark'?'light':'dark';H.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}btnSync(b);b.style.background=n==='dark'?'rgba(31,39,35,.9)':'rgba(255,255,255,.85)';apply()};
      if(H.getAttribute('data-theme')==='dark')b.style.background='rgba(31,39,35,.9)';
      D.body.appendChild(b)}
    else{ex.addEventListener('click',function(){setTimeout(apply,30)})}
    apply();
  }
  if(D.readyState==='loading')D.addEventListener('DOMContentLoaded',function(){setTimeout(init,50)});else setTimeout(init,50);
})();
