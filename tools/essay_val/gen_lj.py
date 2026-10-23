# 估價申論範文頁：版本鈕改為「邏輯拆解 → 考場速寫 → 完整四段式」
# - 邏輯拆解由 lj_data.json 產生（三種排法：① 推理鏈 ② 條文｜本題（計算題＝公式｜代入）③ 地圖＋勾選）
# - 考場速寫＝原「⚡速答版」＋得分關鍵詞（kw）；原速答版的「考試陷阱」改名為「常見失分點」
# - 原題（q-box）與預測依據（pred-info）移出，三個分頁共用
# - 可重複執行：已轉換的卡片會重新產生 lj-panel／sk2
# 用法：python3 gen_lj.py [--demo id1,id2,... 輸出路徑]   （--demo 不動正式頁）
import json, os, re, html, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
PAGE = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html')
E = html.escape
def rich(t): return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', E(t))
CN = '一二三四五'
LAB = {  # kind: (條文標, 本題標, 左欄頭, 右欄頭)
 'explain': ('條文', '說明', '條文／定義', '適用情形・注意'),
 'calc':    ('公式', '代入', '公式', '代入本題數字'),
 'case':    ('條文', '本題', '條文說什麼', '本題套進去'),
 'analyze': ('依據', '本題', '依據／道理', '本題怎麼說')}
DESC = {
 'explain': ('一步一步推：先問一句 → 條文／定義 → 適用情形 → 小結，箭頭寫上下關係。適合第一次讀懂。', '左＝條文或定義說什麼，右＝適用情形與注意事項，一列一組。適合對答案。'),
 'calc':    ('一步一步算：選方法 → 公式 → 代入本題數字 → 小結（含單位），箭頭寫上下關係。適合第一次讀懂。', '左＝公式，右＝代入本題數字，一列一組。適合對答案、驗算。'),
 'case':    ('一步一步推：先問一句 → 條文 → 本題 → 小結，箭頭寫上下關係。適合第一次讀懂。', '左＝條文說什麼，右＝本題套進去，一列一組。適合對答案。')}

def div_end(s, start):
    """s[start] 是 '<div'；回傳對應 '</div>' 之後的位置"""
    d = 0
    for m in re.finditer(r'<(/?)div\b[^>]*>', s[start:]):
        d += -1 if m.group(1) else 1
        if d == 0: return start + m.end()
    raise ValueError('div 不平衡')

