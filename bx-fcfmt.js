/* 互動單字卡背面排版（四科共用，2026-11-07）：
   ①括號外的「。」「；」後換行；②圈號只在括號外、前一字是空白／：；。時才換行（不切 §xx③ 款號）；
   ③「例：」「陷阱：」「⚠️」另起一行；④<b> 粗體＝黃底重點；長粗體（>14 字）只粗體不上底，裡面的數字＋單位才上黃底。不改資料內容。 */
(function(){
var CIR=/[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮]/;
function plainRest(h,i){return h.slice(i).replace(/<[^>]*>/g,'').replace(/\s+/g,'')}
function lb(h){return h.replace(/<b>([\s\S]*?)<\/b>/g,function(m,x){var t=x.replace(/<[^>]*>/g,'');if(t.length<=14)return m;return '<b class="lb">'+x.replace(/(^|>)([^<]*)/g,function(a,p,y){return p+y.replace(/(\d+(?:\.\d+)?\s*(?:日|個月|年|%|％|倍|分之[一二三四五六七八九十\d]+))/g,'<span class="nm">$1</span>')})+'</b>'})}
function fmt(h){return lb(fmt0(h))}
function fmt0(h){
  h=String(h==null?'':h);if(/\n/.test(h))return h;/* 已自行分行的卡（經紀法規）不再加斷行 */var lp=0,o='',d=0,prev='',prev2='',ll=0,tagLast=false,stk=[];
  for(var i=0;i<h.length;i++){
    var c=h[i];
    if(c==='<'){var j=h.indexOf('>',i);if(j<0)j=h.length-1;var tag=h.slice(i,j+1);o+=tag;i=j;tagLast=true;if(/^<br/i.test(tag)){prev='\n';ll=0}continue}
    if(c==='（'||c==='('){d++;stk.push(i)}else if(c==='）'||c===')'){d=Math.max(0,d-1);var st0=stk.pop();lp=(st0!=null)?i-st0:0}
    if(d===0&&prev&&prev!=='\n'&&ll>3){
      if(!tagLast&&CIR.test(c)&&(/[　：；。]/.test(prev)||(prev===' '&&!/[→⚠\uFE0F、，]/.test(prev2)))){o+='<br>';ll=0}
      else if((h.substr(i,2)==='例：'||h.substr(i,3)==='陷阱：'||h.substr(i,3)==='口訣：'||h.substr(i,3)==='記法：'||c==='⚠')&&!/[（(]/.test(prev)){o+='<br>';ll=0}
    }
    o+=c;prev2=prev;prev=c;tagLast=false;ll=(c==='\n')?0:ll+1;
    if(d>0&&c==='；'&&stk.length){var k=i,dd=0;for(;k<h.length;k++){var q=h[k];if(q==='（'||q==='(')dd++;else if(q==='）'||q===')'){if(dd===0)break;dd--}}
      if(k-stk[stk.length-1]>40&&plainRest(h,i+1).length>8){o+='<br>';prev='\n';ll=0}}
    if(d===0&&c==='、'&&prev2==='）'&&lp>12&&plainRest(h,i+1).length>4){o+='<br>';prev='\n';ll=0;continue}
    if(d===0&&(c==='。'||c==='；')){
      var nx=h.slice(i+1,i+6);
      if(plainRest(h,i+1)&&!/^\s*(<br|\n|<\/span><span class=.trap)/i.test(nx)&&!/^\s*[）)」』]/.test(nx)){o+='<br>';prev='\n';ll=0}
    }
  }
  return o.replace(/(<br>\s*){2,}/g,'<br>').replace(/^(\s*<br>)+/,'');
}
var css='.fcx{line-height:1.9}'
 +'.fcx b,.fcx strong{font-weight:800;background:#FFE9A3;color:inherit;padding:0 3px;border-radius:4px;-webkit-box-decoration-break:clone;box-decoration-break:clone}'
 +'.fcx b.lb{background:none;padding:0;font-weight:700}.fcx b.lb .nm{background:#FFE9A3;border-radius:4px;padding:0 3px;font-weight:800}'
 +'.fcx .exm b,:root .fcx .exm b{background:none!important;padding:0}'
 +'@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .fcx b,:root:not([data-theme="light"]) .fcx strong,:root:not([data-theme="light"]) .fcx b.lb .nm{background:rgba(232,190,90,.30)}:root:not([data-theme="light"]) .fcx b.lb{background:none}}'
 +':root[data-theme="dark"] .fcx b,:root[data-theme="dark"] .fcx strong,:root[data-theme="dark"] .fcx b.lb .nm{background:rgba(232,190,90,.30)}:root[data-theme="dark"] .fcx b.lb{background:none}';
try{var st=document.createElement('style');st.id='bx-fcfmt-css';st.textContent=css;(document.head||document.documentElement).appendChild(st)}catch(e){}
window.BXFC={fmt:fmt};
})();
