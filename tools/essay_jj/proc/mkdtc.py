# -*- coding: utf-8 -*-
"""產生《經紀法規_定型化契約專區》。樣式與 bxfab 直接沿用《程序總整理》，確保兩頁同一套視覺。"""
import json, io, re, os

ROOT = '/home/claude/bernih7/brokerx'
SRC = io.open(ROOT + '/經紀法規_程序總整理.html', encoding='utf-8').read()
CSS = re.search(r'<style>([\s\S]*?)</style>', SRC).group(1)
FAB = SRC[SRC.index('<!--bxfab-->'):SRC.index('<!--/bxfab-->') + len('<!--/bxfab-->')]

Q = {x['k']: x for x in json.load(io.open(ROOT + '/tools/essay_jj/quiz_data.json', encoding='utf-8'))['q']}
CHS = json.load(io.open(ROOT + '/tools/essay_jj/chapters.json', encoding='utf-8'))

GRP = {'D2': '預售屋契約', 'D3': '委託銷售契約', 'H1': '消保法定型化規範'}
QD = []
for ch in ['H1', 'D2', 'D3']:
    for x in sorted([v for v in Q.values() if v['ch'] == ch], key=lambda v: (v['y'], v['n'])):
        QD.append({'k': x['k'], 'y': '%d年第%d題' % (x['y'], x['n']), 'g': CHS[ch], 'gr': ch,
                   'q': x['stem'], 'o': x['opt'], 'c': 'ABCD'.index(x['ans']), 'e': x['exp']})

QUIZ = 'https://bernih7.github.io/brokerX/%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html'
HUB = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'
YJ = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%87%89%E8%A8%98%E8%BC%89%E4%B8%8D%E5%BE%97%E8%A8%98%E8%BC%89%E7%B8%BD%E6%95%B4%E7%90%86.html'

S = []


def sec(sid, color, title, cnt, body, open_=False):
    S.append('<details class="sec" id="%s" style="--a:var(--c%s)"%s><summary><h2>%s</h2><span class="cnt">%s</span></summary><div class="bd">\n%s\n</div></details>'
             % (sid, color, ' open' if open_ else '', title, cnt, body))


sec('d0', 'H', '⓪ 四層結構：誰管誰、誰輸給誰', '一張圖看懂', '''
<p style="font-size:14px">不動產的定型化契約一定同時受<b>兩套規範</b>夾擊：上面是<b class="k">消費者保護法</b>（通則，管「條款公不公平」），下面是<b class="k">內政部公告的應記載及不得記載事項</b>（特別規定，管「一定要寫什麼、一定不能寫什麼」）。兩套的制裁方式不一樣，這是本篇所有考點的源頭。</p>
<div class="tw rc"><table style="min-width:680px"><thead><tr><th style="width:9%">層</th><th style="width:24%">是什麼</th><th style="width:30%">法源</th><th>贏過誰／輸給誰</th></tr></thead><tbody>
<tr><td><b>第 1 層</b></td><td>消費者保護法</td><td><span class="law">消保§2⑦⑧⑨、§11～§17-1</span></td><td>最上位。條款違反誠信原則對消費者顯失公平者<b class="k">無效</b>（§12Ⅰ）</td></tr>
<tr><td><b>第 2 層</b></td><td>中央主管機關公告之<b>應記載／不得記載事項</b></td><td><span class="law">消保§17</span>＋內政部四份公告</td><td>應記載事項<b class="k">雖未記載仍構成契約內容</b>（§17Ⅴ）；違反公告之定型化契約，其<b class="k">條款無效</b>（§17Ⅳ）</td></tr>
<tr><td><b>第 3 層</b></td><td>企業經營者預先擬好的<b>定型化契約條款</b></td><td><span class="law">消保§2⑦</span></td><td>牴觸個別磋商條款時，<b class="k">牴觸部分無效</b>（§15）</td></tr>
<tr><td><b>第 4 層</b></td><td>雙方<b>個別磋商條款</b></td><td><span class="law">消保§2⑧</span></td><td>最強。贏過第 3 層</td></tr>
</tbody></table></div>
<div class="mn"><b>由上而下記：</b>消保法 → 內政部公告 → 定型化條款 → 個別磋商條款。<b class="k">但效力由下而上</b>：個別磋商條款贏定型化條款，公告的應記載事項又把定型化契約「補回去」，最上面的消保法 §12 則可以直接把條款打掉。</div>
<p style="font-size:13.5px;margin-top:8px">※ 內政部四份公告（說明書／成屋／預售屋／委託銷售）的<b>逐項內容、不得記載矩陣、空白效果</b>，在另一頁《<a href="@@YJ@@" style="color:var(--pri);font-weight:700">應記載與不得記載總整理</a>》；本頁專攻<b>消保法這一層</b>的體系與效果，兩頁互補不重複。</p>
'''.replace('@@YJ@@',YJ), open_=True)