def render(d):
    kind = d.get('kind', 'case'); dA, dB = DESC.get(kind, DESC['case'])
    subs = d['subs']; multi = len(subs) > 1
    def L(i): return LAB[subs[i].get('kind', kind)]
    def qh(i, sb):
        lab = f'問題{CN[i]}' if multi else '問題'
        return f'<div class="ljq"><span class="ljqn">{lab}</span><span class="ljqt">{E(sb["q"])}</span></div>'
    A = f'<p class="ljd">{dA}</p>'; n = 0
    for i, sb in enumerate(subs):
        tl, tf, hl, hr = L(i)
        A += qh(i, sb)
        if sb.get('pre'): A += f'<div class="ljar ljpre">{E(sb["pre"])}</div>'
        for j, st in enumerate(sb['steps']):
            n += 1
            A += f'<div class="ljst"><div class="ljsq"><span class="ljno">{n}</span>{E(st["ask"])}</div>'
            if st.get('lawh'): A += f'<p><span class="ljt tl">{tl}</span><b>{E(st["lawh"])}</b>：{E(st["law"])}</p>'
            A += f'<p><span class="ljt tf">{tf}</span>{E(st["fact"])}</p>'
            if st.get('res'): A += f'<p><span class="ljt ta">小結</span>{E(st["res"])}</p>'
            A += '</div>'
            if j < len(sb['steps']) - 1: A += f'<div class="ljar">↓ {E(st["link"])}</div>' if st.get('link') else '<div class="ljar">↓</div>'
        A += f'<div class="ljans"><b>答{CN[i] if multi else ""}：</b>{rich(sb["ans"])}</div>'
    if d.get('mnem'): A += f'<div class="kou"><b>口訣</b>　{E(d["mnem"])}</div>'
    B = f'<p class="ljd">{dB}</p>'
    for i, sb in enumerate(subs):
        tl, tf, hl, hr = L(i)
        B += qh(i, sb) + f'<div class="ljch"><span>{hl}</span><span>{hr}</span></div>'
        for st in sb['steps']:
            l = f'<div class="ljh">{E(st["lawh"])}</div>{E(st["law"])}' if st.get('lawh') else f'<div class="ljh">推理</div>{E(st["ask"])}'
            B += f'<div class="ljrow"><div class="ljl">{l}</div><div class="ljr"><div class="ljh">{E(st.get("facth") or tf)}</div>{E(st["fact"])}</div></div>'
        B += f'<div class="ljans"><b>答{CN[i] if multi else ""}：</b>{rich(sb["ans"])}</div>'
    C = '<p class="ljd">一眼看完推理順序，下方寫完逐項勾。適合考前複習。</p><div class="ljmap">'; n = 0
    for i, sb in enumerate(subs):
        C += f'<div><h6>{("問題" + CN[i] + "｜") if multi else ""}{E(sb["q"])}</h6><ul>'
        for j, st in enumerate(sb['steps']):
            n += 1
            C += f'<li><span class="ljno">{n}</span>{E(st["key"])}</li>'
            if j < len(sb['steps']) - 1: C += '<li class="ljdn">↓</li>'
        C += f'</ul><div class="ljans"><b>答：</b>{rich(sb["ans"])}</div></div>'
    C += '</div>'
    ck = d['checks']
    C += f'<div class="ljck"><b>寫完逐項勾（{len(ck)} 個採分點；<span class="ljhot">常錯</span>＝最常漏寫或寫錯）</b><ul>'
    for c in ck:
        tl, tf, hl, hr = L(c['sub'] - 1)
        t, cls = {'law': (tl, 'tl'), 'fact': (tf, 'tf'), 'ans': ('答', 'ta')}[c['t']]
        g = f'<span class="ljg">問題{CN[c["sub"] - 1]}</span>' if multi else ''
        hot = '<span class="ljhot">常錯</span>' if c.get('hot') else ''
        C += f'<li><label><input type="checkbox"><span class="ljt {cls}">{t}</span>{E(c["txt"])}{hot}</label>{g}</li>'
    C += '</ul></div>'
    seg = ('<div class="ljs"><span>排法</span><div class="ljseg">'
           '<button type="button" data-lj="A" class="on">① 推理鏈</button><button type="button" data-lj="B">② ' + {'calc': '公式｜代入', 'explain': '條文｜說明'}.get(kind, '條文｜本題') + '</button><button type="button" data-lj="C">③ 地圖＋勾選</button></div></div>')
    return ('<div class="lj-panel" data-lj-gen="1">' + seg + f'<div class="ljp" data-lj="A">{A}</div><div class="ljp" data-lj="B" hidden>{B}</div><div class="ljp" data-lj="C" hidden>{C}</div></div>')

def sk2(d):
    kw = d.get('kw') or []
    if not kw: return ''
    return ('<div class="sk2" data-lj-gen="1"><div class="sk2t">得分關鍵詞（閱卷看這幾個詞有沒有寫到）</div><div class="sk2c">'
            + ''.join(f'<span>{E(k)}</span>' for k in kw) + '</div></div>')

TABS = ('<div class="ver-bar vt3"><span class="ver-label">看法：</span><div class="seg-wrap">'
        '<button class="ver-btn active" data-ver="lj" onclick="setVer(this.closest(\'.essay-card\'),\'lj\')">邏輯拆解</button>'
        '<button class="ver-btn" data-ver="quick" onclick="setVer(this.closest(\'.essay-card\'),\'quick\')">考場速寫</button>'
        '<button class="ver-btn" data-ver="full" onclick="setVer(this.closest(\'.essay-card\'),\'full\')">完整四段式</button></div></div>')

