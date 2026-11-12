# -*- coding: utf-8 -*-
"""四科模擬卷接上 bx-mockrec.js：每題熟練度（錯題複習卷用）＋每份卷歷次紀錄。可重跑（已改過的檔略過）。"""
import os, re, sys
R = os.path.join(os.path.dirname(__file__), '..', '..')
TAG = '<script src="bx-mockrec.js"></script>'

def rd(f): return open(os.path.join(R, f), encoding='utf-8').read()
def wr(f, s): open(os.path.join(R, f), 'w', encoding='utf-8').write(s)
def rep(s, a, b, f):
    assert s.count(a) == 1, (f, a[:60], s.count(a)); return s.replace(a, b)
def addtag(s):
    i = s.index('</head>'); return s[:i] + TAG + '\n' + s[i:]

SEC = 'function(n){var q=D.Q.filter(function(x){return x.n==n})[0];return q&&q.sec}'

# ① var D 版型（土地法來勝、民法三卷、經紀法規五卷）：有 ID、cl、#rs、mkR
T1 = {'民法_來勝模擬試題一.html': 'civ', '民法_模擬試題一.html': 'civ', '民法_模擬試題二.html': 'civ',
      '經紀法規_診斷卷一.html': 'jj', '經紀法規_高頻考點卷二.html': 'jj', '經紀法規_混淆對比卷三.html': 'jj',
      '經紀法規_全真模擬卷四.html': 'jj', '經紀法規_缺口補強卷五.html': 'jj'}
def t1(f, S):
    s = rd(f)
    s = rep(s, 'st[qq.n]=ok;', 'st[qq.n]=ok;try{BXMR.ans("%s",ID,qq.n,ok)}catch(e){}' % S, f)
    s = re.sub(r'cl\[qq\.n\]=k;', 'cl[qq.n]=k;try{BXMR.cls(ID,qq.n,k)}catch(e){}', s, count=1)
    s = rep(s, 'qHost.querySelector("#rs").onclick=function(){', 'qHost.querySelector("#rs").onclick=function(){try{BXMR.reset(ID,D.Q.length)}catch(e){}', f)
    # 開頁：上次的作答先存成一筆；結果分頁加歷次紀錄
    m = list(re.finditer(r'mkQ\(qHost\);', s))[-1]
    s = s[:m.start()] + 'try{BXMR.boot(ID,D.Q.length)}catch(e){}(function(){var f0=mkR;mkR=function(h){f0(h);try{BXMR.mount("%s",ID,h,D.Q.length,%s)}catch(e){}}})();' % (S, SEC) + s[m.start():]
    return addtag(s)

# ② 土地法診斷卷①②：已有自己的歷次紀錄，只記每題熟練度
def landdiag(f):
    s = rd(f)
    s = rep(s, 'st[qq.n]=ok;pk[qq.n]=ii;', 'st[qq.n]=ok;pk[qq.n]=ii;if(!window._bxRestoring)try{BXMR.rec("land",ID+"-"+qq.n,ok)}catch(e){}', f)
    # 開頁還原時是模擬點擊，不能重複記
    s = rep(s, 'D.Q.forEach(function(q){var i=s.pk[q.n];', 'window._bxRestoring=1;D.Q.forEach(function(q){var i=s.pk[q.n];', f)
    s = rep(s, "if(x)x.onclick()}})}catch(e){}})();go(0);", "if(x)x.onclick()}});window._bxRestoring=0}catch(e){window._bxRestoring=0}})();go(0);", f)
    s = rep(s, '<div class="qn">歷次紀錄（按「重做」時自動保存）</div>', '<div class="qn">歷次紀錄（按「重做」時自動保存）</div><div class="note"><a href="土地法_錯題複習卷.html">▶ 去土地法錯題複習卷（錯題＋新題混合；答錯過的要連續答對 3 次才放過）</a></div>', f)
    return addtag(s)

# ②b 土地法來勝兩卷：練習／考試兩種模式、result() 畫在 p4
def ll(f):
    s = rd(f)
    s = rep(s, 'if(mode==="practice"){revealed[q.n]=true;save();', 'if(mode==="practice"){revealed[q.n]=true;try{BXMR.ans("land",ID,q.n,okq(q,L[i]))}catch(e){}save();', f)
    s = rep(s, 'function finish(){if(tmr){clearInterval(tmr);tmr=null}finished=true;', 'function finish(){if(tmr){clearInterval(tmr);tmr=null}if(mode==="exam")try{D.Q.forEach(function(q){if(ans[q.n]!==undefined)BXMR.ans("land",ID,q.n,okq(q,ans[q.n]))})}catch(e){}finished=true;', f)
    s = rep(s, 'function reset(){ans={};', 'function reset(){try{BXMR.reset(ID,25)}catch(e){}ans={};', f)
    s = rep(s, 'bt.onclick=function(){errs[q.n]=bt.dataset.t;', 'bt.onclick=function(){errs[q.n]=bt.dataset.t;try{BXMR.cls(ID,q.n,bt.dataset.t)}catch(e){}', f)
    m = list(re.finditer(r'\nbuild\(\);\n</script>', s))[-1]
    s = s[:m.start()] + '\ntry{BXMR.boot(ID,25)}catch(e){}(function(){var f0=result;result=function(){f0();try{BXMR.mount("land",ID,$("p4"),25,%s)}catch(e){}}})();' % SEC + s[m.start():]
    return addtag(s)

