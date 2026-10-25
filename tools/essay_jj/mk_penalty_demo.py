# -*- coding: utf-8 -*-
"""《公寓大廈條例罰則》重做 demo。
軸線只有一條：**罰誰 → 誰罰 → 罰多少 → 程序**。
色彩只用站內規範四色：關鍵詞紅粗體、金額金底、口訣綠底、陷阱紅底，條號棕粗體。
條文全部取自 tools/essay_jj/law/lawfull.json 逐字。
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
LAW = json.load(io.open(os.path.join(HERE, 'law', 'lawfull.json'), encoding='utf-8'))
SRC = io.open(os.path.join(ROOT, '經紀法規_程序總整理.html'), encoding='utf-8').read()
CSS = re.search(r'<style>([\s\S]*?)</style>', SRC).group(1)
FAB = SRC[SRC.index('<!--bxfab-->'):SRC.index('<!--/bxfab-->') + len('<!--/bxfab-->')]
HUB = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'


def bt(key, star=''):
    v = LAW[key]
    art = key.split(' ', 1)[1]
    ps = ''.join('<p>%s</p>' % p for p in v['text'].split('\n') if p.strip())
    return ('<details class="bt"><summary><b class="bn">%s</b><span class="bti">%s</span>'
            '<span class="bm">%s</span></summary><div class="btx">%s</div></details>'
            % (art, v.get('title') or key, star, ps))


EXTRA = '''
.bt{margin-top:8px;border:1px solid var(--line);border-radius:9px;background:var(--bg)}
.bt>summary{padding:7px 11px;font-size:.86rem;cursor:pointer;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bt .bn{color:var(--key);font-weight:700;flex:none}
.bt .bti{color:var(--ink);font-weight:500;flex:1;min-width:0}
.bt .bm{font-size:.74rem;color:var(--muted);flex:none}
.btx{padding:0 11px 9px;font-size:.86rem;line-height:1.85}
.btx p{margin:3px 0}
.who{margin-top:14px;border:1px solid var(--line);border-radius:11px;background:var(--card);overflow:hidden}
.who>summary{list-style:none;cursor:pointer;padding:12px 14px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.who>summary::-webkit-details-marker{display:none}
.who>summary::after{content:"\\203A";margin-left:auto;font-size:19px;color:var(--muted);transition:transform .2s}
.who[open]>summary::after{transform:rotate(90deg)}
.who h3{font-family:"Noto Serif TC",serif;font-size:16px;color:var(--ink)}
.who .amt{font-size:.8rem;font-weight:700;background:var(--warn);color:var(--key);padding:1px 8px;border-radius:99px;white-space:nowrap}
.who .org{font-size:.74rem;color:var(--muted);white-space:nowrap}
.whob{padding:0 14px 14px}
.lad{display:grid;gap:8px;margin-top:10px}
.lrow{display:grid;grid-template-columns:96px 1fr;gap:10px;align-items:start;border:1px solid var(--line);border-radius:9px;padding:9px 11px;background:var(--card)}
.lrow .lv{font-weight:700;font-size:.84rem;color:var(--key);background:var(--warn);border-radius:7px;padding:4px 6px;text-align:center}
.lrow .ld b{color:var(--ink)}
.lrow .ld small{display:block;color:var(--muted);font-size:.78rem;margin-top:2px}
@media(max-width:430px){.lrow{grid-template-columns:1fr}.lrow .lv{text-align:left}}
.only{display:grid;gap:8px;margin-top:10px}
.only div{border:1px solid var(--line);border-left:3px solid var(--red);border-radius:8px;padding:8px 11px;font-size:14px;background:var(--card)}
.only b{color:var(--red)}
ul.pl li{margin-top:4px}
.ctr{color:var(--red);font-weight:700}
'''

# ───────── 內容 ─────────
S = []


def sec(sid, color, title, cnt, body, open_=False):
    S.append('<details class="sec" id="%s" style="--a:var(--c%s)"%s><summary><h2>%s</h2>'
             '<span class="cnt">%s</span></summary><div class="bd">\n%s\n</div></details>'
             % (sid, color, ' open' if open_ else '', title, cnt, body))


sec('p0', 'E', '⓪ 先把三個問題分開：罰誰、誰罰、罰多少', '一頁看懂', '''
<p style="font-size:14px">考題問的永遠是這三件事的其中一件，但它們的答案<b class="ctr">不是同一條軸</b>。把它們疊在一起背，就會混。</p>
<div class="tw rc"><table style="min-width:620px"><thead><tr><th style="width:17%">問題</th><th style="width:33%">答案怎麼決定</th><th>記法</th></tr></thead><tbody>
<tr><td><b>罰誰</b><br><span class="law">處罰對象</span></td><td>看<b class="ctr">身分</b>：管理幹部／住戶／區分所有權人／起造人建築業者／管理維護公司與服務人員，共<b>五種</b></td><td>先問「這個人是誰」，不要先想金額</td></tr>
<tr><td><b>誰罰</b><br><span class="law">主管機關</span></td><td>幾乎全部是<b>直轄市、縣（市）主管機關</b>；<b class="ctr">只有 §51 是中央主管機關</b></td><td>記<b class="ctr">一個例外</b>就好</td></tr>
<tr><td><b>罰多少</b><br><span class="law">金額級距</span></td><td>看<b class="ctr">違規的性質</b>：內部失職／生活秩序／安全與財產，共<b>三階</b></td><td>金額不是看身分，是看<b>闖的禍有多大</b></td></tr>
</tbody></table></div>
<div class="mn"><b>為什麼金額要看「性質」不看「身分」：</b>同一個主委，「沒督促投保」只罰 <span class="n">1千～5千</span>（§48①），但「卸任不移交」就跳到 <span class="n">4萬～20萬</span>（§49Ⅰ⑦）。同一個住戶，亂丟垃圾 <span class="n">3千～1.5萬</span>（§47②），但在逃生通道堆雜物 <span class="n">4萬～20萬</span>（§49Ⅰ④）。<b>身分一樣、金額差幾十倍，差在闖的禍。</b></div>
''', open_=True)

sec('p1', 'E', '① 罰多少：三階金額，各對應一種性質', '§47／§48／§49', '''
<div class="lad">
<div class="lrow"><div class="lv">1千～5千<br><small style="color:var(--muted)">§48</small></div>
<div class="ld"><b>內部失職</b>——管理幹部「該做沒做」，還沒造成外部危害
<small>四款全部都是管理負責人、主委或管理委員：①未善盡督促住戶投保責任保險（§17）②無正當理由未執行 §22 促請改善或訴請遷離、出讓之職務 ③無正當理由違反 §35（拒絕利害關係人閱覽影印）④無正當理由未執行 §36 第 1 款、第 5 款至第 12 款職務且顯然影響住戶權益</small></div></div>
<div class="lrow"><div class="lv">3千～1.5萬<br><small style="color:var(--muted)">§47</small></div>
<div class="ld"><b>生活秩序</b>——會議沒開、鄰里公害
<small>三款：①召集人、起造人或臨時召集人違反 §25 或 §28 之<b>召集義務</b> ②住戶違反 <b class="ctr">§16 第 1 項</b>（棄置垃圾、排放污染惡臭、喧囂振動）<b class="ctr">或第 4 項</b>（飼養動物妨礙公共衛生、安寧、安全）③區分所有權人或住戶違反 §6（相鄰義務），經主管機關受理請求、通知限期改善而屆期不改善</small></div></div>
<div class="lrow"><div class="lv">4萬～20萬<br><small style="color:var(--muted)">§49</small></div>
<div class="ld"><b>安全與財產</b>——動到建物、動到錢、動到別人的權利
<small>八款：①區分所有權人對<b>專有部分之利用</b>違反 §5 ②住戶違反 §8Ⅰ 或 §9Ⅱ 變更使用限制，<b class="ctr">經制止而不遵從</b> ③住戶違反 §15Ⅰ <b>擅自變更</b>專有或約定專用之使用 ④住戶違反 <b class="ctr">§16 第 2 項</b>（逃生通道堆置雜物、設柵欄、營業使用、違規廣告物、私設路障）<b class="ctr">或第 3 項</b>（未經核准破壞或變更主要構造）⑤住戶違反 §17 <b>未投保</b>責任保險 ⑥區分所有權人違反 §18Ⅰ② <b>未繳納公共基金</b> ⑦管理負責人、主委或管理委員違反 §20 之<b>公告或移交</b>義務 ⑧<b>起造人或建築業者</b>違反 §57 或 §58</small></div></div>
</div>
<div class="mn"><b>口訣〔自編〕：</b>「<b>幹部失職一到五千・生活秩序三千一萬五・安全財產四萬二十萬</b>」。三階的分界線是「<b>有沒有危害到建物安全、公共安全或別人的錢</b>」。</div>
<div class="tr"><b>§16 一條拆兩階，這是最常考的切點：</b><br>
§16<b class="ctr">Ⅰ</b>（垃圾、污染、惡臭、喧囂、振動）與 §16<b class="ctr">Ⅳ</b>（飼養動物妨礙公衛安寧安全）→ <b>§47②，3千～1.5萬</b><br>
§16<b class="ctr">Ⅱ</b>（逃生通道堆雜物、營業使用、違規廣告物、私設路障）與 §16<b class="ctr">Ⅲ</b>（破壞或變更主要構造）→ <b>§49Ⅰ④，4萬～20萬</b><br>
記法：<b>Ⅰ、Ⅳ 是「吵到人、髒到人」；Ⅱ、Ⅲ 是「逃不出去、房子會垮」</b>，後者貴一個數量級。</div>
''' + '<div class="lawwrap"><div class="group-label">這三條的逐字全文</div>'
    + bt('公寓大廈 §47', '★★★') + bt('公寓大廈 §48', '★★') + bt('公寓大廈 §49', '★★★') + '</div>')

sec('p2', 'E', '② 罰誰：五種身分，各自會踩到哪幾款', '查表用', '''
<div class="tw rc"><table style="min-width:860px"><thead><tr><th style="width:18%">罰誰（處罰對象）</th><th style="width:30%">踩到什麼</th><th style="width:14%">罰多少</th><th style="width:16%">誰罰</th><th>程序</th></tr></thead><tbody>
<tr><td rowspan="2"><b>管理負責人<br>主任委員<br>管理委員</b></td>
<td><b>§48 四款</b>：未督促投保／未執行 §22 職務／違反 §35 拒絕閱覽／未執行 §36①⑤～⑫ 且顯然影響住戶權益</td><td><span class="n">1千～5千</span></td><td rowspan="2">直轄市、縣（市）</td><td rowspan="2">得令限期改善或履行義務、職務；<b class="ctr">屆期不改善或不履行者，得連續處罰</b></td></tr>
<tr><td><b>§49Ⅰ⑦</b>：違反 §20 之<b>公告或移交</b>義務</td><td><span class="n">4萬～20萬</span></td></tr>
<tr><td rowspan="2"><b>住戶</b><br><span class="nv" style="font-size:.78rem;color:var(--muted)">（含非區分所有權人之承租人等）</span></td>
<td><b>§47②</b>：違反 §16Ⅰ 或 Ⅳ（垃圾污染惡臭喧囂振動、飼養動物）</td><td><span class="n">3千～1.5萬</span></td><td rowspan="2">直轄市、縣（市）</td><td rowspan="2">同上，得連續處罰。<b>§49Ⅰ②</b> 另須「<b class="ctr">經制止而不遵從</b>」才罰</td></tr>
<tr><td><b>§49Ⅰ②③④⑤</b>：變更使用限制經制止不遵從／擅自變更使用／§16Ⅱ、Ⅲ／未投保責任保險</td><td><span class="n">4萬～20萬</span></td></tr>
<tr><td rowspan="2"><b>區分所有權人</b></td>
<td><b>§47③</b>：違反 §6 相鄰義務，經通知限期改善屆期不改（住戶亦同）</td><td><span class="n">3千～1.5萬</span></td><td rowspan="2">直轄市、縣（市）</td><td>§47③ 的「<b class="ctr">經主管機關受理請求、通知限期改善</b>」是前提</td></tr>
<tr><td><b>§49Ⅰ①⑥</b>：專有部分之利用違反 §5／未繳納公共基金（§18Ⅰ②）<br><b>§49-1</b>：未依 §29-1Ⅰ 期限內成立管委會或推選管理負責人並報備</td><td><span class="n">4萬～20萬</span><br><b class="ctr">§49-1 按每一專有部分計罰</b></td><td>§49-1 令限期辦理，<b class="ctr">屆期仍未辦理得按次處罰</b></td></tr>
<tr><td><b>起造人<br>建築業者</b></td>
<td><b>§47①</b>：違反 §28 召集義務（起造人）<br><b>§49Ⅰ⑧</b>：違反 §57（檢測點交）或 §58（未領建照即銷售、讓售共用部分）</td><td><span class="n">3千～1.5萬</span><br><span class="n">4萬～20萬</span></td><td>直轄市、縣（市）</td><td>得令限期改善或履行，屆期不改得連續處罰</td></tr>
<tr><td><b>管理維護公司<br>管理服務人員</b></td>
<td><b>§50</b>：違反 §42，<b>未領得登記證、認可證或經廢止後仍營業</b>，或接受委任僱傭執行管理維護服務<br><b>§51Ⅰ</b>：公司違反 §43<br><b>§51Ⅱ</b>：受僱於管理維護公司之服務人員違反 §44<br><b>§51Ⅲ</b>：前項以外之管理服務人員違反 §45</td>
<td><span class="n">4萬～20萬</span><br><span class="n">3萬～15萬</span><br><span class="n">3千～1.5萬</span><br><span class="n">3千～1.5萬</span></td>
<td>§50 直轄市、縣（市）<br><b class="ctr">§51 中央主管機關</b></td>
<td>§50 <b class="ctr">勒令停業或停止執行業務</b>＋罰鍰，拒不遵從得按次連續處罰<br>§51 一律<b class="ctr">先通知限期改正，屆期不改正</b>才處分</td></tr>
</tbody></table></div>
<div class="tr"><b>考試陷阱：</b>①把「<b>誰罰</b>」全部寫成直轄市、縣（市）主管機關——<b class="ctr">§51 三項都是中央主管機關</b>，這是整章唯一的例外。②§50 不是只有罰鍰，<b>一定要寫勒令停業或停止執行業務</b>。③§51 不是直接開罰，<b>先通知限期改正</b>；屆期不改正才「得」停業、廢止許可或登記證、或罰鍰。④§49-1 是<b class="ctr">按每一專有部分</b>處區分所有權人，不是整棟罰一次。</div>
''' + '<div class="lawwrap"><div class="group-label">這三條的逐字全文</div>'
    + bt('公寓大廈 §49之1', '★★') + bt('公寓大廈 §50', '★★') + bt('公寓大廈 §51', '★★★　唯一歸中央') + '</div>')

sec('p3', 'E', '③ 四個「唯一」：考前十秒掃一遍', '最好拿分的四句', '''
<div class="only">
<div><b>唯一歸中央主管機關的：§51</b>　管理維護公司違反 §43（3萬～15萬）、受僱服務人員違反 §44、其他管理服務人員違反 §45（均 3千～1.5萬）。其餘 §47、§48、§49、§49-1、§50 全部是直轄市、縣（市）主管機關。</div>
<div><b>唯一按「每一專有部分」計罰的：§49-1</b>　未於 §29-1Ⅰ 期限內成立管委會或推選管理負責人並報備，按<b>每一專有部分</b>處區分所有權人 4萬～20萬，並令限期辦理，屆期仍未辦理得按次處罰。</div>
<div><b>唯一有「勒令停業」的：§50</b>　無證營業或經廢止後仍營業，勒令停業或停止執行業務，<b>並</b>處 4萬～20萬；拒不遵從得按次連續處罰。</div>
<div><b>唯一有刑責的：§49 第 2 項</b>　<b>有供營業使用事實</b>之住戶，有 §49Ⅰ 第 3 款（擅自變更使用）或第 4 款（§16Ⅱ、Ⅲ）行為，<b>因而致人於死</b>→ 1年以上7年以下有期徒刑，得併科 100萬～500萬罰金；<b>致重傷</b>→ 6個月以上5年以下有期徒刑，得併科 50萬～250萬罰金。</div>
</div>
<div class="mn"><b>口訣〔自編〕：</b>「<b>中央只管 51、按戶只有 49-1、停業只有 50、坐牢只有 49 第 2 項</b>」。四句背完，這一章的「誰罰」與特殊處分就不會錯。</div>
<div class="sub2">另外兩條程序條文</div>
<ul class="pl">
<li><span class="law">§59</span>　<b>誰可以檢舉</b>：召集人、臨時召集人、起造人、建築業者、區分所有權人、住戶、管理負責人、主委或管理委員有 §47、§48、§49 各款情事之一時，<b>他區分所有權人、利害關係人、管理負責人或管理委員會</b>得<b class="ctr">列舉事實及提出證據</b>，報直轄市、縣（市）主管機關處理。</li>
<li><span class="law">§52</span>　<b>不繳怎麼辦</b>：依本條例所處之罰鍰，經限期繳納屆期仍不繳納者，<b class="ctr">依法移送強制執行</b>。</li>
</ul>
''' + '<div class="lawwrap"><div class="group-label">逐字全文</div>' + bt('公寓大廈 §59') + bt('公寓大廈 §52') + '</div>')

sec('p4', 'E', '④ 三十秒自我檢查', '把答案遮起來', '''
<p style="font-size:13.5px;color:var(--muted)">每題先答「罰誰／誰罰／罰多少／要不要先限期」，再展開對答案。</p>
''' + ''.join(
    '<details class="bt"><summary><b class="bn">Q%d</b><span class="bti">%s</span></summary><div class="btx"><p>%s</p></div></details>' % (i + 1, q, a)
    for i, (q, a) in enumerate([
        ('住戶甲在逃生通道堆放雜物，經制止仍不改。', '罰誰＝<b>住戶甲</b>；誰罰＝<b>直轄市、縣（市）主管機關</b>；罰多少＝<b>4萬～20萬</b>（§49Ⅰ④，違反 §16<b class="ctr">Ⅱ</b>）；得令限期改善，屆期不改得連續處罰。<b>注意不是 3千～1.5萬</b>——那是 §16Ⅰ、Ⅳ。'),
        ('主委乙卸任後拒絕移交帳冊。', '罰誰＝<b>主任委員乙</b>；誰罰＝直轄市、縣（市）；罰多少＝<b>4萬～20萬</b>（§49Ⅰ⑦，違反 §20 公告或移交義務）。<b>不是 §48 的 1千～5千</b>——移交是 §49 等級。另 §29Ⅳ：拒絕移交者自任期屆滿日起視同解任。'),
        ('某公寓大廈逾期未成立管委會，共 40 個專有部分。', '罰誰＝<b>區分所有權人</b>；誰罰＝直轄市、縣（市）；罰多少＝<b>按每一專有部分</b>處 4萬～20萬（§49-1），並令限期辦理，屆期仍未辦理得<b>按次</b>處罰。'),
        ('某管理維護公司未領登記證即承接社區管理業務。', '罰誰＝<b>管理維護公司</b>；誰罰＝直轄市、縣（市）；處分＝<b>勒令停業或停止執行業務</b>，<b>並</b>處 4萬～20萬（§50，違反 §42）；拒不遵從得按次連續處罰。'),
        ('受僱於管理維護公司的服務人員丙違反 §44。', '罰誰＝<b>管理服務人員丙</b>；誰罰＝<b class="ctr">中央主管機關</b>（整章唯一例外）；程序＝<b>先通知限期改正</b>，屆期不改正才得廢止認可證、或停止執行業務 <b>3 個月以上 3 年以下</b>、或處 <b>3千～1.5萬</b>（§51Ⅱ）。'),
        ('管理負責人丁無正當理由拒絕利害關係人閱覽公共基金餘額。', '罰誰＝<b>管理負責人丁</b>；誰罰＝直轄市、縣（市）；罰多少＝<b>1千～5千</b>（§48③，違反 §35）；得令限期改善或履行職務，屆期不履行得連續處罰。'),
    ])))

BODY = '\n\n'.join(S)
NAV = ('<nav><a href="#p0">⓪ 三個問題分開</a><a href="#p1">① 罰多少</a><a href="#p2">② 罰誰</a>'
       '<a href="#p3">③ 四個唯一</a><a href="#p4">④ 自我檢查</a></nav>')

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>公寓大廈罰則</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s%s</style></head><body>
<div style="position:sticky;top:0;z-index:99;background:#8A5517;color:#fff;padding:7px 12px;font-size:13px;line-height:1.6">〔<b>重做 demo</b>〕正式頁未動。只走一條軸線：<b>罰誰 → 誰罰 → 罰多少 → 程序</b>；色彩只用站內四色（金額金底、關鍵詞紅、口訣綠底、陷阱紅框）。</div>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規｜公寓大廈條例罰則</h1><div class="sub">罰誰・誰罰・罰多少・要不要先限期　§47～§52、§49-1、§59</div></header>
%s
<main>
<div class="intro"><b>這頁只回答四個問題：</b>這個人是<b>誰</b>（罰誰）→ 哪個機關罰（<b>誰罰</b>）→ 哪一階金額（<b>罰多少</b>）→ 要不要<b>先限期改善</b>。三階金額是看「闖的禍有多大」，不是看身分；主管機關只有 §51 一個例外。條文逐字取自全國法規資料庫現行條文。</div>
<div class="tools"><button id="ea">全部展開</button><button id="ca">全部收合</button></div>

%s

<p class="foot">本頁為備考整理，非法規原文。條文來源：公寓大廈管理條例（全國法規資料庫現行條文，站內條文庫逐字）。考前以紙本六法為準。</p>
</main>
<script>
(function(){
document.getElementById('ea').onclick=function(){document.querySelectorAll('details').forEach(function(x){x.open=true})};
document.getElementById('ca').onclick=function(){document.querySelectorAll('details').forEach(function(x){x.open=false})};
document.querySelectorAll('.rc table').forEach(function(t){var h=[].map.call(t.querySelectorAll('thead th'),function(x){return x.textContent});t.querySelectorAll('tbody tr').forEach(function(r){[].forEach.call(r.children,function(td,i){td.setAttribute('data-l',h[i]||'')})})});
var tb=document.getElementById('themeBtn');function ub(){tb.textContent=document.documentElement.getAttribute('data-theme')==='dark'?'🌙':'☀️'}ub();
tb.onclick=function(){var h=document.documentElement,n=h.getAttribute('data-theme')==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}ub()};
})();
</script>
%s
</body></html>''' % (CSS, EXTRA, NAV, BODY, FAB.replace('%E7%B6%93', '%E7%B6%93'))

dst = os.path.join(ROOT, 'demo', '經紀法規_公寓大廈罰則_demo.html')
os.makedirs(os.path.dirname(dst), exist_ok=True)
io.open(dst, 'w', encoding='utf-8').write(HTML)
print('已產生 demo/經紀法規_公寓大廈罰則_demo.html', len(HTML) // 1024, 'KB')
