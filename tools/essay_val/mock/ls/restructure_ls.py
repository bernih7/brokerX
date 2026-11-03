# -*- coding: utf-8 -*-
"""施工單《申論統一》第一節：補習班卷 2 張（mk-ls1、mk-ls2）改成
   邏輯拆解｜考場速寫｜考場版｜完整四段式（＝本站擬答）｜老師版擬答（來勝原文照抄）
內容來源：src_*.json（site_html 本站擬答、teacher_html 老師版原文，皆原文不改）、out_*.json（lj、quick_html、exam）。
可重跑：整個 card-body 依來源重建。之後跑 exam/inject.py（考場版）與 split_sx_lists.py。"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); EV = os.path.normpath(os.path.join(H, '..', '..')); ROOT = os.path.normpath(os.path.join(EV, '..', '..'))
sys.path.insert(0, EV)
import gen_lj
PAGE = os.path.join(ROOT, '不動產估價概要_申論題實戰範文.html')
LJ = os.path.join(EV, 'lj_data.json'); EXV = os.path.join(EV, 'exam', 'exam_ver.json')
def div_end(s, i):
    d = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[i:]):
        d += 1 if m.group(0).startswith('<div') else -1
        if d == 0: return i + m.end()
def btn(v, t, tip, on=False):
    return ('<button class="ver-btn%s" data-ver="%s" title="%s" onclick="setVer(this.closest(\'.essay-card\'),\'%s\')">%s</button>'
            % (' active' if on else '', v, tip, v, t))
TABS = ('<div class="ver-bar vt5"><span class="ver-label">看法：</span><div class="seg-wrap">'
        + btn('lj', '邏輯拆解', '一步一步推：問一句→條文／公式→本題→小結，附採分點勾選', True)
        + btn('quick', '考場速寫', '考場上來不及時的最小可得分版本：公式、常見失分點、得分關鍵詞')
        + btn('exam', '考場版', '考場 25 分鐘寫得完的版本：意義→法條→涵攝→結論')
        + btn('full', '完整四段式', '本站依現行技術規則寫的完整答案，附條號')
        + btn('teacher', '老師版', '來勝解答原文照抄（補習班模擬題，非官方）') + '</div></div>')
CSS = '''<style id="ls-css">
.teacher-ans{display:none}.essay-card[data-v="teacher"] .teacher-ans{display:block}
.essay-card[data-v="teacher"] :is(.detail-content,.exam-ver,.quick-ans,.lj-panel,.sk2){display:none!important}
.vt5 .ver-label{display:none}.vt5 .seg-wrap{width:100%;max-width:100%}.vt5 .ver-btn{flex:1;text-align:center;padding:5px 1px;font-size:.84rem}
@media(max-width:420px){.vt5 .ver-btn{font-size:.74rem;letter-spacing:-.02em}}
</style>'''
def main():
    s = open(PAGE, encoding='utf-8').read()
    d = json.load(open(LJ, encoding='utf-8')); ev = json.load(open(EXV, encoding='utf-8'))
    for cid in ('mk-ls1', 'mk-ls2'):
        src = json.load(open(os.path.join(H, 'src_%s.json' % cid), encoding='utf-8'))
        out = json.load(open(os.path.join(H, 'out_%s.json' % cid), encoding='utf-8'))
        a = s.find('id="%s"' % cid); a = s.rfind('<div class="essay-card', 0, a)
        b0 = s.find('<div class="card-body">', a); b1 = div_end(s, b0)
        body = ('<div class="card-body">' + TABS + src['q_html']
                + gen_lj.render(out['lj']) + '<div class="quick-ans">' + out['quick_html'] + '</div>' + gen_lj.sk2(out['lj'])
                + '<div class="detail-content">' + src['site_html'] + '</div>'
                + '<div class="teacher-ans">' + src['teacher_html'] + '</div></div>')
        s = s[:b0] + body + s[b1:]
        d = [x for x in d if x['k'] != cid] + [out['lj']]; ev[cid] = out['exam']
    if 'id="ls-css"' in s: s = re.sub(r'<style id="ls-css">.*?</style>', CSS, s, flags=re.S)
    else: s = s.replace('</head>', CSS + '\n</head>', 1)
    open(PAGE, 'w', encoding='utf-8').write(s)
    json.dump(d, open(LJ, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(ev, open(EXV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    # exam/out_*.json 與 in_*.json 也同步（inject.py 會用 out 檔覆蓋；check.py 以 in 檔 full 為完整版）
    import glob, html as _h
    for f in glob.glob(os.path.join(EV, 'exam', 'out_*.json')):
        o = json.load(open(f, encoding='utf-8')); ch = False
        for cid in ('mk-ls1', 'mk-ls2'):
            if cid in o: o[cid] = ev[cid]; ch = True
        if ch: json.dump(o, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    def txt(h):
        h = re.sub(r'<br\s*/?>', '\n', h); h = re.sub(r'</(p|div|li|tr|h\d)>', '\n', h); h = re.sub(r'<[^>]+>', '', h)
        return re.sub(r'\n\s*\n+', '\n', re.sub(r'[ \t]+', ' ', _h.unescape(h))).strip()
    for f in glob.glob(os.path.join(EV, 'exam', 'in_*.json')):
        arr = json.load(open(f, encoding='utf-8')); ch = False
        for x in arr:
            if x['id'] in ('mk-ls1', 'mk-ls2'):
                x['full'] = txt(json.load(open(os.path.join(H, 'src_%s.json' % x['id']), encoding='utf-8'))['site_html']); ch = True
        if ch: json.dump(arr, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('重建 mk-ls1、mk-ls2')
if __name__ == '__main__': main()
