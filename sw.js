const CACHE = 'brokerx-v1';
const FILES = [
  '/',
  '/BrokerX_12週讀書計畫總表.html',
  '/LandLaw_A1A2_quiz.html',
  '/LandLaw_A3A4A5_quiz.html',
  '/LandLaw_B_quiz.html',
  '/LandLaw_C_quiz.html',
  '/LandLaw_D_quiz.html',
  '/LandLaw_E_quiz.html',
  '/LandLaw_FGHI_quiz.html',
  '/不動產估價概要_申論題實戰範文.html',
  '/估價_四大方法比較表.html',
  '/估價_定義填空練習.html',
  '/估價_易混淆概念並排.html',
  '/估價_程序流程記憶圖.html',
  '/估價_考題小卡.html',
  '/估價_計算題攻略.html',
  '/估價_診斷卷一.html',
  '/估價互動單字卡.html',
  '/估價備考指揮中心.html',
  '/估價刷題練習_A1.html',
  '/估價刷題練習_A2.html',
  '/估價刷題練習_A3.html',
  '/估價刷題練習_A4.html',
  '/估價刷題練習_B.html',
  '/估價刷題練習_C1.html',
  '/估價刷題練習_C2.html',
  '/估價刷題練習_D1.html',
  '/估價刷題練習_D2.html',
  '/估價刷題練習_D3.html',
  '/估價刷題練習_E1.html',
  '/估價刷題練習_F1.html',
  '/估價刷題練習_G1.html',
  '/估價刷題練習_H1H2.html',
  '/估價刷題練習_H3I1.html',
  '/估價四大方法系統攻略.html',
  '/估價彩色重點速記.html',
  '/土地法_互動單字卡.html',
  '/土地法_備考指揮中心.html',
  '/土地法_彩色重點速記.html',
  '/土地法_定義填空練習.html',
  '/土地法_罰則總整理.html',
  '/土地法_考題小卡.html',
  '/土地法_讀書攻略與備考指南.html',
  '/土地法互動練習.html',
  '/土地法解析版練習.html',
  '/民法A_互動單字卡.html',
  '/民法A_完整考題小卡.html',
  '/民法A_彩色重點速記.html',
  '/民法A_考題小卡.html',
  '/民法BC_互動單字卡.html',
  '/民法BC_完整考題小卡.html',
  '/民法BC_彩色重點速記.html',
  '/民法BC_考題小卡.html',
  '/民法D_互動單字卡.html',
  '/民法D_完整考題小卡.html',
  '/民法D_彩色重點速記.html',
  '/民法D_考題小卡.html',
  '/民法E_互動單字卡.html',
  '/民法E_完整考題小卡.html',
  '/民法E_彩色重點速記.html',
  '/民法E_考題小卡.html',
  '/民法_備考指揮中心.html',
  '/民法_法律效果總整理.html',
  '/民法_定義填空練習.html',
  '/民法刷題練習_A篇.html',
  '/民法刷題練習_B篇.html',
  '/民法刷題練習_C篇.html',
  '/民法刷題練習_D篇.html',
  '/民法刷題練習_E篇.html',
  '/民法概要_25題模擬測驗.html',
  '/民法申論題_五型答題模板.html',
  '/經紀法規_備考指揮中心.html',
  '/經紀法規_全真模擬卷四.html',
  '/經紀法規_模擬試題一_曾榮耀.html',
  '/經紀法規_混淆對比卷三.html',
  '/經紀法規_罰則總整理.html',
  '/經紀法規_定義填空練習.html',
  '/經紀法規_診斷卷一.html',
  '/經紀法規_讀書攻略與備考指南.html',
  '/經紀法規_高頻考點卷二.html',
  '/經紀法規刷題練習_A1A2A3.html',
  '/經紀法規刷題練習_A4.html',
  '/經紀法規刷題練習_A5.html',
  '/經紀法規刷題練習_E1.html',
  '/經紀法規刷題練習_E3.html',
  '/經紀法規刷題練習_G1_1.html',
  '/經紀法規刷題練習_G1_2.html',
  '/經紀法規刷題練習_G2.html',
  '/經紀法規刷題練習_H1.html',
  '/經紀法規刷題練習_H3_1.html',
  '/經紀法規刷題練習_H3_2.html',
  '/經紀法規刷題練習_其他小章節.html',
  '/經紀法規概要_互動單字卡.html',
  '/經紀法規概要_互動練習.html',
  '/經紀法規概要_彩色重點速記.html',
  '/經紀法規申論題_篇章主題答題模板.html',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
