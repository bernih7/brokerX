# 估價申論「N 型答題模板」頁產生器（可重跑）
# 讀《不動產估價概要_申論題實戰範文.html》的官方 e年-題 卡（題目 .q-box、考場版 .exam-ver），
# 依下方 TYPES 歸型；各型題數、總題數、檔名 N 皆由卡片算出。範例＝該卡考場版原文（不改寫）。
# 用法：python3 tools/essay_val/template/gen_tpl.py
import re, os, html, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
SRC_NAME = '不動產估價概要_申論題實戰範文.html'
s = open(os.path.join(ROOT, SRC_NAME), encoding='utf-8').read()
CN = '零一二三四五六七八九十'


def card_blocks():
    out = {}
    starts = [m for m in re.finditer(r'<div class="essay-card"[^>]*\bid="([^"]+)"', s)]
    for k, m in enumerate(starts):
        en = starts[k + 1].start() if k + 1 < len(starts) else len(s)
        out[m.group(1)] = s[m.start():en]
    return out


def balanced_div(b, start):
    """回傳從 start 起第一個 <div ...> 到其對應 </div> 的完整片段。"""
    depth = 0
    for t in re.finditer(r'<div\b[^>]*>|</div>', b[start:]):
        depth += 1 if t.group(0) != '</div>' else -1
        if depth == 0:
            return b[start:start + t.end()]
    raise ValueError('unbalanced div')


B = card_blocks()
OFF = {}
for cid, b in B.items():
    m = re.fullmatch(r'e(\d+)-(\d)', cid)
    if not m:
        continue
    q = re.search(r'<div class="q-box">(.*?)</div>', b, re.S).group(1)
    q = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', q)).replace('【原題】', '').strip()
    t = re.sub(r'<[^>]+>', '', re.search(r'class="card-title">(.*?)</div>', b, re.S).group(1)).strip()
    i = b.find('<div class="exam-ver">')
    ev = balanced_div(b, i) if i >= 0 else ''
    pri = re.search(r'data-pri="(\w)"', b)
    OFF[cid] = dict(id=cid, y=int(m.group(1)), n=int(m.group(2)), q=q, t=t, ev=ev,
                    pri=pri.group(1) if pri else '', lab=f'{m.group(1)}年第{CN[int(m.group(2))]}題')