def convert(block, d):
    # 1) 取出各部分
    b0 = block.index('<div class="card-body">'); head = block[:b0]
    b1 = div_end(block, b0)
    inner = block[b0 + len('<div class="card-body">'):b1 - len('</div>')]; tail = block[b1 - len('</div>'):]
    # 已轉換：先移除 lj-panel / sk2 / 分頁鈕
    for cls in ('ver-bar', 'lj-panel', 'sk2'):
        while True:
            m = re.search(r'<div class="%s[^"]*"[^>]*>' % cls, inner)
            if not m: break
            inner = inner[:m.start()] + inner[div_end(inner, m.start()):]
    # 2) 取 quick-ans / detail-content
    def pull(cls):
        nonlocal inner
        m = re.search(r'<div class="%s"[^>]*>' % cls, inner)
        if not m: return ''
        e = div_end(inner, m.start()); frag = inner[m.start():e]; inner = inner[:m.start()] + inner[e:]; return frag
    qa = pull('quick-ans')
    # detail-content 已被移出 shared（若先前轉換過，shared 在 detail 外）
    m = re.search(r'<div class="detail-content">', inner)
    if not m: raise ValueError('找不到 detail-content')
    dc_s = m.start(); dc_e = div_end(inner, dc_s)
    dc = inner[dc_s:dc_e]; rest = inner[:dc_s] + inner[dc_e:]
    shared = rest
    # 從 detail-content 內取 q-box / pred-info（第一次轉換時）
    dcin = dc[len('<div class="detail-content">'):-len('</div>')] if dc.endswith('</div>') else dc
    # detail 結尾可能帶註解 <!-- /detail-content -->
    pieces = {}
    for cls in ('pred-info', 'q-box'):
        mm = re.search(r'<div class="%s"[^>]*>' % cls, dcin)
        if mm:
            ee = div_end(dcin, mm.start()); pieces[cls] = dcin[mm.start():ee]; dcin = dcin[:mm.start()] + dcin[ee:]
    sh = rest.strip()
    for cls in ('q-box', 'pred-info'):
        if cls in pieces: sh += pieces[cls]
    # 順序：q-box 在前、pred-info 在後
    parts = re.findall(r'<div class="(?:q-box|pred-info)"[^>]*>.*?</div>', sh, flags=re.S)
    qbox = [p for p in parts if 'class="q-box"' in p]; pinfo = [p for p in parts if 'class="pred-info"' in p]
    assert qbox, '無 q-box'
    shared = ''.join(qbox + pinfo)
    # 考試陷阱 → 常見失分點
    qa = qa.replace('考試陷阱', '常見失分點')
    new_dc = '<div class="detail-content">' + dcin + '</div>'
    newbody = TABS + shared + (render(d) if d else '') + qa + (sk2(d) if d else '') + new_dc
    out = head + '<div class="card-body">' + newbody + tail
    out = re.sub(r'<div class="essay-card([^"]*)"', lambda m: m.group(0) if 'data-v=' in out[:200] else m.group(0), out, count=1)
    return out

