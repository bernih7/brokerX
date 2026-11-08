# -*- coding: utf-8 -*-
"""民法考題解析結尾「📖 相關工具」連結（比照土地法 bxl-links.js，2026-11-02）。
讀 quiz_data.json（520 題）→ 每題最多 4 個連結 → 產生根目錄 bxm-links.js（勿手改，改這支再重跑）。
順序：①題目資料 mem 欄（人工對應的專區段落，排除「考古題」段）②關鍵字（題幹＋選項）③章別預設（彩色重點速記）。"""
import io, json, os, re
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
Q = json.load(io.open(os.path.join(H, 'quiz_data.json'), encoding='utf-8'))['q']

SA, SB, SD, SE = '民法A_彩色重點速記.html', '民法BC_彩色重點速記.html', '民法D_彩色重點速記.html', '民法E_彩色重點速記.html'
DEBT, COM, MOR = '民法_債之發生與移轉.html', '民法_共有專區.html', '民法_抵押權總整理.html'
NUM, EFF, REAL, INH = '民法_數字期間速查.html', '民法_法律效果總整理.html', '民法_物權變動與登記.html', '民法_繼承專區.html'

CH = {
 'A1': [('彩色速記：A1 自然人', SA + '#sec-a1')], 'A2': [('彩色速記：A2 法人', SA + '#sec-a2')],
 'A3': [('彩色速記：A3 物', SA + '#sec-a3')],
 'A4': [('彩色速記：A4 法律行為效力', SA + '#sec-a4'), ('法律效果：無效・得撤銷・效力未定', EFF + '#vx')],
 'A5': [('彩色速記：A5 意思表示瑕疵', SA + '#sec-a5'), ('法律效果：得撤銷的法律行為', EFF + '#s3')],
 'A6': [('彩色速記：A6 代理', SA + '#sec-a6')],
 'A7': [('彩色速記：A7 消滅時效', SA + '#sec-a7'), ('法律效果：時效與除斥期間', EFF + '#s6')],
 'B1': [('彩色速記：B 債編總則', SB + '#sec-b')], 'B2': [('彩色速記：B 債編總則', SB + '#sec-b')],
 'B3': [('彩色速記：B 債編總則', SB + '#sec-b')],
 'B4': [('債之發生：不當得利', DEBT + '#s2'), ('彩色速記：B 債編總則', SB + '#sec-b')],
 'B5': [('債之發生：無因管理', DEBT + '#s1'), ('彩色速記：B 債編總則', SB + '#sec-b')],
 'B6': [('債之發生：侵權行為要件與賠償', DEBT + '#s3'), ('債之發生：誰要一起賠', DEBT + '#s4')],
 'C1': [('彩色速記：C 各種之債', SB + '#sec-c')], 'C2': [('彩色速記：C 各種之債', SB + '#sec-c')],
 'C3': [('彩色速記：C 各種之債', SB + '#sec-c')], 'C4': [('彩色速記：C 各種之債', SB + '#sec-c')],
 'C5': [('債之發生：債權讓與與債務承擔', DEBT + '#s5')],
 'D1': [('彩色速記：D1 物權通則與所有權', SD + '#sec-d1')],
 'D2': [('彩色速記：D1 物權通則與所有權', SD + '#sec-d1'), ('彩色速記：D2 共有', SD + '#sec-d2')],
 'D3': [('彩色速記：D1 物權通則與所有權', SD + '#sec-d1')],
 'D4': [('彩色速記：D1 物權通則與所有權', SD + '#sec-d1')],
 'D5': [('彩色速記：D3 地上權與農育權', SD + '#sec-d3')],
 'D6': [('抵押權總整理：一筆抵押權的一生', MOR + '#s0'), ('彩色速記：D5 抵押權', SD + '#sec-d5')],
 'E1': [('彩色速記：E2 婚姻', SE + '#sec-e2')], 'E2': [('彩色速記：E5 夫妻財產制', SE + '#sec-e5')],
 'E3': [('彩色速記：E4 父母子女', SE + '#sec-e4')],
 'E4': [('繼承專區：總覽流程圖', INH + '#s0'), ('彩色速記：E6 繼承順序與應繼分', SE + '#sec-e6')],
}
# (regex, (標題, 連結), 限定章別 regex 或 None)
KW = [
 (r'最高限額', ('抵押權總整理：最高限額抵押權', MOR + '#s10'), None),
 (r'法定地上權|併付拍賣', ('抵押權總整理：法定地上權與併付拍賣', MOR + '#s7'), None),
 (r'物上保證', ('抵押權總整理：物上保證人', MOR + '#s8'), None),
 (r'抵押', ('抵押權總整理：一筆抵押權的一生', MOR + '#s0'), None),
 (r'質權|留置權', ('抵押權總整理：質權・留置權簡表', MOR + '#s12'), None),
 (r'分管', ('共有專區：分管約定與對受讓人效力', COM + '#s4'), r'^D'),
 (r'公同共有', ('共有專區：公同共有', COM + '#s6'), r'^[DE]'),
 (r'分割', ('共有專區：分割', COM + '#s5'), r'^D'),
 (r'共有|應有部分', ('共有專區：總覽', COM + '#s0'), r'^D'),
 (r'遺囑|遺贈|見證人', ('繼承專區：遺囑', INH + '#s6'), None),
 (r'特留分|扣減', ('繼承專區：特留分與扣減', INH + '#s7'), None),
 (r'拋棄繼承|拋棄其?繼承', ('繼承專區：拋棄繼承', INH + '#s4'), None),
 (r'代位繼承|再轉繼承|應繼分', ('繼承專區：繼承人順序與應繼分', INH + '#s1'), None),
 (r'剩餘財產', ('繼承專區：夫妻財產與繼承的交界', INH + '#s8'), None),
 (r'繼承', ('繼承專區：總覽流程圖', INH + '#s0'), r'^(D|E2|E4)'),
 (r'借名|通謀虛偽', ('物權變動：通謀虛偽・詐欺撤銷・借名登記', REAL + '#s4'), None),
 (r'一物二賣|二重買賣|先後.{0,4}出賣', ('物權變動：二重買賣與登記', REAL + '#s5'), None),
 (r'善意取得|善意受讓|盜贓|遺失物', ('物權變動：動產交付與善意取得', REAL + '#s3'), r'^[AD]'),
 (r'無權處分', ('物權變動：負擔行為 vs 處分行為', REAL + '#s1'), None),
 (r'時效取得', ('物權變動：時效取得與登記', REAL + '#s6'), None),
 (r'占有人|占有物|善意占有|惡意占有|占有之保護|占有輔助', ('彩色速記：D8 占有', SD + '#sec-d8'), r'^D'),
 (r'混同', ('物權變動：物權消滅（混同・拋棄）', REAL + '#s7'), r'^D'),
 (r'登記', ('物權變動：不動產登記', REAL + '#s2'), r'^D'),
 (r'無因管理', ('債之發生：無因管理', DEBT + '#s1'), None),
 (r'不當得利', ('債之發生：不當得利', DEBT + '#s2'), None),
 (r'連帶.{0,6}(賠償|負責)|僱用人|法定代理人.{0,6}連帶', ('債之發生：侵權行為誰要一起賠', DEBT + '#s4'), None),
 (r'債權讓與|債務承擔', ('債之發生：債權讓與與債務承擔', DEBT + '#s5'), None),
 (r'撤回|解除|終止', ('法律效果：撤回・撤銷・解除・終止', EFF + '#s5'), r'^[ABC]'),
 (r'效力未定', ('法律效果：效力未定', EFF + '#s4'), 'ANS'),
 (r'得撤銷', ('法律效果：得撤銷的法律行為', EFF + '#s3'), 'ANS'),
 (r'無效', ('法律效果：無效的法律行為', EFF + '#s2'), 'ANS'),
 (r'利率|利息', ('數字期間速查', NUM), r'^B'),
 (r'時效|除斥', ('數字期間速查：時效・除斥期間並排', NUM + '#s3'), None),
 (r'離婚', ('彩色速記：E3 離婚', SE + '#sec-e3'), r'^E'),
 (r'收養|婚生|認領|監護', ('彩色速記：E4 父母子女', SE + '#sec-e4'), r'^E'),
]
KW = [(re.compile(a), b, c if c in (None, 'ANS') else re.compile(c)) for a, b, c in KW]

