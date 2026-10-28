# 產生《民法｜申論 115 出題預測》頁：歷屆分布＋輪替＋修法熱點＋範圍覆蓋檢查＋模擬卷涵蓋度
# 資料：cards.json（由 民法_備考指揮中心.html 抽出的 81 張申論卡）、民法*_完整考題小卡.html（選擇題 520 題章節）
import re, json, os, html
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
C = json.load(open(os.path.join(HERE, 'cards.json'), encoding='utf-8'))
TPL = open(os.path.join(ROOT, '土地法申論題_六型答題模板.html'), encoding='utf-8').read()
HEAD = TPL[:TPL.index('<title>')] + '<title>民法申論115預測</title>' + TPL[TPL.index('</title>') + 8:TPL.index('<style>')]
CSS = TPL[TPL.index('<style>') + 7:TPL.index('</style>')]
FAB = TPL[TPL.index('<!--bxfab-->'):TPL.index('<!--/bxfab-->') + len('<!--/bxfab-->')] if '<!--bxfab-->' in TPL else ''
FAB = FAB.replace('%E5%9C%9F%E5%9C%B0%E6%B3%95_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html', '%E6%B0%91%E6%B3%95_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html').replace('土地法_備考指揮中心.html', '民法_備考指揮中心.html')  # 首頁鈕指向民法指揮中心
HUB = '民法_備考指揮中心.html'
CN = '一二'
def key(c):
    if c['pred']: return '預' + c['ek'].replace('預測題', '').strip()
    m = re.match(r'(\d+)年第(.)題', c['ek']); return f'{m.group(1)}-{m.group(2)}'
for c in C: c['k'] = key(c)
BY = {c['k']: c for c in C}
GN = {'g1': '共有・分管・區分所有', 'g2': '抵押權・地上權・物權順序', 'g3': '無權處分・善意取得・登記公信', 'g4': '居間・委任・買賣・租賃', 'g5': '意思表示・行為能力・債總', 'g6': '時效・相鄰・繼承'}
def link(k):
    c = BY[k]
    return f'<a class="ek" href="{HUB}#essay={html.escape(k)}" title="{html.escape(c["et"])}">{k}</a>'
off = [c for c in C if not c['pred']]
assert len(off) == 32
yr = lambda c: int(c['k'].split('-')[0])
yrs = sorted({yr(c) for c in off})
rows = ''
for y in yrs:
    es = sorted([c for c in off if yr(c) == y], key=lambda c: CN.index(c['k'][-1]))
    rows += f'<tr><th>{y}</th>' + ''.join(f'<td><span class="gb">{c["g"][1]}</span>{link(c["k"])}<small>{html.escape(c["et"][:30])}</small></td>' for c in es) + '</tr>'
tot = Counter(c['g'] for c in off); r5 = Counter(c['g'] for c in off if yr(c) >= 110)
last = {g: max(yr(c) for c in off if c['g'] == g) for g in tot}
gtab = ''.join(f'<tr><td><span class="gb">{g[1]}</span>{GN[g]}</td><td>{tot[g]}</td><td>{r5[g]}</td><td>{last[g]}</td><td>{114 - last[g]}</td></tr>' for g in sorted(tot, key=lambda g: (-tot[g], g)))
# 物權（D）出現年數
DYRS = [99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 114]
# 選擇題章節
qt = Counter(); q5 = Counter()
for L in ['A', 'BC', 'D', 'E']:
    s = open(os.path.join(ROOT, f'民法{L}_完整考題小卡.html'), encoding='utf-8').read()
    for m in re.finditer(r'"id": "[A-Z]+(\d+)-\d+", "cat": "([^"]+)"', s):
        qt[m.group(2)] += 1
        if int(m.group(1)) >= 110: q5[m.group(2)] += 1
assert sum(qt.values()) == 520
ORDER = [('A 總則', ['自然人', '法人', '物', '法律行為效力', '意思表示瑕疵', '代理', '消滅時效除斥期間']),
         ('B 債編總論', ['B1債之發生與消滅', 'B2債務不履行', 'B3連帶債務與保證', 'B4不當得利', 'B5無因管理', 'B6侵權行為']),
         ('C 債編分則', ['C1買賣', 'C2租賃', 'C3居間承攬委任', 'C4其他各種之債', 'C5債權讓與']),
         ('D 物權', ['D1物概念孳息從物', 'D2所有權共有登記', 'D3拾得遺失添附', 'D4相鄰通行', 'D5地上權農育役權典權', 'D6抵押質權占有']),
         ('E 親屬繼承', ['E1婚約婚姻結婚', 'E2夫妻財產制', 'E3親子收養監護', 'E4繼承遺囑'])]
