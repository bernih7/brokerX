# 《民法_數字期間速查》④ 時效・除斥期間並排（條文原文取自 law.json）；可重跑
import json,os,re,html
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..')
L=json.load(open(os.path.join(H,'law.json'),encoding='utf-8'))
E=html.escape
# (期間, 什麼權利, 起算點, 條號[], 陷阱/提醒)
A=[('<span class="nm">15年</span>','一般請求權','請求權可行使時（§128）',['125','128'],'法律所定期間較短者依其規定，15 年是「沒有特別規定時」才用。'),
('<span class="nm">5年</span>','利息、紅利、租金、贍養費、退職金及其他一年或不及一年之定期給付的<b class="k">各期</b>給付','各期可行使時',['126'],'是「各期」分別算；租金欠款屬此類，不是 §127 的 2 年（§127③ 只限以租賃<b class="k">動產</b>為營業者之租價）。'),
('<span class="nm">2年</span>','§127 八款短期債權：旅店飲食、運送費、租賃動產營業之租價、醫藥看護、律師會計師公證人報酬、技師承攬人報酬、商人製造人手工業人商品代價','請求權可行使時',['127'],'承攬人「報酬」是 2 年，與承攬定作人瑕疵權利的期間不同，不要混。'),
('<span class="nm">2年／10年</span>','侵權行為損害賠償','知有損害<b class="k">及</b>賠償義務人時起 2 年；自有侵權行為時起逾 10 年',['197'],'兩個期間先到者為準；時效完成後若加害人因侵權受利益，仍得依不當得利請求（§197Ⅱ）。'),
('<span class="nm">2年</span>','締約上過失（契約未成立）損害賠償','（條文未定起算點）',['245-1'],'要件是「契約未成立時」，且受害人非因過失而信契約能成立。'),
('<span class="nm">2年</span>','出租人對承租人之損害賠償請求權；承租人之償還費用請求權、工作物取回權','出租人：自受租賃物返還時；承租人：自租賃關係終止時',['456'],'兩邊起算點不同，是常考的對調陷阱。'),
('<span class="nm">1年</span>','占有人之物上請求權（返還、除去、防止）','自侵奪或妨害占有或危險發生後',['963'],'這是占有保護（§962），不是所有權的 §767。'),
('<span class="nm">2年／10年</span>','繼承回復請求權','知悉被侵害時起 2 年；自繼承開始時起逾 10 年',['1146'],'請求權人是「被害人或其法定代理人」。'),
('<span class="nm">2年／5年</span>','剩餘財產差額分配請求權','知有剩餘財產之差額時起 2 年；自法定財產制關係消滅時起逾 5 年',['1030-1'],'與侵權、繼承回復的「10 年」不同，這裡長期間是 5 年。'),
('<span class="nm">2年／5年</span>','剩餘財產分配權利人對受領第三人之返還請求權','知悉分配權利受侵害時起 2 年；自法定財產制關係消滅時起逾 5 年',['1030-3'],'追加計算的對象是消滅前 <span class="nm">5年</span>內處分的婚後財產。')]
B=[('<span class="nm">1年</span>','乘人急迫、輕率、無經驗之暴利行為：聲請法院撤銷或減輕給付','法律行為後',['74'],'要「聲請法院」，不是向相對人表示即可。'),
('<span class="nm">1年</span>','錯誤、傳達不實之撤銷權','意思表示後',['90'],'自「意思表示後」起算，不是知悉錯誤時。'),
('<span class="nm">1年／10年</span>','被詐欺、被脅迫之撤銷權','發見詐欺或脅迫終止後 1 年；自意思表示後經過 10 年不得撤銷',['93'],'錯誤只有 1 年（§90）；詐欺脅迫才有 1 年＋10 年。'),
('<span class="nm">1年／10年</span>','債權人撤銷權（詐害債權）','知有撤銷原因時起 1 年；自行為時起經過 10 年',['245'],'撤銷要「聲請法院」（§244）。'),
('<span class="nm">6個月／5年</span>','物之瑕疵：解除契約或請求減少價金','依 §356 通知後 6 個月；自物之交付時起經過 5 年',['365'],'出賣人故意不告知瑕疵者，不適用 6 個月（Ⅱ）。'),
('<span class="nm">1年</span>','贈與人撤銷贈與（§416 情事）','贈與人知有撤銷原因之時起；贈與人已為宥恕之表示者，撤銷權亦消滅',['416'],'§417 是繼承人撤銷，期間 6 個月。'),
('<span class="nm">6個月</span>','贈與人之繼承人撤銷贈與','知有撤銷原因之時起',['417'],'要件是受贈人故意不法致贈與人死亡或妨礙撤銷。'),
('<span class="nm">6個月／1年</span>','夫妻一方詐害剩餘財產分配之撤銷權（§1020-1）','知有撤銷原因時起 6 個月；自行為時起經過 1 年',['1020-2'],'比 §245 短很多；逾期改看 §1030-3 追加計算。'),
('<span class="nm">6個月／2年</span>','重婚、與配偶以外之人合意性交：請求離婚','知悉後逾 6 個月或情事發生後逾 2 年不得請求',['1053'],'事前同意或事後宥恕也不得請求。')]
C=[('<span class="nm">5年</span>','抵押權：擔保之債權請求權已因時效消滅','消滅時效完成後 5 年間不實行',['880','145'],'時效消滅後債權人仍得就抵押物取償（§145Ⅰ），但利息等各期定期給付不適用（§145Ⅱ）；超過 5 年不實行，抵押權本身消滅。最高法院 87 年度台上字第 969 號判決稱此 5 年為除斥期間。'),
('<span class="nm">6個月</span>','因請求而中斷時效','請求後 6 個月內不起訴，視為不中斷',['130','131'],'這個 6 個月只針對「請求」；起訴另看 §131（撤回其訴或因不合法受駁回裁判確定，視為不中斷）。'),
('<span class="nm">5年</span>','經確定判決等執行名義確定之請求權','原有消滅時效期間不滿 5 年者，因中斷重行起算之期間為 5 年',['137'],'只把「不滿 5 年」的拉長為 5 年；原本 15 年的仍是 15 年。'),
('<span class="nm">1個月</span>','時效不完成（天災或不可避之事變）','自妨礙事由消滅時起 1 個月內',['139'],'是「不完成」（延後完成），不是中斷重算。')]
def law(keys):
    return ''.join('<p><b class="art">§%s</b>（%s）<br>%s</p>'%(k,E(L[k]['s']),E(L[k]['x']).replace('\n','<br>')) for k in keys)
