# 邏輯拆解 render（與 gen_lj.py 相同邏輯，供申論專練卷 zl_lj.py 使用）
import html, re
E = html.escape
def rich(t):  # **粗體**
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', E(t))
TAG = {'law': ('條文', 'tl'), 'fact': ('本題', 'tf'), 'ans': ('答', 'ta')}
CN = '一二三四五'

def render(d):
    subs = d['subs']; multi = len(subs) > 1
    def qh(i, sb):
        lab = f'問題{CN[i]}' if multi else '問題'
        return f'<div class="ljq"><span class="ljqn">{lab}</span><span class="ljqt">{E(sb["q"])}</span></div>'
    # ① 推理鏈
    A = '<p class="ljd">一步一步推：先問一句 → 條文 → 本題 → 小結，箭頭寫上下關係。適合第一次讀懂。</p>'
    n = 0
    for i, sb in enumerate(subs):
        A += qh(i, sb)
        if sb.get('pre'): A += f'<div class="ljar ljpre">{E(sb["pre"])}</div>'
        for j, st in enumerate(sb['steps']):
            n += 1
            A += f'<div class="ljst"><div class="ljsq"><span class="ljno">{n}</span>{E(st["ask"])}</div>'
            if st.get('lawh'): A += f'<p><span class="ljt tl">條文</span><b>{E(st["lawh"])}</b>：{E(st["law"])}</p>'
            A += f'<p><span class="ljt tf">本題</span>{E(st["fact"])}</p>'
            if st.get('res'): A += f'<p><span class="ljt ta">小結</span>{E(st["res"])}</p>'
            A += '</div>'
            if st.get('link') and j < len(sb['steps']) - 1: A += f'<div class="ljar">↓ {E(st["link"])}</div>'
            elif j < len(sb['steps']) - 1: A += '<div class="ljar">↓</div>'
        A += f'<div class="ljans"><b>答{CN[i] if multi else ""}：</b>{rich(sb["ans"])}</div>'
    if d.get('mnem'): A += f'<div class="kou"><b>口訣</b>　{E(d["mnem"])}</div>'
    # ② 條文｜本題
    B = '<p class="ljd">左＝條文說什麼，右＝本題套進去，一列一組。適合對答案。</p>'
    for i, sb in enumerate(subs):
        B += qh(i, sb) + '<div class="ljch"><span>條文說什麼</span><span>本題套進去</span></div>'
        for st in sb['steps']:
            l = f'<div class="ljh">{E(st["lawh"])}</div>{E(st["law"])}' if st.get('lawh') else f'<div class="ljh">推理</div>{E(st["ask"])}'
            B += f'<div class="ljrow"><div class="ljl">{l}</div><div class="ljr"><div class="ljh">{E(st.get("facth") or "本題")}</div>{E(st["fact"])}</div></div>'
        B += f'<div class="ljans"><b>答{CN[i] if multi else ""}：</b>{rich(sb["ans"])}</div>'
    # ③ 地圖＋勾選
    C = '<p class="ljd">一眼看完推理順序，下方寫完逐項勾。適合考前複習。</p><div class="ljmap">'
    n = 0
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
        t, cls = TAG[c['t']]
        g = f'<span class="ljg">問題{CN[c["sub"] - 1]}</span>' if multi else ''
        hot = '<span class="ljhot">常錯</span>' if c.get('hot') else ''
        C += f'<li><label><input type="checkbox"><span class="ljt {cls}">{t}</span>{E(c["txt"])}{hot}</label>{g}</li>'
    C += '</ul></div>'
    return ('<div class="ljs"><span>排法</span><div class="ljseg">'
            '<button type="button" data-lj="A" class="on">① 推理鏈</button><button type="button" data-lj="B">② 條文｜本題</button><button type="button" data-lj="C">③ 地圖＋勾選</button></div></div>'
            f'<div class="ljp" data-lj="A">{A}</div><div class="ljp" data-lj="B" hidden>{B}</div><div class="ljp" data-lj="C" hidden>{C}</div>')