assert sorted(sum([v for _, v in ORDER], [])) == sorted(qt)
MAP = {'自然人': ['106-二', '預38'], '法人': ['預44'], '物': ['預45'], '法律行為效力': ['103-一', '101-一', '預38'],
       '意思表示瑕疵': ['99-一', '103-一', '110-二', '預05', '預26'], '代理': ['111-一', '預23', '預27', '預31', '預39'],
       '消滅時效除斥期間': ['105-一', '107-二', '預09'],
       'B1債之發生與消滅': ['100-一', '101-一', '預16', '預32'], 'B2債務不履行': ['113-一', '預15', '預25', '預43'], 'B3連帶債務與保證': ['106-一', '預36'],
       'B4不當得利': ['103-一', '111-一'], 'B5無因管理': ['預46'], 'B6侵權行為': ['113-一', '預33', '預42'],
       'C1買賣': ['106-二', '112-一', '113-一', '預10', '預16', '預17', '預18', '預32'], 'C2租賃': ['101-二', '102-一', '106-一', '預11', '預19', '預24'],
       'C3居間承攬委任': ['104-一', '112-二', '113-二', '預08', '預13', '預14', '預30', '預31'], 'C4其他各種之債': ['預47'], 'C5債權讓與': ['預07'],
       'D1物概念孳息從物': ['預35'], 'D2所有權共有登記': ['114-一', '110-一', '106-一', '105-二', '103-二', '102-一', '100-二', '預02', '預03', '預12', '預20', '預21'],
       'D3拾得遺失添附': ['預48'], 'D4相鄰通行': ['111-二', '預33', '預34'], 'D5地上權農育役權典權': ['104-二', '109-二', '101-二', '預37', '預40'],
       'D6抵押質權占有': ['99-一', '102-二', '103-二', '105-一', '108-二', '114-二', '預01', '預07', '預24', '預22', '預35'],
       'E1婚約婚姻結婚': ['預49'], 'E2夫妻財產制': ['109-一', '預06', '預41'], 'E3親子收養監護': ['99-二'], 'E4繼承遺囑': ['99-二', '101-一', '102-二', '110-二', '預04', '預29']}
assert all(k in BY for v in MAP.values() for k in v), [k for v in MAP.values() for k in v if k not in BY]
NAME = {'自然人': '自然人（能力・死亡宣告）', '法人': '法人', '物': '物（總則）', '法律行為效力': '法律行為之效力', '意思表示瑕疵': '意思表示瑕疵', '代理': '代理', '消滅時效除斥期間': '消滅時效・除斥期間'}
MOCK = {'意思表示瑕疵': '模一①', 'C3居間承攬委任': '模一②', 'D6抵押質權占有': '模二①', 'D5地上權農育役權典權': '模二①', 'E2夫妻財產制': '模二②', 'D2所有權共有登記': '來勝②', 'C1買賣': '來勝①', 'B2債務不履行': '來勝①'}
crow = ''
for sec, cats in ORDER:
    crow += f'<tr class="sec"><td colspan="5">{sec}</td></tr>'
    for c in cats:
        ks = MAP[c]; noff = sum(1 for k in ks if not BY[k]['pred'])
        flag = '<b class="gap">沒有任何範文</b>' if not ks else ('<b class="gap2">官方沒考過</b>' if noff == 0 else '')
        crow += f'<tr><td>{html.escape(NAME.get(c, c[2:]))}</td><td>{qt[c]}</td><td>{q5[c]}</td><td>{MOCK.get(c, "－")}</td><td>{"".join(link(k) for k in ks)} {flag}</td></tr>'
