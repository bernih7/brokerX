# 產生《土地法｜申論 115 出題預測》頁：歷屆分布＋輪替＋修法熱點＋範圍覆蓋檢查
import re, json, os, html
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
E = json.load(open(os.path.join(HERE, 'data', 'essays.json'), encoding='utf-8'))
TPL = open(os.path.join(ROOT, '土地法申論題_六型答題模板.html'), encoding='utf-8').read()
HEAD = TPL[:TPL.index('<title>')] + '<title>土地法申論115預測</title>' + TPL[TPL.index('</title>') + 8:TPL.index('<style>')]
CSS = TPL[TPL.index('<style>') + 7:TPL.index('</style>')]
FAB = TPL[TPL.index('<!--bxfab-->'):TPL.index('<!--/bxfab-->') + len('<!--/bxfab-->')] if '<!--bxfab-->' in TPL else ''
q = open(os.path.join(ROOT, '土地法互動練習.html'), encoding='utf-8').read()
QB, _ = json.JSONDecoder().raw_decode(q[q.find('[{"id"'):])
ESS = '土地法_申論題分類總覽.html'
SHORT = dict(A='都市計畫・公設保留地', B='土地徵收・區段徵收', C='市地重劃・空地・耕地', D='登記・優購・實價登錄', E='地價稅・土增稅', F='房屋稅・契稅・房地合一', G='地權總則・外國人・農地')
off = [e for e in E if e['kind'] == 'off']
def eid(e):
    if e['kind'] == 'off': y, n = e['key'].split('-'); return f'q-{y}-{n}'
    return e['idv'] or ('pr-%02d' % int(e['key'][1:]) if e['key'].startswith('P') else 'x-' + e['key'][1:])
BY = {e['key']: e for e in E}
def link(k, short=True):
    e = BY[k]; lab = k if e['kind'] == 'off' else ('預' + k if e['kind'] == 'pred' else '模' + k[1:] if e['kind'] == 'mock' else '專' + k[1:])
    return f'<a class="ek" href="{ESS}#{eid(e)}" title="{html.escape(e["nm"])}">{lab}</a>'
TAX = set('EF')
yrs = sorted({int(e['key'].split('-')[0]) for e in off})
rows = ''
for y in yrs:
    es = sorted([e for e in off if int(e['key'].split('-')[0]) == y], key=lambda e: e['key'])
    cells = ''.join(f'<td><span class="g g{e["cat"]}">{e["cat"]}</span>{link(e["key"])}<small>{html.escape(e["nm"][:26])}</small></td>' for e in es)
    rows += f'<tr><th>{y}</th>{cells}</tr>'
tot = Counter(e['cat'] for e in off); r5 = Counter(e['cat'] for e in off if int(e['key'].split('-')[0]) >= 110)
last = {g: max(int(e['key'].split('-')[0]) for e in off if e['cat'] == g) for g in tot}
gtab = ''.join(f'<tr><td><span class="g g{g}">{g}</span>{SHORT[g]}</td><td>{tot[g]}</td><td>{r5[g]}</td><td>{last[g]}</td><td>{115 - last[g] - 1}</td></tr>' for g in sorted(tot, key=lambda g: (-tot[g], g)))
mc = Counter(x['chapter'] for x in QB); mc5 = Counter(x['chapter'] for x in QB if int(x['year']) >= 110); cn = {x['chapter']: x['chapterName'] for x in QB}
MAP = dict(A1=['105-一', 'P13'], A2=['103-一', 'P04', 'P18', 'P19', 'P20', 'P26'], A3=['101-一', '111-一', 'P23', 'P09'], A4=['101-一', '111-一', 'P09'], A5=['P13'],
           B1=['106-二', 'P10'], B2=['99-一', '112-一', '114-一', 'P31', 'P01', 'P34'], B3=['P33'], C1=['P25', 'P34'], C2=['107-一', '113-一', 'P06'], C3=['113-二', 'P25', 'P22'],
           C4=['101-二', 'P03', 'K1'], D1=['108-一', '104-一'], D2=['99-二', 'P12'], D3=['109-一', 'P06'], D4=['X1', 'X2', 'X3', 'K2'],
           E1=['102-二', '105-二', '108-二', '109-二', 'P02'], E2=['103-二', '106-一', '110-一', '114-二', 'P07', 'P29', 'K3'], F1=['104-二', '112-二', 'P27', 'P22', 'K4'],
           G1=['111-二', 'P32'], H1=['107-二', '111-二', 'P30'], I1=['111-一', 'P24'])