sec('d1', 'H', '① 三個定義：定型化契約條款 / 個別磋商條款 / 定型化契約', '消保§2⑦⑧⑨', '''
<div class="tw rc"><table style="min-width:620px"><thead><tr><th style="width:22%">名詞</th><th>定義（§2 逐字重點）</th></tr></thead><tbody>
<tr><td><b>定型化契約條款</b><br><span class="law">§2⑦</span></td><td>企業經營者為與<b class="k">多數消費者</b>訂立<b>同類契約</b>之用，所提出<b class="k">預先擬定</b>之契約條款。<b class="k">不限於書面</b>，其以<b>放映字幕、張貼、牌示、網際網路或其他方法</b>表示者，亦屬之。</td></tr>
<tr><td><b>個別磋商條款</b><br><span class="law">§2⑧</span></td><td>契約當事人<b class="k">個別磋商而合意</b>之契約條款。</td></tr>
<tr><td><b>定型化契約</b><br><span class="law">§2⑨</span></td><td>以企業經營者提出之定型化契約條款作為契約內容之<b class="k">全部或一部</b>而訂立之契約。</td></tr>
</tbody></table></div>
<div class="mn"><b>兩條基本原則（§11）：</b>①定型化契約條款應本<b class="k">平等互惠</b>之原則；②條款<b class="k">如有疑義，應為有利於消費者之解釋</b>。</div>
<div class="tr"><b>考試陷阱：</b>①§2⑦ 是「<b class="k">多數</b>消費者」，不是「<b>不特定</b>多數消費者」——101-11 就在拆這個用字。②「不限於書面」是法條明文，口頭之外的字幕、張貼、牌示、網路都算。③「疑義作有利於消費者解釋」是 §11Ⅱ，不是 §12；§12 講的是<b>顯失公平無效</b>，兩者常被混在同一選項裡。④定型化契約只要「全部<b>或一部</b>」用了定型化條款就算，不是要整份都是。</div>
''')