PRED = [
 ('物權題', '高', '共有：管理（多數決・分管）、處分、分割與抵押權移存', '16 年考 7 次、近 5 年 2 次（110、114），平均 2～3 年一次，是民法申論第一主角；選擇題「所有權・共有・登記」48 題、近 5 年 10 題。換角度再考（優先承購、分割方法、補償金抵押權、分管對受讓人效力）的機率最高。', ['114-一', '110-一', '103-二', '預02', '預03', '預20', '預21']),
 ('物權題', '高', '抵押權與用益物權：法定地上權、併付拍賣、最高限額、地上權消滅', '16 年考 5 次；114 剛考物權優先順序。§876 法定地上權、§877 併付拍賣官方申論從未正面考過（104 考的是§866），選擇題「抵押・質權・占有」43 題。', ['114-二', '108-二', '104-二', '預01', '預24', '預07', '預40']),
 ('總則・債總題', '高', '意思表示瑕疵・行為能力・債務不履行（第 5 組 107 年後 7 屆沒考）', '第 5 組（行為能力・債總）16 年考 5 次，最後一次是 107 年，已隔 7 屆，是全部主題中空最久的（意思表示瑕疵本身 110-二 考過通謀虛偽，分在第 3 組）；112.1.1 起 18 歲成年（106-二 依舊法 20 歲作答），修法後尚未入題。選擇題「自然人」近 5 年 12 題，升溫明顯。', ['103-一', '106-二', '107-一', '預38', '預26', '預25', '預15']),
 ('物權題', '高', '無權處分・善意取得・登記公信力', '16 年考 5 次（99、108、109、110、111），111 後已 3 屆沒考；借名登記（106 年度第 3 次民事庭會議）、通謀虛偽、§759-1 是近 10 年最常見的連結點。', ['110-二', '108-一', '109-一', '99-一', '預05', '預29', '預22']),
 ('債各題', '中', '居間・委任・買賣・租賃（經紀業核心契約）', '112、113 連兩年都考（居間報酬 112-二、113-二；瑕疵擔保 113-一），114 沒考；剛密集考過，連第三年的機率較低，但居間報酬（成立時點、§571 喪失報酬）仍是本科特色題，不可放。', ['113-二', '112-二', '104-一', '113-一', '預14', '預16', '預19']),
 ('物權・親繼題', '中', '時效・相鄰關係', '消滅時效 105、107；相鄰 111；時效取得地上權 109。§796-1、袋地通行（§787～§789）官方只考過一次。', ['105-一', '107-二', '111-二', '109-二', '預33', '預34', '預09']),
 ('親繼題', '中', '繼承・夫妻財產制', '選擇題最大章「繼承・遺囑」64 題、近 5 年 19 題，但申論純繼承只考過 99 年一次，夫妻財產制只在 109-一 出現；特留分 115.8.17 修正（刪除兄弟姊妹）尚未施行，115 年考試仍適用舊法。', ['99-二', '109-一', '預04', '預06', '預41']),
]
prow = ''.join(f'<div class="pc p{lv}"><div class="ph"><span class="pt">{side}</span><span class="pl">{lv}</span><b>{html.escape(t)}</b></div><p>{html.escape(why)}</p><p class="pk">讀這幾題：{"".join(link(k) for k in ks)}</p></div>' for side, lv, t, why, ks in PRED)
MOCKROWS = [('模擬試題一 申論一', '通謀虛偽＋善意第三人、甲對乙之權利', '無權處分・善意取得（高）'),
            ('模擬試題一 申論二', '居間報酬：停止條件、§571 喪失報酬', '居間・委任（中）'),
            ('模擬試題二 申論一', '§876 法定地上權、§877 併付拍賣', '抵押權與用益物權（高）'),
            ('模擬試題二 申論二', '剩餘財產分配、§1030-3 追加計算', '繼承・夫妻財產制（中）'),
            ('<a href="民法_來勝模擬試題一.html">來勝模擬(一)</a> 申論一', '二重買賣（共有應有部分）：登記決定歸屬、§226 給付不能、§249③ 定金加倍', '無權處分・善意取得／債務不履行'),
            ('<a href="民法_來勝模擬試題一.html">來勝模擬(一)</a> 申論二', '應有部分設定抵押＋裁判分割後移存（§819Ⅰ、§824-1Ⅱ③、§873）', '共有（高）')]
