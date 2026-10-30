#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-30：使用者「既然考過為什麼不在旁邊帶入連結跳轉練習呢」。
在《計算題攻略》每張題型卡、《四大方法系統攻略》各考點旁，嵌入站上既有的「可作答」考古題面板
（bxv-topic-qa.js，v555；作答寫進共用 bxv-q2，刷題頁、錯題本、日拱一築都看得到）。
題號清單來自 F 組逐題歸類表（audit_F_table.json，S＋B 口徑合併：要計算的題＋考該公式概念的題），
全部確認存在於 bxv-quiz-data.js。
只跑一次；每個插入點斷言唯一，對不上整支不寫檔。
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
T = json.load(open("/tmp/claude-0/-home-claude/ac4bbd9f-3aea-5322-85d9-48ab97ee8f14/scratchpad/audit_F_table.json", encoding="utf-8"))
KEYS = set()
for l in open(R / "bxv-quiz-data.js", encoding="utf-8"):
    l = l.strip().rstrip(",")
    if l.startswith('{"id"'):
        r = json.loads(l)
        KEYS.add(f"{r['y']}-{r['n']}")
fail = []


def ids(*keys, extra=()):
    s = set(extra)
    for k in keys:
        for part in ("choice_S", "choice_B"):
            for v in T[k].get(part, {}).values():
                s |= set(v)
    bad = [x for x in s if x not in KEYS]
    if bad:
        fail.append(f"✗ 題號不存在：{bad}")
    return ",".join(sorted(s, key=lambda x: (int(x.split("-")[0]), int(x.split("-")[1]))))


def panel(qs, title):
    return f'<div class="bxv-tq" data-qs="{qs}" data-title="{title}"></div>'


def elem_end(s, start):
    """start 指向 <div 開頭，回傳對應 </div> 結尾位置"""
    d = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[start:]):
        d += -1 if m.group(1) else 1
        if d == 0:
            return start + m.end()
    raise ValueError("div 不平衡")


def insert_in(s, anchor, inner_cls, html, name):
    """在 anchor 所在元素內、class=inner_cls 的子元素結尾前插入；inner_cls=None 則插在 anchor 元素結尾前"""
    if s.count(anchor) != 1:
        fail.append(f"✗ {name}：定位 {s.count(anchor)} 次")
        return s
    a = s.index(anchor)
    a = s.rfind("<div", 0, a + 1) if not anchor.startswith("<div") else a
    e = elem_end(s, a)
    if inner_cls:
        b = s.find(f'<div class="{inner_cls}"', a, e)
        if b < 0:
            fail.append(f"✗ {name}：找不到 {inner_cls}")
            return s
        e = elem_end(s, b)
    pos = e - len("</div>")
    print(f"  ✔ {name}")
    return s[:pos] + html + s[pos:]


def add_script(s, name):
    if "bxv-topic-qa.js" in s:
        return s
    if s.count("</body>") != 1:
        fail.append(f"✗ {name}：</body> 不唯一")
        return s
    return s.replace("</body>", '<script src="bxv-topic-qa.js" defer></script>\n</body>')


# ───────── 計算題攻略 ─────────
C = R / "估價_計算題攻略.html"
c = C.read_text(encoding="utf-8")
CARDS = [
    ('<div class="calc-card" id="cc-dep1">', ids("定額法(等速)"), "定額法・折舊計算 考古題"),
    ('<div class="calc-card" id="cc-dep2">', ids("定率法(初期加速)"), "定率法・折舊路徑 考古題"),
    ('<div class="calc-card" id="cc-dep3">', ids("償債基金法(初期減速)"), "償債基金法・折舊路徑 考古題"),
    ('<div class="calc-card" id="cc-dev">', ids("土地開發V公式(含資本利息綜合利率)"), "土地開發分析法 考古題"),
    ('<div class="calc-card" id="cc-cmp">', ids("比較法排除門檻(15%/30%/20%)"), "比較法 15%／30%／20% 考古題"),
    ('<div class="calc-card" id="cc-cap">', ids("資本化率計算(§43五種方法)", "WACC", "債務保障比率法"), "§43 五種資本化率 考古題"),
    ('<div class="calc-card" id="cc-rent">', ids("實質租金(押金運用收益)"), "實質租金 考古題"),
    ('<div class="calc-card" id="cc-floor">', ids("樓層別效用比/地價分配率"), "樓層別效用比 考古題"),
    ('<div class="calc-card" id="split-card">', ids("房地拆價(§99/§101-1/§126)"), "房地拆價 考古題"),
    ('<div class="calc-card" id="annuity-card">', ids("年金現值(§47/可貸金額)"), "年金現值 考古題"),
]
for anchor, qs, title in CARDS:
    c = insert_in(c, anchor, "calc-card-body", panel(qs, title), f"計算題攻略 {title}")
