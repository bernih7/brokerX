# 土地法 5 分鐘兩頁：首頁最上方類別篩選（11-05，可重跑）
import os,re
H=os.path.dirname(os.path.abspath(__file__))
CSS='''/*flt*/.flt{margin:8px 0 14px;border:1px solid var(--line);border-radius:14px;background:var(--surface);padding:10px 12px;display:grid;gap:6px}
.flt .fr{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.flt .fl{font-size:.76rem;font-weight:700;color:var(--sub);min-width:2.6em}
.flt button{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:999px;padding:2px 11px;font-size:.84rem;line-height:1.6}
.flt button.on{background:var(--pri);border-color:var(--pri);color:var(--on);font-weight:700}
.flt .fs{display:flex;justify-content:space-between;align-items:center;font-size:.8rem;color:var(--sub)}
.flt .fs a{cursor:pointer}
'''
HTML='''<div class="flt" id="flt"></div>'''
JS='''/*flt*/
var FK='bx-land-sprint-flt',FLT={g:'',k:'',p:'',s:''};try{var _f=JSON.parse(localStorage.getItem(FK)||'{}');for(var _k in FLT)if(_f[_k])FLT[_k]=_f[_k]}catch(e){}
var GS={'地價稅・土地增值稅':'地價稅・土增稅','都市計畫・公共設施保留地・說明書解說':'都計・公保地','房屋稅・契稅・房地合一（持有與交易稅）':'房屋稅・契稅・房地合一','土地登記・優先購買權・實價登錄':'登記・優購・實價登錄','地權總則・農地・非都市管制':'地權・農地・非都市','土地徵收・區段徵收':'徵收・區段徵收','市地重劃・空地・限期建築':'重劃・空地'};
function fpass(c,s){if(FLT.g&&c.g!==FLT.g)return false;if(FLT.k&&c.k!==FLT.k)return false;
 if(FLT.p==='h'&&c.hpl!=='高')return false;if(FLT.p==='hm'&&!c.hpl)return false;
 if(FLT.s){s=s||stat(c.id);var nw=!s.n&&!s.sp&&!s.read;if(FLT.s==='new'&&!nw)return false;if(FLT.s==='weak'&&!(s.v===2||s.v===3))return false}
 return true}
function fpool(){return CARDS.filter(function(c){return fpass(c)})}
function fdraw(){var GR=[];CARDS.forEach(function(c){if(GR.indexOf(c.g)<0)GR.push(c.g)});
 function row(lab,key,opts){return '<div class="fr"><span class="fl">'+lab+'</span>'+opts.map(function(o){return '<button type="button" data-k="'+key+'" data-v="'+esc(o[0])+'"'+(FLT[key]===o[0]?' class="on"':'')+'>'+esc(o[1])+'</button>'}).join('')+'</div>'}
 var n=fpool().length,act=FLT.g||FLT.k||FLT.p||FLT.s;
 $('flt').innerHTML=row('類別','g',[['','全部']].concat(GR.map(function(g){return [g,GS[g]||g]})))+row('來源','k',[['','全部'],['off','官方'],['pred','預測・專題'],['mock','模擬']])+row('115','p',[['','全部'],['h','🔥 高機率'],['hm','🔥 高＋中']])+row('狀態','s',[['','全部'],['new','沒做過'],['weak','做過不熟']])+'<div class="fs"><span>符合 '+n+'／'+CARDS.length+' 題；「開始下一題」「隨機出題」只從這裡出</span>'+(act?'<a id="fclr">清除篩選</a>':'')+'</div>';
 [].forEach.call($('flt').querySelectorAll('button'),function(b){b.onclick=function(){var k=b.getAttribute('data-k'),v=b.getAttribute('data-v');FLT[k]=(FLT[k]===v?'':v);try{localStorage.setItem(FK,JSON.stringify(FLT))}catch(e){}home()}});
 var cl=$('fclr');if(cl)cl.onclick=function(){FLT={g:'',k:'',p:'',s:''};try{localStorage.removeItem(FK)}catch(e){}home()}}
'''
for fn in ['tpl.html','tpl_reason.html']:
    p=os.path.join(H,fn); s=open(p,encoding='utf-8').read()
    if '/*flt*/' in s: print(fn,'已有'); continue
    s=s.replace('</style>',CSS+'</style>',1)
    s=re.sub(r'(<p class="lead">.*?</p>)',lambda m:m.group(1)+'\n    '+HTML,s,count=1,flags=re.S)
    # order(): filter
    s=s.replace("var arr=CARDS.map(function(c,i){var s=stat(c.id);return {c:c,s:s,i:i}});","var arr=CARDS.map(function(c,i){var s=stat(c.id);return {c:c,s:s,i:i}}).filter(function(x){return fpass(x.c,x.s)});",1)
    s=s.replace("var arr=CARDS.map(function(c,i){return {c:c,s:stat(c.id),i:i}});","var arr=CARDS.map(function(c,i){return {c:c,s:stat(c.id),i:i}}).filter(function(x){return fpass(x.c,x.s)});",1)
    s=s.replace("function randPick(ex){var a=CARDS.filter(function(c){return c.id!==ex});","function randPick(ex){var a=fpool().filter(function(c){return c.id!==ex});if(!a.length)a=CARDS.filter(function(c){return c.id!==ex});",1)
    s=s.replace("$('startBtn').onclick=function(){pick='order';start(order()[0].c.id)};","$('startBtn').onclick=function(){pick='order';var o=order();if(!o.length){alert0();return}start(o[0].c.id)};\nfunction alert0(){var f=$('flt');if(f){f.scrollIntoView({block:'start'});f.style.outline='2px solid var(--bad)';setTimeout(function(){f.style.outline=''},1200)}}",1)
    s=s.replace("var showAll=false;","var showAll=false;\n"+JS,1)
    s=s.replace("function home(){\n  swGo('');","function home(){\n  swGo('');fdraw();",1)
    assert s.count('fpass(')>=3 and 'fdraw();' in s and 'id="flt"' in s, fn
    open(p,'w',encoding='utf-8').write(s); print(fn,'ok')
