# -*- coding: utf-8 -*-
"""產生《經紀法規_程序總整理》。條文依 tools/essay_jj/law/lawfull.json 逐字；考古題取自 quiz_data.json。"""
import json, io, os, sys

ROOT = '/home/claude/bernih7/brokerx'
Q = {x['k']: x for x in json.load(io.open(ROOT + '/tools/essay_jj/quiz_data.json', encoding='utf-8'))['q']}
CHS = json.load(io.open(ROOT + '/tools/essay_jj/chapters.json', encoding='utf-8'))
PICK = json.load(io.open(os.path.dirname(os.path.abspath(__file__)) + '/pick.json', encoding='utf-8'))

PNAME = {
 'P1': '① 經紀業生命週期', 'P2': '② 經紀人員', 'P3': '③ 區權會', 'P4': '④ 住戶違規階梯',
 'P5': '⑤ 公共基金與點交', 'P6': '⑥ 消費爭議階梯', 'P7': '⑦ 公平會調查裁處',
 'P8': '⑧ 結合管制', 'P9': '⑨ 聯合行為許可', 'P10': '⑩ 說明書簽章'}

QD = []
for p, ks in PICK.items():
    for k in ks:
        x = Q[k]
        QD.append({'k': k, 'y': '%d年第%d題' % (x['y'], x['n']), 'g': CHS.get(x['ch'], x['ch']),
                   'gr': p, 'q': x['stem'], 'o': x['opt'], 'c': 'ABCD'.index(x['ans']), 'e': x['exp']})

QUIZ = 'https://bernih7.github.io/brokerX/%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E6%B3%95%E6%A2%9D%E8%A7%A3%E6%9E%90%E7%B7%B4%E7%BF%92.html'
HUB = '%E7%B6%93%E7%B4%80%E6%B3%95%E8%A6%8F_%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html'

CSS = r'''
:root{--pri:#2F5D50;--pri2:#3E7566;--key:#8A5517;--onpri:#FFFFFF;--hbg1:#2F5D50;--hbg2:#3E7566;--bg:#F5F1E6;--ink:#25302C;--red:#A8402B;--gold:#B8782E;--green:#35693F;--card:#FFFEFA;--line:#DDD6C0;--muted:#66706A;--blue:#1E3E6E;--surface2:#ECE6D4;--warn:#FFF1D6;--cA:#2F5D50;--cC:#8A5517;--cD:#B9722A;--cE:#3A5A78;--cG:#6B4E8A;--cH:#A8402B;color-scheme:light}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--pri:#84C2AE;--pri2:#6FAE9A;--key:#E0B070;--onpri:#10201B;--hbg1:#24413A;--hbg2:#2D4F46;--bg:#161C19;--ink:#E7ECE6;--red:#E05040;--gold:#E0B070;--green:#8FCB93;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--blue:#6090D8;--surface2:#27302B;--warn:#3A2E14;--cA:#84C2AE;--cC:#E0B070;--cD:#E29A5E;--cE:#6AA8D0;--cG:#B08CC8;--cH:#E88070;color-scheme:dark}}
:root[data-theme="dark"]{--pri:#84C2AE;--pri2:#6FAE9A;--key:#E0B070;--onpri:#10201B;--hbg1:#24413A;--hbg2:#2D4F46;--bg:#161C19;--ink:#E7ECE6;--red:#E05040;--gold:#E0B070;--green:#8FCB93;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--blue:#6090D8;--surface2:#27302B;--warn:#3A2E14;--cA:#84C2AE;--cC:#E0B070;--cD:#E29A5E;--cE:#6AA8D0;--cG:#B08CC8;--cH:#E88070;color-scheme:dark}
:root[data-theme="light"]{--pri:#2F5D50;--pri2:#3E7566;--key:#8A5517;--onpri:#FFFFFF;--hbg1:#2F5D50;--hbg2:#3E7566;--bg:#F5F1E6;--ink:#25302C;--red:#A8402B;--gold:#B8782E;--green:#35693F;--card:#FFFEFA;--line:#DDD6C0;--muted:#66706A;--blue:#1E3E6E;--surface2:#ECE6D4;--warn:#FFF1D6;--cA:#2F5D50;--cC:#8A5517;--cD:#B9722A;--cE:#3A5A78;--cG:#6B4E8A;--cH:#A8402B;color-scheme:light}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:58px}
body{font-family:"Noto Sans TC",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.75;font-size:15px}
header{background:linear-gradient(135deg,var(--hbg1),var(--hbg2));color:#fff;padding:22px 16px 18px;text-align:center;position:relative}
header h1{font-family:"Noto Serif TC",serif;font-size:21px;font-weight:700;margin-bottom:4px}
header .sub{font-size:13px;opacity:.9}
.theme{position:absolute;right:12px;top:12px;font:inherit;font-size:15px;border:1px solid rgba(255,255,255,.5);background:rgba(255,255,255,.12);color:#fff;border-radius:99px;width:36px;height:36px;cursor:pointer}
nav{position:sticky;top:0;z-index:20;background:var(--card);border-bottom:1px solid var(--line);padding:8px 12px;display:flex;gap:6px;overflow-x:auto;scrollbar-width:thin}
nav a{flex:none;font-size:12px;font-weight:700;padding:4px 12px;border-radius:99px;border:1px solid var(--line);color:var(--pri);text-decoration:none;background:var(--card)}
main{max-width:980px;margin:0 auto;padding-block:16px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.intro{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--pri);border-radius:8px;padding:12px 14px;font-size:13.5px;color:var(--muted)}
.intro b{color:var(--ink)}
.tools{display:flex;gap:8px;margin:14px 0 4px;flex-wrap:wrap}
.tools button{font:inherit;font-size:13px;font-weight:700;padding:6px 14px;border-radius:99px;border:1px solid var(--pri);background:var(--card);color:var(--pri);cursor:pointer}
details.sec{margin-top:16px;background:var(--card);border:1px solid var(--line);border-left:5px solid var(--a,var(--pri));border-radius:10px;overflow:hidden}
details.sec>summary{list-style:none;cursor:pointer;padding:13px 16px;display:flex;align-items:center;gap:10px}
details.sec>summary::-webkit-details-marker{display:none}
details.sec>summary h2{font-family:"Noto Serif TC",serif;font-size:16.5px;color:var(--a,var(--pri));flex:1;min-width:0}
details.sec>summary .cnt{font-size:12px;color:var(--muted);flex:none}
details.sec>summary::after{content:"\203A";font-size:20px;color:var(--muted);transition:transform .2s}
details.sec[open]>summary::after{transform:rotate(90deg)}
.bd{padding:2px 16px 16px}
.law{font-weight:700;color:var(--key)}
.k{color:var(--red);font-weight:700}
.n{background:var(--warn);color:var(--key);font-weight:700;padding:0 4px;border-radius:4px;white-space:nowrap}
.mn{background:color-mix(in srgb,var(--green) 13%,var(--card));border:1px solid color-mix(in srgb,var(--green) 35%,transparent);border-radius:8px;padding:9px 12px;margin-top:10px;font-size:14px}
.mn b{color:var(--green)}
.tr{background:color-mix(in srgb,var(--red) 10%,var(--card));border-left:4px solid var(--red);border-radius:6px;padding:8px 12px;margin-top:10px;font-size:14px}
.tr b{color:var(--red)}
ol.flow{list-style:none;counter-reset:f;margin-top:8px}
ol.flow li{counter-increment:f;position:relative;padding:8px 0 8px 40px;border-left:2px solid var(--line);margin-left:13px;min-width:0}
ol.flow li::before{content:counter(f);position:absolute;left:-14px;top:8px;width:26px;height:26px;border-radius:50%;background:var(--a,var(--pri));color:var(--onpri);font-weight:700;font-size:13px;display:grid;place-items:center}
ol.flow li:last-child{border-left-color:transparent}
.steps{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:8px 0 2px;font-size:12px}
.steps a{color:var(--a,var(--pri));text-decoration:none;border:1px solid var(--line);border-radius:99px;padding:2px 9px;background:var(--bg)}
.steps i{color:var(--muted);font-style:normal}
.tw{overflow-x:auto;margin-top:8px;border:1px solid var(--line);border-radius:8px}
table{width:100%;border-collapse:collapse;min-width:600px;font-size:13.5px}
th,td{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--surface2);font-weight:700}
.fil{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}
.fil button{font:inherit;font-size:12px;font-weight:700;padding:4px 11px;border-radius:99px;border:1px solid var(--line);background:var(--card);color:var(--muted);cursor:pointer}
.fil button.on{border-color:var(--pri);color:var(--pri);background:color-mix(in srgb,var(--pri) 10%,var(--card))}
.qz{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-top:10px;background:var(--bg)}
.qz .qh{font-size:12px;color:var(--muted);margin-bottom:3px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.qz .qh a{margin-left:auto;color:var(--pri);text-decoration:none;border:1px solid var(--line);border-radius:99px;padding:1px 9px;font-weight:700}
.qz .qt{font-size:14.5px;margin-bottom:6px}
.qz button.op{display:flex;gap:8px;width:100%;text-align:left;font:inherit;font-size:14px;padding:7px 10px;margin-top:5px;border:1px solid var(--line);border-radius:7px;background:var(--card);color:var(--ink);cursor:pointer}
.qz button.op b{flex:none}
.qz button.op.ok{border-color:var(--green);background:color-mix(in srgb,var(--green) 12%,var(--card))}
.qz button.op.ng{border-color:var(--red);background:color-mix(in srgb,var(--red) 10%,var(--card))}
.qz .ex{display:none;font-size:13.5px;margin-top:8px;border-top:1px dashed var(--line);padding-top:6px}
.qz.done .ex{display:block}
.qz .ex div{margin-top:4px}
.qz .ex .y{color:var(--green);font-weight:700}.qz .ex .x{color:var(--red);font-weight:700}
.score{font-size:13px;color:var(--muted);margin-top:6px}
.foot{font-size:12.5px;color:var(--muted);margin:22px 0 56px}
.sub2{font-family:"Noto Serif TC",serif;font-size:15px;color:var(--a,var(--pri));margin:16px 0 4px;padding-top:10px;border-top:1px dashed var(--line)}
p+p{margin-top:6px}
ul.pl{margin:6px 0 0 20px;font-size:14px}
ul.pl li{margin-top:3px}
@media(max-width:430px){details.sec>summary{padding:11px 12px}.bd{padding:2px 12px 14px}}
'''

