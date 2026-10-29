#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-29（深夜）：依使用者截圖意見修《估價_計算題攻略》與《綜合模擬卷四》申論二。

使用者三點：
 ① 計算題攻略「沒分類可以跳，其他頁都有」→ 本頁 0 個頁內連結（技術規則專欄 8、四大方法比較表 6）。
 ② ④高危未出現考點「都高危，你竟然沒有整理好」
 ③ 模擬卷四 DCF 公式「好背嗎？」

查證（bxv-quiz-data.js、KB《技術規則全文逐字》）發現的錯：
 a. ④ 三張卡的「命中機率 70%／65%／45%」沒有任何依據，而且同一區塊標「高危」卻有一張評「中」→ 拿掉。
 b. DCF 卡：「選擇題近兩年開始出現DCF計算題（112、113年選擇）」→ 題庫 112、113 沒有 DCF 計算；
    DCF 計算只有 103-37 一題。
 c. DCR 卡：「另 109 年也考過」→ 109 年沒有；考過的是 104-39（計算）。111～114 連續四年正確。
 d. 定率法卡：「近年選擇題持續考定率法（108、110、113年）」→ 110-5、113-21 都是定額法，108 沒有；
    與定率法直接相關的是 102-16（成本價格最低＝定率法），路徑題 103-11、106-26。
    ② 定率法卡的「108選 110選 113選」同樣錯，一起改。
 e. DCF 公式期末價值寫成 (1＋Y)ⁿ，§32 是 (1＋Y)ⁿ′。
 f. 頁面順序是 ④→⑥→⑤，編號跳號 → ⑥收益法補充改 ⑤、⑤高分技巧改 ⑥（id inc-extra 不變）。
 g. 模擬卷四申論二用 V／NOIₜ／r／Pₙ／n，與 §32 的 P／CFk／Y／Pn′／n′ 不同，101-18、102-27
    正是考這組符號 → 改成條文符號；程序改用 §34 六步（與收益法同一套），
    「Pₙ＝NOI(n+1)÷末期資本化率」標為教材作法（條文未規定）。
 h. 他頁連到本頁「資本化率」的連結指向 #inc-extra（那裡沒有五種資本化率）→ 改指 #cc-cap；
    範文 e113-1 的「估價_計算題組.html#dcf」錨點不存在 → 改指《估價_DCF計算題組》。

只跑一次。每項檢查原文出現次數，對不上整支不寫檔。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CALC = ROOT / "估價_計算題攻略.html"
MOCK4 = ROOT / "估價_綜合模擬卷四.html"
ESSAY = ROOT / "不動產估價概要_申論題實戰範文.html"
HUB = ROOT / "估價備考指揮中心.html"

fail = []


def rep(s, name, old, new, n_exp=1):
    n = s.count(old)
    if n != n_exp:
        fail.append(f"✗ {name}：出現 {n} 次（應為 {n_exp}）｜{old[:80]}")
        return s
    print(f"  ✔ {name}")
    return s.replace(old, new)


def qa(i, label):
    return f'<a class="q" href="估價_考題小卡.html#{i}">{label}</a>'


# ───────────────────────── 計算題攻略 ─────────────────────────
s = CALC.read_text(encoding="utf-8")

CSS = """/* v590 頁內導覽、④整理 */
.jump-nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:50;background:var(--paper);border-bottom:1px solid var(--rule)}
.jump-nav .in{max-width:860px;margin:0 auto;padding:8px 20px;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.jump-nav .in::-webkit-scrollbar{display:none}
.jump-nav a{flex:none;font-size:12px;padding:3px 11px;border-radius:99px;border:1px solid var(--rule);color:var(--ink);background:var(--card);text-decoration:none;white-space:nowrap}
.jump-nav a:hover{border-color:var(--stamp);color:var(--stamp)}
.section,.calc-card,.not-yet-card{scroll-margin-top:56px}
.cat-row{display:flex;flex-wrap:wrap;gap:4px 12px;margin:-8px 0 18px;font-size:12px;color:var(--ink-soft);line-height:1.8}
.cat-row .g{font-weight:700;color:var(--ink)}
.cat-row a,.not-yet-card a.q{color:var(--blue);text-decoration:none;border-bottom:1px dotted currentColor;white-space:nowrap}
.not-yet-card{min-width:0}
.ny-k{font-size:11px;font-weight:700;color:var(--purple);letter-spacing:1px;margin:12px 0 4px}
.ny-f{font-size:13.5px;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:8px 10px;overflow-x:auto;line-height:1.9;color:var(--ink)}
.ny-f .sym{display:block;font-size:12px;color:var(--ink-soft);line-height:1.7;margin-top:2px}
.not-yet-card ol{font-size:12px;padding-left:18px;line-height:1.75;color:var(--ink)}
.not-yet-card .src{font-size:11px;color:var(--ink-soft);font-weight:400}

/* DIVIDER */"""
s = rep(s, "CSS", "/* DIVIDER */", CSS)