CSS = '''<style id="lj-css">
/* 邏輯拆解（估價）：沿用頁面 token，深淺色自動跟隨 */
.essay-card .lj-panel,.essay-card .sk2{display:none}
.essay-card[data-v="lj"] .quick-ans,.essay-card[data-v="lj"] .detail-content,
.essay-card[data-v="quick"] .detail-content,.essay-card[data-v="full"] .quick-ans{display:none}
.essay-card[data-v="lj"] .lj-panel{display:block}
.essay-card[data-v="quick"] .quick-ans,.essay-card[data-v="quick"] .sk2,.essay-card[data-v="full"] .detail-content{display:block}
.essay-card:not([data-v]) .quick-ans{display:none}
.ver-bar.vt3 .seg-wrap{max-width:100%}
.sk2{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--paper2)}
.sk2t{font-size:.76rem;font-weight:700;color:var(--muted);margin-bottom:5px}
.sk2c{display:flex;flex-wrap:wrap;gap:6px}
.sk2c span{font-size:.82rem;font-weight:700;border:1px solid var(--line);border-radius:999px;padding:1px 10px;background:color-mix(in srgb,var(--gold) 14%,var(--paper2))}
.ljs{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 8px}
.ljs>span{font-size:.78rem;color:var(--muted);font-weight:700}
.ljseg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--paper2)}
.ljseg button{font:inherit;font-size:.8rem;padding:5px 11px;border:0;background:transparent;color:var(--ink);cursor:pointer}
.ljseg button+button{border-left:1px solid var(--line)}
.ljseg button.on{background:color-mix(in srgb,var(--primary) 16%,var(--paper2));color:var(--primary);font-weight:700}
.ljp[hidden]{display:none}
.ljd{font-size:.8rem;color:var(--muted);margin:2px 0 8px}
.ljq{display:flex;gap:8px;align-items:flex-start;margin:14px 0 8px}
.ljqn{flex:none;background:var(--primary);color:var(--paper2);font-weight:700;border-radius:7px;padding:1px 8px;font-size:.82rem}
.ljqt{font-weight:700;font-size:.92rem;line-height:1.55}
.ljt{display:inline-block;font-size:.72rem;font-weight:700;border-radius:5px;padding:0 6px;margin-right:6px;vertical-align:1px;white-space:nowrap}
.ljt.tl{background:color-mix(in srgb,var(--land) 16%,var(--paper2));color:var(--land)}
.ljt.tf{background:color-mix(in srgb,var(--gold) 18%,var(--paper2));color:var(--key)}
.ljt.ta{background:color-mix(in srgb,var(--green) 18%,var(--paper2));color:var(--green)}
.ljno{display:inline-flex;align-items:center;justify-content:center;flex:none;width:19px;height:19px;border-radius:50%;border:1.5px solid var(--primary);color:var(--primary);font-size:.72rem;font-weight:700;margin-right:6px}
.ljst{border:1px solid var(--line);border-radius:10px;padding:8px 11px;background:var(--paper2)}
.ljsq{font-weight:700;font-size:.88rem;display:flex;align-items:center;margin-bottom:3px}
.ljst p{margin:3px 0;font-size:.86rem;line-height:1.7}
.ljar{text-align:center;color:var(--muted);font-size:.78rem;line-height:1.35;padding:4px 6px}
.ljar.ljpre{text-align:left;padding:0 0 6px}
.ljans{background:color-mix(in srgb,var(--green) 12%,var(--paper2));border-left:4px solid var(--green);border-radius:8px;padding:7px 11px;font-size:.88rem;margin:8px 0 4px;line-height:1.7}
.ljans b{color:var(--green)}
.kou{margin-top:10px;background:color-mix(in srgb,var(--gold) 12%,var(--paper2));border:1px solid var(--line);border-radius:8px;padding:7px 11px;font-size:.86rem;line-height:1.7}
.ljch{display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.74rem;color:var(--muted);margin-bottom:4px}
.ljrow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:6px}
.ljrow>div{min-width:0;border-radius:8px;padding:7px 10px;font-size:.85rem;line-height:1.65}
.ljl{background:color-mix(in srgb,var(--land) 10%,var(--paper2))}.ljr{background:color-mix(in srgb,var(--gold) 10%,var(--paper2))}
.ljh{font-size:.76rem;font-weight:700;margin-bottom:1px}.ljl .ljh{color:var(--land)}.ljr .ljh{color:var(--key)}
.ljmap{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px}
.ljmap>div{min-width:0;border:1px solid var(--line);border-radius:10px;padding:8px 11px;background:var(--paper2)}
.ljmap h6{margin:0 0 6px;font-size:.86rem;font-family:inherit}
.ljmap ul{list-style:none;margin:0;padding:0;font-size:.84rem}
.ljmap li{display:flex;align-items:flex-start;padding:2px 0;line-height:1.55}
.ljmap li.ljdn{color:var(--muted);padding:0 0 0 25px;font-size:.72rem}
.ljck{margin-top:12px;border:1px solid var(--line);border-radius:10px;padding:8px 11px;font-size:.86rem}
.ljck ul{list-style:none;margin:6px 0 0;padding:0}
.ljck li{display:flex;gap:6px;align-items:flex-start;padding:6px 0;border-top:1px dashed var(--line)}
.ljck label{flex:1;min-width:0;display:block;line-height:1.6;cursor:pointer}
.ljck input{margin:0 6px 0 0;vertical-align:-2px;accent-color:var(--primary)}
.ljg{font-size:.74rem;color:var(--muted);white-space:nowrap}
.ljhot{display:inline-block;font-size:.7rem;font-weight:700;color:var(--stamp);background:color-mix(in srgb,var(--stamp) 12%,var(--paper2));border-radius:5px;padding:0 5px;margin-left:5px;white-space:nowrap}
@media (max-width:560px){.ljrow,.ljch{grid-template-columns:1fr}.ljch{display:none}.ljrow{gap:3px;margin-bottom:10px}.ljs>span{display:none}.ljseg{display:flex;flex-wrap:nowrap;width:100%}.ljseg button{flex:1;padding:6px 2px;font-size:.76rem;white-space:nowrap}.ver-bar.vt3 .ver-label{display:none}.ver-bar.vt3 .seg-wrap{width:100%}.ver-bar.vt3 .ver-btn{flex:1;text-align:center;padding:5px 4px}}
</style>'''
JS = '''<script id="lj-js">(function(){var K="bxv-ljv";function set(v,save){document.querySelectorAll(".ljseg button").forEach(function(b){b.classList.toggle("on",b.dataset.lj===v)});document.querySelectorAll(".ljp").forEach(function(p){p.hidden=p.dataset.lj!==v});if(save){try{localStorage.setItem(K,v)}catch(e){}}}
document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest(".ljseg button");if(b)set(b.dataset.lj,true)});
try{var v=localStorage.getItem(K);if(v&&/^[ABC]$/.test(v))set(v,false)}catch(e){}})();
function setVer(card,mode){card.setAttribute("data-v",mode);card.querySelectorAll(".ver-btn").forEach(function(b){b.classList.toggle("active",b.dataset.ver===mode)})}
document.querySelectorAll(".essay-card").forEach(function(c){if(!c.getAttribute("data-v"))setVer(c,"lj")});</script>'''

