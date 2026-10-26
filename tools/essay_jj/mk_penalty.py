# -*- coding: utf-8 -*-
"""重建《經紀法規_公寓大廈條例罰則整理》。

使用者三輪回饋：①沒有邏輯、重點沒抓到 ②色彩混雜看不清楚什麼是重點
③罰誰／誰罰／罰多少沒想清楚 ④灰色一堆、要換行但不要太長 ⑤整體要好辨識。

做法：不用表格、不用段落。**一個違規行為一張卡**，卡內固定四列
「罰誰／誰罰／罰多少／程序」，標籤在左、內容在右，一列一行，不會有長段。
顏色只用在金額膠囊與左側級距色條，其餘一律墨色。

條文全部取自 tools/essay_jj/law/lawfull.json 逐字。考古題深連結沿用舊頁。
產生正式頁：python3 tools/essay_jj/mk_penalty.py
產生 demo ：python3 tools/essay_jj/mk_penalty.py --demo
"""
import html as H
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
LAW = json.load(io.open(os.path.join(HERE, 'law', 'lawfull.json'), encoding='utf-8'))
DEMO = '--demo' in sys.argv
DST = os.path.join(ROOT, 'demo', '經紀法規_公寓大廈罰則_demo.html') if DEMO \
    else os.path.join(ROOT, '經紀法規_公寓大廈條例罰則整理.html')
QUIZ = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html'
HUB = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'

# 借用《程序總整理》的樣式骨架與 FAB
SRC = io.open(os.path.join(ROOT, '經紀法規_程序總整理.html'), encoding='utf-8').read()
BASECSS = re.search(r'<style>([\s\S]*?)</style>', SRC).group(1)
FAB = SRC[SRC.index('<!--bxfab-->'):SRC.index('<!--/bxfab-->') + len('<!--/bxfab-->')]

# ───────────────────────── 資料：一個違規行為一筆 ─────────────────────────
# tier: 金額級距（決定左側色條與膠囊）  who 罰誰 / org 誰罰 / amt 罰多少 / proc 程序
LV = {
    'a': ('1千–5千', '§48'),
    'b': ('3千–1.5萬', '§47'),
    'c': ('3萬–15萬', '§51Ⅰ'),
    'd': ('4萬–20萬', '§49'),
}
LOCAL = '直轄市、縣（市）'
CENTRAL = '<b class="ctr">中央主管機關</b>'
P_FIX = '得令限期改善或履行<br>屆期不改，<b>得連續處罰</b>'

