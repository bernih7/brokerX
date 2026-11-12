# -*- coding: utf-8 -*-
"""產生四科錯題複習卷題池 bx-pool-<科>.js：各模擬卷題目＋歷屆題庫，統一格式。
每題 {id, p:卷代碼或 "h", src:出處, sec, stem, opts, ok:[正解索引], ex:[四選項解析], tr:陷阱}
id：模擬卷＝<卷>-<題號>（與 bx-mockrec.js 記錄一致）；歷屆＝h:<年>-<題號>。可重跑。"""
import os, re, json, html as H
R = os.path.join(os.path.dirname(__file__), '..', '..')
L = 'ABCD'
def rd(f): return open(os.path.join(R, f), encoding='utf-8').read()
def jd(s, mark):
    i = s.index(mark) + len(mark); return json.JSONDecoder().raw_decode(s[i:])[0]
def strip(t):  # 題庫文字裡少數 HTML 標記
    t = re.sub(r'<br\s*/?>', '\n', t or ''); t = re.sub(r'<[^>]+>', '', t); return H.unescape(t).strip()
def item(id, p, src, sec, stem, opts, ok, ex, tr='', an=None):
    assert len(ex or []) in (0, 4), (id, '解析數≠4：逐項判斷要放 st，不能塞進選項解析')
    ex = [strip(x) for x in (ex or [])] + [''] * (4 - len(ex or []))
    d = dict(id=id, p=p, src=src, sec=sec or '', stem=strip(stem), opts=[strip(o) for o in opts], ok=ok, ex=ex[:4], tr=strip(tr))
    if an: d['an'] = [strip(x) for x in an]
    return d

def varD(f, pid, name, S):
    s = rd(f); D = jd(s, 'var D=') if 'var D=' in s else None
    out = []
    for q in D['Q']:
        ok = [L.index(q['ans'])] + [L.index(a) for a in q.get('alt') or [] if a in L]
        out.append(item('%s-%s' % (pid, q['n']), pid, '%s 第%s題' % (name, q['n']), q.get('sec') or q.get('ch', ''), q['stem'], q['opts'], sorted(set(ok)), q.get('notes'), q.get('trap', ''), q.get('st')))
    return out

def vq(f, pid, name):
    s = rd(f); i = s.index('const QUESTIONS=') + len('const QUESTIONS=')
    Q = json.JSONDecoder().raw_decode(s[i:])[0]
    return [item('%s-%d' % (pid, k + 1), pid, '%s 第%d題' % (name, k + 1), '', q['text'], [re.sub(r'^[A-D][.．、]\s*', '', o) for o in q['opts']], [q['ans']], q.get('exps')) for k, q in enumerate(Q)]

def hs(f):
    s = rd(f); i = s.index('const ITEMS = '); j = s.index('];', i) + 1
    js = s[i + len('const ITEMS = '):j]
    import subprocess
    Q = json.loads(subprocess.check_output(['node', '-e', 'process.stdout.write(JSON.stringify(eval(require("fs").readFileSync(0,"utf8"))))'], input=js.encode()))
    return [item('hs1-%d' % (k + 1), 'hs1', '估價來勝模擬試題一 第%d題' % (k + 1), q.get('ch', ''), q['q'], q['opts'], [q['correct']], q.get('explains'), q.get('trap', '')) for k, q in enumerate(Q)]

def vdiag(f):
    s = rd(f); out = []
    for m in re.finditer(r'<div class="card" id="c(\d+)" data-a="([A-D])" data-cat="([^"]*)"[^>]*>(.*?)\n</div>\s*(?=<!--|</div>\s*\n\s*<div class="res|<div class="card"|\n\n)', s, re.S):
        n, a, cat, body = m.groups()
        stem = re.search(r'<div class="stem">(.*?)</div>', body, re.S).group(1)
        opts = re.findall(r'<span class="nt">(.*?)</span></button>', body, re.S)
        tr = re.search(r'<div class="trap" id="t\d+">(.*?)</div>\s*$', body, re.S)
        tr = strip(tr.group(1)) if tr else ''
        out.append(item('vdiag1-%s' % n, 'vdiag1', '估價診斷卷① 第%s題' % n, cat, stem, opts, [L.index(a)], ['', '', '', ''], tr))
    return out

