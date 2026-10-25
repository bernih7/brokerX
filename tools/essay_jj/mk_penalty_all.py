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
import urllib.parse as _up
PENU = _up.quote('經紀法規_公寓大廈條例罰則整理.html')
TOTU = _up.quote('經紀法規_罰則總整理.html')
FCU = _up.quote('經紀法規_公平法消保法罰則整理.html')
CMPU = _up.quote('經紀法規_四法罰則總比較.html')

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


# ── 以「金額」為軸分組：這頁的用途就是反查「某個金額有哪些條文」 ──
def amtkey(r):
    try:
        return (float(r['lo']), float(r['hi']))
    except Exception:
        return None


def amtlab(lo, hi):
    def one(v):
        if v < 1:
            return '%d千' % round(v * 10)
        return '%g萬' % v
    return '%s–%s' % (one(lo), one(hi))


LAWORD = {'條例': 0, '公寓': 1, '公平法': 2, '消保法': 3}
KINDS = ['罰鍰', '停業廢止', '人員處分', '刑責', '賠償']
KINDLAB = {'罰鍰': '罰鍰', '停業廢止': '停業・廢止', '人員處分': '人員處分',
           '刑責': '刑責', '賠償': '損害賠償'}


def artnum(a):
    m = re.match(r'§\s*(\d+)(?:[之\-](\d+))?', a)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else (999, 0)


groups = {}
others = {k: [] for k in KINDS[1:]}
for r in D:
    if r['kind'] == '罰鍰' and amtkey(r):
        groups.setdefault(amtkey(r), []).append(r)
    else:
        others.setdefault(r['kind'], []).append(r)
for g in groups.values():
    g.sort(key=lambda r: (LAWORD.get(r['law'], 9), artnum(r['art'])))

ORDER = sorted(groups, key=lambda k: (k[0], k[1]))

SHORTN = {'條例': '經紀業', '公寓': '公寓大廈', '公平法': '公平法', '消保法': '消保法'}


def qual(r):
    """amt 欄位在級距之外多寫的限定（按戶、並勒令停業…），要顯示出來"""
    lab = amtlab(*amtkey(r))
    a = r['amt'].replace('元', '').replace('萬萬', '萬')
    for cand in (lab, lab.replace('–', '-'), r['amt'].split('，')[0].split('／')[0]):
        if a.startswith(cand.replace('元', '')):
            a = a[len(cand.replace('元', '')):]
            break
    a = a.lstrip('，,／/ ').strip()
    return '<span class="qf">%s</span>' % a if a else ''


def rowhtml(r):
    return ('<tr><td class="c1"><b>%s</b>%s</td><td class="c2">%s%s</td>'
            '<td class="c3">%s</td><td class="c4">%s</td></tr>'
            % (SHORTN[r['law']], r['art'], r['act'], qual(r),
               r['who'], r.get('cond') or '—'))


def table(rows):
    return ('<div class="tw2"><table class="pt"><thead><tr>'
            '<th>法規・條號</th><th>違規行為</th><th>罰誰</th><th>程序</th>'
            '</tr></thead><tbody>%s</tbody></table></div>'
            % ''.join(rowhtml(r) for r in rows))


def gid(k):
    return 'a' + str(k[0]).replace('.', 'p') + '_' + str(k[1]).replace('.', 'p')


# 金額索引：一排可點的金額，點了跳到該組
IDX = '<div class="amtidx">' + ''.join(
    '<a class="ac" href="#%s"><b>%s</b><span>%d</span></a>'
    % (gid(k), amtlab(*k), len(groups[k])) for k in ORDER) + '</div>'

SEC = ''
for k in ORDER:
    rows = groups[k]
    laws = '、'.join(dict.fromkeys(SHORTN[r['law']] for r in rows))
    SEC += ('<section class="ag" id="%s"><h3 class="agh"><span class="av">%s</span>'
            '<span class="an2">%d 筆</span><span class="al2">%s</span></h3>%s</section>'
            % (gid(k), amtlab(*k), len(rows), laws, table(rows)))

