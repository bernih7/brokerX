# -*- coding: utf-8 -*-
"""11-14 續：完整四段式原本以 <b> 標的數字、門檻、效果，改成黃底粗體 <mark class="hl">（與考場版、民法一致），
只轉段中短重點（2～16 字且含數字／比例／期限或法律效果字），段首小標 <b>（一）…</b> 不動；長段（>150 字）在「；」後另起一行。可重跑。"""
import os, re
R = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
H = os.path.join(R, '經紀法規_備考指揮中心.html'); h = open(H, encoding='utf-8').read()
KEY = re.compile(r'[\d一二三四五六七八九十兩]+\s*(?:個月|日|年|小時|名|人|倍|萬|元|%)|分之|/\d|以上|以下|過半數|半數|無效|不生效力|視為|連帶|申誡|停止|廢止|撤銷|不得|應經|須經|推定|加倍|全體|禁止|罰鍰|罰金')
def div_end(s, a):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[a:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return a + m.end()
n = 0; pos = 0; out = []
for m in re.finditer(r'<div class="vp" data-v="0"', h):
    a = m.start(); b = div_end(h, a); v = h[a:b]
    for blk in ('b3', 'b4'):
        i = v.find('<div class="blk %s"' % blk)
        if i < 0: continue
        j = div_end(v, i); seg = v[i:j]
        def para(mm):
            global n
            tag, attrs, inner = mm.group(1), mm.group(2), mm.group(3)
            if 'data-b2m' in attrs: return mm.group(0)
            lead = re.match(r'\s*<b>[^<]{0,30}</b>', inner); lead_s = lead.group(0) if lead else ''
            rest = inner[len(lead_s):]
            def cv(bm):
                global n
                t = bm.group(1)
                if 2 <= len(t) <= 16 and KEY.search(t): n += 1; return '<mark class="hl">' + t + '</mark>'
                return bm.group(0)
            rest = re.sub(r'<b>([^<]{1,40})</b>', cv, rest)
            plain = re.sub(r'<[^>]+>', '', inner)
            if len(plain) > 150 and tag == 'p':
                rest = re.sub(r'；(?=[^<\s])', '；<br>', rest)
            return '<%s%s data-b2m>%s%s</%s>' % (tag, attrs, lead_s, rest, tag)
        keep = []
        seg2 = re.sub(r'<div class="(?:btw|lawwrap)">.*?</details></div>', lambda x: (keep.append(x.group(0)), '\x00%d\x00' % (len(keep) - 1))[1], seg, flags=re.S)
        seg2 = re.sub(r'<(p|li)((?:\s[^>]*)?)>(.*?)</\1>', para, seg2, flags=re.S)
        seg2 = re.sub(r'\x00(\d+)\x00', lambda x: keep[int(x.group(1))], seg2)
        v = v[:i] + seg2 + v[j:]
    out.append(h[pos:a]); out.append(v); pos = b
out.append(h[pos:]); open(H, 'w', encoding='utf-8').write(''.join(out)); print('轉換', n)
