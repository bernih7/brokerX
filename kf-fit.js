/* 公式小卡：一行呈現，太寬時自動縮小（不換行） */
(function(){
  function fitOne(e){
    if(e._fitting) return; e._fitting=true;
    try{
      e.style.zoom='';
      var w=e.clientWidth; if(!w){return;}
      var z=1,i=0;
      while(e.scrollWidth>e.clientWidth+1 && i<12){ z=Math.max(.62,z*Math.min(.97,e.clientWidth/e.scrollWidth)); e.style.zoom=z.toFixed(3); i++; if(z<=.62)break; }
    }finally{e._fitting=false;}
  }
  function all(){document.querySelectorAll('.kf-eq').forEach(fitOne);}
  function init(){
    all();
    if(window.ResizeObserver){
      var ro=new ResizeObserver(function(es){es.forEach(function(x){fitOne(x.target)})});
      document.querySelectorAll('.kf-eq').forEach(function(e){ro.observe(e)});
    }
    window.addEventListener('resize',all);
    document.addEventListener('toggle',all,true);
    document.addEventListener('click',function(){setTimeout(all,80)},true);
    if(document.fonts&&document.fonts.ready)document.fonts.ready.then(all);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
