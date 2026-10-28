# 土地法申論頁產生器（2026-10-18）

- `src.html`：申論範文的**唯一原始檔**（舊版標記：details.it、vp data-v=0/1/2、details.full）。要改範文就改這份，再重新產生。
- `data/`：essays.json（題目清單與分組）、M*_out.json（必提重點／結論必寫／最容易漏／引用條文）、F*_law.json（逐字條文全文）、oq.json（考選部原題全文）。
- `python3 gen_full.py` → 產生 `../../土地法_申論題分類總覽.html`（正式頁）。
- 版面樣式 `full.css`、互動 `full.js`。
- 作法說明見知識庫《備考_申論頁標準作法_跨科套用指南_v2》。

- 2026-10-28：`gen_full.py` 重產後，**要再依序跑** `python3 mk_esl_land.py`（申論卡輪數／用時／自評，鍵 `bx-land-es-log`）與 `python3 mk_esrd_land.py`（每卡「📚 這題該讀哪幾頁」），否則這兩塊會被蓋掉。
- 2026-10-28：`gen_pred.py` 目前讀題庫的格式已過期（JSONDecodeError），115 預測頁改用手動維護；要重啟產生器前先修讀檔。
