import json
# 從對話紀錄取出上一段 patch 腳本，改計數後存檔
found=None
for line in open('/root/.claude/projects/-home-claude/c1b89b96-7748-571f-810e-82d6369bb908.jsonl',encoding='utf-8'):
    if 'addlaw' not in line: continue
    o=json.loads(line)
    def walk(x):
        global found
        if isinstance(x,str):
            if x.startswith('cd ') and "addlaw('s10'" in x and 'mg_before' in x: found=x
        elif isinstance(x,dict): [walk(v) for v in x.values()]
        elif isinstance(x,list): [walk(v) for v in x]
    walk(o)
a=found.index("<<'EOF'\n")+8;b=found.rindex("\nEOF")
code=found[a:b]
code=code.replace("R('<b class=\"ar\">§881-17</b><span class=\"nv\">（依 108-二 範文所引 §881-17；非 law.json，待對全文）</span>','<b class=\"ar\">§881-17</b>')",
 "R('<b class=\"ar\">§881-17</b><span class=\"nv\">（依 108-二 範文所引 §881-17；非 law.json，待對全文）</span>','<b class=\"ar\">§881-17</b>',4)")
code=code.replace("R('不準用 <b class=\"ar\">§880</b><span class=\"nv\">","R('不準用 <b class=\"ar\">§880</b><span class=\"nv\">",1)
open('mgpatch.py','w',encoding='utf-8').write(code);print(len(code),',4)' in code)