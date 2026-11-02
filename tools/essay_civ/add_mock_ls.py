# -*- coding: utf-8 -*-
"""民法《來勝115模擬試題（一）》申論 2 題收進指揮中心申論分頁（v3 第八節／經紀法規 v455 作法）。
- 卡片 data-key「來勝-一」（g3 無權處分・登記）、「來勝-二」（g1 共有）；class 加 pred mock（虛線框）、data-lv="M"。
- 完整四段式＝《民法_來勝模擬試題一》本站擬答原文（parts／warn），考場速寫＝ls_mock.json，邏輯拆解＝lj_mock_ls.json（併入 lj_data.json），
  考場版＝exam_ver/ev_6.json（之後跑 build_ev.py 注入）。老師版留在模擬卷頁，卡片內附連結。
- 同時調整：申論篩選加「補習班」、各組標題與已讀計數把補習班與預測分開算、bxm-use.js 申論總數、gen_lj.py 卡數。
可重跑（先移除舊的兩張卡再插入）。"""
import io, json, os, re, html
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
HUB = os.path.join(R, '民法_備考指揮中心.html'); LS = os.path.join(R, '民法_來勝模擬試題一.html')
E = html.escape
s = io.open(HUB, encoding='utf-8').read()
src = io.open(LS, encoding='utf-8').read()
DATA = json.JSONDecoder().raw_decode(src[src.index('var D=') + 6:])[0]['E']
META = json.load(io.open(os.path.join(H, 'ls_mock.json'), encoding='utf-8'))
LJ = json.load(io.open(os.path.join(H, 'lj_mock_ls.json'), encoding='utf-8'))
LAW = json.load(io.open(os.path.join(R, 'tools', 'civ_quiz', 'law.json'), encoding='utf-8'))
CIRC = dict(zip('ⅠⅡⅢⅣⅤⅥⅦ', '①②③④⑤⑥⑦'))

# lj_data.json 併入
LJF = os.path.join(H, 'lj_data.json'); LD = json.load(io.open(LJF, encoding='utf-8'))
LD = [x for x in LD if x['k'] not in {y['k'] for y in LJ}] + LJ
io.open(LJF, 'w', encoding='utf-8').write(json.dumps(LD, ensure_ascii=False, indent=1))
gl = io.open(os.path.join(H, 'gen_lj.py'), encoding='utf-8').read()
ns = {'re': re, 'html': html, 'E': E}
exec(gl[gl.index('def rich('):gl.index('VT = ')], ns)
render = ns['render']
gl2 = re.sub(r'assert done == \d+, done', 'assert done == 83, done  # 官方 32＋預測 49＋補習班 2', gl)
if gl2 != gl: io.open(os.path.join(H, 'gen_lj.py'), 'w', encoding='utf-8').write(gl2)

def paras(t): return ''.join('<p>' + E(x) + '</p>' for x in t.split('\n') if x.strip())

def lawcard(a, title):
    x = LAW[a]['x']; ps = []
    for line in x.split('\n'):
        line = line.strip()
        if line and line[0] in CIRC: line = CIRC[line[0]] + ' ' + line[1:].strip()
        ps.append('<p>' + E(line) + '</p>')
    return ('<details class="bt"><summary><b class="bn">§%s</b><span class="bti">%s</span><span class="bm">補習班模擬卷用到</span></summary>'
            '<div class="btx">%s</div></details>') % (a, E(title), ''.join(ps))