CSS = '''<style id="lj-css">
.ebody .vp[data-v="1"] .sk2{margin-top:12px;border:1px solid var(--line);border-radius:10px;padding:4px 12px 8px}
.ljs{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:4px 0 6px;padding:6px 8px;background:var(--bg);border-radius:10px}
.ljs>span{font-size:.8rem;color:var(--sub)}
.ljseg{display:inline-flex;flex-wrap:wrap;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:var(--surface)}
.ljseg button{font:inherit;font-size:.82rem;padding:5px 11px;border:0;background:transparent;color:var(--ink);cursor:pointer}
.ljseg button+button{border-left:1px solid var(--line)}
.ljseg button.on{background:var(--pri-soft);color:var(--pri);font-weight:700}
.ljseg button:focus-visible{outline:2px solid var(--pri);outline-offset:-2px}
.ljp[hidden]{display:none}
.ljd{font-size:.8rem;color:var(--sub);margin:2px 0 8px}
.ljq{display:flex;gap:8px;align-items:flex-start;margin:14px 0 8px}
.ljqn{flex:none;background:var(--pri);color:var(--on);font-weight:700;border-radius:7px;padding:1px 8px;font-size:.84rem}
.ljqt{font-weight:700;font-size:.95rem;line-height:1.55}
.ljt{display:inline-block;font-size:.72rem;font-weight:700;border-radius:5px;padding:0 6px;margin-right:6px;vertical-align:1px;white-space:nowrap}
.ljt.tl{background:color-mix(in srgb,var(--b2) 16%,var(--surface));color:var(--b2)}
.ljt.tf{background:color-mix(in srgb,var(--b3) 16%,var(--surface));color:var(--b3)}
.ljt.ta{background:color-mix(in srgb,var(--b4) 18%,var(--surface));color:var(--b4)}
.ljno{display:inline-flex;align-items:center;justify-content:center;flex:none;width:19px;height:19px;border-radius:50%;border:1.5px solid var(--pri);color:var(--pri);font-size:.72rem;font-weight:700;margin-right:6px}
.ljst{border:1px solid var(--line);border-radius:10px;padding:8px 11px;background:var(--surface)}
.ljsq{font-weight:700;font-size:.9rem;display:flex;align-items:center;margin-bottom:3px}
.ljst p{margin:3px 0;font-size:.88rem;line-height:1.65}
.ljar{text-align:center;color:var(--sub);font-size:.8rem;line-height:1.35;padding:4px 6px}
.ljar.ljpre{text-align:left;padding:0 0 6px}
.ljans{background:color-mix(in srgb,var(--b4) 12%,var(--surface));border-left:4px solid var(--b4);border-radius:8px;padding:7px 11px;font-size:.9rem;margin:8px 0 4px;line-height:1.65}
.ljans b{color:var(--b4)}
.ljch{display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:.74rem;color:var(--sub);margin-bottom:4px}
.ljrow{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:6px}
.ljrow>div{min-width:0;border-radius:8px;padding:7px 10px;font-size:.88rem;line-height:1.6}
.ljl{background:color-mix(in srgb,var(--b2) 10%,var(--surface))}.ljr{background:color-mix(in srgb,var(--b3) 10%,var(--surface))}
.ljh{font-size:.76rem;font-weight:700;margin-bottom:1px}.ljl .ljh{color:var(--b2)}.ljr .ljh{color:var(--b3)}
.ljmap{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px}
.ljmap>div{min-width:0;border:1px solid var(--line);border-radius:10px;padding:8px 11px;background:var(--surface)}
.ljmap h6{margin:0 0 6px;font-size:.88rem}
.ljmap ul{list-style:none;margin:0;padding:0;font-size:.86rem}
.ljmap li{display:flex;align-items:flex-start;padding:2px 0;line-height:1.55}
.ljmap li.ljdn{color:var(--sub);padding:0 0 0 25px;font-size:.72rem}
.ljck{margin-top:12px;border:1px solid var(--line);border-radius:10px;padding:8px 11px;font-size:.88rem}
.ljck ul{list-style:none;margin:6px 0 0;padding:0}
.ljck li{display:flex;gap:6px;align-items:flex-start;padding:6px 0;border-top:1px dashed var(--line)}
.ljck label{flex:1;min-width:0;display:block;line-height:1.6;cursor:pointer}
.ljck input{margin:0 6px 0 0;vertical-align:-2px;accent-color:var(--pri)}
.ljg{font-size:.74rem;color:var(--sub);white-space:nowrap}
.ljhot{display:inline-block;font-size:.7rem;font-weight:700;color:var(--bad);background:var(--bad-soft);border-radius:5px;padding:0 5px;margin-left:5px;white-space:nowrap}
@media (max-width:560px){.ljrow,.ljch{grid-template-columns:1fr}.ljch{display:none}.ljrow{gap:3px;margin-bottom:10px}.ljs>span{display:none}.ljs{padding:0;background:none}.ljseg{display:flex;flex-wrap:nowrap;width:100%}.ljseg button{flex:1;padding:6px 2px;font-size:.78rem;white-space:nowrap}}
</style>'''
