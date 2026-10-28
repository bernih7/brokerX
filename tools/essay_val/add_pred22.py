#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新增申論卡 pred-22：殘餘法（§44 土地、§45 建物）＋ §47 一定期間收益價格。

為什麼補這張：6 張收益法申論卡裡，§44、§45、§47 **一條都沒碰到**，
但這三條在選擇題考過 7 題（§44/§45：101-33、100-24、102-13、110-20、113-14；
§47：106-25），而且算式只有一兩行，極適合出小計算。

公式與數字全部取自站上《估價_計算題攻略》⑥收益法補充（已對技術規則逐字核實），
沒有自行推導。(二) 的數字同 110-20，(三) 同 106-25。

同時更新三個寫死的題數（新增一張卡就會過期）：
  bxv-use.js  TOT.essay 53→54、「官方 32＋預測 21」→22
  申論頁 footer「官方32題＋預測21題」→22
  指揮中心「官方32題＋預測6題」→22（這個數字本來就已經過期，站上早就 21 張）

可重複執行。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PAGE = ROOT / "不動產估價概要_申論題實戰範文.html"
LJ = Path(__file__).resolve().parent / "lj_data.json"
USE = ROOT / "bxv-use.js"
HUB = ROOT / "估價備考指揮中心.html"

CARD = '''<div class="essay-card" data-v="lj" id="pred-22" data-pri="A" data-type="income">
  <div class="card-header" onclick="toggleCard(this)">
    <div class="card-header-left">
      <span class="card-year tier-p">🔮 115預測㉒｜A級</span>
      <div class="card-title">【115預測㉒】殘餘法：土地收益價格與建物收益價格（§44、§45）＋一定期間收益價格（§47）</div>
      <div class="card-meta"><span class="tag">§44</span><span class="tag">§45</span><span class="tag">§47</span><span class="tag">殘餘法</span><span class="tag">計算</span><span class="tag" style="background:#fff7e6;border-color:var(--key);color:var(--key);">模擬題</span></div>
    </div>
    <button class="read-btn" id="rbtn-pred-22" onclick="event.stopPropagation();toggleRead('pred-22')">☐ 已讀</button>
    <span class="card-arrow">▼</span>
  </div>
  <div class="card-body">
    <div class="q-box">
      <strong>【模擬題】</strong> 依不動產估價技術規則：(一)土地收益價格與建物收益價格各應如何求取？請列式說明，並說明「折舊前淨收益」與「已扣除折舊提存費之淨收益」在算式上的差別。(二)某房地之年淨收益（已扣折舊提存費）為100萬元，建物成本價格2,000萬元、建物收益資本化率3%、土地收益資本化率2%，試求土地收益價格。(三)某不動產可收益年數10年，每年折舊前淨收益10萬元，收益資本化率3%，試求其收益價格。（25分）
    </div><div class="pred-info"><strong>🔮 預測依據：</strong>§44、§45、§47 在選擇題考過 7 題（101-33、100-24、102-13、110-20、113-14、106-25 等），但<strong>六張收益法申論卡一條都沒碰到</strong>；算式短、數字好給，是典型的小計算題材。§47 與 §30 的「有期限 vs 無限期」更是歷年最愛的對比點。</div>
    <div class="quick-ans">
      <div class="qa-blk qa-def"><div class="qa-label">▌ 三條公式各管什麼</div>
        <b>§44</b> 求<b>土地</b>收益價格（建物那半已知）｜<b>§45</b> 求<b>建物</b>收益價格（土地那半已知）｜<b>§47</b> <b>一定期間</b>的收益價格（有年限，要乘年金現值係數）
      </div>
      <div class="qa-blk qa-form"><div class="qa-label">▌ 公式</div>
        土地收益價格＝（房地淨收益－<b>建物成本價格×建物收益資本化率</b>）÷ 土地收益資本化率（§44）<br>
        建物收益價格＝（房地淨收益－<b>土地價格×土地收益資本化率</b>）÷ 建物收益資本化率（§45）<br>
        P＝a×[1－1÷(1＋r)<sup>n′</sup>]÷r（§47；a＝平均一年期間<b>折舊前</b>淨收益）
      </div>
      <div class="qa-blk qa-calc"><div class="qa-label">▌ 代入</div>
        (二) 建物淨收益＝2,000×3%＝60萬；土地淨收益＝100－60＝40萬；土地收益價格＝40÷2%＝<b>2,000萬元</b><br>
        (三) 係數＝[1－1÷1.03<sup>10</sup>]÷0.03＝(1－0.74409)÷0.03＝<b>8.5302</b>；P＝10萬×8.5302≈<b>85.3萬元</b>
      </div>
      <div class="qa-blk qa-trap"><div class="qa-label">▌ 常見失分點</div>
        題目說「<b>折舊前</b>／未扣折舊提存費」→ <b>建物那一半</b>的率要<b>加折舊提存率</b>；說「已扣除」→ 不加。<b>土地永遠不折舊</b>，土地那半只用土地收益資本化率（113-14 的錯誤選項就是分母少了折舊提存率）。<br>
        §47 有年限 → 要乘<b>年金現值係數</b>；§30 直接資本化法是<b>無限期</b> → P＝a÷r 直接除。看到「一定期間」「可收益年數」「10 年」就不能直接除。<br>
        (1＋r)<sup>－n</sup> 是<b>負</b>次方，先算 1.03<sup>10</sup>＝1.3439 再<b>取倒數</b>，不要忘了被 1 減。<br>
        ⚠️「<b>殘餘法</b>」是<b>教材用語</b>，技術規則只寫公式、沒有這個名稱（101-33 答「殘餘法」）。
      </div>
    </div>
    <div class="detail-content">

    <div class="section-h">一、定義：兩種殘餘與一種有期限收益</div>
    <p>收益法求取收益價格時，若房地之淨收益已知，而土地與建物其中一方之價格或淨收益可先行確定，即可將房地淨收益扣除「已知的那一半」，剩餘部分還原為「未知的那一半」之收益價格，實務與教材稱為<strong>殘餘法</strong>；<strong>技術規則僅規定算式，並未使用「殘餘法」此一名稱</strong>。另一種情形為收益年限並非永續，而是限於一定期間，此時收益價格不得以永續年金直接除，應以<strong>年金現值</strong>之觀念折現。</p>

    <div class="section-h">二、法條（§44、§45、§47）</div>
    <ul>
      <li><strong>§44 土地收益價格</strong>：建物淨收益＝建物成本價格×建物收益資本化率；房地淨收益減建物淨收益即土地淨收益，再除以土地收益資本化率。淨收益<strong>已扣除</strong>折舊提存費者適用第二項第一款；屬<strong>折舊前</strong>淨收益者，依第二項第二款，建物該半須以「建物收益資本化率<strong>＋</strong>建物價格日期當時價值未來每年折舊提存率」計算。</li>
      <li><strong>§45 建物收益價格</strong>：方向相反。土地淨收益得先以比較法求取土地比較價格，再乘土地收益資本化率；房地淨收益減土地淨收益後，除以建物收益資本化率（折舊前者同樣加計折舊提存率）。</li>
      <li><strong>§47 一定期間之收益價格</strong>：P＝a×[1－1÷(1＋r)<sup>n′</sup>]÷r，a 為平均一年期間<strong>折舊前</strong>淨收益、r 為收益資本化率、n′ 為可收益之年數；一定期間終止後有期末價值者，收益價格<strong>得加計該期末價值之現值</strong>，期末價值並得扣除處分不動產所需之相關費用。條文另明定<strong>收益價格已知者，得適用該公式反推</strong>平均一年期間折舊前淨收益。</li>
    </ul>

    <div class="section-h">三、涵攝（代入本題）</div>
    <p><strong>（一）土地收益價格（§44）</strong>：本題淨收益已扣折舊提存費，故建物該半不加折舊提存率。</p>
    <div class="note">建物淨收益＝2,000萬×3%＝<b>60萬元</b>　→　土地淨收益＝100萬－60萬＝<b>40萬元</b>　→　土地收益價格＝40萬÷2%＝<b>2,000萬元</b></div>
    <p><strong>（二）一定期間收益價格（§47）</strong>：可收益年數 10 年，屬一定期間，應乘年金現值係數。</p>
    <div class="note">年金現值係數＝[1－1÷1.03<sup>10</sup>]÷0.03＝(1－0.74409)÷0.03＝<b>8.5302</b>　→　P＝10萬×8.5302≈<b>85.3萬元</b></div>
    <p>若本題改為永續收益，則依 §30 直接資本化法 P＝10萬÷3%≈333.3萬元，與 85.3 萬元差距甚大，可見「有無年限」對收益價格之影響極為關鍵。</p>

    <div class="section-h">四、結論</div>
    <p class="conclusion">綜上，土地與建物收益價格之求取，係以房地淨收益扣除可先確定之一方淨收益後，就餘額以各自之收益資本化率還原（§44、§45）；淨收益<strong>是否已扣折舊提存費</strong>，決定建物該半之分母是否加計折舊提存率，土地則因不折舊而始終僅用土地收益資本化率。本題土地收益價格為<strong>2,000萬元</strong>。至收益期間有年限者，應依 §47 乘以年金現值係數折現，本題為<strong>85.3萬元</strong>，與永續還原之結果差異甚鉅，估價時務必先確認收益期間究為永續或一定期間。<br><span class="zj">結尾卓見</span>先問「哪一半已知、折舊扣了沒、收益有沒有年限」，三問定分，<span class="zjk">算式自明</span>。</p>

    </div>
  </div>
</div>
'''