# ============ 內容 ============
S = []


def sec(sid, color, title, cnt, body, open_=False):
    S.append('<details class="sec" id="%s" style="--a:var(--c%s)"%s><summary><h2>%s</h2><span class="cnt">%s</span></summary><div class="bd">\n%s\n</div></details>'
             % (sid, color, ' open' if open_ else '', title, cnt, body))


# ⓪ 總比較表
sec('t0', 'A', '⓪ 十大程序總比較表', '10 種程序', '''
<p style="font-size:13.5px;color:var(--muted)">先橫著比「誰啟動→多久→誰決定→不做會怎樣」，再展開各程序細節。數字一律以現行法為準。</p>
<div class="tw rc"><table style="min-width:900px"><thead><tr><th style="width:13%">程序</th><th style="width:16%">誰啟動</th><th style="width:24%">關鍵期限</th><th style="width:21%">門檻／決定者</th><th>不做的效果</th></tr></thead><tbody>
<tr><td><b>① 經紀業生命週期</b><br><span class="law">條例§5～§10</span></td><td>業者向直轄市、縣（市）主管機關申請許可</td><td>許可後 <span class="n">6個月</span> 內開始營業（正當理由得展延 <span class="n">1次、3個月</span>）；開業後 <span class="n">15日</span> 內備查；變更／分設／裁撤／遷出 <span class="n">30日</span> 內備查</td><td>直轄市、縣（市）主管機關</td><td>逾期未開業→<b class="k">廢止許可</b>（§7Ⅰ）；自行停業連續 <span class="n">6個月</span> 以上→得廢止許可（§30）</td></tr>
<tr><td><b>② 經紀人員</b><br><span class="law">條例§13～§15</span></td><td>考試及格者向<b>戶籍所在地</b>直轄市、縣（市）主管機關請領</td><td>經紀人證書效期 <span class="n">4年</span>，期滿前 <span class="n">6個月</span> 內檢附 <span class="n">30小時</span> 訓練換證；營業員證明 <span class="n">4年</span>，期滿檢附 <span class="n">20小時</span> 重新登錄</td><td>直轄市、縣（市）主管機關（營業員為中央指定之機構、團體）</td><td>未換證且效期屆滿→<b class="k">註銷證書</b>（細則§18），重領須最近 4 年內 30 小時</td></tr>
<tr><td><b>③ 區權會</b><br><span class="law">公寓§25～§34</span></td><td>召集人（主委／管理負責人／互推／主管機關指定臨時召集人）</td><td>開會前 <span class="n">10日</span> 書面通知（急迫臨時會公告不得少於 <span class="n">2日</span>）；紀錄會後 <span class="n">15日</span> 內送達</td><td>一般決議：<b class="k">2/3 出席、出席 3/4 同意</b>（§31）</td><td>未達定額→得就同一議案<b class="k">重新召集</b>（§32 低門檻＋7 日反對期）</td></tr>
<tr><td><b>④ 住戶違規階梯</b><br><span class="law">公寓§16、§21、§22</span></td><td>管理負責人或管理委員會</td><td>促請改善<b class="k">3個月</b>仍未改善→訴請遷離；判決確定後 <span class="n">3個月</span> 內不自行出讓→聲請拍賣</td><td>訴請遷離／出讓須<b class="k">經區權會決議</b></td><td>罰鍰 3,000～15,000（§47）或 4萬～20萬（§49），並得連續處罰</td></tr>
<tr><td><b>⑤ 公共基金與點交</b><br><span class="law">公寓§18、§28、§57</span></td><td>起造人</td><td>登記區權人<b class="k">過半數且比例過半</b>→<span class="n">3個月</span> 內召集第一次區權會；管委會成立後 <span class="n">7日</span> 內會同檢測點交；檢測不過歸責起造人者，<span class="n">1個月</span> 內再點交</td><td>主管機關報備後由<b>公庫代為撥付</b>公共基金</td><td>起造人違反 §57、§58→罰 <span class="n">4萬～20萬</span>（§49Ⅰ⑧）</td></tr>
<tr><td><b>⑥ 消費爭議階梯</b><br><span class="law">消保§43～§46</span></td><td>消費者</td><td>企業經營者應於申訴之日起 <span class="n">15日</span> 內妥適處理</td><td>一申訴（企業／消保團體／消費者服務中心）→二申訴（<b>消保官</b>）→調解（消費爭議調解委員會，<span class="n">7～21名</span>，消保官為主席）→消訴</td><td>調解成立作成調解書，準用鄉鎮市調解條例 §25～§29（得經法院核定）</td></tr>
<tr><td><b>⑦ 公平會調查裁處</b><br><span class="law">公平§26～§28、§40</span></td><td>檢舉或<b>依職權</b></td><td>承諾改正→得<b class="k">中止調查</b>，裁處權時效停止進行</td><td>公平交易委員會</td><td>限期令停止改正＋罰 <span class="n">10萬～5千萬</span>；屆期不改→按次 <span class="n">20萬～1億</span>（§40Ⅰ）</td></tr>
<tr><td><b>⑧ 結合管制</b><br><span class="law">公平§10～§13、§39</span></td><td>事業<b class="k">事前申報</b>（非許可制）</td><td>受理完整資料之日起 <span class="n">30工作日</span> 內不得結合；必要時縮短或延長，延長<b class="k">不得逾 60 工作日</b></td><td>整體經濟利益<b class="k">大於</b>限制競爭不利益者，不得禁止（§13Ⅰ）</td><td>未申報而結合→禁止結合等處分＋罰 <span class="n">20萬～5千萬</span>（§39Ⅰ）</td></tr>
<tr><td><b>⑨ 聯合行為許可</b><br><span class="law">公平§14～§16、§40</span></td><td>事業<b class="k">事前申請許可</b></td><td>主管機關應於 <span class="n">3個月</span> 內決定（必要時延長<b class="k">一次</b>）；許可期限不得逾 <span class="n">5年</span>；屆滿前 <span class="n">3～6個月</span> 申請延展，每次不得逾 <span class="n">5年</span></td><td>八款例外且<b class="k">有益於整體經濟與公共利益</b></td><td>§40 罰鍰；情節重大得處上一年度銷售金額 <span class="n">10%</span> 以下（§40Ⅱ）</td></tr>
<tr><td><b>⑩ 說明書簽章</b><br><span class="law">條例§22～§24</span></td><td>經紀業指派經紀人</td><td>解說<b class="k">前</b>經委託人簽章（§23Ⅱ）→簽約時交付相對人並由<b class="k">相對人簽章</b>（§24Ⅰ）</td><td>六類文件須經紀人簽章；代銷不適用①委託契約書②要約書</td><td>違反 §22Ⅰ：業者罰 <span class="n">6萬～30萬</span>（§29Ⅰ①）＋經紀人<b class="k">申誡</b>（§31Ⅰ①）</td></tr>
</tbody></table></div>
<div class="mn"><b>橫向記憶：</b>「<b>6 個月開業</b>、<b>15 日備查</b>、<b>30 日變更</b>」是經紀業三大數字；「<b>10 日通知、15 日送紀錄</b>」是區權會兩大數字；「<b>30 工作日</b>結合、<b>3 個月</b>聯合、<b>15 日</b>申訴」是三法各自的招牌天數——這三組最常被互換出題。</div>
''', open_=True)