def split_cards(s):
    ms = list(re.finditer(r'<div class="essay-card[^"]*"[^>]*\bid="([^"]+)"', s))
    res = []
    for i, m in enumerate(ms):
        st = m.start(); e = div_end(s, st); res.append((m.group(1), st, e))
    return res

def process(s, D, only=None):
    cards = split_cards(s); out = []; pos = 0; n = 0
    for cid, st, e in cards:
        if only is not None and cid not in only: continue
        if cid not in D: continue
        blk = s[st:e]
        new = convert(blk, D[cid])
        new = re.sub(r'^<div class="essay-card([^"]*)"', lambda m: '<div class="essay-card%s" data-v="lj"' % m.group(1) if 'data-v=' not in blk[:300] else m.group(0), new, count=1)
        out.append(s[pos:st]); out.append(new); pos = e; n += 1
    out.append(s[pos:]); return ''.join(out), n

def inject(s):
    s = re.sub(r'<style id="lj-css">.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<script id="lj-js">.*?</script>', '', s, flags=re.S)
    # 舊 setVer 移除（新 JS 內有）
    s = re.sub(r"<script>\n// 速答版 / 完整版 切換\nfunction setVer\(card, mode\)\{.*?\n\}\n</script>\n?", '', s, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    return s

if __name__ == '__main__':
    D = {x['k']: x for x in json.load(open(os.path.join(HERE, 'lj_data.json'), encoding='utf-8'))}
    s = open(PAGE, encoding='utf-8').read()
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        ids = sys.argv[2].split(','); outp = sys.argv[3]
        t, n = process(s, D, set(ids))
        # 只留 demo 卡
        keep = []
        for cid, st, e in split_cards(t):
            if cid in ids: keep.append(t[st:e].replace('class="essay-card', 'class="essay-card open', 1))
        head = t[:t.index('<body')]
        kf = open(os.path.join(ROOT, 'kf-fit.js'), encoding='utf-8').read()
        body = ('<body><header><h1>邏輯拆解 demo｜不動產估價申論範文</h1><div class="sub">三分頁：邏輯拆解 → 考場速寫 → 完整四段式（正式頁尚未更動）</div></header>'
                '<div style="max-width:880px;margin:14px auto;padding:0 14px"><details class="tgroup" open><summary><div class="g-head"><div class="g-title">示範 3 題</div></div></summary><div class="g-body">'
                + '\n'.join(keep) + '</div></details></div>'
                '<script>function toggleCard(h){h.closest(".essay-card").classList.toggle("open")}function toggleRead(){}</script>'
                '<script>' + kf + '</script></body></html>')
        head = re.sub(r'<script src="bxv-use.js"[^>]*></script>', '', head)
        res = inject(head + body)
        open(outp, 'w', encoding='utf-8').write(res); print('demo', n, outp, len(res))
    else:
        t, n = process(s, D); t = inject(t)
        open(PAGE, 'w', encoding='utf-8').write(t); print('page', n)
