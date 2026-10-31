# -*- coding: utf-8 -*-
"""全站深淺色：讓沒存過偏好的頁跟隨系統設定（方案 A）。

bug：開機腳本在沒存過偏好時把 data-theme 寫死成 "light"，
而深色 CSS 的條件是 :root:not([data-theme="light"])，於是系統深色被擋掉。
修法：沒存過偏好就「不要寫 data-theme」，交給 prefers-color-scheme；
按過切換鈕才寫入 localStorage('bx-theme')，之後以使用者的選擇為準。
切換鈕與按鈕文字的判斷一律改成「有屬性看屬性，沒屬性看系統」。

安全前置檢查：淺色色票必須定義在裸 :root 上。若某頁只在 [data-theme="light"]
定義淺色變數，拿掉屬性會讓它沒有顏色——那種頁會被跳過並列出來。

可重複執行（替換後的字串不會再被配對到）。
"""
import io, os, glob, re, sys, collections

SYS = '((window.matchMedia&&matchMedia("(prefers-color-scheme:dark)").matches)?"dark":"light")'

PAIRS = [
 # (說明, 舊字串, 新字串)
 ('A 開機寫死（雙引號）',
  'document.documentElement.setAttribute("data-theme",s||"light")',
  'if(s)document.documentElement.setAttribute("data-theme",s)'),
 ('A2 開機寫死（單引號）',
  "document.documentElement.setAttribute('data-theme',s||'light')",
  "if(s)document.documentElement.setAttribute('data-theme',s)"),
 ('C 開機寫死＋replace',
  'document.documentElement.setAttribute("data-theme",(s||"light").replace(/"/g,""))',
  'if(s)document.documentElement.setAttribute("data-theme",s.replace(/"/g,""))'),
 ('B setTh(sv0||"light")', 'setTh(sv0||"light")', 'setTh(sv0)'),
 ("E setTh(bx||ll||'light')",
  "setTh(lsG('bx-theme')||lsG('ll_theme')||'light')",
  "setTh(lsG('bx-theme')||lsG('ll_theme'))"),
 ("D setTh(bx||'light')", "setTh(lsG('bx-theme')||'light')", "setTh(lsG('bx-theme'))"),
 ('G toggleTheme 讀屬性預設 light',
  'c=h.getAttribute("data-theme")||"light"',
  'c=h.getAttribute("data-theme")||' + SYS),
 ('H ub() 初始讀屬性預設 light',
  'ub(document.documentElement.getAttribute("data-theme")||"light")',
  'ub(document.documentElement.getAttribute("data-theme")||' + SYS + ')'),
 # F：估價 113 真題頁自成一套，load 時還會把 light 寫進 localStorage
 ('F 估價113 getTheme',
  'const getTheme = ()=>{ try{return localStorage.getItem("bx-theme")||"light";}catch(e){return "light";} };',
  'const getTheme = ()=>{ try{return localStorage.getItem("bx-theme");}catch(e){return null;} };\n'
  'const curDark = ()=>{ var t=getTheme(); return t?t==="dark":(window.matchMedia&&matchMedia("(prefers-color-scheme:dark)").matches); };'),
 ('F2 估價113 applyTheme',
  'const applyTheme = t=>{ document.documentElement.setAttribute("data-theme",t); tt.textContent=t==="dark"?"☀️":"🌙"; try{localStorage.setItem("bx-theme",t);}catch(e){} };',
  'const applyTheme = t=>{ if(t){document.documentElement.setAttribute("data-theme",t); try{localStorage.setItem("bx-theme",t);}catch(e){}} tt.textContent=curDark()?"☀️":"🌙"; };'),
 ('F3 估價113 toggle',
  'tt.onclick = ()=>applyTheme(getTheme()==="dark"?"light":"dark");',
  'tt.onclick = ()=>applyTheme(curDark()?"light":"dark");'),
]

