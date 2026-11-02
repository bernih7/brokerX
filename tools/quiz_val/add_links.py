#!/usr/bin/env python3
"""把 bxv-links.js 的「相關工具」連結列接到估價考題解析結尾（比照土地法 bxl-links.js）。

可重複執行：已接過的檔案會略過（以 BXV_LINKS_HTML / bxv-links.js 字樣判斷）。
  python3 tools/quiz_val/add_links.py            # 套用到站台根目錄
  python3 tools/quiz_val/add_links.py --root DIR # 套用到另一份複本（試跑用）
  python3 tools/quiz_val/add_links.py --check    # 只核對 bxv-links.js 每個連結的檔案與錨點 id 是否存在

會改：
  ① 估價刷題練習_*.html（16 支章節頁＋113 真題頁）：解析結尾接連結列，並在 bxv-use.js 後加 <script src="bxv-links.js">
  ② bxv-topic-qa.js：考古題作答面板解析結尾接連結列；boot 時先載 bxv-links.js
  ③ bxv-topic-q.js：考古題清單面板解析（展開後）結尾接連結列；載入時先載 bxv-links.js
每處替換都用確切字串，找不到或不唯一就 assert 失敗、整批不寫入。
"""
import argparse, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEF_ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

TAG = '<script src="bxv-links.js"></script>'
USE = '<script src="bxv-use.js"></script>'

# ── 章節頁（標準版：explainHtml 字串累加） ──
STD_OLD = "      explainHtml += '</div>' + (!a.correct && window.bxvCard ? bxvMore(0) : '');\n"
STD_NEW = STD_OLD + (
    "      if(window.BXV_LINKS_HTML){const _so=it.q+(it.opts||[]).join('');"
    "explainHtml+=BXV_LINKS_HTML(it.cat,_so,_so+(it.explains||[]).join(''));}\n")

# ── I2J1（模板字串版） ──
I2_OLD = "    </div>${!ans.correct&&window.bxvCard?bxvMore(0):''}`:''}"
I2_NEW = ("    </div>${!ans.correct&&window.bxvCard?bxvMore(0):''}"
          "${window.BXV_LINKS_HTML?BXV_LINKS_HTML(it.cat,it.q+(it.opts||[]).join(''),"
          "it.q+(it.opts||[]).join('')+(it.explains||[]).join('')):''}`:''}")

# ── 113 真題頁（DOM 版） ──
T113_OLD = "      } else card.appendChild(eb);\n"
T113_NEW = T113_OLD + (
    "      if(window.BXV_LINKS_HTML){ const _so = item.q + (item.opts||[]).join('');"
    " const _lk = BXV_LINKS_HTML(item.cat, _so, _so + (item.explains||[]).join(''));"
    " if(_lk) card.insertAdjacentHTML(\"beforeend\", _lk); }\n")

# ── bxv-topic-qa.js ──
QA_OLD1 = "          }).join('') + '</div>' + (_wr ? bxvMore(0) : '');\n"
QA_NEW1 = QA_OLD1 + (
    "          if (window.BXV_LINKS_HTML) h += BXV_LINKS_HTML(q.ch, q.stem + q.opt.join(''),"
    " q.stem + q.opt.join('') + (q.exp || []).join(''));\n")
QA_OLD2 = ("    if (window.BXV_QUIZ) { init(); return; }\n"
           "    var s = document.createElement('script'); s.src = 'bxv-quiz-data.js'; s.onload = init; document.head.appendChild(s);\n")
QA_NEW2 = ("    function data() {\n"
           "      if (window.BXV_QUIZ) { init(); return; }\n"
           "      var s = document.createElement('script'); s.src = 'bxv-quiz-data.js'; s.onload = init; document.head.appendChild(s);\n"
           "    }\n"
           "    if (window.BXV_LINKS_HTML) { data(); return; }\n"
           "    var s0 = document.createElement('script'); s0.src = 'bxv-links.js'; s0.onload = s0.onerror = data; document.head.appendChild(s0);\n")

# ── bxv-topic-q.js ──
TQ_OLD1 = "    var nt=q.note?'<div class=\"nt\">⚠️ '+esc(q.note)+'</div>':'';\n"
TQ_NEW1 = TQ_OLD1 + (
    "    if(window.BXV_LINKS_HTML)nt+=BXV_LINKS_HTML(q.ch,q.q+q.opts.join(''),q.q+q.opts.join('')+(q.exps||[]).join(''));\n")