sec('d2', 'H', '② 審閱期：30 日以內的「合理期間」', '消保§11-1；內政部公告 5 日／3 日', '''
<ol class="flow">
<li><b>原則</b>：企業經營者與消費者訂立定型化契約<b class="k">前</b>，應有 <span class="n">30 日以內</span>之<b class="k">合理期間</b>，供消費者審閱<b class="k">全部</b>條款內容（<span class="law">§11-1Ⅰ</span>）。</li>
<li><b>不能叫人拋棄</b>：以定型化契約條款使消費者<b class="k">拋棄</b>審閱權者，<b class="k">無效</b>（<span class="law">§11-1Ⅱ</span>）。</li>
<li><b>違反的效果</b>：違反第一項規定者，<b class="k">其條款不構成契約之內容</b>。<b class="k">但消費者得主張該條款仍構成契約之內容</b>（<span class="law">§11-1Ⅲ</span>）。</li>
<li><b>行業別公告</b>：中央主管機關得選擇特定行業，參酌條款重要性、涉及事項多寡及複雜程度等，<b class="k">公告</b>定型化契約之審閱期間（<span class="law">§11-1Ⅳ</span>）。</li>
</ol>
<div class="tw rc"><table style="min-width:560px"><thead><tr><th style="width:42%">不動產四份公告</th><th style="width:26%">審閱期</th><th>備註</th></tr></thead><tbody>
<tr><td>不動產<b>說明書</b>應記載及不得記載事項</td><td><b>—</b></td><td>說明書不是契約，<b class="k">無審閱期</b></td></tr>
<tr><td><b>成屋</b>買賣定型化契約</td><td>至少 <span class="n">5 日</span></td><td rowspan="2">兩份買賣契約同為 5 日</td></tr>
<tr><td><b>預售屋</b>買賣定型化契約</td><td>至少 <span class="n">5 日</span></td></tr>
<tr><td><b>不動產委託銷售</b>定型化契約（含要約書附件）</td><td>不得少於 <span class="n">3 日</span></td><td>委託契約比買賣契約短</td></tr>
</tbody></table></div>
<div class="mn"><b>口訣〔自編〕：</b>「<b>母法 30 以內、買賣 5 天、委託 3 天、說明書沒有</b>」。</div>
<div class="tr"><b>考試陷阱：</b>①§11-1Ⅰ 是「<b class="k">30 日以內</b>之合理期間」，<b>不是「至少 30 日」</b>——這是審閱期最常被倒過來的一句。②違反審閱期的效果是「<b class="k">不構成契約之內容</b>」，<b>不是無效</b>；而且<b class="k">消費者還可以反過來主張它構成契約內容</b>（對消費者有利時）。③使消費者拋棄審閱權的「<b>條款</b>」才是無效；違反審閱期本身走「不構成內容」——兩個效果在同一條裡，常被對調。④說明書沒有審閱期，別被「不動產四份公告」一起套上 5 日。</div>
''')

