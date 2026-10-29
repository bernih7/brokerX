# -*- coding: utf-8 -*-
"""《經紀法規_應記載不得記載總整理》版型 A：

① 新增一節「數字 → 屬於誰」反向索引（插在第四節「三份契約：數字一次看」之後，成為第五節）。
② 顏色統一：原本 t1–t4 在第二節是「土地／成屋／預售屋」的順序分隔（t2 還一色兩用），
   在第四節卻是「成屋／預售屋／委託銷售」的固定歸屬——同一個顏色在不同節代表不同東西。
   改成全頁一義：成屋 t1、預售屋 t2、委託銷售 t3、土地 tl、連動考點 pe，並在導覽列下方加圖例。
③ 導覽列加「數字索引」錨點，後面各節的國字編號跟著後移。

資料全部來自該頁第二、四節既有內容，沒有新增任何事實。可重複執行。
"""
import io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, '經紀法規_應記載不得記載總整理.html')

# 節 id → 國字編號（插入新節後的順序）
NUM = {'s0': '一', 's1': '二', 's2': '三', 's3': '四', 's3b': '五',
       's4': '六', 's5': '七', 's6': '八', 's7': '九', 's8': '十'}

CSS = """<style id="numidx-css">
/* 版型 A：顏色全頁一義 + 數字反向索引 */
.r.tl{border-left-color:var(--blue)}
.lgd{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;margin:6px 0 2px;font-size:.78rem;color:var(--muted)}
.lgd i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.lgd span{white-space:nowrap}
.nxw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:6px}
table.nx{border-collapse:collapse;width:100%;font-size:.86rem;min-width:520px}
table.nx th,table.nx td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
table.nx th{font-size:.74rem;color:var(--muted);font-weight:700;letter-spacing:.04em;white-space:nowrap}
table.nx td.nv{font-family:"Noto Serif TC",serif;font-weight:800;white-space:nowrap;
  color:var(--numfg);background:var(--numbg);border-radius:6px;font-variant-numeric:tabular-nums}
.own{display:inline-block;font-size:.74rem;font-weight:700;padding:1px 7px;border-radius:999px;margin:1px 3px 1px 0;white-space:nowrap;color:#fff}
.own.o-l{background:var(--blue)}.own.o-c{background:var(--pri)}
.own.o-p{background:var(--orange)}.own.o-w{background:var(--gold)}
.own.o-d{background:var(--purple)}
.nxhot{color:var(--vermillion);font-weight:800}
@media(max-width:620px){
  table.nx{min-width:0}
  table.nx thead{display:none}
  table.nx tr{display:block;border-bottom:1px solid var(--line);padding:7px 0}
  table.nx td{display:block;border:0;padding:2px 0}
  table.nx td.nv{display:inline-block;padding:1px 9px}
}
</style>"""

ROWS = [
 ('3 日', [('o-w', '委託銷售')],
  '契約及附件審閱期<b class="hl">不得少於 3 日</b>（要約書同）。約定剛好 3 日合法'),
 ('5 日', [('o-p', '預售屋'), ('o-c', '成屋')],
  '買方攜回審閱<b class="hl">至少 5 日</b>，不得拋棄'),
 ('24 小時', [('o-w', '委託銷售')],
  '受託人收到要約書／定金，<b class="hl">24 小時內</b>轉交、送交委託人'),
 ('2 日', [('o-w', '委託銷售')],
  '定金無法送交時，<b class="hl">2 日內</b>書面通知'),
 ('7 日', [('o-c', '成屋')],
  '買方逾期 1 個月且經<b class="hl">催告 7 日</b>仍未付 → 賣方得解約'),
 ('20 日', [('o-p', '預售屋')],
  '每次付款間隔<b class="hl">20 日以上</b>'),
 ('3 個月', [('o-w', '委託銷售')],
  '受託人簽約前應據實提供<b class="hl">近 3 個月</b>成交行情'),
 ('4 個月', [('o-p', '預售屋')],
  '使用執照核發後<b class="hl">4 個月內</b>備妥文件辦移轉登記'),
 ('6 個月', [('o-p', '預售屋')],
  '領得使用執照後<b class="hl">6 個月內</b>通知交屋'),
 ('15 年', [('o-p', '預售屋')],
  '結構部分保固<b class="hl">15 年</b>；固定建材及設備 1 年'),
 ('萬分之二', [('o-c', '成屋'), ('o-p', '預售屋')],
  '成屋：賣方違約、遲延交屋；預售屋：買方逾期付款'),
 ('萬分之五', [('o-p', '預售屋')],
  '預售屋賣方逾期開工、取照、通知交屋'),
 ('15 %', [('o-c', '成屋'), ('o-p', '預售屋')],
  '<span class="nxhot">方向相反</span>：成屋是違約金<b class="hl">上限</b>；'
  '預售屋賣方違約賠償<b class="hl">不得低於</b> 15%、買方沒收<b class="hl">最高不超過</b> 15%'),
 ('2 % / 3 %', [('o-p', '預售屋')],
  '面積誤差：不足賣方全部找補、超過買方最多找補 <b class="hl">2%</b>；誤差超過 <b class="hl">3%</b> 買方得解約'),
 ('50 %', [('o-w', '委託銷售')],
  '買方違約定金被沒收，給受託人<b class="hl">不得逾定金 50%</b>，且不得逾約定報酬'),
 ('300 公尺', [('o-d', '說明書')],
  '成屋：周邊重要環境設施半徑 <b class="hl">300 公尺</b>；預售屋：水災淹水救助紀錄 300 公尺'),
 ('5 年', [('o-d', '說明書')],
  '預售屋部分：<b class="hl">最近 5 年內</b>基地周邊有無水災淹水救助紀錄'),
 ('8 項', [('o-l', '土地'), ('o-d', '說明書')],
  '土地（素地）「使用管制內容」的 <b class="hl">8 項</b>特殊管制'),
 ('7 大項 / 4 大項', [('o-d', '說明書')],
  '土地 <b class="hl">7 大項</b>；成屋、預售屋各 <b class="hl">4 大項</b>'),
]

