/* iPad 視窗大小改變後版面沒跟著變寬（全站共用，2026-11-07）
   iPad Chrome／Safari 從分割畫面或小視窗放到全螢幕、或轉方向時，網頁有時仍用舊的窗寬排版：
   內容偏左、右邊一大塊空白、右側固定鈕往左跑。偵測到視窗寬度變了就重新套一次 viewport，讓瀏覽器重新排版。 */
(function(){
  if(window.__bxvp)return;window.__bxvp=1;
  function meta(){return document.querySelector('meta[name=viewport]')}
  var m=meta();if(!m)return;
  var base=m.getAttribute('content')||'width=device-width,initial-scale=1';
  function sig(){var v=window.visualViewport;return [window.innerWidth,window.outerWidth||0,v?Math.round(v.width*v.scale):0,(window.matchMedia&&matchMedia('(orientation: landscape)').matches)?1:0].join('x')}
  var last=sig(),tm=null;
  function reapply(){try{var old=meta();if(!old)return;var n=document.createElement('meta');n.name='viewport';n.content=base;
    old.parentNode.replaceChild(n,old);
    if(window.scrollX)window.scrollTo(0,window.scrollY)}catch(e){}}
  /* 窗寬和螢幕（依方向）差很多，也重套一次（分割畫面時重套無害） */
  function scr(){var a=screen.width||0,b=screen.height||0,land=window.matchMedia&&matchMedia('(orientation: landscape)').matches;return land?Math.max(a,b):Math.min(a,b)}
  function stale(){var ow=window.outerWidth||0,cw=document.documentElement.clientWidth,sw=scr();return (ow>0&&Math.abs(ow-cw)>24&&Math.abs(ow-window.innerWidth)>24)||(sw>0&&sw-window.innerWidth>24&&!stale.done&&(stale.done=1))}
  function check(force){clearTimeout(tm);tm=setTimeout(function(){var s=sig();if(force||s!==last||stale()){last=s;reapply();setTimeout(function(){last=sig()},400)}},250)}
  addEventListener('resize',function(){check(false)});
  addEventListener('orientationchange',function(){check(true)});
  addEventListener('pageshow',function(e){if(e.persisted)check(true)});
  document.addEventListener('visibilitychange',function(){if(!document.hidden)check(false)});
  if(window.visualViewport)visualViewport.addEventListener('resize',function(){check(false)});
  if(stale())check(true);
})();
