#!/usr/bin/env python3
"""產生 bxv-hl.js：答完題後「選項錯在哪（黃底紅線）」「解析的正確資訊（黃底粗體）」標記。
資料：tools/quiz_val/hl_data.json  {id:[null|{"e":[選項子字串],"f":[解析子字串]}]*4}
用法（repo 根目錄）：node tools/quiz_val/extract_items.js > /tmp/quiz_items.json && python3 tools/quiz_val/gen_hl.py
會先檢查每個 e／f 都是目前章節頁 opts／explains 的逐字子字串，對不上就不寫檔。"""
import json,sys
items={x['id']:x for x in json.load(open('/tmp/quiz_items.json'))}
hl=json.load(open('tools/quiz_val/hl_data.json',encoding='utf-8'))
bad=[];out={}
for k,v in hl.items():
    x=items.get(k)
    if not x: bad.append(f'{k} 不在題庫');continue
    row=[];any_=False
    for i,a in enumerate(v):
        if not a or not a.get('e'): row.append(0);continue
        for e in a['e']:
            if e not in x['opts'][i]: bad.append(f'{k}[{i}] e：{e}')
        for f in a.get('f',[]):
            if f not in x['exps'][i]: bad.append(f'{k}[{i}] f：{f}')
        row.append([a['e'],a.get('f',[])]);any_=True
    if any_: out[k]=row
if bad: print('\n'.join(bad));sys.exit('有對不上的標記，未寫檔')
HELPER=r"""
(function(){
  if(!document.getElementById('bxv-hl-css')){var st=document.createElement('style');st.id='bxv-hl-css';
  st.textContent='mark.hl-err,mark.hl-ok{background:#FFE45C;color:#2a2112;border-radius:3px;padding:0 2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}'
   +'mark.hl-err{box-shadow:inset 0 -2px 0 #C0392B}mark.hl-ok{font-weight:700}'
   +'mark.hl-bad{background:none;color:inherit;text-decoration:underline 2px #D0392B;text-underline-offset:3px;text-decoration-skip-ink:none}'
   +'.hl-legend{display:block;font-size:11px;font-weight:400;color:var(--muted,#8a7f6e);margin-top:2px;letter-spacing:0}'
   +'.hl-legend mark{font-size:11px}';
  (document.head||document.documentElement).appendChild(st);}
  function mk(text,specs){
    text=String(text==null?'':text);var rs=[];
    specs.forEach(function(s){var p=s[0];if(!p)return;var k=text.indexOf(p);
      while(k>=0){var ov=rs.some(function(r){return k<r[1]&&k+p.length>r[0]});
        if(!ov&&!/<[^>]*$/.test(text.slice(0,k)))rs.push([k,k+p.length,s[1]]);
        if(!s[2])break;k=text.indexOf(p,k+p.length);}});
    rs.sort(function(a,b){return a[0]-b[0]});var o='',c=0;
    rs.forEach(function(r){o+=text.slice(c,r[0])+'<mark class="'+r[2]+'">'+text.slice(r[0],r[1])+'</mark>';c=r[1]});
    return o+text.slice(c);}
  /* kind:'opt' 標選項錯字；'exp' 標解析正確資訊＋錯字紅底線 */
  window.bxvHL=function(id,i,text,kind){
    var r=(window.BXV_HL||{})[id];var a=r&&r[i];if(!a)return text;
    if(kind==='opt')return mk(text,a[0].map(function(p){return[p,'hl-err',0]}));
    return mk(text,a[1].map(function(p){return[p,'hl-ok',0]}).concat(a[0].filter(function(p){return p.length>=2}).map(function(p){return[p,'hl-bad',1]})));};
  window.bxvHLlegend='<span class="hl-legend">選項中 <mark class="hl-err">黃底紅線</mark>＝錯在這裡；解析中 <mark class="hl-ok">黃底粗體</mark>＝正確資訊</span>';
})();
"""
js='/* 由 tools/quiz_val/gen_hl.py 產生；資料改 tools/quiz_val/hl_data.json 後重跑，不要手改。 */\nwindow.BXV_HL='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n'+HELPER
open('bxv-hl.js','w',encoding='utf-8').write(js)
print('題',len(out),'標註選項',sum(1 for r in out.values() for a in r if a),'bytes',len(js.encode()))
