# -*- coding: utf-8 -*-
"""估價「申論 5 分鐘・推理版」（改自經紀法規 tools/essay_jj/sprint/build_reason.py）。內容一字不改，只換呈現方式。
用法：python3 tools/essay_val/sprint/build_reason.py          → 估價_申論5分鐘_推理版.html
      python3 tools/essay_val/sprint/build_reason.py demo     → demo/估價_申論5分鐘_推理版_demo.html（3 張、不存紀錄）
- 推理鏈：lj_data.json 的 subs／steps（步驟標籤依邏輯拆解類型：條文・公式・依據／說明・代入・本題，與範文頁「① 推理鏈」相同）
- ③ 速寫骨架：範文頁「考場速寫」.quick-ans 的定義／公式／代入各塊＋口訣（lj mnem）
- ④ 失分點：.quick-ans 的「常見失分點」塊（依「；」分條）
- ⑤ 得分關鍵詞：lj_data.json 的 kw；條號型關鍵詞用 kw_cn.json 的中文代表（2～8 字，條號小字附在後面），程式發現仍有條號就中止
秒數依文字量分配（模板 plan()），題數、步數都從資料算。卡片清單與 build_sprint.py 共用（load()）。"""
import os, re, json, sys
import sys as _s, os as _o; _s.path.insert(0, _o.path.normpath(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), '..', '..'))); import sprint_hp as _hp  # 115 高／中機率排序（11-03）
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, H); sys.path.insert(0, os.path.normpath(os.path.join(H, '..', '..')))
from build_sprint import load, md, clean, div_body
from sprint_sx_law import annotate  # 速寫法條塊：只有條號清單時補本題名稱、一條一行（11-03，共用）

LAB = {'explain': ('條文', '說明'), 'calc': ('公式', '代入'), 'case': ('條文', '本題'), 'analyze': ('依據', '本題')}  # 同 tools/essay_val/gen_lj.py
QA = {'qa-def': 'b1', 'qa-form': 'b2', 'qa-calc': 'b3'}
ART = re.compile(r'§|第\s*\d+\s*條')

def kw_mark(h):
    """範文頁重點 <span class="qa-kw">…</span> → <mark>…</mark>（依巢狀深度配對結尾；空的拿掉）"""
    out, stack, pos = [], [], 0
    for m in re.finditer(r'<span\b[^>]*>|</span>', h):
        out.append(h[pos:m.start()]); pos = m.end(); t = m.group(0)
        if t.startswith('<span'):
            kw = 'class="qa-kw"' in t; stack.append(kw); out.append('<mark>' if kw else t)
        else:
            out.append('</mark>' if (stack.pop() if stack else False) else t)
    out.append(h[pos:])
    return re.sub(r'<mark>\s*</mark>', '', ''.join(out))

def quick(c):
    i = c.find('<div class="quick-ans')
    if i < 0: return [], []
    qa, _ = div_body(c, i)
    sx, lose = [], []
    for m in re.finditer(r'<div class="qa-blk ([^"]+)">', qa):
        body, _ = div_body(qa, m.start())
        lm = re.match(r'\s*<div class="qa-label">(.*?)</div>', body, re.S)
        lab = clean(lm.group(1)).lstrip('▌').strip() if lm else ''
        body = body[lm.end():] if lm else body
        body = kw_mark(body.strip())
        body = re.sub(r'<code class="qa-code">', '<code>', body)
        body = re.sub(r'\s*\n\s*', '', body)
        cls = m.group(1).split()[0]
        if cls == 'qa-trap':
            # 依「；」與 <br> 分條（標籤內的分號不切）
            parts = re.split(r'<br\s*/?>|；(?![^<]*>)', body)
            lose += [p.strip() for p in parts if clean(p)]
        else:
            sx.append([QA.get(cls, 'b4'), lab, '<p>%s</p>' % body])
    return sx, lose

def build(cards):
    kwcn = json.load(open(os.path.join(H, 'kw_cn.json'), encoding='utf-8'))
    out, skip, todo = [], [], {}
    for c in cards:
        lj = c['_lj']; sx, lose = quick(c['_c'])
        if not sx or not lj.get('kw'):
            skip.append((c['id'], '沒有考場速寫或得分關鍵詞')); continue
        steps_all = [st for s_ in lj['subs'] for st in s_['steps']]
        # 只有條號清單的塊：補本題名稱、一條一行（與經紀法規／民法同一支 sprint_sx_law.annotate；其他塊不動）
        for x in sx:
            core = re.sub(r'<[^>]+>', '', x[2])
            if re.fullmatch(r'[\s§\dⅠ-Ⅹ①-⑳之\-、，；。–～]+', core) and '§' in core: x[2] = annotate(x[2], steps_all)[0]
        kind = lj.get('kind', 'case')
        subs = []
        for s_ in lj['subs']:
            tl, tf = LAB.get(s_.get('kind') or kind, LAB['case'])
            subs.append({'q': s_['q'], 'pre': s_.get('pre', ''), 'ans': md(s_.get('ans', '')),
                         'st': [dict({f: st.get(f, '') for f in ('ask', 'key', 'lawh', 'law', 'facth', 'fact', 'res', 'link')}, lt=st.get('lt') or tl, ft=tf) for st in s_['steps']]})
        m = kwcn.get(c['id'], {}); kws = []
        for k in lj['kw']:
            if k in m:
                if m[k] is None: continue
                kws.append({'c': m[k], 'a': k})
            else: kws.append({'c': k, 'a': ''})
        bad = [x['c'] for x in kws if ART.search(x['c'])]
        if bad: todo[c['id']] = bad
        out.append({'id': c['id'], 'no': c['no'], 't': c['t'], 'g': c['g'], 'q': c['q'], 'subs': subs, 'sx': sx,
                    'kou': lj.get('mnem', ''), 'kws': kws, 'lose': lose, 'k': c['k'], 'tier': c['tier']})
    return out, skip, todo

if __name__ == '__main__':
    demo = 'demo' in sys.argv
    cards, skip0 = load()
    if demo: cards = [c for c in cards if c['id'] in ('e105-1', 'e113-1', 'pred-6')]
    data, skip, todo = build(cards)
    json.dump(todo, open(os.path.join(H, 'kw_todo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if todo:
        print('⚠ 得分關鍵詞仍是條號、尚無中文代表（已寫入 kw_todo.json，請在 kw_cn.json 補 2～8 字中文代表）：', todo)
        if not demo: sys.exit(1)
    tpl = open(os.path.join(H, 'tpl_reason.html'), encoding='utf-8').read()
    out = tpl.replace('/*__DATA__*/[]', json.dumps(_hp.tag(data, 'val'), ensure_ascii=False)).replace('/*__DEMO__*/false', 'true' if demo else 'false').replace('__ROOT__', '../' if demo else '')
    dst = os.path.join(ROOT, 'demo', '估價_申論5分鐘_推理版_demo.html') if demo else os.path.join(ROOT, '估價_申論5分鐘_推理版.html')
    open(dst, 'w', encoding='utf-8').write(out)
    print('推理版', len(data), '張；推理', sum(len(s['st']) for d in data for s in d['subs']), '步；關鍵詞', sum(len(d['kws']) for d in data), '個；失分點', sum(len(d['lose']) for d in data), '條')
    if skip0 or skip: print('⚠ 未列入：', skip0 + skip)