TQ_OLD2 = ('if(window.BXV_QUIZ)init();else{var s=document.createElement("script");s.src="bxv-quiz-data.js";'
           's.onload=init;document.head.appendChild(s)}\n')
TQ_NEW2 = ('function data(){if(window.BXV_QUIZ)init();else{var s=document.createElement("script");s.src="bxv-quiz-data.js";'
           's.onload=init;document.head.appendChild(s)}}\n'
           'if(window.BXV_LINKS_HTML)data();else{var s0=document.createElement("script");s0.src="bxv-links.js";'
           's0.onload=s0.onerror=data;document.head.appendChild(s0)}\n')


def rep(s, old, new, name):
    n = s.count(old)
    assert n == 1, '%s：找到 %d 處（應為 1）：%r' % (name, n, old[:80])
    return s.replace(old, new)


def check_links(root):
    """核對 bxv-links.js 裡每個 [標題, 檔案#錨點]：檔案存在、錨點 id 存在於該檔。回傳核對過的錨點數。"""
    js = open(os.path.join(root, 'bxv-links.js'), encoding='utf-8').read()
    consts = dict(re.findall(r"(\b[A-Z0-9]+) = '([^']+\.html)'", js))
    assert consts, '讀不到 bxv-links.js 的檔名常數'
    pairs = set()
    for c, a in re.findall(r"\b([A-Z0-9]+)(?: \+ '#([^']+)')?\]", js):
        if c in consts:
            pairs.add((consts[c], a))
    bad, nanc = [], 0
    for f, a in sorted(pairs):
        p = os.path.join(root, f)
        if not os.path.exists(p):
            bad.append('缺檔 ' + f); continue
        if a:
            nanc += 1
            if not re.search(r'\bid="%s"' % re.escape(a), open(p, encoding='utf-8').read()):
                bad.append('缺錨點 %s#%s' % (f, a))
    assert not bad, '連結核對失敗：\n  ' + '\n  '.join(bad)
    print('連結核對：%d 個目標（%d 個帶錨點）全部存在' % (len(pairs), nanc))
    return nanc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=DEF_ROOT)
    ap.add_argument('--check', action='store_true')
    o = ap.parse_args()
    root = os.path.abspath(o.root)
    check_links(root)
    if o.check:
        return

    out = {}
    pages = sorted(glob.glob(os.path.join(root, '估價刷題練習_*.html')))
    assert len(pages) == 17, '估價刷題練習_*.html 應有 17 支（16 章＋113），實際 %d' % len(pages)
    for p in pages:
        s = open(p, encoding='utf-8').read(); s0 = s
        name = os.path.basename(p)
        if 'BXV_LINKS_HTML' not in s:
            if name == '估價刷題練習_I2J1.html':
                s = rep(s, I2_OLD, I2_NEW, name)
            elif name == '估價刷題練習_113真題.html':
                s = rep(s, T113_OLD, T113_NEW, name)
            else:
                s = rep(s, STD_OLD, STD_NEW, name)
        if TAG not in s:
            s = rep(s, USE, USE + TAG, name)
        if s != s0:
            out[p] = s

    p = os.path.join(root, 'bxv-topic-qa.js')
    s = open(p, encoding='utf-8').read(); s0 = s
    if 'BXV_LINKS_HTML(q.ch' not in s:
        s = rep(s, QA_OLD1, QA_NEW1, 'bxv-topic-qa.js 解析')
    if "'bxv-links.js'" not in s:
        s = rep(s, QA_OLD2, QA_NEW2, 'bxv-topic-qa.js boot')
    if s != s0:
        out[p] = s

    p = os.path.join(root, 'bxv-topic-q.js')
    s = open(p, encoding='utf-8').read(); s0 = s
    if 'BXV_LINKS_HTML(q.ch' not in s:
        s = rep(s, TQ_OLD1, TQ_NEW1, 'bxv-topic-q.js 解析')
    if '"bxv-links.js"' not in s:
        s = rep(s, TQ_OLD2, TQ_NEW2, 'bxv-topic-q.js 載入')
    if s != s0:
        out[p] = s

    for p, s in out.items():
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print('已改', os.path.relpath(p, root))
    if not out:
        print('都已接過，沒有變更')


if __name__ == '__main__':
    main()