mrow = ''.join(f'<tr><td>{a}</td><td>{html.escape(b)}</td><td>{c}</td></tr>' for a, b, c in MOCKROWS)
X = '''
.blk{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 14px 10px}
.blk h2{font:700 17px/1.4 "Noto Serif TC",serif;color:var(--pri);margin:0 0 8px}
.blk p{margin:6px 0}.note{font-size:13px;color:var(--muted)}
.tw{overflow-x:auto;margin:6px -4px}.tw table{border-collapse:collapse;width:100%;min-width:520px;font-size:13.5px}
.tw th,.tw td{border-bottom:1px solid var(--line);padding:6px 6px;text-align:left;vertical-align:top}.tw thead th{color:var(--muted);font-weight:500;font-size:12.5px}
.tw td small{display:block;color:var(--muted);font-size:12px;line-height:1.45}.tw td:nth-child(n+2){font-variant-numeric:tabular-nums}
.tw tr.sec td{font-weight:700;color:var(--pri);background:var(--tint);border-bottom:0}
.gb{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:6px;background:var(--pri);color:var(--onpri);font-size:12px;font-weight:700;margin-right:6px}
.ek{display:inline-block;font-size:12.5px;padding:1px 8px;margin:2px 4px 2px 0;border-radius:99px;border:1px solid var(--line);color:var(--pri);text-decoration:none;background:var(--tint)}
.gap{color:var(--red);font-size:12px}.gap2{color:var(--muted);font-size:12px;font-weight:500}
.one{background:var(--pri);color:var(--onpri);border-radius:14px;padding:14px}.one b{font:700 16px/1.5 "Noto Serif TC",serif;display:block;margin-bottom:6px}.one p{margin:4px 0;font-size:14px}
.one a{color:var(--onpri)}
.pc{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0;background:var(--bg)}
.ph{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}.ph b{font:700 15px/1.45 "Noto Serif TC",serif;flex:1 1 100%}
.pt{font-size:12px;color:var(--muted)}.pl{font-size:12px;font-weight:700;padding:0 8px;border-radius:99px;background:var(--line)}
.p高 .pl{background:var(--b4s);color:var(--b4);border:1px solid var(--b4l)}.p中 .pl{background:var(--b3s);color:var(--b3);border:1px solid var(--b3l)}
.pc p{margin:4px 0;font-size:14px}.pk{font-size:13px}
ol.st{margin:4px 0;padding-left:20px}ol.st li{margin:3px 0}
.grpl{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:4px 12px;font-size:13.5px;margin:4px 0}
'''
glist = ''.join(f'<span><span class="gb">{g[1]}</span>{GN[g]}</span>' for g in GN)
body = f'''<main><header><h1>民法｜申論 115 出題預測</h1><p class="sub">依 99～114 年官方申論 32 題、選擇題 520 題、修法時點與本站模擬卷推估；推估不是保證，用來決定讀的順序。<a href="{HUB}#essay=114-一">回申論分頁 ›</a></p></header>
<div class="one"><b>一句話：115 年最可能是「一題物權＋一題總則／債編」。</b><p>物權題先讀：共有（第一主角）、抵押權與法定地上權、無權處分與善意取得。</p><p>總則・債編題先讀：行為能力・意思表示瑕疵（第 5 組 107 後 7 屆沒考、18 歲成年修法後沒考；通謀虛偽 110 年考過）、債務不履行。</p><p>練習卷：<a href="民法_申論專練卷.html">申論專練卷①（補模擬卷沒蓋到的三個主題）›</a></p></div>
<section class="blk"><h2>一、出題結構：16 年有 12 年至少一題落在物權三組</h2><p>以本頁分組計，第 1～3 組（共有／抵押地上／無權處分善意取得）16 年中有 12 年至少出一題；101、107、112、113 四年沒有（其中 101 典權、107 已登記不動產時效、112 靈骨塔物權法定仍碰到物權觀念，只有 113 瑕疵擔保＋居間完全沒碰物權）。102、108、109、110、114 五年兩題都在物權三組（110-二 通謀虛偽偏總則）。另一題通常是總則（意思表示、行為能力、時效、代理）或債編（居間、買賣、代位權）。</p><p>本頁沿用申論分頁的 6 組：</p><div class="grpl">{glist}</div><div class="tw"><table><thead><tr><th>年</th><th>第一題</th><th>第二題</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section class="blk"><h2>二、六組主題：考過幾次、多久沒考</h2><div class="tw"><table><thead><tr><th>主題</th><th>16 年考</th><th>近 5 年（110～114）</th><th>最後一次</th><th>已隔幾屆沒考</th></tr></thead><tbody>{gtab}</tbody></table></div><p class="note">5 組（意思表示・行為能力・債總）最後一次是 107 年，已隔 7 屆，是空最久的一組；4 組（居間・買賣）近 5 年考了 4 題，112、113 兩年的 4 題全在這組。</p></section>
<section class="blk"><h2>三、115 年預測（高＝優先讀）</h2>{prow}<p class="note">修法依據：民法§12（112.1.1 施行，18 歲成年）；§205（110.1.20 公布、公布後 6 個月施行，約定利率上限 16%）；§1223 特留分（115.8.17 公布、尚未施行，115 年考試適用舊法）。實務：最高法院 106 年度第 3 次民事庭會議（借名登記有權處分說）、80 年度第 2 次民事庭會議（時效取得地上權須已申請登記並經受理）、65 年台上字第 156 號判例（押租金不隨同移轉）。以上已逐字核對，見 KB《民法_現行條文核實表_補遺_20261020》。</p></section>
<section class="blk"><h2>四、範圍檢查：每一章都有範文可讀嗎？</h2><p>選擇題章節（題數最能反映出題範圍）對照本站申論範文（官方＋預測）；「模擬卷」欄是本站民法模擬試題一、二的申論落在哪一章。</p><div class="tw"><table><thead><tr><th>章節</th><th>選擇 16 年</th><th>近 5 年</th><th>模擬卷申論</th><th>本站範文（點開）</th></tr></thead><tbody>{crow}</tbody></table></div><p class="note">原本 6 章沒有任何範文（法人、物、無因管理、其他各種之債、拾得遺失添附、婚約婚姻），2026-10-28 已補預測題 44～49 各一張，另補 §188 僱用人責任（預42）、§244 詐害債權（預43）。申論專練卷①題三另有贈與（§406、§408、§419）與繼承的組合。</p></section>
<section class="blk"><h2>五、模擬卷涵蓋度：限時卷有練到哪些預測主題？</h2><p>本站民法限時模擬卷共 3 份、6 題申論（自擬 2 份＋補習班來勝卷 1 份；25 題整卷模擬是官方歷屆，不另計）：</p><div class="tw"><table><thead><tr><th>卷別</th><th>考點</th><th>對應預測主題</th></tr></thead><tbody>{mrow}</tbody></table></div><p><b>缺口</b>：預測「高」的<b>共有</b>原本一題都沒有，來勝卷申論二（分割後抵押權移存）補到一部分，但共有物<b>管理・分管</b>仍沒練到；<b>意思表示瑕疵・行為能力・債務不履行</b>只有來勝卷申論一碰到給付不能；另「其他各種之債」整章沒有範文。已補成 <a href="民法_申論專練卷.html">申論專練卷①</a>（三題各 25 分、限時 75 分鐘、自擬非官方）。</p></section>
<section class="blk"><h2>六、怎麼用這頁</h2><ol class="st"><li>平日每天讀一題「高」，物權、總則債編交錯。</li><li>每題先看「邏輯拆解」讀懂推理順序，再看「考場速寫」記骨架與失分點，最後對照「完整四段式」寫一次。</li><li>假日做申論專練卷①（限時 75 分鐘），寫完對照範文逐項勾採分點。</li><li>「中」的題目放第二輪；選擇題錯最多的章節優先。</li></ol></section>
</main>'''
page = HEAD + '<style>' + CSS + X + '</style></head><body><button id="theme-btn" onclick="toggleTheme()" title="切換深淺色" aria-label="切換深淺色">☀️</button>' + body
page += '<script>function ub(t){var b=document.getElementById("theme-btn");if(b)b.textContent=t==="dark"?"🌙":"☀️"}function toggleTheme(){var h=document.documentElement,c=h.getAttribute("data-theme")||"light",n=c==="dark"?"light":"dark";h.setAttribute("data-theme",n);ub(n);try{localStorage.setItem("bx-theme",n)}catch(e){}}ub(document.documentElement.getAttribute("data-theme")||"light");</script>'
page += FAB + '\n<script src="bxm-use.js"></script>\n<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("/brokerX/sw.js",{scope:"/brokerX/"});</script>\n</body></html>'
open(os.path.join(ROOT, '民法_申論115出題預測.html'), 'w', encoding='utf-8').write(page)
print('ok', len(page), dict(tot), dict(r5), last)
