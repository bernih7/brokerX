#!/usr/bin/env python3
"""v613：答錯 → 更正卡＋「看完整解析」收合；黃底只標你選的與答案兩個選項；拿掉圖例、解析內重複標籤、答錯提示列。可重跑。"""
import glob
s0g=['']
def R(s,o,n,f):
    if 'bxvCard' in s0g[0] : return s
    assert s.count(o)==1,(f,o[:70]); return s.replace(o,n)
for f in sorted(glob.glob('估價刷題練習_*.html')):
    if '113真題' in f: continue
    s=open(f,encoding='utf-8').read();s0=s;s0g[0]=s
    if 'I2J1' in f:
        s=R(s,"bxvHL(it.id,i,o,'opt'):o}","bxvHL(it.id,i,o,'opt',ans.selected,it.correct):o}",f)
        s=R(s,"${ans?`<div class=\"explain-box\">","${ans?`${!ans.correct&&window.bxvCard?bxvCard(it.id,ans.selected,it.correct)+bxvMore(1):''}<div class=\"explain-box\">",f)
        s=R(s,"<div class=\"explain-title\">▸ 逐選項解析${(window.BXV_HL||{})[it.id]?bxvHLlegend:''}</div>","<div class=\"explain-title\">▸ 逐選項解析</div>",f)
        s=R(s,"<div class=\"explain-item${i===it.correct?' right':''}\">","<div class=\"explain-item${i===it.correct?' right':''}${!ans.correct&&i!==it.correct&&i!==ans.selected?' dim':''}\">",f)
        s=R(s,"bxvHL(it.id,i,ex,'exp'):ex}","bxvHL(it.id,i,ex,'exp',ans.correct?null:ans.selected,it.correct):ex}",f)
        s=R(s,"      </div>`).join('')}\n    </div>`:''}","      </div>`).join('')}\n    </div>${!ans.correct&&window.bxvCard?bxvMore(0):''}`:''}",f)
    else:
        s=R(s,"bxvHL(it.id,i,opt,'opt'):opt}","bxvHL(it.id,i,opt,'opt',a.selected,it.correct):opt}",f)
        s=R(s,"explainHtml = (!a.correct ? `<div class=\"ans-verdict\">✗ 答錯了：你選 <b>${letters[a.selected]}</b>，正確答案 <b>${letters[it.correct]}</b></div>` : '') + '<div class=\"explain-box\"><div class=\"explain-title\">📚 逐選項解析' + ((window.BXV_HL||{})[it.id]&&window.bxvHLlegend?bxvHLlegend:'') + '</div>';",
              "explainHtml = (!a.correct ? (window.bxvCard ? bxvCard(it.id,a.selected,it.correct) + bxvMore(1) : `<div class=\"ans-verdict\">✗ 答錯了：你選 <b>${letters[a.selected]}</b>，正確答案 <b>${letters[it.correct]}</b></div>`) : '') + '<div class=\"explain-box\"><div class=\"explain-title\">📚 逐選項解析</div>';",f)
        s=R(s,"const cls = isCorrect ? 'explain-item right' : 'explain-item';","const cls = (isCorrect ? 'explain-item right' : 'explain-item') + (!a.correct && !isCorrect && i!==a.selected ? ' dim' : '');",f)
        s=R(s,"bxvHL(it.id,i,it.explains[i],'exp'):it.explains[i])","bxvHL(it.id,i,it.explains[i],'exp',a.correct?null:a.selected,it.correct):it.explains[i])",f)
        s=R(s,"const meTag = (i===a.selected && !isCorrect) ? '<span class=\"exp-me\">你選的</span>' : ((isCorrect && !a.correct) ? '<span class=\"exp-ans\">正確答案</span>' : '');","const meTag = '';",f)
        s=R(s,"      explainHtml += '</div>';\n","      explainHtml += '</div>' + (!a.correct && window.bxvCard ? bxvMore(0) : '');\n",f)
    if s!=s0: open(f,'w',encoding='utf-8').write(s);print('改',f)