OTH = ''
for kind in KINDS[1:]:
    rows = sorted(others.get(kind) or [],
                  key=lambda r: (LAWORD.get(r['law'], 9), artnum(r['art'])))
    if not rows:
        continue
    OTH += ('<section class="ag"><h3 class="agh"><span class="av vk">%s</span>'
            '<span class="an2">%d 筆</span></h3>'
            '<div class="tw2"><table class="pt"><thead><tr><th>法規・條號</th>'
            '<th>情形</th><th>對象</th><th>處分內容</th></tr></thead><tbody>%s'
            '</tbody></table></div></section>'
            % (KINDLAB[kind], len(rows),
               ''.join('<tr><td class="c1"><b>%s</b>%s</td><td class="c2">%s</td>'
                       '<td class="c3">%s</td><td class="c4">%s</td></tr>'
                       % (SHORTN[r['law']], r['art'], r['act'], r['who'], r['amt'])
                       for r in rows)))

JUR = ('<div class="jur"><b>誰罰</b>'
       '<b>經紀業條例</b>：直轄市、縣（市）。管轄依細則——§29 由經紀業所在地為之，'
       '但 §29Ⅰ①②或Ⅱ 且營業處所或行為地不同轄區者由該地為之（細則§25-1）；'
       '§14Ⅲ、§31Ⅱ 由原發證之戶籍所在地（細則§26）；§32Ⅰ 由公司或商號所在地（細則§28-1）。<br>'
       '<b>公寓大廈</b>：直轄市、縣（市）。<b class="ctr">只有 §51（管理維護公司與管理服務人員）歸中央</b>，'
       '這是整章唯一例外。<br>'
       '<b>公平法</b>：一律<b class="ctr">公平交易委員會</b>（中央）；刑責由公平會移送檢察機關。<br>'
       '<b>消保法</b>：罰鍰由直轄市、縣（市）；§51 懲罰性賠償金是<b>法院</b>依請求判決，不是行政罰。</div>')

CSS = """
.purpose{border:1px solid var(--line);border-left:4px solid var(--pri);border-radius:10px;
  background:var(--card);padding:11px 13px;font-size:13.5px;line-height:1.95;color:var(--ink);margin-top:12px}
.purpose b{color:var(--ink)}
.purpose .ph{display:block;width:fit-content;font-size:.74rem;font-weight:700;background:var(--pri);
  color:var(--on);border-radius:99px;padding:2px 9px;margin:0 0 6px}
.purpose ul{margin:6px 0 0;padding-left:1.15em}
.purpose li{margin-top:3px}
.purpose a{color:var(--pri);font-weight:700;text-decoration:none;border-bottom:1px solid currentColor}

.amtidx{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}
.amtidx .ac{display:flex;align-items:baseline;gap:5px;text-decoration:none;
  border:1.5px solid var(--line);background:var(--card);border-radius:99px;padding:5px 11px}
.amtidx .ac b{font-family:"Noto Serif TC",serif;font-size:14px;color:var(--key);font-weight:700}
.amtidx .ac span{font-size:11px;color:var(--muted)}
.amtidx .ac:hover{border-color:var(--key)}

.jur{margin-top:12px;border:1px solid var(--line);border-left:4px solid var(--key);
  border-radius:10px;background:var(--card);padding:10px 13px;font-size:13px;
  line-height:1.95;color:var(--ink)}
.jur>b:first-child{display:block;width:fit-content;font-size:.74rem;font-weight:700;
  background:var(--key);color:#fff;border-radius:99px;padding:2px 9px;margin:0 0 5px}
:root[data-theme="dark"] .jur>b:first-child{color:#161C19}
.jur b{color:var(--ink)}
.ctr{color:var(--red);font-weight:700}

.ag{margin-top:20px;scroll-margin-top:12px}
.agh{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin:0 0 7px;
  padding-bottom:6px;border-bottom:2px solid var(--key)}
.agh .av{font-family:"Noto Serif TC",serif;font-size:19px;font-weight:700;color:var(--key)}
.agh .av.vk{font-size:16.5px;color:var(--pri)}
.agh .an2{font-size:.76rem;color:var(--muted)}
.agh .al2{font-size:.76rem;color:var(--muted);margin-left:auto}

.tw2{overflow-x:auto;border:1px solid var(--line);border-radius:9px;background:var(--card)}
table.pt{border-collapse:collapse;width:100%;min-width:610px;font-size:13px}
table.pt th{text-align:left;font-size:.76rem;font-weight:700;color:var(--muted);
  background:var(--surface2);padding:7px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
table.pt td{padding:8px 10px;border-bottom:1px solid var(--line);line-height:1.75;
  vertical-align:top;color:var(--ink)}
table.pt tr:last-child td{border-bottom:none}
table.pt .c1{white-space:nowrap;width:9.4em}
table.pt .c1 b{color:var(--muted);font-weight:500;font-size:.86em;margin-right:4px}
table.pt .c1{color:var(--key);font-weight:700}
table.pt .c2{min-width:14em}
table.pt .c3{white-space:nowrap;width:8.6em}
table.pt .c4{width:13em;color:var(--sub,var(--muted))}
table.pt .qf{display:inline-block;margin-left:6px;font-size:.78rem;font-weight:700;
  color:var(--red);background:var(--bad-soft,rgba(168,64,43,.1));border-radius:5px;padding:0 6px}

/* 手機：不要橫捲。一列拆兩行——條號＋行為在上，罰誰・程序在下 */
@media(max-width:620px){
  .tw2{overflow-x:visible}
  table.pt{min-width:0;display:block}
  table.pt thead{display:none}
  table.pt tbody,table.pt tr{display:block}
  table.pt tr{padding:9px 11px;border-bottom:1px solid var(--line)}
  table.pt tr:last-child{border-bottom:none}
  table.pt td{display:inline;padding:0;border:none}
  table.pt .c1{width:auto;white-space:nowrap}
  table.pt .c1::after{content:"　"}
  table.pt .c2{min-width:0}
  table.pt .c3,table.pt .c4{width:auto;display:inline;font-size:12.5px;color:var(--muted)}
  table.pt .c3::before{content:"罰誰 ";font-size:.84em}
  table.pt .c4::before{content:"・程序 ";font-size:.84em}
  table.pt .c3{display:block;margin-top:4px}
}
"""