# ── 題型定義：依 32 題官方題的問法歸納（不是考選部分類） ──
TYPES = [
 dict(k='calc', name='純計算型', sub='題目給齊數字，求一個數值',
      sig='題目把數字都給了，問「為若干」「為多少」「試算價格」「請列式說明…公式…現值為多少」。',
      ske=['意義：方法一句話＋本題要求算什麼（哪些數字是干擾資料先講）',
           '法條：公式逐字寫出，每個符號都要定義',
           '涵攝：一步一式「公式 → 代入 → 結果（含單位）」；中間值保留，最後才四捨五入並註明',
           '結論：答案數字＋單位，並寫明計算基礎（例：費用以哪個金額為基礎）'],
      lose=['只寫答案，沒寫公式與符號意義', '萬元、元混用或漏單位', '題目給的干擾資料硬拿來算（如已給總銷售金額卻再用面積推算）',
            '計算基礎有兩種做法時沒寫明採哪一種', '公式混用（定率法對「餘值」計算，不可寫成原始成本×年數）'],
      ids=['e102-2', 'e107-1', 'e105-2'], demo='e107-1'),
 dict(k='mix', name='說明＋計算混合型', sub='前半說明制度，後半舉例或代入計算',
      sig='前半「請說明／何謂／有那些」，後半「試舉例說明…計算過程與結果」「假設…請問」「試繪製示意圖」「另請分析合理性」。',
      ske=['意義：先把說明題的概念講清楚，再點出計算要求',
           '法條：說明部分的依據＋計算公式',
           '涵攝：（一）說明部分逐小題答；（二）計算部分「公式 → 代入 → 結果」；（三）問合理性時，從路徑選用、參數、方法侷限、交叉驗證逐點分析',
           '結論：說明的重點一句＋計算結果一句'],
      lose=['只算數字，前半說明題沒答（或反過來）', '自訂例子不合理（例：資金比重加總不是 100%）',
            '題目要求繪圖卻沒畫示意圖', '合理性只寫「合理」，沒有分點理由'],
      ids=['e99-1', 'e101-2', 'e105-1', 'e112-2'], demo='e112-2'),
 dict(k='formula', name='公式說明型', sub='不給數字，問怎麼算、各項怎麼決定',
      sig='題目沒有數字，問「如何計算」「計算公式」「計算依據與方法」「如何估計」「成本項目內容為何」。',
      ske=['意義：方法或公式的用途一句話',
           '法條：公式逐字寫出',
           '涵攝：每個符號（或每個成本項目）一段：是什麼 → 怎麼決定 → 依據；可自設小例子說明',
           '結論：公式＋各項如何決定，一句收束'],
      lose=['只抄公式，沒說每一項怎麼決定', '把資本利息、利潤列進直接或間接成本（它們在公式中另以利率處理）',
            '直接成本、間接成本歸類錯', '公式運算順序寫錯（先除後減，不是直接相減）'],
      ids=['e111-1', 'e104-2', 'e100-1', 'e113-2'], demo='e113-2'),
 dict(k='cmp', name='比較辨析型', sub='兩三個相近概念的意義、差異或關係',
      sig='題幹有「何謂A？何謂B？」「有何差異」「請說明三者的關係」。',
      ske=['意義：每個概念各給一句定義',
           '法條：各自的依據',
           '涵攝：先各自說明，再「逐項」比較（範圍、工具、適用目的……）或畫出三者關係，每項兩邊都要寫到',
           '結論：一句話點出最核心的差異或關係'],
      lose=['兩個概念各寫一大段，沒有逐項對照', '把同一類的兩種方法寫成新舊取代關係',
            '只寫定義，題目問的「差異／關係」沒答', '題目後半另問程序或資料時漏答'],
      ids=['e113-1', 'e107-2', 'e111-2'], demo='e113-1'),
 dict(k='list', name='列舉型', sub='依技術規則列出項目、要件、資料',
      sig='題幹有「有那些」「應考慮那些因素」「應蒐集那些資料」「調整重點為何」「有那些種類」。',
      ske=['意義：這份清單的目的（為什麼要列這些）',
           '法條：列舉的條文與款數',
           '涵攝：先分組（例：交易動機／交易關係／交易標的／交易程序），每組列款 → 一句說明 → 一個例子',
           '結論：收束款數，並寫出處理原則（例：先調整，無法量化才不採用）'],
      lose=['款數不齊', '只列名詞，沒有說明與例子', '漏寫處理方式或例外',
            '一題多個小問時漏答其中一問（列舉題常附帶「意義」或「如何處理」）'],
      ids=['e99-2', 'e102-1', 'e110-1', 'e106-2', 'e109-2', 'e114-1', 'e109-1', 'e103-2'], demo='e102-1'),
 dict(k='proc', name='方法選用與程序型', sub='給一個標的或情境，問用什麼方法、怎麼估',
      sig='題幹有「應如何評估／估價」「應採用何種估價方法」「估價程序為何」「適用時機」「如何提供…建議」。',
      ske=['意義：標的特性 → 適合的方法',
           '法條：方法的意義與程序依據',
           '涵攝：（一）選用的方法與理由；（二）每個方法依序寫運用程序；（三）兼採二種以上方法後綜合比較、決定價格',
           '結論：採用的方法＋程序要點＋綜合決定'],
      lose=['只用一種方法', '程序順序顛倒或漏步驟', '沒交代為什麼選這個方法', '漏寫最後的綜合比較與決定價格'],
      ids=['e106-1', 'e108-2', 'e101-1', 'e114-2', 'e110-2', 'e103-1'], demo='e114-2'),
 dict(k='case', name='情境判斷型', sub='市場現象或對話，問屬於哪一類、是否恰當',
      sig='題目先給一段事實（市場不景氣、凶殺事件、仲介說法），再問「屬於那一類／那一種原則」「是否恰當」「是否會影響價格」「如何掌握」。',
      ske=['意義：開頭直接下判斷（屬於哪一類、恰不恰當）',
           '法條：相關的原則、因素或規定',
           '涵攝：歸類理由 → 套題目事實 → 對價格的影響方向（比較法、收益法怎麼反映）→ 區辨相近概念',
           '結論：判斷＋理由一句'],
      lose=['沒有先下結論，整段都在介紹制度', '歸類錯（個別因素、區域因素混淆）',
            '和相近概念混在一起沒有區辨', '寫出沒有依據的固定折減比率'],
      ids=['e108-1', 'e112-1', 'e104-1', 'e100-2'], demo='e112-1'),
]

