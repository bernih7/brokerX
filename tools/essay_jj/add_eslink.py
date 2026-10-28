# -*- coding: utf-8 -*-
"""施工單第 6 項：申論卡加「📚 這題該讀哪幾頁」。

每張卡 2–3 條連結，連到站內既有的整理頁（必要時帶錨點）。
執行前會逐條檢查「檔案存在＋錨點 id 存在」，有一條失效就中止，不寫檔。
可重複執行：以 <style id="eslink-css"> … </script><!--/eslink--> 為邊界整段換掉，
卡內舊的 .eslink 區塊也會先移除。
"""
import io, os, re, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
HUB = os.path.join(ROOT, '經紀法規_備考指揮中心.html')

P = {  # 短代號 → (檔名, 顯示名)
 'proc':  ('經紀法規_程序總整理.html', '程序總整理'),
 'pen':   ('經紀法規_罰則總整理.html', '罰則總整理'),
 'fine':  ('經紀法規_罰鍰與處分一覽表.html', '罰鍰與處分一覽表'),
 'four':  ('經紀法規_四法罰則總比較.html', '四法罰則總比較'),
 'num':   ('經紀法規_數字速查.html', '數字速查'),
 'mix':   ('經紀法規_易混淆概念並排.html', '易混淆概念並排'),
 'color': ('經紀法規概要_彩色重點速記.html', '彩色重點速記'),
 'fill':  ('經紀法規_定義填空練習.html', '定義填空練習'),
 'must':  ('經紀法規_應記載不得記載總整理.html', '應記載／不得記載總整理'),
 'con':   ('經紀法規_定型化契約專區.html', '定型化契約專區'),
 'void':  ('經紀法規_定型化契約_無效vs不構成.html', '定型化契約：無效 vs 不構成'),
 'apt':   ('經紀法規_公寓大廈條例罰則整理.html', '公寓大廈條例罰則整理'),
 'fair':  ('經紀法規_公平法獨占聯合結合整理.html', '公平法：獨占・聯合・結合'),
 'fhpen': ('經紀法規_公平法消保法罰則整理.html', '公平法・消保法罰則整理'),
}
# 帶錨點的捷徑：代號 → (短代號, 錨點 id, 顯示名)
A = {
 'proc1': ('proc', 'p1', '程序總整理 ① 經紀業生命週期'),
 'proc2': ('proc', 'p2', '程序總整理 ② 經紀人員'),
 'proc3': ('proc', 'p3', '程序總整理 ③ 區分所有權人會議'),
 'proc4': ('proc', 'p4', '程序總整理 ④ 檢舉、調處與罰鍰不繳'),
}

DEF = {  # 篇別預設
 'pk-a': ['proc1', 'pen', 'color'],
 'pk-c': ['must', 'fill'],
 'pk-d': ['con', 'void', 'must'],
 'pk-e': ['proc3', 'apt', 'num'],
 'pk-g': ['fair', 'fhpen', 'num'],
 'pk-h': ['fhpen', 'void', 'num'],
}

OVR = {  # 單張卡指定
 'es-fw01': ['fair', 'pen'],
 'es-fw04': ['color', 'pen', 'mix'],
 'es-fw06': ['pen', 'mix', 'fine'],
 'es-fw09': ['proc1', 'num'],
 'es-fw11': ['proc2', 'pen'],
 'es-fw14': ['fill', 'pen'],
 'es-fw15': ['proc1', 'num', 'pen'],
 'es-fw16': ['fair', 'pen'],
 'es-fw17': ['fair', 'fhpen'],
 'es-fw18': ['fill', 'color'],
 'es-fw23': ['pen', 'mix', 'fine'],
 'es-fw25': ['proc1', 'num', 'fine'],
 'es-fw27': ['pen', 'mix'],
 'es-fw30': ['color', 'pen'],
 'es-mk1':  ['fill', 'pen', 'four'],
 'es-a1':   ['proc2', 'num'],
 'es-a2':   ['proc1', 'num', 'pen'],
 'es-a3':   ['proc2', 'pen'],
 'es-a4':   ['num', 'pen'],
 'es-a5':   ['num', 'mix'],
 'es-a6':   ['pen', 'four'],
 'es-a7':   ['pen', 'color'],
 'es-a8':   ['proc4', 'pen'],
 'es-a9':   ['proc1', 'num', 'fine'],
 'es-fw03': ['must', 'color'],
 'es-fw19': ['must', 'fill'],
 'es-c1':   ['must', 'con'],
 'es-c2':   ['must', 'void'],
 'es-fw21': ['con', 'void', 'must'],
 'es-d1':   ['con', 'void'],
 'es-d2':   ['con', 'must'],
 'es-d3':   ['void', 'must'],
 'es-fw05': ['proc4', 'apt'],
 'es-fw08': ['proc3', 'num'],
 'es-fw13': ['must', 'fill'],
 'es-fw20': ['must', 'fill'],
 'es-fw22': ['proc4', 'apt'],
 'es-fw28': ['proc3', 'num'],
 'es-fw31': ['proc3', 'num'],
 'es-e4':   ['proc4', 'apt'],
 'es-e5':   ['must', 'fill'],
 'es-e6':   ['apt', 'num'],
 'es-fw10': ['fair', 'num'],
 'es-fw12': ['fair', 'fhpen'],
 'es-fw26': ['fair', 'fhpen'],
 'es-g5':   ['fair', 'fhpen'],
 'es-g7':   ['fair', 'void'],
 'es-fw07': ['proc4', 'fhpen'],
 'es-fw32': ['proc4', 'fhpen'],
 'es-fw29': ['fhpen', 'fair'],
 'es-mk2':  ['must', 'void'],
 'es-h2':   ['void', 'must'],
 'es-e11':  ['apt', 'proc4', 'must'],
}

