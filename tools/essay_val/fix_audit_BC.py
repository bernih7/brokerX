#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-30 估價計算全面複核：B 組（申論範文計算卡）＋C 組（公式整理頁）裁決後修正。
每項都回技術規則逐字（§26、§30、§36、§40、§43、§45、§46、§57、§68、§79、§81、§99～§101、§125、§130）
或 python 重算、或 bxv-quiz-data.js 確認。

不採／改寫：
 - B7（757.2 係數取四位）：與同卡 0.6310 一致，差 0.1，不改。
 - B14（pred-2 累加法表「資本回收率」）：自設教材範例，不改數字。
 - C-26（實質租金年份換 101）：題庫實際的實質租金計算題只有 103-38、104-24、105-26、113-19，
   改為 4 次（100-40 是定義題、114 年沒有計算題）；統計區依次數重排。
 - C-25 改為全題庫口徑：證券化 DCF 以契約租金為原則 102-8、104-13、105-17、110-13 共 4 次。
 - 「條文」標籤改成「教材」（不是「說明」），讓考生一眼看出不能寫「依技術規則」。

申論範文的邏輯拆解由 lj_data.json 產生，但 gen_lj.py 與正式頁已有 35 行漂移（版本鈕名稱等），
**不可重跑 gen_lj.py**；本腳本直接改正式頁，並把同樣的修改寫進 lj_data.json（新增 step／check 的 "lt" 欄），
gen_lj.py 同步支援 "lt"，日後重產時結果一致。
只跑一次。每項斷言出現次數，對不上整支不寫檔。
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
HERE = Path(__file__).resolve().parent
fail, files = [], {}


def rep(fn, name, old, new, n=1):
    s = files.get(fn) or (R / fn).read_text(encoding="utf-8")
    c = s.count(old)
    if c != n:
        fail.append(f"✗ {fn}｜{name}：出現 {c} 次（應為 {n}）")
        return
    files[fn] = s.replace(old, new)
    print(f"  ✔ {fn}｜{name}（{c}）")


ES = "不動產估價概要_申論題實戰範文.html"
TL = '<span class="ljt tl">條文</span>'
TJ = '<span class="ljt tl">教材</span>'

# ── B1／B2／B17：教材內容掛「條文」標籤 ──
LAB = {
    "e107-1": {"steps": ["定率法公式", "定率法意義", "陷阱：不可混用"],
               "checks": ["公式 C×(1－r)ⁿ", "定率法意義：固定折舊率×餘值"]},
    "e111-1": {"steps": ["公式", "定額法（等速折舊）", "定率法・償債基金法", "三法對應"],
               "checks": ["三法累積折舊額", "定額法每年折舊額", "定率法（對前一年餘值", "路徑與方法對應"]},
    "e105-1": {"steps": ["座標", "線形"], "checks": ["三種路徑與方法"]},
    "pred-1": {"steps": [], "checks": ["對應不可混淆"]},
    "e100-1": {"steps": ["土地乘1、建物乘½"], "checks": []},
}
for cid, d in LAB.items():
    for h in d["steps"]:
        rep(ES, f"{cid} 步驟「{h}」→教材", f"{TL}<b>{h}</b>：", f"{TJ}<b>{h}</b>：")
    for t in d["checks"]:
        rep(ES, f"{cid} 勾選「{t}」→教材", f"{TL}{t}", f"{TJ}{t}")

# ── B3 實質租金方塊 ──
rep(ES, "B3 e114-1 §130 方塊",
    '<span class="kf-c k-o">押金或保證金</span><span class="kf-op">＋</span><span class="kf-c k-g">權利金</span><span class="kf-op">＋</span><span class="kf-c k-n">其他相關運用收益</span>',
    '<span class="kf-c k-o">押金或保證金、權利金及其他相關運用收益</span>')