sec('d3', 'C', '③ 核心對照：「無效」vs「不構成契約之內容」', '最高頻考點', '''
<p style="font-size:14px">H1 篇幾乎每年都考這一刀。同樣是「這個條款不算數」，消保法分成兩種法律效果，<b class="k">能不能由消費者選擇</b>是最大的差別。</p>
<div class="tw rc"><table style="min-width:760px"><thead><tr><th style="width:9%">條</th><th style="width:34%">情形</th><th style="width:21%">效果</th><th>消費者可否主張仍有效</th></tr></thead><tbody>
<tr><td><span class="law">§11-1Ⅱ</span></td><td>以條款使消費者<b>拋棄審閱權</b></td><td><b class="k">無效</b></td><td>不可</td></tr>
<tr><td><span class="law">§11-1Ⅲ</span></td><td><b>未給審閱期</b></td><td><b class="k">不構成契約之內容</b></td><td><b class="k">可以</b>（但書明文）</td></tr>
<tr><td><span class="law">§12Ⅰ</span></td><td>條款違反<b>誠信原則、對消費者顯失公平</b></td><td><b class="k">無效</b></td><td>不可</td></tr>
<tr><td><span class="law">§14</span></td><td>條款<b>未經記載於定型化契約中</b>，依正常情形<b>顯非消費者所得預見</b>（異常條款）</td><td><b class="k">不構成契約之內容</b></td><td>條文未設但書</td></tr>
<tr><td><span class="law">§15</span></td><td>定型化契約條款<b>牴觸個別磋商條款</b></td><td><b class="k">牴觸部分無效</b></td><td>不可</td></tr>
<tr><td><span class="law">§17Ⅳ</span></td><td>違反公告之<b>應記載或不得記載事項</b></td><td>該<b class="k">定型化契約條款無效</b>；契約效力依 §16 定之</td><td>不可</td></tr>
<tr><td><span class="law">§17Ⅴ</span></td><td>公告之<b>應記載事項</b>雖未記載於契約</td><td><b class="k">仍構成契約之內容</b>（反向補進去）</td><td>—</td></tr>
<tr><td><span class="law">細則§12</span></td><td>條款因<b>字體、印刷或其他情事</b>致難以注意其存在或辨識</td><td><b class="k">不構成契約之內容</b></td><td><b class="k">可以</b>（但書明文）</td></tr>
</tbody></table></div>
<div class="sub2">§12Ⅱ 推定顯失公平的三款（背死）</div>
<ul class="pl">
<li>一、違反<b class="k">平等互惠</b>原則者。</li>
<li>二、條款與其所排除不予適用之<b class="k">任意規定之立法意旨顯相矛盾</b>者。</li>
<li>三、契約之<b class="k">主要權利或義務</b>，因受條款之限制，致<b class="k">契約之目的難以達成</b>者。</li>
</ul>
<p style="font-size:13.5px;margin-top:6px">何謂「違反平等互惠原則」，<span class="law">細則§14</span> 列四款：①給付與對待給付<b>顯不相當</b>②消費者應負擔<b>非其所能控制之危險</b>③消費者違約時應負擔<b>顯不相當之賠償責任</b>④其他顯有不利於消費者之情形。是否顯失公平，<span class="law">細則§13</span> 應斟酌<b>契約性質、締約目的、全部條款內容、交易習慣及其他情事</b>判斷。</p>
<div class="sub2">一部無效之後：契約還在不在（§16）</div>
<p>定型化契約中之定型化契約條款，<b>全部或一部無效或不構成契約內容之一部</b>者，<b class="k">除去該部分契約亦可成立者，其他部分仍為有效</b>；<b class="k">但對當事人之一方顯失公平者，該契約全部無效</b>（<span class="law">§16</span>）。</p>
<div class="mn"><b>口訣〔自編〕：</b>「<b>兩個『不構成』都有後路</b>」——沒給審閱期（§11-1Ⅲ）與字體看不清（細則§12），消費者都可以反過來主張它算數；其餘一律是<b>無效</b>，消費者沒有選擇權。</div>
<div class="tr"><b>考試陷阱：</b>①§14 的異常條款是「<b class="k">未經記載於</b>定型化契約中」＋「依正常情形<b class="k">顯非消費者所得預見</b>」兩個要件，不是只看一個。②§15 是「<b class="k">牴觸部分</b>無效」，不是整份契約無效、也不是個別磋商條款無效。③§16 的原則是「<b class="k">其他部分仍為有效</b>」，<b>例外</b>才是全部無效（顯失公平時）——方向常被倒過來。④§17Ⅳ（違反公告→條款無效）與 §17Ⅴ（應記載未記載→仍構成內容）是<b class="k">一正一反</b>，同一條兩個方向，最容易混。⑤§12Ⅱ 是「<b class="k">推定</b>」顯失公平（可舉反證推翻），不是「視為」。⑥主張符合本節規定之事實者，<b class="k">由企業經營者負舉證責任</b>（§17-1）。</div>
''')