def rows(T):
    h=''
    for v,what,start,keys,trap in T:
        h+=('<div class="sx4r"><div class="sx4v">%s</div><div class="sx4b"><div class="sx4w">%s</div>'
            '<div class="sx4s"><span class="tg">起算</span>%s</div><div class="sx4t">⚠ %s</div>'
            '<details class="sx4l"><summary>%s 條文原文</summary>%s</details></div></div>')%(v,what,start,trap,'、'.join('§'+k for k in keys),law(keys))
    return h
for T in (A,B,C):
    for r in T:
        for k in r[3]: assert k in L,k
sec=('<section id="s4"><h2>④ 時效・除斥期間並排</h2>'
 '<p class="nt" style="margin:0 0 8px">同一張表看「多久、從何時起算、哪裡容易對調」。<b class="k">消滅時效</b>完成後債務人得拒絕給付（§144），可中斷（§129）；<b class="k">除斥期間</b>是形成權（撤銷、解除）的存續期間，期間經過權利即消滅。條文原文取自《民法_現行條文核實表》與補遺。</p>'
 '<div class="sx4k">口訣：一般 15、定期 5、短期 2；侵權、繼承回復「2 年＋10 年」；剩餘財產「2 年＋5 年」；撤銷權多為 1 年（詐欺脅迫、詐害債權再加 10 年）〔自編〕</div>'
 '<h3>A. 消滅時效（請求權）</h3><div class="sx4">'+rows(A)+'</div>'
 '<h3>B. 除斥期間（撤銷權・解除權等形成權）</h3><div class="sx4">'+rows(B)+'</div>'
 '<h3>C. 中斷・不完成・擔保物權的特別規定</h3><div class="sx4">'+rows(C)+'</div>'
 '<p class="nt">註：「消滅時效／除斥期間」的分類是教材通用分法，條文本身多只寫「因○年間不行使而消滅」或「經過○年而消滅」。</p></section>')
css=('<style id="sx4-css">.sx4{border:1px solid var(--bd);border-radius:10px;overflow:hidden;background:var(--sf);margin:6px 0 10px}'
 '.sx4r{display:grid;grid-template-columns:86px 1fr;gap:8px;padding:9px 10px;border-bottom:1px solid var(--bd)}.sx4r:last-child{border-bottom:0}'
 '.sx4v{font-weight:700;font-size:13.5px}.sx4b{min-width:0}.sx4w{font-size:14px}.sx4s{font-size:13px;color:var(--tx);margin-top:3px}.sx4s .tg{margin-right:6px}'
 '.sx4t{font-size:12.5px;margin-top:4px;background:#fbe3dd;color:#6a2416;border-radius:6px;padding:3px 7px}[data-theme=dark] .sx4t{background:#3a221d;color:#ffb5a6}'
 '.sx4k{background:#e3f1e5;color:#1f4a2a;border-radius:8px;padding:7px 10px;font-size:13.5px;margin:4px 0 6px}[data-theme=dark] .sx4k{background:#1f3326;color:#bfe5c7}'
 'details.sx4l{margin-top:4px}details.sx4l>summary{padding:2px 0;font-size:12.5px;color:var(--pri);font-weight:600}details.sx4l p{font-size:13px;margin:4px 0;background:var(--sf2);border-radius:6px;padding:6px 8px}'
 '.sx4 .art{color:#8a5517}[data-theme=dark] .sx4 .art{color:#e2bc84}@media(max-width:420px){.sx4r{grid-template-columns:1fr}}</style>')
P=os.path.join(R,'民法_數字期間速查.html'); s=open(P,encoding='utf-8').read()
s=re.sub(r'<section id="s4">.*?</section>','',s,flags=re.S); s=re.sub(r'<style id="sx4-css">.*?</style>','',s,flags=re.S)
a='<section id="s3"><h2>③ 易混淆整理</h2><div id="b3"></div></section>'; assert s.count(a)==1
s=s.replace(a,a+'\n'+sec)
if '<a href="#s4">' not in s: s=s.replace('<a href="#s3">易混淆</a>','<a href="#s3">易混淆</a><a href="#s4">時效並排</a>')
s=s.replace('</head>',css+'</head>',1)
open(P,'w',encoding='utf-8').write(s); print('ok',len(A)+len(B)+len(C),'列')
