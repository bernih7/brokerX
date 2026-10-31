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
   +'.bxv-fix{border-left:4px solid #E7C74A;background:#FFF6CC;color:#2B2620;border-radius:8px;padding:10px 12px;margin:10px 0 8px;font-size:13.5px;line-height:1.75}'
   +'.bxv-fix .h{font-weight:700;color:#A84030;font-size:13px;margin-bottom:4px}'
   +'.bxv-fix .rw{display:grid;grid-template-columns:4.6em 1fr;gap:2px 8px}.bxv-fix .k{color:#857B6C;font-size:12px;padding-top:2px}'
   +'.bxv-fix .r{color:#A84030}.bxv-fix .g{font-weight:700}'
   +'@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .bxv-fix{background:#3A3220;color:#ECE5D8;border-left-color:#8A7430}:root:not([data-theme="light"]) .bxv-fix .r,:root:not([data-theme="light"]) .bxv-fix .h{color:#E58A78}:root:not([data-theme="light"]) .bxv-fix .k{color:#A79D8C}}'
   +':root[data-theme="dark"] .bxv-fix{background:#3A3220;color:#ECE5D8;border-left-color:#8A7430}:root[data-theme="dark"] .bxv-fix .r,:root[data-theme="dark"] .bxv-fix .h{color:#E58A78}:root[data-theme="dark"] .bxv-fix .k{color:#A79D8C}'
   +'details.exp-more>summary{cursor:pointer;font-size:12.5px;color:var(--pri,var(--green,#2F5D4E));margin:4px 0;list-style:none;font-weight:600}details.exp-more>summary::-webkit-details-marker{display:none}details.exp-more>summary::before{content:"▸ 看"}details.exp-more[open]>summary::before{content:"▾ 收起"}'
   +'details.exp-more[open]>summary{margin-bottom:6px}.explain-item.dim,.xr.dim,.bxv-tq .ex>div.dim{opacity:.55}';
  (document.head||document.documentElement).appendChild(st);}
  function mk(text,specs){
    text=String(text==null?'':text);var rs=[];
    specs.forEach(function(s){var p=s[0];if(!p)return;var k=text.indexOf(p);
      if(k>=0&&!rs.some(function(r){return k<r[1]&&k+p.length>r[0]})&&!/<[^>]*$/.test(text.slice(0,k)))rs.push([k,k+p.length,s[1]]);});
    rs.sort(function(a,b){return a[0]-b[0]});var o='',c=0;
    rs.forEach(function(r){o+=text.slice(c,r[0])+'<mark class="'+r[2]+'">'+text.slice(r[0],r[1])+'</mark>';c=r[1]});
    return o+text.slice(c);}
  function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
  /* kind:'opt' 標選項錯字；'exp' 標解析正確資訊。給 sel／cor 時只標「你選的」與「答案」兩個選項 */
  window.bxvHL=function(id,i,text,kind,sel,cor){
    if(sel!=null&&i!==sel&&i!==cor)return text;
    var r=(window.BXV_HL||{})[id];var a=r&&r[i];if(!a)return text;
    return mk(text,(kind==='opt'?a[0]:a[1]).map(function(p){return[p,kind==='opt'?'hl-err':'hl-ok']}));};
  var STRIKE={'錯在':1,'答案錯在':1,'你算的':1},BOLD={'應該是':1,'因為':1,'正確算法':1};
  /* 更正卡：noHead=true 時不印「你選 X，答案是 Y」那行（頁面已有判定列） */
  window.bxvCard=function(id,sel,cor,noHead){
    var r=(window.BXV_CARD||{})[id],rows=r&&r[sel];
    if(noHead&&!rows)return '';
    var h='<div class="bxv-fix">'+(noHead?'':'<div class="h">✗ 你選 '+'ABCD'[sel]+'，答案是 '+'ABCD'[cor]+'</div>');
    if(rows){h+='<div class="rw">'+rows.map(function(x){var t=esc(x[1]);
      return '<span class="k">'+x[0]+'</span><span'+(BOLD[x[0]]?' class="g"':'')+'>'+(STRIKE[x[0]]?'<span class="r">'+t+'</span>':t)+'</span>'}).join('')+'</div>';}
    return h+'</div>';};
  window.bxvMore=function(open){return open?'<details class="exp-more"><summary>四個選項的完整解析</summary>':'</details>'};
})();
"""
import os
card=json.load(open('tools/quiz_val/card_data.json',encoding='utf-8')) if os.path.exists('tools/quiz_val/card_data.json') else {}
card={k:v for k,v in card.items() if v and any(v)}
js='/* 由 tools/quiz_val/gen_hl.py 產生；資料改 tools/quiz_val/hl_data.json／card_data.json 後重跑，不要手改。 */\nwindow.BXV_HL='+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\nwindow.BXV_CARD='+json.dumps({k:[(c['rows'] if c else 0) for c in v] for k,v in card.items()},ensure_ascii=False,separators=(',',':'))+';\n'+HELPER
open('bxv-hl.js','w',encoding='utf-8').write(js)
print('題',len(out),'標註選項',sum(1 for r in out.values() for a in r if a),'bytes',len(js.encode()))
