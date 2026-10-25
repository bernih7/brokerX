# -*- coding: utf-8 -*-
"""申論頁版面整理 demo（獨立檔，正式頁不動）。
五項：①摘要列壓成一行、chips 收到展開後 ②拿掉左側色條 ③legend 縮短並修掉過時分頁名稱
④子分頁說明只在需要時顯示 ⑤加「只看未讀」切換。
"""
import io, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = os.path.join(ROOT, '經紀法規_備考指揮中心.html')
LIVE = '--live' in sys.argv
DST = SRC if LIVE else os.path.join(ROOT, 'demo', '經紀法規_申論版面_demo.html')
s = io.open(SRC, encoding='utf-8').read()

# ───── ② 拿掉左側色條，改細框＋左上篇別小標 ─────
o = 'details.essay-detail{border-left:5px solid var(--pk,var(--line))}'
assert s.count(o) == 1
s = s.replace(o, 'details.essay-detail{border-left:1px solid var(--line)}')
o = 'details.essay-detail.pred{border-style:solid;border-left-style:dashed}'
assert s.count(o) == 1
s = s.replace(o, 'details.essay-detail.pred{border-style:dashed}')

# ───── ③ legend 改寫（修掉過時的分頁名稱與色條說明） ─────
m = re.search(r'<div class="ess-leg">[\s\S]*?</div>', s)
assert m
s = s[:m.start()] + (
    '<div class="ess-leg"><b>★★★</b> 16 年反覆考・<b>★★</b> 高機率・<b>★</b> 低頻參考・'
    '<b>虛線框</b>＝預測題或補習班模擬卷（不是真題）。<br>'
    '每題三個分頁：<b>邏輯拆解</b>（第一次讀懂）→ <b>考場速寫</b>（含失分點）→ <b>完整四段式</b>。'
    '標題列只留級別，<b>關鍵詞展開後才出現</b>。</div>') + s[m.end():]

# ───── ⑤ 只看未讀 切換（加在進度列） ─────
o = '<button type="button" id="esNext">挑下一題未讀</button>'
assert s.count(o) == 1
s = s.replace(o, '<button type="button" id="esOnlyUnread">只看未讀</button>' + o)

CSS = '''
/* ── 版面整理 demo ── */
details.essay-detail{padding:2px 12px}
details.essay-detail>summary.es-sum{padding:9px 0}
/* ① 摘要列壓成一行：標題與級別同列，關鍵詞收到展開後 */
.es-top{align-items:center;gap:7px}
.essay-num{flex:none}
.es-t{flex:1;min-width:0;line-height:1.5;order:9}
.es-top{flex-wrap:wrap}
.es-top>.es-lv{flex:none;white-space:nowrap;margin-right:0}
@media(max-width:430px){.es-t{flex:1 0 100%;margin-top:2px}}
.es-meta{margin-top:0}
details.essay-detail:not([open])>summary .es-meta:empty,details.essay-detail:not([open])>summary .es-meta{display:none}
details.essay-detail[open]>summary .es-meta{display:flex}
details.essay-detail:not([open])>summary .es-meta .kc{display:none}
details.essay-detail[open]>summary .es-meta{margin-top:6px}
@media(min-width:520px){
  details.essay-detail:not([open])>summary .es-sum-row{display:flex;align-items:center;gap:8px}
}
/* ② 篇別改成左上小標籤 */
.pkdot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--pk,var(--line));display:inline-block}
details.essay-detail.pred .pkdot{box-shadow:inset 0 0 0 1px var(--surface)}
/* ④ 子分頁說明預設收起，由「？」開關 */
.ljd{display:none}
.ljp.showd .ljd{display:block}
.ljhelp{font:inherit;font-size:.72rem;font-weight:700;border:1px solid var(--line);background:var(--surface);color:var(--sub);border-radius:50%;width:20px;height:20px;cursor:pointer;flex:none;line-height:1}
.ljhelp.on{border-color:var(--pri);color:var(--pri)}
/* 進度列：數字一列、按鈕一列 */
.es-prog-row{display:block}
.es-prog-row b{display:flex;flex-wrap:wrap;gap:2px 10px;font-size:.86rem}
.es-prog-btns{display:flex;gap:8px;margin-top:8px}
.es-prog-btns button{flex:1;font:inherit;font-size:.8rem;font-weight:700;padding:6px 10px;border-radius:99px;border:1.5px solid var(--pri);background:var(--surface);color:var(--pri);cursor:pointer}
/* ⑤ 只看未讀 */
#esOnlyUnread.on{background:var(--pri);color:var(--on)}
.essay-detail.hid{display:none}
'''
i = s.rindex('</style>')
s = s[:i] + CSS + s[i:]

