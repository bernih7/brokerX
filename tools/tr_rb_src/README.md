# 任務：把《估價_技術規則專欄》第 N 篇改成「B 版型：左條文・右怎麼記」

使用者看過 demo 選了 B 版型。第一篇（t1 總則與程序）我已做好，**完全照它的寫法**：
- 範例片段：`t1.html`（同目錄）；CSS：`rb.css`（不要改，有需要的新 class 先問——基本上不需要）。
- 原頁：/home/claude/brokerx/估價_技術規則專欄.html。每篇是 `<details class="tp" id="tN">…<div class="tp-b">（內容）</div></details>`。你只產出 `tN.html` = 新的 tp-b 內層 HTML。
- 預覽：`cd /home/claude/brokerx && python3 tools/tr_rb_assemble.py <本資料夾> --out _tr_preview_tN.html`（N 換成你的篇號，避免和別人互蓋），再開 http://localhost:8777/_tr_preview_tN.html#tN（伺服器若沒開：`(python3 -m http.server 8777 >/dev/null 2>&1 &)`）。

## 版型（每一列）
```
<section class="rb"><div class="rb-l"><h2><span class="law">§N</span>標題<span class="tag v">逐字核對</span></h2>
  <ol class="ln">…每款一個 <li><span class="n">一</span><span>…</span></li>…</ol>   ← 款／項／步驟「一款一行」
  （名詞＋定義用 <ol class="ln kv">，左格放名詞）（分組用 <div class="grp">）（補充一句用 <p class="tail">）
  （原頁的圖 .kf／SVG／表格：原封不動放在 rb-l 裡）
</div><div class="rb-r"><div class="lbl">怎麼記</div><div class="mn">口訣</div><div class="mn-src">口訣・來源頁</div>
  <div class="lbl">陷阱</div><ul class="tx"><li>…正確寫法用 <span class="ok">…</span>，錯的寫法用 <s>…</s>（題號）</li></ul>
  <div class="lbl">考古</div><div class="qs"><a class="qlk" href="估價_考題小卡.html#ID">年-題</a>…</div>
</div></section>
```
- 標籤沿用原頁：`<span class="tag v">逐字核對</span>`、`tag z`（整理）、`tag e`（考古）——照原頁該段原本的標籤。
- **算例、計算步驟**（原頁的「兩個一定會算的」「算例」）：放進相關條文那一列的 rb-l（保留原本 .kf 公式卡），或獨立一列 h2 用「算例」，右欄寫口訣／陷阱。

## 硬規則
1. **原頁該篇的每一個事實、數字、條號、圖、表、題號連結都要保留**（可以搬位置、可以拆行，不可以刪）。做完寫 `tN_map.md`：原頁每一段（h2 與每個 li／kf-step／p）→ 新的哪一列，逐條列出。
2. 條文內容以逐字檔為準：/tmp/claude-0/-home-claude/ac4bbd9f-3aea-5322-85d9-48ab97ee8f14/scratchpad/law/估價_技術規則_全文逐字_§1-§133_20261022.md（及同資料夾其他逐字檔）。標「逐字核對」的列，條文句子要盡量用逐字（可省略不重要的字，但不得改意思、不得改用字）。原頁若與逐字不符，以逐字為準並在 map 檔註明「原頁寫錯：…」。
3. **一款一行**：凡是條文有一、二、三款或 ①②③ 的，都拆成 ol.ln 每款一行；不得再把多款塞在同一句。
4. 原頁「考試陷阱」那一節要**拆散**，每一條搬到最相關的那一列右欄「陷阱」；真的無處歸的放最後一列。
5. 口訣只能從 `MN.md` 挑（照標的來源頁寫 mn-src），或依 MN.md 最後一段的規則自編。**MN.md 前五項是全站統一版，一定用那個版本**。
6. 題號連結：沿用原頁的 `a.qlk` href；新加的題號連結要先確認 ID 存在：`grep -c '"VXX_年_題"' /home/claude/brokerx/估價_考題小卡.html`。不確定題號是否考這條就不要加。
7. 不要用 <b> 以外的新強調樣式；<mark> 只標關鍵字（每行 1～2 個）。不要用紅色大底。
8. 不要改原頁、不要改 rb.css、不要 git commit；只寫 tN.html 與 tN_map.md。
9. 驗收：預覽 390 寬（淺色、深色）與 1100 寬各截圖自己看過；`node /home/claude/brokerx/tools/theme/contrast_scan.js dark /tmp/x_tN.json _tr_preview_tN` 該篇無新增問題；回報 map 摘要與「原頁寫錯」清單。