# ① 經紀業生命週期
sec('p1', 'A', '① 經紀業生命週期：許可 → 開業 → 異動 → 退場', '條例§5～§10、細則§2～§13-3', '''
<div class="sub2">八步流程</div>
<ol class="flow">
<li><b>申請許可</b>：經營經紀業者，應向主管機關<b class="k">申請許可後</b>，依法辦理公司或商業登記；<b class="k">經營國外不動產仲介或代銷業務者，以公司型態為限</b>（<span class="law">條例§5Ⅰ</span>）。應檢附申請書一式二份、負責人／董事／監察人／經理人名冊及身分證明文件影本（<span class="law">細則§2</span>）。</li>
<li><b>審查與補正</b>：合於規定者予以許可，並副知轄內同業公會轉知全國聯合會；不合規定者通知<b class="k">15日內補正</b>，屆期未補正<b class="k">駁回</b>（<span class="law">細則§3</span>）。有 §6Ⅰ 七款消極資格之一者不得申請，已許可者撤銷或廢止（<span class="law">條例§6</span>）。</li>
<li><b>六個月內三件事</b>：許可後應於 <span class="n">6個月</span> 內①辦妥公司或商業登記②繳存營業保證金③加入<b class="k">登記所在地</b>之同業公會（<span class="law">細則§4</span>）；逾期未開始營業者<b class="k">廢止許可</b>，但有正當理由得申請<b class="k">展延一次，以 3 個月為限</b>（<span class="law">條例§7Ⅰ</span>）。</li>
<li><b>開業備查</b>：開始營業後 <span class="n">15日</span> 內檢附申請書、公司或商業登記證明、<b>營業保證金繳存證明</b>、同業公會會員證明、經紀人員名冊及證書影本等，向所在地直轄市、縣（市）主管機關<b class="k">申請備查</b>（<span class="law">細則§5</span>）。</li>
<li><b>異動備查（三十日家族）</b>：名稱／所在地／組織型態／經營型態／營業項目、負責人與董監經理人變更→<b class="k">變更之日起 30 日</b>內書面備查（<span class="law">細則§6</span>）；遷出管轄區→<b class="k">遷出後 30 日</b>內向遷入機關申請遷入備查並加入遷入地公會（<span class="law">細則§7</span>）；分設營業處所→<b class="k">設立後 30 日</b>內備查（<span class="law">細則§8</span>，條例§5Ⅲ）；分設事項變更→<b class="k">30 日</b>內（<span class="law">細則§9</span>）；分設處所裁撤→<b class="k">裁撤後 30 日</b>內（<span class="law">細則§10</span>）。</li>
<li><b>人員配置與名冊</b>：每一營業處所<b class="k">至少置經紀人一人</b>；非常態營業處所銷售總金額達 <b class="k">6 億元</b>以上者至少置專業經紀人一人；<b class="k">經紀營業員每逾 20 名增設經紀人一人</b>（<span class="law">條例§11</span>）。經紀人到職之日起 <span class="n">15日</span> 內造具名冊報請所在地主管機關<b class="k">層報中央</b>主管機關備查，異動時亦同（<span class="law">條例§12</span>）。</li>
<li><b>保證金的維持</b>：營業保證金由全國聯合會統一於指定金融機構設<b>營業保證基金專戶</b>，組成管理委員會保管；<b class="k">由經紀業擔任之委員不得超過委員總數 2/5</b>（<span class="law">條例§8Ⅰ、Ⅱ</span>）。低於法定額度時，全國聯合會應通知經紀業<b class="k">1 個月內補足</b>（<span class="law">條例§8Ⅳ</span>）。保證金<b class="k">獨立</b>於經紀業及經紀人員之外，不因其債權債務而讓與、扣押、抵銷或設定負擔（<span class="law">條例§9Ⅰ</span>）。</li>
<li><b>退場與退還</b>：因合併、變更組織者權利隨之移轉；因<b>申請解散</b>者，得自<b class="k">核准註銷營業之日滿 1 年後 2 年內</b>請求退還原繳存之營業保證金，<b class="k">但不含孳息</b>（<span class="law">條例§9Ⅱ</span>）。得請求退還之情形限三種：公司申請解散、商號申請歇業、營業項目變更後已無仲介及代銷業而組織仍存續（<span class="law">細則§13-1</span>）。開始營業後<b class="k">自行停止營業連續 6 個月以上</b>且未依法辦理停業登記者，得廢止其許可（<span class="law">條例§30</span>）。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>「<b>許 6 開 15 變 30</b>」——許可後 6 個月開業、開業後 15 日備查、任何變更 30 日備查。退還保證金則是「<b>滿 1 年後、2 年內</b>」，不是「1 年內」。</div>
<div class="tr"><b>考試陷阱：</b>①「加入<b>登記所在地</b>同業公會」不是「營業處所所在地」；所在地尚未設公會者加入<b>鄰近</b>直轄市、縣（市）公會，設立後應即加入（細則§12）。②代銷經紀業在代銷公會未設立前，先加入<b>仲介</b>經紀業公會（細則§13）。③保證金退還是「核准註銷營業之日<b>滿 1 年後 2 年內</b>」，常被改成「1 年內」「2 年後」。④§7Ⅰ的展延是「<b>一次、3 個月</b>」，不是 6 個月。⑤繳存保證金<b>超過一定金額</b>的部分，得以金融機構保證函擔保（§7Ⅲ），不是全部都能用保證函。</div>
''')

# ② 經紀人員
sec('p2', 'A', '② 經紀人員：資格 → 請領 → 換證 → 註銷 → 重領', '條例§13～§17、§31；細則§15～§20', '''
<div class="sub2">經紀人 vs 經紀營業員（兩條平行線）</div>
<div class="tw rc"><table style="min-width:640px"><thead><tr><th style="width:17%">項目</th><th style="width:42%">不動產經紀人</th><th>不動產經紀營業員</th></tr></thead><tbody>
<tr><td>取得資格</td><td>經紀人<b class="k">考試及格</b>並領有經紀人證書（<span class="law">§13Ⅰ</span>）</td><td>經中央主管機關或其認可之機構、團體舉辦<b class="k">訓練合格</b>，<b>或</b>經紀人考試及格，並向中央指定之機構、團體<b class="k">登錄</b>及領有證明（<span class="law">§13Ⅱ</span>）</td></tr>
<tr><td>前置經歷</td><td>考試及格後須具備<b class="k">1 年以上經紀營業員經驗</b>，始得請領（<span class="law">§14Ⅰ</span>）</td><td>無；訓練<b class="k">不得少於 30 小時</b>（<span class="law">§13Ⅲ</span>）</td></tr>
<tr><td>發證機關</td><td>向<b class="k">戶籍所在地</b>直轄市、縣（市）主管機關申請（<span class="law">細則§15Ⅰ</span>）；外國人向<b class="k">居留地</b>申請（<span class="law">細則§16</span>）</td><td>中央主管機關<b>指定之機構、團體</b>（§13Ⅱ）</td></tr>
<tr><td>效期</td><td><span class="n">4年</span>（<span class="law">§15Ⅰ</span>）</td><td>證明有效期限 <span class="n">4年</span>（<span class="law">§13Ⅲ</span>）</td></tr>
<tr><td>期滿怎麼辦</td><td>檢附<b class="k">4 年內 30 小時</b>以上專業訓練證明，向直轄市、縣（市）政府<b class="k">換證</b>；應於有效期限屆滿<b class="k">前 6 個月內</b>申請（<span class="law">細則§17Ⅰ</span>）</td><td>檢附完成訓練 <b class="k">20 小時</b>以上證明，向中央指定之機構、團體<b class="k">重新登錄</b>（<span class="law">§13Ⅲ</span>）</td></tr>
</tbody></table></div>
<div class="sub2">換證與註銷的五步</div>
<ol class="flow">
<li><b>期滿前 6 個月內申請</b>：檢附申請書、30 小時以上訓練證明、原證書（<span class="law">細則§17Ⅰ</span>）。</li>
<li><b>審查</b>：合格即換發；不合規定通知 <span class="n">15日</span> 內補正，屆期未補正駁回並退還文件（<span class="law">細則§17Ⅱ</span>）。</li>
<li><b>新效期起算</b>：換發證書之有效期限，自<b class="k">原證書有效期限屆滿之次日起算 4 年</b>；得以在原證書<b>加註延長</b>之方式為之（<span class="law">細則§17Ⅲ、Ⅳ</span>）。</li>
<li><b>註銷</b>：未依規定換證、或申請被駁回而原證書效期屆滿者，由原核發機關<b class="k">註銷原證書</b>，並公告周知、通知當事人、其任職經紀業所在地主管機關及所屬公會轉知全國聯合會（<span class="law">細則§18</span>）。</li>
<li><b>重新請領</b>：經註銷後重新申請核發者，應檢附細則§15Ⅰ①～④文件，及<b class="k">最近 4 年內</b>完成專業訓練 <b class="k">30 小時</b>以上之證明原本及影本（<span class="law">細則§19</span>）。證書損壞或滅失申請換發或補發者，敘明原因並檢附§15Ⅰ①～④文件（<span class="law">細則§20</span>）。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>人「<b>4 年 30 小時</b>」、員「<b>4 年 20 小時</b>」；<b>人換證、員重新登錄</b>；人找<b>縣市政府</b>、員找<b>中央指定機構團體</b>。</div>
<div class="tr"><b>考試陷阱：</b>①請領經紀人證書找<b>戶籍所在地</b>，不是任職地、不是居住地（外國人才是居留地）。②「1 年以上經紀營業員經驗」是<b>請領證書</b>的要件，不是<b>參加考試</b>的要件。③經紀人員應<b class="k">專任一經紀業</b>，不得為自己或他經紀業執業；<b>但經所屬經紀業同意</b>為他經紀業執行業務者不在此限（§16）——「一律不得」是錯的。④經紀業不得僱用未具經紀人員資格者從事仲介或代銷（§17），違反罰 6 萬～30 萬（§29Ⅰ①）。⑤懲戒兩檔：違反§16、§22Ⅰ、§23、§25 →<b class="k">申誡</b>；違反§19Ⅰ（收取差價或其他報酬）→<b class="k">6 個月以上 3 年以下停止執行業務</b>；申誡<b class="k">3 次</b>另予停業處分，停業累計達 <b class="k">5 年</b>以上廢止證書或證明（§31）。</div>
''')

