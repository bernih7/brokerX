/* bxv-links.js — 估價考題解析結尾的「相關工具」連結（16 支刷題章節頁、113 真題頁、整理頁考古題面板共用；比照土地法 bxl-links.js）
   BXV_LINKS(章別, 題幹＋選項, 題幹＋選項＋解析) → [[標題, 連結], …]（最多 4 個）
     章別可給章節代碼（A1…I2J1）或子分類（B1 B2 H1 H2 H3 I1 I2 J1）。
   BXV_LINKS_HTML(同上) → 一列連結膠囊的 HTML（沒有就回空字串；連到「目前這一頁」的會略過）
   所有檔名與錨點 id 都經 tools/quiz_val/add_links.py 的 check_links() 逐一核對過存在。 */
(function () {
  var CS = '估價彩色重點速記.html', CC = '估價_計算題攻略.html', MIX = '估價_易混淆概念並排.html',
    TR = '估價_技術規則專欄.html', PR = '估價_估價程序總整理.html', SP = '估價_特殊標的總整理.html',
    RT = '估價_租金估計攻略表.html', BU = '估價_營造施工費四法.html', LV = '估價_地價調查估計規則專欄.html',
    M4 = '估價_四大方法比較表.html', SYS = '估價四大方法系統攻略.html',
    DEV = '估價_土開計算題組.html', DCF = '估價_DCF計算題組.html', SPL = '估價_房地拆價計算題組.html';

  /* 章別預設（子分類優先，查不到再用章節代碼） */
  var CH = {
    A1: [['彩色速記：A1 估價原則', CS + '#sec-a1'], ['技術規則專欄：總則與程序', TR + '#t1']],
    A2: [['彩色速記：A2 價格種類', CS + '#sec-a2'], ['易混淆：正常／限定／特定／特殊價格', MIX + '#price']],
    A3: [['彩色速記：A3 影響因素', CS + '#sec-a3'], ['易混淆：近鄰地區／類似地區／同一供需圈', MIX + '#area']],
    A4: [['估價程序總整理：八步驟一表背完', PR + '#cheat'], ['彩色速記：A4 估價程序', CS + '#sec-a4']],
    B1: [['彩色速記：B 比較法', CS + '#sec-b'], ['計算題攻略：比較法四項調整', CC + '#cc-adj'], ['易混淆：15%／30%／20% 排除關卡', MIX + '#rules']],
    B2: [['計算題攻略：數筆土地合併分算', CC + '#cc-merge'], ['彩色速記：B 比較法', CS + '#sec-b']],
    C1: [['營造施工費四法', BU + '#s1'], ['易混淆：重建成本 vs 重置成本', MIX + '#rebuild'], ['彩色速記：C 成本法', CS + '#sec-c']],
    C2: [['計算題攻略：折舊三法', CC + '#cc-dep'], ['易混淆：三種折舊方法並排', MIX + '#depreciation'], ['彩色速記：C 成本法', CS + '#sec-c']],
    D1: [['計算題攻略：直接資本化法', CC + '#cc-direct'], ['彩色速記：D 收益法', CS + '#sec-d'], ['四大方法系統攻略：收益法', SYS + '#tab-income']],
    D2: [['計算題攻略：五種資本化率決定方法', CC + '#cc-cap'], ['易混淆：五種資本化率方法並排', MIX + '#caprate']],
    D3: [['易混淆：直接資本化法 vs DCF', MIX + '#dcf-vs-direct'], ['DCF 計算題組', DCF], ['四大方法系統攻略：證券化 DCF 特別規定', SYS + '#sec-dcf']],
    E1: [['計算題攻略：土地開發 V 公式', CC + '#cc-dev'], ['彩色速記：E 土地開發分析法', CS + '#sec-e'], ['技術規則專欄：土地開發分析法', TR + '#t5']],
    F1: [['租金估計攻略表', RT], ['計算題攻略：實質租金計算', CC + '#cc-rent'], ['易混淆：租金種類並排', MIX + '#rent']],
    G1: [['彩色速記：H 房地估價（樓層別效用比）', CS + '#sec-h'], ['計算題攻略：樓層別效用比計算', CC + '#cc-floor'], ['特殊標的總整理：房地估價', SP + '#s3']],
    H1: [['特殊標的總整理：權利估價', SP + '#s5'], ['彩色速記：J 權利估價', CS + '#sec-j']],
    H2: [['特殊標的總整理：特殊宗地', SP + '#s2'], ['彩色速記：G 宗地估價', CS + '#sec-g']],
    H3: [['彩色速記：K 都市更新權利變換', CS + '#sec-k'], ['特殊標的總整理：都更基地權利價值', SP + '#s5b'], ['計算題攻略：權利變換分配', CC + '#cc-urban']],
    I1: [['彩色速記：B 比較法（含 CAMA）', CS + '#sec-b'], ['技術規則專欄：比較法（含 CAMA §19-20）', TR + '#t2']],
    I2: [['特殊標的總整理：土地改良物', SP + '#s4'], ['彩色速記：I 土地改良物估價', CS + '#sec-i']],
    J1: [['特殊標的總整理：宗地通則', SP + '#s1'], ['彩色速記：G 宗地估價', CS + '#sec-g']]
  };
  CH.B = CH.B1;
  CH.H1H2 = [CH.H2[0], CH.H1[0], CH.H2[1]];
  CH.H3I1 = [CH.H3[0], CH.I1[0], CH.H3[1]];
  CH.I2J1 = [CH.I2[0], CH.J1[0], CH.I2[1]];

  /* 關鍵字（先比題幹＋選項；第 3 欄 1＝也比解析；第 4 欄＝限定章別代碼開頭） */
  var KW = [
    [/定率法/, ['計算題攻略：定率法折舊', CC + '#cc-dep2']],
    [/償債基金/, ['計算題攻略：償債基金法折舊', CC + '#cc-dep3']],
    [/定額法|殘餘價格|殘價率/, ['計算題攻略：定額法・殘餘價格', CC + '#cc-dep1']],
    [/折舊提存/, ['計算題攻略：收益法折舊提存費', CC + '#dep-inc']],
    [/折舊|耐用年數/, ['計算題攻略：折舊三法', CC + '#cc-dep']],
    [/耐用年數/, ['易混淆：物理 vs 經濟耐用年數', MIX + '#useful-life']],
    [/重建成本|重置成本/, ['易混淆：重建成本 vs 重置成本', MIX + '#rebuild']],
    [/營造施工費|淨計法|單位(面積|體積)法|工程造價比較法|單位工程/, ['營造施工費四法', BU + '#s1']],
    [/規劃設計費|廣告費|銷售費|管理費/, ['易混淆：成本法費用的計算基礎', MIX + '#cost-type'], 0, /^[CE]/],
    [/樓層別效用比|區分所有|樓層效用|地價分配率/, ['彩色速記：H 房地估價（樓層別效用比）', CS + '#sec-h']],
    [/樓層別效用比|樓層效用/, ['計算題攻略：樓層別效用比計算', CC + '#cc-floor']],
    [/建物價值比率|房地總價|拆算|拆分/, ['計算題攻略：房地總價拆土地單價', CC + '#split-card']],
    [/建物價值比率|房地總價/, ['房地拆價計算題組', SPL]],
    [/權利變換|都市更新|更新後/, ['彩色速記：K 都市更新權利變換', CS + '#sec-k']],
    [/權利變換|權利價值比率/, ['計算題攻略：權利變換分配', CC + '#cc-urban']],
    [/實質租金|支付租金/, ['計算題攻略：實質租金計算', CC + '#cc-rent']],
    [/續訂|新訂/, ['易混淆：新訂 vs 續訂租約', MIX + '#rentmethod'], 0, /^F/],
    [/續訂|經濟租金/, ['計算題攻略：續訂租金差額分配', CC + '#cc-renew'], 0, /^F/],
    [/租金/, ['租金估計攻略表', RT]],
    [/土地開發分析|開發分析|開發.{0,4}(利潤率|資本利息)/, ['計算題攻略：土地開發 V 公式', CC + '#cc-dev']],
    [/土地開發分析|開發分析/, ['土地開發計算題組', DEV]],
    [/風險溢酬|債務保障比率|貸款常數|有效總收入乘數|市場萃取|加權平均資金成本|資本化率/, ['易混淆：五種資本化率方法並排', MIX + '#caprate']],
    [/資本化率|收益資本化|還原利率|收益價格/, ['計算題攻略：直接資本化・資本化率', CC + '#cc-cap']],
    [/折現現金流量|DCF|折現率|期末價值|期末處分/, ['易混淆：直接資本化法 vs DCF', MIX + '#dcf-vs-direct']],
    [/折現現金流量|DCF/, ['DCF 計算題組', DCF]],
    [/證券化/, ['四大方法系統攻略：證券化 DCF 特別規定', SYS + '#sec-dcf']],
    [/殘餘法|土地殘餘|建物殘餘/, ['計算題攻略：殘餘法', CC + '#cc-resid']],
    [/年金|複利現價|複利終價/, ['計算題攻略：年金現值', CC + '#annuity-card']],
    [/總費用|有效總收入|空置|淨收益/, ['四大方法系統攻略：總費用應計入 vs 不應計入', SYS + '#sec-fee'], 0, /^D/],
    [/調整率|試算價格|排除/, ['易混淆：15%／30%／20% 排除關卡', MIX + '#rules'], 0, /^[AB]/],
    [/情況調整|價格日期調整|區域因素調整|個別因素調整/, ['易混淆：比較法調整四順序', MIX + '#adjust']],
    [/近鄰地區|類似地區|同一供需圈/, ['易混淆：近鄰地區／類似地區／同一供需圈', MIX + '#area']],
    [/正常價格|限定價格|特定價格|特殊價格/, ['易混淆：正常／限定／特定／特殊價格', MIX + '#price']],
    [/價格日期|勘察日期/, ['易混淆：價格日期／勘察日期', MIX + '#dates']],
    [/估價報告書/, ['估價程序總整理：⑧ 製作估價報告書', PR + '#s8']],
    [/估價計畫/, ['估價程序總整理：② 擬定估價計畫', PR + '#s2']],
    [/基本事項/, ['估價程序總整理：① 確定估價基本事項', PR + '#s1']],
    [/勘估標的狀態|確認勘估/, ['估價程序總整理：④ 確認勘估標的狀態', PR + '#s4']],
    [/估價方法.{0,6}(兩|二|2)種|兼採/, ['估價程序總整理：⑥ 運用估價方法', PR + '#s6']],
    [/地價區段|區段地價|宗地單位地價|地價調查/, ['地價調查估計規則專欄', LV + '#s1']],
    [/徵收.{0,4}(補償|市價)|市價查估/, ['地價調查估計規則專欄：徵收補償市價查估', LV + '#s9']],
    [/計量模型|CAMA|自變數|判定係數/, ['彩色速記：B 比較法（含 CAMA）', CS + '#sec-b']],
    [/以素地|素地為前提|建物影響/, ['易混淆：素地 vs 考慮建物影響', MIX + '#bareland']],
    [/合併|分割/, ['計算題攻略：數筆土地合併分算', CC + '#cc-merge'], 0, /^[BGHJ]/],
    [/污染/, ['計算題攻略：受污染土地減損', CC + '#cc-pollute']],
    [/地上權|典權|地役|不動產役權|租賃權|容積移轉|區分地上權/, ['特殊標的總整理：權利估價', SP + '#s5']],
    [/土地改良物|農作改良物|工事改良物/, ['特殊標的總整理：土地改良物', SP + '#s4']],
    [/公共設施保留地|畸零地|袋地|溫泉|墓地|林地|農作|高爾夫|海埔|鹽田|祭祀/, ['特殊標的總整理：特殊宗地', SP + '#s2'], 0, /^[GHIJ]/]
  ];

  function BXV_LINKS(ch, so, all) {
    ch = String(ch || ''); so = String(so || ''); all = String(all || so);
    var out = [], seen = {}, kw = [];
    KW.forEach(function (r) {
      if (r[3] && !r[3].test(ch)) return;
      if (r[0].test(r[2] ? all : so) && !seen[r[1][1]]) { seen[r[1][1]] = 1; kw.push(r[1]); }
    });
    /* 關鍵字最多 3 個，保留至少 1 格給章別預設 */
    out = kw.slice(0, 3);
    var def = CH[ch] || CH[ch.slice(0, 2)] || CH[ch.charAt(0)] || [];
    def.forEach(function (a) { if (!out.some(function (b) { return b[1] === a[1]; })) out.push(a); });
    kw.slice(3).forEach(function (a) { out.push(a); });
    return out.slice(0, 4);
  }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function here() { try { return decodeURIComponent(location.pathname.split('/').pop() || ''); } catch (e) { return ''; } }
  function css() {
    if (document.getElementById('bxv-links-css')) return;
    var s = document.createElement('style'); s.id = 'bxv-links-css';
    var dk = '.bxv-links a{background:rgba(184,120,46,.16)!important;color:#E9C48C!important;border-color:#C08A45!important}';
    s.textContent = '.bxv-links{margin-top:10px;padding-top:8px;border-top:1px dashed rgba(127,127,127,.35)}'
      + '.bxv-links .bxv-lt{font-size:12.5px;font-weight:700;opacity:.75;margin-bottom:4px}'
      + '.bxv-links a{display:inline-block;margin:2px 6px 4px 0;padding:3px 11px;border:1px solid #B8782E;border-radius:99px;color:#8A5517;background:#FBF1D9;text-decoration:none;font-size:13px;font-weight:700;line-height:1.5}'
      + '.bxv-links a:hover{text-decoration:underline}'
      + '@media(prefers-color-scheme:dark){:root:not([data-theme="light"]) ' + dk + '}'
      + ':root[data-theme="dark"] ' + dk;
    (document.head || document.documentElement).appendChild(s);
  }
  function BXV_LINKS_HTML(ch, so, all) {
    var me = here();
    var l = BXV_LINKS(ch, so, all).filter(function (a) { return !me || a[1].split('#')[0] !== me; });
    if (!l.length) return '';
    css();
    return '<div class="bxv-links"><div class="bxv-lt">📖 相關工具（點了另開分頁）</div>'
      + l.map(function (a) {
        return '<a target="_blank" rel="noopener" href="' + esc(a[1]) + '" onclick="event.stopPropagation()">' + esc(a[0]) + ' →</a>';
      }).join('') + '</div>';
  }
  window.BXV_LINKS = BXV_LINKS; window.BXV_LINKS_HTML = BXV_LINKS_HTML;
})();