# ── B4／B5／B8／B10／B11／B12 預測依據的頻率說法 ──
rep(ES, "B4 pred-1 最高頻", "折舊為16年申論最高頻主題（105、107、111、112年共4題，另104年收益法折舊提存1題）",
    "折舊為16年申論高頻主題之一（105、107、111、112年共4題，另104年收益法折舊提存1題；土開法同為5題）")
rep(ES, "B5 pred-14 最高頻", "折舊是16年申論最高頻主題（105、107、111、112共4題，另104收益法折舊提存）",
    "折舊是16年申論高頻主題之一（105、107、111、112共4題，另104收益法折舊提存；土開法同為5題）")
rep(ES, "B8 pred-9 共7題", "成本法是16年申論最常出現的方法（折舊5題、成本法程序／重建重置2題，共7題）",
    "成本法是16年申論常出現的方法之一（折舊5題、重建重置與程序1題，共6題，與比較法並列）")
rep(ES, "B10 pred-13 依據", "（選擇題99-32、103-36、109-8、110-14考過），§125基地價值比率公式更被標為高頻計算題",
    "（選擇題99-32考過區分所有建物拆價；103-36、109-8考過權利變換基地價值比率之規定），§125基地價值比率公式可直接出計算")
rep(ES, "B11 pred-22 依據", "§44、§45、§47 在選擇題考過 7 題（101-33、100-24、102-13、110-20、113-14、106-25 等）",
    "§44、§45 在選擇題考過 5 題（101-33、101-37、102-13、110-20、113-14；另 100-24 考 §46 綜合率、106-25 考年金現值）")
rep(ES, "B11 歷年最愛", "§47 與 §30 的「有期限 vs 無限期」更是歷年最愛的對比點。", "§47 與 §30 的「有期限 vs 無限期」是易混對比點。")
rep(ES, "B12 pred-6 高頻題", "樓層別效用比為估價師實務高頻題，", "樓層別效用比在選擇題 G1 題群反覆出現，")
# ── B6 定率法中間值 ──
rep(ES, "B6a", '<span class="ljt tf">代入</span>r＝1－0.1¹⁄⁴⁰＝1－0.9442≈5.59%', '<span class="ljt tf">代入</span>r＝1－0.1¹⁄⁴⁰＝1－0.9441≈5.59%')
rep(ES, "B6b", '<div class="ljh">代入</div>r＝1－0.1¹⁄⁴⁰＝1－0.9442≈5.59%', '<div class="ljh">代入</div>r＝1－0.1¹⁄⁴⁰＝1－0.9441≈5.59%')
rep(ES, "B6c", "＝ 1 － 0.9442 ＝ 約 <strong>5.59%</strong>", "＝ 1 － 0.9441 ＝ 約 <strong>5.59%</strong>")
# ── B9 pred-13 §99／§100 一致 ──
rep(ES, "B9 §100 標題後公式",
    "§100 相減（區分所有建物；一般房地才是 §99）</b>：基地價格＝房地價格－建物成本價格；基地單價＝基地價格÷基地面積",
    "§100 相減（區分所有建物；一般房地才是 §99）</b>：基地權利價格＝房地價格－建物成本價格；基地權利單價＝基地權利價格÷基地持分面積；基地單價＝基地權利單價×平均地價分配率÷該建物之地價分配率")