# ── 檢查：官方卡全部歸型且不重複；範例卡須在該型清單內 ──
allids = [i for t in TYPES for i in t['ids']]
missing = sorted(set(OFF) - set(allids)); extra = sorted(set(allids) - set(OFF))
assert not missing, ('未歸型的官方卡', missing)
assert not extra, ('歸型清單有不存在的卡', extra)
assert len(allids) == len(set(allids)), '有卡重複歸型'
for t in TYPES:
    assert t['demo'] in t['ids'], t['k']
    assert OFF[t['demo']]['ev'], ('範例卡沒有考場版', t['demo'])
    t['ids'].sort(key=lambda i: (OFF[i]['y'], OFF[i]['n']))
N = len(TYPES); TOTAL = len(OFF)
OUT_NAME = f'估價申論題_{N}型答題模板.html'
OUT = os.path.join(ROOT, OUT_NAME)
for old in glob.glob(os.path.join(ROOT, '估價申論題_*型答題模板.html')):
    if os.path.basename(old) != OUT_NAME:
        os.remove(old)  # 只清本產生器自己產出的舊檔名
CNN = CN[N] if N <= 10 else str(N)

ART = re.compile(r'(§\s?\d+(?:-\d+)?(?:之\d+)?(?:[ⅠⅡⅢⅣⅤ]+)?(?:第[一二三四五六七八九十]+款)?)')
def art(x):
    return ART.sub(r'<span class="art">\1</span>', x)
E = html.escape
SRC_URL = SRC_NAME

def item(i):
    c = OFF[i]
    return (f'<li><a href="{SRC_URL}#{i}" data-id="{i}"><span class="yl">{c["lab"]}</span>'
            f'<span class="ti">{art(E(c["t"]))}</span><span class="rd" aria-label="已讀">✓</span></a></li>')

body = ''
for n, t in enumerate(TYPES, 1):
    d = OFF[t['demo']]
    body += (
        f'<details class="ty" id="t-{t["k"]}" data-t="{t["k"]}"><summary><span class="tn">{CN[n]}</span>'
        f'<span class="tt"><b>{t["name"]}</b><small>{t["sub"]}</small></span>'
        f'<span class="tc"><b>{len(t["ids"])}</b>題</span></summary><div class="tb">'
        f'<p class="sig"><b>判型訊號（題目用語）</b>{art(t["sig"])}</p>'
        f'<div class="ske"><p class="h">答題骨架（四段式）</p><ol>' + ''.join(f'<li>{art(x)}</li>' for x in t['ske']) + '</ol></div>'
        f'<div class="lose"><p class="h">常見失分點</p><ul>' + ''.join(f'<li>{art(x)}</li>' for x in t['lose']) + '</ul></div>'
        f'<p class="h">官方歷屆（{len(t["ids"])} 題）</p><ul class="ol">' + ''.join(item(i) for i in t['ids']) + '</ul>'
        f'<details class="demo"><summary><span class="dk">示範</span><b>{d["lab"]}｜{art(E(d["t"]))}</b><span class="dl">考場版原文</span></summary>'
        f'<div class="db"><div class="oq"><b>原題</b>{E(d["q"])}</div>{d["ev"]}'
        f'<a class="go" href="{SRC_URL}#{d["id"]}">到範文頁看完整四段式 ›</a></div></details>'
        f'<label class="got"><input type="checkbox" class="gk"> 我已掌握這一型</label></div></details>')

mx = max(len(t['ids']) for t in TYPES)
dist = ''.join(f'<a class="dr" href="#t-{t["k"]}"><span>{CN[n]}　{t["name"]}</span><i style="--w:{len(t["ids"])/mx*100:.0f}%"></i><b>{len(t["ids"])}</b></a>'
               for n, t in enumerate(TYPES, 1))
