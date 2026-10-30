#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-30 估價計算全面複核：F 組（《計算題攻略》出現年統計）— 依使用者選擇重建。
使用者決定：①只算「要動手算」的題（S 口徑，與頁面圖例「選＝選擇題考計算」一致）；
           ②「風險等級」「115年預測」兩欄沒有依據 → 改成可查證的「最近一次考」。
資料：scratchpad/audit_F_table.json（F 組以 bxv-quiz-data.js 520 題＋申論範文 32 張官方卡逐題歸類）。
本腳本：重建頁首 ribbon 三格、①總覽表、③矩陣；②⑤卡片次數與 chips、文字敘述依 F 組定位字串修正。
只跑一次。每項斷言出現次數，對不上整支不寫檔。
"""
import json
import re
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent.parent
P = R / "估價_計算題攻略.html"
T = json.load(open("/tmp/claude-0/-home-claude/ac4bbd9f-3aea-5322-85d9-48ab97ee8f14/scratchpad/audit_F_table.json", encoding="utf-8"))
FI = json.load(open("/tmp/claude-0/-home-claude/ac4bbd9f-3aea-5322-85d9-48ab97ee8f14/scratchpad/F_items.json", encoding="utf-8"))
s = P.read_text(encoding="utf-8")
fail = []
YEARS = list(range(99, 115))
CN = "一二三四五"


def rep(name, old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        fail.append(f"✗ {name}：出現 {c} 次（應為 {n}）")
        return
    s = s.replace(old, new)
    print(f"  ✔ {name}")


def S(key):
    d = T[key]
    ch = {int(y): v for y, v in d.get("choice_S", {}).items()}
    es = {int(y): v for y, v in d.get("essay_S", {}).items()}
    return ch, es


def latest(key):
    ch, es = S(key)
    ys = sorted(set(ch) | set(es))
    if not ys:
        return "未考過計算", 0
    y = ys[-1]
    ids = list(ch.get(y, [])) + [f"{e[1:4]}申{CN[int(e.split('-')[1]) - 1]}" for e in es.get(y, [])]
    return f"{y}（{'、'.join(ids)}）", y


# ── 頁首 ribbon ──
for lab, key, kind in [("折舊計算出現年", "成本法折舊計算(三法合計)", "union"),
                       ("資本化率計算年", "資本化率計算(§43五種方法)", "union"),
                       ("土地開發申論次", "土地開發V公式(含資本利息綜合利率)", "essay")]:
    ch, es = S(key)
    v = len(set(ch) | set(es)) if kind == "union" else sum(len(x) for x in es.values())
    pat = re.compile(r'<div class="stat-num">\d+</div>(\s*)<div class="stat-label">' + lab + "</div>")
    if len(pat.findall(s)) != 1:
        fail.append(f"✗ ribbon {lab}")
    else:
        s = pat.sub(lambda m: f'<div class="stat-num">{v}</div>{m.group(1)}<div class="stat-label">{lab}</div>', s)
        print(f"  ✔ ribbon {lab} → {v}")

# ── ① 總覽表 ──
ROWKEY = [("成本法折舊計算", "成本法折舊計算(三法合計)"), ("資本化率計算", "資本化率計算(§43五種方法)"),
          ("比較法調整率計算", "比較法排除門檻(15%/30%/20%)"), ("土地開發V公式計算", "土地開發V公式(含資本利息綜合利率)"),
          ("實質租金計算", "實質租金(押金運用收益)"), ("樓層別效用比計算", "樓層別效用比/地價分配率"),
          ("直接資本化收益價格", "直接資本化收益價格(P=a÷r)"), ("WACC", "WACC"), ("合併開發", "合併開發分配"),
          ("都更基地價值比率", "都更基地價值比率(§125)"), ("DCF折現現金流量", "DCF")]
a = s.find('<table class="overview-table">')
b = s.find("</table>", a) + len("</table>")
tbl = s[a:b]
rows = re.findall(r"<tr>\s*(<td>.*?</td>)\s*(<td>[^<]*</td>)\s*<td>\d+</td>.*?</tr>", tbl, re.S)
if len(rows) != 11:
    fail.append(f"✗ ①表列數 {len(rows)}")
else:
    out = []
    for name_td, meth_td in rows:
        nm = re.sub(r"<[^>]+>", "", name_td)
        key = next((k for p, k in ROWKEY if nm.startswith(p)), None)
        if not key:
            fail.append(f"✗ ①表找不到題型 {nm}")
            continue
        ch, es = S(key)
        cy, ec = len(ch), sum(len(x) for x in es.values())
        lt, ly = latest(key)
        name_td = name_td.replace("各期現金流÷(1+r)ⁿ加總", "各期淨收益與期末價值以 Y 折現加總（§32）")
        name_td = name_td.replace("素地價值÷（素地價值＋建物成本×(1－累積折舊率)）（§125）",
                                  "素地價值÷〔素地價值＋營造或施工費單價×(1－累積折舊率)×全棟建物面積〕（§125）")
        out.append((cy + ec, ly, f"""        <tr>
          {name_td}
          {meth_td}
          <td>{cy}</td>
          <td>{ec}</td>
          <td><strong>{cy + ec}</strong></td>
          <td style="font-size:12px">{lt}</td>
        </tr>"""))
    out.sort(key=lambda x: (-x[0], -x[1]))
    new_tbl = """<table class="overview-table">
      <thead>
        <tr>
          <th style="text-align:left;min-width:160px">計算題型</th>
          <th>所屬方法</th>
          <th>選擇題<br>出現年</th>
          <th>申論題<br>出現次</th>
          <th>合計</th>
          <th>最近一次考</th>
        </tr>
      </thead>
      <tbody>
