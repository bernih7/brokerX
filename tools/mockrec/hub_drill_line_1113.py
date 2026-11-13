# 指揮中心模擬卷列加「各題熟練度（含錯題複習卷）」一行；可重跑（已加者略過）
import re,sys
FN=r'''function bxDrillLine(S,pid,N){var a={};try{a=JSON.parse(localStorage.getItem("bx_drill_"+S)||"{}")}catch(e){}var d=0,t=0;for(var i=1;i<=N;i++){var r=a[pid+"-"+i];if(!r)continue;if(r.w?r.s>=3:r.c>=1)d++;else t++}return (d+t)?("各題（含錯題複習卷）：放過 "+d+"・還要練 "+t+"・沒做過 "+(N-d-t)):""}
function bxDrillAdd(el,txt){if(!el||!txt||el.querySelector(".bxdl"))return;var s=document.createElement("span");s.className="bxdl";s.style.cssText="display:block;margin-top:2px;font-weight:400;font-size:.88em;color:var(--muted,#888)";s.textContent=txt;el.appendChild(s)}
'''
MARK='function bxDrillLine('
def patch(fn,old,new):
    t=open(fn,encoding='utf-8').read()
    if MARK in t: print('skip',fn);return
    assert t.count(old)==1,(fn,t.count(old))
    open(fn,'w',encoding='utf-8').write(t.replace(old,new))
    print('ok',fn)
# 民法
o="['civ1','civ2','civls1'].forEach(function(id,i){var r=ls('bx_mock_'+id),el=$('smk'+(i+1));if(el&&r&&r.n)el.textContent='最近：已答 '+r.a+'／'+r.n+'・答對 '+r.c+'（選擇題 '+(r.c*2)+'／50）'});"
n=FN+"['civ1','civ2','civls1'].forEach(function(id,i){var r=ls('bx_mock_'+id),el=$('smk'+(i+1));if(el&&r&&r.n)el.textContent='整卷最近一次：已答 '+r.a+'／'+r.n+'・答對 '+r.c+'（選擇題 '+(r.c*2)+'／50）';bxDrillAdd(el,bxDrillLine('civ',id,25))});"
patch('民法_備考指揮中心.html',o,n)
# 經紀法規
o="document.querySelectorAll('.mk').forEach(function(el){var s=mockState(el.dataset.mock);if(!s)return;el.textContent='答 '+s.a+'/'+s.n+'・對 '+s.c+'（'+s.pct+'%）'});"
n=FN+"document.querySelectorAll('.mk').forEach(function(el){var s=mockState(el.dataset.mock);if(s)el.textContent='整卷：答 '+s.a+'/'+s.n+'・對 '+s.c+'（'+s.pct+'%）';bxDrillAdd(el,bxDrillLine('jj',el.dataset.mock,el.dataset.mock==='full5'?31:25))});"
patch('經紀法規_備考指揮中心.html',o,n)
# 估價
o="      row.innerHTML='<div class=\"mock-name\">'+m.name+'</div>'+score;\n      c.appendChild(row);"
n="      row.innerHTML='<div class=\"mock-name\">'+m.name+'</div>'+score;\n      c.appendChild(row);\n      var P={bx_mock_hs1:['hs1',25],bx_mockx_1:['mockx1',24],bx_mock_1:['vdiag1',25]},pp=P[key]||(/^bx_mockc_(\\d)$/.test(key)?['mockc'+key.slice(-1),25]:null);\n      if(pp)bxDrillAdd(row.querySelector('.mock-name'),bxDrillLine('val',pp[0],pp[1]));"
t=open('估價備考指揮中心.html',encoding='utf-8').read()
if MARK not in t:
    t=t.replace("  function renderMocks(cid){",FN+"  function renderMocks(cid){",1)
    assert t.count(o)==1
    t=t.replace(o,n);open('估價備考指揮中心.html','w',encoding='utf-8').write(t);print('ok val')
