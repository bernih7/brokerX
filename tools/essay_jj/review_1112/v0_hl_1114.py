# -*- coding: utf-8 -*-
"""11-14 使用者：「考場版以及完整四段式…要一眼就看到重點能夠背誦…一次改完」。完整四段式（v0）全 75 張統一處理：
① 定義、涵攝、結論每段（p／li）標 1～2 處黃底粗體 <mark class="hl">（規則同考場版 hl_ev_1114：金額、法律效果、期限比例、應／須／不得義務句；不標條號）；
② 長段在「。」後遇「本題／故／惟／但／依同／依前」另起一行；結論段每句（。）、每個「；」答點各一行。
只動 v0 的 b1／b3／b4；「這題要背的條文」不動。可重跑（已處理的段落有 data-hl 標記略過）。"""
import os, re, sys
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(R, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
N = r'[\d,.一二三四五六七八九十百千萬兩]+'
PAT = [
    ('amt', re.compile(r'(?:新臺幣)?' + N + r'萬?元以上' + N + r'萬?元以下(?:之)?(?:罰鍰|罰金)?')),
    ('eff', re.compile(r'(?:應於加計利息後)?加倍返還(?:支付人)?|負連帶(?:損害)?賠償責任|其(?:定型化契約)?條款無效|條款無效|不生效力|仍構成契約之內容|不構成契約之內容|視為[^，。；：、（）<]{2,14}|廢止其(?:許可|經紀人員證書或證明)|應予申誡|停止執行業務|停止營業處分|推定顯失公平|禁止其營業|限期令停止、改正')),
    ('per', re.compile(r'[\d一二三四五六七八九十]+\s*(?:個月|日|年|小時|名)(?:內|以上|以下|後|為限)?[^，。；：（）<]{0,40}')),
    ('frac', re.compile(r'[一二三四五六七八九十\d]\s*(?:分之|/)\s*[一二三四五六七八九十\d](?:以上)?[^，。；：（）<]{0,40}')),
    ('must', re.compile(r'(?:應經|須經|應由|不得|始得|應先)[^，。；：（）<]{2,40}')),
]
def textmark(inner, k):
    # 只在「不在任何標籤內」的純文字段落上標
    toks = re.split(r'(<[^>]+>)', inner); depth = 0; used = 0; out = []
    for t in toks:
        if t.startswith('<'):
            if re.match(r'<(b|mark|a|span|strong|em|i|sup|sub)\b', t): depth += 1
            elif re.match(r'</(b|mark|a|span|strong|em|i|sup|sub)>', t): depth -= 1
            out.append(t); continue
        if depth or used >= k or not t.strip(): out.append(t); continue
        spans = []
        for kind, rx in PAT:
            for mm in rx.finditer(t):
                s, e = mm.span()
                if kind in ('per', 'frac', 'must'): s = max(t.rfind(c, 0, s) for c in '，。；：、（「') + 1
                seg = t[s:e].strip('，、 '); seg = re.sub(r'^(?:並|且|而|即|故|則|其)', '', seg)
                if len(seg) < 3 or len(seg) > 30 or re.search(r'第\s*\d+\s*條|[①-⑳]|§', seg): continue
                s = t.find(seg, s)
                if any(not (e2 <= s or s + len(seg) <= s2) for s2, e2 in spans): continue
                spans.append((s, s + len(seg))); break
            if len(spans) + used >= k: break
        for s, e in sorted(spans, reverse=True):
            t = t[:s] + '<mark class="hl">' + t[s:e] + '</mark>' + t[e:]
        used += len(spans); out.append(t)
    return ''.join(out)
def depth0_sub(inner, rx, rep):
    toks = re.split(r'(<[^>]+>)', inner); depth = 0; out = []
    for t in toks:
        if t.startswith('<'):
            if re.match(r'<(b|mark|a|span|strong|em|i)\b', t): depth += 1
            elif re.match(r'</(b|mark|a|span|strong|em|i)>', t): depth -= 1
            out.append(t)
        else: out.append(t if depth else rx.sub(rep, t))
    return ''.join(out)
BRK = re.compile(r'。(?=(?:本題|故|惟|但|依同|依前|又|另)[^。]{4,})')
def para(tag, attrs, inner, blk):
    if 'data-hl' in attrs: return None
    plain = re.sub(r'<[^>]+>', '', inner)
    if len(plain) < 8: return None
    k = 1 if blk == 'b1' else 2
    inner = textmark(inner, k)
    if len(plain) > 90: inner = depth0_sub(inner, BRK, '。<br>')
    if blk == 'b4' and len(plain) > 60:
        inner = depth0_sub(inner, re.compile(r'([；。])(?=[^<\s])'), r'\1<br>')
    return '<%s%s data-hl>%s</%s>' % (tag, attrs, inner, tag)
def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()
n = 0
for m in list(re.finditer(r'<details id="(es-[^"]+)"', h)):
    pass
pos = 0; out = []
for m in re.finditer(r'<div class="vp" data-v="0"', h):
    a = m.start(); b = div_end(h, a); v = h[a:b]
    for blk in ('b1', 'b3', 'b4'):
        i = v.find('<div class="blk %s"' % blk)
        if i < 0: continue
        j = div_end(v, i); seg = v[i:j]
        # 不動要背條文
        keep = []
        def hide(mm): keep.append(mm.group(0)); return '\x00%d\x00' % (len(keep) - 1)
        seg2 = re.sub(r'<div class="(?:btw|lawwrap)">.*?</details></div>', hide, seg, flags=re.S)
        def rp(mm):
            r = para(mm.group(1), mm.group(2), mm.group(3), blk)
            return mm.group(0) if r is None else r
        seg2 = re.sub(r'<(p|li)((?:\s[^>]*)?)>(.*?)</\1>', rp, seg2, flags=re.S)
        seg2 = re.sub(r'\x00(\d+)\x00', lambda mm: keep[int(mm.group(1))], seg2)
        v = v[:i] + seg2 + v[j:]
    out.append(h[pos:a]); out.append(v); pos = b; n += 1
out.append(h[pos:]); h = ''.join(out)
open(H, 'w', encoding='utf-8').write(h)
print('v0', n, 'mark.hl in v0 total', sum(x.count('<mark class="hl">') for x in re.findall(r'<div class="vp" data-v="0".*?<!--v0end-->', h, re.S)) if '<!--v0end-->' in h else '')
