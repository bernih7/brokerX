# -*- coding: utf-8 -*-
"""5 分鐘衝刺／推理版排序（11-03 使用者）：①115 出題預測「高」且沒做過 → ②「中」且沒做過 → ③其他沒做過 → ④做過的依不熟程度（同程度高機率先）。
資料來源＝各科《申論115出題預測》頁（民法：p高／p中 區塊的「讀這幾題」；經紀法規、估價：頁內 D.topics 的 tier 與題卡）。
用法：build 腳本 json.dumps 前呼叫 tag(cards, subj)；python3 tools/sprint_hp.py 會修改各科模板的 order()/reason()（可重跑）。"""
import os, re, json, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
TIER = {'高': 0, '中': 1}
def _civ():
    s = open(os.path.join(R, '民法_申論115出題預測.html'), encoding='utf-8').read(); out = []
    for m in re.finditer(r'<div class="pc p(\S+?)">.*?讀這幾題：(.*?)</p>', s, re.S):
        out.append((m.group(1), re.findall(r'essay=([^"]+)"', m.group(2))))
    return out
def _D(fn):
    s = open(os.path.join(R, fn), encoding='utf-8').read(); i = s.find('var D=') + 6
    return json.JSONDecoder().raw_decode(s[i:])[0]
def _jj():
    return [(t['tier'], ['es-' + o['fw'] for o in t['off'] if o.get('fw')] + ['es-' + p['id'] for p in t['pred']]) for t in _D('經紀法規_申論115出題預測.html')['topics']]
def _val():
    return [(t['tier'], list(t.get('cards', [])) + list(t.get('sec', []))) for t in _D('估價_申論115出題預測.html')['topics']]
def ranks(subj):
    src = {'civ': _civ, 'jj': _jj, 'val': _val}[subj](); out = {}; n = 0
    for tier, ids in src:
        if tier not in TIER: continue
        for i in ids:
            n += 1
            if i not in out: out[i] = (TIER[tier] * 1000 + n, tier)
    return out
def tag(cards, subj):
    M = ranks(subj); hit = 0
    for c in cards:
        r = M.get(c.get('id'))
        if r: c['hp'], c['hpl'] = r; hit += 1
        else: c.pop('hp', None); c.pop('hpl', None)
    print('  115 高／中機率排序：%d／%d 張有標' % (hit, len(cards)))
    return cards

def patch_templates():
    for sub in ('essay_civ', 'essay_jj', 'essay_val'):
        for fn in ('tpl.html', 'tpl_reason.html'):
            p = os.path.join(R, 'tools', sub, 'sprint', fn)
            if not os.path.exists(p): continue
            s = open(p, encoding='utf-8').read()
            if 'function hpR(' in s: print('skip', p); continue
            m = re.search(r"  fresh\.sort\(function\(a,b\)\{return (\w+)\(a\.c\)-\1\(b\.c\)\|\|a\.c\.tier-b\.c\.tier\|\|a\.i-b\.i\}\);", s); assert m, p
            s = s.replace(m.group(0), "  function hpR(c){return c.hp==null?9999:c.hp}\n  fresh.sort(function(a,b){return hpR(a.c)-hpR(b.c)||%s(a.c)-%s(b.c)||a.c.tier-b.c.tier||a.i-b.i});" % (m.group(1), m.group(1)), 1)
            a = "seen.sort(function(a,b){return vr(a.s.v)-vr(b.s.v)||pct(a)-pct(b)||a.s.t-b.s.t});"; assert s.count(a) == 1, p
            s = s.replace(a, "seen.sort(function(a,b){return vr(a.s.v)-vr(b.s.v)||hpR(a.c)-hpR(b.c)||pct(a)-pct(b)||a.s.t-b.s.t});", 1)
            a = "if(!s.n&&!s.sp&&!s.read)o.push('<span class=\"chip new\">沒做過</span>');"; assert s.count(a) == 1, p
            s = s.replace(a, "if(x.c.hpl)o.push('<span class=\"chip '+(x.c.hpl==='高'?'hard':'mid')+'\">🔥 115 '+x.c.hpl+'機率</span>');\n  " + a, 1)
            s = s.replace('沒做過的優先，再來不熟的 ----', '115 高機率且沒做過的優先 → 中機率沒做過 → 其他沒做過 → 做過但不熟的（11-03） ----', 1)
            open(p, 'w', encoding='utf-8').write(s); print('ok', p)
if __name__ == '__main__':
    for sj in ('civ', 'jj', 'val'):
        M = ranks(sj); print(sj, '高', sum(1 for v in M.values() if v[1] == '高'), '中', sum(1 for v in M.values() if v[1] == '中'))
    patch_templates()
