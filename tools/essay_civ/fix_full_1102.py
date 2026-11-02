# 民法申論完整版疑點修正（KB《民法_申論完整版疑點_考場版審稿_20261102》A 類＋判決字號疑誤植）
# 範圍：指揮中心申論卡（各分頁）、lj_data.json（邏輯拆解來源）、exam_ver/ev_*.json（考場版來源）。可重跑。
import io, json, os, glob, re
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..'))
HUB = os.path.join(ROOT, '民法_備考指揮中心.html')
# (卡片key, 舊字串, 新字串)
FIX = [
 # 106-一：第271條是「應各平均分擔」
 ('106-一', '民法採可分之債原則上按比例分擔之立場', '民法採可分之債原則上平均分擔之立場（第271條）'),
 ('106-一', '按比例分別向四人請求', '按平均分擔之部分分別向四人請求'),
 ('106-一', '<strong>可分之債原則上按比例分擔</strong>之立場', '<strong>可分之債原則上平均分擔</strong>之立場（第271條）'),
 ('106-一', '戊<mark>按比例</mark>請求', '戊<mark>按平均分擔部分</mark>請求'),
 ('106-一', '戊按比例請求', '戊按平均分擔部分請求'),
 ('106-一', '借款可分按比例', '借款可分平均分'),
 ('106-一', '§271 按比例各自要', '§271 平均各自要'),
 # 105-二：返還是第767條第1項前段、拆除（除去妨害）是中段
 ('105-二', '第767條第1項中段及第821條但書，請求甲拆除鐵皮屋並將平台返還', '第767條第1項前段、中段及第821條但書，請求甲拆除鐵皮屋並將平台返還'),
 ('105-二', '§767Ⅰ中段、§821但書請求拆除返還', '§767Ⅰ前段・中段、§821但書請求拆除返還'),
 # 114-二：除去用益權的依據是第866條第2項
 ('114-二', '依民法第866條，法院得除去', '依民法第866條第2項，法院得除去'),
 ('114-二', '法院得依第866條除去丙之地上權', '法院得依第866條第2項除去丙之地上權'),
 # 112-一：判決字號與所論條號相同，疑誤植 → 不寫字號
 ('112-一', '（最高法院102年度台上字第425號判決參照）', ''),
 ('112-一', '未占有者則否（最高法院102年度台上字第425號判決）', '未占有者則否（實務見解）'),
 ('112-一', '（最高法院102年度台上字第425號判決）', '（實務見解）'),
 ('112-一', '（最高法院102年度台上字第425號）', ''),
 # 113-二：丙僅遲延，不能逕依第249條第2款；甲得不返還的依據是當事人約定（第249條序文「除當事人另有訂定外」）
 ('113-二', '依第249條第2款甲原則上得不返還之定金', '依約定甲得不返還之定金'),
 ('113-二', '使甲喪失依第249條第2款不返還定金之機會', '使甲喪失依約定不返還定金之機會'),
]
# 預25：法條塊補第226條、第256條（涵攝已用到）
P25 = ('預25', '⑧ 第263條：第258條及第260條之規定，於當事人依法律之規定終止契約者準用之。',
       '⑧ 第263條：第258條及第260條之規定，於當事人依法律之規定終止契約者準用之。⑨ 第226條第1項：因可歸責於債務人之事由，致給付不能者，債權人得請求賠償損害。⑩ 第256條：債權人於有第二百二十六條之情形時，得解除其契約。')
FIX.append(P25)
cnt = {}
def apply_text(t, keyfilter=None):
    for k, a, b in FIX:
        if keyfilter and k != keyfilter: continue
        if a in t and (b == '' or b not in t or a not in b):
            n = t.count(a); t = t.replace(a, b); cnt[(k, a)] = cnt.get((k, a), 0) + n
    return t
# 1) 指揮中心：只在該卡範圍內換
s = io.open(HUB, encoding='utf-8').read()
for key in sorted({k for k, _, _ in FIX}):
    i = s.index('data-key="%s"' % key); j = s.find('<details class="essay', i + 10); j = len(s) if j < 0 else j
    s = s[:i] + apply_text(s[i:j], key) + s[j:]
io.open(HUB, 'w', encoding='utf-8').write(s)
# 2) lj_data.json
p = os.path.join(H, 'lj_data.json'); D = json.load(io.open(p, encoding='utf-8'))
for d in D:
    k = d.get('k')
    if k in {x for x, _, _ in FIX}:
        d2 = json.loads(apply_text(json.dumps(d, ensure_ascii=False), k)); d.clear(); d.update(d2)
io.open(p, 'w', encoding='utf-8').write(json.dumps(D, ensure_ascii=False, indent=1))
# 3) 考場版來源
for f in glob.glob(os.path.join(H, 'exam_ver', 'ev_*.json')):
    E = json.load(io.open(f, encoding='utf-8'))
    for k in list(E):
        E[k] = json.loads(apply_text(json.dumps(E[k], ensure_ascii=False), k))
    io.open(f, 'w', encoding='utf-8').write(json.dumps(E, ensure_ascii=False, indent=1))
for (k, a), n in sorted(cnt.items()): print(k, n, a[:30])
print('total', sum(cnt.values()))
