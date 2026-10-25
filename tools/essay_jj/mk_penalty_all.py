# -*- coding: utf-8 -*-
"""四個罰則頁收成一套：建立唯一資料源 penalty.json，並重建《罰鍰與處分一覽表》。

起因：同一條號在四個頁面各寫一遍，而且裸寫「§17」根本分不出是哪一部法——
經紀業條例§17（僱用未具資格者，6–30萬）、公寓大廈§17（未投保，4–20萬）、
消保法§17（定型化契約應記載事項）是三件完全不同的事。

做法：
  1. 把《罰鍰與處分一覽表》既有的 var D（73 筆，已逐筆對過 lawfull.json，金額
     全部正確）抽成 tools/essay_jj/penalty.json，作為四頁共用的唯一資料源。
  2. 補上原本沒有的 org 欄（誰罰）。這是使用者指出「罰誰、誰罰、罰多少沒想清楚」
     裡唯一還缺的一欄。
  3. 條號一律帶法規全名，不再裸寫 §N。
  4. 一覽表用《公寓大廈條例罰則整理》同一套版型重建：一筆一卡、固定四欄。

執行：python3 tools/essay_jj/mk_penalty_all.py
"""
import collections
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PJ = os.path.join(HERE, 'penalty.json')
LAW = json.load(io.open(os.path.join(HERE, 'law', 'lawfull.json'), encoding='utf-8'))
DST = os.path.join(ROOT, '經紀法規_罰鍰與處分一覽表.html')

SRC = io.open(os.path.join(ROOT, '經紀法規_程序總整理.html'), encoding='utf-8').read()
BASECSS = re.search(r'<style>([\s\S]*?)</style>', SRC).group(1)
FAB = SRC[SRC.index('<!--bxfab-->'):SRC.index('<!--/bxfab-->') + len('<!--/bxfab-->')]
QZ = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html'

FULL = {'條例': '不動產經紀業管理條例', '細則': '不動產經紀業管理條例施行細則',
        '公寓': '公寓大廈管理條例', '公平法': '公平交易法', '消保法': '消費者保護法'}
SHORT = {'條例': '經紀業條例', '細則': '施行細則', '公寓': '公寓大廈',
         '公平法': '公平法', '消保法': '消保法'}

LOCAL = '直轄市、縣（市）主管機關'
CENTRAL = '<b class="ctr">中央主管機關</b>'
FTC = '<b class="ctr">公平交易委員會</b>'
COURT = '法院（刑事）'

# ── 誰罰：依法規與條號決定，例外逐條列出 ──
def org_of(r):
    law, art = r['law'], r['art']
    if r['kind'] == '刑責':
        return COURT + '；須由主管機關先移送'
    if law == '公平法':
        return FTC + '（中央）'
    if law == '消保法':
        if art in ('§51', '§60'):
            return '法院（民事）' if art == '§51' else LOCAL
        return LOCAL
    if law == '公寓':
        if art.startswith('§51'):
            return CENTRAL
        return LOCAL
    if law == '條例':
        if art.startswith('§31'):
            return '經紀業所在地' + LOCAL + '<b class="ctr">交付懲戒</b>'
        if art.startswith('§32'):
            return LOCAL + '<span class="sub2x">（管轄見下方說明）</span>'
        return LOCAL
    return LOCAL


