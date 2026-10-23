# 合併 lj_out/out_*.json → lj_data.json，並檢查 65 題齊全、無重複
import json,os,glob,sys
HERE=os.path.dirname(os.path.abspath(__file__))
ES=[x['eid'] for x in json.load(open(os.path.join(HERE,'essays.json'),encoding='utf-8'))]
DEMO={x['k']:x for x in json.load(open(os.path.join(HERE,'lj_demo.json'),encoding='utf-8'))}
got={}
for f in sorted(glob.glob(os.path.join(HERE,'lj_out','out_*.json'))):
    try: part=json.load(open(f,encoding='utf-8'))
    except Exception as ex: sys.exit('✗ %s 無法解析：%s'%(os.path.basename(f),ex))
    for d in part:
        k=d['k']
        if k in got: print('⚠ 重複：',k,'（後者覆蓋前者）')
        got[k]=d
    print(os.path.basename(f),len(part),'題')
# 定稿範例優先
for k,v in DEMO.items():
    if k in got: print('ℹ',k,'改用 lj_demo.json 的定稿版')
    got[k]=v
miss=[k for k in ES if k not in got]
extra=[k for k in got if k not in ES]
if miss: sys.exit('✗ 缺 %d 題：%s'%(len(miss),'、'.join(miss)))
if extra: sys.exit('✗ 多出不存在的題：'+'、'.join(extra))
out=[got[k] for k in ES]
json.dump(out,open(os.path.join(HERE,'lj_data.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
nsub=sum(len(d['subs']) for d in out); nstep=sum(len(s['steps']) for d in out for s in d['subs'])
nex=sum(1 for d in out if d.get('example'))
print('✓ lj_data.json 共 %d 題、%d 子題、%d 步驟、說明型（舉例）%d 題'%(len(out),nsub,nstep,nex))