sec('d4', 'C', '④ 應記載 vs 不得記載：誰訂、怎麼罰', '消保§17、§56-1', '''
<ol class="flow">
<li><b>誰訂</b>：<b class="k">中央主管機關</b>為預防消費糾紛、保護消費者權益、促進定型化契約之公平化，得<b class="k">選擇特定行業</b>，擬訂其定型化契約應記載或不得記載事項，<b class="k">報請行政院核定後公告之</b>（<span class="law">§17Ⅰ</span>）。不動產四份公告的中央主管機關是<b class="k">內政部</b>。</li>
<li><b>應記載事項的內容範圍（§17Ⅱ 五款）</b>：①契約之<b>重要權利義務事項</b>②<b>違反契約之法律效果</b>③<b>預付型交易之履約擔保</b>④契約之<b>解除權、終止權及其法律效果</b>⑤其他與契約履行有關之事項。</li>
<li><b>不得記載事項的內容範圍（§17Ⅲ 四款）</b>：①企業經營者<b>保留契約內容或期限之變更權或解釋權</b>②<b>限制或免除企業經營者之義務或責任</b>③<b>限制或剝奪消費者行使權利，加重消費者之義務或責任</b>④其他對消費者<b>顯失公平</b>事項。</li>
<li><b>兩個法律效果</b>：違反公告之定型化契約，其條款<b class="k">無效</b>，契約效力依 §16 定（<span class="law">§17Ⅳ</span>）；公告之<b>應記載事項雖未記載</b>於定型化契約，<b class="k">仍構成契約之內容</b>（<span class="law">§17Ⅴ</span>）。使用定型化契約者，主管機關<b class="k">得隨時派員查核</b>（§17Ⅵ）。</li>
<li><b>行政罰（§56-1）</b>：企業經營者使用定型化契約違反 §17Ⅰ 公告之應記載或不得記載事項者，除法律另有處罰規定外，<b class="k">經主管機關令其限期改正而屆期不改正者，處 3 萬～30 萬元</b>；<b class="k">經再次令其限期改正而屆期不改正者，處 5 萬～50 萬元，並得按次處罰</b>。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>「<b>先令改正才罰、罰完再令、再不改加碼</b>」——§56-1 是<b class="k">雙層階梯</b>：3～30 萬 → 5～50 萬＋按次。沒有「立即開罰」這回事。</div>
<div class="tr"><b>考試陷阱：</b>①公告流程是「中央主管機關<b>擬訂</b> → <b class="k">報請行政院核定</b> → 公告」，少了行政院那一關就是錯的。②§56-1 要<b class="k">先令限期改正、屆期不改</b>才罰，<b>不是一違反就罰</b>。③兩段罰鍰是 <b>3～30 萬</b> 與 <b>5～50 萬</b>，不是 3～15 萬、不是 6～30 萬（那是經紀業條例 §29 的級距）。④「應記載事項未記載<b class="k">仍構成契約內容</b>」對<b>消費者有利</b>；「不得記載卻記載了」則是<b class="k">該條款無效</b>——兩種方向要分清楚。⑤應記載事項的詳細逐項內容在《應記載與不得記載總整理》，本頁只管法律效果。</div>
''')

sec('d5', 'D', '⑤ 不動產三份契約：空白沒寫會怎樣', '內政部公告；詳細版見另一頁', '''
<p style="font-size:14px">這幾題的考法固定：<b>某一欄空白未記載</b>，問法律效果。答案不是「契約無效」就是「不得收」或「可隨時終止」，記住這張小表就夠。</p>
<div class="tw rc"><table style="min-width:640px"><thead><tr><th style="width:36%">空白的欄位</th><th style="width:32%">效果</th><th>考古題</th></tr></thead><tbody>
<tr><td>委託銷售<b>價格</b>未記載金額</td><td><b class="k">契約無效</b></td><td>101-24、103-11</td></tr>
<tr><td>委託銷售<b>期間</b>未記載</td><td>委託人得<b class="k">隨時以書面終止</b></td><td>101-24</td></tr>
<tr><td><b>服務報酬</b>數額空白</td><td>受託人<b class="k">不得向委託人收取</b>服務報酬</td><td>103-5</td></tr>
<tr><td>沒收<b>定金</b>百分比未記載</td><td>受託人<b class="k">不得請求該部分費用</b>，亦<b class="k">不得再收報酬</b></td><td>102-13</td></tr>
<tr><td>委託銷售契約及其附件<b>審閱期間</b></td><td><b class="k">不得少於 3 日</b></td><td>101-33</td></tr>
</tbody></table></div>
<div class="sub2">預售屋兩個高頻點</div>
<ul class="pl">
<li><b>履約擔保四種方式</b>：不動產<b class="k">開發信託</b>、<b class="k">價金信託</b>、<b class="k">價金返還保證</b>、<b class="k">同業連帶擔保</b>（113-8）。不動產開發信託＝建商將<b>建案土地及資金</b>信託予金融機構或經許可之信託業者，依<b>工程進度專款專用</b>；簽約時賣方應提供<b>信託證明文件</b>。</li>
<li><b>管線費用</b>：接通自來水、電力之管線費及其相關費用（安裝、配置、設計費等），依公告規定之負擔方式記載（113-20）。</li>
</ul>
<p style="font-size:13.5px;margin-top:8px">※ 四份公告的完整架構、不得記載矩陣、逐項數字，見《<a href="@@YJ@@" style="color:var(--pri);font-weight:700">應記載與不得記載總整理</a>》；斡旋金／要約書的「不得記載」在<b class="k">要約書附件</b>而非委託銷售契約本體（委託銷售契約本體只有 5 項不得記載事項），那一頁有完整說明。</p>
<div class="tr"><b>考試陷阱：</b>①「價格空白＝<b class="k">契約無效</b>」是唯一一個導向無效的，其餘都是「不得收」或「得終止」。②審閱期：委託銷售 <b>3 日</b>、買賣 <b>5 日</b>，別互換。③斡旋金相關的「不得記載」條款位置（要約書附件 vs 契約本體）是 109-17、103-39 的切點。</div>
'''.replace('@@YJ@@',YJ))

