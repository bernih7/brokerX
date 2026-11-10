# -*- coding: utf-8 -*-
"""施工單《定義填空整套》第六節：統計分開。可重跑。
bxv-use.js：TOT.fill＝定義填空張數（不含 S）、TOT.fillEs＝申論四段張數（兩者由頁面資料計算）；
fillEsDone()；指揮中心「進度」記憶工具一列「定義填空（選擇題攻略）」、申論區一列「申論四段填空（申論題攻略）」（#essay）；文字報告兩行。
指揮中心：申論分頁「先讀什麼・怎麼答・限時寫」加入口；記憶工具清單說明。"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
P = os.path.join(ROOT, '估價_定義填空練習.html'); U = os.path.join(ROOT, 'bxv-use.js'); HUB = os.path.join(ROOT, '估價備考指揮中心.html')
s = open(P, encoding='utf-8').read()
i = s.find('const DATA'); j = s.find('\n];', i)
nfill = len(re.findall(r"\bcid:'", s[i:j]))
m = re.search(r'/\*ES_DATA\*/const ES_DATA = (.*?);/\*/ES_DATA\*/', s, re.S)
nes = sum(len(ch['cards']) for ch in json.loads(m.group(1)))
s = re.sub(r'(id="fillTotal">)\d+', r'\g<1>%d' % nfill, s); s = re.sub(r'(id="fillEsTotal">)\d+', r'\g<1>%d' % nes, s)
s = re.sub(r'(id="fillDone">已完成 0／)\d+', r'\g<1>%d' % nfill, s); s = re.sub(r'(id="fillEsDone">申論四段 0／)\d+', r'\g<1>%d' % nes, s)
open(P, 'w', encoding='utf-8').write(s)

u = open(U, encoding='utf-8').read()
def rep(old, new):
    global u
    if new in u: return
    if u.count(old) != 1: print('（略過，已被他次改版）', old[:40]); return
    u = u.replace(old, new)
u = re.sub(r'TOT=\{fill:\d+,(?:fillEs:\d+,)?', 'TOT={fill:%d,fillEs:%d,' % (nfill, nes), u, count=1)
rep('function fillDone(){var f=ld("bxv-fill",{}),n=0;Object.keys(f).forEach(function(k){if(f[k]&&FILL_RE.test(k))n++});return n}',
    'function fillDone(){var f=ld("bxv-fill",{}),n=0;Object.keys(f).forEach(function(k){if(f[k]&&FILL_RE.test(k))n++});return n}\n/* 申論四段填空（S1～Sn 章，卡號 S章-兩位序號）另計，不算進定義填空 */\nfunction fillEsDone(){var f=ld("bxv-fill",{}),n=0;Object.keys(f).forEach(function(k){if(f[k]&&/^S\\d+-\\d{2}$/.test(k))n++});return n}')
rep(' var fk=fillDone();\n L.push("定義填空練習：已確認 "+fk+" 張"+(fk?"":"（尚無紀錄；此功能 2026-10-13 起才開始記錄）"));',
    ' var fk=fillDone(),fe=fillEsDone();\n L.push("定義填空（選擇題攻略）：已確認 "+fk+"／"+TOT.fill+" 張"+(fk?"":"（尚無紀錄；此功能 2026-10-13 起才開始記錄）"));\n L.push("申論四段填空（申論題攻略）：已確認 "+fe+"／"+TOT.fillEs+" 張");')
rep('R4.push(row("估價_定義填空練習","定義填空練習",fd,ft,',
    'R4.push(row("估價_定義填空練習","定義填空（選擇題攻略）",fd,ft,')
rep('G.push({g:"申論",rows:[row("不動產估價概要_申論題實戰範文","申論題實戰範文",en,TOT.essay,"已讀 "+en+"／"+TOT.essay+" 題（官方 32＋本站模擬 7＋補習班模擬 2＋預測 22）")]});',
    'var fe2=Math.min(fillEsDone(),TOT.fillEs),rfe=row("估價_定義填空練習","申論四段填空（申論題攻略）",fe2,TOT.fillEs,"已完成 "+fe2+"／"+TOT.fillEs+" 張");rfe.url+="#essay";rfe.read=null;rfe.open=null;\n G.push({g:"申論",rows:[row("不動產估價概要_申論題實戰範文","申論題實戰範文",en,TOT.essay,"已讀 "+en+"／"+TOT.essay+" 題（官方 32＋本站模擬 7＋補習班模擬 2＋預測 22）"),rfe]});')
# 申論「已讀」原本只認 e／pred 卡號，漏算本站模擬卷與補習班卷（mk-）
rep('if(/^(e\\d+-[12]|pred-\\d+)$/.test(id))en++', 'if(/^(e\\d+-[12]|pred-\\d+|mk-[a-z0-9-]+)$/.test(id))en++')
rep('fillDone:fillDone,countQ', 'fillDone:fillDone,fillEsDone:fillEsDone,countQ')
# FILL_RE 依頁面定義章代碼重寫（新增章節時自動涵蓋）
chs = re.findall(r"id:'([A-Z][A-Z0-9]*)', label:", s[i:j])
u = re.sub(r'var FILL_RE=/\^\([^)]*\)-\\d\{2\}\$/;', lambda m: 'var FILL_RE=/^(%s)-\\d{2}$/;' % '|'.join(chs), u, count=1)
open(U, 'w', encoding='utf-8').write(u)

h = open(HUB, encoding='utf-8').read()
A = ('<a class="sp-a" href="%E4%BC%B0%E5%83%B9_%E5%AE%9A%E7%BE%A9%E5%A1%AB%E7%A9%BA%E7%B7%B4%E7%BF%92.html#essay"><span class="sp-n"><b>📝 申論四段填空</b>'
     '<small>官方 32 題依相似題型合併成卡：問題定義→法條定義→問題核心→結論＋卓見，空格一格一格翻，一題一題隨機</small></span><span class="sp-g">填空練 ▸</span></a>')
if 'sp-a" href="%E4%BC%B0%E5%83%B9_%E5%AE%9A%E7%BE%A9%E5%A1%AB%E7%A9%BA%E7%B7%B4%E7%BF%92.html#essay"' not in h:
    k = h.find('  </div><!--/drill-box-->'); assert k > 0
    h = h[:k] + '    ' + A + '\n' + h[k:]
h = h.replace('<span class="tl-nm">定義填空練習</span><span class="tl-ds">A1–I 所有章節</span>', '<span class="tl-nm">定義填空練習</span><span class="tl-ds">A1–I 所有章節＋申論四段（另一分類）</span>')
open(HUB, 'w', encoding='utf-8').write(h)
print('定義', nfill, '申論四段', nes)
