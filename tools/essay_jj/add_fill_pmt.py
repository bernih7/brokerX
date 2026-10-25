# -*- coding: utf-8 -*-
"""把「白話 p／口訣 m／考試陷阱 t」三段併進《經紀法規_定義填空練習》的 106 張卡，
並補精確條號（src）。規格與《民法_定義填空練習》一致，跨科同一套。

資料來源：tools/essay_jj/fill_enrich.json（key = 章ID-索引）
可重複執行：每次都用 enrich 檔覆蓋 p/m/t，src 只在 enrich 有給新值時才換。
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PAGE = os.path.join(ROOT, '經紀法規_定義填空練習.html')
ENR = os.path.join(HERE, 'fill_enrich.json')

s = io.open(PAGE, encoding='utf-8').read()
E = json.load(io.open(ENR, encoding='utf-8'))

# ── 取出 DATA 陣列 ──
i0 = s.index('DATA')
st = s.index('[', i0)
d, k = 0, st
while True:
    if s[k] == '[':
        d += 1
    elif s[k] == ']':
        d -= 1
        if d == 0:
            break
    k += 1
raw = s[st:k + 1]
D = json.loads(raw)

# ── 內容修正（逐字條文核對後才改；每一筆都註明依據） ──
FIX = {
    # 說明書不得記載共六點（6laws 鏡像逐字，版本與 115.1.13 內政部令一致）。
    # 原卡只收四點，補上第四點「夾層」；第五點另見 C-1。
    'C-0': {
        'blank': '不動產說明書不得記載：本說明書內容___；___說明書；'
                 '實際所有權面積以外之「___面積」「___面積」「___面積」等類似名詞；'
                 '預售屋未領建照之___設計或空間面積；房價有___空間。',
        'answer': '不動產說明書不得記載：本說明書內容<span class="key">僅供參考</span>；'
                  '<span class="key">繳回</span>說明書；實際所有權面積以外之'
                  '「<span class="key">受益</span>面積」「<span class="key">銷售</span>面積」'
                  '「<span class="key">使用</span>面積」等類似名詞；預售屋未領建照之'
                  '<span class="key">夾層</span>設計或空間面積；房價有'
                  '<span class="key">上漲</span>空間。',
    },
    # 建物型態逐字：區分所有建物含透天厝、店面、辦公商業大樓、套房——原卡漏列，
    # 而「透天厝屬區分所有建物」正是標準陷阱。
    'C-6': {
        'blank': '建物型態分三類：<b>一般建物</b>＝單獨所有權___共有部分（獨棟、連棟、雙併）；'
                 '<b>區分所有建物</b>＝公寓（___樓含以下無電梯）、___、店面、辦公商業大樓、'
                 '住宅或複合型大樓（___層含以上有電梯）、華廈（___層含以下有電梯）、'
                 '套房（一房一廳一衛）；<b>其他特殊建物</b>＝工廠、廠辦、___、倉庫。',
        'answer': '建物型態分三類：<b>一般建物</b>＝單獨所有權<span class="key">無</span>共有部分'
                  '（獨棟、連棟、雙併）；<b>區分所有建物</b>＝公寓（<span class="key">五</span>樓含以下無電梯）、'
                  '<span class="key">透天厝</span>、店面、辦公商業大樓、住宅或複合型大樓'
                  '（<span class="key">十一</span>層含以上有電梯）、華廈（<span class="key">十</span>層含以下有電梯）、'
                  '套房（一房一廳一衛）；<b>其他特殊建物</b>＝工廠、廠辦、'
                  '<span class="key">農舍</span>、倉庫。',
    },
    # 公寓大廈§55Ⅱ 逐字有但書「但得不受第七條各款不得為約定專用部分之限制」，
    # 原卡漏掉；這個但書正是§7「寫了也不生效力」的唯一例外。
    'F-3': {
        'blank': '規約範本由___定之（§60Ⅰ），§56 規約草約得依規約範本___（§60Ⅱ）；'
                 '本條例施行前已取得___之公寓大廈，於區權會訂定規約前，以規約範本___規約，'
                 '但得<b>不受___各款不得為約定專用部分之限制</b>（§55Ⅱ）。',
        'answer': '規約範本由<span class="key">中央主管機關</span>定之（§60Ⅰ），'
                  '§56 規約草約得依規約範本<span class="key">制作</span>（§60Ⅱ）；'
                  '本條例施行前已取得<span class="key">建造執照</span>之公寓大廈，'
                  '於區權會訂定規約前，以規約範本<span class="key">視為</span>規約，'
                  '但得<b>不受<span class="key">第七條</span>各款不得為約定專用部分之限制</b>（§55Ⅱ）。',
    },
    # 公寓大廈§4Ⅱ 逐字：「專有部分不得與其所屬建築物共用部分之應有部分及其基地
    # 所有權或地上權之應有部分分離而為移轉或設定負擔。」原卡漏「地上權」與「設定負擔」。
    'E-2': {
        'blank': '專有部分不得與其所屬建築物___之應有部分，及其基地___或___之應有部分，'
                 '分離而為___或___。',
        'answer': '專有部分不得與其所屬建築物<span class="key">共用部分</span>之應有部分，'
                  '及其基地<span class="key">所有權</span>或<span class="key">地上權</span>之應有部分，'
                  '分離而為<span class="key">移轉</span>或<span class="key">設定負擔</span>。',
    },
    # 公寓大廈§7 逐字共五款，原卡只寫到第三款，且第二款漏「通往室外之通路或門廳；
    # 社區內各巷道、防火巷弄」——防火巷弄、門廳正是選擇題常見選項。
    'E-3': {
        'blank': '不得約定專用（§7 五款）：①本身所占之___；②連通數個專有部分之走廊或樓梯，'
                 '及其通往室外之通路或___；社區內各巷道、___；③基礎、主要樑柱、承重牆壁、'
                 '樓地板及___之構造；④約定專用有違___使用限制者；⑤其他有固定使用方法，'
                 '並屬區分所有權人生活利用上___之共用部分。',
        'answer': '不得約定專用（§7 五款）：①本身所占之<span class="key">地面</span>；'
                  '②連通數個專有部分之走廊或樓梯，及其通往室外之通路或'
                  '<span class="key">門廳</span>；社區內各巷道、<span class="key">防火巷弄</span>；'
                  '③基礎、主要樑柱、承重牆壁、樓地板及<span class="key">屋頂</span>之構造；'
                  '④約定專用有違<span class="key">法令</span>使用限制者；'
                  '⑤其他有固定使用方法，並屬區分所有權人生活利用上'
                  '<span class="key">不可或缺</span>之共用部分。',
    },
    # 公寓大廈§25Ⅲ 逐字：召集人「任期一至二年，連選得連任一次」——原卡把「連任一次」
    # 只掛在主委等人身上，召集人被歸到「其餘連選得連任」會讀錯。
    'E-12': {
        'blank': '召集人任期___年，未規定者___年，連選得連任___次；'
                 '主委、管理負責人、財務監察委員連選得連任___次，其餘管理委員連選___。',
        'answer': '召集人任期<span class="key">1至2</span>年，未規定者<span class="key">1</span>年，'
                  '連選得連任<span class="key">1</span>次；'
                  '主委、管理負責人、財務監察委員連選得連任<span class="key">1</span>次，'
                  '其餘管理委員連選<span class="key">得連任</span>。',
    },
    # 公寓大廈§49Ⅱ 除徒刑外另有罰金，原卡漏列。
    'E-17': {
        'blank': '供營業使用之住戶違反擅自變更使用／§16Ⅱ、Ⅲ，致人於死者處___有期徒刑，'
                 '得併科___罰金；致重傷者處___有期徒刑，得併科___罰金。',
        'answer': '供營業使用之住戶違反擅自變更使用／§16Ⅱ、Ⅲ，致人於死者處'
                  '<span class="key">1年以上7年以下</span>有期徒刑，得併科'
                  '<span class="key">100萬以上500萬以下</span>罰金；致重傷者處'
                  '<span class="key">6個月以上5年以下</span>有期徒刑，得併科'
                  '<span class="key">50萬以上250萬以下</span>罰金。',
    },
    # 公平法§21Ⅰ 逐字含「或以其他使公眾得知之方法」與「與商品相關而」，原卡把範圍
    # 限縮在「商品或廣告上」，正是誘答設計的那一塊。
    'G-0': {
        'blank': '事業不得在商品或廣告上，或以其他使___之方法，對於與商品相關而'
                 '足以影響___之事項，為___或___之表示或表徵。',
        'answer': '事業不得在商品或廣告上，或以其他使<span class="key">公眾得知</span>之方法，'
                  '對於與商品相關而足以影響<span class="key">交易決定</span>之事項，為'
                  '<span class="key">虛偽不實</span>或<span class="key">引人錯誤</span>之表示或表徵。',
    },
    # 公平法§21Ⅴ 但書逐字為「非屬知名公眾人物、專業人士或機構」，原卡漏「專業人士」。
    'G-1': {
        'blank': '廣告代理業、媒體業明知或可得而知仍製作／傳播，與廣告主負___責任；'
                 '非屬知名公眾人物、___或___之薦證者，僅於受廣告主報酬___範圍內負連帶責任。',
        'answer': '廣告代理業、媒體業明知或可得而知仍製作／傳播，與廣告主負'
                  '<span class="key">連帶損害賠償</span>責任；非屬知名公眾人物、'
                  '<span class="key">專業人士</span>或<span class="key">機構</span>之薦證者，'
                  '僅於受廣告主報酬<span class="key">10倍</span>範圍內負連帶責任。',
    },
    # 公寓大廈施行細則§10 逐字：「財務報表，指公共基金之現金收支表及管理維護費之
    # 現金收支表及財產目錄、費用及應收未收款明細。」原卡只寫「現金收支表及財產目錄」，
    # 漏掉「管理維護費之現金收支表」與「費用及應收未收款明細」。
    'F-4': {
        'blank': '會計憑證指___憑證；會計帳簿指___帳及___帳；'
                 '財務報表指公共基金之現金收支表、管理維護費之現金收支表、'
                 '___目錄，及費用及___明細。',
        'answer': '會計憑證指<span class="key">原始</span>憑證；'
                  '會計帳簿指<span class="key">日記</span>帳及<span class="key">總分類</span>帳；'
                  '財務報表指公共基金之現金收支表、管理維護費之現金收支表、'
                  '<span class="key">財產</span>目錄，及費用及'
                  '<span class="key">應收未收款</span>明細。',
    },
}

n_pmt, n_src, n_fix, miss = 0, 0, 0, []
for ch in D:
    for i, c in enumerate(ch['cards']):
        key = '%s-%d' % (ch['id'], i)
        if key in FIX:
            c.update(FIX[key])
            n_fix += 1
        e = E.get(key)
        if not e:
            miss.append(key)
            continue
        for f in ('p', 'm', 't'):
            v = (e.get(f) or '').strip()
            if v:
                c[f] = v
            else:
                c.pop(f, None)
        n_pmt += 1
        ns = (e.get('src') or '').strip()
        if ns and ns != c.get('src'):
            c['src'] = ns
            n_src += 1

new = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
s = s[:st] + new + s[k + 1:]
io.open(PAGE, 'w', encoding='utf-8').write(s)

tot = sum(len(ch['cards']) for ch in D)
print('卡片共 %d 張｜補上白話/口訣/陷阱 %d 張｜換掉 src %d 張｜內容修正 %d 張'
      % (tot, n_pmt, n_src, n_fix))
if miss:
    print('⚠ enrich 檔沒有的卡：', miss)
have = lambda f: sum(1 for ch in D for c in ch['cards'] if c.get(f))
print('現況：白話 %d／口訣 %d／陷阱 %d' % (have('p'), have('m'), have('t')))
# 條號（§12、第12條）或點次（第十二點、第三點、(四)3）都算有出處
PIN = re.compile(r'§\s*\d|第\s*[\d一二三四五六七八九十百]+\s*[條點項款]|（[一二三四五六七八九十]+）\s*\d')
noart = [('%s-%d' % (ch['id'], i), c['src'])
         for ch in D for i, c in enumerate(ch['cards'])
         if not PIN.search(c.get('src', ''))]
print('src 仍無條號／點次：%d 張' % len(noart))
for x in noart:
    print('   ', x)