# ③ 區權會
sec('p3', 'E', '③ 區分所有權人會議：召集 → 通知 → 出席 → 決議 → 紀錄', '公寓§25、§28～§35', '''
<div class="sub2">六步流程</div>
<ol class="flow">
<li><b>誰召集</b>：由具區分所有權人身分之<b>管理負責人、管委會主任委員或管理委員</b>為召集人；無者由區分所有權人<b class="k">互推一人</b>；無法互推時，各區分所有權人得申請主管機關<b class="k">指定臨時召集人</b>，不申請時主管機關得視需要指定一人或<b>依規約輪流擔任</b>，任期至互推召集人為止（<span class="law">§25Ⅲ、Ⅳ</span>）。召集人任期依區權會或規約，<b class="k">1 至 2 年，連選得連任一次</b>；未規定者任期 1 年（§25Ⅲ）。</li>
<li><b>何時開</b>：<b class="k">每年至少召開定期會議一次</b>。應召開臨時會議之情形兩款：①發生重大事故有及時處理之必要，經管理負責人或管委會請求；②經<b class="k">區分所有權人 1/5 以上且其區分所有權比例合計 1/5 以上</b>，書面載明召集目的及理由請求（<span class="law">§25Ⅰ、Ⅱ</span>）。</li>
<li><b>通知</b>：召集人於<b class="k">開會前 10 日</b>以書面載明開會內容通知各區分所有權人；有急迫情事須召開臨時會者得以<b>公告</b>為之，<b class="k">公告期間不得少於 2 日</b>（<span class="law">§30Ⅰ</span>）。<b class="k">管理委員之選任事項</b>應在開會通知中載明並公告，<b class="k">不得以臨時動議提出</b>（<span class="law">§30Ⅱ</span>）。</li>
<li><b>一般決議門檻</b>：除規約另有規定外，應有<b class="k">區分所有權人 2/3 以上及其區分所有權比例合計 2/3 以上出席</b>，以<b class="k">出席人數 3/4 以上及其區分所有權比例占出席人數區分所有權 3/4 以上之同意</b>行之（<span class="law">§31</span>）。</li>
<li><b>未獲決議→重新召集（§32 三段式）</b>：①開議門檻降為<b class="k">區分所有權人 3 人並 1/5 以上及其比例合計 1/5 以上出席</b>，以<b class="k">出席過半數及比例過半數</b>同意作成決議；②會議紀錄送達後，各區分所有權人得於<b class="k">7 日內</b>以書面表示反對；③書面反對意見<b class="k">未超過</b>全體區分所有權人及其比例合計<b class="k">半數</b>時，該決議<b class="k">視為成立</b>；主席應於決議成立後 <b class="k">10 日</b>內書面送達全體區分所有權人並公告（<span class="law">§32</span>）。</li>
<li><b>紀錄與閱覽</b>：會議應作成紀錄，載明開會經過及決議事項，由<b>主席簽名</b>，於<b class="k">會後 15 日內</b>送達各區分所有權人並公告；紀錄應與簽名簿及<b>代理出席委託書</b>一併保存（<span class="law">§34</span>）。利害關係人於必要時得請求閱覽或影印規約、公共基金餘額、會計憑證帳簿、財務報表、欠繳情形、管委會會議紀錄及區權會紀錄，<b class="k">管理負責人或管委會不得拒絕</b>（<span class="law">§35</span>）。</li>
</ol>
<div class="sub2">特別生效要件（§33）：決議之外還要「那個人」同意</div>
<ul class="pl">
<li>專有部分經區權會<b>約定為約定共用部分</b> → 應經<b class="k">該專有部分區分所有權人同意</b>。</li>
<li>外牆面、樓頂平臺設置<b>廣告物、基地台</b>等強波發射設備 → 設於<b class="k">屋頂</b>者經<b>頂層</b>區分所有權人同意；設於<b class="k">其他樓層</b>者經<b>該樓層</b>區分所有權人同意，該層住戶並得<b>參加區權會陳述意見</b>。</li>
<li>依 §56Ⅰ 成立之<b>約定專用部分變更</b> → 應經<b class="k">使用該約定專用部分之區分所有權人同意</b>；但顯已違反公共利益經法院判決確定者，不在此限。</li>
</ul>
<div class="mn"><b>口訣〔自編〕：</b>一般決議「<b>2/3 出席、3/4 同意</b>」；重開「<b>1/5 出席、過半同意、7 日反對、10 日送達</b>」；通知「<b>前 10 日</b>」、紀錄「<b>後 15 日</b>」。</div>
<div class="tr"><b>考試陷阱：</b>①§32 重新召集是「<b>3 人<u>並</u> 1/5 以上</b>」，兩個條件同時要，不是擇一。②「7 日內反對」的效果是「<b>未超過半數即視為成立</b>」，不是「超過半數才成立」——方向常被倒過來。③<b>管理委員選任</b>不得以臨時動議提出（§30Ⅱ）；其他事項法條沒禁止。④臨時會請求門檻是「<b>1/5 人數＋1/5 比例</b>」，不是 1/4、不是只看人數。⑤任期「1 至 2 年，連選得連任<b>一次</b>」只限主委、管理負責人及負責<b>財務、監察</b>業務之管理委員；<b>其餘管理委員連選得連任</b>（§29Ⅲ）——這是 114-3 的考點。</div>
''')

# ④ 住戶違規階梯
sec('p4', 'E', '④ 住戶違規階梯：制止 → 報請處罰 → 訴請遷離 → 出讓拍賣', '公寓§6、§9、§15、§16、§21、§22、§47、§49', '''
<div class="sub2">四階上升</div>
<ol class="flow">
<li><b>第一階：管委會制止、按規約處理</b>。住戶違反 §16Ⅰ～Ⅳ（棄置垃圾污染惡臭喧囂振動／堆置雜物設柵欄營業使用違規廣告物私設路障／未經核准破壞變更主要構造／飼養動物妨礙公共衛生安寧安全）時，管理負責人或管委會<b class="k">應予制止或按規約處理</b>，<b class="k">經制止而不遵從者，得報請直轄市、縣（市）主管機關處理</b>（<span class="law">§16Ⅴ</span>）。擅自變更使用執照用途者亦同，並<b>要求回復原狀</b>（<span class="law">§15Ⅱ</span>）。</li>
<li><b>第二階：主管機關罰鍰</b>。§47 三款（召集人／起造人／臨時召集人違反召集義務、住戶違反§16Ⅰ或Ⅳ、違反§6 經通知限期改善屆期不改）→<b class="k">3,000～15,000 元</b>，並得令限期改善或履行，屆期不改<b class="k">得連續處罰</b>。§49 八款（含違反§16Ⅱ或Ⅲ、擅自變更§15Ⅰ使用、未繳公共基金、未投保責任保險、起造人違反§57或§58 等）→<b class="k">4 萬～20 萬元</b>，同樣得令限期改善並連續處罰。</li>
<li><b>第三階：訴請法院強制遷離</b>。住戶有下列之一，由管理負責人或管委會<b class="k">促請改善，於 3 個月內仍未改善</b>者，得依<b class="k">區權會決議</b>訴請法院強制其遷離：①積欠應分擔費用，<b class="k">經強制執行後再度積欠</b>金額達其<b class="k">區分所有權總價 1%</b>；②違反本條例經依<b class="k">§49Ⅰ①～④</b>處罰鍰後仍不改善或續犯；③其他違反法令或規約<b class="k">情節重大</b>（<span class="law">§22Ⅰ</span>）。</li>
<li><b>第四階：訴請出讓、聲請拍賣</b>。前項住戶如為<b>區分所有權人</b>，得依區權會決議訴請法院命其<b class="k">出讓區分所有權及其基地所有權應有部分</b>；<b class="k">判決確定後 3 個月內</b>不自行出讓並完成移轉登記者，得<b class="k">聲請法院拍賣</b>（<span class="law">§22Ⅱ</span>）。拍賣所得，於積欠本條例應分擔之費用，其<b class="k">受償順序與第一順位抵押權同</b>（<span class="law">§22Ⅲ</span>）。</li>
</ol>
<div class="sub2">另一條線：單純欠費（§21）</div>
<p>區分所有權人或住戶積欠應繳公共基金或應分擔、其他應負擔之費用，<b class="k">已逾二期或達相當金額</b>，<b class="k">經定相當期間催告仍不給付</b>者，管理負責人或管委會得<b class="k">訴請法院命其給付</b>應繳金額<b>及遲延利息</b>（<span class="law">§21</span>）。此為<b>給付之訴</b>，與 §22 的<b>遷離／出讓</b>是兩回事。</p>
<div class="mn"><b>口訣〔自編〕：</b>「<b>欠兩期先催告告給付（§21）；再積欠達 1% 才趕人（§22）</b>」。§21 不需區權會決議，§22 <b>一定要</b>區權會決議。</div>
<div class="tr"><b>考試陷阱：</b>①§21 的門檻是「逾<b>二期</b>或達相當金額」＋「定相當期間<b>催告</b>」，缺催告就起訴會被挑錯。②§22Ⅰ① 是「<b>經強制執行後『再度』積欠</b>」達總價 1%，不是第一次欠到 1% 就能趕人。③促請改善是「<b>3 個月</b>」，不是 1 個月、不是 6 個月。④出讓判決確定後「<b>3 個月</b>內不自行出讓」才能聲請拍賣。⑤拍賣所得受償順序與<b>第一順位抵押權同</b>（不是優先於、也不是次於）。⑥違反 §16Ⅰ、Ⅳ 走 §47（3千～1萬5），違反 §16Ⅱ、Ⅲ 走 §49（4萬～20萬）——<b>同一條不同項，罰鍰差一個數量級</b>，這是 E5 最愛考的切點。</div>
''')

