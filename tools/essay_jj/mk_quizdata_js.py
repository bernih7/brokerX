# -*- coding: utf-8 -*-
"""產生 bxj-quiz-data.js：給整理頁的「考古題面板」用的共用題庫（對應估價 bxv-quiz-data.js）。
唯一事實來源仍是 tools/essay_jj/quiz_data.json，改題請改那裡再重跑本檔。"""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
D = json.load(io.open(os.path.join(HERE, 'quiz_data.json'), encoding='utf-8'))
dis = {}
p = os.path.join(HERE, 'disputed.json')
if os.path.exists(p):
    dis = json.load(io.open(p, encoding='utf-8'))
out = {'q': [], 'law': D['law']}
for x in D['q']:
    o = {k: x[k] for k in ('k', 'ch', 'y', 'n', 'stem', 'opt', 'ans', 'exp') if k in x}
    if x.get('law'):  o['law'] = x['law']
    if x.get('ref'):  o['ref'] = x['ref']
    if x.get('oos'):  o['oos'] = x['oos']
    if x.get('sr'):   o['sr'] = x['sr']
    if x.get('dis') or (x['k'] in dis): o['dis'] = x.get('dis') or dis[x['k']]
    out['q'].append(o)
f = os.path.join(ROOT, 'bxj-quiz-data.js')
io.open(f, 'w', encoding='utf-8').write(
    '/* 經紀法規共用題庫（給整理頁的考古題面板）。由 tools/essay_jj/mk_quizdata_js.py 從 quiz_data.json 產生，不要手改。 */\n'
    'window.BXJ_QUIZ=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('bxj-quiz-data.js %d 題・條文 %d 條・%.0f KB' % (len(out['q']), len(out['law']), os.path.getsize(f)/1024))