NAV = """<!-- 頁內導覽 -->
<nav class="jump-nav" aria-label="本頁章節"><div class="in">
<a href="#s1">① 頻次總覽</a><a href="#s2">② 公式拆解</a><a href="#s3">③ 出現矩陣</a><a href="#s4">④ 高危未出現</a><a href="#inc-extra">⑤ 收益法補充</a><a href="#s6">⑥ 高分技巧</a>
</div></nav>

<!-- ① 總覽表 -->
<div class="section" id="s1">"""
s = rep(s, "導覽列＋①id", "<!-- ① 總覽表 -->\n<div class=\"section\">", NAV)

CAT = """
  <div class="cat-row"><span class="g">依方法跳：</span>
    <span>成本法 <a href="#cc-dep1">定額</a>・<a href="#cc-dep2">定率</a>・<a href="#cc-dep3">償債基金</a></span>
    <span>土地開發 <a href="#cc-dev">V公式</a></span>
    <span>比較法 <a href="#cc-cmp">三道排除關卡</a></span>
    <span>收益法 <a href="#cc-cap">五種資本化率</a>・<a href="#ny-dcf">DCF</a>・<a href="#inc-extra">殘餘法等⑤</a></span>
    <span>租金 <a href="#cc-rent">實質租金</a></span>
    <span>房地 <a href="#cc-floor">樓層別效用比</a>・<a href="#split-card">拆土地單價</a></span>
  </div>"""
s = rep(s, "②id＋方法分類列",
        '<div class="section">\n  <div class="section-title">② 必考計算題型 · 公式完整拆解 <span class="sub-note">A級必考 4 大類型</span></div>',
        '<div class="section" id="s2">\n  <div class="section-title">② 必考計算題型 · 公式完整拆解 <span class="sub-note">A級必考 4 大類型</span></div>' + CAT)
s = rep(s, "③id", '<div class="section">\n  <div class="section-title">③ ',
        '<div class="section" id="s3">\n  <div class="section-title">③ ')
s = rep(s, "⑥收益法補充→⑤", '<div class="section-title">⑥ 收益法補充：',
        '<div class="section-title">⑤ 收益法補充：')
s = rep(s, "⑤高分技巧→⑥＋id",
        '<!-- ⑤ 備考得分技巧 -->\n<div class="section">\n  <div class="section-title">⑤ 計算題高分技巧',
        '<!-- ⑥ 備考得分技巧 -->\n<div class="section" id="s6">\n  <div class="section-title">⑥ 計算題高分技巧')

# ② 卡片 id
for cid, title in [("cc-dep1", "成本法①：定額法"), ("cc-dep2", "成本法②：定率法"),
                   ("cc-dep3", "成本法③：償債基金法"), ("cc-dev", "土地開發分析法：V公式"),
                   ("cc-cmp", "比較法：三道排除關卡"), ("cc-cap", "收益法：五種資本化率"),
                   ("cc-rent", "租金估計：實質租金"), ("cc-floor", "樓層別效用比計算")]:
    pat = re.compile(r'<div class="calc-card">(?=(?:(?!<div class="calc-card">).){0,400}?'
                     + re.escape(title) + ')', re.S)
    hits = pat.findall(s)
    if len(hits) != 1:
        fail.append(f"✗ 卡片 id {cid}：找到 {len(hits)} 張")
    else:
        s = pat.sub(f'<div class="calc-card" id="{cid}">', s, count=1)
        print(f"  ✔ 卡片 id {cid}")

# ② 定率法卡出現年
s = rep(s, "② 定率法卡出現年",
        '<span class="year-chip chip-essay">107申（完整計算）</span><span class="year-chip chip-choice">108選</span>'
        '<span class="year-chip chip-choice">110選</span><span class="year-chip chip-choice">113選</span>',
        '<span class="year-chip chip-essay">107申（公式＋代入一次）</span>'
        '<span class="year-chip chip-choice">102選（成本價格最低）</span>'
        '<span class="year-chip chip-choice">103選・106選（折舊路徑）</span>')

