# 備考｜全科更新日誌 封存（2026-10-31 全科 v607）

> 自主檔原文搬移，未改寫。

## 2026-10-31｜全科 v607：深淺色改為跟隨系統設定（方案 A，四科 90 頁）

起因：v601 的 artifact demo。使用者回「**A　四科 58 頁**」——選方案 A（跟隨系統）、四科一起改。

### 一、⚠️ 範圍比 v601 說的大很多：58 頁 → 90 頁，九種寫法
v601 只掃了「雙引號版的 `setAttribute("data-theme",s||"light")`」，所以報 58 頁。
這次改用 regex 全面掃，同一個 bug 有**九種**寫法：

| 寫法 | 處數 |
|---|---|
| `setAttribute("data-theme",s\|\|"light")` 雙引號 | 58 |
| `setAttribute('data-theme',s\|\|'light')` 單引號 | 27 |
| `setAttribute("data-theme",(s\|\|"light").replace(...))` | 1 |
| `setTh(sv0\|\|"light")` | 11 |
| `setTh(lsG('bx-theme')\|\|'light')` | 14 |
| `setTh(lsG('bx-theme')\|\|lsG('ll_theme')\|\|'light')` | 1 |
| `setT(…:'light')` | 1 |
| 估價113真題自成一套的 `getTheme/applyTheme`（load 時還把 light **寫進 localStorage**） | 3 |
| 切換鈕與按鈕文字 `getAttribute('data-theme')==='dark'` | 67 |

另外兩個**不是 JS**的：
- **估價備考指揮中心在 `<html>` 標籤裡寫死 `data-theme="light"`**（只有這一頁；JS 怎麼改都沒用）。
- **民法_數字期間速查、民法_用詞分類與申論必背**的深色色票只寫在 `[data-theme=dark]`
  （不加引號、不加 `:root`），**完全沒有 prefers-color-scheme media query** → 拿掉屬性會接不到深色、變全白。

最後一類（67 處切換鈕）不會讓畫面壞掉，但**系統深色時第一次按鈕會變成空按**
（它以為現在是 light，於是切到 dark，畫面沒變化）。

### 二、改法
- 開機腳本：**有存過偏好才 `setAttribute`，沒存過就不寫**，交給 `prefers-color-scheme`。
- 切換鈕與按鈕文字：一律改成「有屬性看屬性，沒屬性看系統」
  （`getAttribute('data-theme')||((matchMedia('(prefers-color-scheme:dark)').matches)?'dark':'light')`）。
- 按下切換鈕才寫 `localStorage('bx-theme')`，之後以使用者的選擇為準。**鍵名未改**。
- 那兩頁民法：把既有的 `[data-theme=dark]` 規則**原值鏡像**一份進
  `@media (prefers-color-scheme:dark){:root:not([data-theme=light]) …}`
  （`<style id="sysdark-css">`，**未新增任何顏色值**）。
- 估價備考指揮中心：拿掉 `<html>` 的 `data-theme="light"`。

### 三、範圍
**90 頁：民法 34、經紀法規 32、土地法 19、估價 5。** 站上原本就正常的那 110 頁未動。

### 四、驗證
- **安全前置檢查**（寫檔前）：淺色色票要在裸 `:root`、且頁內要有 prefers-color-scheme
  media query，不符的頁跳過並列出。第一版檢查綁死 `--bg` 變數名，誤判了
  《土地法_彩色重點速記》（那頁用 `--paper`）→ 改成不綁變數名後 0 頁被跳過。
- **全 89 頁 × 系統深色／淺色**：深色底色亮度 <110、淺色 >140、**載入時 0 頁寫 data-theme**、
  0 JS 例外、0 橫向溢出 → 「驗完 89 頁；有問題 0 頁」。
- 17 頁逐一測切換鈕：系統深色下按一次 → 屬性變 light、localStorage 寫入 light、畫面轉淺。
- 90 頁 JS 語法檢查 0 錯；九種寫法殘留掃描 0 筆；兩支腳本可重複執行（第二次跑 0 頁）。
- **rebase 後重驗**（其他科同時改了同一批檔案、git 自動合併）：殘留 0、抽驗 8 頁（四科各 2）全 OK。
- 腳本 `tools/fix_theme_system.py`（第一、二階段）、`tools/fix_theme_stage3.py`；
  另有三頁的寫法 regex 沒抓到、手工改（估價_來勝模擬試題一、民法_定義填空練習、經紀法規_定義填空練習）。
- sw.js 先 pull 再取 origin max+1（origin v606 → **v607**，664f413）。

### 五、⚠️ 其他科同步
1. **這件事已經四科一起做完，不要再各自處理**（v601 原寫「民法 32 頁請民法對話自行處理」，
   使用者後來指示四科一起改，已全部完成）。
2. **「同一個 bug 只掃一種寫法」會嚴重低估範圍**——本輪 58 → 90 頁。
   掃這類問題要用 regex 涵蓋引號、空白、變數名的變體，不要用字面字串比對。
3. **安全前置檢查不要綁特定變數名**（本輪誤判一頁）。各科色票 token 名不同
   （`--bg`／`--paper`／`--cp-card`…），條件要寫成「裸 `:root` 裡有任何 `--xxx:`」。
4. **深色色票只寫在 `[data-theme=dark]` 而沒有 media query 的頁，拿掉屬性就會變全白**。
   四科若還有這種頁（本輪在民法找到 2 頁），作法是把既有規則**原值**鏡像進 media query，不要調色。
5. **本機 `tools/kb*` 鏡像落後了四筆**（土地法 v606、估價 v605／v604、土地法 v602），
   不能拿來當日誌底稿。寫日誌一律 `project_read` 取 KB 版。