ACTS = [
    # ── §48：1千–5千 ──
    dict(t='a', art='§48①', name='沒督促住戶投保責任保險',
         base='違反 §17（住戶應投保公共意外責任保險）之督促義務',
         who='管理負責人、主委、管理委員', org=LOCAL, proc=P_FIX),
    dict(t='a', art='§48②', name='不執行 §22 的促請改善或訴請遷離、出讓',
         base='無正當理由不做 §22 的職務', who='管理負責人、主委、管理委員',
         org=LOCAL, proc=P_FIX, note='要件是<b>無正當理由</b>，有正當理由不罰'),
    dict(t='a', art='§48③', name='拒絕利害關係人閱覽、影印',
         base='無正當理由違反 §35', who='管理負責人、主委、管理委員',
         org=LOCAL, proc=P_FIX),
    dict(t='a', art='§48④', name='不執行 §36①、⑤～⑫ 的職務',
         base='無正當理由不執行，<b>且顯然影響住戶權益</b>',
         who='管理負責人、主委、管理委員', org=LOCAL, proc=P_FIX,
         note='多一道門檻：<b>顯然影響住戶權益</b>才罰'),
    # ── §47：3千–1.5萬 ──
    dict(t='b', art='§47①', name='該開的會沒開、該召集的沒召集',
         base='違反 §25（區權會召集）或 §28（起造人三個月內召集）',
         who='召集人、起造人、臨時召集人', org=LOCAL, proc=P_FIX,
         exams=['99-30', '113-7'], exnote='113-7 考 §28 起造人三個月內召集，不是罰鍰題'),
    dict(t='b', art='§47②', name='亂丟垃圾、污染惡臭、喧囂振動；養動物妨礙公衛安寧',
         base='住戶違反 <b class="ctr">§16Ⅰ</b> 或 <b class="ctr">§16Ⅳ</b>',
         who='住戶', org=LOCAL, proc=P_FIX,
         note='§16 一條拆兩階，<b>Ⅰ、Ⅳ 在這裡</b>；Ⅱ、Ⅲ 在 §49Ⅰ④，貴一個數量級'),
    dict(t='b', art='§47③', name='違反相鄰義務',
         base='區分所有權人或住戶違反 §6',
         who='區分所有權人、住戶', org=LOCAL,
         proc='<b>先經主管機關受理請求</b><br>通知限期改善，屆期不改才罰',
         note='這一款<b>不是直接開罰</b>，要先有人請求、先通知限期改善'),
    # ── §49：4萬–20萬 ──
    dict(t='d', art='§49Ⅰ①', name='專有部分的利用違反 §5',
         base='妨害建築物正常使用、違反區分所有權人共同利益',
         who='區分所有權人', org=LOCAL, proc=P_FIX, exams=['102-20']),
    dict(t='d', art='§49Ⅰ②', name='變更使用限制，經制止還不聽',
         base='違反 §8Ⅰ（外牆、樓頂平臺等）或 §9Ⅱ（共用部分使用）',
         who='住戶', org=LOCAL, proc=P_FIX,
         note='這一款要<b class="ctr">經制止而不遵從</b>才罰，單純違反不夠',
         exams=['99-24', '110-2']),
    dict(t='d', art='§49Ⅰ③', name='擅自變更專有或約定專用的使用',
         base='違反 §15Ⅰ', who='住戶', org=LOCAL, proc=P_FIX),
    dict(t='d', art='§49Ⅰ④', name='逃生通道堆雜物、營業使用、違規廣告、私設路障；破壞主要構造',
         base='住戶違反 <b class="ctr">§16Ⅱ</b> 或 <b class="ctr">§16Ⅲ</b>',
         who='住戶', org=LOCAL, proc=P_FIX,
         note='和 §47② 的差別：<b>Ⅰ、Ⅳ 是吵到人髒到人；Ⅱ、Ⅲ 是逃不出去、房子會垮</b>',
         exams=['106-34']),
    dict(t='d', art='§49Ⅰ⑤', name='沒投保責任保險',
         base='住戶違反 §17', who='住戶', org=LOCAL, proc=P_FIX,
         note='同一件事兩個對象：<b>住戶沒投保</b>罰 4萬–20萬；'
              '<b>幹部沒督促</b>只罰 1千–5千（§48①）'),
    dict(t='d', art='§49Ⅰ⑥', name='沒繳公共基金',
         base='區分所有權人違反 §18Ⅰ②（未依區權會決議繳納）',
         who='區分所有權人', org=LOCAL, proc=P_FIX,
         exams=['100-8', '101-16', '105-38']),
    dict(t='d', art='§49Ⅰ⑦', name='卸任不公告、不移交',
         base='違反 §20 的公告或移交義務',
         who='管理負責人、主委、管理委員', org=LOCAL, proc=P_FIX,
         note='移交是 §49 等級，<b>不是 §48 的 1千–5千</b>。另 §29Ⅳ：拒絕移交者，'
              '自任期屆滿日起視同解任'),
    dict(t='d', art='§49Ⅰ⑧', name='起造人、建築業者違反 §57、§58',
         base='§57 七日內會同檢測並移交／§58 未領建造執照不得銷售、不得讓售共用部分',
         who='起造人、建築業者', org=LOCAL, proc=P_FIX,
         exams=['104-29', '105-34', '110-1', '112-11'],
         exnote='這四題考的是起造人義務本身，不是罰鍰'),
    dict(t='d', art='§49-1', name='逾期沒成立管委會、沒推管理負責人',
         base='未依 §29-1Ⅰ 期限內成立並辦理報備',
         who='區分所有權人', org=LOCAL,
         amt='<b class="ctr">按每一專有部分</b>處 4萬–20萬',
         proc='令限期辦理<br>屆期仍未辦理，<b>得按次處罰</b>',
         note='全章<b>唯一按戶計罰</b>的一條。40 戶就是罰 40 次，不是整棟一次'),
    dict(t='d', art='§50', name='無證營業，或被廢止後還在做',
         base='管理維護公司或管理服務人員違反 §42',
         who='管理維護公司、管理服務人員', org=LOCAL,
         amt='<b class="ctr">勒令停業或停止執行業務</b>，<b>並</b>處 4萬–20萬',
         proc='拒不遵從，<b>得按次連續處罰</b>',
         note='全章<b>唯一有勒令停業</b>的一條。只寫罰鍰會漏掉一半'),
    # ── §51：中央管 ──
    dict(t='c', art='§51Ⅰ', name='管理維護公司違反 §43',
         base='§43：公司應依規定僱用服務人員並負管理責任',
         who='管理維護公司', org=CENTRAL,
         amt='3萬–15萬，或停業、廢止許可或登記證',
         proc='<b class="ctr">先通知限期改正</b><br>屆期不改正才處分',
         note='未依規定申領登記證者，<b>中央主管機關應廢止其許可</b>'),
    dict(t='b', art='§51Ⅱ', name='受僱於管理維護公司的服務人員違反 §44',
         base='§44：受僱服務人員之執業規範',
         who='受僱之管理服務人員', org=CENTRAL,
         amt='廢止認可證／停止執業 <b>3 個月–3 年</b>／3千–1.5萬',
         proc='<b class="ctr">先通知限期改正</b><br>屆期不改正才處分'),
    dict(t='b', art='§51Ⅲ', name='其他管理服務人員違反 §45',
         base='§45：前項以外之管理服務人員執業規範',
         who='其他管理服務人員', org=CENTRAL,
         amt='廢止認可證／停止執業 <b>6 個月–3 年</b>／3千–1.5萬',
         proc='<b class="ctr">先通知限期改正</b><br>屆期不改正才處分',
         note='停業期間與 Ⅱ 不同：<b>Ⅱ 是 3 個月起、Ⅲ 是 6 個月起</b>，上限都是 3 年'),
]