# ④ 整段重寫
a = s.find('<div class="section">\n  <div class="section-title">④ 高危未出現考點')
b = s.find('<!-- ⑥ 收益法補充')
if a < 0 or b < 0 or s.count('<div class="section-title">④ 高危未出現考點') != 1:
    fail.append(f"✗ ④ 區塊定位失敗 a={a} b={b}")
else:
    S4 = f"""<div class="section" id="s4">
  <div class="section-title">④ 高危未出現考點 <span class="sub-note">三題都是：選擇題反覆考，申論還沒考過「完整計算版」</span></div>
  <div class="not-yet-grid">

    <div class="not-yet-card" id="ny-dep2">
      <h4>⚡ 定率法：完整計算申論</h4>
      <div class="ny-k">為什麼高危</div>
      <div class="reason">申論只考過 107-一，而且只要「公式＋代入一次」：1,000 萬×0.98⁵≈903.92 萬。還沒考過「逐年列表」或「和定額法並列比較」。選擇題考過 {qa("VC2_102_16","102-16")}（三法中成本價格最低＝定率法）、{qa("VC2_103_11","103-11")}、{qa("VC2_106_26","106-26")}（三種折舊路徑，§68）。</div>
      <div class="ny-k">要背的公式 <span class="src">教材公式；§68 只規定三種路徑，沒有列算式</span></div>
      <div class="ny-f">第 n 年末現值 ＝ C ×（1－r）<sup>n</sup><br>累積折舊額 ＝ C ×［1－（1－r）<sup>n</sup>］
        <span class="sym">C＝重建成本　r＝每年折舊率　n＝經歷年數</span></div>
      <div class="ny-k">考場怎麼寫</div>
      <ol><li>先寫公式與符號。</li><li>逐年列表：期初價值 → 當年折舊額（期初價值×r）→ 期末價值。</li><li>寫結論，補一句：定率法屬<b>初期加速折舊</b>路徑（§68），第 1 年折舊額最大、逐年遞減。</li></ol>
      <div class="calc-history" style="margin:10px 0 0">公式拆解：<a href="#cc-dep2">② 定率法卡</a>｜模擬：<a href="估價_綜合模擬卷二.html">綜合模擬卷二・申論一</a>｜範文：<a href="不動產估價概要_申論題實戰範文.html#pred-1">115預測①　折舊三路徑</a></div>
    </div>

    <div class="not-yet-card" id="ny-dcr">
      <h4>⚡ 債務保障比率法：公式＋代入＋推估收益價格</h4>
      <div class="ny-k">為什麼高危</div>
      <div class="reason">選擇題 111～114 年<b>連續四年</b>都考（{qa("VD2_111_3","111-3")}、{qa("VD2_112_18","112-18")}、{qa("VD2_113_13","113-13")}、{qa("VD2_114_8","114-8")}；{qa("VD2_104_39","104-39")} 也考過計算），申論還沒考過整套流程。</div>
      <div class="ny-k">要背的公式 <span class="src">§43④ 逐字；收益價格用 §30</span></div>
      <div class="ny-f">收益資本化率 ＝ 債務保障比率 × 貸款常數 × <b>貸款資金</b>占不動產價格比率<br>收益價格 ＝ 淨收益 ÷ 收益資本化率
        <span class="sym">例 114-8：1.3 × 0.055 × 70% ＝ 5.005% ≈ 5%</span></div>
      <div class="ny-k">考場陷阱</div>
      <ol><li>第三個乘數是「<b>貸款資金</b>」占價格比率。題目給自有資金時要先換算。</li><li>104-39：貸款以外的資金占 40% → 貸款占 60%，1.3×0.1×60%＝7.8%。</li><li>112-18：自有資金 15 億／價格 60 億 → 貸款占 75%，1.5×0.1×75%＝11.25%。</li></ol>
      <div class="calc-history" style="margin:10px 0 0">公式拆解：<a href="#cc-cap">② 五種資本化率卡</a>｜範文：<a href="不動產估價概要_申論題實戰範文.html#pred-16">115預測⑯　DCR＋有效總收入乘數</a>｜<a href="不動產估價概要_申論題實戰範文.html#pred-2">115預測②　§43 五種方法</a>｜選擇：<a href="估價_綜合模擬卷四.html">綜合模擬卷四 第18題</a></div>
    </div>

    <div class="not-yet-card" id="ny-dcf">
      <h4>⚡ DCF 折現現金流量：完整計算申論</h4>
      <div class="ny-k">為什麼高危</div>
      <div class="reason">申論考過 113-一（DCF 與直接資本化法的差異），沒要求計算。選擇題的 DCF 計算只考過一次（{qa("VD3_103_37","103-37")}），其他 DCF 題都在考符號：{qa("VD3_101_18","101-18")}（Pn′）、{qa("VD3_102_27","102-27")}（n′）、{qa("VD3_114_23","114-23")}（期末價值用折現率）。</div>
      <div class="ny-k">要背的公式 <span class="src">§32，符號照條文寫</span></div>
      <div class="ny-f">P ＝ Σ CF<sub>k</sub> ÷（1＋Y）<sup>k</sup> ＋ P<sub>n′</sub> ÷（1＋Y）<sup>n′</sup>　（k＝1～n′）
        <span class="sym">P＝收益價格　CF<sub>k</sub>＝各期淨收益　Y＝折現率　n′＝折現現金流量分析期間　k＝各年期　P<sub>n′</sub>＝期末價值</span>
        <span class="sym"><b>白話：</b>每一年的淨收益各自折回今天，最後的期末價值也折回今天，全部加起來就是 P。</span></div>
      <div class="ny-k">代入示範（103-37）</div>
      <div class="ny-f">每年淨收益 10 萬、第 3 年底以 200 萬出售、折現率 5%<br>10÷1.05 ＋ 10÷1.05² ＋（10＋200）÷1.05³ ＝ 9.52 ＋ 9.07 ＋ 181.41 ≈ <b>200 萬</b></div>
      <div class="ny-k">考場陷阱</div>
      <ol><li>期末價值和最後一期淨收益<b>同一期</b>折現（上例第 3 年的 10＋200 一起 ÷1.05³），不要多折一期。</li><li>期末價值用<b>折現率 Y</b> 折現，不是資本化率（114-23）。</li><li>n′ 是<b>分析期間</b>，不是耐用年數（102-27）。</li></ol>
      <div class="calc-history" style="margin:10px 0 0">範文：<a href="不動產估價概要_申論題實戰範文.html#pred-11">115預測⑪　DCF 之計算（§31、§32）</a>｜模擬：<a href="估價_綜合模擬卷四.html">綜合模擬卷四・申論二</a>｜練習：<a href="估價_DCF計算題組.html">DCF 計算題組</a></div>
    </div>

  </div>
</div>

<div class="section-divider"></div>


"""
    s = s[:a] + S4 + s[b:]
    print("  ✔ ④ 整段重寫")

