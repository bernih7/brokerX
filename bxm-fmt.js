/* 民法頁共用：條號連結（全國法規資料庫民法 B0000001）＋重點標色。僅民法使用。 */
(function(){
var LAW='https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=B0000001&flno=';
var NUM=/\d+(?:\.\d+)?(?:～\d+)?(?:個月|週年|年|日|歲|人|倍|萬元|元|%)|[一二三四五六七八九十兩百]+(?:個月|週年|年|日|歲|人|倍|萬元|元)|[一二三四五六七八九十]+分之[一二三四五六七八九十]+|\d+分之\d+|\d+\/\d+/g;
var SKIP='A,B.k,.nm,.kw,.ef,.sec,SCRIPT,STYLE';
function inSkip(n,root){for(var p=n.parentNode;p&&p!==root;p=p.parentNode){if(p.nodeType!==1)continue;var t=p.tagName;if(t==='A'||t==='SCRIPT'||t==='STYLE')return true;var c=p.className||'';if(/(^|\s)(k|nm|kw|sec)(\s|$)/.test(c))return true}return false}
function textNodes(root){var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),a=[],n;while(n=w.nextNode())a.push(n);return a}
function wrap(root,re,mk){textNodes(root).forEach(function(n){if(inSkip(n,root))return;var s=n.nodeValue;re.lastIndex=0;if(!re.test(s))return;re.lastIndex=0;var f=document.createDocumentFragment(),i=0,m;while(m=re.exec(s)){if(m.index>i)f.appendChild(document.createTextNode(s.slice(i,m.index)));f.appendChild(mk(m[0]));i=m.index+m[0].length}if(i<s.length)f.appendChild(document.createTextNode(s.slice(i)));n.parentNode.replaceChild(f,n)})}
function link(root,skipSel){
 wrap0(root,skipSel)}
function wrap0(root,skipSel){
 var re=/§(\d+(?:-\d+)?)/g;
 textNodes(root).forEach(function(n){
  for(var p=n.parentNode;p&&p!==root;p=p.parentNode){if(p.tagName==='A'||(skipSel&&p.matches&&p.matches(skipSel)))return}
  var s=n.nodeValue;re.lastIndex=0;if(!re.test(s))return;re.lastIndex=0;
  var f=document.createDocumentFragment(),i=0,m;
  while(m=re.exec(s)){if(m.index>i)f.appendChild(document.createTextNode(s.slice(i,m.index)));
   var a=document.createElement('a');a.className='lw';a.href=LAW+m[1];a.target='_blank';a.rel='noopener';a.title='開啟全國法規資料庫 民法第'+m[1].replace('-','之')+'條';a.textContent=m[0];f.appendChild(a);i=m.index+m[0].length}
  if(i<s.length)f.appendChild(document.createTextNode(s.slice(i)));n.parentNode.replaceChild(f,n)})}
function hi(root,keyRe){
 if(keyRe)wrap(root,keyRe,function(t){var b=document.createElement('b');b.className='k kw';b.textContent=t;return b});
 wrap(root,NUM,function(t){var s=document.createElement('span');s.className='nm';s.textContent=t;return s})}
function effect(root){[].forEach.call(root.querySelectorAll('.ct'),function(el){
 var h=el.innerHTML,i=h.lastIndexOf('→');if(i<0)return;var pre=h.slice(0,i);
 if((pre.match(/<b/g)||[]).length!==(pre.match(/<\/b>/g)||[]).length)return;
 el.innerHTML=pre+'→<span class="ef">'+h.slice(i+1)+'</span>'})}
window.BXF={link:link,hi:hi,effect:effect,LAW:LAW};
})();