rep(ES, "B9 口訣", "給成本→減（§99）", "給成本→減（§100）")
rep(ES, "B9 地圖", "§99 給成本→相減", "§100 給成本→相減")
rep(ES, "B9 結論", "則依§99相減", "則依§100相減")
# ── B13 §43 用字 ──
rep(ES, "B13 合理淨收益率", "正常淨收益率", "淨收益率（合理淨收益率）", 3)
rep(ES, "B13 貸款資金占不動產價格比率", "貸款常數×貸款比率", "貸款常數×貸款資金占不動產價格比率", 5)
# ── B15 e99-1 用 r ──
rep(ES, "B15 方塊", '<span class="kf-c k-s">R 資本化率或折現率</span>', '<span class="kf-c k-s">r 收益資本化率或折現率</span>')
rep(ES, "B15 標題", "資本化率 R（WACC）", "資本化率 r（WACC）")
rep(ES, "B15 算式", "R＝Σ（Wi×Ki）", "r＝Σ（Wi×Ki）", 4)
rep(ES, "B15 速寫", "R ＝ Σ（Wi × Ki）", "r ＝ Σ（Wi × Ki）")
# ── B16 C 的定義 ──
rep(ES, "B16 C＝建物總成本", "C＝重建成本、", "C＝建物總成本（重建或重置成本）、", 6)
# ── B18～B21 ──
rep(ES, "B18 §68 敘明", "，故估價人員並應敘明所選路徑與該建物特性、市場動態之對應理由。",
    "，作答時宜說明所選路徑與該建物特性、市場動態之對應理由（§68Ⅱ之敘明係就耐用年數之推估）。", 3)
rep(ES, "B19 §40 要件", "除考量建物收益資本化率外，加計未來每年折舊提存率。",
    "除考量建物收益資本化率或折現率外，應加計建物價格日期當時價值未來每年折舊提存率。", 3)
rep(ES, "B20 §26 先檢討", "差距≈24.2% ≥ 20%，須排除", "差距≈24.2% ≥ 20%，先重新檢討；檢討後仍達 20% 以上者排除")
rep(ES, "B21 n′", "(1＋r)<sup>－n</sup> 是", "(1＋r)<sup>－n′</sup> 是")
# ── B22 寫死的群組題數 ──
for o, n in [("收益法（4）", "收益法（7）"), ("成本法（10）", "成本法（11）"), ("A篇概念（10）", "A篇概念（14）"),
             ("🔴 A 必練（12）", "🔴 A 必練（14）"), ("🟡 B 了解（19）", "🟡 B 了解（25）"),
             ('<span class="g-vis" data-total="6">6題（含預測4）</span>', '<span class="g-vis" data-total="7">7題（含預測5）</span>')]:
    rep(ES, f"B22 {o[:10]}", o, n)

# ───────────────────────── C 組 ─────────────────────────
SY, CM, CO, ME, CF, FI, CA, HUB, RT = ("估價四大方法系統攻略.html", "估價_四大方法比較表.html", "估價_技術規則專欄.html",
                                       "估價彩色重點速記.html", "估價_易混淆概念並排.html", "估價_定義填空練習.html",
                                       "估價互動單字卡.html", "估價備考指揮中心.html", "估價_租金估計攻略表.html")
for fn, n in [(SY, 3), (CM, 1), (CO, 1), (ME, 1)]:
    rep(fn, "C1-6 (1－s) 標籤", "(1－s) 殘餘價格率", "(1－s) 1－殘餘價格率", n)
rep(SY, "C2 d 年折舊額", "d 年折舊額", "年折舊額")
rep(SY, "C7 §26 高低平均",
    '<div class="cl">平均值＝(800＋950＋850)÷3＝866.7萬<br></div><div class="cl">差距率＝(950−800)÷866.7＝150÷866.7≈17.3% &lt; 20% → 三件均保留</div>',
    '<div class="cl">高低平均值＝(950＋800)÷2＝875萬<br></div><div class="cl">差距率＝(950−800)÷875＝150÷875≈17.1% &lt; 20% → 三件均保留</div>')
rep(SY, "C8 §26 高低平均", "若乙改為1050萬：差距率＝(1050−800)÷900≈<b>27.8%</b> &gt; 20%",
    "若乙改為1050萬：差距率＝(1050−800)÷[(1050＋800)÷2]＝250÷925≈<b>27.0%</b> &gt; 20%")
for fn in (SY, ME):
    rep(fn, "C9/10 V 公式括號", '<span class="kf-op">－</span><span class="kf-c k-g">C 直接成本＋M 間接成本</span>',
        '<span class="kf-op">－</span><span class="kf-c k-g">(C 直接成本＋M 間接成本)</span>')
