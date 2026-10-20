# 產生《民法｜申論專練卷①》：以 民法_模擬試題一.html 為外殼，只留申論分頁、計時 75 分鐘
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)
from zl_data import E
src = open(os.path.join(ROOT, '民法_模擬試題一.html'), encoding='utf-8').read()
j = src.find('var D=')
d, end = json.JSONDecoder().raw_decode(src[j + 6:])
head, tail = src[:j], src[j + 6 + end:]
D = {"Q": [], "E": E, "timer": True}
page = head + 'var D=' + json.dumps(D, ensure_ascii=False) + tail
def rep(a, b, n=1):
    global page
    assert page.count(a) == n, (a[:60], page.count(a))
    page = page.replace(a, b)
rep('<title>', '<title>民法申論專練卷① ', 1) if '<title>' in page else None
page = re.sub(r'<title>[^<]*</title>', '<title>民法申論專練卷</title>', page, count=1)
page = re.sub(r'<h1>[^<]*</h1>', '<h1>民法申論專練卷①（自擬・限時 75 分鐘）</h1>', page, count=1)
page = re.sub(r'<div class="sub">.*?</div></div></header>', '<div class="sub">自擬專練卷（非官方考題）：申論 3 題、每題 25 分，限時 75 分鐘。補本站限時模擬卷沒練到的三個主題——共有（預測「高」）、行為能力＋詐欺＋瑕疵擔保（預測「高」，107 年後 7 屆沒考）、贈與＋歸扣與限定責任（選擇題 21 題的「其他各種之債」章原本沒有範文）。建議先寫在紙上，再展開擬答對照；依據見 <a href="民法_申論115出題預測.html">115 出題預測</a>。</div></div></header>', page, count=1, flags=re.S)
rep(',ID="civ1";', ',ID="civess1";')
rep('var ID="civ1";', 'var ID="civess1";')
rep('left=5400,', 'left=4500,')
# 申論分頁加計時器
rep("""function mkE(host){
 host.innerHTML='<div class="note">申論兩題共 50 分。建議先自己寫在紙上，再展開擬答（3 個版本）對照。</div>';""",
"""function mkE(host){
 host.innerHTML='<div class="score"><span>申論 3 題・共 75 分</span><span id="tm2">'+mm(left)+'</span><button id="tb2">開始計時</button><button id="rs2">重設</button></div><div class="note">每題約 25 分鐘。先寫在紙上，時間到再展開擬答（3 個版本）逐項對照採分點。</div>';
 var b=host.querySelector("#tb2"),t=host.querySelector("#tm2");
 if(tmr){b.textContent="暫停"}
 b.onclick=function(){if(tmr){clearInterval(tmr);tmr=null;b.textContent="繼續計時";return}
  b.textContent="暫停";tmr=setInterval(function(){left--;var e=document.getElementById("tm2");if(e)e.textContent=mm(Math.max(left,0));
   if(left<=0){clearInterval(tmr);tmr=null;if(e)e.textContent="時間到";var bb=document.getElementById("tb2");if(bb)bb.textContent="已結束"}},1000)};
 host.querySelector("#rs2").onclick=function(){if(tmr){clearInterval(tmr);tmr=null}left=4500;t.textContent=mm(left);b.textContent="開始計時"};""")
rep('var TABS=["作答"].concat(D.E?["申論"]:[]).concat(["結果"]);', 'var TABS=["申論"];')
rep('mkQ(qHost);go(0);', 'go(0);')
open(os.path.join(ROOT, '民法_申論專練卷.html'), 'w', encoding='utf-8').write(page)
print('ok', len(page))