ONLY = [
    ('唯一歸中央的', '§51', '三項都是中央主管機關。其餘 §47、§48、§49、§49-1、§50 全部是直轄市、縣（市）。'),
    ('唯一按戶計罰的', '§49-1', '按每一專有部分處區分所有權人 4萬–20萬。'),
    ('唯一勒令停業的', '§50', '勒令停業或停止執行業務，並處 4萬–20萬。'),
    ('唯一有刑責的', '§49Ⅱ', '限<b>有供營業使用事實</b>之住戶，且有 §49Ⅰ③ 或 ④ 之行為。'),
]


def ex(a):
    """考古題連結列"""
    ks = a.get('exams')
    if not ks:
        return ''
    links = '、'.join('<a href="%s#q=%s">%s</a>' % (QUIZ, k, k) for k in ks)
    tail = '<br><span class="exn">%s</span>' % a['exnote'] if a.get('exnote') else ''
    more = ('　<a class="go" href="%s#q=%s">練這 %d 題 ▸</a>'
            % (QUIZ, ','.join(ks), len(ks)))
    return '<div class="row ex"><span class="k">考古題</span><span class="v">%s%s%s</span></div>' \
           % (links, more, tail)


def card(a):
    amt = a.get('amt') or LV[a['t']][0]
    note = '<div class="nt">%s</div>' % a['note'] if a.get('note') else ''
    return (
        '<article class="act t%s">'
        '<div class="hd"><span class="ar">%s</span><h3>%s</h3></div>'
        '<div class="base">%s</div>'
        '<div class="rows">'
        '<div class="row"><span class="k">罰誰</span><span class="v">%s</span></div>'
        '<div class="row"><span class="k">誰罰</span><span class="v">%s</span></div>'
        '<div class="row"><span class="k">罰多少</span><span class="v amtv">%s</span></div>'
        '<div class="row"><span class="k">程序</span><span class="v">%s</span></div>'
        '%s</div>%s</article>'
        % (a['t'], a['art'], a['name'], a['base'],
           a['who'], a['org'], amt, a['proc'], ex(a), note))