sec('d6', 'H', '⑥ 延伸：通訊交易・訪問交易・分期付款', '消保§18、§19、§19-2、§21', '''
<ol class="flow">
<li><b>兩種特種交易的定義</b>：<b class="k">通訊交易</b>＝企業經營者以廣播、電視、電話、傳真、型錄、報紙、雜誌、網際網路、傳單或其他類似方法，消費者<b class="k">於未能檢視商品或服務下</b>而訂立之契約；<b class="k">訪問交易</b>＝企業經營者<b class="k">未經邀約</b>而與消費者在其<b>住居所、工作場所、公共場所或其他場所</b>所訂立之契約（<span class="law">§2⑩⑪</span>）。</li>
<li><b>七日解除權</b>：消費者得於<b class="k">收受商品或接受服務後 7 日內</b>，以<b>退回商品或書面通知</b>方式解除契約，<b class="k">無須說明理由及負擔任何費用或對價</b>；但通訊交易有<b>合理例外情事</b>者不在此限（例外由<b class="k">行政院</b>定之）（<span class="law">§19Ⅰ、Ⅱ</span>）。</li>
<li><b>未告知解除權→期間後延</b>：企業經營者未依 §18Ⅰ③ 提供解除契約相關資訊者，7 日期間<b class="k">自提供之次日起算</b>；但自 §19Ⅰ 的 7 日期間起算<b class="k">已逾 4 個月者，解除權消滅</b>（<span class="law">§19Ⅲ</span>）。</li>
<li><b>發信主義</b>：消費者於期間內<b class="k">已交運商品或發出書面</b>者，<b class="k">契約視為解除</b>（<span class="law">§19Ⅳ</span>）。違反本條所為之約定，<b class="k">其約定無效</b>（§19Ⅴ）。檢查之必要或不可歸責於自己之事由致商品毀損滅失變更者，<b class="k">解除權不消滅</b>（<span class="law">細則§17</span>）；收受商品或接受服務<b>前</b>也可以書面解除（<span class="law">細則§18</span>）。</li>
<li><b>解除後的兩個 15 日</b>：以書面通知解除者，企業經營者應於<b class="k">收到通知之次日起 15 日內</b>至原交付處所或約定處所<b>取回商品</b>；應於<b class="k">取回商品、收到退回商品或解除服務契約通知之次日起 15 日內</b>，<b>返還已支付之對價</b>。回復原狀之約定較民法§259 不利於消費者者，<b class="k">無效</b>（<span class="law">§19-2</span>）。</li>
<li><b>分期付款</b>：應以<b class="k">書面</b>為之，載明①<b>頭期款</b>②各期價款與其他附加費用合計之<b>總價款與現金交易價格之差額</b>③<b>利率</b>。未記載利率者，<b class="k">按現金交易價格週年利率 5% 計算</b>；違反①②者，消費者<b class="k">不負現金交易價格以外價款之給付義務</b>（<span class="law">§21</span>）。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>「<b>7 日猶豫、4 個月上限、兩個 15 日、利率 5%</b>」。</div>
<div class="tr"><b>考試陷阱：</b>①七日起算點是「<b class="k">收受商品或接受服務後</b>」，不是「訂約後」。②訪問交易的關鍵字是「<b class="k">未經邀約</b>」——消費者自己打電話請業務到家就不是訪問交易。③「<b class="k">無須說明理由及負擔任何費用或對價</b>」整句都是法條，少掉「或對價」就不完整。④逾 4 個月解除權消滅的「4 個月」起算是<b>自 §19Ⅰ 的 7 日期間起算</b>。⑤分期付款未載利率是按<b class="k">現金交易價格</b>週年利率 5%，不是法定利率 5% 的民法 §203——數字一樣但基準不同。</div>
''')