def links(q):
    out, seen = [], set()
    def add(t, u):
        if u not in seen and len(out) < 4: seen.add(u); out.append([t, u])
    for m in q.get('mem') or []:
        page, sid, title, label = m
        if '考古題' in title: continue
        t = re.sub(r'\s*申論(暗線|高頻)?$', '', re.sub(r'\s+', ' ', title).strip()).rstrip('：:')
        add(label + '：' + re.sub(r'^[⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮]\s*', '', t)[:22], page + '.html#' + sid)
    so = q['stem'] + ' '.join(q['opt']); ch = q['ch']
    sa = q['stem'] + ' '.join(q['opt'][ord(a) - 65] for a in q['acc'] if 'A' <= a <= 'D')  # 題幹＋正解選項
    for rx, (t, u), lim in KW:
        if lim == 'ANS':
            if rx.search(sa): add(t, u)
            continue
        if lim and not lim.search(ch): continue
        if rx.search(so): add(t, u)
    for t, u in CH.get(ch, []): add(t, u)
    return out

M = {q['k']: links(q) for q in Q}
assert all(M.values())
for v in M.values():
    for t, u in v: assert os.path.exists(os.path.join(ROOT, u.split('#')[0])), u
JS = '''/* bxm-links.js — 民法考題解析結尾「📖 相關工具」連結（由 tools/civ_quiz/mk_links.py 產生，勿手改）
   BXM_LINKS(題號 '114-1') → [[標題, 連結], …]（最多 4 個）；BXM_LINKS_HTML(題號) → 一列連結膠囊（沒有就回空字串） */
(function () {
  var M = %s;
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function BXM_LINKS(k) { return M[String(k)] || []; }
  function BXM_LINKS_HTML(k) {
    var l = BXM_LINKS(k); if (!l.length) return '';
    return '<div class="bxm-links" style="margin-top:10px;padding-top:8px;border-top:1px dashed rgba(127,127,127,.35)">'
      + '<div style="font-size:12.5px;font-weight:700;opacity:.75;margin-bottom:4px">📖 相關工具（點了另開分頁）</div>'
      + l.map(function (a) {
        return '<a class="bxm-lk" target="_blank" rel="noopener" href="' + esc(a[1]) + '" onclick="event.stopPropagation()">' + esc(a[0]) + ' →</a>';
      }).join('') + '</div>';
  }
  var st = document.createElement('style');
  st.textContent = '.bxm-lk{display:inline-block;margin:2px 6px 4px 0;padding:3px 11px;border:1px solid #B8782E;border-radius:99px;color:#8A5517;background:#FBF1D9;text-decoration:none;font-size:13px;font-weight:700;line-height:1.5}'
    + '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .bxm-lk{background:#3A2C17;color:#F2C98A;border-color:#8A6230}}'
    + ':root[data-theme="dark"] .bxm-lk{background:#3A2C17;color:#F2C98A;border-color:#8A6230}';
  (document.head || document.documentElement).appendChild(st);
  window.BXM_LINKS = BXM_LINKS; window.BXM_LINKS_HTML = BXM_LINKS_HTML;
})();
''' % json.dumps(M, ensure_ascii=False, separators=(',', ':'))
io.open(os.path.join(ROOT, 'bxm-links.js'), 'w', encoding='utf-8').write(JS)
import collections
print('題數', len(M), '連結數分布', collections.Counter(len(v) for v in M.values()))