rep(CO, "C11 104-23", '<a class="qlk" href="估價_考題小卡.html#VE1_104_23">104-23</a> 官方答案用 1/4，與現行 §79 衝突，站上已標示。',
    '<a class="qlk" href="估價_考題小卡.html#VE1_104_23">104-23</a> 官方答案即 §79 公式（土地全額、建物×½）；「×1/4」是錯誤選項。')
rep(HUB, "C11 指揮中心 104-23", "官方 104-23 用 1/4（與現行衝突）", "104-23 官方答案即本式，「×1/4」是錯誤選項")
rep(SY, "C12 DCR 年份", '<span class="freq">109、111～114年出現</span>', '<span class="freq">104、106、111～114年出現</span>')
rep(SY, "C13 DCR 敘述", "近年高頻：109、112、113、114年均有考，必須能代入計算",
    "111～114 年連續出現（104-39、106-29、112-18、114-8 為代入計算），必須能代入計算")
rep(SY, "C14 定額法頻次", '<span class="freq">14年中考過12次</span>', '<span class="freq">16年中11個年度考過</span>')
rep(SY, "C15 三道排除", '三道排除規則 <span class="badge" style="background:var(--comp)">16年每年必考</span>',
    '三道排除規則 <span class="badge" style="background:var(--comp)">16年考過14年</span>')
rep(SY, "C16 調整順序", '整四步驟順序 <span class="badge" style="background:var(--comp)">每年必考</span>',
    '整四步驟順序 <span class="badge" style="background:var(--comp)">常考</span>')
rep(SY, "C17 折舊路徑", '折舊路徑速記 <span class="badge" style="background:var(--cost)">每年必考</span>',
    '折舊路徑速記 <span class="badge" style="background:var(--cost)">高頻</span>')
rep(SY, "C18 增值性", "和風險性方向相反，這是每年出現的陷阱。", "和風險性方向相反，這是常見陷阱（如 114-20）。")
rep(ME, "C19 速記三道排除", "<h3>★★★三道排除規則上限（每年必考）</h3>", "<h3>★★★三道排除規則上限（16年考過14年）</h3>")
rep(CF, "C20 易混淆三道排除", '<span class="rb-badge">每年必考</span>', '<span class="rb-badge">16年考過14年</span>')
rep(CF, "C21 調整順序", "比較法調整四順序（每年考順序題）", "比較法調整四順序（常考）")
rep(FI, "C22 §21", "技術規則§21★每年必考順序", "技術規則§21★常考順序")
rep(FI, "C23 §25-26", "技術規則§25-26★16年每年考", "技術規則§25-26★16年考過14年")
rep(SY, "C24 折舊前還原只適用建物", "<code>P＝淨收益÷(資本化率＋折舊提存率)</code>",
    "<code>建物收益價格＝建物折舊前淨收益÷(建物收益資本化率＋折舊提存率)</code>（§45）；房地則用 §46：土地率×土地價值比率＋(建物率＋折舊提存率)×建物價值比率")
for fn in (SY, CM, CO, ME):
    rep(fn, "C27 定率法符號", "不要和定率法的 d（每年對餘值打折的比率）", "不要和定率法的 r（每年對餘值打折的比率）")
