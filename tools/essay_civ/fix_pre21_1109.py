# -*- coding: utf-8 -*-
"""預21（甲持偽造同意書處分共有物）補「乙、丙得依§184Ⅰ前段向甲請求損害賠償」——題目（二）問乙丙如何救濟，原答案只寫塗銷。
四分頁同步：完整四段式／考場速寫（指揮中心直接改）、考場版（ev_1.json）、邏輯拆解（lj_data.json）。可重跑（已改過則跳過）。
改完依序跑：gen_lj.py → build_ev.py（gen_lj 會拿掉考場版鈕，build_ev 要在後）→ civ_essay_redesign.py → mk_card_viewer.py → sprint/build_sprint.py"""
import io, json, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
F = os.path.join(ROOT, '民法_備考指揮中心.html')
TORT = '甲偽造同意書處分乙、丙之應有部分，係故意不法侵害乙、丙之所有權，乙、丙並得依第184條第1項前段向甲請求損害賠償'
def rep(t, old, new):
    if new in t: return t
    assert t.count(old) == 1, old[:40]; return t.replace(old, new)
s = io.open(F, encoding='utf-8').read()
a = s.find('data-key="預21"'); b = s.find('class="rd" data-key="預21"', a); t = s[a:b]
# 完整四段式：法條⑧、涵攝（二）摘要與內文、結論
t = rep(t, '（第2項並準用第821條）。</p>', '（第2項並準用第821條）。⑧ 第184條第1項前段：因故意或過失，不法侵害他人之權利者，負損害賠償責任。</p>')
t = rep(t, '2. 乙、丙得依第821條、第767條第1項中段請求除去妨害、回復原狀。</span>', '2. 乙、丙得依第821條、第767條第1項中段請求除去妨害、回復原狀，並得依第184條第1項前段向甲請求損害賠償。</span>')
t = rep(t, '結果丁取得甲三分之一之應有部分，與乙、丙成為分別共有人。</p>',
        '結果丁取得甲三分之一之應有部分，與乙、丙成為分別共有人。另偽造之同意書非乙、丙之意思表示，乙、丙亦無以自己行為表示授與代理權之外觀（非第169條之表見代理），不生同意或承認之效力；' + TORT + '。</p>')
t = rep(t, '請求除去妨害，回復原狀。（三）公同共有時，甲之處分整體', '請求除去妨害，回復原狀，並得依第184條第1項前段向甲請求損害賠償。（三）公同共有時，甲之處分整體')
# 考場速寫
t = rep(t, '<mark>§828Ⅲ</mark>公同共有處分全體同意。</p>', '<mark>§828Ⅲ</mark>公同共有處分全體同意；<mark>§184Ⅰ前段</mark>侵權損害賠償。</p>')
t = rep(t, '登記無不實，丁<mark>無信賴基礎</mark>；', '登記無不實，丁<mark>無信賴基礎</mark>；乙丙請求塗銷逾越部分，並得依§184Ⅰ前段向甲<mark>請求賠償</mark>；')
t = rep(t, '2/3無效，丁不得善意取得；公同共有', '2/3無效，丁不得善意取得，乙丙得塗銷並向甲求償；公同共有')
t = rep(t, '<li>公同共有仍套用第819條第1項，漏寫第828條第3項及全部無權處分</li>',
        '<li>公同共有仍套用第819條第1項，漏寫第828條第3項及全部無權處分</li><li>「乙、丙得如何救濟」只寫塗銷，漏寫依第184條第1項前段向甲請求損害賠償</li>')
s = s[:a] + t + s[b:]
io.open(F, 'w', encoding='utf-8').write(s)
# 考場版
p = os.path.join(H, 'exam_ver', 'ev_1.json'); d = json.load(io.open(p, encoding='utf-8')); e = d['預21']
e[1][1] = rep(e[1][1], '第828條第2項、第3項（公同共有之準用與處分）。', '第828條第2項、第3項（公同共有之準用與處分）；第184條第1項前段（侵權行為）。')
e[2][1] = rep(e[2][1], '就逾越甲應有部分之登記回復原狀。理由在於登記正確時無信賴可保護。',
              '就逾越甲應有部分之登記回復原狀；偽造同意書非乙、丙之意思表示，不生同意或承認之效力，甲故意不法侵害乙、丙之所有權，乙、丙並得依第184條第1項前段向甲請求損害賠償。理由在於登記正確時無信賴可保護。')
e[3][1] = rep(e[3][1], '中段請求除去妨害、回復原狀。（三）', '中段請求除去妨害、回復原狀，並得依第184條第1項前段向甲請求損害賠償。（三）')
io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
# 邏輯拆解
p = os.path.join(H, 'lj_data.json'); L = json.load(io.open(p, encoding='utf-8'))
x = [i for i in L if i['k'] == '預21'][0]; sub = x['subs'][1]; st = sub['steps']
if not any('§184' in z.get('lawh', '') for z in st):
    st[1]['link'] = '登記拿回來了，造成的損害找誰？'
    st.append({"ask": "乙丙除了拿回登記，還能向誰請求賠償？", "lawh": "§184Ⅰ前段 侵權行為",
               "law": "因故意或過失，不法侵害他人之權利者，負損害賠償責任。", "facth": "甲偽造同意書",
               "fact": "偽造的同意書不是乙丙的意思表示，乙丙也沒有自己表示授權的行為（不是 §169 表見代理），不生同意或承認效力；甲故意處分乙丙的應有部分，侵害其所有權。",
               "res": "乙丙得向甲請求損害賠償。", "key": "§184Ⅰ前段 → 向甲求償"})
    sub['ans'] = sub['ans'] + '乙丙並得依 §184Ⅰ前段**向甲請求損害賠償**。'
    k = [i for i, c in enumerate(x['checks']) if c['txt'].startswith('乙丙依 §821')][0]
    x['checks'].insert(k + 1, {"t": "ans", "txt": "乙丙依 §184Ⅰ前段向甲請求損害賠償（偽造同意書不生同意效力）", "sub": 2, "hot": True})
    io.open(p, 'w', encoding='utf-8').write(json.dumps(L, ensure_ascii=False, indent=1) + '\n')
print('預21 OK')