LEGEND = ('<div class="lgd"><b style="color:var(--ink)">顏色＝哪一份：</b>'
          '<span><i style="background:var(--blue)"></i>土地</span>'
          '<span><i style="background:var(--pri)"></i>成屋</span>'
          '<span><i style="background:var(--orange)"></i>預售屋</span>'
          '<span><i style="background:var(--gold)"></i>委託銷售</span>'
          '<span><i style="background:var(--purple)"></i>連動考點</span>'
          '<small>（全頁同一套，不再一色兩用）</small></div>')


def section():
    tr = ''
    for num, owners, txt in ROWS:
        ow = ''.join('<span class="own ' + c + '">' + n + '</span>' for c, n in owners)
        tr += '<tr><td class="nv">' + num + '</td><td>' + ow + '</td><td>' + txt + '</td></tr>'
    html = (
      '<details class="sc must" id="s3b"><summary><span class="n2">五</span>'
      '<div class="t2"><h2>數字 → 屬於誰（反向索引）</h2>'
      '<small>考場上先想到數字，再回推是哪一份</small>'
      '<span class="dat">__N__ 組數字，全部出自第二、四節</span></div>'
      '<span class="tg2">必背</span><span class="ar">▸</span></summary>'
      '<div class="sb"><div class="hlnote">用法：看到「5 日」先問<b>是哪一份的 5 日</b>。'
      '這張表把前面兩節散開的數字反過來排，考前掃一遍就知道哪些數字會互相撞。</div>'
      '__LEGEND__'
      '<div class="nxw"><table class="nx"><thead><tr><th>數字</th><th>屬於哪一份</th><th>內容</th></tr></thead>'
      '<tbody>__TR__</tbody></table></div>'
      '<div class="hlnote" style="margin-top:8px">⚠️ 最容易混的三組：'
      '<b>審閱期</b> 成屋／預售屋 5 日、委託銷售 3 日｜'
      '<b>15%</b> 成屋是上限、預售屋是下限（方向相反）｜'
      '<b>萬分之二 vs 萬分之五</b> 預售屋買方逾期是萬分之二、賣方逾期是萬分之五。</div>'
      '</div></details>')
    return html.replace('__N__', str(len(ROWS))).replace('__LEGEND__', LEGEND).replace('__TR__', tr)

def main():
    s = io.open(PAGE, encoding='utf-8').read()

    # 可重複執行：先移除舊的 CSS 區塊與舊的 s3b 節
    s = re.sub(r'<style id="numidx-css">.*?</style>', '', s, flags=re.S)
    m = re.search(r'<details class="sc[^"]*" id="s3b">', s)
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
    s = s.replace('<a href="#s3b">數字索引</a>', '')

    # ② 顏色全頁一義：第二節的列依標題重新上色
    i1 = s.index('id="s1"'); i2 = s.index('id="s2"')
    seg = s[i1:i2]

    def recolor(mm):
        cls = mm.group(1)
        if cls == 'pe':
            return mm.group(0)
        t = ' '.join(re.sub(r'<[^>]+>', ' ', mm.group(2)).split()).lstrip('> ')[:30]
        new = 'tl' if t.startswith('土地') else ('t1' if t.startswith('成屋') else
              ('t2' if '預售屋' in t else cls))
        return mm.group(0).replace('class="r ' + cls + '"', 'class="r ' + new + '"', 1)

    seg2 = re.sub(r'<details class="r (t\d|pe|tl)"([^>]*>\s*<summary[^>]*>.*?</summary>)',
                  recolor, seg, flags=re.S)
    s = s[:i1] + seg2 + s[i2:]

    # 圖例：放在第二節與第四節的 .sb 開頭各一份
    s = re.sub(r'(<div class="lgd">.*?</div>)', '', s, flags=re.S)
    for sid in ('s1', 's3'):
        a = s.index('id="%s"' % sid)
        b = s.index('<div class="sb">', a) + len('<div class="sb">')
        s = s[:b] + LEGEND + s[b:]

    # ① 插入新節
    a = s.index('<details class="sc often" id="s4">')
    # 新節屬「必背」組，要插在「常考」組標籤之前，不然會被歸到常考那一組
    g = s.rfind('<div class="grp2">', 0, a)
    if g > 0 and a - g < 200:
        a = g
    s = s[:a] + section() + s[a:]

    # ③ 導覽列加錨點
    s = s.replace('<a href="#s4">空白效果</a>',
                  '<a href="#s3b">數字索引</a><a href="#s4">空白效果</a>', 1)

    # 各節國字編號重排
    for sid, n in NUM.items():
        s = re.sub(r'(id="%s"><summary><span class="n2">)[^<]*(</span>)' % sid,
                   lambda mm, n=n: mm.group(1) + n + mm.group(2), s)

    # CSS
    s = s.replace('</style>', '</style>\n' + CSS, 1)
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('版型 A 已套用：新增「數字 → 屬於誰」%d 列；第二節重新上色；圖例 2 處；節號重排 %d 節'
          % (len(ROWS), len(NUM)))


if __name__ == '__main__':
    main()