rep(SY, "C28 利潤率 R", "(1＋r)×(1＋i)", "(1＋R)×(1＋i)")
rep(SY, "C28 利潤率 R", "r：適當之利潤率", "R：適當之利潤率")
rep(SY, "C28 利潤率 R", "利潤率r＝10%", "利潤率R＝10%")
rep(CM, "C29 利潤率 R", "（1 + r 利潤率）", "（1 + R 利潤率）")
rep(ME, "C30 利潤率 R", "（1＋r）<small>利潤率</small>", "（1＋R）<small>利潤率</small>")
rep(ME, "C30 利潤率 R", "(1＋r)×(1＋i)", "(1＋R)×(1＋i)")
rep(SY, "C31 GIM", '<span class="kf-c k-o">GIM 有效總收入乘數</span>', '<span class="kf-c k-o">有效總收入乘數</span>')
rep(CM, "C32 §36 用字", "有效總收入＝總收入 − 空置及收租損失。", "有效總收入＝總收入 − 閒置及其他原因所造成之收入損失（§36）。")
rep(CM, "C32 §36 用字", '<span class="kf-c k-o">− 空置及收租損失</span>', '<span class="kf-c k-o">− 閒置及其他原因所造成之收入損失</span>')
rep(CO, "C33 §36 用字", "閒置及其他收入損失", "閒置及其他原因所造成之收入損失", 2)
rep(HUB, "C33 §36 用字", "閒置及其他收入損失", "閒置及其他原因所造成之收入損失")
rep(SY, "C34 客觀", '<span class="kf-c k-s">未來平均1年期間淨收益</span>', '<span class="kf-c k-s">未來平均1年期間之客觀淨收益</span>')
rep(CF, "C35 §57 並列", "（§57 替代算法；首選依內政部建築師酬金標準表及縣市政府造價表計算）",
    "（§57 兩種算法擇一：依內政部建築師酬金標準表及縣市政府建造執照工程造價表計算，或按實際營造施工費 2%～3% 推估）")
rep(CM, "C36 E1 題數", "★鐵打必考　選擇24題｜申論5次", "★鐵打必考　土開選擇25題｜申論5次")
rep(CA, "C37 §125 用字", "基地價值比率＝素地總價值÷（素地總價值＋建物成本價格〔營造施工費單價×(1－累積折舊率)×全棟面積〕）",
    "基地價值比率＝〔素地單價×基地總面積〕÷〔素地單價×基地總面積＋（營造或施工費單價×(1－累積折舊率)×全棟建物面積）〕")

# C25／C26：租金統計區依題庫重算並依次數重排
OLD_ST = re.compile(r'<div class="st-list">.*?</div>\n</div>', re.S)
rt = (R / RT).read_text(encoding="utf-8")
m = OLD_ST.findall(rt)
CARD = ('  <div class="st-card">\n    <div class="st-top"><span class="st-tag {t}">{tn}</span><span class="st-name">{name}</span>'
        '<span class="st-n">{n} 次</span></div>\n    <div class="st-bar"><i class="{t}" style="width:{w}%"></i></div>\n'
        '    <div class="st-years">{ys}<span class="st-yl">年</span></div>\n    <div class="st-tip">{tip}</div>\n  </div>\n')
ROWS = [("h", "最高頻", "估計以何種租金為原則", ["103", "105", "112", "113", "114"], "答案永遠是「實質租金」"),
        ("m", "高頻", "實質租金計算", ["103", "104", "105", "113"], "支付租金＋押金運用收益；押金「N 個月」先換算成金額"),
        ("m", "高頻", "差額分配法", ["100", "102", "106", "110"], "100、102、106 考計算；110 考「差額」的定義"),
        ("m", "高頻", "DCF 法的淨收益基準", ["102", "104", "105", "110"], "證券化採 DCF：以「契約租金」計，不是實質租金"),
        ("l", "中頻", "限定租金辨識", ["99", "106", "107"], "關鍵字：續訂、合併、擴租"),
        ("l", "中頻", "新訂 vs 續訂估計方式", ["101", "104", "105"], "企業總收入法 → 只適用新訂（價格×租金收益率 §132②、§133② 新訂續訂都有）")]
if len(m) != 1:
    fail.append(f"✗ {RT}｜統計區定位 {len(m)}")
else:
    body = '<div class="st-list">\n' + "".join(
        CARD.format(t=t, tn=tn, name=nm, n=len(ys), w=round(len(ys) / 6 * 100),
                    ys="".join(f'<span class="st-y">{y}</span>' for y in ys), tip=tip) for t, tn, nm, ys, tip in ROWS) + "</div>\n</div>"
    files[RT] = rt.replace(m[0], body, 1)
    print(f"  ✔ {RT}｜統計區重排（實質租金計算 4、DCF 基準 4）")