DRILL = [dict(id=i, q=OFF[i]['q'], lab=OFF[i]['lab'], k=t['k']) for t in TYPES for i in t['ids']]
TMETA = [dict(k=t['k'], n=CN[n], name=t['name'], sig=t['sig']) for n, t in enumerate(TYPES, 1)]

CSS = '''
:root{--pri:#2F5D50;--onpri:#FFFFFF;--bg:#F5F1E6;--ink:#25302C;--card:#FFFEFA;--line:#DDD6C0;--muted:#66706A;--green:#35693F;--red:#A8402B;--key:#8A5517;
--b1:#35693F;--b1s:#EEF4EA;--b1l:#C9DCC2;--b2:#3E6B8C;--b2s:#ECF1F6;--b2l:#C4D4E2;--b3:#9A6424;--b3s:#FBF2E6;--b3l:#EBD3B2;--b4:#A8402B;--b4s:#FBEDE9;--b4l:#EBC5BC;--art:#80887F;color-scheme:light}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--pri:#84C2AE;--onpri:#10201B;--bg:#161C19;--ink:#E7ECE6;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--green:#8FCB93;--red:#E8857A;--key:#E0B070;--b1:#8FCB93;--b1s:#1E2B22;--b1l:#35503B;--b2:#7DB4D8;--b2s:#1B2630;--b2l:#33495C;--b3:#E0B070;--b3s:#2C2517;--b3l:#5A4728;--b4:#E8857A;--b4s:#2E1D1A;--b4l:#5C3530;--art:#8E9891;color-scheme:dark}}
:root[data-theme="dark"]{--pri:#84C2AE;--onpri:#10201B;--bg:#161C19;--ink:#E7ECE6;--card:#1F2723;--line:#34403A;--muted:#9AA79F;--green:#8FCB93;--red:#E8857A;--key:#E0B070;--b1:#8FCB93;--b1s:#1E2B22;--b1l:#35503B;--b2:#7DB4D8;--b2s:#1B2630;--b2l:#33495C;--b3:#E0B070;--b3s:#2C2517;--b3l:#5A4728;--b4:#E8857A;--b4s:#2E1D1A;--b4l:#5C3530;--art:#8E9891;color-scheme:dark}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.75 "Noto Sans TC",system-ui,sans-serif;padding:18px 16px 96px;overflow-wrap:anywhere}
main{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
h1{font:700 22px/1.3 "Noto Serif TC",serif;margin:0;color:var(--pri);text-wrap:balance;padding-right:46px}
.sub{color:var(--muted);font-size:13px;margin:4px 0 0}
details>summary{list-style:none;cursor:pointer}details>summary::-webkit-details-marker{display:none}
#theme-btn{position:fixed;top:10px;right:10px;z-index:50;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:18px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.art{color:var(--art);font-weight:400}
.box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.prg{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums}.prg b{color:var(--pri);font-size:16px}
.how>summary{font-weight:700;color:var(--pri);font-size:14px}.how>summary::after{content:" ▾";color:var(--muted)}.how[open]>summary::after{content:" ▴"}
.how ol,.how ul{margin:6px 0 0;padding-left:1.3em;font-size:14px}.how li{margin:2px 0}.how p{margin:8px 0 0;font-size:13.5px;color:var(--muted)}
.h{font-size:13px;font-weight:700;color:var(--muted);margin:6px 0 2px}
.dr{display:grid;grid-template-columns:minmax(0,10.5em) 1fr 2em;gap:8px;align-items:center;font-size:13px;margin:3px 0;color:var(--ink);text-decoration:none}.dr i{display:block;height:10px;border-radius:5px;background:var(--pri);width:var(--w)}.dr b{text-align:right;font-variant-numeric:tabular-nums}
/* 判型練習 */
.drill .dh{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}.drill .dh b{font:700 16px "Noto Serif TC",serif;color:var(--pri)}.drill .dh small{color:var(--muted);font-size:12.5px;font-variant-numeric:tabular-nums}
.dq{margin:8px 0;padding:10px 12px;border-radius:10px;background:var(--b2s);border:1px solid var(--b2l);font-size:14.5px}.dq .yl{display:block;font-size:12px;color:var(--b2);font-weight:700}
.opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(9.5em,1fr));gap:6px}
.opts button,.mini{font:inherit;font-size:13.5px;padding:7px 10px;border-radius:9px;border:1.5px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer;text-align:left}
.opts button.ok{border-color:var(--green);background:var(--b1s);color:var(--b1);font-weight:700}.opts button.ng{border-color:var(--red);background:var(--b4s);color:var(--b4)}
.opts button:disabled{cursor:default}
.fb{margin-top:8px;font-size:14px}.fb .r{font-weight:700}.fb .r.ok{color:var(--green)}.fb .r.ng{color:var(--red)}.fb p{margin:4px 0}
.drow{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px}.drow .mini{font-weight:700}.drow .pri{background:var(--pri);color:var(--onpri);border-color:var(--pri)}
/* 題型 */
.ty{background:var(--card);border:1px solid var(--line);border-radius:14px}
.ty>summary{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:4px 12px;align-items:center;padding:12px 14px}
.tn{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--pri);color:var(--onpri);font:700 15px "Noto Serif TC",serif}
.ty.got .tn{background:var(--green)}
.tt b{display:block;font:700 16px "Noto Serif TC",serif;color:var(--pri)}.tt small{color:var(--muted);font-size:12.5px}
.tc{text-align:center;font-size:11px;color:var(--muted);line-height:1.2}.tc b{display:block;font:700 17px "Noto Serif TC",serif;color:var(--ink)}
.ty[open]>summary{border-bottom:1px solid var(--line)}
.tb{padding:10px 14px 14px;display:flex;flex-direction:column;gap:8px;font-size:14px}
.sig{margin:0;padding:8px 12px;border-radius:9px;border:1px solid var(--b2l);background:var(--b2s)}.sig b{display:block;font-size:12.5px;color:var(--b2)}
.ske{border:1px solid var(--b1l);background:var(--b1s);border-radius:9px;padding:6px 12px}.ske .h{color:var(--b1)}.ske ol{margin:2px 0;padding-left:1.3em}.ske li{margin:3px 0}
.lose{border:1px solid var(--b4l);background:var(--b4s);border-radius:9px;padding:6px 12px}.lose .h{color:var(--b4)}.lose ul{margin:2px 0;padding-left:1.2em}
.ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.ol a{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px;align-items:baseline;padding:6px 10px;border:1px solid var(--line);border-radius:9px;background:var(--bg);color:var(--ink);text-decoration:none;font-size:13.5px}
.ol .yl{font-size:12px;color:var(--key);white-space:nowrap;font-variant-numeric:tabular-nums}.ol .rd{color:var(--green);font-weight:700;visibility:hidden}.ol a.read .rd{visibility:visible}
.demo{border:1px solid var(--b3l);border-radius:10px;background:var(--b3s)}
.demo>summary{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;padding:8px 10px}.demo .dk{font-size:12px;font-weight:700;color:var(--onpri);background:var(--b3);padding:0 8px;border-radius:99px}.demo>summary b{flex:1;min-width:0;font-size:14px}.demo .dl{font-size:11.5px;color:var(--muted)}
.db{padding:0 10px 10px}.oq{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:8px 11px;font-size:13.5px;margin-bottom:8px}.oq b{display:block;font-size:12px;color:var(--muted)}
.go{display:inline-block;margin-top:8px;font-size:13px;font-weight:700;color:var(--pri)}
.got{display:flex;gap:8px;align-items:center;font-weight:700;color:var(--pri);margin-top:6px}.got input{width:18px;height:18px;accent-color:var(--green)}
.ctl{display:flex;gap:8px}
.note{font-size:12.5px;color:var(--muted);margin:4px 2px}
/* 考場版（取自範文頁同名樣式） */
.exam-ver{display:flex;flex-direction:column;gap:8px}
.exam-ver{--ev1:#2F6B4F;--ev2:#2F6690;--ev3:#9A6A14;--ev4:#A8432F;--evbg:#FFFFFF;--evink:#26302C;--evsub:#6B746F}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) .exam-ver{--ev1:#7CC4A0;--ev2:#82B4DA;--ev3:#DDB15E;--ev4:#E39482;--evbg:#1E2422;--evink:#E4E0D6;--evsub:#A7AFA9}}
:root[data-theme="dark"] .exam-ver{--ev1:#7CC4A0;--ev2:#82B4DA;--ev3:#DDB15E;--ev4:#E39482;--evbg:#1E2422;--evink:#E4E0D6;--evsub:#A7AFA9}
.exam-ver .evb{background:color-mix(in srgb,var(--c) 11%,var(--evbg));border-radius:10px;padding:9px 13px;color:var(--evink)}
.exam-ver .evb.e1{--c:var(--ev1)}.exam-ver .evb.e2{--c:var(--ev2)}.exam-ver .evb.e3{--c:var(--ev3)}.exam-ver .evb.e4{--c:var(--ev4)}
.exam-ver b.evh{display:block;color:var(--c);font-size:.86rem;margin-bottom:2px}
.exam-ver .evb p{margin:4px 0 0;line-height:1.85;max-width:44em;font-size:.95rem}.exam-ver .evb>p:first-of-type{margin-top:0}
.exam-ver .art{color:var(--evsub);font-weight:400}
.exam-ver .evp{margin-top:12px}.exam-ver .evp:first-of-type{margin-top:4px}.exam-ver .evp .evh{font-weight:700;margin-top:0}
.exam-ver .evx{display:flex;gap:8px;align-items:baseline}
.exam-ver .lawn{color:var(--evink);font-weight:500;margin-left:2px}
.exam-ver .evli{display:block;padding-left:1.15em;text-indent:-1.15em;margin-top:3px}
.exam-ver .evt{flex:none;font-size:.74em;line-height:1.6;padding:0 7px;border-radius:999px;background:color-mix(in srgb,var(--evink) 9%,transparent);color:var(--evsub);font-weight:600}
'''