LJ_ENTRY = {
    "k": "pred-22", "kind": "calc",
    "subs": [
        {"q": "土地收益價格與建物收益價格各如何求取？折舊前與已扣折舊有何差別？",
         "kind": "explain",
         "steps": [
             {"ask": "已知的是哪一半？", "lawh": "§44／§45 的分工",
              "law": "§44 用建物那半去推土地；§45 用土地那半去推建物。",
              "facth": "怎麼判斷", "fact": "題目先給誰的價格或淨收益，就從誰扣起。",
              "res": "先認哪一半已知，才知道用哪一條。", "key": "給建物用§44 給土地用§45",
              "link": "扣完之後怎麼還原？"},
             {"ask": "扣完之後怎麼還原？", "lawh": "條文算式",
              "law": "房地淨收益－已知那半之淨收益＝未知那半之淨收益，再除以該半之收益資本化率。",
              "facth": "折舊前要加率", "fact": "淨收益為折舊前者，建物那半之分母須加計折舊提存率（§44Ⅱ②）；土地不折舊，永遠只用土地收益資本化率。",
              "res": "分子相減、分母看折舊扣了沒。", "key": "折舊前→建物加折舊提存率"}],
         "ans": "依**§44**由建物推土地、**§45**由土地推建物；房地淨收益扣掉已知那半，再除以該半之收益資本化率。淨收益若為**折舊前**，**建物**那半分母要加**折舊提存率**；**土地不折舊**，不加。"},
        {"q": "求土地收益價格（房地淨收益100萬、建物成本價格2,000萬、建物率3%、土地率2%）。",
         "kind": "calc",
         "steps": [
             {"ask": "先算哪一步？", "lawh": "公式",
              "law": "建物淨收益＝建物成本價格×建物收益資本化率",
              "facth": "代入", "fact": "2,000萬×3%",
              "res": "建物淨收益 60 萬元。", "key": "2000×3%＝60萬", "link": "剩下的是誰的？"},
             {"ask": "剩下的是誰的？", "lawh": "公式",
              "law": "房地淨收益－建物淨收益＝土地淨收益；÷土地收益資本化率＝土地收益價格",
              "facth": "代入", "fact": "100萬－60萬＝40萬；40萬÷2%",
              "res": "土地收益價格 2,000 萬元。", "key": "(100－60)÷2%＝2000萬"}],
         "ans": "建物淨收益＝2,000×3%＝**60萬**；土地淨收益＝100－60＝**40萬**；土地收益價格＝40÷2%＝**2,000萬元**。",
         "pre": "題目說淨收益已扣折舊提存費，所以建物那半不加折舊提存率。"},
        {"q": "求一定期間之收益價格（年淨收益10萬、10年、資本化率3%）。",
         "kind": "calc",
         "steps": [
             {"ask": "可以直接除嗎？", "lawh": "§30 vs §47",
              "law": "§30 直接資本化法是無限期，P＝a÷r；§47 是一定期間，要乘年金現值係數。",
              "facth": "本題", "fact": "題目寫「可收益年數10年」＝一定期間。",
              "res": "不能直接除，要用 §47。", "key": "有年限→不能直接除", "link": "係數怎麼算？"},
             {"ask": "係數怎麼算？", "lawh": "§47 公式",
              "law": "P＝a×[1－1÷(1＋r)ⁿ′]÷r",
              "facth": "代入", "fact": "1.03¹⁰＝1.3439 → 取倒數 0.74409；(1－0.74409)÷0.03＝8.5302；10萬×8.5302",
              "res": "收益價格約 85.3 萬元。", "key": "10萬×8.5302≈85.3萬"}],
         "ans": "係數＝[1－1÷1.03¹⁰]÷0.03＝**8.5302**；P＝10萬×8.5302≈**85.3萬元**。若誤用永續還原（§30）會算成 10萬÷3%≈333.3萬，差了四倍。"}],
    "checks": ["先認哪一半已知（§44 還是 §45）", "淨收益折舊扣了沒（決定建物分母加不加折舊提存率）",
               "土地不折舊，只用土地收益資本化率", "有年限用 §47 乘年金現值係數，不可直接除",
               "(1＋r) 的負次方要先取倒數", "「殘餘法」是教材用語，不是條文名稱"],
    "kw": ["土地收益價格", "建物收益價格", "折舊提存率", "收益資本化率", "年金現值係數",
           "一定期間", "平均一年期間折舊前淨收益", "期末價值"],
    "mnem": "先認哪半、再看折舊、最後問年限",
}

