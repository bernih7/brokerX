import sys,importlib.util,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import Ctx
c=Ctx()
for f in sys.argv[1:]:
    if f=='--dry': continue
    spec=importlib.util.spec_from_file_location('m',f); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for k,cid,o,n in m.E: c.apply(k,cid,o,n)
for x in c.log: 
    if x[2]==0: print('  (已套用或0命中)',x)
if '--dry' in sys.argv:
    for e in c.err: print('找不到：',e)
    print('dry：',len(c.log),'筆，未命中',len(c.err))
else: c.save()
