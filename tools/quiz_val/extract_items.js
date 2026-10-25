// 從 16 個章節刷題頁抽出 ITEMS（單一資料來源＝章節頁）；用法：node tools/quiz_val/extract_items.js > /tmp/quiz_items.json
const fs=require('fs');
const CH={A1:'估價刷題練習_A1',A2:'估價刷題練習_A2',A3:'估價刷題練習_A3',A4:'估價刷題練習_A4',B:'估價刷題練習_B',C1:'估價刷題練習_C1',C2:'估價刷題練習_C2',D1:'估價刷題練習_D1',D2:'估價刷題練習_D2',D3:'估價刷題練習_D3',E1:'估價刷題練習_E1',F1:'估價刷題練習_F1',G1:'估價刷題練習_G1',H1H2:'估價刷題練習_H1H2',H3I1:'估價刷題練習_H3I1',I2J1:'估價刷題練習_I2J1'};
function load(f){const s=fs.readFileSync(f,'utf8');const m=s.match(/const ITEMS\s*=\s*\[/);const st=s.indexOf(m[0])+m[0].length-1;let d=0,i=st,inS=null,esc=false;for(;i<s.length;i++){const c=s[i];if(inS){if(esc)esc=false;else if(c==='\\')esc=true;else if(c===inS)inS=null;continue}if(c==='"'||c==="'"||c==='`'){inS=c;continue}if(c==='[')d++;else if(c===']'){d--;if(d===0)break}}return eval(s.slice(st,i+1))}
const out=[];
for(const ch in CH){for(const it of load(CH[ch]+'.html')){out.push({id:it.id,ch,cat:it.cat,year:it.year,q:it.q,opts:it.opts,exps:it.explains||[],correct:it.correct,note:it.note||null})}}
process.stdout.write(JSON.stringify(out));
