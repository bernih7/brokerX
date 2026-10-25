# -*- coding: utf-8 -*-
"""《經紀法規_數字速查》。

經紀法規的數字密度是四科最高，而考題套路就是「同一個數字屬於哪一條」：
3萬–15萬 出現在 8 條、6萬–30萬 一個罰建商一個罰經紀業、15日 出現在 12 條。
單獨背數字必定混，所以這頁反過來建索引：先看數字，再看它屬於誰。

版型沿用罰則頁：一個數字一張卡，卡內一條一行，標籤在左。
資料全部從 tools/essay_jj/law/lawfull.json 逐字抽出後人工標主體。
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
LAW = json.load(io.open(os.path.join(HERE, 'law', 'lawfull.json'), encoding='utf-8'))
DST = os.path.join(ROOT, '經紀法規_數字速查.html')

SRC = io.open(os.path.join(ROOT, '經紀法規_程序總整理.html'), encoding='utf-8').read()
BASECSS = re.search(r'<style>([\s\S]*?)</style>', SRC).group(1)
FAB = SRC[SRC.index('<!--bxfab-->'):SRC.index('<!--/bxfab-->') + len('<!--/bxfab-->')]

# ───────── 金額：同一個級距出現在哪幾條 ─────────
# who＝罰誰（這是最常被調包的一欄）  note＝這一條的辨識點
MONEY = [
    ('6萬–30萬', True, [
        ('經紀業條例 §29Ⅰ①', '經紀業', '違反§7Ⅵ、§11、§17、§19Ⅰ、§21Ⅰ、Ⅱ或§22Ⅰ'),
        ('平均地權條例 §81-2Ⅴ', '<b class="ctr">建商（銷售預售屋者）</b>',
         '契約不符公告之應記載／不得記載事項，<b class="ctr">按戶（棟）</b>計罰'),
    ], '數字一樣，<b>一個罰經紀業、一個罰建商而且按戶棟</b>。114-7 考的就是這個。'),
    ('3萬–15萬', True, [
        ('經紀業條例 §29Ⅰ②', '經紀業',
         '未依限申報登錄，或登錄價格、交易面積不實；<b>按戶（棟）</b>罰，並令限期改正，屆期未改按次；'
         '經處罰二次仍未改正，按次處 30萬–100萬'),
        ('經紀業條例 §29Ⅰ③', '經紀業',
         '未依限報備查、規避妨礙拒絕查核（§24-1Ⅵ）、違反§24-2 → <b>直接罰</b>'),
        ('經紀業條例 §29Ⅰ④', '經紀業',
         '違反§12、§18、§20、§27 → <b class="ctr">應先令限期改正</b>，屆期未改正才罰'),
        ('公寓大廈 §51Ⅰ', '管理維護公司',
         '違反§43；<b class="ctr">中央主管機關</b>先通知限期改正，屆期不改正才處分'),
    ], '經紀業條例裡有三款都是 3萬–15萬，<b>差別在要不要先限期改正</b>：②②③直接罰、④先改正。'
       '再加上公寓大廈§51Ⅰ 是<b class="ctr">中央</b>罰。'),
    ('4萬–20萬', False, [
        ('公寓大廈 §49Ⅰ①～⑧', '住戶／區分所有權人／幹部／起造人', '八款，安全與財產等級'),
        ('公寓大廈 §49-1', '區分所有權人', '<b class="ctr">按每一專有部分</b>計罰'),
        ('公寓大廈 §50', '管理維護公司、管理服務人員', '<b class="ctr">勒令停業</b>並處罰鍰'),
    ], '三條同金額，<b>§49-1 按戶、§50 要先勒令停業</b>，§49 是一般的八款。'),
    ('3千–1.5萬', False, [
        ('公寓大廈 §47①②③', '召集人起造人／住戶／區分所有權人', '生活秩序等級'),
        ('公寓大廈 §51Ⅱ', '受僱之管理服務人員', '<b class="ctr">中央</b>罰；另可停業 3個月–3年'),
        ('公寓大廈 §51Ⅲ', '其他管理服務人員', '<b class="ctr">中央</b>罰；另可停業 <b>6個月</b>–3年'),
    ], '§51Ⅱ 與 Ⅲ 金額一樣，<b>停業下限不同：Ⅱ 是 3 個月、Ⅲ 是 6 個月</b>，上限都 3 年。'),
    ('30萬–100萬', True, [
        ('經紀業條例 §29Ⅰ②後段', '經紀業', '申報登錄不實<b>經處罰二次仍未改正</b>，按次處'),
        ('平均地權條例 §81-2', '建商等', '申報登錄相關之加重級距'),
    ], '這是<b>加重級距</b>，前提都是已經罰過還不改。'),
    ('6千–3萬', True, [
        ('經紀業條例 §29Ⅰ⑥', '經紀業',
         '申報登錄<b>租金、價格及面積以外</b>資訊不實，應先令限期改正，屆期未改才罰'),
        ('平均地權條例 §81-2', '建商等', '對應之較輕級距'),
    ], '經紀業條例裡最輕的一級，而且<b>要先限期改正</b>。'),
    ('1萬–5萬', False, [
        ('經紀業條例 §29Ⅰ⑤', '經紀業', '<b class="ctr">租賃</b>案件未依限申報登錄，或租金、面積不實'),
    ], '這一級只有一條，關鍵字是<b>租賃</b>（§24-1Ⅰ）。買賣是 §29Ⅰ②的 3萬–15萬。'),
    ('1千–5千', False, [
        ('公寓大廈 §48①～④', '管理負責人、主委、管理委員', '幹部失職四款'),
    ], '全章最輕，<b>只罰幹部</b>。'),
    ('10萬–30萬', False, [
        ('經紀業條例 §32Ⅰ', '非經紀業而經營仲介或代銷者',
         '主管機關<b class="ctr">先禁止其營業</b>並處罰鍰；禁止後仍繼續營業，才處 1 年以下有期徒刑'),
    ], '這是<b>無照經營</b>。注意順序：先禁止營業＋罰鍰 → 還不停才有刑責。'),
    ('10萬–5000萬', True, [
        ('公平法 §40Ⅰ', '事業', '違反§9獨占、§15聯合、§19、§20；按次 20萬–1億'),
        ('公平法 §42', '事業', '違反§21不實廣告、§23～§25；<b class="ctr">按次是 10萬–5000萬</b>'),
    ], '<b class="ctr">§42 的本罰是 5萬–2500萬</b>，按次才變 10萬–5000萬；§40 的本罰才是 10萬–5000萬。'
       '另「上一會計年度銷售金額 <b>10%</b>」的上限<b class="ctr">只用於§9、§15 且情節重大</b>（§40Ⅱ）。'),
    ('5萬–50萬', True, [
        ('公平法 §44', '事業', '拒絕§27 調查，或規避妨礙拒絕；得連續處罰'),
        ('消保法 §56-1', '企業經營者', '定型化契約違反§17Ⅰ公告之應記載／不得記載事項，經限期改正屆期不改正'),
    ], '一個在公平法、一個在消保法。<b>消保法§56-1 本身寫「除法律另有處罰規定外」</b>，'
       '所以預售屋契約違規是走平均地權條例§81-2Ⅴ，不是這一條（114-7）。'),
    ('3萬–30萬', True, [
        ('消保法 §56-1', '企業經營者', '前述再經限期改正屆期不改正之加重'),
        ('消保法 §57', '企業經營者', '規避妨礙拒絕主管機關依§33、§38 所為之調查'),
    ], '同在消保法，一個是契約內容違規、一個是<b>妨礙調查</b>。'),
]

# ───────── 期間：同一個天數出現在哪幾條 ─────────
PERIOD = [
    ('30日', [
        ('經紀業條例 §24-1Ⅰ', '仲介：租賃案件自簽訂租賃契約書之日起 30 日內申報登錄'),
        ('經紀業條例 §24-1Ⅱ', '代銷：委託代銷契約簽訂、變更或終止之日起 30 日內報備查；'
                           '買賣契約書簽訂之日起 30 日內申報登錄'),
        ('平均地權條例 §47-3Ⅱ', '預售屋：簽訂或解除買賣契約書之日起 30 日內申報登錄'),
        ('施行細則 §6～§9', '經紀業變更、遷出遷入、分設、裁撤等備查期限'),
    ], '<b>買賣與租賃都是 30 日</b>，不要跟備查的 15 日混。'),
    ('15日', [
        ('施行細則 §5', '經紀業<b>開始營業後</b> 15 日內申請備查'),
        ('平均地權條例 §47-3', '預售屋備查內容<b>變更之日起</b> 15 日內報請變更備查'),
        ('消保法 §19-2Ⅰ', '企業經營者應於收到解約通知之<b class="ctr">次日起</b> 15 日內取回商品'),
        ('消保法 §19-2Ⅱ', '應於取回商品等之<b class="ctr">次日起</b> 15 日內返還對價'),
        ('消保法 §43', '企業經營者對申訴應於<b>申訴之日起</b> 15 日內妥適處理'),
        ('公寓大廈 §34', '區權會會議紀錄作成後 15 日內送達'),
    ], '消保法那三個 15 日，<b class="ctr">兩個是「次日起」、一個是「之日起」</b>——'
       '§19-2 兩項都是次日起，§43 申訴是之日起。110-16 考的就是這個。'),
    ('7日', [
        ('消保法 §19Ⅰ', '通訊交易、訪問交易<b>猶豫期 7 日</b>（收受商品或接受服務後）'),
        ('公寓大廈 §57', '起造人應於管委會成立或管理負責人推選後 <b>7 日</b>內會同檢測並移交'),
        ('公寓大廈 §32Ⅱ', '重新召集之決議，區分所有權人得於 7 日內以書面表示反對'),
        ('公寓大廈 §20', '公告或移交相關期限'),
    ], '消保法的 7 日是<b>消費者的權利</b>，公寓大廈的 7 日是<b>別人的義務</b>。'),
    ('3個月', [
        ('公寓大廈 §22Ⅰ', '促請改善後 <b>3 個月</b>仍未改善，才得訴請強制遷離'),
        ('公寓大廈 §22Ⅱ', '判決確定後 <b>3 個月</b>內不自行出讓，才得聲請拍賣'),
        ('公寓大廈 §28', '起造人應於領得使用執照 <b>3 個月</b>內召集第一次區權會'),
        ('公平法 §15Ⅱ', '主管機關對聯合行為許可申請應於 <b>3 個月</b>內決定，必要時得延長一次'),
        ('公寓大廈 §51Ⅱ', '停止執行業務 <b>3 個月</b>以上 3 年以下'),
    ], '§22 一條裡有<b>兩個 3 個月</b>：促請改善後 3 個月（進法院前）、判決確定後 3 個月（進拍賣前）。'),
    ('4年', [
        ('經紀業條例 §13Ⅲ', '經紀<b>營業員</b>證明有效期限 4 年，期滿檢附 <b>20 小時</b>訓練重新登錄'),
        ('經紀業條例 §15Ⅰ', '經紀<b>人</b>證書有效期限 4 年，期滿檢附 <b>30 小時</b>訓練換證'),
    ], '效期都是 4 年，<b class="ctr">時數不同：營業員重新登錄 20 小時、經紀人換證 30 小時</b>。'
       '初訓是 30 小時（§13Ⅲ）。全場唯一的 20 小時就是營業員重新登錄。'),
    ('1年', [
        ('經紀業條例 §14Ⅰ', '經紀人考試及格後須有 <b>1 年以上</b>營業員經驗才能請領證書'),
        ('經紀業條例 §9Ⅱ', '解散者得自核准註銷營業之日<b>滿 1 年後 2 年內</b>請求退還營業保證金'),
        ('經紀業條例 §29Ⅰ⑦', '停止營業至補足營業保證金為止；<b>停業達 1 年者應廢止許可</b>'),
        ('經紀業條例 §32Ⅰ', '無照經營經禁止後仍營業，處 <b>1 年以下</b>有期徒刑'),
        ('公寓大廈 §25Ⅲ', '召集人任期 1 至 2 年；規約未定者任期 1 年，連選得連任 1 次'),
    ], '營業保證金退還是<b class="ctr">滿 1 年「後」2 年「內」</b>，兩個數字缺一不可。'),
    ('5年', [
        ('公平法 §16Ⅱ', '聯合行為許可期限<b>不得逾 5 年</b>；延展每次不得逾 5 年'),
        ('公平法 §41', '裁處權因 <b>5 年</b>期間經過而消滅'),
        ('經紀業條例 §31Ⅱ', '懲戒相關之 5 年期間'),
        ('說明書 預售屋（四）3', '最近 <b>5 年</b>內基地周邊半徑 <b>300 公尺</b>有無水災淹水救助紀錄'),
    ], '公平法聯合行為許可「不得逾 3 年」是<b class="ctr">舊制</b>，現行是 5 年（112-17 考過）。'),
]

RATIO = [
    ('出席 2/3、同意 3/4', '公寓大廈 §31',
     '區權會決議：出席 <b>2/3</b> 以上及區分所有權比例合計 2/3 以上；'
     '以出席人數 <b>3/4</b> 以上及其區分所有權比例占出席 3/4 以上同意。'
     '<b class="ctr">3/4 是「出席人數」的 3/4，不是全體的 3/4。</b>'),
    ('出席 1/5、過半數同意', '公寓大廈 §32',
     '前條未獲決議時重新召集：區分所有權人 <b>3 人並 1/5</b> 以上及比例合計 1/5 以上出席，'
     '出席過半數且比例過半數同意。會議紀錄送達後各區分所有權人得於 <b>7 日</b>內書面反對；'
     '反對未超過全體半數，決議視為成立。'),
    ('1/5 請求', '公寓大廈 §25Ⅱ②',
     '經區分所有權人 <b>1/5</b> 以上及比例合計 1/5 以上，書面載明目的及理由請求召集臨時會議。'),
    ('2/5 上限', '經紀業條例 §9（基金管理委員會）',
     '營業保證基金管理委員會中<b>由經紀業擔任之委員，不得超過總數 2/5</b>。'),
    ('1/3、1/4 結合門檻', '公平法 §11Ⅰ',
     '因結合使市占率達 <b>1/3</b>，或參與結合之一事業市占率達 <b>1/4</b>，'
     '或上一會計年度銷售金額超過公告金額者，應申報。'),
    ('1% 積欠', '公寓大廈 §22Ⅰ①',
     '積欠應分擔費用經強制執行後<b>再度積欠</b>，金額達區分所有權總價 <b>1%</b>，'
     '得促請改善並訴請強制遷離。'),
    ('10% 銷售額', '公平法 §40Ⅱ',
     '違反<b class="ctr">§9、§15 且情節重大</b>者，得處上一會計年度銷售金額 <b>10%</b> 以下罰鍰。'
     '<b class="ctr">不適用於§19、§20</b>。'),
    ('10 倍報酬', '公平法 §21Ⅴ但書',
     '<b>非屬</b>知名公眾人物、專業人士或機構之薦證者，僅於受廣告主報酬 <b>10 倍</b>範圍內負連帶責任。'),
]

CSS = '''
.nums{display:grid;gap:11px;margin-top:12px}
.num{border:1px solid var(--line);border-left:5px solid var(--c,var(--line));
  border-radius:11px;background:var(--card);padding:11px 13px 12px}
.num.hot{--c:#A8402B}.num.cool{--c:#B8782E}
:root[data-theme="dark"] .num.hot{--c:#E05040}
:root[data-theme="dark"] .num.cool{--c:#E0B070}
@media(prefers-color-scheme:dark){
 :root:not([data-theme="light"]) .num.hot{--c:#E05040}
 :root:not([data-theme="light"]) .num.cool{--c:#E0B070}}
.num .nh{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}
.num .nv{font-family:"Noto Serif TC",serif;font-size:17px;font-weight:700;
  color:var(--key);flex:none}
.num .cnt2{font-size:.76rem;color:var(--muted);flex:none}
.num .warnf{font-size:.74rem;font-weight:700;color:#fff;background:var(--red);
  border-radius:99px;padding:1px 8px;flex:none}
:root[data-theme="dark"] .num .warnf{color:#161C19}
.num .items{margin-top:9px;display:grid;gap:7px}
.num .it{display:grid;grid-template-columns:9.4em 1fr;gap:9px;font-size:13.5px;
  line-height:1.8;align-items:start}
@media(max-width:400px){.num .it{grid-template-columns:1fr}
 .num .it .ar2{border-bottom:1px solid var(--line);padding-bottom:2px}}
.num .it .ar2{font-weight:700;color:var(--key);font-size:.88rem}
.num .it .who2{color:var(--ink);font-weight:700;display:block}
.num .it .d2{color:var(--muted);display:block;font-size:.92em;margin-top:1px}
.num .it b{color:var(--ink)}
.num .it .ctr{color:var(--red)}
.num .tip{margin-top:9px;padding:7px 10px;border-radius:8px;background:var(--bg);
  border:1px solid var(--line);border-left:4px solid var(--red);font-size:13px;
  line-height:1.85;color:var(--ink)}
.num .tip b{color:var(--ink)}.num .tip .ctr{color:var(--red)}
.ctr{color:var(--red);font-weight:700}
'''

S = []


def sec(sid, title, cnt, body, open_=False):
    S.append('<details class="sec" id="%s" style="--a:var(--cE)"%s><summary><h2>%s</h2>'
             '<span class="cnt">%s</span></summary><div class="bd">\n%s\n</div></details>'
             % (sid, ' open' if open_ else '', title, cnt, body))


def mcard(v, hot, rows, tip):
    its = ''.join(
        '<div class="it"><div class="ar2">%s</div><div><span class="who2">%s</span>'
        '<span class="d2">%s</span></div></div>' % (a, w, d) for a, w, d in rows)
    flag = '<span class="warnf">跨法規</span>' if hot else ''
    n = len(rows)
    return ('<div class="num %s"><div class="nh"><span class="nv">%s</span>'
            '<span class="cnt2">%d 條</span>%s</div>'
            '<div class="items">%s</div><div class="tip">%s</div></div>'
            % ('hot' if n >= 3 or hot else 'cool', v, n, flag, its, tip))


def pcard(v, rows, tip):
    its = ''.join(
        '<div class="it"><div class="ar2">%s</div><div><span class="who2">%s</span></div></div>'
        % (a, d) for a, d in rows)
    return ('<div class="num %s"><div class="nh"><span class="nv">%s</span>'
            '<span class="cnt2">%d 條</span></div>'
            '<div class="items">%s</div><div class="tip">%s</div></div>'
            % ('hot' if len(rows) >= 4 else 'cool', v, len(rows), its, tip))


sec('n1', '① 罰鍰金額：同一個數字屬於誰', '%d 組' % len(MONEY),
    '<div class="nums">%s</div>' % ''.join(mcard(*m) for m in MONEY), open_=True)

sec('n2', '② 期間：同一個天數出現在哪幾條', '%d 組' % len(PERIOD),
    '<div class="nums">%s</div>' % ''.join(pcard(*p) for p in PERIOD), open_=True)

sec('n3', '③ 比例與門檻', '%d 組' % len(RATIO),
    '<div class="nums">%s</div>' % ''.join(
        '<div class="num cool"><div class="nh"><span class="nv">%s</span>'
        '<span class="cnt2">%s</span></div><div class="tip" style="margin-top:8px">%s</div></div>'
        % (v, a, d) for v, a, d in RATIO))

BODY = '\n\n'.join(S)
NAV = '<nav><a href="#n1">① 罰鍰金額</a><a href="#n2">② 期間</a><a href="#n3">③ 比例門檻</a></nav>'

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>經紀法規｜數字速查</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s%s</style></head><body>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規｜數字速查</h1><div class="sub">先看數字，再看它屬於誰</div></header>
%s
<main>
<div class="intro"><b>為什麼要反過來查：</b>經紀法規的罰鍰級距有 <b>10 組是跨條重複</b>的——3萬–15萬出現在 <b>4 條</b>、6萬–30萬一個罰經紀業一個罰建商、15日出現在 <b>6 條</b>。單獨背數字一定會混，差別全在<b>主體</b>與<b>前提</b>。這頁每張卡先給數字，再列出它屬於哪幾條、各罰誰。<b class="ctr">跨法規</b>標記的最容易錯。</div>
<div class="tools"><button id="ea">全部展開</button><button id="ca">全部收合</button></div>

%s

<p class="foot">本頁為備考整理，非法規原文。金額、期間、比例皆逐字取自站內條文庫（全國法規資料庫現行條文）。考前以紙本六法為準。</p>
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
</body></html>''' % (BASECSS, CSS, NAV, BODY, FAB)

io.open(DST, 'w', encoding='utf-8').write(HTML)
print('已產生 經紀法規_數字速查.html', len(HTML) // 1024, 'KB')
print('金額 %d 組｜期間 %d 組｜比例 %d 組'
      % (len(MONEY), len(PERIOD), len(RATIO)))
