// 深淺色對比掃描：node tools/theme/contrast_scan.js <dark|light> <out.json> [檔名過濾regex]
// 需先在 repo 根目錄開 python3 -m http.server 8777。回報文字與實際底色對比 < 3 的元素（同頁同文字去重）。
// 祖先有 background-image（漸層）時底色無法判定，標 grad 另列，需人工看截圖。
const {chromium}=require('playwright');const fs=require('fs');
const mode=process.argv[2]||'dark',outp=process.argv[3]||'/tmp/contrast.json',flt=process.argv[4]?new RegExp(process.argv[4]):null;
const files=fs.readdirSync('.').filter(f=>f.endsWith('.html')&&(!flt||flt.test(f)));
(async()=>{const b=await chromium.launch();const out={};
const ctx=await b.newContext({viewport:{width:1100,height:900},colorScheme:'light'});await ctx.addInitScript(m=>{try{localStorage.setItem('bx-theme',m)}catch(e){}},mode);
for(const f of files){const p=await ctx.newPage();
 try{await p.goto('http://localhost:8777/'+encodeURI(f),{waitUntil:'load',timeout:20000});await p.waitForTimeout(500);
 await p.evaluate(()=>{document.querySelectorAll('details').forEach(d=>d.open=true)});
 const bad=await p.evaluate(()=>{
  function rgb(s){const m=s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null}
  function lum(c){const a=c.slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)});return .2126*a[0]+.7152*a[1]+.0722*a[2]}
  function bg(el){let e=el;while(e){const cs=getComputedStyle(e);if(cs.backgroundImage&&cs.backgroundImage!=='none'&&/gradient/.test(cs.backgroundImage))return 'grad';const c=rgb(cs.backgroundColor);if(c&&c[3]>0.5)return c;e=e.parentElement}return rgb(getComputedStyle(document.body).backgroundColor)||[255,255,255,1]}
  const res=[];const seen=new Set();
  for(const el of document.querySelectorAll('body *')){
   if(/blank-mask/.test(el.className))continue;
   let txt='';for(const n of el.childNodes)if(n.nodeType===3)txt+=n.textContent;txt=txt.trim();if(txt.length<1)continue;
   const r=el.getBoundingClientRect();if(r.width<2||r.height<2)continue;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||cs.display==='none')continue;
   let op=1,e=el;while(e){op*=+getComputedStyle(e).opacity;e=e.parentElement}if(op<0.35)continue;
   const fg=rgb(cs.color);if(!fg||fg[3]<0.2)continue;const b=bg(el);
   const k=txt.slice(0,24)+'|'+el.className;if(seen.has(k))continue;seen.add(k);
   if(b==='grad'){continue}
   const L1=lum(fg),L2=lum(b);const cr=(Math.max(L1,L2)+.05)/(Math.min(L1,L2)+.05);
   if(cr<3)res.push([+cr.toFixed(2),txt.slice(0,30),cs.color,'bg:'+b.slice(0,3).join(','),el.tagName+'.'+(el.className||'').toString().slice(0,40)])
  }return res});
 if(bad.length)out[f]=bad;}catch(e){out[f]=[['ERR',e.message.slice(0,80)]]}
 await p.close()}
fs.writeFileSync(outp,JSON.stringify(out,null,1));
const n=Object.values(out).reduce((a,v)=>a+v.length,0);
console.log(mode,'pages',files.length,'with issues',Object.keys(out).length,'items',n,'severe(<1.6)',Object.values(out).flat().filter(r=>r[0]<1.6).length);await b.close()})();