# 113真題
f='估價刷題練習_113真題.html';s=open(f,encoding='utf-8').read();s0=s;s0g[0]=s
E="String(%s).replace(/&/g,'&amp;').replace(/</g,'&lt;')"
s=R(s,'bxvHL(item.id, oi, '+E%'opt'+', "opt")','bxvHL(item.id, oi, '+E%'opt'+', "opt", answers[item.id], item.correct)',f)
s=R(s,'      if((window.BXV_HL||{})[item.id] && window.bxvHLlegend) et.insertAdjacentHTML("beforeend", bxvHLlegend);\n','',f)
s=R(s,'        ei.className = "explain-item" + (li === item.correct ? " right" : "");','        ei.className = "explain-item" + (li === item.correct ? " right" : "") + (!isCorrect && li !== item.correct && li !== answers[item.id] ? " dim" : "");',f)
s=R(s,'bxvHL(item.id, li, '+E%'item.explains[li]'+', "exp")','bxvHL(item.id, li, '+E%'item.explains[li]'+', "exp", isCorrect ? null : answers[item.id], item.correct)',f)
s=R(s,'      card.appendChild(eb);\n','      if(!isCorrect && window.bxvCard){\n        card.insertAdjacentHTML("beforeend", bxvCard(item.id, answers[item.id], item.correct));\n        const dm = document.createElement("details"); dm.className = "exp-more";\n        dm.innerHTML = "<summary>四個選項的完整解析</summary>"; dm.appendChild(eb); card.appendChild(dm);\n      } else card.appendChild(eb);\n',f)
if s!=s0: open(f,'w',encoding='utf-8').write(s);print('改',f)
# 解析版練習
f='估價解析版練習.html';s=open(f,encoding='utf-8').read();s0=s;s0g[0]=s
s=R(s,'bxvHL(q.id,i,q.opts[i],"opt")','bxvHL(q.id,i,q.opts[i],"opt",idx,q.correct)',f)
s=R(s,'  q.opts.forEach(function(o,i){var isOk=i===q.correct,pk=i===idx;\n    h+=\'<div class="xr\'+(isOk?" ok":"")+(pk&&!isOk?" pick":"")',
      '  if(!ok&&window.bxvCard)h+=bxvCard(q.id,idx,q.correct,true)+bxvMore(1);\n  q.opts.forEach(function(o,i){var isOk=i===q.correct,pk=i===idx;\n    h+=\'<div class="xr\'+(isOk?" ok":"")+(pk&&!isOk?" pick":"")+(!ok&&!isOk&&!pk?" dim":"")',f)
s=R(s,'bxvHL(q.id,i,q.exps[i],"exp")','bxvHL(q.id,i,q.exps[i],"exp",ok?null:idx,q.correct)',f)
s=R(s,'  if(q.note)h+=\'<div class="notebox">','  if(!ok&&window.bxvCard)h+=bxvMore(0);\n  if(q.note)h+=\'<div class="notebox">',f)
if s!=s0: open(f,'w',encoding='utf-8').write(s);print('改',f)
# 面板
f='bxv-topic-qa.js';s=open(f,encoding='utf-8').read();s0=s;s0g[0]=s
s=R(s,"bxvHL(q._id, i, esc(o), 'opt')","bxvHL(q._id, i, esc(o), 'opt', 'ABCD'.indexOf(picked), 'ABCD'.indexOf(acc[0]))",f)
s=R(s,"          h += '<div class=\"ex\">' + (q.exp || []).map(function (t, i) {\n            var L = 'ABCD'[i];\n            return '<div class=\"' + (acc.indexOf(L) >= 0 ? 'y' : '')",
      "          var _wr = !ok && !isFree(q) && window.bxvCard, _si = 'ABCD'.indexOf(picked), _ci = 'ABCD'.indexOf(acc[0]);\n          if (_wr) h += bxvCard(q._id, _si, _ci, true) + bxvMore(1);\n          h += '<div class=\"ex\">' + (q.exp || []).map(function (t, i) {\n            var L = 'ABCD'[i];\n            return '<div class=\"' + (acc.indexOf(L) >= 0 ? 'y' : '') + (_wr && acc.indexOf(L) < 0 && L !== picked ? ' dim' : '')",f)
s=R(s,"bxvHL(q._id, i, rich(t), 'exp')","bxvHL(q._id, i, rich(t), 'exp', ok ? null : 'ABCD'.indexOf(picked), 'ABCD'.indexOf(acc[0]))",f)
s=R(s,"          }).join('') + '</div>';\n          var ls = (q.law","          }).join('') + '</div>' + (_wr ? bxvMore(0) : '');\n          var ls = (q.law",f)
if s!=s0: open(f,'w',encoding='utf-8').write(s);print('改',f)
