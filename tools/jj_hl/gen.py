# 合併 out_*.json → hl_data.json → bxj-hl.js。改標示請改 hl_data.json 後重跑，不要手改 bxj-hl.js。
import json,glob,os
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(os.path.dirname(D))
data={}
if os.path.exists(f'{D}/hl_data.json'): data=json.load(open(f'{D}/hl_data.json',encoding='utf-8'))
for f in sorted(glob.glob(f'{D}/out_*.json')): data.update(json.load(open(f,encoding='utf-8')))
json.dump(data,open(f'{D}/hl_data.json','w',encoding='utf-8'),ensure_ascii=False,indent=0,sort_keys=True)
compact={k:[[p for p in ps] for ps in v] for k,v in data.items() if any(v)}
js='''/* 經紀法規解析黃底粗體。由 tools/jj_hl/gen.py 產生；改 tools/jj_hl/hl_data.json 後重跑，不要手改。 */
window.BXJ_HL=%s;
(function(){
  if(!document.getElementById('bxj-hl-css')){var st=document.createElement('style');st.id='bxj-hl-css';
   st.textContent='mark.bxj-hl{background:#FFE45C;color:#2a2112;font-weight:700;border-radius:3px;padding:0 2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}';
   (document.head||document.documentElement).appendChild(st);}
  function esc(t){return String(t==null?'':t).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
  /* k＝題號「年-題」；i＝選項序 0～3；回傳已跳脫的 HTML */
  window.bxjHL=function(k,i,text){
    var t=esc(text),ps=(window.BXJ_HL[k]||[])[i]||[],rs=[];
    ps.forEach(function(p){p=esc(p);var a=t.indexOf(p);
      if(a>=0&&!rs.some(function(r){return a<r[1]&&a+p.length>r[0]}))rs.push([a,a+p.length])});
    rs.sort(function(x,y){return x[0]-y[0]});var o='',c=0;
    rs.forEach(function(r){o+=t.slice(c,r[0])+'<mark class="bxj-hl">'+t.slice(r[0],r[1])+'</mark>';c=r[1]});
    return o+t.slice(c);};
})();
'''%json.dumps(compact,ensure_ascii=False,separators=(',',':'))
open(f'{R}/bxj-hl.js','w',encoding='utf-8').write(js)
print('questions',len(compact),'phrases',sum(len(p) for v in compact.values() for p in v))