# ───────────────────────── lj_data.json 同步 ─────────────────────────
LJ = HERE / "lj_data.json"
raw = LJ.read_text(encoding="utf-8")
for o, n in [("1－0.9442", "1－0.9441"), ("正常淨收益率", "淨收益率（合理淨收益率）"),
             ("貸款常數×貸款比率", "貸款常數×貸款資金占不動產價格比率"), ("R＝Σ（Wi×Ki）", "r＝Σ（Wi×Ki）"),
             ("資本化率 R（WACC）", "資本化率 r（WACC）"), ("C＝重建成本、", "C＝建物總成本（重建或重置成本）、"),
             ("給成本→減（§99）", "給成本→減（§100）"), ("§99 給成本→相減", "§100 給成本→相減"),
             ("差距≈24.2% ≥ 20%，須排除", "差距≈24.2% ≥ 20%，先重新檢討；檢討後仍達 20% 以上者排除"),
             ("，故估價人員並應敘明所選路徑與該建物特性、市場動態之對應理由。",
              "，作答時宜說明所選路徑與該建物特性、市場動態之對應理由（§68Ⅱ之敘明係就耐用年數之推估）。"),
             ("除考量建物收益資本化率外，加計未來每年折舊提存率。",
              "除考量建物收益資本化率或折現率外，應加計建物價格日期當時價值未來每年折舊提存率。"),
             ("基地價格＝房地價格－建物成本價格；基地單價＝基地價格÷基地面積", "基地權利價格＝房地價格－建物成本價格；基地權利單價＝基地權利價格÷基地持分面積；基地單價＝基地權利單價×平均地價分配率÷該建物之地價分配率")]:
    c = raw.count(o)
    raw = raw.replace(o, n)
    print(f"  ・lj_data {o[:16]}：{c} 處")
data = json.loads(raw)
byk = {d["k"]: d for d in data}
for cid, d in LAB.items():
    card = byk[cid]
    for h in d["steps"]:
        hit = [st for sb in card["subs"] for st in sb["steps"] if st.get("lawh") == h]
        if len(hit) != 1:
            fail.append(f"✗ lj_data {cid} 步驟 {h}：{len(hit)}")
        for st in hit:
            st["lt"] = "教材"
    for t in d["checks"]:
        hit = [c for c in card["checks"] if c["txt"].startswith(t)]
        if len(hit) != 1:
            fail.append(f"✗ lj_data {cid} 勾選 {t}：{len(hit)}")
        for c in hit:
            c["lt"] = "教材"

# gen_lj.py 支援 lt
G = HERE / "gen_lj.py"
g = G.read_text(encoding="utf-8")
o1 = "if st.get('lawh'): A += f'<p><span class=\"ljt tl\">{tl}</span><b>{E(st[\"lawh\"])}</b>：{E(st[\"law\"])}</p>'"
n1 = "if st.get('lawh'): A += f'<p><span class=\"ljt tl\">{st.get(\"lt\", tl)}</span><b>{E(st[\"lawh\"])}</b>：{E(st[\"law\"])}</p>'"
o2 = "t, cls = {'law': (tl, 'tl'), 'fact': (tf, 'tf'), 'ans': ('答', 'ta')}[c['t']]"
n2 = o2 + "\n        if c.get('lt'): t = c['lt']"
if g.count(o1) != 1 or g.count(o2) != 1:
    fail.append(f"✗ gen_lj.py lt 支援：{g.count(o1)} {g.count(o2)}")
else:
    g = g.replace(o1, n1).replace(o2, n2)

if fail:
    print("\n".join(fail))
    sys.exit("\n有項目對不上，全部不寫檔。")
for fn, s in files.items():
    (R / fn).write_text(s, encoding="utf-8")
LJ.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
G.write_text(g, encoding="utf-8")
print(f"寫入 {len(files)} 個頁面＋lj_data.json＋gen_lj.py")
