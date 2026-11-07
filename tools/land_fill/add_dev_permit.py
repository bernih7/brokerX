# -*- coding: utf-8 -*-
"""B1 補★陷阱卡：開發許可的許可／廢止／失效／撤銷（109-7、107-16）。可重跑。"""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, '..', '..'))
P = os.path.join(R, '土地法_定義填空練習.html')
s = open(P, encoding='utf-8').read()
i = s.find('const DATA = ') + 13; D, e = json.JSONDecoder().raw_decode(s[i:])
TERM = '開發許可：許可要件 vs 廢止 vs 失效 vs 撤銷★陷阱'
b1 = [c for c in D if c['id'] == 'B1'][0]
b1['cards'] = [c for c in b1['cards'] if c['term'] != TERM]
txt = ('①<b>許可</b>（審議要件，區計§15-2Ⅰ）：國土利用適當合理；不違反土地利用或環保計畫；環保、自然保育、災害防止妥適規劃；'
       '與水源、交通、排水、電力、電信、垃圾處理等公共設施及公用設備能[[相互配合]]；取得土地及建物[[權利證明文件]]。<br>'
       '②<b>廢止</b>（許可後，非都規則§21Ⅰ，由直轄市、縣（市）政府報經[[區域計畫擬定機關]]廢止）：一、違反核定之土地使用計畫、目的事業或環評等法規，經[[限期改善而未改善]]；'
       '二、興辦事業計畫經廢止或依法失效，或整地排水計畫、水土保持計畫之核准經廢止（或失效）；三、申請人[[自行申請廢止]]。<br>'
       '③<b>失效</b>（非都規則§23，要旨）：許可後 [[1年]] 內未完成分區異動登記等（得展期，每次≤1年、以2次為限），或 [[10年]] 內未取得使用執照／營運文件（得展期≤5年、1次）→ 原許可失其效力。<br>'
       '④<b>撤銷</b>（要旨）：非都規則沒有專條；許可本身違法 → 依行政程序法撤銷，撤銷後[[溯及既往]]失效（行政程序法§118；法務部 101.11.26 法律字第10100106120號）。')
blank = re.sub(r'\[\[(.+?)\]\]', '___', txt); ans = re.sub(r'\[\[(.+?)\]\]', r'<span class="key">\1</span>', txt)
b1['cards'].append({'term': TERM, 'blank': blank, 'answer': ans,
  'src': '區域計畫法§15-2Ⅰ（站內條文庫）；非都市土地使用管制規則§21Ⅰ、§23（113.3.29 版）；行政程序法§118；109-7 錯誤選項把「公共設施能相互配合」（許可要件）當成廢止事由',
  'mc': 2, 'essay': 0, 'mcx': ['109-7', '107-16']})
s = s[:i] + json.dumps(D, ensure_ascii=False, indent=1) + s[i + e:]
n = sum(len(c['cards']) for c in D if c['id'][0] != 'S')
s = re.sub(r'定義 \d+ 題', '定義 %d 題' % n, s)
open(P, 'w', encoding='utf-8').write(s)
U = os.path.join(R, 'bx-use.js'); u = open(U, encoding='utf-8').read()
u = re.sub(r'fill:\d+', 'fill:%d' % n, u, 1); open(U, 'w', encoding='utf-8').write(u)
print('定義', n)
