# -*- coding: utf-8 -*-
"""《民法_備考指揮中心》申論卡加「📚 這題該讀哪幾頁」（施工單第 6 項，對應估價 v529）。

依每張卡的主題標籤（summary 的 .ec，例如「D共有／抵押權」）套關鍵詞規則，每張最多 3 個連結，
同一頁只留最具體的那一節。規則為 2026-10-27 使用者確認版；101-一 標籤「B+D+E」手動指定。
執行時檢查每個連結的檔案與錨點都存在。可重複執行（以 <style id="esrd-css">～<script id="esrd-js"> 為邊界）。
"""
import io, os, re, json, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '民法_備考指揮中心.html')

P = {'inh': '民法_繼承專區', 'co': '民法_共有專區', 'mg': '民法_抵押權總整理', 'ch': '民法_物權變動與登記',
     'A': '民法A_彩色重點速記', 'BC': '民法BC_彩色重點速記', 'D': '民法D_彩色重點速記', 'E': '民法E_彩色重點速記',
     'num': '民法_數字期間速查', 'eff': '民法_法律效果總整理', 'debt': '民法_債之發生與移轉'}
# (關鍵詞, 頁, 錨點, 顯示名) —— 由具體到一般排列，先命中者優先
RULES = [
 ('婚約', 'E', 'sec-e2', 'E 速記・婚姻'),
 ('遺失物', 'D', 'sec-d1', 'D 速記・物權通則與所有權'),
 ('僱用人', 'debt', 's4', '債之發生與移轉 ④ 誰要一起賠'),
 ('侵權', 'debt', 's3', '債之發生與移轉 ③ 侵權要件與範圍'),
 ('無因管理', 'debt', 's1', '債之發生與移轉 ① 無因管理'),
 ('撤銷權', 'BC', 'sec-b', 'BC 速記・債編總則'),
 ('法人', 'A', 'sec-a2', 'A 速記・法人'),
 ('從物', 'A', 'sec-a3', 'A 速記・物'),
 ('贈與', 'BC', 'sec-c', 'BC 速記・債編各論'),
 ('繼承', 'inh', '', '繼承專區'),
 ('夫妻財產', 'E', 'sec-e5', 'E 速記・夫妻財產制'),
 ('最高限額', 'mg', 's10', '抵押權總整理 ⑩ 最高限額'),
 ('物權優先', 'mg', 's11', '抵押權總整理 ⑪ 物權優先順序'),
 ('抵押', 'mg', '', '抵押權總整理'),
 ('區分所有', 'co', 's4', '共有專區 ④ 分管與 §799-1'),
 ('共有', 'co', '', '共有專區'),
 ('善意取得', 'ch', 's3', '物權變動與登記 ③ 善意取得'),
 ('無權處分', 'ch', 's1', '物權變動與登記 ① 無權處分'),
 ('不動產登記', 'ch', 's2', '物權變動與登記 ② 登記'),
 ('取得時效', 'ch', 's6', '物權變動與登記 ⑥ 時效取得'),
 ('時效', 'num', 's4', '數字期間速查 ④ 時效・除斥期間'),
 ('相鄰', 'D', 'sec-d1', 'D 速記・物權通則與所有權'),
 ('地上權', 'D', 'sec-d3', 'D 速記・地上權與農育權'),
 ('用益物權', 'D', 'sec-d3', 'D 速記・地上權與農育權'),
 ('典權', 'D', 'sec-d7', 'D 速記・典權'),
 ('占有', 'D', 'sec-d8', 'D 速記・占有'),
 ('居間', 'BC', 'sec-c', 'BC 速記・委任／居間／承攬'),
 ('委任', 'BC', 'sec-c', 'BC 速記・委任／居間／承攬'),
 ('買賣', 'BC', 'sec-c', 'BC 速記・買賣'),
 ('瑕疵擔保', 'BC', 'sec-c', 'BC 速記・買賣（瑕疵擔保）'),
 ('租賃', 'BC', 'sec-c', 'BC 速記・租賃'),
 ('契約成立', 'BC', 'sec-b', 'BC 速記・契約之成立'),
 ('代位', 'BC', 'sec-b', 'BC 速記・債編總則'),
 ('多數債務人', 'BC', 'sec-b', 'BC 速記・債編總則'),
 ('債', 'BC', 'sec-b', 'BC 速記・債編總則'),
 ('代理', 'A', 'sec-a6', 'A 速記・代理'),
 ('行為能力', 'A', 'sec-a1', 'A 速記・自然人（行為能力）'),
 ('意思表示', 'A', 'sec-a5', 'A 速記・意思表示瑕疵'),
 ('法律行為', 'eff', 's1', '法律效果總整理 ① 三態總覽'),
 ('A總則', 'A', '', 'A 速記・民法總則'),
 ('物權', 'ch', '', '物權變動與登記'),
 ('所有權', 'D', 'sec-d1', 'D 速記・物權通則與所有權'),
]
MANUAL = {'101-一': [('inh', 's4', '繼承專區 ④ 拋棄繼承'), ('mg', 's9', '抵押權總整理 ⑨ 消滅（拋棄）')]}

