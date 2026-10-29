# -*- coding: utf-8 -*-
"""《經紀法規_應記載不得記載總整理》版型 B：四份公告並排為主軸。

新增一節「同一件事，四份公告怎麼寫」，放在第一節總覽之後，成為全頁主軸：
橫軸＝說明書／成屋買賣／預售屋買賣／委託銷售，縱軸＝考試會拿來互相比的項目。
原本的細節節（說明書架構、不得記載矩陣、三份契約數字、數字反向索引）全部保留，
矩陣只放「誰有、數字多少」，細節仍在原節——所以不是兩份手寫稿，數字的單一來源是本檔的 ROWS。

⚠️ 既有的「不得記載事項」矩陣（第四節）本來就是四份並排，不重做，本節只放**應記載／內容面**。
可重複執行。節號由 add_numidx.py 統一重排（執行順序：add_grid.py → add_numidx.py）。
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, '經紀法規_應記載不得記載總整理.html')

X = '—'
# (項目, 說明書, 成屋買賣, 預售屋買賣, 委託銷售, 備註／陷阱)
ROWS = [
 ('審閱期', X, '至少 <b>5 日</b>', '至少 <b>5 日</b>', '不得少於 <b>3 日</b><small>（含要約書附件）</small>',
  '說明書沒有審閱期；<b>3 日 vs 5 日</b>是最常考的一組。委託銷售約定剛好 3 日合法。'),
 ('違約金', X, '房地總價款 <b>15%</b> 為<b>上限</b>', '賣方賠償<b>不得低於</b> 15%；買方沒收<b>最高不超過</b> 15%',
  X, '<span class="gh">方向相反</span>：成屋是天花板、預售屋是地板。'),
 ('遲延利息', X, '賣方違約、遲延交屋：每日<b>萬分之二</b>', '買方逾期付款：萬分之二；賣方逾期開工／取照／通知交屋：<b>萬分之五</b>',
  X, '同一份契約裡買賣雙方利率不同，只有預售屋。'),
 ('買方違約解約', X, '逾期 5 日起算息；逾期 <b>1 個月</b>且<b>催告 7 日</b>仍未付 → 解約沒收（15% 為限）',
  X, X, '只有成屋契約把解約門檻寫死。'),
 ('面積誤差找補', X, X, '不足賣方<b>全部</b>找補；超過買方最多找補 <b>2%</b>；誤差逾 <b>3%</b> 買方得解約',
  X, '<span class="gh">只有預售屋</span>。'),
 ('保固', X, X, '結構 <b>15 年</b>；固定建材及設備 <b>1 年</b>', X, '<span class="gh">只有預售屋</span>。'),
 ('付款間隔', X, X, '每次間隔 <b>20 日以上</b>', X, '<span class="gh">只有預售屋</span>。'),
 ('登記與交屋期限', X, X, '使照核發後 <b>4 個月</b>內辦移轉登記；領照後 <b>6 個月</b>內通知交屋',
  X, '4 個月和 6 個月容易對調。'),
 ('管線費', X, X, '自來水、電力管線費及相關費用由<b>賣方</b>負擔', X, '考古題 113-20。'),
 ('稅費分擔', X, '土增稅<b>賣方</b>；契稅、印花稅、登記規費、保險費<b>買方</b>', X, X,
  '只有成屋契約逐項列。'),
 ('履約擔保', '預售屋部分應記載「各期價金之<b>履約保證機制</b>方式」', X,
  '五選一：不動產開發信託、價金返還保證、價金信託、同業連帶擔保、公會連帶保證協定', X,
  '說明書要「寫出用哪一種」，契約才是「有哪五種」。考古題 113-8。'),
 ('約定專用', X, X, '規約草約訂定者，<b>非屬避難之屋頂平臺</b>得為約定專用', X, '考古題 103-12。'),
 ('空白欄沒填的效果', X, X, X,
  '價格空白 → 契約<b>無效</b>；期間空白 → 得<b>隨時書面終止</b>；報酬空白 → <b>不得收取</b>；沒收定金比例空白 → <b>不得請求</b>',
  '<span class="gh">只有委託銷售</span>，而且四個效果各不相同——空白欄裡<b>只有價格是無效</b>。'),
 ('時限義務', X, X, X,
  '簽約前提供近 <b>3 個月</b>成交行情；收到要約書 <b>24 小時</b>內轉交；收受定金 <b>24 小時</b>內送交（無法送交 <b>2 日</b>內書面通知）',
  '<span class="gh">只有委託銷售</span>。'),
 ('附件', '建物現況確認書<b>不得替代</b>說明書', '建物現況確認書（<b>賣方</b>填寫）',
  '廣告宣傳品、建材設備表、平面圖<b>為契約之一部分</b>', '<b>要約書</b>（審閱期不少於 3 日、7 項應記載）',
  '同一份現況確認書，說明書那邊是「不得替代」，成屋那邊是「附件」。'),
 ('周邊環境／嫌惡設施', '成屋：周邊重要環境設施半徑 <b>300 公尺</b>；預售屋：最近 <b>5 年</b>內 300 公尺水災淹水救助紀錄',
  X, X, X, '<span class="gh">只有說明書</span>有揭露義務。'),
 ('應記載架構', '土地 <b>7 大項</b>；成屋、預售屋各 <b>4 大項</b>', X, X, X,
  '預售屋架構與成屋相同，多出工程進度、規約草約等。'),
 ('不得記載：四份都有的三項', '僅供參考、繳回、面積名詞', '僅供參考、繳回、面積名詞',
  '僅供參考、繳回、面積名詞', '僅供參考、繳回、面積名詞',
  '口訣<b>參、繳、面</b>；其餘是專屬項目，詳見「不得記載事項」那一節。'),
 ('誰訂', '內政部擬定，報<b>行政院</b>核定公告<small>（114-11 官方答案）</small>', '依<b>消保法§17</b> 由中央主管機關擬訂公告',
  '依<b>消保法§17</b>', '依<b>消保法§17</b>',
  '⚠️ 經紀業條例 §22Ⅲ 條文只寫「由中央主管機關定之」，問條文怎麼寫時答這句。'),
 ('本站考古題', '13 題', '0 題', '5 題', '9 題', '說明書最多，成屋契約本身一題都沒考過。'),
]

CSS = """<style id="grid-css">
/* 版型 B：四份公告並排主軸 */
.gdw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:6px}
table.gd{border-collapse:collapse;width:100%;font-size:.84rem;min-width:760px}
table.gd th,table.gd td{border:1px solid var(--line);padding:7px 8px;vertical-align:top;line-height:1.6}
table.gd thead th{position:sticky;top:0;z-index:1;font-size:.78rem;letter-spacing:.03em;color:#fff}
table.gd thead th.it{background:var(--muted)}
table.gd thead th.c1{background:var(--purple)}
table.gd thead th.c2{background:var(--pri)}
table.gd thead th.c3{background:var(--orange)}
table.gd thead th.c4{background:var(--gold)}
table.gd td.it{font-weight:700;white-space:nowrap;background:var(--paper-dark);color:var(--ink)}
table.gd td.no{text-align:center;color:var(--muted);background:var(--paper2)}
table.gd td.nt{font-size:.8rem;color:var(--muted);background:var(--paper2)}
table.gd .gh{color:var(--vermillion);font-weight:800}
table.gd b{color:var(--numfg);background:var(--numbg);border-radius:4px;padding:0 3px}
@media(max-width:700px){
  table.gd{min-width:0;border:0}
  table.gd thead{display:none}
  table.gd tr{display:block;border:1px solid var(--line);border-radius:10px;margin-bottom:10px;overflow:hidden}
  table.gd td{display:block;border:0;border-top:1px solid var(--line)}
  table.gd td.it{border-top:0;font-size:.92rem;padding:8px 10px}
  table.gd td.no{display:none}
  table.gd td[data-c]::before{content:attr(data-c);display:block;font-size:.72rem;font-weight:700;
    letter-spacing:.04em;color:var(--muted);margin-bottom:2px}
  table.gd td.nt::before{content:"要注意"}
}
</style>"""

HEAD = [('說明書', 'c1'), ('成屋買賣契約', 'c2'), ('預售屋買賣契約', 'c3'), ('委託銷售契約', 'c4')]


def section():
    tr = ''
    for it, a, b, c, d, note in ROWS:
        tds = ''
        for (nm, _), v in zip(HEAD, (a, b, c, d)):
            cls = 'no' if v == X else ''
            tds += '<td class="%s" data-c="%s">%s</td>' % (cls, nm, v)
        tr += ('<tr><td class="it" data-c="項目">%s</td>%s<td class="nt" data-c="要注意">%s</td></tr>'
               % (it, tds, note))
    ths = ''.join('<th class="%s">%s</th>' % (c, n) for n, c in HEAD)
    return (
      '<details class="sc must" id="s0b"><summary><span class="n2">二</span>'
      '<div class="t2"><h2>同一件事，四份公告怎麼寫</h2>'
      '<small>橫著看，一眼比出四份的差別</small>'
      '<span class="dat">__N__ 個比得起來的項目</span></div>'
      '<span class="tg2">必背</span><span class="ar">▸</span></summary>'
      '<div class="sb"><div class="hlnote">這張是全頁主軸：考古題最愛問「<b>這一項是哪一份的</b>」。'
      '「—」＝那份公告沒有這一項；<span class="gh">紅字</span>＝只有一份有，或兩份方向相反。'
      '條號、完整敘述與考古題連結在後面各節，這裡只放「誰有、數字多少」。</div>'
      '<div class="gdw"><table class="gd"><thead><tr><th class="it">項目</th>__THS__<th class="it">要注意</th></tr></thead>'
      '<tbody>__TR__</tbody></table></div>'
      '<div class="hlnote" style="margin-top:8px">⚠️ 這張表只放<b>應記載／內容面</b>。'
      '「不得記載事項」的四份並排矩陣在後面單獨一節，不在這裡重複。</div>'
      '</div></details>')\
      .replace('__N__', str(len(ROWS))).replace('__THS__', ths).replace('__TR__', tr)


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    s = re.sub(r'<style id="grid-css">.*?</style>', '', s, flags=re.S)
    m = re.search(r'<details class="sc[^"]*" id="s0b">', s)
    if m:
        d, k = 0, m.end()
        while True:
            x, y = s.find('<details', k), s.find('</details>', k)
            if 0 <= x < y:
                d += 1; k = x + 8
            else:
                if d == 0:
                    end = y + 10; break
                d -= 1; k = y + 10
        s = s[:m.start()] + s[end:]
    s = s.replace('<a href="#s0b">四份並排</a>', '')

    a = s.index('<details class="sc must" id="s1">')
    g = s.rfind('<div class="grp2">', 0, a)
    if g > 0 and a - g < 200:
        a = g
    s = s[:a] + section() + s[a:]
    s = s.replace('<a href="#s1">說明書</a>', '<a href="#s0b">四份並排</a><a href="#s1">說明書</a>', 1)
    s = s.replace('</style>', '</style>\n' + CSS, 1)
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('版型 B 已套用：四份公告並排主軸 %d 列（節號請再跑 add_numidx.py 重排）' % len(ROWS))


if __name__ == '__main__':
    main()
