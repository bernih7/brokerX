# 合併 out/land*.json → bxl-core.js、out/val*.json → bxv-core.js（可重跑）
import json,glob
for pre,var,fn,head in [('land','BXL_CORE','bxl-core.js','土地法'),('val','BXV_CORE','bxv-core.js','估價')]:
    D={}
    for f in sorted(glob.glob('tools/core_gen/out/%s*.json'%pre)):D.update(json.load(open(f)))
    open(fn,'w').write('/* %s刷題解析「一句重點」（每選項一句，濃縮自現有解析，不加新內容）。由 tools/core_gen/merge.py 產生，改 tools/core_gen/out/*.json 後重跑。 */\nwindow.%s=%s;\n'%(head,var,json.dumps(D,ensure_ascii=False,separators=(',',':'))))
    print(fn,len(D))