calc_out = s

# ───────────────────────── 綜合模擬卷四 申論二 ─────────────────────────
m = MOCK4.read_text(encoding="utf-8")
q = m.find("二、試述折現現金流量分析法之意義、應用時機、公式及估價程序")
a = m.find('<div class="section-h">（一）意義</div>', q)
endtxt = "資本化率用於直接資本化或求期末值。</p>"
b = m.find(endtxt, a)
if q < 0 or a < 0 or b < 0 or m.count(endtxt) != 1:
    fail.append(f"✗ 模擬卷四申論二定位失敗 q={q} a={a} b={b}")
else:
    b += len(endtxt)
    sym = lambda k, v: (f'<div class="kf-eq"><span class="kf-c k-s">{k}</span><span class="kf-op">＝</span>'
                        f'<span class="kf-c k-m">{v}</span></div>')
    NEW = f"""<div class="section-h">（一）意義</div>
        <p>折現現金流量分析法，指勘估標的未來折現現金流量分析期間之<b>各期淨收益</b>及<b>期末價值</b>，以適當<b>折現率</b>折現後加總推算勘估標的價格之方法（技術規則§31Ⅰ）。</p>

        <div class="section-h">（二）應用時機</div>
        <p>1. <b>條文明定</b>：得適用於以投資為目的之不動產投資評估（§31Ⅱ）。</p>
        <p>2. 以不動產證券化為估價目的者，各期淨收益以契約租金計算為原則（§33Ⅱ）；以契約約定租金作為信託利益分配基礎者，DCF 之收益價格應賦予相對較大之權重（§15Ⅱ）。</p>
        <p>3. 實務歸納：各期收益有明確變動趨勢（如租金逐年調升）、各期淨收益不穩定而直接資本化法不易適用時。</p>

        <div class="section-h">（三）公式（§32，符號照條文）</div>
        <div class="cbox"><div class="kf-eq"><span class="kf-c k-s">P</span><span class="kf-op">＝</span><span class="kf-c k-m">Σ CF<sub>k</sub> ÷ (1＋Y)<sup>k</sup></span><span class="kf-op">＋</span><span class="kf-c k-m">P<sub>n′</sub> ÷ (1＋Y)<sup>n′</sup></span></div><div class="kf-note">其中（k＝1～n′）：</div>{sym("P","收益價格")}{sym("CF<sub>k</sub>","各期淨收益")}{sym("Y","折現率")}{sym("n′","折現現金流量分析期間")}{sym("k","各年期")}{sym("P<sub>n′</sub>","期末價值")}</div>
        <p><b>白話：</b>每一年的淨收益各自折回今天，最後的期末價值也折回今天，全部加起來就是 P。</p>

        <div class="section-h">（四）估價程序（§34，與收益法同一套六步）</div>
        <p>① 蒐集總收入、總費用及折現率等資料（§35：最近三年）</p>
        <p>② 推算有效總收入（§36）</p>
        <p>③ 推算總費用（§38；證券化目的者依<b>信託計畫資料</b>推算）</p>
        <p>④ 計算淨收益：有效總收入－總費用（§42）</p>
        <p>⑤ 決定折現率（§43 五種方法）</p>
        <p>⑥ 計算收益價格：依 §32 將各期淨收益及期末價值折現加總</p>
        <p>DCF 另須決定<b>分析期間 n′</b> 與<b>期末價值 P<sub>n′</sub></b>（§31、§32）。期末價值常以「第 n′＋1 期淨收益 ÷ 期末資本化率」推估——<b>這是教材作法，條文未規定</b>；推估出 P<sub>n′</sub> 後，仍以折現率 Y 折現。</p>

        <p>🎯 <b>DCF vs 直接資本化：</b>直接資本化法用「未來平均一年期間」之客觀淨收益÷收益資本化率（§29、§30）；DCF 用分析期間內「各期」淨收益及期末價值折現加總。</p>
        <p>🎯 <b>符號題：</b>101-18 考 P<sub>n′</sub>＝期末價值；102-27 考 n′＝折現現金流量分析期間（不是耐用年數）。</p>
        <p>🎯 <b>折現率 vs 資本化率：</b>各期淨收益與期末價值都用折現率 Y 折現（114-23）；資本化率用於直接資本化法，或在教材作法中用來推估期末價值。</p>"""
    m = m[:a] + NEW + m[b:]
    print("  ✔ 模擬卷四申論二重寫")