FIL = '<button class="on" data-g="all">全部 %d</button>' % len(QD) + ''.join(
    '<button data-g="%s">%s %d</button>' % (g, GRP[g], len([x for x in QD if x['gr'] == g])) for g in ['H1', 'D2', 'D3'])
sec('tq','H','⑦ 考古題：D 篇＋H1 篇 '+str(len(QD))+' 題', str(len(QD))+' 題', '''
<p style="font-size:13px;color:var(--muted)">H1 消保法定型化規範 23 題、D2 預售屋契約 5 題、D3 委託銷售契約 9 題，本篇全收。作答後顯示逐選項解析；右上角可跳到《法條解析練習》同一題標錯誤類型。</p>
<div class="fil" id="fil">@@FIL@@</div>
<div class="score" id="score"></div>
<div id="qlist"></div>
'''.replace('@@FIL@@',FIL), open_=True)

BODY = '\n\n'.join(S)
NAV = ('<nav><a href="#d0">⓪ 四層結構</a><a href="#d1">① 三個定義</a><a href="#d2">② 審閱期</a>'
       '<a href="#d3">③ 無效 vs 不構成</a><a href="#d4">④ 應記載／不得記載</a><a href="#d5">⑤ 三份契約空白</a>'
       '<a href="#d6">⑥ 特種交易</a><a href="#tq">⑦ 考古題</a></nav>')

SCRIPT = re.search(r'<script>\nvar QUIZ=[\s\S]*?\n</script>', SRC).group(0)
SCRIPT = re.sub(r'var QD=\[[\s\S]*?\];\n', 'var QD=' + json.dumps(QD, ensure_ascii=False, separators=(',', ':')) + ';\n', SCRIPT, count=1)

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>定型化契約專區</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s</style></head><body>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規概要｜定型化契約專區</h1><div class="sub">消保法這一層：四層結構・三個定義・審閱期・無效 vs 不構成・應記載不得記載效果・特種交易｜考古 %d 題</div></header>
%s
<main>
<div class="intro"><b>怎麼讀：</b>本頁專攻<b>消費者保護法</b>對定型化契約的規範，核心是 ③「<b>無效</b> vs <b>不構成契約之內容</b>」那張對照表——H1 篇幾乎每年都從那裡出題。內政部四份公告的<b>逐項內容</b>在《應記載與不得記載總整理》，本頁只處理<b>法律效果</b>，兩頁互補。條文依全國法規資料庫現行條文逐字；口訣標〔自編〕。</div>
<div class="tools"><button id="ea">全部展開</button><button id="ca">全部收合</button></div>

%s

<p class="foot">本頁為備考整理，非法規原文。條文來源：消費者保護法及其施行細則（全國法規資料庫現行條文）、內政部公告之不動產定型化契約應記載及不得記載事項。考前以紙本六法為準。</p>
</main>
%s
%s
</body></html>''' % (CSS, len(QD), NAV, BODY, SCRIPT, FAB)

dst = ROOT + '/經紀法規_定型化契約專區.html'
io.open(dst, 'w', encoding='utf-8').write(HTML)
print('已產生 經紀法規_定型化契約專區.html', len(HTML) // 1024, 'KB｜考古題', len(QD), '題')