# ⑤ 公共基金與點交
sec('p5', 'E', '⑤ 公共基金與點交：提列 → 成立管委會 → 點交 → 撥付', '公寓§18、§20、§28、§57、§58、§49', '''
<div class="sub2">六步流程</div>
<ol class="flow">
<li><b>起造人提列</b>：公共基金來源四款——①起造人就公寓大廈<b class="k">領得使用執照一年內</b>之管理維護事項，應按<b class="k">工程造價一定比例或金額提列</b>；②區分所有權人依區權會決議繳納；③本基金之<b>孳息</b>；④其他收入（<span class="law">§18Ⅰ</span>）。</li>
<li><b>繳交證明</b>：依①提列之公共基金，起造人於<b class="k">使用執照申請時</b>，應提出繳交各直轄市、縣（市）主管機關<b class="k">公庫代收</b>之證明（<span class="law">§18Ⅱ</span>）。</li>
<li><b>成立管理組織</b>：建築物所有權登記之區分所有權人達<b class="k">半數以上及其區分所有權比例合計半數以上</b>時，起造人應於 <span class="n">3個月</span> 內召集區權會，<b class="k">成立管理委員會或推選管理負責人</b>，並向主管機關<b class="k">報備</b>（<span class="law">§28Ⅰ</span>）。起造人為數人時應互推一人為之；出席未達 §31 定額而未能成立管委會者，起造人應<b class="k">就同一議案重新召集會議一次</b>（<span class="law">§28Ⅱ</span>）。成立前，<b class="k">起造人為公寓大廈之管理負責人</b>（<span class="law">§28Ⅲ</span>）。</li>
<li><b>檢測與點交</b>：起造人應將共用部分、約定共用部分與其附屬設施設備，及使用維護手冊、廠商資料、使用執照謄本、竣工圖說、水電機械消防及管線圖說，於<b class="k">管委會成立或管理負責人推選或指定後 7 日內</b>，<b class="k">會同政府主管機關</b>、管委會或管理負責人<b>現場</b>針對水電、機械設施、消防設施及各類管線<b class="k">進行檢測</b>，確認功能正常無誤後移交（<span class="law">§57Ⅰ</span>）。</li>
<li><b>檢測不過怎麼辦</b>：不能通過檢測或功能有明顯缺陷者，管委會或管理負責人<b class="k">得報請主管機關處理</b>；<b class="k">歸責起造人者</b>，主管機關命起造人負責修復改善，並於 <span class="n">1個月</span> 內再會同辦理移交（<span class="law">§57Ⅱ</span>）。</li>
<li><b>公庫撥付</b>：於成立管委會或推選管理負責人，<b class="k">並完成依 §57 點交</b>共用部分、約定共用部分及其附屬設施設備後<b class="k">向主管機關報備</b>，由<b class="k">公庫代為撥付</b>（<span class="law">§18Ⅱ</span>）。公共基金應<b class="k">設專戶儲存</b>，由管理負責人或管委會負責管理；經區權會決議<b>交付信託</b>者，由其交付信託；<b class="k">運用應依區權會之決議</b>為之（<span class="law">§18Ⅲ</span>）。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>「<b>執照提列 → 過半召集 → 成立 7 日點交 → 報備公庫撥付</b>」。四個關卡少一個，公庫就不撥款。</div>
<div class="tr"><b>考試陷阱：</b>①起造人召集第一次區權會的門檻是「<b>登記區分所有權人過半數『且』比例合計過半數</b>」，兩個都要。②期限是「<b>3 個月</b>內召集」、「成立後 <b>7 日</b>內點交」、「修復後 <b>1 個月</b>內再移交」——三個數字常互換。③提列基準是「<b>工程造價</b>一定比例或金額」，不是「房屋總價」。④公共基金<b class="k">運用</b>要依區權會決議；住戶想拿去投資，須經區權會決議且不得違反 §18Ⅲ 的專戶／信託規定。⑤<b>本條例公布施行前起造人已取得建造執照者，不適用</b>提列義務（§18Ⅳ）。⑥起造人違反 §57、§58 → §49Ⅰ⑧，罰 <b>4 萬～20 萬</b>；區分所有權人未依區權會決議繳納公共基金 → §49Ⅰ⑥，同樣 4 萬～20 萬。</div>
''')

# ⑥ 消費爭議階梯
sec('p6', 'H', '⑥ 消費爭議階梯：申訴 → 再申訴 → 調解 → 消訴／團體訴訟', '消保§43～§47、§49、§50、§53', '''
<div class="sub2">四階救濟</div>
<ol class="flow">
<li><b>第一次申訴</b>：消費者與企業經營者因商品或服務發生消費爭議時，得向<b class="k">企業經營者、消費者保護團體或消費者服務中心（或其分中心）</b>申訴（<span class="law">§43Ⅰ</span>）。企業經營者對於消費者之申訴，應於<b class="k">申訴之日起 15 日內</b>妥適處理（<span class="law">§43Ⅱ</span>）。</li>
<li><b>第二次申訴（再申訴）</b>：依第一項申訴<b class="k">未獲妥適處理</b>時，得向<b class="k">直轄市、縣（市）政府消費者保護官</b>申訴（<span class="law">§43Ⅲ</span>）。</li>
<li><b>調解</b>：申訴未能獲得妥適處理時，得向<b class="k">直轄市或縣（市）消費爭議調解委員會</b>申請調解（<span class="law">§44</span>）。調解委員會置委員 <b class="k">7 名至 21 名</b>，由縣市政府代表、消保官、消保團體代表、企業經營者所屬或相關職業團體代表、學者及專家充任，<b class="k">以消費者保護官為主席</b>（<span class="law">§45</span>）。程序<b class="k">得不公開</b>，經辦人員應<b>保守秘密</b>（<span class="law">§45-1</span>）。調解成立應<b class="k">作成調解書</b>，其作成及效力<b class="k">準用鄉鎮市調解條例§25～§29</b>（<span class="law">§46</span>）。</li>
<li><b>訴訟</b>：消費訴訟<b class="k">得由消費關係發生地之法院管轄</b>（<span class="law">§47</span>）。另有兩種團體訴訟：<b>損害賠償訴訟</b>——消保團體對同一原因事件致<b class="k">眾多消費者</b>受害時，得<b class="k">受讓 20 人以上</b>消費者損害賠償請求權後，以<b>自己名義</b>提起（<span class="law">§50Ⅰ</span>）；<b>不作為訴訟</b>——<b class="k">消保官或消保團體</b>就企業經營者<b class="k">重大違反</b>本法有關保護消費者規定之行為，得向法院訴請停止或禁止之，<b class="k">免繳裁判費</b>（<span class="law">§53</span>）。</li>
</ol>
<div class="sub2">消保團體提訴的三個門檻（§49Ⅰ）</div>
<ul class="pl">
<li>許可設立<b class="k">二年以上</b>；</li>
<li>置有<b class="k">消費者保護專門人員</b>；</li>
<li>申請<b class="k">行政院評定優良</b>。三者齊備，始得以自己名義提起 §50 損害賠償訴訟或 §53 不作為訴訟，且<b class="k">應委任律師</b>代理訴訟（§49Ⅱ）。</li>
</ul>
<div class="mn"><b>口訣〔自編〕：</b>「<b>一申企團中心、二申消保官、三調解、四起訴</b>」；數字是「<b>15 日處理、7～21 名委員、20 人受讓、2 年設立</b>」。</div>
<div class="tr"><b>考試陷阱：</b>①第一次申訴的對象<b class="k">不含消保官</b>（消保官是第二階）；也<b>不含內政部</b>。②§50 受讓是「<b>20 人以上</b>」，中途有人終止讓與<b>致人數不足 20 人者，不影響</b>其實施訴訟之權能（§50Ⅱ）。③提起 §50、§53 訴訟的門檻在 <b>§49</b>（設立 2 年＋專門人員＋行政院評定優良），<b class="k">不是「經消保官同意」</b>——這是 99-25 的陷阱。④§53 不作為訴訟的原告是「<b>消保官『或』消保團體</b>」，不是只有消保團體。⑤消費訴訟管轄是「<b>得由</b>消費關係發生地法院管轄」（選擇管轄），不是「專屬」。⑥調解書效力是<b>準用鄉鎮市調解條例</b>，不是直接等同確定判決。</div>
''')