def card(key, m, d, lj):
    P = dict(d['parts']); no = '一二'[m['q_from']]
    chips = '<i class="pc">補習班模擬卷・非官方</i>' + ''.join('<i>%s</i>' % E(c) for c in m['chips'])
    summ = ('<summary><span class="eh"><span class="ck" aria-label="已讀">✓</span><b class="et">%s</b><span class="st"></span></span>'
            '<span class="em"><span class="ek">來勝模擬(一) 申論%s</span><span class="ec">%s</span></span><span class="chips">%s</span></summary>') % (E(m['et']), no, E(m['ec']), chips)
    oq = ('<div class="oq"><b>【補習班模擬卷｜來勝115模擬試題（一）申論題%s，出題：高律、嶺律；非考選部官方試題】</b>%s'
          '<br><a href="%%E6%%B0%%91%%E6%%B3%%95_%%E4%%BE%%86%%E5%%8B%%9D%%E6%%A8%%A1%%E6%%93%%AC%%E8%%A9%%A6%%E9%%A1%%8C%%E4%%B8%%80.html">老師版擬答與本站差異 →</a></div>') % (no, E(d['q']))
    vt = '<div class="vt"><button class="on" data-v="3">邏輯拆解</button><button data-v="1">考場速寫</button><button data-v="0">完整四段式</button></div>'
    # 完整四段式
    sub = re.split(r'\n?(?=（[一二三]）)', P['三、涵攝分析'].strip()); sub = [x for x in sub if x.strip()]
    assert len(sub) == len(m['sub_titles']), (key, len(sub))
    hs = ''.join('<details class="sub2"><summary><b>%s</b><span class="pt">%s</span></summary><div class="full">%s</div></details>'
                 % (E(t), E(pt), paras(re.sub(r'^（[一二三]）', '', x))) for t, pt, x in zip(m['sub_titles'], m['sub_pts'], sub))
    concl = re.sub(r'(?<=。)(?=（二）)', '\n', P['四、結論'])
    warn = [x for x in d['warn'].split('\n') if x.strip() and not x.startswith('補習班模擬題') and not x.startswith('【老師版與本站差異】') and not x.startswith('【老師原文錯字】')]
    bt = '<div class="btw"><div class="bth">📌 這題要背的條文（%d 條）</div>%s</div>' % (len(m['laws']), ''.join(lawcard(a, t) for a, t in m['laws']))
    full = ('<div class="vp" data-v="0" hidden>'
            '<details class="blk b1 fd"><summary><h5>一、定義</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b2 fd"><summary><h5>二、法條</h5></summary><div class="fdb">%s%s</div></details>'
            '<details class="blk b3 fd"><summary><h5>三、涵攝分析</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b4 fd"><summary><h5>四、結論</h5></summary><div class="fdb">%s</div></details>'
            '<details class="blk b5 fd"><summary><h5>考試陷阱・延伸</h5></summary><div class="fdb">%s%s</div></details></div>') % (
        paras(P['一、定義']), paras(P['二、法條']), bt, hs, paras(concl), paras(P['考試陷阱']), paras('\n'.join(warn)))
    # 考場速寫＋得分關鍵
    sk = dict((x[0], x[1]) for x in d['v'][1]['parts'])
    quick = '<div class="vp" data-v="1" hidden>' + ''.join('<div class="blk b%d"><h5>%s</h5><p>%s</p></div>' % (i + 1, h, t) for i, (h, t) in enumerate(m['quick']))
    quick += '<div class="kou"><b>口訣〔自編〕</b>　%s</div>' % E(d['m'])
    quick += '<div class="sk2"><h5>得分關鍵詞</h5><div class="chips big">%s</div><h5>常見失分點</h5><ul>%s</ul><h5>加分點</h5><p>%s</p></div></div>' % (
        ''.join('<i>%s</i>' % E(x.strip()) for x in sk['得分關鍵詞'].split('｜')),
        ''.join('<li>%s</li>' % E(re.sub(r'^[①②③④⑤]\s*', '', x)) for x in sk['常見失分點'].split('\n') if x.strip()), E(sk['加分點']))
    ljv = '<div class="vp" data-v="3" data-lj-root="1">' + render(lj) + '</div>'
    return ('<details class="essay es %s pred mock" data-lv="M" data-key="%s" data-yr="" data-g="%s">%s<div class="ebody">%s%s%s%s%s'
            '<label class="done"><input type="checkbox" class="rd" data-key="%s"> 我已讀過這題</label></div></details>\n') % (
        m['p'], key, m['g'], summ, oq, vt, full, quick, ljv, key)