# ───────────────────────── 他頁連結 ─────────────────────────
e = ESSAY.read_text(encoding="utf-8")
e = rep(e, "範文 e104-2 標籤 ⑥→⑤", "['計算題攻略 ⑥折舊提存率 §41','估價_計算題攻略.html#inc-extra']",
        "['計算題攻略 ⑤折舊提存率 §41','估價_計算題攻略.html#inc-extra']")
e = rep(e, "範文 e99-1 資本化率錨點", "['計算題攻略 五種資本化率','估價_計算題攻略.html#inc-extra']",
        "['計算題攻略 五種資本化率','估價_計算題攻略.html#cc-cap']")
e = rep(e, "範文 e113-1 斷掉的錨點", "['計算題組 DCF 8 題','估價_計算題組.html#dcf']",
        "['DCF 計算題組','估價_DCF計算題組.html']")
h = HUB.read_text(encoding="utf-8")
h = rep(h, "指揮中心 D2 資本化率錨點", "D2:['計算題攻略 資本化率','估價_計算題攻略.html#inc-extra']",
        "D2:['計算題攻略 資本化率','估價_計算題攻略.html#cc-cap']")

if fail:
    print("\n".join(fail))
    sys.exit("\n有項目對不上，全部不寫檔。")
CALC.write_text(calc_out, encoding="utf-8")
MOCK4.write_text(m, encoding="utf-8")
ESSAY.write_text(e, encoding="utf-8")
HUB.write_text(h, encoding="utf-8")
print("寫入 4 個檔案完成")