# ⑦ 公平會調查裁處
sec('p7', 'G', '⑦ 公平會調查裁處：檢舉／職權 → 調查 → 中止或裁處 → 按次', '公平§26～§28、§34、§35、§40', '''
<div class="sub2">五步流程</div>
<ol class="flow">
<li><b>發動</b>：主管機關對於涉有違反本法規定、<b class="k">危害公共利益</b>之情事，得依<b class="k">檢舉或職權</b>調查處理（<span class="law">§26</span>）。</li>
<li><b>調查三手段</b>：①<b>通知</b>當事人及關係人到場陳述意見；②<b>通知</b>提出帳冊、文件及其他必要資料或證物；③<b>派員前往</b>當事人及關係人之事務所、營業所或其他場所為必要之調查（<span class="law">§27Ⅰ</span>）。調查所得可為證據之物<b class="k">得扣留</b>，範圍及期間以保全證據目的所必要者為限（§27Ⅱ）。受調查者<b class="k">無正當理由不得規避、妨礙或拒絕</b>（§27Ⅲ）；執行人員<b class="k">應出示證明文件，未出示者受調查者得拒絕</b>（§27Ⅳ）。</li>
<li><b>中止調查（承諾制）</b>：事業承諾在所定期限內採取具體措施<b>停止並改正</b>涉有違法行為者，主管機關<b class="k">得中止調查</b>並監督履行；已履行者<b>得終止調查</b>。但有三款<b class="k">應恢復調查</b>：未履行承諾、所依據事實發生重大變化、承諾係基於不完整或不真實之資訊（<span class="law">§28Ⅰ～Ⅲ</span>）。<b class="k">裁處權時效自中止調查之日起停止進行</b>；恢復調查者，自恢復之翌日起與停止前已經過期間<b>一併計算</b>（§28Ⅳ）。</li>
<li><b>裁處</b>：對違反 §9（獨占）、§15（聯合）、§19、§20 之事業，<b class="k">得限期令停止、改正其行為或採取必要更正措施，並得處 10 萬～5,000 萬元罰鍰</b>；屆期仍不停止改正者，<b class="k">得繼續限期令停止改正，並按次處 20 萬～1 億元</b>，至停止改正為止（<span class="law">§40Ⅰ</span>）。違反 §9、§15 經認定<b class="k">情節重大</b>者，得處該事業<b class="k">上一會計年度銷售金額 10% 以下</b>罰鍰，不受前項金額限制（§40Ⅱ）。</li>
<li><b>刑事後手</b>：違反 §9 或 §15，經依 §40Ⅰ 限期令停止改正而<b class="k">屆期未停止改正，或停止後再為相同違反行為</b>者，處行為人<b class="k">3 年以下有期徒刑</b>、拘役或科或併科 <b class="k">1 億元以下罰金</b>（<span class="law">§34</span>）。</li>
</ol>
<div class="mn"><b>口訣〔自編〕：</b>「<b>先行政、後刑事</b>」——公平法對獨占、聯合是<b>行政先行</b>，一定要先有 §40Ⅰ 的限期令停止，屆期不改或再犯才進 §34 刑責。</div>
<div class="tr"><b>考試陷阱：</b>①§26 是「<b>得</b>依檢舉或職權調查」，不是「應」；且限於<b>危害公共利益</b>之情事。②調查人員<b class="k">未出示證明文件，受調查者得拒絕</b>——這一句常被改成「仍不得拒絕」。③中止調查後<b class="k">裁處權時效停止進行</b>，恢復後與先前期間<b>一併計算</b>（不是重新起算）。④§40Ⅰ 首罰上限 <b>5,000 萬</b>、按次 <b>20 萬～1 億</b>；情節重大另有<b>銷售金額 10%</b>。⑤<b>窩裡反減免</b>（§35）適用對象限<b class="k">違反 §15（聯合行為）</b>之事業，且須<b class="k">經主管機關事先同意</b>；獨占不適用。⑥罰鍰的「停止營業」處分每次以 <b>6 個月</b>為限（§39Ⅳ），那是<b>結合</b>違規的後手處分，別跟 §40 混。</div>
''')

# ⑧ 結合管制
sec('p8', 'G', '⑧ 結合管制：申報門檻 → 等待期 → 不禁止或附款 → 未申報的後果', '公平§10～§13、§39', '''
<div class="sub2">什麼叫「結合」（§10Ⅰ 五款）</div>
<ul class="pl">
<li>①與他事業<b>合併</b>；②持有或取得他事業股份或出資額<b class="k">達到有表決權股份總數或資本總額 1/3 以上</b>；③<b>受讓或承租</b>他事業全部或主要部分之營業或財產；④與他事業<b>經常共同經營</b>或<b>受他事業委託經營</b>；⑤<b>直接或間接控制</b>他事業之業務經營或人事任免。</li>
<li>計算第②款時，應將<b class="k">具控制從屬關係之事業、受同一事業控制之從屬事業</b>所持有或取得之股份一併計入（§10Ⅱ）。</li>
</ul>
<div class="sub2">五步流程</div>
<ol class="flow">
<li><b>判斷是否須申報（§11Ⅰ 三款）</b>：①結合後<b class="k">市場占有率達 1/3</b>；②參與結合之<b class="k">一事業市場占有率達 1/4</b>；③參與結合事業<b class="k">上一會計年度銷售金額超過主管機關公告之金額</b>。三者有一即<b class="k">應先向主管機關提出申報</b>。</li>
<li><b>例外不適用（§12 六款）</b>：①已持有他事業<b class="k">50% 以上</b>有表決權股份，再與該他事業結合；②<b>同一事業</b>持股 50% 以上之事業<b>彼此間</b>結合；③將全部或主要部分營業、財產或可獨立營運之營業，讓與其<b class="k">獨自新設</b>之他事業；④依公司法§167Ⅰ但書或證交法§28-2 <b>收回股東所持股份</b>致原有股東符合§10Ⅰ②；⑤單一事業轉投資成立並持有 <b class="k">100%</b> 股份之子公司；⑥其他經主管機關公告之類型。</li>
<li><b>等待期</b>：事業自主管機關<b class="k">受理完整申報資料之日起算 30 工作日</b>內<b class="k">不得為結合</b>；主管機關認為必要時得將該期間<b class="k">縮短或延長</b>，並以書面通知（<span class="law">§11Ⅶ</span>）。<b class="k">延長之期間不得逾 60 工作日</b>，對延長期間之案件應依 §13 作成決定（§11Ⅷ）。</li>
<li><b>屆期未通知＝得逕行結合</b>：主管機關屆期未為延長通知或未作成決定者，事業<b class="k">得逕行結合</b>；但①經申報事業同意<b>再延長</b>期間、②申報事項<b>有虛偽不實</b>者，不得逕行結合（<span class="law">§11Ⅸ</span>）。</li>
<li><b>實體標準與附款</b>：結合對<b class="k">整體經濟利益大於限制競爭之不利益</b>者，主管機關<b class="k">不得禁止</b>其結合（<span class="law">§13Ⅰ</span>）；所為決定<b class="k">得附加條件或負擔</b>（§13Ⅱ）。</li>
</ol>
<div class="sub2">違反的後果（§39）</div>
<ul class="pl">
<li>未申報而結合、違反等待期、經禁止仍結合、未履行所附負擔 → 得<b class="k">禁止結合、限期令分設事業、處分全部或部分股份、轉讓部分營業、免除擔任職務或其他必要處分</b>，並得處 <b class="k">20 萬～5,000 萬元</b>罰鍰（§39Ⅰ）。</li>
<li>申報事項<b>虛偽不實</b>而結合 → 同上處分，罰 <b class="k">10 萬～100 萬元</b>（§39Ⅱ）。</li>
<li>違反上開處分 → 得<b class="k">命令解散、勒令歇業或停止營業</b>；停止營業之期間<b class="k">每次以 6 個月為限</b>（§39Ⅲ、Ⅳ）。</li>
</ul>
<div class="mn"><b>口訣〔自編〕：</b>結合是「<b>申報制</b>」不是「許可制」；門檻「<b>三分之一、四分之一、公告金額</b>」；等待「<b>30 工作日，延長不逾 60 工作日</b>」；例外記「<b>50%、100%、獨自新設、收回股份</b>」。</div>
<div class="tr"><b>考試陷阱：</b>①題幹若寫「向中央主管機關<b>申請許可</b>」就是錯的，現行法是<b class="k">事前申報</b>（舊法才是許可制，99 年、104 年舊題的「許可」用語要用現行法讀）。②期間單位是「<b class="k">工作日</b>」不是「日」。③§10Ⅰ② 的門檻是 <b>1/3</b>（結合定義）；§11Ⅰ① 的門檻是 <b>1/3</b>（市占率）、② 是 <b>1/4</b>——定義與申報門檻的數字容易混。④§12① 是「已持有<b>他事業</b> 50% 以上再與<b>該他事業</b>結合」，不是跟任何第三事業。⑤§13Ⅰ 是「<b>不得禁止</b>」（雙重否定），不是「得許可」。⑥罰鍰級距：一般 <b>20 萬～5,000 萬</b>、虛偽不實 <b>10 萬～100 萬</b>，兩者方向相反（虛偽不實反而比較低），常被對調。</div>
''')

