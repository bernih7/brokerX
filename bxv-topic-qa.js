/* 估價｜整理頁內嵌「可作答」考古題面板　bxv-topic-qa.js
   用法：<div class="bxv-tq" data-qs="104-27,111-8" data-title="全程序順序"></div>
         或 <div class="bxv-tq" data-chs="F1" data-title="租金估計"></div>
   ⚠️ 本檔由 tools/mk_bxv_topicqa.py 從 bxj-topic-q.js 產生，**不要手改**，改上游再重跑。
   ⚠️ 與 bxv-topic-q.js（只讀版，四大方法比較表／特殊標的總整理在用）是兩支，那支不動。
   作答一律走 BXREP.rec／tag／conf，寫進共用的 bxv-q2，並雙寫章節頁存檔，
   所以在這裡答的題，刷題章節頁、錯題本、日拱一築面板都看得到。 */
(function () {
  /* 章 → 刷題章節頁的存檔前綴（與估價解析版練習的 ANS 相同） */
  var ANS = {A1:"valuation_practice_a1_v2",A2:"valuation_practice_a2_v2",A3:"valuation_practice_a3_v2",
    A4:"valuation_practice_a4_v2",B:"valuation_practice_b_v2",C1:"valuation_practice_c1_v2",
    C2:"valuation_practice_c2_v2",D1:"valuation_practice_d1_v2",D2:"valuation_practice_d2_v2",
    D3:"valuation_practice_d3_v2",E1:"valuation_practice_e1_v2",F1:"valuation_practice_f1_v2",
    G1:"valuation_practice_g1_v2",H1H2:"valuation_practice_h1h2_v2",
    H3I1:"valuation_practice_h3i1_v2",I2J1:"val_prac_i2j1_v1"};
  function stGet(k){try{return JSON.parse(localStorage.getItem("bxv-st:"+k)||"{}")||{}}catch(e){return {}}}
  function stSet(k,v){try{localStorage.setItem("bxv-st:"+k,JSON.stringify(v))}catch(e){}}
  /* BXREP 要的物件：**不可以帶 num**，帶了 qid 會變成 章-年-num */
  function ad(q){return {chapter:q.ch, year:q._year, id:q._id};}
  var TQ_DARK = '--paper2:#222926;--paper-dark:#1C2825;--paper:#1A1F1D;'
    + '--muted:var(--sub,var(--ink-soft,var(--ink-2,#9AA79F)));'
    + '--primary:var(--pri,#84C2AE);--onc:#10201B;'
    + '--hi-red:var(--red,var(--stamp,var(--trap,#E07060)));'
    + '--hi-grn:var(--green,var(--note,#8FCB93));'
    + '--hi-gold:var(--gold,var(--warn,#E0B070));'
    + '--hot:#E58A78;--hotbg:rgba(224,112,96,.16);--numfg:#F0D9A0;--numbg:rgba(240,185,60,.16)';
  var CSS = ''
    + '.bxv-tq{margin:16px 0;border:1px solid var(--line,#DDD6C3);border-radius:12px;background:var(--paper2,#F0EDE0);color:var(--fg,var(--ink,#25302C));font-size:14px;overflow:hidden}'
    + '.bxv-tq *{box-sizing:border-box}'
    + '.bxv-tq .th{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;justify-content:space-between;padding:11px 13px;border-bottom:1px solid var(--line,#DDD6C3);background:var(--paper-dark,#F0EDE0)}'
    + '.bxv-tq .th b{font-size:14.5px}'
    + '.bxv-tq .th a{color:var(--primary,var(--pri,#2F5D50));font-weight:700;text-decoration:none;font-size:12.5px;white-space:nowrap}'
    + '.bxv-tq .sm{padding:9px 13px 0;color:var(--muted,#7A8C84);font-size:12.5px;line-height:1.7}'
    + '.bxv-tq .chips{display:flex;flex-wrap:wrap;gap:6px;padding:9px 13px}'
    + '.bxv-tq .chip{border:1px solid var(--line,#DDD6C3);background:transparent;color:inherit;border-radius:999px;padding:3px 10px;font-size:12px;cursor:pointer;font-family:inherit}'
    + '.bxv-tq .chip.on{background:var(--primary,var(--pri,#2F5D50));border-color:var(--primary,var(--pri,#2F5D50));color:var(--onc,#ffffff);font-weight:700}'
    + '.bxv-tq .ls{max-height:560px;overflow:auto;border-top:1px solid var(--line,#DDD6C3)}'
    + '.bxv-tq details.qq{border-bottom:1px solid var(--line,#DDD6C3);background:var(--paper2,#F0EDE0)}'
    + '.bxv-tq details.qq[open]{background:var(--paper,#FFFEFA)}'
    + '.bxv-tq summary{cursor:pointer;padding:9px 13px;display:flex;gap:8px;align-items:baseline;list-style:none}'
    + '.bxv-tq summary::-webkit-details-marker{display:none}'
    + '.bxv-tq .yr{flex:none;color:var(--muted,#7A8C84);font-size:11.5px;min-width:54px;font-variant-numeric:tabular-nums}'
    + '.bxv-tq .st{flex:none;font-size:11.5px;font-weight:700;min-width:40px}'
    + '.bxv-tq .st.x{color:var(--hi-red,var(--vermillion,#A84030))}.bxv-tq .st.o{color:var(--hi-grn,var(--green,#2F6B45))}'
    + '.bxv-tq .st.g{color:var(--hi-gold,var(--gold,#B8782E))}.bxv-tq .st.u{color:var(--muted,#7A8C84);font-weight:400}'
    + '.bxv-tq .qt{min-width:0;line-height:1.55}'
    + '.bxv-tq .bd{padding:0 13px 13px}'
    + '.bxv-tq .ops{display:grid;gap:6px;margin:2px 0 0}'
    + '.bxv-tq .op{display:flex;gap:8px;text-align:left;width:100%;border:1px solid var(--line,#DDD6C3);background:var(--paper2,#F0EDE0);'
    + 'color:inherit;border-radius:9px;padding:8px 10px;font:inherit;font-size:13.5px;line-height:1.6;cursor:pointer}'
    + '.bxv-tq .op .L{flex:none;font-weight:800;color:var(--muted,#7A8C84)}'
    + '.bxv-tq .op:disabled{cursor:default}'
    + '.bxv-tq .op.ok{border-color:var(--hi-grn,var(--green,#2F6B45));background:color-mix(in srgb,var(--hi-grn,var(--green,#2F6B45)) 12%,transparent)}'
    + '.bxv-tq .op.ok .L{color:var(--hi-grn,var(--green,#2F6B45))}'
    + '.bxv-tq .op.ng{border-color:var(--hi-red,var(--vermillion,#A84030));background:color-mix(in srgb,var(--hi-red,var(--vermillion,#A84030)) 12%,transparent)}'
    + '.bxv-tq .op.ng .L{color:var(--hi-red,var(--vermillion,#A84030))}'
    + '.bxv-tq .me{flex:none;font-size:11px;font-weight:700;color:var(--hi-red,var(--vermillion,#A84030));align-self:center;border:1px solid currentColor;border-radius:4px;padding:0 5px}.bxv-tq .op.ok .me,.bxv-tq .me.ans{color:var(--hi-grn,var(--green,#2F6B45))}'
    + '.bxv-tq .vd{margin:9px 0 0;font-weight:800;font-size:13.5px}'
    + '.bxv-tq .vd.y{color:var(--hi-grn,var(--green,#2F6B45))}.bxv-tq .vd.n{color:var(--hi-red,var(--vermillion,#A84030))}'
    + '.bxv-tq .ex{margin-top:7px;display:grid;gap:4px;font-size:12.8px;line-height:1.65}'
    + '.bxv-tq .ex div{display:flex;gap:7px}'
    + '.bxv-tq .ex .L{flex:none;font-weight:800;color:var(--muted,#7A8C84)}'
    + '.bxv-tq .ex .y .L{color:var(--hi-grn,var(--green,#2F6B45))}'
    + '.bxv-tq .lw{margin-top:8px;border:1px solid var(--line,#DDD6C3);border-radius:8px;background:var(--paper2,#F0EDE0)}'
    + '.bxv-tq .lw>summary{padding:7px 10px;font-size:12.5px;color:var(--muted,#7A8C84);font-weight:700}'
    + '.bxv-tq .lw .lb{padding:0 10px 9px;font-size:12.6px;line-height:1.75}'
    + '.bxv-tq .lw h5{margin:7px 0 2px;font-size:12.6px;color:var(--primary,var(--pri,#2F5D50))}'
    + '.bxv-tq .lw p{margin:0 0 3px}'
    + '.bxv-tq .row{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:9px}'
    + '.bxv-tq .row .lb2{font-size:12px;color:var(--muted,#7A8C84);flex:none}'
    + '.bxv-tq .tg,.bxv-tq .sg{border:1px solid var(--line,#DDD6C3);background:var(--paper2,#F0EDE0);color:inherit;'
    + 'border-radius:8px;padding:4px 9px;font:inherit;font-size:12.2px;cursor:pointer}'
    + '.bxv-tq .tg.on{background:var(--hi-red,var(--vermillion,#A84030));border-color:var(--hi-red,var(--vermillion,#A84030));color:#fff;font-weight:700}'
    + '.bxv-tq .sg.on{background:var(--hi-grn,var(--green,#2F6B45));border-color:var(--hi-grn,var(--green,#2F6B45));color:#fff;font-weight:700}'
    + '.bxv-tq .sg[data-sh="1"].on{background:var(--hi-gold,var(--gold,#B8782E));border-color:var(--hi-gold,var(--gold,#B8782E))}'
    + '.bxv-tq .sg[data-sh="2"].on{background:var(--hi-red,var(--vermillion,#A84030));border-color:var(--hi-red,var(--vermillion,#A84030))}'
    + '.bxv-tq .again{border:1px dashed var(--line,#DDD6C3);background:transparent;color:var(--muted,#7A8C84);'
    + 'border-radius:8px;padding:4px 9px;font:inherit;font-size:12px;cursor:pointer;margin-left:auto}'
    + '.bxv-tq .oos{margin:7px 0 0;padding:8px 10px;border-radius:8px;background:var(--hotbg,rgba(168,64,43,.10));'
    + 'color:var(--hot,#A84030);font-size:12.6px;line-height:1.65;font-weight:700}'
    + '.bxv-tq .dis{margin:7px 0 0;padding:8px 10px;border-radius:8px;background:var(--numbg,rgba(240,185,60,.30));'
    + 'color:var(--numfg,#25302C);font-size:12.6px;line-height:1.65}'
    + '.bxv-tq .em{padding:16px 13px;color:var(--muted,#7A8C84)}'
    /* 深色：頁面多半沒定義 --paper2／--paper-dark／--muted／--hi-*，原 fallback 是淺色值 → 在面板上補深色 token（兩份式）；bxv-hl.js 的「完整解析」摺疊鈕 fallback #2F5D4E 在沒 --pri/--green 的頁（四大方法）會深底深字，面板內一併蓋掉 */
    + '@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .bxv-tq{' + TQ_DARK + '}'
    + ':root:not([data-theme="light"]) .bxv-tq .tg.on,:root:not([data-theme="light"]) .bxv-tq .sg.on{color:#10201B}:root:not([data-theme="light"]) .bxv-tq details.exp-more>summary{color:var(--pri,var(--green,#84C2AE))}}'
    + ':root[data-theme="dark"] .bxv-tq{' + TQ_DARK + '}'
    + ':root[data-theme="dark"] .bxv-tq .tg.on,:root[data-theme="dark"] .bxv-tq .sg.on{color:#10201B}:root[data-theme="dark"] .bxv-tq details.exp-more>summary{color:var(--pri,var(--green,#84C2AE))}'
    + '@media(max-width:420px){.bxv-tq .yr{min-width:50px}.bxv-tq .again{margin-left:0}}';

  var KN = { A: 'A 法條混淆', B: 'B 粗心', C: 'C 真的不熟', D: 'D 猜的' };

  function ld(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function sv(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function rich(t) { return esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  function qid(q) { return q.ch + '-' + q._year + '-' + q._id; }
  function db() { return ld('bxv-q2', {}); }

  /* 作答一律走 BXREP（寫 bxv-q2），再雙寫章節頁存檔，兩邊才看得到同一筆 */
  function rec(q, chosenLetter, ok) {
    var idx = 'ABCD'.indexOf(chosenLetter);
    try { if (window.BXREP && BXREP.rec) BXREP.rec(ad(q), idx, ok); } catch (e) { }
    var p = ANS[q.ch]; if (!p) return;
    var a = stGet(p + '_answers'); a[q._id] = { selected: idx, correct: !!ok }; stSet(p + '_answers', a);
    var t = stGet(p + '_errortags'); if (q._id in t) { delete t[q._id]; stSet(p + '_errortags', t); }
  }
  function tagIt(q, k) {
    try { if (window.BXREP && BXREP.tag) BXREP.tag(ad(q), k); } catch (e) { }
    var p = ANS[q.ch]; if (!p) return;
    var t = stGet(p + '_errortags'); t[q._id] = k; stSet(p + '_errortags', t);
  }
  function sureIt(q, sh) {
    try { if (window.BXREP && BXREP.conf) BXREP.conf(ad(q), sh === 1 ? 'shaky' : (sh === 2 ? 'guess' : 'sure')); } catch (e) { }
  }
  function accept(q) {
    if (q.dis && q.dis.kind === 'dual' && q.dis.alt) return [q.ans, q.dis.alt];
    return [q.ans];
  }
  function isFree(q) { return !!(q.oos || (q.dis && q.dis.kind === 'free')); }


  /* ── 把 BXV_QUIZ.items 轉成本面板要的形狀 ── */
  function build() {
    var Q = window.BXV_QUIZ; if (!Q || !Q.items) return null;
    return {
      law: {},
      q: Q.items.map(function (a) {
        return {
          k: a.y + '-' + a.n, ch: a.ch, y: a.y, n: a.n,
          stem: a.q, opt: a.opts, exp: a.exps, ans: 'ABCD'[a.correct],
          _year: a.year, _id: a.id
        };
      })
    };
  }

  function init() {
    var Q = build(); if (!Q) return;
    var byK = {}, LAW = Q.law || {};
    Q.q.forEach(function (x) { byK[x.k] = x; });
    var wclr = +(function () { try { return localStorage.getItem('bxv-wclr') || 0; } catch (e) { return 0; } })() || 0;

    document.querySelectorAll('.bxv-tq').forEach(function (box) {
      var items;
      var qs = (box.getAttribute('data-qs') || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
      if (qs.length) {
        var seen = {};
        items = qs.map(function (k) { return byK[k]; }).filter(function (x) { if (!x || seen[x.k]) return false; seen[x.k] = 1; return true; });
      } else {
        var chs = (box.getAttribute('data-chs') || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
        items = Q.q.filter(function (x) { return chs.indexOf(x.ch) >= 0 && x.sr !== 'mock'; });
      }
      items.sort(function (a, b) { return b.y - a.y || a.n - b.n; });
      if (!items.length) { box.innerHTML = ''; return; }
      var title = box.getAttribute('data-title') || '本節';

      var F = 'all';
      function stat() {
        var D = db();
        items.forEach(function (q) {
          var r = D[qid(q)];
          q._r = r || null;
          q._s = !r || !r.n ? 'u' : (r.ok ? ((r.k === 'D' || r.g === 1 || r.sh === 1) ? 'g' : 'o') : 'x');
          q._wrong = !!(r && r.n && !r.ok && (r.t || 0) > wclr);
          q._k = r ? (r.k || '') : '';
        });
      }
      function counts() {
        var c = { all: items.length, u: 0, x: 0, A: 0, B: 0, C: 0, D: 0, N: 0, g: 0 };
        items.forEach(function (q) {
          if (q._s === 'u') c.u++;
          if (q._s === 'g') c.g++;
          if (q._wrong) { c.x++; if (q._k) c[q._k]++; else c.N++; }
        });
        return c;
      }
      function match(q) {
        return F === 'all'
          || (F === 'u' && q._s === 'u')
          || (F === 'x' && q._wrong)
          || (F === 'g' && q._s === 'g')
          || (F === 'N' && q._wrong && !q._k)
          || ((F === 'A' || F === 'B' || F === 'C' || F === 'D') && q._wrong && q._k === F);
      }

      function body(q) {
        var picked = (q._r && q._r.n && q._r.c != null && q._r.c !== '') ? 'ABCD'[q._r.c] || '' : '';
        var acc = accept(q), ok = acc.indexOf(picked) >= 0 || (picked && isFree(q));
        var h = '';
        if (q.oos) h += '<div class="oos">⚠️ 這題的法源已刪除，不會再考，不計正確率。</div>';
        if (q.dis) h += '<div class="dis"><b>' + (q.dis.kind === 'free' ? '考選部一律給分' : (q.dis.kind === 'dual' ? '爭議題：兩解皆判對' : '爭議題：維持官方答案')) + '</b><br>' + rich(q.dis.why || '') + '</div>';
        h += '<div class="ops">' + q.opt.map(function (o, i) {
          var L = 'ABCD'[i], cls = '';
          if (picked) cls = acc.indexOf(L) >= 0 ? ' ok' : (L === picked ? ' ng' : '');
          return '<button type="button" class="op' + cls + '" data-l="' + L + '"' + (picked ? ' disabled' : '') + '>'
            + '<span class="L">' + L + '</span><span>' + (picked && window.bxvHL ? bxvHL(q._id, i, esc(o), 'opt', 'ABCD'.indexOf(picked), 'ABCD'.indexOf(acc[0])) : esc(o)) + '</span>'
            + (L === picked ? '<span class="me">你選的</span>' : (picked && acc.indexOf(L) >= 0 ? '<span class="me ans">正確答案</span>' : '')) + '</button>';
        }).join('') + '</div>';
        if (picked) {
          h += '<div class="vd ' + (ok ? 'y' : 'n') + '">' + (isFree(q) ? '這題不計正確率' : (ok ? '答對了' : '答錯了　你選 ' + picked + '，正確答案 ' + acc.join(' 或 '))) + '</div>';
          var _wr = !ok && !isFree(q) && window.bxvCard, _si = 'ABCD'.indexOf(picked), _ci = 'ABCD'.indexOf(acc[0]);
          if (_wr) h += bxvCard(q._id, _si, _ci, true) + bxvMore(1);
          h += '<div class="ex">' + (q.exp || []).map(function (t, i) {
            var L = 'ABCD'[i];
            return '<div class="' + (acc.indexOf(L) >= 0 ? 'y' : '') + (_wr && acc.indexOf(L) < 0 && L !== picked ? ' dim' : '') + '"><span class="L">' + L + '</span><span>' + (window.bxvHL ? bxvHL(q._id, i, rich(t), 'exp', ok ? null : 'ABCD'.indexOf(picked), 'ABCD'.indexOf(acc[0])) : rich(t)) + '</span></div>';
          }).join('') + '</div>' + (_wr ? bxvMore(0) : '');
          var ls = (q.law || []).filter(function (k) { return LAW[k]; });
          if (ls.length) {
            h += '<details class="lw"><summary>本題相關法條（' + ls.length + ' 條）</summary><div class="lb">'
              + ls.map(function (k) {
                var L = LAW[k];
                return '<h5>' + esc(k) + (L.t ? '　' + esc(L.t) : '') + (L.v === false ? '（要點整理，非逐字）' : '') + '</h5>'
                  + String(L.x || '').split('\n').map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('');
              }).join('') + '</div></details>';
          } else if (q.ref) {
            h += '<details class="lw"><summary>本題出處</summary><div class="lb"><p>' + esc(q.ref) + '</p></div></details>';
          }
          if (!isFree(q)) {
            if (ok) {
              var cs = (q._r && (q._r.sh === 0 || q._r.sh === 1 || q._r.sh === 2)) ? String(q._r.sh) : (q._r && q._r.g === 1 ? '2' : '');
              h += '<div class="row"><span class="lb2">這題你多確定？</span>'
                + [['0', '👍 很確定'], ['1', '🤔 對了但不熟'], ['2', '🎲 用猜的']].map(function (a) {
                  return '<button type="button" class="sg' + (cs === a[0] ? ' on' : '') + '" data-sh="' + a[0] + '">' + a[1] + '</button>';
                }).join('')
                + '<button type="button" class="again">再作答一次</button></div>';
            } else {
              h += '<div class="row"><span class="lb2">錯在哪？</span>'
                + ['A', 'B', 'C', 'D'].map(function (k) {
                  return '<button type="button" class="tg' + (q._k === k ? ' on' : '') + '" data-k="' + k + '">' + KN[k] + '</button>';
                }).join('')
                + '<button type="button" class="again">再作答一次</button></div>';
            }
          } else {
            h += '<div class="row"><button type="button" class="again">再作答一次</button></div>';
          }
        }
        return h;
      }

      function head() {
        var c = counts(), done = items.length - c.u;
        var deep = items.map(function (q) { return q.k; }).join(',');
        return '<div class="th"><b>🎯 考古題・' + esc(title) + '　' + items.length + ' 題</b>'
          + '<a href="估價解析版練習.html#q=' + deep + '">到練習頁連續做 →</a></div>'
          + '<div class="sm">已作答 <b>' + done + '</b>／' + items.length + '　目前錯題 <b>' + c.x + '</b>'
          + '　對了但不熟或猜的 <b>' + c.g + '</b>。作答會寫進共用紀錄，日拱一築面板與錯題本同步看得到。</div>'
          + '<div class="chips">' + [['all', '全部'], ['u', '還沒做'], ['x', '目前錯題'], ['g', '不熟／猜的'],
            ['A', 'A 混淆'], ['B', 'B 粗心'], ['C', 'C 不熟'], ['D', 'D 猜的'], ['N', '錯了沒標']]
            .map(function (a) { return '<button type="button" class="chip' + (F === a[0] ? ' on' : '') + '" data-f="' + a[0] + '">' + a[1] + ' ' + c[a[0]] + '</button>'; }).join('')
          + '</div>';
      }

      function draw(keepOpen) {
        stat();
        var open = keepOpen || {};
        box.querySelectorAll('details.qq[open]').forEach(function (d) { open[d.getAttribute('data-k')] = 1; });
        var a = items.filter(match);
        var ls = a.length ? a.map(function (q) {
          var sl = q._s === 'u' ? '還沒做' : (q._s === 'x' ? '✗ 錯' : (q._s === 'g' ? '△ 不熟' : '✓ 會'));
          return '<details class="qq" data-k="' + q.k + '"' + (open[q.k] ? ' open' : '') + '>'
            + '<summary><span class="yr">' + q.y + '-' + q.n + '</span>'
            + '<span class="st ' + q._s + '">' + sl + '</span>'
            + '<span class="qt">' + esc(q.stem) + '</span></summary>'
            + '<div class="bd">' + body(q) + '</div></details>';
        }).join('') : '<div class="em">這個條件下沒有題目。</div>';
        box.innerHTML = head() + '<div class="ls">' + ls + '</div>';
      }

      box.addEventListener('click', function (e) {
        var t = e.target;
        var chip = t.closest && t.closest('.chip');
        if (chip) { F = chip.getAttribute('data-f'); draw(); return; }
        var det = t.closest && t.closest('details.qq');
        if (!det) return;
        var q = byK[det.getAttribute('data-k')]; if (!q) return;
        var op = t.closest('.op');
        if (op && !op.disabled) { rec(q, op.getAttribute('data-l'), accept(q).indexOf(op.getAttribute('data-l')) >= 0 || isFree(q)); draw(); return; }
        var tg = t.closest('.tg'); if (tg) { tagIt(q, tg.getAttribute('data-k')); draw(); return; }
        var sg = t.closest('.sg'); if (sg) { sureIt(q, parseInt(sg.getAttribute('data-sh'), 10)); draw(); return; }
        if (t.closest('.again')) {
          var DB = db(); if (DB[qid(q)]) { DB[qid(q)].n = 0; DB[qid(q)].c = ''; delete DB[qid(q)].sh; sv('bxv-q2', DB); }
          var p = ANS[q.ch];
          if (p) { var aa = stGet(p + '_answers'); if (q._id in aa) { delete aa[q._id]; stSet(p + '_answers', aa); } }
          draw(); return;
        }
      });
      draw();
      document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') draw(); });
    });
  }

  var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
  function boot() {
    if (!document.querySelector('.bxv-tq')) return;
    if (window.BXV_QUIZ) { init(); return; }
    var s = document.createElement('script'); s.src = 'bxv-quiz-data.js'; s.onload = init; document.head.appendChild(s);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
