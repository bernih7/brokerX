# -*- coding: utf-8 -*-
"""依填空頁 DATA 同步張數：頁首、指揮中心工具卡、bxj-use.js（FILLN＝定義各章、FILLES＝申論四段各章；進度兩列、文字報告兩行）。可重跑。"""
import json, re, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = os.path.join(ROOT, '經紀法規_定義填空練習.html')
f = open(P, encoding='utf-8').read(); i = f.find('const DATA = ') + 13; D, _ = json.JSONDecoder().raw_decode(f[i:])
FN = {c['id']: len(c['cards']) for c in D if c['id'][0] != 'S'}
FS = {c['id']: len(c['cards']) for c in D if c['id'][0] == 'S'}
nf, ns = sum(FN.values()), sum(FS.values())
f = re.sub(r'<div class="sub">[^<]*</div>', '<div class="sub">章節練習＋隨機測驗｜定義 %d 張・申論四段 %d 張</div>' % (nf, ns), f, count=1)
open(P, 'w', encoding='utf-8').write(f)

H = os.path.join(ROOT, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
h2 = re.sub(r'(<b>定義填空練習</b><small>)[^<]*(</small></div><span class="rvb">)[^<]*(</span>)',
            r'\g<1>點空格看答案・隨機測驗・鍵盤操作・申論四段填空\g<2>%d 張＋申論四段 %d\g<3>' % (nf, ns), h, count=1)
assert h2 != h or '申論四段 %d<' % ns in h
open(H, 'w', encoding='utf-8').write(h2)

U = os.path.join(ROOT, 'bxj-use.js'); u = open(U, encoding='utf-8').read()
fn = 'FILLN={' + ','.join('%s:%d' % kv for kv in FN.items()) + '}'
fs = 'FILLES={' + ','.join('%s:%d' % kv for kv in FS.items()) + '}'
u = re.sub(r'FILLN=\{[^}]*\}', fn, u, count=1)
if 'FILLES=' in u: u = re.sub(r'FILLES=\{[^}]*\}', fs, u, count=1)
else: u = u.replace(fn + ',', fn + ',' + fs + ',', 1)
assert 'FILLES=' in u
if 'function fillEsKeys' not in u:
    u = u.replace('function fillTotal(){', 'function fillEsKeys(){var f=ld("bxj-fill",{});return Object.keys(f).filter(function(k){var a=/^(S\\d+)-(\\d+)$/.exec(k);return f[k]&&a&&FILLES[a[1]]!=null&&+a[2]<FILLES[a[1]]})}\nfunction fillEsTotal(){var t=0,c;for(c in FILLES)t+=FILLES[c];return t}\nfunction fillTotal(){', 1)
old_rec = 'L.push("定義填空練習（共 "+fillTotal()+" 張）：已確認 "+fk+" 張"'
if old_rec in u:
    u = u.replace(old_rec, 'L.push("定義填空（選擇題攻略）（共 "+fillTotal()+" 張）：已確認 "+fk+" 張"', 1)
    # 申論四段另起一行
    k = u.find('L.push("定義填空（選擇題攻略）'); e = u.find(');', k) + 2
    u = u[:e] + 'var fe0=fillEsKeys().length;L.push("申論四段填空（申論題攻略）（共 "+fillEsTotal()+" 張）：已確認 "+fe0+" 張");' + u[e:]
old_r3 = 'R3.push(row("經紀法規_定義填空練習","定義填空練習",fk,FT2,'
if old_r3 in u: u = u.replace(old_r3, 'R3.push(row("經紀法規_定義填空練習","定義填空（選擇題攻略）",fk,FT2,', 1)
if '申論四段填空（申論題攻略）",' not in u:
    a = ' G.push({g:"申論",rows:R4});'
    assert u.count(a) == 1
    u = u.replace(a, ' var fe=fillEsKeys().length,FE=fillEsTotal(),rfe=row("經紀法規_定義填空練習","申論四段填空（申論題攻略）",fe,FE,"已完成 "+fe+"／"+FE+" 張（"+pc(fe,FE)+"%）");rfe.url+="#essay";R4.push(rfe);\n' + a, 1)
open(U, 'w', encoding='utf-8').write(u)
print('定義', nf, FN, '申論四段', ns, FS)