# ⑨ 聯合行為許可
sec('p9', 'G', '⑨ 聯合行為：原則禁止 → 八款例外 → 許可期限 → 延展與減免', '公平§14～§16、§34、§35、§40', '''
<div class="sub2">什麼叫「聯合行為」（§14）</div>
<ul class="pl">
<li>指<b class="k">具競爭關係之同一產銷階段事業</b>，以<b>契約、協議或其他方式之合意</b>，共同決定商品或服務之<b>價格、數量、技術、產品、設備、交易對象、交易地區</b>或其他相互約束事業活動之行為，而<b class="k">足以影響生產、商品交易或服務供需之市場功能</b>者（§14Ⅰ）。</li>
<li>「其他方式之合意」指契約、協議以外之<b class="k">意思聯絡，不問有無法律拘束力</b>，事實上可導致共同行為者（§14Ⅱ）。合意得依<b class="k">市場狀況、商品特性、成本及利潤考量、經濟合理性</b>等相當依據之因素<b class="k">推定</b>之（§14Ⅲ）。</li>
<li><b class="k">同業公會</b>或其他團體藉<b>章程、會員大會、理監事會議決議或其他方法</b>所為約束事業活動之行為，<b>亦為</b>聯合行為（§14Ⅳ）。</li>
</ul>
<div class="sub2">四步流程</div>
<ol class="flow">
<li><b>原則禁止</b>：事業不得為聯合行為（<span class="law">§15Ⅰ</span>本文）。</li>
<li><b>例外八款＋兩要件</b>：須<b class="k">有益於整體經濟與公共利益</b>，<b class="k">並經申請主管機關許可</b>。八款為：①統一規格型式（降低成本、改良品質或增進效率）②共同研究開發③<b>專業發展</b>（分別作專業發展，促進合理經營）④確保或促進<b>輸出</b>，專就國外市場競爭予以約定⑤加強貿易效能，就國外商品或服務<b>輸入</b>採共同行為⑥<b class="k">經濟不景氣</b>，難以維持或生產過剩，有計畫適應需求而限制產銷數量、設備或價格⑦增進<b class="k">中小企業</b>經營效率或加強競爭能力⑧其他為促進產業發展、技術創新或經營效率所必要（<span class="law">§15Ⅰ①～⑧</span>）。</li>
<li><b>決定期限</b>：主管機關收受申請，應於 <span class="n">3個月</span> 內為決定；<b class="k">必要時得延長一次</b>（<span class="law">§15Ⅱ</span>）。</li>
<li><b>許可期限與延展</b>：許可<b class="k">得附加條件或負擔</b>；<b class="k">應附期限，不得逾 5 年</b>；有正當理由者，得於<b class="k">期限屆滿前 3 個月至 6 個月期間內</b>以書面申請延展，<b class="k">每次延展不得逾 5 年</b>（<span class="law">§16</span>）。</li>
</ol>
<div class="sub2">違反的後果</div>
<ul class="pl">
<li>行政：§40Ⅰ 限期令停止改正＋<b class="k">10 萬～5,000 萬</b>；屆期不改按次 <b class="k">20 萬～1 億</b>。情節重大者得處<b class="k">上一會計年度銷售金額 10% 以下</b>（§40Ⅱ）。</li>
<li>刑事：經限期令停止改正而<b class="k">屆期未改或停止後再為相同違反行為</b> → 行為人 <b class="k">3 年以下有期徒刑</b>、拘役或科或併科 <b class="k">1 億元以下罰金</b>（§34）。</li>
<li>減免（窩裡反，§35）：①<b class="k">尚未為主管機關知悉或調查前</b>，就所參與之聯合行為提出<b>書面檢舉或陳述具體違法</b>並<b>檢附事證及協助調查</b>；②<b class="k">調查期間</b>陳述具體違法並檢附事證及協助調查。<b class="k">經主管機關事先同意</b>者，免除或減輕 §40Ⅰ、Ⅱ 之罰鍰。</li>
</ul>
<div class="mn"><b>口訣〔自編〕：</b>許可「<b>3 個月決定、延長一次</b>」；期限「<b>5 年</b>」；延展「<b>屆滿前 3～6 個月申請，每次不逾 5 年</b>」。三個 3、兩個 5。</div>
<div class="tr"><b>考試陷阱：</b>①延展申請的時間窗是「<b class="k">屆滿前 3 個月至 6 個月期間內</b>」，不是「屆滿前 3 個月內」、也不是「屆滿後」。②「<b>延長一次</b>」講的是<b>主管機關決定期間</b>（§15Ⅱ），「<b>每次不逾 5 年</b>」講的是<b>延展次數不限</b>（§16Ⅱ）——兩個「一次／每次」常被對調。③聯合行為限「<b class="k">同一產銷階段</b>」之<b>水平</b>競爭者；上下游的垂直約定走 §19、§20，不是 §14。④<b>同業公會的決議</b>也是聯合行為（§14Ⅳ）——不動產仲介公會共同約束服務報酬或委託契約型態，就是典型違法態樣。⑤八款例外一定要<b class="k">「並經申請主管機關許可」</b>，只符合八款但沒申請仍然違法。⑥§35 窩裡反只適用<b>聯合行為</b>，且須<b>事先同意</b>。</div>
''')

# ⑩ 說明書簽章
sec('p10', 'C', '⑩ 不動產說明書：簽章 → 解說 → 交付 → 視為契約一部', '條例§22～§24、§24-2、§29、§31', '''
<div class="sub2">六類應由經紀人簽章之文件（§22Ⅰ）</div>
<div class="tw rc"><table style="min-width:600px"><thead><tr><th style="width:8%">款次</th><th style="width:46%">文件</th><th>代銷經紀業</th></tr></thead><tbody>
<tr><td>一</td><td>不動產<b>出租、出售委託契約書</b></td><td><b class="k">不適用</b>（§22Ⅱ）</td></tr>
<tr><td>二</td><td>不動產<b>承租、承購要約書</b></td><td><b class="k">不適用</b>（§22Ⅱ）</td></tr>
<tr><td>三</td><td><b>定金收據</b></td><td>適用</td></tr>
<tr><td>四</td><td>不動產<b>廣告稿</b></td><td>適用</td></tr>
<tr><td>五</td><td>不動產<b>說明書</b></td><td>適用</td></tr>
<tr><td>六</td><td>不動產<b>租賃、買賣契約書</b></td><td>適用</td></tr>
</tbody></table></div>
<p style="font-size:13.5px;margin-top:6px">第五款之不動產說明書<b>應記載及不得記載事項</b>，由<b class="k">中央主管機關</b>定之（§22Ⅲ）。</p>
<div class="sub2">四步時序</div>
<ol class="flow">
<li><b>製作與簽章</b>：經紀業<b class="k">指派經紀人</b>在六類文件上簽章（<span class="law">§22Ⅰ</span>）。</li>
<li><b>委託人先簽章</b>：說明書<b class="k">於提供解說前，應經委託人簽章</b>（<span class="law">§23Ⅱ</span>）。</li>
<li><b>向相對人解說</b>：經紀人員在執行業務過程中，<b class="k">應以不動產說明書向與委託人交易之相對人解說</b>（<span class="law">§23Ⅰ</span>）。</li>
<li><b>簽約時交付＋相對人簽章</b>：雙方當事人簽訂租賃或買賣契約書時，經紀人應將說明書<b class="k">交付與委託人交易之相對人</b>，並由<b class="k">相對人在說明書上簽章</b>；該說明書<b class="k">視為租賃或買賣契約書之一部分</b>（<span class="law">§24</span>）。</li>
</ol>
<div class="sub2">相關：雙方代理與申報登錄</div>
<ul class="pl">
<li><b>雙方代理（§24-2）</b>：經營仲介業務者經買賣或租賃雙方當事人之<b class="k">書面同意</b>，得同時接受雙方委託，並應①公平提供雙方類似不動產之<b>交易價格</b>②公平提供<b>契約內容規範</b>之說明③提供買受人或承租人<b>必要資訊</b>④告知依仲介專業<b>應查知之瑕疵</b>⑤協助進行<b>必要之檢查</b>⑥其他中央主管機關規定。</li>
<li><b>申報登錄（§24-1）</b>：仲介之<b class="k">租賃</b>案件 → 簽訂租賃契約書之日起 <span class="n">30日</span> 內申報登錄；代銷<b class="k">預售屋</b> → 簽訂、變更或終止委託代銷契約之日起 <span class="n">30日</span> 內<b>報備</b>，並於簽訂<b>買賣契約書</b>之日起 <span class="n">30日</span> 內申報登錄。</li>
</ul>
<div class="sub2">違反的雙軌後果</div>
<ul class="pl">
<li><b>對經紀業</b>：違反 §22Ⅰ → <b class="k">6 萬～30 萬</b>罰鍰（§29Ⅰ①），並應令限期改正，屆期未改<b>按次處罰</b>（§29Ⅱ）。</li>
<li><b>對經紀人員</b>：違反 §16、<b>§22Ⅰ</b>、§23、§25 → <b class="k">申誡</b>（§31Ⅰ①）；申誡 <b>3 次</b>另予 6 個月以上 3 年以下停業，停業累計達 <b>5 年</b>以上廢止證書或證明（§31Ⅱ）。</li>
</ul>
<div class="mn"><b>口訣〔自編〕：</b>「<b>委託人<u>先</u>簽 → 解說 → 簽約時交付 → 相對人<u>後</u>簽</b>」。誰先誰後是本題組唯一的核心。</div>
<div class="tr"><b>考試陷阱：</b>①<b class="k">委託人簽章在「解說前」，相對人簽章在「簽約時」</b>——兩個簽章的時點與對象常被對調。②代銷不適用的是<b class="k">第①、②款</b>（委託契約書、要約書），<b>不含</b>定金收據與廣告稿。③「視為<b>契約書之一部分</b>」是 §24Ⅱ 的法律效果，不是「視為要約」「視為廣告」。④說明書的解說義務在<b class="k">經紀人員</b>（含營業員），簽章義務在<b class="k">經紀人</b>——103-2 就是拆這一刀。⑤違反 §22Ⅰ 是<b class="k">業者罰鍰＋人員申誡「雙罰」</b>，只答一邊會被扣分（114-18 的考點）。⑥收取差價或其他報酬（§19Ⅰ）對人員是<b>停業 6 個月～3 年</b>，不是申誡——申誡與停業的分界要背熟。</div>
''')

