/* bx-drill.js — 刷題頁共用：隨機排序＋固定題數抽題＋本組進度
   BXD.mount({before:el, list:el, order:true|false, res:fn(item)->null|true|false, onChange:fn})
   BXD.run(all, pool, idFn, sig) → 要顯示的陣列（先排序、再抽題）
   BXD.on() → 是否正在「固定題數」模式（頁面可用來省略年份分隔標題）
   設定（排序、題數）記在 localStorage，全站共用；抽出的那一組記在 sessionStorage（重新整理不會換題）。 */
(function(){
  var PK = 'bxd-set:' + location.pathname;
  function lg(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function ls(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }
  function sg(){ try{ return JSON.parse(sessionStorage.getItem(PK)||'null'); }catch(e){ return null; } }
  function ssv(v){ try{ sessionStorage.setItem(PK, JSON.stringify(v)); }catch(e){} }

  var N = parseInt(lg('bxd-n')||'0',10) || 0;
  var ORD = lg('bxd-ord') || 'year';
  var SEED = (sg()||{}).seed || String(Math.random()).slice(2,10);
  var cfg = null, last = [], lastIdf = null, root = null, stEl = null, obs = null, tmr = 0;

  function h(s){ var x = 2166136261; for(var i=0;i<s.length;i++){ x ^= s.charCodeAt(i); x = Math.imul(x,16777619); } x ^= x>>>16; x = Math.imul(x,0x85ebca6b); x ^= x>>>13; x = Math.imul(x,0xc2b2ae35); x ^= x>>>16; return x>>>0; }
  function save(fz){ ssv({seed:SEED, fz:fz||null}); }

  var CSS = '.bxd{display:flex;flex-direction:column;gap:8px;margin:10px 0 12px;font-size:.9rem}'
   + '.bxd-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px}'
   + '.bxd-lb{font-weight:700;margin-right:4px;opacity:.75;font-size:.85em}'
   + '.bxd-row button{font:inherit;font-size:.88em;color:inherit;background:transparent;border:1px solid color-mix(in srgb,currentColor 28%,transparent);border-radius:99px;padding:5px 13px;cursor:pointer;line-height:1.3}'
   + '.bxd-row button.on{background:color-mix(in srgb,currentColor 13%,transparent);border-color:currentColor;font-weight:700}'
   + '.bxd-row .bxd-re{margin-left:auto}'
   + '.bxd-st{border-left:3px solid currentColor;padding:6px 10px;background:color-mix(in srgb,currentColor 6%,transparent);border-radius:0 8px 8px 0;line-height:1.6}'
   + '.bxd-st b{font-variant-numeric:tabular-nums}'
   + '.bxd-st .bxd-done{font-weight:700}';

  function mount(o){
    cfg = o; if(root) return;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    root = document.createElement('div'); root.className = 'bxd';
    var html = '';
    if(o.order) html += '<div class="bxd-row" data-r="o"><span class="bxd-lb">出題順序</span><button data-o="year">依年份</button><button data-o="rand">隨機</button></div>';
    html += '<div class="bxd-row" data-r="n"><span class="bxd-lb">本次題數</span><button data-n="0">全部</button><button data-n="10">10 題</button><button data-n="20">20 題</button><button data-n="40">40 題</button><button class="bxd-re" type="button">🔀 換一組</button></div>';
    html += '<div class="bxd-st" hidden></div>';
    root.innerHTML = html;
    o.before.parentNode.insertBefore(root, o.before);
    stEl = root.querySelector('.bxd-st');
    [].forEach.call(root.querySelectorAll('button[data-o]'), function(b){ b.type='button'; b.onclick = function(){ ORD = b.dataset.o; ls('bxd-ord',ORD); mark(); change(); }; });
    [].forEach.call(root.querySelectorAll('button[data-n]'), function(b){ b.type='button'; b.onclick = function(){ N = +b.dataset.n; ls('bxd-n',String(N)); save(null); mark(); change(); }; });
    root.querySelector('.bxd-re').onclick = function(){ SEED = String(Math.random()).slice(2,10); save(null); change(); };
    mark();
    if(o.list && window.MutationObserver){
      obs = new MutationObserver(function(){ clearTimeout(tmr); tmr = setTimeout(status, 40); });
      obs.observe(o.list, {childList:true, subtree:true, attributes:true, attributeFilter:['class']});
    }
  }
  function mark(){
    if(!root) return;
    [].forEach.call(root.querySelectorAll('button[data-o]'), function(b){ b.classList.toggle('on', b.dataset.o===ORD); });
    [].forEach.call(root.querySelectorAll('button[data-n]'), function(b){ b.classList.toggle('on', +b.dataset.n===N); });
    var re = root.querySelector('.bxd-re');
    re.hidden = !(N>0 || ORD==='rand');
    re.textContent = N>0 ? '🔀 換一組' : '🔀 重新洗牌';
  }
  function change(){ if(cfg && cfg.onChange) cfg.onChange(); window.scrollTo({top: root ? Math.max(0, root.getBoundingClientRect().top + window.scrollY - 12) : 0}); }

  function run(all, pool, idf, sig){
    lastIdf = idf;
    var arr = pool.slice();
    if(N>0){
      var k = sig + '|' + N, s = sg(), fz = s && s.fz;
      if(fz && fz.k===k && s.seed===SEED){
        var m = {}; all.forEach(function(it){ m[idf(it)] = it; });
        arr = fz.ids.map(function(i){ return m[i]; }).filter(Boolean);
      } else {
        arr.sort(function(a,b){ return h(SEED+'#'+idf(a)) - h(SEED+'#'+idf(b)); });
        arr = arr.slice(0, N);
        save({k:k, ids:arr.map(idf), from:pool.length});
      }
    } else if(ORD==='rand' && cfg && cfg.order){
      arr.sort(function(a,b){ return h(SEED+'#'+idf(a)) - h(SEED+'#'+idf(b)); });
    }
    last = arr;
    setTimeout(status, 0);
    return arr;
  }
  function status(){
    if(!stEl || !cfg || !cfg.res) return;
    if(!(N>0)){ stEl.hidden = true; return; }
    var s = sg(), from = s && s.fz ? s.fz.from : last.length;
    var done=0, ok=0;
    last.forEach(function(it){ var r = cfg.res(it); if(r===true||r===false){ done++; if(r) ok++; } });
    var t = last.length;
    var html = '本組 <b>'+t+'</b> 題'+(t<N ? '（目前篩選只有 '+t+' 題）' : '（從 '+from+' 題中隨機抽）')
      + '｜已作答 <b>'+done+'</b>｜答對 <b>'+ok+'</b>｜答錯 <b>'+(done-ok)+'</b>';
    if(t && done===t) html += '<br><span class="bxd-done">✅ 這組做完了：正確率 '+Math.round(ok/t*100)+'%</span>　按「🔀 換一組」再抽 '+N+' 題';
    stEl.innerHTML = html; stEl.hidden = !t;
  }
  window.BXD = { mount:mount, run:run, on:function(){ return N>0; }, rand:function(){ return N>0 || ORD==='rand'; }, refresh:status };
})();