CSS = """<style id="eslink-css">
.eslink{margin:8px 0 0;padding-top:8px;border-top:1px dashed var(--line);font-size:.8rem;color:var(--sub)}
.eslink b{color:var(--ink);font-weight:700}
.eslink .els{display:inline-flex;flex-wrap:wrap;gap:6px;margin-left:6px;vertical-align:middle}
.eslink a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 10px;
  background:var(--surface);color:var(--pri);text-decoration:none;font-size:.78rem;line-height:1.5}
.eslink a:hover{border-color:var(--pri);background:var(--pri-soft)}
@media(max-width:480px){.eslink .els{margin-left:0;margin-top:6px;display:flex}}
</style>"""


def build_links():
    s = io.open(HUB, encoding='utf-8').read()
    cards = re.findall(r'<details id="(es-[^"]+)" class="essay-detail([^"]*)">', s)
    out = {}
    for cid, cls in cards:
        pk = next((c for c in cls.split() if c.startswith('pk-')), None)
        keys = OVR.get(cid) or DEF.get(pk) or []
        if not keys:
            print('✗ %s 沒有對應頁（篇別 %s）' % (cid, pk)); sys.exit(1)
        out[cid] = keys
    return s, out


def resolve(key):
    if key in A:
        short, anc, name = A[key]
        return P[short][0] + '#' + anc, name, P[short][0], anc
    f, name = P[key]
    return f, name, f, None


def check(keys_used):
    bad = []
    cache = {}
    for k in sorted(keys_used):
        href, name, f, anc = resolve(k)
        path = os.path.join(ROOT, f)
        if not os.path.exists(path):
            bad.append('%s：檔案不存在 %s' % (k, f)); continue
        if anc:
            if f not in cache:
                cache[f] = io.open(path, encoding='utf-8').read()
            if ('id="%s"' % anc) not in cache[f]:
                bad.append('%s：%s 裡沒有 id="%s"' % (k, f, anc))
    return bad


def main():
    s, mp = build_links()
    used = set()
    for v in mp.values():
        used.update(v)
    bad = check(used)
    if bad:
        print('✗ 連結檢查沒過，未寫檔：')
        for b in bad:
            print('  ', b)
        sys.exit(1)
    # 先移除舊區塊
    s = re.sub(r'<div class="eslink">.*?</div>(?=<label class="esdone")', '', s, flags=re.S)
    s = re.sub(r'<style id="eslink-css">.*?<!--/eslink-->', '', s, flags=re.S)
    n = 0
    for cid, keys in mp.items():
        links = ''.join('<a href="%s">%s</a>' % resolve(k)[:2] for k in keys)
        blk = '<div class="eslink"><b>📚 這題該讀哪幾頁</b><span class="els">%s</span></div>' % links
        a = '<details id="%s" class="essay-detail' % cid
        i = s.index(a)
        j = s.index('<label class="esdone"', i)
        s = s[:j] + blk + s[j:]
        n += 1
    i = s.rindex('</body>')
    s = s[:i] + CSS + '<!--/eslink-->\n' + s[i:]
    io.open(HUB, 'w', encoding='utf-8').write(s)
    print('已寫入「這題該讀哪幾頁」：%d 張卡、%d 個不重複連結，全數檢查通過' % (n, len(used)))


if __name__ == '__main__':
    main()