COUNTS = [
    (USE, "essay:53", "essay:54"),
    (USE, "（官方 32＋預測 21）", "（官方 32＋預測 22）"),
    (PAGE, "官方32題＋預測21題（99–114年）", "官方32題＋預測22題（99–114年）"),
    (HUB, "申論題攻略表（官方32題＋預測6題，🔴🟡🟢三級）", "申論題攻略表（官方32題＋預測22題，🔴🟡🟢三級）"),
]


def main():
    s = PAGE.read_text(encoding="utf-8")
    if 'id="pred-22"' in s:
        print("  － pred-22 已存在，略過插卡")
    else:
        anchor = '<div class="essay-card" data-v="lj" id="pred-11"'
        if s.count(anchor) != 1:
            sys.exit(f"找不到插入位置（pred-11 出現 {s.count(anchor)} 次）")
        s = s.replace(anchor, CARD + anchor, 1)
        PAGE.write_text(s, encoding="utf-8")
        print("  ✔ 插入 pred-22（排在 pred-11 之前，同屬收益法組）")

    d = json.loads(LJ.read_text(encoding="utf-8"))
    if any(x["k"] == "pred-22" for x in d):
        print("  － lj_data 已有 pred-22")
    else:
        i = next(n for n, x in enumerate(d) if x["k"] == "pred-11")
        d.insert(i, LJ_ENTRY)
        LJ.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  ✔ lj_data 新增 pred-22（共 {len(d)} 筆）")

    for path, old, new in COUNTS:
        t = path.read_text(encoding="utf-8")
        if new in t:
            print(f"  － {path.name} 題數已是新值")
            continue
        if t.count(old) != 1:
            sys.exit(f"✗ {path.name}：找不到（或不只一處）{old!r}")
        path.write_text(t.replace(old, new, 1), encoding="utf-8")
        print(f"  ✔ {path.name}：{old} → {new}")


if __name__ == "__main__":
    main()