def bt(key, star=''):
    v = LAW[key]
    art = key.split(' ', 1)[1]
    ps = ''.join('<p>%s</p>' % p for p in v['text'].split('\n') if p.strip())
    return ('<details class="bt"><summary><b class="bn">%s</b><span class="bti">%s</span>'
            '<span class="bm">%s</span></summary><div class="btx">%s</div></details>'
            % (art, v.get('title') or key, star, ps))


CSS = '''
/* ── 罰則卡：一個行為一張，四列固定欄位 ── */
.lvbar{display:grid;gap:7px;margin-top:10px}
.lvb{display:grid;grid-template-columns:7.2em 1fr;gap:10px;align-items:center;
  border:1px solid var(--line);border-left:5px solid var(--c);border-radius:9px;
  padding:8px 11px;background:var(--card);font-size:13.5px;line-height:1.75}
.lvb .m{font-weight:700;color:var(--key);background:var(--warn);border-radius:6px;
  padding:3px 6px;text-align:center;font-size:.86rem;white-space:nowrap}
.lvb .d b{color:var(--ink)}
.lvb .d small{display:block;color:var(--muted);font-size:.8rem;margin-top:1px}

.acts{display:grid;gap:11px;margin-top:12px}
.act{border:1px solid var(--line);border-left:5px solid var(--c);border-radius:11px;
  background:var(--card);padding:11px 13px 12px}
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
.act .ar{font-weight:700;color:var(--key);font-size:.92rem;flex:none}
.act h3{font-family:"Noto Serif TC",serif;font-size:15px;color:var(--ink);
  flex:1;min-width:0;line-height:1.55;margin:0;font-weight:700}
.act .amtv{font-weight:700}
.act .amtv::first-line{line-height:1.8}
.act .row .v.amtv{color:var(--key)}
.act .base{margin-top:5px;font-size:13px;color:var(--muted);line-height:1.8}
.act .rows{margin-top:9px;display:grid;gap:5px}
.act .row{display:grid;grid-template-columns:3.6em 1fr;gap:9px;
  font-size:13.5px;line-height:1.8;align-items:start}
.act .row .k{color:var(--muted);font-size:.8rem;font-weight:700;
  padding-top:2px;letter-spacing:.04em}
.act .row .v{color:var(--ink);min-width:0}
.act .row.ex .v a{color:var(--pri);font-weight:700;text-decoration:none;
  border-bottom:1px solid currentColor}
.act .row.ex .v a.go{border:1px solid var(--pri);border-radius:99px;
  padding:1px 9px;font-size:.8rem;white-space:nowrap;display:inline-block;margin-top:3px}
.act .row.ex .exn{color:var(--muted);font-size:.8rem}
.act .nt{margin-top:9px;padding:7px 10px;border-radius:8px;background:var(--bg);
  border:1px solid var(--line);border-left:4px solid var(--red);
  font-size:13px;line-height:1.85;color:var(--ink)}
.act .nt b{color:var(--ink)}
.act .nt .ctr{color:var(--red)}
.ctr{color:var(--red);font-weight:700}

.onlys{display:grid;gap:8px;margin-top:10px}
.only1{display:grid;grid-template-columns:7.4em 1fr;gap:10px;align-items:start;
  border:1px solid var(--line);border-left:4px solid var(--red);border-radius:9px;
  padding:9px 11px;background:var(--card);font-size:13.5px;line-height:1.85}
.only1 .w{font-weight:700;color:var(--red);font-size:.84rem}
.only1 .a{font-weight:700;color:var(--key)}

.bt{margin-top:8px;border:1px solid var(--line);border-radius:9px;background:var(--bg)}
.bt>summary{padding:7px 11px;font-size:.86rem;cursor:pointer;display:flex;gap:8px;
  flex-wrap:wrap;align-items:center}
.bt .bn{color:var(--key);font-weight:700;flex:none}
.bt .bti{color:var(--ink);font-weight:500;flex:1;min-width:0}
.bt .bm{font-size:.74rem;color:var(--muted);flex:none}
.btx{padding:0 11px 9px;font-size:.86rem;line-height:1.85}
.btx p{margin:3px 0}
.q30{display:grid;gap:7px;margin-top:10px}
.q30 div{border:1px solid var(--line);border-radius:9px;padding:9px 12px;
  background:var(--card);font-size:13.5px;line-height:1.85;color:var(--ink)}
.q30 b{color:var(--key)}
'''