# 安全前置檢查（不綁特定變數名）：
# ① 裸 :root{...} 裡要有自訂屬性（淺色色票的所在）
# ② 要有 @media (prefers-color-scheme...)，拿掉屬性後深色才接得上
ROOT_VARS = re.compile(r':root\s*\{[^}]*--[\w-]+\s*:', re.S)
HAS_MEDIA = re.compile(r'@media\s*\([^)]*prefers-color-scheme')

def main():
    dry = '--write' not in sys.argv
    tot = collections.Counter(); pages = collections.Counter(); skipped = []
    for p in sorted(glob.glob('*.html')):
        s = io.open(p, encoding='utf-8').read()
        if not any(old in s for _, old, _ in PAIRS):
            continue
        # 前置檢查
        if '--' in s and not ROOT_VARS.search(s):
            skipped.append((p, '裸 :root 沒有自訂屬性，淺色色票位置不明'))
            continue
        if not HAS_MEDIA.search(s):
            skipped.append((p, '沒有 prefers-color-scheme media query，拿掉屬性接不到深色'))
            continue
        out = s; hits = []
        for name, old, new in PAIRS:
            n = out.count(old)
            if n:
                out = out.replace(old, new)
                tot[name] += n; hits.append('%s×%d' % (name.split()[0], n))
        if out != s:
            pages[p] = 1
            if not dry:
                io.open(p, 'w', encoding='utf-8').write(out)
            print('  %-44s %s' % (p[:42], ' '.join(hits)))
    print('\n%s：%d 頁' % ('已改' if not dry else '試跑（未寫檔）', len(pages)))
    for k, _, _ in PAIRS:
        if tot[k]: print('   %-32s %d 處' % (k, tot[k]))
    if skipped:
        print('\n⚠️ 跳過（色票結構不安全，需人工看）：')
        for p, why in skipped: print('   %-44s %s' % (p[:42], why))
    def subj(p):
        for x in ('經紀法規', '民法', '土地法', '估價', '備考'):
            if p.startswith(x): return x
        return '其他'
    print('\n分科：', dict(collections.Counter(subj(p) for p in pages)))

if __name__ == '__main__':
    main()


# ── 第二階段：切換鈕與按鈕文字也要「有屬性看屬性，沒屬性看系統」 ──
# 這些寫法不會讓畫面壞掉（load 時不寫屬性），但系統深色時第一次按鈕會變成空按
# （它以為現在是 light，於是切到 dark，畫面沒變化）。
RX_DARK = re.compile(r"""([\w$][\w$.]*)\.getAttribute\((['"])data-theme\2\)\s*={2,3}\s*(['"])dark\3""")
SETT_LIGHT = (
  """setT(sv?JSON.parse('"'+sv.replace(/"/g,'')+'"'):'light')""",
  """setT(sv?JSON.parse('"'+sv.replace(/"/g,'')+'"'):null)""")

def eff(m):
    recv, q, q2 = m.group(1), m.group(2), m.group(3)
    sysq = ('((window.matchMedia&&matchMedia(%s(prefers-color-scheme:dark)%s).matches)?%sdark%s:%slight%s)'
            % (q, q, q, q, q, q))
    return ('(%s.getAttribute(%sdata-theme%s)||%s)===%sdark%s'
            % (recv, q, q, sysq, q2, q2))

def stage2():
    dry = '--write' not in sys.argv
    pages = 0; n1 = n2 = 0
    for p in sorted(glob.glob('*.html')):
        s = io.open(p, encoding='utf-8').read()
        out, k = RX_DARK.subn(eff, s)
        if SETT_LIGHT[0] in out:
            out = out.replace(*SETT_LIGHT); n2 += 1
        if out != s:
            n1 += k; pages += 1
            if not dry: io.open(p, 'w', encoding='utf-8').write(out)
            print('  %-44s 切換判斷×%d' % (p[:42], k))
    print('\n第二階段%s：%d 頁，切換判斷 %d 處，setT 預設 %d 處'
          % ('已改' if not dry else '試跑', pages, n1, n2))

if __name__ == '__main__' and '--stage2' in sys.argv:
    stage2()
