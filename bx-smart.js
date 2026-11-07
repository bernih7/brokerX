/* 智慧配題 v2（四科共用，2026-11-07）
   每輪 want 題＝錯題最多 4 題（C→A→D→B→未標，舊的先）＋不熟／用猜的最多 2 題＋其餘出「沒做過」；
   沒做過的名額依「該章剩下沒做過的題數 × 該章近 5 年考頻（相對歷屆）」分配；
   章內：同一條文被考過的年數多的先、年份新的先；沒做過的不夠才用其餘錯題、不熟、答對題（最久沒練的先）補滿。
   各頁只提供存取函式：ch(q)、y(q)、st(q)→{c:0錯/1沒做/2不熟/3確定,k,t}、con(q)→條文鍵、all（官方題全集，算考頻用）。 */
window.BXSMART=(function(){
  var NUM=/(?:§\s*|第\s*)(\d+)(?:\s*條)?(?:\s*(?:之|-)\s*(\d+))?/;
  function art(t){t=String(t||'');var m=NUM.exec(t);return m?(m[1]+(m[2]?'-'+m[2]:'')):''}
  function rnd(){return Math.random()}
  function hot(o){
    var all=o.all||[],by={},T=0,R=0,maxY=0;
    all.forEach(function(q){var y=+o.y(q)||0;if(y>maxY)maxY=y});
    all.forEach(function(q){var c=o.ch(q),y=+o.y(q)||0,b=by[c]||(by[c]={t:0,r:0});b.t++;T++;if(y>=maxY-4){b.r++;R++}});
    var base=T?R/T:0,h={};
    Object.keys(by).forEach(function(c){var b=by[c];h[c]=(b.t<5||!base)?1:Math.max(.5,Math.min(2,(b.r/b.t)/base))});
    return h;
  }
  function freq(o){
    var f={};(o.all||[]).forEach(function(q){var k=o.con?o.con(q):'';if(!k)return;k=o.ch(q)+'|'+k;(f[k]=f[k]||{})[o.y(q)]=1});
    var n={};Object.keys(f).forEach(function(k){n[k]=Object.keys(f[k]).length});return n;
  }
  function run(list,o){
    var want=Math.min(o.want||30,list.length);if(!want)return [];
    var capW=Math.max(4,Math.round(want*.13)),capU=Math.max(2,Math.round(want*.07));
    var W=[],N=[],U=[],S=[];
    list.forEach(function(q){var s=o.st(q)||{c:1};var x={q:q,s:s,r:rnd()};(s.c===0?W:s.c===1?N:s.c===2?U:S).push(x)});
    W.sort(function(a,b){return (a.s.k||0)-(b.s.k||0)||(a.s.t||0)-(b.s.t||0)||a.r-b.r});
    U.sort(function(a,b){return (a.s.t||0)-(b.s.t||0)||a.r-b.r});
    S.sort(function(a,b){return (a.s.t||0)-(b.s.t||0)||a.r-b.r});
    var w=W.slice(0,Math.min(capW,want)),u=U.slice(0,Math.min(capU,want-w.length)),R=want-w.length-u.length;
    /* 沒做過：分章配額 */
    var H=hot(o),F=freq(o),by={};
    N.forEach(function(x){var c=o.ch(x.q);x.f=F[c+'|'+(o.con?o.con(x.q):'')]||0;x.yy=+o.y(x.q)||0;(by[c]=by[c]||[]).push(x)});
    var chs=Object.keys(by),quota={};chs.forEach(function(c){quota[c]=0;by[c].sort(function(a,b){return b.f-a.f||b.yy-a.yy||a.r-b.r})});
    var left=Math.min(R,N.length);
    while(left>0){
      var open=chs.filter(function(c){return quota[c]<by[c].length});if(!open.length)break;
      var tw=0,wt={};open.forEach(function(c){wt[c]=(by[c].length-quota[c])*(H[c]||1);tw+=wt[c]});
      var give=open.map(function(c){var e=left*wt[c]/tw;return {c:c,f:Math.floor(e),r:e-Math.floor(e)}}),g=0;
      give.forEach(function(x){var a=Math.min(x.f,by[x.c].length-quota[x.c]);quota[x.c]+=a;g+=a});
      give.sort(function(a,b){return b.r-a.r});
      for(var i=0;i<give.length&&g<left;i++){if(quota[give[i].c]<by[give[i].c].length){quota[give[i].c]++;g++}}
      if(!g)break;left-=g;
    }
    var nn=[];chs.forEach(function(c){nn=nn.concat(by[c].slice(0,quota[c]))});
    /* 不夠才補：其餘錯題 → 不熟 → 答對（最久沒練） */
    var rest=W.slice(w.length).concat(U.slice(u.length),S),fill=[];
    while(w.length+u.length+nn.length+fill.length<want&&rest.length)fill.push(rest.shift());
    var others=u.concat(nn,fill);
    for(var j=others.length-1;j>0;j--){var k=Math.random()*(j+1)|0,t=others[j];others[j]=others[k];others[k]=t}
    var out=w.concat(others).map(function(x){return x.q});
    var cc={};nn.forEach(function(x){var c=o.ch(x.q);cc[c]=(cc[c]||0)+1});
    var top=Object.keys(cc).sort(function(a,b){return cc[b]-cc[a]}).map(function(c){return c+' '+cc[c]});
    var msg='本輪：錯題 '+w.length+'・不熟 '+u.length+'・沒做過 '+nn.length+(fill.length?'・複習 '+fill.length:'')+(top.length?'（'+top.slice(0,5).join('、')+(top.length>5?'…':'')+'）':'');
    BXSMART.last=msg;toast(msg);
    return out;
  }
  function toast(m){
    try{var d=document.getElementById('bxSmartToast');
      if(!d){d=document.createElement('div');d.id='bxSmartToast';d.setAttribute('role','status');
        d.style.cssText='position:fixed;left:50%;transform:translateX(-50%);bottom:calc(76px + env(safe-area-inset-bottom,0px));z-index:80;max-width:calc(100vw - 32px);box-sizing:border-box;padding:10px 16px;border-radius:12px;background:#2F5D50;color:#FFFEFA;font:13px/1.55 system-ui,-apple-system,"Noto Sans TC",sans-serif;box-shadow:0 4px 16px rgba(0,0,0,.25);text-align:center;transition:opacity .4s;cursor:pointer';
        d.onclick=function(){d.style.opacity=0};document.body.appendChild(d)}
      d.textContent='🧭 '+m;d.style.opacity=1;clearTimeout(d._t);d._t=setTimeout(function(){d.style.opacity=0},5000)}catch(e){}
  }
  var HINT='智慧配題：每輪 30 題＝錯題最多 4 題（C 真的不熟→A→D→B→未標）＋不熟／用猜的最多 2 題，其餘全出「沒做過」的題。沒做過的依「這章還剩幾題 × 近 5 年考頻」分到各章，章內同一條文被考過越多年的先出；沒做過的不夠才用其他錯題、答對題補滿。開始時下方會顯示本輪組成。';
  return {run:run,art:art,hint:HINT,last:''};
})();