def build():
    s = io.open(DST, encoding='utf-8').read()
    i = s.index('var D=[')
    j = s.index('];', i)
    D = json.loads(s[i + 6:j + 1])
    for r in D:
        r['lawfull'] = FULL[r['law']]
        r['lawshort'] = SHORT[r['law']]
        r['org'] = org_of(r)
    json.dump(D, io.open(PJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return D


D = build() if not os.path.exists(PJ) else json.load(io.open(PJ, encoding='utf-8'))
# 每次都重算 org，方便調整規則
for r in D:
    r['lawfull'] = FULL[r['law']]
    r['lawshort'] = SHORT[r['law']]
    r['org'] = org_of(r)
json.dump(D, io.open(PJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ── 逐筆對條文驗金額 ──
CN = '零一二三四五六七八九十百千萬億'
DIG = {c: i for i, c in enumerate('零一二三四五六七八九')}


def cn(x):
    u = {'十': 10, '百': 100, '千': 1000}
    tot = cur = big = 0
    for c in x:
        if c in DIG:
            cur = DIG[c]
        elif c in u:
            cur = cur or 1
            tot += cur * u[c]
            cur = 0
        elif c == '萬':
            big += (tot + cur or 1) * 10000
            tot = cur = 0
        elif c == '億':
            big += (tot + cur or 1) * 100000000
            tot = cur = 0
    return big + tot + cur


bad = []
for r in D:
    if r['kind'] != '罰鍰':
        continue
    m = re.match(r'§\s*(\d+)(?:[之\-](\d+))?', r['art'])
    if not m:
        continue
    key = '%s §%s' % (r['lawshort'], m.group(1)) + ('之%s' % m.group(2) if m.group(2) else '')
    v = LAW.get(key)
    if not v:
        bad.append((key, '條文庫查無'))
        continue
    found = {(cn(a), cn(b)) for a, b in
             re.findall(r'新臺幣([%s]+)元以上([%s]+)元以下' % (CN, CN), v['text'])}
    lo, hi = int(float(r['lo']) * 10000), int(float(r['hi']) * 10000)
    if found and (lo, hi) not in found:
        bad.append((key, '表 %s｜條文 %s' % (r['amt'],
                    '、'.join('%g萬-%g萬' % (a / 10000, b / 10000) for a, b in sorted(found)))))

# ── 版型：一筆一卡、固定四欄（與公寓大廈罰則頁同一套）──
TIER = [(0, 0.5, 'ta'), (0.5, 2, 'tb'), (2, 3.1, 'tc'), (3.1, 1e9, 'td')]


def tier(r):
    try:
        lo = float(r['lo'])
    except Exception:
        return 'tb'
    for a, b, c in TIER:
        if a <= lo < b:
            return c
    return 'td'


KINDLAB = {'罰鍰': '罰鍰', '停業廢止': '停業・廢止', '人員處分': '人員處分',
           '刑責': '刑責', '賠償': '損害賠償'}


def card(r):
    raw = (r.get('note') or '').strip()
    if raw.startswith('◆'):
        raw = raw.split('｜', 1)[1].strip() if '｜' in raw else ''
    note = ('<div class="nt">%s</div>' % raw) if raw else ''
    return (
        '<article class="act %s" data-law="%s" data-kind="%s">'
        '<div class="hd"><span class="ar">%s %s</span><h3>%s</h3>'
        '<span class="kd">%s</span></div>'
        '<div class="rows">'
        '<div class="row"><span class="k">罰誰</span><span class="v">%s</span></div>'
        '<div class="row"><span class="k">誰罰</span><span class="v">%s</span></div>'
        '<div class="row"><span class="k">罰多少</span><span class="v amtv">%s</span></div>'
        '<div class="row"><span class="k">程序</span><span class="v">%s</span></div>'
        '</div>%s</article>'
        % (tier(r), r['law'], r['kind'], r['lawshort'], r['art'], r['act'],
           KINDLAB.get(r['kind'], r['kind']), r['who'], r['org'], r['amt'],
           r.get('cond') or '—', note))


CSS = '''
.filters{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}
.fb2{font:inherit;font-size:.82rem;font-weight:700;padding:5px 12px;border-radius:99px;
  border:1.5px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.fb2.on{border-color:var(--pri);background:var(--pri);color:var(--on)}
.cntline{margin-top:9px;font-size:.82rem;color:var(--muted)}
.acts{display:grid;gap:11px;margin-top:11px}
.act{border:1px solid var(--line);border-left:5px solid var(--c,var(--line));
  border-radius:11px;background:var(--card);padding:11px 13px 12px}
.act.ta{--c:#7A8B72}.act.tb{--c:#B8782E}.act.tc{--c:#8A5517}.act.td{--c:#A8402B}
:root[data-theme="dark"] .act.ta{--c:#9DB295}
:root[data-theme="dark"] .act.tb{--c:#E0B070}
:root[data-theme="dark"] .act.tc{--c:#E0B070}
:root[data-theme="dark"] .act.td{--c:#E05040}
@media(prefers-color-scheme:dark){
 :root:not([data-theme="light"]) .act.ta{--c:#9DB295}
 :root:not([data-theme="light"]) .act.tb{--c:#E0B070}
 :root:not([data-theme="light"]) .act.tc{--c:#E0B070}
 :root:not([data-theme="light"]) .act.td{--c:#E05040}}
.act .hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:7px}
.act .ar{font-weight:700;color:var(--key);font-size:.9rem;flex:none}
.act h3{font-family:"Noto Serif TC",serif;font-size:15px;color:var(--ink);
  flex:1;min-width:0;line-height:1.55;margin:0;font-weight:700}
.act .kd{flex:none;font-size:.74rem;color:var(--muted);border:1px solid var(--line);
  border-radius:99px;padding:1px 8px}
.act .rows{margin-top:9px;display:grid;gap:5px}
.act .row{display:grid;grid-template-columns:3.6em 1fr;gap:9px;font-size:13.5px;
  line-height:1.8;align-items:start}
.act .row .k{color:var(--muted);font-size:.8rem;font-weight:700;padding-top:2px;letter-spacing:.04em}
.act .row .v{color:var(--ink);min-width:0}
.act .row .v.amtv{color:var(--key);font-weight:700}
.act .nt{margin-top:9px;padding:7px 10px;border-radius:8px;background:var(--bg);
  border:1px solid var(--line);border-left:4px solid var(--red);
  font-size:13px;line-height:1.85;color:var(--ink)}
.sub2x{font-size:.82em;color:var(--muted)}
.ctr{color:var(--red);font-weight:700}
.act[hidden]{display:none}
.lawgrp{margin-top:18px}
.lawgrp[hidden]{display:none}
.lgh{font-family:"Noto Serif TC",serif;font-size:16.5px;color:var(--pri);margin:0 0 7px;
  display:flex;align-items:baseline;gap:9px;padding-bottom:6px;border-bottom:2px solid var(--pri)}
.lgn{font-size:.74rem;color:var(--muted);font-family:inherit;font-weight:400}
.jur{border:1px solid var(--line);border-left:4px solid var(--pri);border-radius:9px;
  background:var(--card);padding:9px 12px;font-size:13.5px;line-height:1.9;color:var(--ink)}
.jur>b:first-child{display:block;width:fit-content;font-size:.74rem;font-weight:700;
  background:var(--pri);color:var(--on);border-radius:99px;padding:2px 9px;margin:0 0 5px}
.jur b{color:var(--ink)}
.mnx{margin-top:7px;border:1px solid var(--line);border-left:4px solid var(--green);
  border-radius:9px;background:var(--card);padding:9px 12px}
.mnx>b:first-child{display:block;width:fit-content;font-size:.74rem;font-weight:700;
  background:var(--green);color:#fff;border-radius:99px;padding:2px 9px;margin:0 0 5px}
:root[data-theme="dark"] .mnx>b:first-child,:root[data-theme="dark"] .jur>b:first-child{color:#10201B}
.mnc{font-family:"Noto Serif TC",serif;font-size:15.5px;font-weight:700;letter-spacing:.14em;color:var(--ink)}
.mnn{display:block;margin-top:4px;font-size:12.5px;color:var(--muted)}
'''

LAWS = ['條例', '公寓', '公平法', '消保法']
KINDS = ['罰鍰', '停業廢止', '人員處分', '刑責', '賠償']


def artnum(a):
    m = re.match(r'§\s*(\d+)(?:[之\-](\d+))?', a)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (999, 0)


# 每個法規只講一次管轄
JUR = {
 '條例': '管轄依施行細則：§29 的處罰由<b>經紀業所在地</b>主管機關為之，'
         '但 §29Ⅰ①②或Ⅱ 且營業處所或執行業務行為地不同轄區者，由該地主管機關為之（細則§25-1）；'
         '§14Ⅲ、§31Ⅱ 由<b>原發證之戶籍所在地</b>主管機關為之（細則§26）；'
         '§32Ⅰ 由公司或商號所在地主管機關為之，行為地不同者由行為地查明後移請（細則§28-1）。',
 '公寓': '除 <b class="ctr">§51（管理維護公司與管理服務人員）歸中央主管機關</b>外，'
         '§47、§48、§49、§49-1、§50 全部是直轄市、縣（市）主管機關。這是整章唯一的例外。',
 '公平法': '一律由<b class="ctr">公平交易委員會</b>（中央主管機關）處分；刑責部分須由公平會移送檢察機關。',
 '消保法': '罰鍰由直轄市、縣（市）主管機關處分；§51 懲罰性賠償金是<b>法院</b>依消費者請求判決，不是行政罰。',
}


def grp(law):
    rows = sorted([r for r in D if r['law'] == law],
                  key=lambda r: (KINDS.index(r['kind']) if r['kind'] in KINDS else 9, artnum(r['art'])))
    mn = ''.join(re.match(r'◆(\S)', r['note']).group(1)
                 for r in rows if (r.get('note') or '').startswith('◆'))
    head = ('<div class="lawgrp" data-law="%s"><h3 class="lgh">%s<span class="lgn">%d 筆</span></h3>'
            '<div class="jur"><b>誰罰</b>%s</div>' % (law, FULL[law], len(rows), JUR[law]))
    if mn:
        head += ('<div class="mnx"><b>記憶字</b><span class="mnc">%s</span>'
                 '<span class="mnn">每張卡依序取一字，整組串起來背</span></div>' % mn)
    return head + '<div class="acts">%s</div></div>' % ''.join(card(r) for r in rows)


FILTERS = ('<div class="filters">'
           + ''.join('<button class="fb2 on" data-f="law:%s">%s</button>' % (l, FULL[l]) for l in LAWS)
           + '</div><div class="filters">'
           + ''.join('<button class="fb2 on" data-f="kind:%s">%s</button>' % (k, KINDLAB[k]) for k in KINDS)
           + '</div><div class="cntline" id="cnt"></div>')

BODY = ''.join(grp(l) for l in LAWS)

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>經紀法規｜罰鍰與處分一覽表</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s%s</style></head><body>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規｜罰鍰與處分一覽表</h1><div class="sub">四法共 %d 筆・罰誰・誰罰・罰多少・程序</div></header>
<main>
<div class="intro"><b>這是四個罰則頁共用的資料源。</b>每一筆都標<b>法規全名</b>，不裸寫 §N——
同一個 §17，經紀業條例是「僱用未具資格者 6–30萬」、公寓大廈是「未投保 4–20萬」、
消保法是「定型化契約應記載事項」，三件完全不同的事。金額已逐筆比對全國法規資料庫現行條文。</div>
%s
%s
<p class="foot">本頁為備考整理，非法規原文。資料源 tools/essay_jj/penalty.json，四頁共用。考前以紙本六法為準。</p>
</main>
<script>
(function(){
var off={};
function sync(){
  var n=0;
  [].forEach.call(document.querySelectorAll('.act'),function(a){
    var h=off['law:'+a.dataset.law]||off['kind:'+a.dataset.kind];
    a.hidden=!!h; if(!h)n++;
  });
  [].forEach.call(document.querySelectorAll('.lawgrp'),function(g){
    g.hidden = !g.querySelector('.act:not([hidden])');
  });
  document.getElementById('cnt').textContent='顯示 '+n+' / %d 筆';
}
document.addEventListener('click',function(e){
  var b=e.target.closest('.fb2'); if(!b)return;
  var f=b.dataset.f; off[f]=!off[f]; b.classList.toggle('on',!off[f]); sync();
});
sync();
var tb=document.getElementById('themeBtn');function cur(){return document.documentElement.getAttribute('data-theme')}
function ub(){tb.textContent=cur()==='dark'?'🌙':'☀️'}ub();
tb.onclick=function(){var h=document.documentElement,n=cur()==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}ub()};
})();
</script>
%s
</body></html>''' % (BASECSS, CSS, len(D), FILTERS, BODY, len(D), FAB)

io.open(DST, 'w', encoding='utf-8').write(HTML)
print('已重建 經紀法規_罰鍰與處分一覽表.html', len(HTML) // 1024, 'KB')
print('資料源 tools/essay_jj/penalty.json：%d 筆' % len(D))
print('法規分布：', dict(collections.Counter(r['lawshort'] for r in D)))
print('處分類型：', dict(collections.Counter(r['kind'] for r in D)))
print('金額與條文不符：%d 筆 %s' % (len(bad), bad if bad else ''))