JS = '''(function(){
var KG="bxv-tpl-got",KD="bxv-tpl-drill",TM=%s,DR=%s;
function ld(k,d){try{var v=JSON.parse(localStorage.getItem(k)||"null");return v==null?d:v}catch(e){return d}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
var G=ld(KG,{}),D=ld(KD,{});if(typeof D!=="object"||Array.isArray(D))D={};D.a=D.a||{};
var R=ld("bx-essay-read",[]);if(!Array.isArray(R))R=[];
var T=[].slice.call(document.querySelectorAll(".ty"));
function stat(){var g=0;T.forEach(function(t){var on=!!G[t.dataset.t];t.classList.toggle("got",on);t.querySelector(".gk").checked=on;if(on)g++});
document.getElementById("gotN").textContent=g;
var as=document.querySelectorAll(".ol a"),r=0;as.forEach(function(a){var on=R.indexOf(a.dataset.id)>=0;a.classList.toggle("read",on);if(on)r++});
document.getElementById("readN").textContent=r;
var n=0,ok=0;DR.forEach(function(q){if(q.id in D.a){n++;if(D.a[q.id])ok++}});
document.getElementById("drN").textContent=n;document.getElementById("drOk").textContent=ok;document.getElementById("drN2").textContent=n+"／"+DR.length+"，答對 "+ok}
T.forEach(function(t){t.querySelector(".gk").addEventListener("change",function(){if(this.checked)G[t.dataset.t]=1;else delete G[t.dataset.t];sv(KG,G);stat()})});
document.querySelectorAll("[data-all]").forEach(function(b){b.onclick=function(){var o=b.dataset.all==="open";T.forEach(function(t){t.open=o})}});
/* 判型練習：先出沒練過的，再出答錯的，最後隨機 */
var tmap={};TM.forEach(function(t){tmap[t.k]=t});
var cur=null,mode="all";
function pick(){var pool=DR.filter(function(q){return mode==="wrong"?D.a[q.id]===0:!(q.id in D.a)});
if(!pool.length&&mode==="all")pool=DR.filter(function(q){return D.a[q.id]===0});
if(!pool.length)pool=mode==="wrong"?[]:DR.slice();
var c=pool.filter(function(q){return !cur||q.id!==cur.id});if(c.length)pool=c;
return pool.length?pool[Math.floor(Math.random()*pool.length)]:null}
function esc(x){return String(x).replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c]})}
function show(){cur=pick();var q=document.getElementById("dq"),o=document.getElementById("opts"),f=document.getElementById("fb");f.innerHTML="";
if(!cur){q.innerHTML="目前沒有答錯的題目，切回「全部題目」繼續練。";o.innerHTML="";return}
q.innerHTML='<span class="yl">'+cur.lab+'</span>'+esc(cur.q);
o.innerHTML=TM.map(function(t){return '<button type="button" data-k="'+t.k+'">'+t.n+'　'+t.name+'</button>'}).join("");
o.querySelectorAll("button").forEach(function(b){b.onclick=function(){answer(b.dataset.k)}})}
function answer(k){var ok=k===cur.k;D.a[cur.id]=ok?1:0;D.t=Math.floor(Date.now()/1000);sv(KD,D);
document.querySelectorAll("#opts button").forEach(function(b){b.disabled=true;if(b.dataset.k===cur.k)b.classList.add("ok");else if(b.dataset.k===k)b.classList.add("ng")});
var t=tmap[cur.k];document.getElementById("fb").innerHTML='<p class="r '+(ok?"ok":"ng")+'">'+(ok?"✓ 判對了":"✗ 這題是「"+t.n+"　"+t.name+"」")+'</p><p><b>判型訊號：</b>'+t.sig+'</p><p><a href="#t-'+t.k+'" class="go" data-open="t-'+t.k+'">看這一型的骨架 ›</a>　<a class="go" href="%s#'+cur.id+'">看這題範文 ›</a></p>';
var a=document.querySelector("#fb [data-open]");if(a)a.onclick=function(){var d=document.getElementById(a.dataset.open);if(d)d.open=true};stat()}
document.getElementById("dNext").onclick=show;
document.getElementById("dMode").onclick=function(){mode=mode==="all"?"wrong":"all";this.textContent=mode==="all"?"只練答錯的":"全部題目";show()};
document.getElementById("dReset").onclick=function(){if(!confirm("清除判型練習紀錄？"))return;D={a:{}};sv(KD,D);stat();show()};
stat();show();
var h=decodeURIComponent((location.hash||"").slice(1));if(h){var d=document.getElementById(h);if(d){if(d.tagName==="DETAILS")d.open=true;d.scrollIntoView()}}
})();
function ub(t){var b=document.getElementById("theme-btn");if(b)b.textContent=t==="dark"?"🌙":"☀️"}
function cur_t(){var a=document.documentElement.getAttribute("data-theme");if(a)return a;return matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}
function toggleTheme(){var n=cur_t()==="dark"?"light":"dark";document.documentElement.setAttribute("data-theme",n);ub(n);try{localStorage.setItem("bx-theme",n)}catch(e){}}
ub(cur_t());''' % (json.dumps(TMETA, ensure_ascii=False), json.dumps(DRILL, ensure_ascii=False), SRC_URL)