# ③ 經紀法規曾榮耀卷：沒有 ID／cl／結果分頁
def tch(f):
    s = rd(f)
    s = rep(s, 'st[qq.n]=ok;', 'st[qq.n]=ok;try{BXMR.ans("jj","tch1",qq.n,ok)}catch(e){}', f)
    s = rep(s, '$("rs").onclick=function(){st={};', '$("rs").onclick=function(){try{BXMR.reset("tch1",25)}catch(e){}st={};', f)
    s = rep(s, 'function build(){', 'var _bxm=0;function build(){if(!_bxm){_bxm=1;try{BXMR.boot("tch1",25)}catch(e){}}', f)
    s = rep(s, ' $("rs").onclick=function(){try{BXMR.reset', ' try{var hh=$("p1").appendChild(document.createElement("div"));BXMR.mount("jj","tch1",hh,25,null)}catch(e){}\n $("rs").onclick=function(){try{BXMR.reset', f)
    return addtag(s)

# ④ 估價綜合模擬卷一～五、自編補強卷：QUESTIONS＋selectOpt＋resetAll
VQ = {'估價_綜合模擬卷一.html': 'mockc1', '估價_綜合模擬卷二.html': 'mockc2', '估價_綜合模擬卷三.html': 'mockc3',
      '估價_綜合模擬卷四.html': 'mockc4', '估價_綜合模擬卷五.html': 'mockc5', '估價_自編補強卷.html': 'mockx1'}
def vq(f, pid):
    s = rd(f)
    s = rep(s, 'const isRight=(oi===q.ans);', 'const isRight=(oi===q.ans);try{BXMR.ans("val","%s",QUESTIONS.indexOf(q)+1,isRight)}catch(e){}' % pid, f)
    s = rep(s, "if(!confirm('確定要重置所有作答紀錄？'))return;", "if(!confirm('確定要重置所有作答紀錄？'))return;try{BXMR.reset('%s',QUESTIONS.length)}catch(e){}" % pid, f)
    m = list(re.finditer(r'\ninit\(\);', s))[-1]
    s = s[:m.start()] + "\ntry{BXMR.boot('%s',QUESTIONS.length)}catch(e){}" % pid + s[m.start():m.end()] + \
        "\ntry{var qc=document.getElementById('quizContainer'),hh=document.createElement('div');qc.parentNode.insertBefore(hh,qc.nextSibling);BXMR.mount('val','%s',hh,QUESTIONS.length,null)}catch(e){}" % pid + s[m.end():]
    return addtag(s)

# ⑤ 估價來勝：作答會記在 v_hs1_answers（重開還在），所以給「重做本卷」鈕
def hs(f):
    s = rd(f)
    s = rep(s, '  answers[id] = idx;\n  saveAnswers();', '  answers[id] = idx;\n  saveAnswers();\n  try{var _i=ITEMS.findIndex(function(x){return x.id===id});BXMR.ans("val","hs1",_i+1,idx===ITEMS[_i].correct)}catch(e){}', f)
    i = s.index('</script>', s.index('function renderMC'))
    s = s[:i] + "\ntry{var _p1=document.getElementById('p1'),hh=document.createElement('div');_p1.parentNode.insertBefore(hh,_p1.nextSibling);BXMR.mount('val','hs1',hh,ITEMS.length,null,function(){answers={};saveAnswers();saveMockScore();renderMC();window.scrollTo(0,0)})}catch(e){}\n" + s[i:]
    return addtag(s)

# ⑥ 估價診斷卷①：重新整理就清空 → 開頁先存上一次；給「重做本卷」鈕
def vdiag(f):
    s = rd(f)
    s = rep(s, 'var right=(ch===ans);', 'var right=(ch===ans);try{BXMR.ans("val","vdiag1",n,right)}catch(e){}', f)
    i = s.rindex('</script>')
    s = s[:i] + "\ntry{BXMR.boot('vdiag1',25);var _ft=document.querySelector('footer'),hh=document.createElement('div');hh.style.cssText='max-width:900px;margin:0 auto;padding:0 16px';_ft.parentNode.insertBefore(hh,_ft);BXMR.mount('val','vdiag1',hh,25,null,function(){location.reload()})}catch(e){}\n" + s[i:]
    return addtag(s)

# ⑦ 民法 25 題模擬測驗（歷屆真題組卷）：記到歷屆題熟練度 h:年-題
def civ25(f):
    s = rd(f)
    s = rep(s, '  const isOk=isOK(q,optIdx);', '  const isOk=isOK(q,optIdx);\n  try{var _m=String(q.year).match(/(\\d+)年第(\\d+)題/);if(_m)BXMR.rec("civ","h:"+_m[1]+"-"+_m[2],isOk)}catch(e){}', f)
    return addtag(s)

JOBS = [(f, lambda f=f, S=S: t1(f, S)) for f, S in T1.items()] + \
       [(f, lambda f=f: landdiag(f)) for f in ['土地法_診斷卷一.html', '土地法_診斷卷二.html']] + \
       [(f, lambda f=f: ll(f)) for f in ['土地法_來勝模擬試題一_土地法規.html', '土地法_來勝模擬試題一_土地稅法.html']] + \
       [('經紀法規_模擬試題一_曾榮耀.html', lambda: tch('經紀法規_模擬試題一_曾榮耀.html'))] + \
       [(f, lambda f=f, p=p: vq(f, p)) for f, p in VQ.items()] + \
       [('估價_來勝模擬試題一.html', lambda: hs('估價_來勝模擬試題一.html')),
        ('估價_診斷卷一.html', lambda: vdiag('估價_診斷卷一.html')),
        ('民法概要_25題模擬測驗.html', lambda: civ25('民法概要_25題模擬測驗.html'))]
for f, job in JOBS:
    if TAG in rd(f): print('skip', f); continue
    s = job(); wr(f, s); print('ok', f)