S = []


def sec(sid, title, cnt, body, open_=False):
    S.append('<details class="sec" id="%s" style="--a:var(--cE)"%s><summary><h2>%s</h2>'
             '<span class="cnt">%s</span></summary><div class="bd">\n%s\n</div></details>'
             % (sid, ' open' if open_ else '', title, cnt, body))


# ⓪ 四級金額 + 誰罰
lvrows = ''.join(
    '<div class="lvb" style="--c:%s"><div class="m">%s</div><div class="d"><b>%s</b>'
    '<small>%s</small></div></div>' % (c, m, d, s2)
    for c, m, d, s2 in [
        ('#7A8B72', '1千–5千', '幹部失職（§48）', '該做沒做，還沒造成外部危害。只罰管理負責人、主委、管理委員'),
        ('#B8782E', '3千–1.5萬', '生活秩序（§47）', '會議沒開、鄰里公害。另 §51Ⅱ、Ⅲ 的服務人員也是這一級'),
        ('#8A5517', '3萬–15萬', '管理維護公司（§51Ⅰ）', '這一級<b>只有一條</b>，而且是中央主管機關罰'),
        ('#A8402B', '4萬–20萬', '安全與財產（§49、§49-1、§50）', '動到建物、動到錢、動到別人的權利'),
    ])
sec('p0', '⓪ 四級金額：看闖的禍，不是看身分', '先看這個', '''
<div class="lvbar">%s</div>
<div class="mn"><b>為什麼看性質不看身分</b>
<span class="mnw">同一個主委：沒督促投保 1千–5千（§48①）；卸任不移交 4萬–20萬（§49Ⅰ⑦）。</span>
<span class="mnw">同一個住戶：亂丟垃圾 3千–1.5萬（§47②）；逃生通道堆雜物 4萬–20萬（§49Ⅰ④）。</span>
<span class="mnq">身分一樣，金額差幾十倍——差在闖的禍。</span></div>
<div class="tr"><b>誰罰</b>除了 <b class="ctr">§51 是中央主管機關</b>，其餘全部是直轄市、縣（市）主管機關。
<span class="mnq">整章只要記這一個例外。</span></div>
''' % lvrows, open_=True)

# ① 行為卡
sec('p1', '① 一個行為一張卡：罰誰・誰罰・罰多少・程序', '%d 個行為' % len(ACTS),
    '<div class="acts">%s</div>' % ''.join(card(a) for a in ACTS), open_=True)

# ② 四個唯一
sec('p2', '② 四個「唯一」', '考前十秒掃一遍',
    '<div class="onlys">%s</div>' % ''.join(
        '<div class="only1"><div class="w">%s</div><div><span class="a">%s</span>　%s</div></div>'
        % (w, a, d) for w, a, d in ONLY)
    + '<div class="mn"><b>口訣</b><span class="tag" style="font-size:.74rem;color:var(--muted)">自編</span>'
      '<span class="mnq">中央只管 51<br>按戶只有 49-1<br>停業只有 50<br>坐牢只有 49 第 2 項</span></div>'
    + '<div class="tr"><b>§49Ⅱ 刑責</b>'
      '<div class="q30" style="margin-top:7px">'
      '<div><b>致人於死</b>　1 年以上 7 年以下有期徒刑，得併科 100萬–500萬罰金</div>'
      '<div><b>致重傷</b>　6 個月以上 5 年以下有期徒刑，得併科 50萬–250萬罰金</div>'
      '</div></div>')