FAB = '''<!--bxfab-->
<style>
#bxfab{--fp:#2F5D50;--fs:#FFFEFA;--fo:#FFFFFF;--fl:#DDD6C0;position:fixed;left:0;right:0;bottom:calc(14px + env(safe-area-inset-bottom,0px));padding:0 12px;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none;z-index:60}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}}
:root[data-theme="dark"] #bxfab{--fp:#84C2AE;--fs:#1F2723;--fo:#10201B;--fl:#34403A}
#bxfab>*{pointer-events:auto}
#bxfab .bx-up{position:relative;width:40px;height:40px;border-radius:50%;border:0;background:var(--fs);color:var(--fp);padding:0;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.22);cursor:pointer;opacity:.4;transition:opacity .25s}
#bxfab .bx-up.act{opacity:1}
#bxfab .bx-up .rg{position:absolute;inset:0;width:100%;height:100%}
#bxfab .bx-up .rg circle{fill:none;stroke-width:3}
#bxfab .bx-up .rg .t{stroke:var(--fl)}#bxfab .bx-up .rg .p{stroke:var(--fp);stroke-linecap:round;transform:rotate(-90deg);transform-origin:center;transition:stroke-dashoffset .1s}
#bxfab svg.ic{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;position:relative}
#bxfab .bx-hub{width:40px;height:40px;border-radius:50%;background:var(--fp);color:var(--fo);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.25);text-decoration:none}
#bxfab .bx-hub svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
</style>
<div id="bxfab"><button class="bx-up" id="navUp" aria-label="回到最上方" onclick="window.scrollTo({top:0,behavior:'smooth'})"><svg class="rg" viewBox="0 0 44 44"><circle class="t" cx="22" cy="22" r="19"/><circle class="p" cx="22" cy="22" r="19" stroke-dasharray="119.4" stroke-dashoffset="119.4"/></svg><svg class="ic" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button><a class="bx-hub" href="%E4%BC%B0%E5%83%B9%E5%82%99%E8%80%83%E6%8C%87%E6%8F%AE%E4%B8%AD%E5%BF%83.html" aria-label="回備考指揮中心" title="回備考指揮中心"><svg viewBox="0 0 24 24"><path d="M3 11l9-8 9 8M5 10v10h5v-6h4v6h5V10"/></svg></a></div>
<script>(function(){var b=document.querySelector("#bxfab .bx-up"),p=b.querySelector(".p");function f(){var h=document.documentElement,m=h.scrollHeight-window.innerHeight,y=window.scrollY||0,r=m>0?Math.min(1,y/m):0;p.setAttribute("stroke-dashoffset",(119.4*(1-r)).toFixed(1));b.classList.toggle("act",y>160)}window.addEventListener("scroll",f,{passive:true});window.addEventListener("resize",f);f()})();</script>
<!--/bxfab-->'''