# 移除舊卡
for key in META:
    i = s.find('<details class="essay es p4 pred mock" data-lv="M" data-key="%s"' % key)
    if i >= 0:
        e = s.index('</details>\n', s.index('<label class="done"><input type="checkbox" class="rd" data-key="%s">' % key, i)) + len('</details>\n')
        s = s[:i] + s[e:]
LJD = {x['k']: x for x in LJ}
for key, m in META.items():
    c = card(key, m, DATA[m['q_from']], LJD[key])
    a = re.search(r'<details class="essay[^"]*\bpred\b[^"]*" data-lv="P" data-key="[^"]+" data-yr="[^"]*" data-g="%s"' % m['g'], s)
    s = s[:a.start()] + c + s[a.start():]

# 篩選鈕
if 'data-f="M"' not in s:
    s = s.replace('<button data-f="P">', '<button data-f="M">補習班 2</button>\n    <button data-f="P">', 1)
JSR = [
 ("if(curF==='A'||curF==='B'||curF==='C'||curF==='P')ok=e.dataset.lv===curF;", "if(curF==='A'||curF==='B'||curF==='C'||curF==='P'||curF==='M')ok=e.dataset.lv===curF;"),
 ("ep=es.filter(function(e){return e.classList.contains('pred')}),", "ep=es.filter(function(e){return e.classList.contains('pred')&&!e.classList.contains('mock')}),em=es.filter(function(e){return e.classList.contains('mock')}),"),
 ("sb.textContent='已讀　官方 '+ro+'／'+eo.length+'　預測 '+rp+'／'+ep.length}});", "sb.textContent='已讀　官方 '+ro+'／'+eo.length+(em.length?'　補習班 '+em.filter(function(e){return readSet[e.dataset.key]}).length+'／'+em.length:'')+'　預測 '+rp+'／'+ep.length}});"),
 ("$('essum').textContent='已讀懂 '+r+'／'+N+' 題作答架構（官方 32＋預測 41）'", "$('essum').textContent='已讀懂 '+r+'／'+N+' 題作答架構（官方 '+essays.filter(function(e){return !e.classList.contains('pred')}).length+'＋補習班 '+essays.filter(function(e){return e.classList.contains('mock')}).length+'＋預測 '+essays.filter(function(e){return e.classList.contains('pred')&&!e.classList.contains('mock')}).length+'）'"),
 ("var np=d.querySelectorAll('.essay.pred').length,", "var np=d.querySelectorAll('.essay.pred:not(.mock)').length,nm=d.querySelectorAll('.essay.mock').length,"),
 ("var e1=d.querySelector('.essay:not(.pred)'),e2=d.querySelector('.essay.pred');", "var e1=d.querySelector('.essay:not(.pred)'),e2=d.querySelector('.essay.pred:not(.mock)'),e3=d.querySelector('.essay.mock');if(e3){var h3=document.createElement('div');h3.className='gsec p';h3.textContent='補習班模擬卷（非官方）'+nm+' 題';e3.before(h3)}"),
]
for a, b in JSR:
    if b in s: continue
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
io.open(HUB, 'w', encoding='utf-8').write(s)

U = os.path.join(R, 'bxm-use.js'); u = io.open(U, encoding='utf-8').read()
u2 = u.replace('name:"申論 81 題（官方32＋預測49）",done:rn,total:81,pct:Math.round(rn/81*100),txt:"已讀 "+rn+"／81"',
               'name:"申論 83 題（官方32＋補習班2＋預測49）",done:rn,total:83,pct:Math.round(rn/83*100),txt:"已讀 "+rn+"／83"')
if u2 != u: io.open(U, 'w', encoding='utf-8').write(u2)
print('ok', s.count('class="essay'), '張；bxm-use', '83' if '申論 83 題' in u2 else '未改')