mk = {}
for f, lab in [('土地法_來勝模擬試題一_土地法規.html', '法規'), ('土地法_來勝模擬試題一_土地稅法.html', '稅法')]:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    for c in re.findall(r'"ch": "([A-I]\d)"', s): mk[c] = mk.get(c, 0) + 1
crow = ''
for c in sorted(mc):
    ks = MAP[c]; noff = sum(1 for k in ks if BY[k]['kind'] == 'off')
    flag = '<b class="gap">官方申論沒考過</b>' if noff == 0 else ''
    crow += f'<tr><td>{html.escape(cn[c])}</td><td>{mc[c]}</td><td>{mc5[c]}</td><td>{mk.get(c, 0) or "－"}</td><td>{"".join(link(k) for k in ks)} {flag}</td></tr>'
assert all(k in BY for v in MAP.values() for k in v)
PRED = [
 ('法規題', '高', '土地徵收：撤銷・廢止・收回、區段徵收抵價地、徵收補償', '官方 109 之後 5 年沒考徵收（104、108、109 曾考）；選擇題徵收四章共 85 題、近 5 年 21 題；補習班模擬卷申論二即押撤銷與廢止。', ['K2', 'X1', 'X2', 'X3', '109-一', 'P12', 'P11']),
 ('法規題', '高', '平均地權條例 112 年修正：私法人購屋、預售屋、讓與轉售、炒作', '112.7.1 施行後官方申論尚未考；選擇題「申報登錄・預售屋」近 5 年 8 題（全 16 年才 11 題），出題明顯升溫；補習班模擬卷申論一即押私法人購屋。', ['K1', 'P03', 'P17', '101-二']),
 ('法規題', '高', '公共設施保留地與都市計畫', '16 年考 5 次、近 5 年 2 次（112、114），是法規題第一主角；換角度再考（取得方式、使用限制、地價稅、規定地價）的機率仍高。', ['114-一', '112-一', '99-二', 'P01', 'P34', 'P31']),
 ('法規題', '中', '登記與優先購買權：預告登記、§34-1、登記效力', '登記選擇題量最大（55 題）但申論只考過 103 預告登記；優購 101、111 考過。', ['103-一', '111-一', 'P04', 'P18', 'P20', 'P23']),
 ('法規題', '中', '地權總則：外國人、不得私有、§14Ⅲ（113.8.7 修正）', '110 考過外國人；§14 第 3 項 113.8.7 改列兩款，修法後未考。', ['110-二', '105-一', 'P13', 'P14', 'P15', 'P16']),
 ('稅法題', '高', '房屋稅 2.0：自住條件、差別稅率、按年計徵、變更申報', '113.7.1 施行後只在 113-二 考到空屋房屋稅一角；自住要件、§6-1 按年計徵、§7 申報都還沒考；補習班模擬卷申論（稅法二）即押此題。', ['K4', 'P27', '112-二', '113-二', '104-二']),
 ('稅法題', '高', '地價稅：納稅義務人、自用住宅、累進稅率', '稅法題 102 年起地價稅 4 次（102、105、108、109）、土增稅 4 次（103、106、110、114）大致輪替；114 剛考土增稅，地價稅自 109 後已 5 屆沒考。', ['109-二', '108-二', '105-二', 'P02']),
 ('稅法題', '中', '土地增值稅特殊規則：信託、配偶贈與、減免、計算', '114 剛考（非都市公設用地免徵），連考機率較低；但信託土地官方從未考過，補習班模擬卷（稅法一）押題。', ['K3', '110-一', 'P07', 'P29']),
 ('稅法題', '中', '房地合一稅 2.0', '107、111 兩次（都和土增稅、契稅比較）；補習班模擬卷選擇題 7 題，比重異常高。', ['P30', '107-二', '111-二']),
]
prow = ''.join(f'<div class="pc p{lv}"><div class="ph"><span class="pt">{side}</span><span class="pl">{lv}</span><b>{html.escape(t)}</b></div><p>{html.escape(why)}</p><p class="pk">讀這幾題：{"".join(link(k) for k in ks)}</p></div>' for side, lv, t, why, ks in PRED)
X = '''
.blk{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 14px 10px}
.blk h2{font:700 17px/1.4 "Noto Serif TC",serif;color:var(--pri);margin:0 0 8px}
.blk p{margin:6px 0}.note{font-size:13px;color:var(--muted)}
.tw{overflow-x:auto;margin:6px -4px}.tw table{border-collapse:collapse;width:100%;min-width:520px;font-size:13.5px}
.tw th,.tw td{border-bottom:1px solid var(--line);padding:6px 6px;text-align:left;vertical-align:top}.tw thead th{color:var(--muted);font-weight:500;font-size:12.5px}
.tw td small{display:block;color:var(--muted);font-size:12px;line-height:1.45}.tw td:nth-child(n+2){font-variant-numeric:tabular-nums}
.g{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:6px;background:var(--pri);color:var(--onpri);font-size:12px;font-weight:700;margin-right:6px}
.ek{display:inline-block;font-size:12.5px;padding:1px 8px;margin:2px 4px 2px 0;border-radius:99px;border:1px solid var(--line);color:var(--pri);text-decoration:none;background:var(--tint)}
.gap{color:var(--red);font-size:12px}
.one{background:var(--pri);color:var(--onpri);border-radius:14px;padding:14px}.one b{font:700 16px/1.5 "Noto Serif TC",serif;display:block;margin-bottom:6px}.one p{margin:4px 0;font-size:14px}
.pc{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0;background:var(--bg)}
.ph{display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}.ph b{font:700 15px/1.45 "Noto Serif TC",serif;flex:1 1 100%}
.pt{font-size:12px;color:var(--muted)}.pl{font-size:12px;font-weight:700;padding:0 8px;border-radius:99px;background:var(--line)}
.p高 .pl{background:var(--b4s);color:var(--b4);border:1px solid var(--b4l)}.p中 .pl{background:var(--b3s);color:var(--b3);border:1px solid var(--b3l)}
.pc p{margin:4px 0;font-size:14px}.pk{font-size:13px}
ol.st{margin:4px 0;padding-left:20px}ol.st li{margin:3px 0}
'''
body = f'''<main><header><h1>土地法｜申論 115 出題預測</h1><p class="sub">依 99～114 年官方申論 32 題、選擇題 518 題、修法時點與補習班模擬卷推估；推估不是保證，用來決定讀的順序。<a href="{ESS}">回申論總覽 ›</a></p></header>
<div class="one"><b>一句話：115 年最可能是「一題土地法規＋一題土地稅法」。</b><p>法規題先讀：土地徵收（撤銷・廢止）、平均地權 112 修正（私法人、預售屋）、公共設施保留地。</p><p>稅法題先讀：房屋稅 2.0（自住、按年計徵、申報）、地價稅（109 後 5 屆沒考）。</p></div>
<section class="blk"><h2>一、出題結構：102 年起幾乎都是「法規一題＋稅法一題」</h2><p>102～114 年 13 屆中，12 屆是一題土地法規（都市計畫、徵收、重劃、登記、地權）配一題稅法（地價稅、土增稅、房屋稅、房地合一）；113 年兩題都在 C 組，但第二題問的是空屋房屋稅與空地稅，仍含稅法。99～101 年未固定。</p><p>稅法題內部：地價稅（102、105、108、109）與土地增值稅（103、106、110、114）大致輪流；房屋稅與房地合一穿插（104、107、111、112、113）。</p><div class="tw"><table><thead><tr><th>年</th><th>第一題</th><th>第二題</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section class="blk"><h2>二、七大主題：考過幾次、多久沒考</h2><div class="tw"><table><thead><tr><th>主題</th><th>16 年考</th><th>近 5 年</th><th>最後一次</th><th>已隔幾屆沒考</th></tr></thead><tbody>{gtab}</tbody></table></div><p class="note">B 組（徵收）109 年後就沒考，已隔 5 屆；A 組近 3 年考 2 次仍是熱門。</p></section>
<section class="blk"><h2>三、115 年預測（高＝優先讀）</h2>{prow}<p class="note">修法依據（已核對條文）：平均地權條例 112.2.8 修正、112.7.1 施行（§79-1 私法人購屋、§47-3、§47-4 預售屋）；房屋稅條例 112.12.19 修正、113.7.1 施行（§5 差別稅率、§6-1 按年計徵）；土地法§14Ⅲ 113.8.7 修正；土地稅法§54Ⅱ 114.1.24 修正（再行出售罰鍰改為「2%以下」）；文化資產保存法§99 112.11.29 修正（歷史建築、紀念建築用地改為免徵地價稅、房屋稅）。</p></section>
<section class="blk"><h2>四、範圍檢查：每一章都有範文可讀嗎？</h2><p>選擇題章節（題數最能反映出題範圍）對照本站申論範文；「模擬卷」欄是補習班模擬試題一（土地法規＋土地稅法，各 25 題）在該章的選擇題數。</p><div class="tw"><table><thead><tr><th>章節</th><th>選擇 16 年</th><th>近 5 年</th><th>模擬卷</th><th>本站範文（點開）</th></tr></thead><tbody>{crow}</tbody></table></div><p class="note">22 章每章至少有一篇範文；標「官方申論沒考過」的章節，只靠預測題或模擬卷範文，是官方第一次考時最容易失分的地方。補習班模擬卷 4 題申論已全部收進申論總覽（模1～模4）。目前手上的模擬卷只有這一份（另有自建診斷卷，只有選擇題），拿到新的模擬卷再補進來。</p></section>
<section class="blk"><h2>五、怎麼用這頁</h2><ol class="st"><li>平日每天讀一題「高」，依上面順序：法規、稅法交錯。</li><li>每題先看「邏輯拆解」，再看「考場速寫」，最後看完整四段式；用速寫版默寫骨架。</li><li>「中」的題目放假日讀；選擇題錯最多的章節優先。</li></ol></section>
</main>'''
page = HEAD + '<style>' + CSS + X + '</style></head><body><button id="theme-btn" onclick="toggleTheme()" title="切換深淺色" aria-label="切換深淺色">☀️</button>' + body
page += '<script>function ub(t){var b=document.getElementById("theme-btn");if(b)b.textContent=t==="dark"?"🌙":"☀️"}function toggleTheme(){var h=document.documentElement,c=h.getAttribute("data-theme")||"light",n=c==="dark"?"light":"dark";h.setAttribute("data-theme",n);ub(n);try{localStorage.setItem("bx-theme",n)}catch(e){}}ub(document.documentElement.getAttribute("data-theme")||"light");</script>'
page += FAB + '\n<script src="bx-use.js"></script>\n<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("/brokerX/sw.js",{scope:"/brokerX/"});</script>\n</body></html>'
open(os.path.join(ROOT, '土地法_申論115出題預測.html'), 'w', encoding='utf-8').write(page)
print('ok', len(page))