def hist(S):
    out = []
    if S in ('land', 'jj'):
        js = rd('bxl-quiz-data.js' if S == 'land' else 'bxj-quiz-data.js')
        Q = json.loads(js[js.index('{"q":'):js.rindex('}') + 1])['q']
        for q in Q:
            a = q['ans']; ok = [L.index(a)] if isinstance(a, str) else [a]
            out.append(item('h:' + q['k'], 'h', '%s年第%s題' % (q['y'], q['n']), q['ch'], q['stem'], q['opt'], ok, q['exp']))
    elif S == 'civ':
        for q in [q for q in json.load(open(os.path.join(R, 'tools/civ_quiz/quiz_data.json'), encoding='utf-8'))['q'] if q['acc'] and len(q['acc']) < 4]:  # 一律給分題不出
            out.append(item('h:' + q['k'], 'h', '%s年第%s題' % (q['y'], q['n']), q['ch'], q['stem'], q['opt'], sorted(L.index(a) for a in q['acc']), q['exp']))
    else:
        import subprocess
        Q = json.loads(subprocess.check_output(['node', '-e', 'global.window=global;require("./bxv-quiz-data.js");process.stdout.write(JSON.stringify(BXV_QUIZ.items))'], cwd=R))
        for q in Q:
            hid, src = ('h:%s-%s' % (q['y'], q['n']), '%s年第%s題' % (q['y'], q['n'])) if q['y'] else ('h:' + q['id'], '刷題補充題 ' + q['id'])
            out.append(item(hid, 'h', src, q['ch'], q['q'], q['opts'], [q['correct']], q['exps']))
    return out

P = {
 'land': [('土地法_診斷卷一.html', 'landdiag1', '土地法診斷卷①'), ('土地法_診斷卷二.html', 'landdiag2', '土地法診斷卷②'),
          ('土地法_來勝模擬試題一_土地法規.html', 'll_a1', '來勝(一)土地法規'), ('土地法_來勝模擬試題一_土地稅法.html', 'll_b1', '來勝(一)土地稅法')],
 'civ': [('民法_來勝模擬試題一.html', 'civls1', '民法來勝(一)'), ('民法_模擬試題一.html', 'civ1', '民法模擬試題一'), ('民法_模擬試題二.html', 'civ2', '民法模擬試題二')],
 'jj': [('經紀法規_診斷卷一.html', 'diag1', '經紀法規診斷卷①'), ('經紀法規_高頻考點卷二.html', 'hi2', '高頻考點卷②'), ('經紀法規_混淆對比卷三.html', 'cf3', '混淆對比卷③'),
        ('經紀法規_全真模擬卷四.html', 'full4', '全真模擬卷④'), ('經紀法規_缺口補強卷五.html', 'full5', '缺口補強卷⑤'), ('經紀法規_模擬試題一_曾榮耀.html', 'tch1', '曾榮耀模擬試題一')],
 'val': [],
}
VQ = [('估價_綜合模擬卷一.html', 'mockc1', '估價綜合模擬卷一'), ('估價_綜合模擬卷二.html', 'mockc2', '估價綜合模擬卷二'), ('估價_綜合模擬卷三.html', 'mockc3', '估價綜合模擬卷三'),
      ('估價_綜合模擬卷四.html', 'mockc4', '估價綜合模擬卷四'), ('估價_綜合模擬卷五.html', 'mockc5', '估價綜合模擬卷五'), ('估價_自編補強卷.html', 'mockx1', '估價自編補強卷')]

for S in ['land', 'civ', 'jj', 'val']:
    mock, papers = [], {}
    for f, pid, name in P[S]:
        mock += varD(f, pid, name, S); papers[pid] = [name, f]
    if S == 'val':
        for f, pid, name in VQ:
            mock += vq(f, pid, name); papers[pid] = [name, f]
        mock += hs('估價_來勝模擬試題一.html'); papers['hs1'] = ['估價來勝模擬試題一', '估價_來勝模擬試題一.html']
        d = vdiag('估價_診斷卷一.html'); mock += d; papers['vdiag1'] = ['估價診斷卷①', '估價_診斷卷一.html']
        assert len(d) == 25, len(d)
    h = hist(S)
    for q in mock + h:
        assert len(q['opts']) == 4 and q['ok'] and all(0 <= k < 4 for k in q['ok']), q['id']
    ids = [q['id'] for q in mock + h]; assert len(ids) == len(set(ids)), S
    open(os.path.join(R, 'bx-pool-%s.js' % S), 'w', encoding='utf-8').write(
        '/* %s錯題複習卷題池（模擬卷 %d 題＋歷屆 %d 題）。由 tools/mockrec/pool.py 產生，不要手改。 */\nwindow.BXPOOL=%s;\n' %
        ({'land': '土地法', 'civ': '民法', 'jj': '經紀法規', 'val': '估價'}[S], len(mock), len(h),
         json.dumps(dict(S=S, papers=papers, q=mock + h), ensure_ascii=False, separators=(',', ':'))))
    print(S, 'mock', len(mock), 'hist', len(h), 'papers', len(papers), os.path.getsize(os.path.join(R, 'bx-pool-%s.js' % S)) // 1024, 'KB')