# ③ §22 強制遷離與出讓
sec('p3', '③ §22 強制遷離與強制出讓', '考古 5 題', '''
<div class="q30">
<div><b>一、誰可以發動</b>　<b>管理負責人或管理委員會</b>促請改善——不是主管機關</div>
<div><b>二、三個月</b>　促請改善後 <b>3 個月內仍未改善</b>，才進下一步</div>
<div><b>三、要先開會</b>　依<b>區分所有權人會議之決議</b>，訴請法院強制遷離</div>
<div><b>四、住戶是區分所有權人時</b>　得訴請法院命其<b>出讓</b>區分所有權及基地應有部分</div>
<div><b>五、判決確定後 3 個月</b>　不自行出讓並完成移轉登記，管委會得<b>聲請法院拍賣</b></div>
<div><b>六、拍賣所得</b>　積欠的應分擔費用，受償順序<b class="ctr">與第一順位抵押權同</b></div>
<div><b>七、幹部不做會怎樣</b>　無正當理由不執行 §22 職務 → <b>§48② 罰 1千–5千</b></div>
</div>
<div class="tr"><b>三款發動事由</b>
<div class="q30" style="margin-top:7px">
<div>① 積欠應分擔費用，<b>經強制執行後再度積欠</b>，金額達區分所有權總價 <b class="ctr">1%</b></div>
<div>② 違反本條例經依 <b>§49Ⅰ①～④</b> 處罰鍰後，仍不改善或續犯</div>
<div>③ 其他違反法令或規約<b>情節重大</b></div>
</div>
<span class="mnw">兩個 3 個月要分清楚：<b>促請改善後 3 個月</b>（進法院前）、<b>判決確定後 3 個月</b>（進拍賣前）。</span></div>
<div class="row ex" style="margin-top:10px;font-size:13.5px">考古題　''' +
    '、'.join('<a href="%s#q=%s" style="color:var(--pri);font-weight:700">%s</a>' % (QUIZ, k, k)
              for k in ['99-27', '100-10', '103-19', '105-37', '110-6']) +
    '　<a class="go" href="%s#q=99-27,100-10,103-19,105-37,110-6" '
    'style="border:1px solid var(--pri);border-radius:99px;padding:1px 9px;'
    'color:var(--pri);text-decoration:none;font-weight:700">練這 5 題 ▸</a></div>' % QUIZ)

# ④ 檢舉與不繳
sec('p4', '④ 檢舉、調處與罰鍰不繳', '§59、§59-1、§52', '''
<div class="q30">
<div><b>§59 誰可以檢舉</b>　他區分所有權人、利害關係人、管理負責人或管理委員會，
<b class="ctr">列舉事實並提出證據</b>，報直轄市、縣（市）主管機關處理</div>
<div><b>§59-1 爭議調處</b>　直轄市、縣（市）政府為處理公寓大廈爭議事件，
<b>得聘請資深之專家、學者及建築師、律師，並指定公寓大廈及建築管理主管人員</b>，
組設<b class="ctr">公寓大廈爭議事件調處委員會</b>；該委員會之組織由<b class="ctr">內政部</b>定之</div>
<div><b>§52 不繳怎麼辦</b>　經限期繳納屆期仍不繳納者，<b class="ctr">依法移送強制執行</b></div>
</div>
<div class="tr"><b>三條容易混</b>
<ul class="kl" style="margin-top:7px">
<li><span>§59</span><div>對<b>主管機關</b>檢舉違規 → 走<b>行政罰</b>（§47～§49）</div></li>
<li><span>§59-1</span><div>向<b>縣市政府的調處委員會</b>聲請 → 走<b>爭議調處</b>，不是罰</div></li>
<li><span>§22</span><div>由<b>管委會</b>促請改善、訴請法院 → 走<b>強制遷離、出讓、拍賣</b></div></li>
</ul>
<span class="mnq">同一件惡鄰糾紛，三條路可以並行：檢舉求罰、聲請調處、訴請趕人。</span>
<span class="mnw">組設調處委員會的是<b>縣市政府</b>，訂組織的是<b>內政部</b>，兩個主體不要混。</span></div>
''' + '<div class="lawwrap"><div class="group-label">逐字全文</div>' + bt('公寓大廈 §59') + bt('公寓大廈 §59之1') + bt('公寓大廈 §52') + '</div>')

# ⑤ 逐字條文
sec('p5', '⑤ 逐字條文', '對紙本用',
    '<div class="lawwrap">' + ''.join(
        bt('公寓大廈 ' + a, s2) for a, s2 in [
            ('§47', '★★★'), ('§48', '★★'), ('§49', '★★★'),
            ('§49之1', '★★'), ('§50', '★★'), ('§51', '★★★　唯一歸中央'),
            ('§22', '★★★'), ('§52', ''), ('§59', '')]) + '</div>')