PURPOSE = """<div class="purpose"><b class="ph">這頁拿來做什麼</b>
<b>反查用：先想到金額，再找哪些條文。</b>四法 73 筆依<b>金額級距</b>分組，
上面的索引一排掃過去就知道每個級距各有幾條；點一下跳到那一組，整組一次背完。
<ul>
<li><b>和其他罰則頁的分工</b>——<br>
　<b>這頁</b>：以<b>金額</b>為軸，跨四法。問「6–30萬有哪些」「3–15萬怎麼分」時看這頁。<br>
　<a href="%s">公寓大廈條例罰則整理</a>：以<b>違規行為</b>為軸，單一法規逐條詳解，每條都有罰誰・誰罰・罰多少・程序。<br>
　<a href="%s">罰則總整理</a>：以<b>對象</b>為軸，經紀業（公司）vs 經紀人員（個人）。<br>
　<a href="%s">公平法＋消保法罰則</a>：那兩法的罰鍰、刑責、賠償倍數與時效。<br>
　<a href="%s">四法罰則總比較</a>：同一個行為在四法各怎麼罰。</li>
<li><b>資料源</b>：四頁共用 penalty.json，金額已逐筆比對全國法規資料庫現行條文。</li>
<li><b>條號一律帶法規名</b>——同一個 §17，經紀業條例是「僱用未具資格者 6–30萬」、
公寓大廈是「未投保 4–20萬」、消保法是「定型化契約應記載事項」，三件完全不同的事。</li>
</ul></div>""" % (PENU, TOTU, FCU, CMPU)

HTML = """<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>經紀法規｜罰鍰與處分一覽表</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s%s</style></head><body>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規｜罰鍰與處分一覽表</h1><div class="sub">以金額反查：四法共 %d 筆、%d 個金額級距</div></header>
<main>
%s
%s
%s
%s
%s
<p class="foot">本頁為備考整理，非法規原文。資料源 tools/essay_jj/penalty.json，四個罰則頁共用。考前以紙本六法為準。</p>
</main>
<script>
(function(){
var tb=document.getElementById('themeBtn');function cur(){return document.documentElement.getAttribute('data-theme')}
function ub(){tb.textContent=cur()==='dark'?'🌙':'☀️'}ub();
tb.onclick=function(){var h=document.documentElement,n=cur()==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}ub()};
})();
</script>
%s
</body></html>""" % (BASECSS, CSS, len(D), len(ORDER), PURPOSE, IDX, JUR, SEC, OTH, FAB)

io.open(DST, 'w', encoding='utf-8').write(HTML)
print('已重建 經紀法規_罰鍰與處分一覽表.html', len(HTML) // 1024, 'KB')
print('金額級距 %d 組（最大一組 %d 筆）｜其他處分 %d 筆'
      % (len(ORDER), max(len(v) for v in groups.values()),
         sum(len(v) for v in others.values())))
print('金額與條文不符：%d 筆 %s' % (len(bad), bad if bad else ''))
