/* 經紀法規｜整理頁內嵌「考古題面板」——讀整理頁的時候順便作答。
   用法：<div class="bxj-tq" data-qs="99-8,100-36" data-title="聯合行為"></div>
         或 <div class="bxj-tq" data-chs="G1,G2" data-title="公平法"></div>
         ＋ <script src="bxj-topic-q.js" defer></script>
   ⚠️ 與估價 bxv-topic-q.js 的差別：這裡「可以直接作答」，作答寫入共用紀錄 bxj-q2
      （透過 BXREP.rec／tag，id＝章-年-題，與 12 支刷題頁、法條解析練習、日拱一築面板完全共用）。
   題庫來自 bxj-quiz-data.js（由 tools/essay_jj/mk_quizdata_js.py 自 quiz_data.json 產生）。 */
(function () {
  var CSS = ''
    + '.bxj-tq{margin:16px 0;border:1px solid var(--line);border-radius:12px;background:var(--paper2);color:var(--ink);font-size:14px;overflow:hidden}'
    + '.bxj-tq *{box-sizing:border-box}'
    + '.bxj-tq .th{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:baseline;justify-content:space-between;padding:11px 13px;border-bottom:1px solid var(--line);background:var(--paper-dark)}'
    + '.bxj-tq .th b{font-size:14.5px}'
    + '.bxj-tq .th a{color:var(--pri);font-weight:700;text-decoration:none;font-size:12.5px;white-space:nowrap}'
    + '.bxj-tq .sm{padding:9px 13px 0;color:var(--muted);font-size:12.5px;line-height:1.7}'
    + '.bxj-tq .chips{display:flex;flex-wrap:wrap;gap:6px;padding:9px 13px}'
    + '.bxj-tq .chip{border:1px solid var(--line);background:transparent;color:inherit;border-radius:999px;padding:3px 10px;font-size:12px;cursor:pointer;font-family:inherit}'
    + '.bxj-tq{--bxj-onc:#FFFFFF}'
    + '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .bxj-tq{--bxj-onc:#161C19}}'
    + ':root[data-theme="dark"] .bxj-tq{--bxj-onc:#161C19}'
    + '.bxj-tq .chip.on{background:var(--pri);border-color:var(--pri);color:var(--onc,var(--bxj-onc));font-weight:700}'
    + '.bxj-tq .ls{max-height:560px;overflow:auto;border-top:1px solid var(--line)}'
    + '.bxj-tq details.qq{border-bottom:1px solid var(--line);background:var(--paper2)}'
    + '.bxj-tq details.qq[open]{background:var(--paper)}'
    + '.bxj-tq summary{cursor:pointer;padding:9px 13px;display:flex;gap:8px;align-items:baseline;list-style:none}'
    + '.bxj-tq summary::-webkit-details-marker{display:none}'
    + '.bxj-tq .yr{flex:none;color:var(--muted);font-size:11.5px;min-width:54px;font-variant-numeric:tabular-nums}'
    + '.bxj-tq .st{flex:none;font-size:11.5px;font-weight:700;min-width:40px}'
    + '.bxj-tq .st.x{color:var(--vermillion)}.bxj-tq .st.o{color:var(--green)}'
    + '.bxj-tq .st.g{color:var(--gold)}.bxj-tq .st.u{color:var(--muted);font-weight:400}'
    + '.bxj-tq .qt{min-width:0;line-height:1.55}'
    + '.bxj-tq .bd{padding:0 13px 13px}'
    + '.bxj-tq .ops{display:grid;gap:6px;margin:2px 0 0}'
    + '.bxj-tq .op{display:flex;gap:8px;text-align:left;width:100%;border:1px solid var(--line);background:var(--paper2);'
    + 'color:inherit;border-radius:9px;padding:8px 10px;font:inherit;font-size:13.5px;line-height:1.6;cursor:pointer}'
    + '.bxj-tq .op .L{flex:none;font-weight:800;color:var(--muted)}'
    + '.bxj-tq .op:disabled{cursor:default}'
    + '.bxj-tq .op.ok{border-color:var(--green);background:color-mix(in srgb,var(--green) 12%,transparent)}'
    + '.bxj-tq .op.ok .L{color:var(--green)}'
    + '.bxj-tq .op.ng{border-color:var(--vermillion);background:color-mix(in srgb,var(--vermillion) 12%,transparent)}'
    + '.bxj-tq .op.ng .L{color:var(--vermillion)}'
    + '.bxj-tq .me{flex:none;font-size:11px;font-weight:700;color:var(--muted);align-self:center}'
    + '.bxj-tq .vd{margin:9px 0 0;font-weight:800;font-size:13.5px}'
    + '.bxj-tq .vd.y{color:var(--green)}.bxj-tq .vd.n{color:var(--vermillion)}'
    + '.bxj-tq .ex{margin-top:7px;display:grid;gap:4px;font-size:12.8px;line-height:1.65}'
    + '.bxj-tq .ex div{display:flex;gap:7px}'
    + '.bxj-tq .ex .L{flex:none;font-weight:800;color:var(--muted)}'
    + '.bxj-tq .ex .y .L{color:var(--green)}'
    + '.bxj-tq .lw{margin-top:8px;border:1px solid var(--line);border-radius:8px;background:var(--paper2)}'
    + '.bxj-tq .lw>summary{padding:7px 10px;font-size:12.5px;color:var(--muted);font-weight:700}'
    + '.bxj-tq .lw .lb{padding:0 10px 9px;font-size:12.6px;line-height:1.75}'
    + '.bxj-tq .lw h5{margin:7px 0 2px;font-size:12.6px;color:var(--pri)}'
    + '.bxj-tq .lw p{margin:0 0 3px}'
    + '.bxj-tq .row{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:9px}'
    + '.bxj-tq .row .lb2{font-size:12px;color:var(--muted);flex:none}'
    + '.bxj-tq .tg,.bxj-tq .sg{border:1px solid var(--line);background:var(--paper2);color:inherit;'
    + 'border-radius:8px;padding:4px 9px;font:inherit;font-size:12.2px;cursor:pointer}'
    + '.bxj-tq .tg.on{background:var(--vermillion);border-color:var(--vermillion);color:#fff;font-weight:700}'
    + '.bxj-tq .sg.on{background:var(--green);border-color:var(--green);color:#fff;font-weight:700}'
    + '.bxj-tq .sg[data-sh="1"].on{background:var(--gold);border-color:var(--gold)}'
    + '.bxj-tq .sg[data-sh="2"].on{background:var(--vermillion);border-color:var(--vermillion)}'
    + '.bxj-tq .again{border:1px dashed var(--line);background:transparent;color:var(--muted);'
    + 'border-radius:8px;padding:4px 9px;font:inherit;font-size:12px;cursor:pointer;margin-left:auto}'
    + '.bxj-tq .oos{margin:7px 0 0;padding:8px 10px;border-radius:8px;background:var(--hotbg);'
    + 'color:var(--hot);font-size:12.6px;line-height:1.65;font-weight:700}'
    + '.bxj-tq .dis{margin:7px 0 0;padding:8px 10px;border-radius:8px;background:var(--numbg);'
    + 'color:var(--numfg);font-size:12.6px;line-height:1.65}'
    + '.bxj-tq .em{padding:16px 13px;color:var(--muted)}'
    + '@media(max-width:420px){.bxj-tq .yr{min-width:50px}.bxj-tq .again{margin-left:0}}';

  var KN = { A: 'A 法條混淆', B: 'B 粗心', C: 'C 真的不熟', D: 'D 猜的' };

  function ld(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function sv(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function rich(t) { return esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
  function qid(q) { return q.ch + '-' + q.y + '-' + q.n; }
  function db() { return ld('bxj-q2', {}); }

  /* 作答一律走 BXREP，格式才會和 12 支刷題頁、法條解析練習完全一致 */
  function rec(q, chosen, ok) {
    if (window.BXREP && BXREP.rec) { try { BXREP.rec({ chapter: q.ch, year: q.y, qnum: q.n }, chosen, ok); return; } catch (e) { } }
    var DB = db(), id = qid(q), r = DB[id] || { n: 0, w: 0, h: [] };
    r.c = chosen; r.ok = ok ? 1 : 0; r.g = 0; r.k = ''; delete r.sh;
    r.t = Math.floor(Date.now() / 1000); r.n = (r.n || 0) + 1;
    if (!ok) r.w = (r.w || 0) + 1;
    (r.h = r.h || []).push([r.t, r.ok, 0]); if (r.h.length > 10) r.h.shift();
    DB[id] = r; sv('bxj-q2', DB);
  }
  function tagIt(q, k) {
    if (window.BXREP && BXREP.tag) { try { BXREP.tag({ chapter: q.ch, year: q.y, qnum: q.n }, k); return; } catch (e) { } }
    var DB = db(), r = DB[qid(q)]; if (!r) return; r.k = k; r.g = (k === 'D') ? 1 : 0; sv('bxj-q2', DB);
  }
  /* 答對自評：0 很確定／1 對了但不熟／2 用猜的（2 一併寫 g=1，沿用「猜對不算會」） */
  function sureIt(q, sh) {
    var DB = db(), r = DB[qid(q)]; if (!r) return;
    r.sh = sh; r.g = (sh === 2) ? 1 : 0; sv('bxj-q2', DB);
  }

  function accept(q) {
    if (q.dis && q.dis.kind === 'dual' && q.dis.alt) return [q.ans, q.dis.alt];
    return [q.ans];
  }
  function isFree(q) { return !!(q.oos || (q.dis && q.dis.kind === 'free')); }

  function init() {
    var Q = window.BXJ_QUIZ; if (!Q) return;
    var byK = {}, LAW = Q.law || {};
    Q.q.forEach(function (x) { byK[x.k] = x; });
    var wclr = +(function () { try { return localStorage.getItem('bxj-wclr') || 0; } catch (e) { return 0; } })() || 0;

    document.querySelectorAll('.bxj-tq').forEach(function (box) {
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
        var picked = q._r && q._r.n ? (q._r.c || '') : '';
        var acc = accept(q), ok = acc.indexOf(picked) >= 0 || (picked && isFree(q));
        var h = '';
        if (q.oos) h += '<div class="oos">⚠️ 這題的法源已刪除，不會再考，不計正確率。</div>';
        if (q.dis) h += '<div class="dis"><b>' + (q.dis.kind === 'free' ? '考選部一律給分' : (q.dis.kind === 'dual' ? '爭議題：兩解皆判對' : '爭議題：維持官方答案')) + '</b><br>' + rich(q.dis.why || '') + '</div>';
        h += '<div class="ops">' + q.opt.map(function (o, i) {
          var L = 'ABCD'[i], cls = '';
          if (picked) cls = acc.indexOf(L) >= 0 ? ' ok' : (L === picked ? ' ng' : '');
          return '<button type="button" class="op' + cls + '" data-l="' + L + '"' + (picked ? ' disabled' : '') + '>'
            + '<span class="L">' + L + '</span><span>' + esc(o) + '</span>'
            + (L === picked ? '<span class="me">你選的</span>' : '') + '</button>';
        }).join('') + '</div>';
        if (picked) {
          h += '<div class="vd ' + (ok ? 'y' : 'n') + '">' + (isFree(q) ? '這題不計正確率' : (ok ? '答對了' : '答錯了　正解：' + acc.join(' 或 '))) + '</div>';
          h += '<div class="ex">' + (q.exp || []).map(function (t, i) {
            var L = 'ABCD'[i];
            return '<div class="' + (acc.indexOf(L) >= 0 ? 'y' : '') + '"><span class="L">' + L + '</span><span>' + rich(t) + '</span></div>';
          }).join('') + '</div>';
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
          + '<a href="經紀法規_法條解析練習.html#q=' + deep + '">到練習頁連續做 →</a></div>'
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
          var DB = db(); if (DB[qid(q)]) { DB[qid(q)].n = 0; DB[qid(q)].c = ''; delete DB[qid(q)].sh; sv('bxj-q2', DB); }
          draw(); return;
        }
      });
      draw();
      document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') draw(); });
    });
  }

  var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
  function boot() {
    if (!document.querySelector('.bxj-tq')) return;
    if (window.BXJ_QUIZ) { init(); return; }
    var s = document.createElement('script'); s.src = 'bxj-quiz-data.js'; s.onload = init; document.head.appendChild(s);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