page = f'''<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><script src="bx-vp.js"></script><title>估價申論{CNN}型模板</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap">
<script>/*bxdef*/(function(){{var s=null;try{{s=localStorage.getItem('bx-theme')}}catch(e){{}}if(s)document.documentElement.setAttribute('data-theme',s)}})();</script>
<style>{CSS}</style></head><body><button id="theme-btn" onclick="toggleTheme()" title="切換深淺色" aria-label="切換深淺色">☀️</button><main>
<header><h1>估價｜申論{CNN}型答題模板</h1><p class="sub">官方 99～114 年 {TOTAL} 題依問法歸成 {N} 型。看到題目先判型，骨架就出來了。</p></header>
<div class="prg"><span>已掌握 <b id="gotN">0</b>／{N} 型</span><span>判型練習 <b id="drN">0</b>／{TOTAL}，答對 <b id="drOk">0</b></span><span>官方範文已讀 <b id="readN">0</b>／{TOTAL}</span></div>
<details class="box how"><summary>怎麼用這頁・考場 60 秒 SOP</summary>
<ol><li>先讀題目最後的問句，框出問了幾件事（估價題常是「說明＋計算」兩段）。</li><li>對照「判型訊號」決定是哪一型；一題兩問就各自判型，分兩段寫。</li><li>題目有數字 → 圈起來，先寫公式再代入，結果一定帶單位。</li><li>四段式不變：意義→法條→涵攝→結論。</li></ol>
<p>判型練習：題目隨機出（先出沒練過的），選型後立刻對答案並顯示判型訊號；紀錄只存在這台裝置。「已讀」打勾沿用範文頁的已讀紀錄。題型是依問法歸類的備考分類，不是考選部分類；示範一律是範文頁考場版原文。</p></details>
<div class="box"><p class="h" style="margin-top:0">官方 {TOTAL} 題的題型分布</p>{dist}</div>
<section class="box drill" id="drill"><div class="dh"><b>判型練習</b><small>已練 <span id="drN2">0</span></small></div>
<div class="dq" id="dq"></div><div class="opts" id="opts"></div><div class="fb" id="fb"></div>
<div class="drow"><button type="button" class="mini pri" id="dNext">下一題</button><button type="button" class="mini" id="dMode">只練答錯的</button><button type="button" class="mini" id="dReset">清除紀錄</button></div></section>
<div class="ctl"><button type="button" class="mini" data-all="open">全部展開</button><button type="button" class="mini" data-all="close">全部收合</button></div>
{body}
<p class="note">題數由產生器從範文頁官方卡自動計算（tools/essay_val/template/gen_tpl.py）。</p>
</main><script>{JS}</script>
{FAB}
<script src="bxv-use.js"></script>
<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("/brokerX/sw.js",{{scope:"/brokerX/"}});</script>
</body></html>'''
open(OUT, 'w', encoding='utf-8').write(page)
print('ok', OUT_NAME, len(page), 'total', TOTAL)
for n, t in enumerate(TYPES, 1):
    print(CN[n], t['name'], len(t['ids']), 'demo', t['demo'])
