/* 「下一題」一點就換（四科共用，2026-11-07）
   iPad／手機：頁面還在慣性捲動時點按鈕，瀏覽器只會「停住捲動」不送 click，看起來像按了沒反應；
   快速連點也可能被當成雙擊放大。這裡對「下一題」類按鈕：
   ①加 touch-action:manipulation（取消雙擊放大）；
   ②手指點下到放開移動 <12px、<700ms 就直接觸發一次（並取消瀏覽器之後補送的 click，避免連跳兩題）。 */
(function(){
  var SEL='#nextBtn,#next,[data-bxtap]';
  try{var st=document.createElement('style');st.textContent='button,a,.opt,.wtag{touch-action:manipulation}';document.head.appendChild(st)}catch(e){}
  /* 換題後回到題目開頭；題目很短時頁面仍可往上拉（iPad 瀏覽器工具列收起後，頁面不能捲就拉不回頂端） */
  function quizBox(){var q=document.querySelector('#quizScreen,#quiz');return q&&!q.hidden&&!q.classList.contains('hidden')?q:null}
  /* 頁面不可左右平移（iPad 有元素略超出時，整頁會被推到左邊、右側空白）；開頁若已偏移就拉回 */
  try{var st3=document.createElement('style');st3.textContent='html,body{overflow-x:clip;max-width:100%}';document.head.appendChild(st3);if(window.scrollX)window.scrollTo(0,window.scrollY)}catch(e){}
  try{if(document.querySelector('#quizScreen,#quiz')&&!document.getElementById('segs')){var st2=document.createElement('style');st2.textContent='body{min-height:calc(100vh + 60px)}';document.head.appendChild(st2)}}catch(e){}
  /* iPad：捲在長解析底部時換題，頁面瞬間變短，WebKit 可能卡在「畫面被往下推、拉不回頂端」的狀態
     （右上固定鈕下移、底部固定鈕看不到）。改成：換題／開始前先捲好位置（頁面變短之前），換完再檢查一次並解卡。 */
  var GO='#nextBtn,#next,#startBtn,#start,#resumeGo,#restartBtn,#again';
  function unstick(y){try{var v=window.visualViewport,h=document.documentElement,max=Math.max(0,h.scrollHeight-window.innerHeight);
    if(window.scrollX||window.scrollY>max+1||(v&&(v.offsetTop>1||v.offsetLeft>1))){window.scrollTo(0,Math.min(max,y+1));window.scrollTo(0,Math.min(max,y))}}catch(e){}}
  function target(){var q=quizBox();if(!q)return window.scrollY;var t=q.getBoundingClientRect().top;return t<0?Math.max(0,t+window.scrollY-8):window.scrollY}
  document.addEventListener('click',function(e){
    var b=e.target&&e.target.closest?e.target.closest(GO):null;if(!b||document.getElementById('segs')||!document.querySelector('#quizScreen,#quiz'))return;
    var isNext=b.matches('#nextBtn,#next'),y=isNext?target():0;
    if(window.scrollX||y!==window.scrollY)window.scrollTo(0,y);
    setTimeout(function(){var y2=target();if(window.scrollX||y2!==window.scrollY)window.scrollTo(0,y2);unstick(window.scrollY)},30);
    setTimeout(function(){unstick(window.scrollY)},350);
  },true);
  var t0=null;
  function hit(el){return el&&el.closest?el.closest(SEL):null}
  document.addEventListener('touchstart',function(e){
    var b=hit(e.target);if(!b||e.touches.length!==1){t0=null;return}
    var p=e.touches[0];t0={b:b,x:p.clientX,y:p.clientY,t:Date.now()};
  },{passive:true,capture:true});
  document.addEventListener('touchend',function(e){
    var s=t0;t0=null;if(!s)return;
    var p=e.changedTouches&&e.changedTouches[0];if(!p)return;
    if(Math.abs(p.clientX-s.x)>12||Math.abs(p.clientY-s.y)>12||Date.now()-s.t>700)return;
    var b=s.b;if(b.disabled||b.hidden||b.classList.contains('hidden')||!b.offsetParent)return;
    var r=b.getBoundingClientRect();if(p.clientX<r.left||p.clientX>r.right||p.clientY<r.top||p.clientY>r.bottom)return;
    e.preventDefault();b.click();
  },{passive:false,capture:true});
})();