for t_anchor, qs, title in [
    ("收益法④：殘餘法（§44 土地、§45 建物）", ids("殘餘法(§44/§45)"), "殘餘法 考古題"),
    ("收益法⑤：房地綜合收益資本化率（§46）", ids("房地綜合收益資本化率(§46)"), "房地綜合收益資本化率 考古題"),
    ("收益法⑥：折舊提存率 d（§41 等速折舊型）", ids("折舊提存率d(§41)", extra=("103-28",)), "折舊提存率 考古題"),
]:
    if c.count(t_anchor) != 1:
        fail.append(f"✗ ⑤ 卡 {t_anchor}：{c.count(t_anchor)}")
        continue
    i = c.index(t_anchor)
    a = c.rfind('<div class="calc-card"', 0, i)
    e = elem_end(c, a)
    b = c.find('<div class="calc-card-body"', a, e)
    eb = elem_end(c, b) - len("</div>")
    c = c[:eb] + panel(qs, title) + c[eb:]
    print(f"  ✔ 計算題攻略 {title}")
for anchor, qs, title in [
    ('<div class="not-yet-card" id="ny-dep2">', ids("定率法(初期加速)"), "定率法 考古題"),
    ('<div class="not-yet-card" id="ny-dcr">', ids("債務保障比率法"), "債務保障比率法 考古題"),
    ('<div class="not-yet-card" id="ny-dcf">', ids("DCF"), "DCF 考古題"),
]:
    c = insert_in(c, anchor, None, panel(qs, title), f"計算題攻略 ④ {title}")
c = add_script(c, "計算題攻略")

# ───────── 四大方法系統攻略 ─────────
S = R / "估價四大方法系統攻略.html"
s = S.read_text(encoding="utf-8")
s23 = "100-21,101-22,103-21,104-36,106-7"
for k in s23.split(","):
    if k not in KEYS:
        fail.append(f"✗ 題號不存在 {k}")
a1 = "📌 判斷邏輯：這些情況的影響<b>無法有效掌握及量化調整</b>時，才不予採用。"
if s.count(a1) != 1:
    fail.append("✗ §23 判斷邏輯定位")
i = s.index(a1)
blk = s.rfind('<div class="block">', 0, i)
e = elem_end(s, blk)
s = s[:e] + panel(s23, "§23 特殊交易／不予採用 考古題") + s[e:]
print("  ✔ 系統攻略 §23 面板")
a2 = '<div class="kf"><div class="kf-step"><div class="kf-t"><b>★</b>某筆土地合併後分配價格</div>'
if s.count(a2) != 1:
    fail.append("✗ 合併開發 kf 定位")
else:
    i = s.index(a2)
    e = elem_end(s, i)
    s = s[:e] + panel(ids("合併開發分配"), "合併開發分配 考古題") + s[e:]
    print("  ✔ 系統攻略 合併開發面板")
# 各分頁末尾放整章練習
for tab, chs, title in [("tab-cost", "C1,C2", "成本法（C1 重建成本・C2 折舊）整章考古題"),
                        ("tab-comp", "B,G1", "比較法（B 比較法・G1 樓層效用）整章考古題"),
                        ("tab-income", "D1,D2,D3", "收益法（D1～D3）整章考古題"),
                        ("tab-land", "E1", "土地開發分析法（E1）整章考古題")]:
    anc = f'<div class="content" id="{tab}">'
    if s.count(anc) != 1:
        fail.append(f"✗ {tab}：{s.count(anc)}")
        continue
    a = s.index(anc)
    e = elem_end(s, a) - len("</div>")
    s = s[:e] + f'\n  <div class="bxv-tq" data-chs="{chs}" data-title="{title}"></div>\n' + s[e:]
    print(f"  ✔ 系統攻略 {tab} 整章面板")
s = add_script(s, "系統攻略")

if fail:
    print("\n".join(fail))
    sys.exit("\n有項目對不上，全部不寫檔。")
C.write_text(c, encoding="utf-8")
S.write_text(s, encoding="utf-8")
print("寫入完成")