# 考古題
FIL = '<button class="on" data-g="all">全部 %d</button>' % len(QD) + ''.join(
    '<button data-g="%s">%s %d</button>' % (p, PNAME[p].split(' ')[1], len(PICK[p])) for p in PICK)
sec('tq', 'A', '⑪ 考古題：程序相關 %d 題' % len(QD), '%d 題' % len(QD), '''
<p style="font-size:13px;color:var(--muted)">依十大程序分組。作答後顯示逐選項解析（與《法條解析練習》同一份）；每題右上角可跳到解析練習頁的同一題，在那裡標錯誤類型 A／B／C／D。</p>
<div class="fil" id="fil">%s</div>
<div class="score" id="score"></div>
<div id="qlist"></div>
''' % FIL, open_=True)

BODY = '\n\n'.join(S)

NAV = ('<nav><a href="#t0">⓪ 總比較表</a>' +
       ''.join('<a href="#p%d">%s</a>' % (i + 1, PNAME['P%d' % (i + 1)]) for i in range(10)) +
       '<a href="#tq">⑪ 考古題</a></nav>')

HTML = '''<!DOCTYPE html><html lang="zh-Hant"><head><script>/*bxdef*/(function(){var s=null;try{s=localStorage.getItem('bx-theme')}catch(e){}document.documentElement.setAttribute('data-theme',s||'light')})();</script><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>經紀法規程序總整理</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap"><style>%s</style></head><body>
<header><button class="theme" id="themeBtn" aria-label="切換深淺色">☀️</button><h1>經紀法規概要｜程序總整理</h1><div class="sub">經紀業・經紀人員・區權會・住戶違規・基金點交・消費爭議・公平會・結合・聯合・說明書｜10 大程序＋考古 %d 題</div></header>
%s
<main>
<div class="intro"><b>怎麼讀：</b>先看 ⓪ 總比較表，把十個程序的「誰啟動、幾天、誰決定、不做會怎樣」橫著比一次；再依弱點展開單一程序。條文依站內條文庫逐字（全國法規資料庫現行法）；口訣標〔自編〕。各程序末段的「考試陷阱」是歷屆實際被拆過的切點。</div>
<div class="tools"><button id="ea">全部展開</button><button id="ca">全部收合</button></div>

%s

<p class="foot">本頁為備考整理，非法規原文。條文來源：不動產經紀業管理條例及其施行細則、公寓大廈管理條例、消費者保護法、公平交易法（全國法規資料庫現行條文，站內條文庫逐字）。考前以紙本六法為準。</p>
</main>
<script>
var QUIZ=%s;
var QD=%s;
(function(){var L=['A','B','C','D'],box=document.getElementById('qlist'),ok=0,done=0;
function sc(){document.getElementById('score').textContent=done?('已作答 '+done+'／'+QD.length+'，答對 '+ok):''}
QD.forEach(function(d){var w=document.createElement('div');w.className='qz';
 var h='<div class="qh"><span>【'+d.y+'】</span><span>'+d.g+'</span><a href="'+QUIZ+'#q='+d.k+'" target="_blank" rel="noopener">到解析練習 ↗</a></div><div class="qt">'+d.q+'</div>';
 d.o.forEach(function(o,i){h+='<button class="op" data-i="'+i+'"><b>'+L[i]+'</b><span>'+o+'</span></button>'});
 h+='<div class="ex">';d.e.forEach(function(e,i){h+='<div><span class="'+(i===d.c?'y':'x')+'">'+L[i]+(i===d.c?' ✓ 正解':' ✗')+'</span> '+e+'</div>'});h+='</div>';
 w.innerHTML=h;w.dataset.gr=d.gr;box.appendChild(w);
 w.querySelectorAll('.op').forEach(function(b){b.onclick=function(){if(w.classList.contains('done'))return;var i=+b.dataset.i;w.classList.add('done');done++;if(i===d.c)ok++;
  w.querySelectorAll('.op')[d.c].classList.add('ok');if(i!==d.c)b.classList.add('ng');sc()}})});
var fb=document.getElementById('fil');if(fb)fb.onclick=function(ev){var b=ev.target.closest('button');if(!b)return;fb.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});var g=b.dataset.g;box.querySelectorAll('.qz').forEach(function(q){q.hidden=g!=='all'&&q.dataset.gr!==g})};
document.querySelectorAll('.rc table').forEach(function(t){var h=[].map.call(t.querySelectorAll('thead th'),function(x){return x.textContent});t.querySelectorAll('tbody tr').forEach(function(r){[].forEach.call(r.children,function(td,i){td.setAttribute('data-l',h[i]||'')})})});
document.querySelectorAll('ol.flow').forEach(function(ol,k){var lis=[].slice.call(ol.children);if(!lis.length||!lis.every(function(li){return li.firstElementChild&&li.firstElementChild.tagName==='B'}))return;var d=document.createElement('div');d.className='steps';d.innerHTML=lis.map(function(li,i){li.id='st'+k+'_'+i;return '<a href="#st'+k+'_'+i+'">'+'①②③④⑤⑥⑦⑧⑨⑩'[i]+' '+li.firstElementChild.textContent+'</a>'}).join('<i>→</i>');ol.parentNode.insertBefore(d,ol)});
document.getElementById('ea').onclick=function(){document.querySelectorAll('details.sec').forEach(function(x){x.open=true})};
document.getElementById('ca').onclick=function(){document.querySelectorAll('details.sec').forEach(function(x){x.open=false})};
var tb=document.getElementById('themeBtn');function ub(){tb.textContent=document.documentElement.getAttribute('data-theme')==='dark'?'🌙':'☀️'}ub();
tb.onclick=function(){var h=document.documentElement,n=h.getAttribute('data-theme')==='dark'?'light':'dark';h.setAttribute('data-theme',n);try{localStorage.setItem('bx-theme',n)}catch(e){}ub()};
if(location.hash){var el=document.querySelector(location.hash);if(el){var p=el.closest('details.sec');if(p)p.open=true;setTimeout(function(){el.scrollIntoView()},60)}}
})();
</script>
<!--bxfab-->
<style>
#bxfab{--fp:#2F5D50;--fs:#FFFEFA;--fo:#FFFFFF;--fl:#DDD6C0;position:fixed;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom,0px));padding:0 12px;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none;z-index:60}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}}
:root[data-theme="dark"] #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}
#bxfab>*{pointer-events:auto}
#bxfab .bx-up{position:relative;width:40px;height:40px;border-radius:50%%;border:0;background:var(--fs);color:var(--fp);padding:0;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.22);cursor:pointer;opacity:.4;transition:opacity .25s}
#bxfab .bx-up.act{opacity:1}
#bxfab .bx-up .rg{position:absolute;inset:0;width:100%%;height:100%%}
#bxfab .bx-up .rg circle{fill:none;stroke-width:3}
#bxfab .bx-up .rg .t{stroke:var(--fl)}#bxfab .bx-up .rg .p{stroke:var(--fp);stroke-linecap:round;transform:rotate(-90deg);transform-origin:center;transition:stroke-dashoffset .1s}
#bxfab svg.ic{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;position:relative}
#bxfab .bx-hub{width:40px;height:40px;border-radius:50%%;background:var(--fp);color:var(--fo);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.25);text-decoration:none}
#bxfab .bx-hub svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
</style>
<div id="bxfab"><button class="bx-up" id="navUp" aria-label="回到最上方" onclick="window.scrollTo({top:0,behavior:'smooth'})"><svg class="rg" viewBox="0 0 44 44"><circle class="t" cx="22" cy="22" r="19"/><circle class="p" cx="22" cy="22" r="19" stroke-dasharray="119.4" stroke-dashoffset="119.4"/></svg><svg class="ic" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button><a class="bx-hub" href="%s" aria-label="回備考指揮中心" title="回備考指揮中心"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10"/></svg></a></div>
<script>(function(){var b=document.querySelector("#bxfab .bx-up"),p=b.querySelector(".p");function f(){var h=document.documentElement,m=h.scrollHeight-window.innerHeight,y=window.scrollY||0,r=m>0?Math.min(1,y/m):0;p.setAttribute("stroke-dashoffset",(119.4*(1-r)).toFixed(1));b.classList.toggle("act",y>160)}window.addEventListener("scroll",f,{passive:true});window.addEventListener("resize",f);f();var bar=document.getElementById("bxfab"),vv=window.visualViewport;function z(){if(!vv||!bar)return;var s=vv.scale;if(s<=1.02){bar.style.transform="";bar.style.transformOrigin="";return}var lh=document.documentElement.clientHeight;bar.style.transformOrigin="left bottom";bar.style.transform="translate("+vv.offsetLeft+"px,"+(vv.offsetTop+vv.height-lh)+"px) scale("+(1/s)+")"}if(vv){vv.addEventListener("resize",z);vv.addEventListener("scroll",z);z()}})();</script>
<!--/bxfab-->
</body></html>''' % (CSS, len(QD), NAV, BODY,
                     json.dumps(QUIZ, ensure_ascii=False),
                     json.dumps(QD, ensure_ascii=False, separators=(',', ':')),
                     HUB)

dst = ROOT + '/經紀法規_程序總整理.html'
io.open(dst, 'w', encoding='utf-8').write(HTML)
print('已產生 經紀法規_程序總整理.html', len(HTML) // 1024, 'KB｜考古題', len(QD), '題')