BODY = '\n\n'.join(S)
NAV = ('<nav><a href="#p0">⓪ 四級金額</a><a href="#p1">① 行為卡</a>'
       '<a href="#p2">② 四個唯一</a><a href="#p3">③ §22 遷離出讓</a>'
       '<a href="#p4">④ 檢舉・調處・不繳</a><a href="#p5">⑤ 逐字條文</a></nav>')

MNCSS = '''
.mn,.tr{background:var(--card);border:1px solid var(--line);border-radius:9px;
  padding:10px 13px 11px;margin-top:11px;font-size:14px;line-height:1.95;color:var(--ink)}
.mn{border-left:5px solid var(--green)}
.tr{border-left:5px solid var(--red)}
.mn>b:first-child,.tr>b:first-child{display:inline-block;font-size:.76rem;font-weight:700;
  letter-spacing:.04em;padding:2px 9px;border-radius:99px;margin:0 7px 5px 0;vertical-align:1px}
.mn>b:first-child{background:var(--green);color:#fff}
.tr>b:first-child{background:var(--red);color:#fff}
:root[data-theme="dark"] .mn>b:first-child,:root[data-theme="dark"] .tr>b:first-child{color:#10201B}
.mn b,.tr b{color:var(--ink)}
.mn .ctr,.tr .ctr{color:var(--red)}
.mnq{display:block;margin-top:6px;font-family:"Noto Serif TC",serif;font-size:15.5px;
  font-weight:700;color:var(--ink);letter-spacing:.02em;line-height:2}
.mnw{display:block;margin-top:5px;font-size:13.5px;color:var(--muted)}
'''

BANNER = ('<div style="position:sticky;top:0;z-index:99;background:#8A5517;color:#fff;'
          'padding:7px 12px;font-size:13px;line-height:1.6">〔<b>demo</b>〕正式頁未動。</div>'
          ) if DEMO else ''

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>%s公寓大廈條例罰則</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s%s%s</style></head><body>
%s<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規｜公寓大廈條例罰則</h1><div class="sub">罰誰・誰罰・罰多少・程序　§22、§47～§52、§49-1、§59、§59-1</div></header>
%s
<main>
<div class="intro"><b>這頁只回答四件事：</b>這個人是<b>誰</b>、哪個機關<b>罰</b>、哪一<b>級金額</b>、要不要<b>先限期改善</b>。金額看闖的禍有多大，不是看身分；主管機關只有 <b>§51</b> 一個例外。</div>
<div class="tools"><button id="ea">全部展開</button><button id="ca">全部收合</button></div>

%s

<p class="foot">本頁為備考整理，非法規原文。條文逐字取自全國法規資料庫現行公寓大廈管理條例。考前以紙本六法為準。</p>
</main>
<script>
(function(){
document.getElementById('ea').onclick=function(){document.querySelectorAll('details').forEach(function(x){x.open=true})};
document.getElementById('ca').onclick=function(){document.querySelectorAll('details').forEach(function(x){x.open=false})};
var tb=document.getElementById('themeBtn');function cur(){return document.documentElement.getAttribute('data-theme')}
function ub(){tb.textContent=cur()==='dark'?'🌙':'☀️'}ub();
tb.onclick=function(){var h=document.documentElement,n=cur()==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}ub()};
function op(id){var d=id&&document.getElementById(id);if(d&&d.tagName==='DETAILS'){d.open=true;setTimeout(function(){d.scrollIntoView({behavior:'smooth',block:'start'})},40)}}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('nav a');if(a&&a.getAttribute('href').charAt(0)==='#'){e.preventDefault();op(a.getAttribute('href').slice(1))}});
if(location.hash)op(location.hash.slice(1));
})();
</script>
%s
</body></html>''' % ('〔demo〕' if DEMO else '', BASECSS, CSS, MNCSS, BANNER, NAV, BODY, FAB)

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, 'w', encoding='utf-8').write(HTML)
print('已產生', os.path.relpath(DST, ROOT), len(HTML) // 1024, 'KB')
print('行為卡 %d 張｜考古題深連結 %d 個'
      % (len(ACTS), len(re.findall(r'#q=', HTML))))
