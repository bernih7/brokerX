/* bx-wrong.js（11-14）：錯誤選項裡「錯的字」標紅。
   使用者：「錯的字要標出來」。從解析抓「不是X／錯在「X」／非「X」／而非X」的 X，
   在選項原文找到同一段字（含 40%↔百分之四十、3個月↔三個月 這類數字寫法互換）就標 <mark class="bxw">。
   bxWrong(選項文字, 解析文字) → 選項中要標的片語陣列；bxWrongHtml(已 escape 的 html, 片語陣列) → 加標記；
   bxWrongExp(解析 html) → 把解析裡「不是」後面的錯誤字也標同一種紅。 */
(function(){
  if(!document.getElementById('bxw-css')){var s=document.createElement('style');s.id='bxw-css';s.textContent=
   'mark.bxw{background:none!important;color:#B3261E;font-weight:700;text-decoration:underline wavy #B3261E 1px;text-underline-offset:3px;-webkit-text-decoration:underline wavy #B3261E 1px;padding:0}'+
   '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) mark.bxw{color:#FF8E7E;text-decoration-color:#FF8E7E}}'+
   ':root[data-theme="dark"] mark.bxw{color:#FF8E7E;text-decoration-color:#FF8E7E}';
   (document.head||document.documentElement).appendChild(s)}
  var CN='零一二三四五六七八九';
  function cn(n){n=+n;if(isNaN(n)||n<0||n>=1000)return null;if(n<10)return CN[n];if(n<20)return '十'+(n%10?CN[n%10]:'');
    if(n<100)return CN[Math.floor(n/10)]+'十'+(n%10?CN[n%10]:'');var h=Math.floor(n/100),r=n%100;return CN[h]+'百'+(r?(r<10?'零'+CN[r]:(r<20?'一'+cn(r):cn(r))):'')}
  function variants(x){var v=[x];
    var m=/^(\d+(?:\.\d+)?)%$/.exec(x);if(m&&cn(m[1]))v.push('百分之'+cn(m[1]));
    m=/^(\d+)(個月|年|日|天|倍|成|人|戶|次|公畝|公頃)(.*)$/.exec(x);if(m&&cn(m[1])){v.push(m[1]+' '+m[2]+m[3],cn(m[1])+m[2]+m[3]);if(m[3])v.push(m[1]+m[2],m[1]+' '+m[2],cn(m[1])+m[2])}
    m=/^(\d+(?:\.\d+)?)‰$/.exec(x);if(m&&cn(m[1]))v.push('千分之'+cn(m[1]));
    return v}
  var TRG=/(?:錯在|不是|並非|而非|非屬|並不是|不在|非(?=[「『]))\s*(?:以|按|在|由|向|於)?\s*([「『"“]?)([^，。；：、（）()「」『』"“”\s]{1,24})/g;
  window.bxWrong=function(opt,exp){opt=String(opt||'');exp=String(exp||'').replace(/<[^>]+>/g,'');
    var out=[],m;TRG.lastIndex=0;
    while((m=TRG.exec(exp))){var x=m[2];
      if(m[1]){var close=exp.indexOf(m[1]==='「'?'」':m[1]==='『'?'』':'”',m.index+m[0].length-x.length);if(close>0&&close-(m.index+m[0].length-x.length)<=30)x=exp.slice(m.index+m[0].length-x.length,close)}
      x=x.replace(/(?:核定|為準|之規定|規定|的|之)$/,'');
      if(x.length<2)continue;
      var hit=null;variants(x).some(function(y){if(opt.indexOf(y)>=0){hit=y;return true}});
      /* 找不到整段時，從尾巴逐字縮短（至少留 2 字；數字開頭不縮） */
      if(!hit&&!/^\d/.test(x))for(var k=x.length-1;k>=3;k--){var y=x.slice(0,k);if(opt.indexOf(y)>=0&&!/^(?:土地|政府|所有|依法|規定|應|得)$/.test(y)){hit=y;break}}
      if(hit&&(/^[\d.]+$/.test(hit)||/^(?:全部|比例|政府|一般|原則|應即|僅就|基地|所得|宅地|視為|公頃|百元|土地|規定|機關|期間|應|得)$/.test(hit)))hit=null;
      if(hit&&out.indexOf(hit)<0)out.push(hit)}
    return out};
  window.bxWrongHtml=function(h,ph){(ph||[]).forEach(function(p){var e=p.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');var i=h.indexOf(e);if(i>=0)h=h.slice(0,i)+'<mark class="bxw">'+e+'</mark>'+h.slice(i+e.length)});return h};
  /* 解析：「不是『X』」「不是X」的 X 改標紅（原本若被標成黃底，換掉） */
  window.bxWrongExp=function(h){return String(h).replace(/(錯在|不是|並非|而非|並不是|非(?=[「『]))(\s*(?:以|按|在|由|向|於)?\s*[「『]?)(?:<mark[^>]*>)?([^<，。；：、（）()「」『』\s]{1,24}?)(?:<\/mark>)?(?=[」』，。；：、）)\s]|$|核定|為準)/g,function(_,a,b,x){return a+b+'<mark class="bxw">'+x+'</mark>'})};
  /* 題幹是否問「錯誤／非／不得…」（與 bx-xrow.js 同規則的簡版） */
  window.bxWrongNeg=window.bxNegStem||function(st){st=String(st||'');var i=Math.max(st.lastIndexOf('何'),st.lastIndexOf('哪'));var t=st.slice(i<0?Math.max(0,st.length-14):i);
    return /錯誤|不正確|有誤|非(?!公共設施|都市)|不得|不屬|不包括|不包含|不是|不適用|不在(?!此限)|不需|不必|不應|不可|不能/.test(t.replace(/（[^）]*）/g,''))};
})();