s = io.open(HUB, encoding='utf-8').read()
E = re.findall(r'<details class="essay[^"]*"[^>]*data-key="([^"]+)"[^>]*><summary>.*?<span class="ec">([^<]*)</span>', s)
MAP = {}
for k, ec in E:
    if k in MANUAL:
        hit = MANUAL[k]
    else:
        hit, pages = [], set()
        for kw, pg, an, nm in RULES:
            if kw in ec and pg not in pages:
                hit.append((pg, an, nm)); pages.add(pg)
        hit = hit[:3]
    assert hit, (k, ec)
    MAP[k] = [[urllib.parse.quote(P[pg] + '.html') + ('#' + an if an else ''), nm] for pg, an, nm in hit]
# 檢查連結
for k, L in MAP.items():
    for u, nm in L:
        f, _, a = urllib.parse.unquote(u).partition('#')
        txt = io.open(os.path.join(ROOT, f), encoding='utf-8').read()
        assert not a or ('id="%s"' % a) in txt, (k, u)

BLOCK = '''<style id="esrd-css">
.esrd{margin:8px 0 4px;padding:8px 11px;border-radius:10px;background:var(--pri-soft);font-size:.8rem;line-height:1.7}
.esrd b{color:var(--pri);margin-right:4px}
.esrd a{display:inline-block;margin:2px 6px 2px 0;padding:2px 9px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);text-decoration:none;font-weight:700;font-size:.76rem}
</style>
<script id="esrd-js">
/* 申論卡「📚 這題該讀哪幾頁」：依主題標籤配對的整理頁（產生器 tools/civ_quiz/mk_esrd.py） */
(function(){var M=__MAP__;
[].forEach.call(document.querySelectorAll('details.essay'),function(e){var L=M[e.dataset.key],b=e.querySelector('.ebody');if(!L||!b||b.querySelector('.esrd'))return;
 var d=document.createElement('div');d.className='esrd';d.innerHTML='<b>📚 這題該讀哪幾頁</b>'+L.map(function(x){return '<a href="'+x[0]+'" target="_blank" rel="noopener">'+x[1]+' ▸</a>'}).join('');
 var oq=b.querySelector('.oq');if(oq&&oq.nextSibling)b.insertBefore(d,oq.nextSibling);else b.insertBefore(d,b.firstChild)});
})();
</script>'''.replace('__MAP__', json.dumps(MAP, ensure_ascii=False, separators=(',', ':')))

if 'id="esrd-css"' in s:
    a = s.index('<style id="esrd-css">'); b = s.index('</script>', s.index('<script id="esrd-js">')) + len('</script>')
    s = s[:a] + BLOCK + s[b:]
else:
    i = s.rindex('</body>'); s = s[:i] + BLOCK + s[i:]
io.open(HUB, 'w', encoding='utf-8').write(s)
n = sum(len(v) for v in MAP.values()); u = len({x[0] for v in MAP.values() for x in v})
print('申論卡 %d 張、連結 %d 個（不重複 %d）全部存在' % (len(MAP), n, u))