# 進度列：兩顆鈕包成自己一列
_o = '<button type="button" id="esOnlyUnread">只看未讀</button><button type="button" id="esNext">挑下一題未讀</button></div>'
assert s.count(_o) == 1, '找不到進度列按鈕'
s = s.replace(_o, '</div><div class="es-prog-btns"><button type="button" id="esOnlyUnread">只看未讀</button>'
                  '<button type="button" id="esNext">挑下一題未讀</button></div>')

JS = '''
<script>/* 版面整理 demo */
(function(){
var ES=[].slice.call(document.querySelectorAll(".essay-detail[id^=es-]"));
if(!ES.length)return;
/* ① 去掉「範文01★」尾端重複的星（級別膠囊已經有星） */
ES.forEach(function(d){
  var n=d.querySelector(".essay-num");
  if(n)n.textContent=n.textContent.replace(/[★\\s]+$/,"");
  /* ② 篇別小圓點 */
  var top=d.querySelector(".es-top");
  if(top&&!top.querySelector(".pkdot")){
    var s=document.createElement("span");s.className="pkdot";top.insertBefore(s,top.firstChild);
  }
  /* ① 級別移到標題同一列（原本自己佔一行） */
  var lv=d.querySelector(".es-meta > .es-lv");
  if(top&&lv&&n)top.insertBefore(lv,n.nextSibling);
});
/* ④ 每個排法面板加一顆「？」，只有按下才顯示說明；選擇記在 bxj-ljhelp */
var HK="bxj-ljhelp",open=false;
try{open=localStorage.getItem(HK)==="1"}catch(e){}
[].slice.call(document.querySelectorAll(".ljs")).forEach(function(bar){
  if(bar.querySelector(".ljhelp"))return;
  var b=document.createElement("button");
  b.type="button";b.className="ljhelp";b.textContent="？";b.title="顯示／隱藏這個排法的說明";
  bar.appendChild(b);
  b.addEventListener("click",function(ev){
    ev.preventDefault();ev.stopPropagation();
    open=!open;try{localStorage.setItem(HK,open?"1":"0")}catch(e){}
    sync();
  });
});
function sync(){
  [].slice.call(document.querySelectorAll(".ljp")).forEach(function(p){p.classList.toggle("showd",open)});
  [].slice.call(document.querySelectorAll(".ljhelp")).forEach(function(b){b.classList.toggle("on",open)});
}
sync();
/* ⑤ 只看未讀 */
var btn=document.getElementById("esOnlyUnread");
if(btn)btn.addEventListener("click",function(){
  var on=!btn.classList.contains("on");
  btn.classList.toggle("on",on);
  var R={};try{R=JSON.parse(localStorage.getItem("bxj-es-read")||"{}")||{}}catch(e){}
  ES.forEach(function(d){d.classList.toggle("hid",on&&!!R[d.id])});
  btn.textContent=on?"顯示全部":"只看未讀";
});
})();</script>
'''
i = s.rindex('</body>')
s = s[:i] + JS + s[i:]

if not LIVE:
    s = s.replace('<title>', '<title>〔版面 demo〕', 1)
    BANNER = ('<div style="position:sticky;top:0;z-index:99;background:#8A5517;color:#fff;'
              'padding:7px 12px;font-size:13px;line-height:1.6">'
              '〔版面整理 <b>demo</b>〕正式頁未動。改了五項：①標題列壓成一行、關鍵詞展開後才出現 '
              '②拿掉左側色條改小圓點 ③說明縮短並修掉過時的分頁名稱 ④排法說明收到「？」裡 '
              '⑤進度列加「只看未讀」。</div>')
    s = s.replace('<body>', '<body>' + BANNER, 1)

os.makedirs(os.path.dirname(DST), exist_ok=True)
io.open(DST, 'w', encoding='utf-8').write(s)
print('已產生', os.path.relpath(DST, ROOT), len(s) // 1024, 'KB')
