# -*- coding: utf-8 -*-
"""民法解析結尾接上 bxm-links.js（刷題 5 頁、考題小卡 8 頁、法條解析練習＋tpl）。可重跑。"""
import io, os, glob
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
TAG = '<script src="bxm-exp.js"></script>'; ADD = TAG + '<script src="bxm-links.js"></script>'
P = [
 ('民法刷題練習_?篇.html', "  });\n  if(s){\n    const tr=mk('div','err-tag');",
  "  });\n  if(window.BXM_LINKS_HTML){const lk=BXM_LINKS_HTML(q.year+'-'+q.num);if(lk){const w=mk('div');w.innerHTML=lk;ex.appendChild(w)}}/*bxm-links*/\n  if(s){\n    const tr=mk('div','err-tag');"),
 ('民法*考題小卡.html', "expList.appendChild(div);\n  });",
  "expList.appendChild(div);\n  });\n  if(window.BXM_LINKS_HTML){const ym=String(c.year||'').match(/(\\d+)年第(\\d+)題/);const lk=ym?BXM_LINKS_HTML(ym[1]+'-'+ym[2]):'';if(lk){const w=document.createElement('div');w.innerHTML=lk;expList.appendChild(w)}}/*bxm-links*/"),
 ('民法*考題小卡.html', "expList.appendChild(div);});",
  "expList.appendChild(div);});if(window.BXM_LINKS_HTML){const ym=String(c.year||'').match(/(\\d+)年第(\\d+)題/);const lk=ym?BXM_LINKS_HTML(ym[1]+'-'+ym[2]):'';if(lk){const w=document.createElement('div');w.innerHTML=lk;expList.appendChild(w)}}/*bxm-links*/"),
 ('民法_法條解析練習.html', "document.getElementById('exs').innerHTML=eh;",
  "if(window.BXM_LINKS_HTML)eh+=BXM_LINKS_HTML(q.k);/*bxm-links*/\n  document.getElementById('exs').innerHTML=eh;"),
 ('tools/civ_quiz/tpl.html', "document.getElementById('exs').innerHTML=eh;",
  "if(window.BXM_LINKS_HTML)eh+=BXM_LINKS_HTML(q.k);/*bxm-links*/\n  document.getElementById('exs').innerHTML=eh;"),
]
done = {}
for pat, a, b in P:
    if b is None: continue
    for f in sorted(glob.glob(os.path.join(R, pat))):
        s = io.open(f, encoding='utf-8').read()
        if '/*bxm-links*/' not in s:
            if s.count(a) != 1: continue  # 另一種寫法（壓縮版）由下一條處理
            s = s.replace(a, b)
        if 'bxm-links.js' not in s and TAG in s: s = s.replace(TAG, ADD, 1)
        io.open(f, 'w', encoding='utf-8').write(s); done[os.path.basename(f)] = 'bxm-links.js' in s
print(len(done), sorted(k for k, v in done.items() if v)); bad = [f for f in done if '/*bxm-links*/' not in io.open(os.path.join(R, f) if os.path.exists(os.path.join(R, f)) else os.path.join(H, f), encoding='utf-8').read()]; print('未接上', bad); assert not bad