""" + "\n".join(x[2] for x in out) + """
      </tbody>
    </table>"""
    s = s[:a] + new_tbl + s[b:]
    print("  ✔ ①總覽表重建（11 列，依合計排序；最近一次考）")
rep("① 副標", '<span class="sub-note">依「選擇題＋申論題」累計出現年次排序</span>',
    '<span class="sub-note">只計「要動手算」的題（選擇題算年數、申論算題數），依合計排序；各年題號見 ③</span>')

# ── ③ 矩陣 ──
MKEY = {"成本法定額折舊": "定額法(等速)", "成本法定率折舊": "定率法(初期加速)", "成本法償債基金": "償債基金法(初期減速)",
        "比較法排除規則": "比較法排除門檻(15%/30%/20%)", "土地開發V公式": "土地開發V公式(含資本利息綜合利率)",
        "資本化率計算": "資本化率計算(§43五種方法)", "WACC計算": "WACC", "債務保障比率法": "債務保障比率法",
        "實質租金計算": "實質租金(押金運用收益)", "樓層別效用比": "樓層別效用比/地價分配率", "DCF折現現金流量": "DCF"}
a = s.find('<table class="matrix-table">')
b = s.find("</table>", a)
seg = s[a:b]
cnt = 0


def mrow(m):
    global cnt
    lab = m.group(1)
    key = MKEY.get(lab)
    if not key:
        fail.append(f"✗ 矩陣列 {lab}")
        return m.group(0)
    ch, es = S(key)
    cells = []
    for y in YEARS:
        c, e = y in ch, y in es
        ids = "、".join(list(ch.get(y, [])) + [x[1:] for x in es.get(y, [])])
        tip = f' title="{ids}"' if ids else ""
        cells.append(f'<td class="cell-b"{tip}>雙</td>' if c and e else f'<td class="cell-c"{tip}>選</td>' if c
                     else f'<td class="cell-e"{tip}>申</td>' if e else '<td class="cell-n">—</td>')
    cnt += 1
    return (f"<tr>\n          <td>{lab}</td>\n          " + "".join(cells[:8]) + "\n          " + "".join(cells[8:]) + "\n        </tr>")


seg2 = re.sub(r"<tr>\s*<td>([^<]+)</td>\s*(?:<td class=\"cell-[a-z]\">[^<]*</td>\s*){16}</tr>", mrow, seg)
if cnt != 11:
    fail.append(f"✗ 矩陣重建列數 {cnt}")
else:
    s = s[:a] + seg2 + s[b:]
    print("  ✔ ③矩陣重建（11 列；格子 title 為題號）")
rep("③ 副標", '<span class="sub-note">選 = 選擇題　申 = 申論題　雙 = 兩者皆考</span>',
    '<span class="sub-note">選 = 選擇題考計算　申 = 申論題考計算　雙 = 兩者皆考；只考公式概念的題不計</span>')

# ── ②⑤ 卡片次數、chips、文字（F 組定位字串） ──
SKIP = set(range(1, 17)) | set(range(44, 55)) | {36, 39, 40}
for num, old, new in FI:
    if num in SKIP or not old:
        continue
    rep(f"F-{num}", old, new)
rep("F-36（定位已被 A 組改過）", "104、111、112、113、114年都考過（111～114 連續四年）",
    "104、106、112、114年考過計算（104-39、106-29、112-18、114-8），111、113年考過公式概念（111-3、113-13）")
rep("F-40（定位已被 A 組改過）", "申論題常附「殘餘價格率10%」，要換算為 s=0.10 代入。",
    "申論題給的「殘餘價格率」（105、112 年都是 5%）要換算為 s＝0.05 代入。")
rep("② 副標", '<span class="sub-note">A級必考 4 大類型</span>', '<span class="sub-note">各卡右上角＝要動手算的出現次數</span>')

if fail:
    print("\n".join(fail))
    sys.exit("\n有項目對不上，全部不寫檔。")
P.write_text(s, encoding="utf-8")
print("寫入完成")
