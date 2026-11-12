# 申論中文數字→阿拉伯數字（v823）。不動：完整版「二、法條」條文逐字區塊、條文全文(btx)、原題(oq)、曾老師版、「」引文、標籤屬性
import re,json,sys
sys.path.insert(0,'tools/essay_land')
from cnnum import conv_text
def block_end(s,i,tag):
    d=0; p=re.compile(r'<(/?)%s\b[^>]*>'%tag)
    for m in p.finditer(s,i):
        d+= -1 if m.group(1) else 1
        if d==0: return m.end()
    return len(s)
def protected(s):
    R=[]
    for pat,tag in [(r'<details class="blk b2"','details'),(r'<div class="btx"','div'),(r'<div class="vp" data-v="5"','div'),(r'<[a-z]+ class="oq"',None),(r'<div class="bt"','div')]:
        for m in re.finditer(pat,s):
            t=tag or re.match(r'<([a-z]+)',m.group(0)).group(1)
            R.append((m.start(),block_end(s,m.start(),t)))
    R.sort(); M=[]
    for a,b in R:
        if M and a<=M[-1][1]: M[-1]=(M[-1][0],max(b,M[-1][1]))
        else: M.append((a,b))
    return M
def conv_html(s,lo,hi):
    out=[];pos=lo
    for a,b in protected(s[lo:hi]):
        a+=lo;b+=lo
        out.append(conv_text(s[pos:a])); out.append(s[a:b]); pos=b
    out.append(conv_text(s[pos:hi]))
    return ''.join(out)
def do_page(f):
    s=open(f,encoding='utf-8').read()
    a=s.find('<details class="es'); b=s.rfind('</details>')+len('</details>')
    n=conv_html(s,a,b)
    s2=s[:a]+n+s[b:]
    open(f,'w',encoding='utf-8').write(s2); return s!=s2
def conv_json_obj(o,skipk=('q','law','lawh','t','no','id','k','g','lv','tier','link')):
    if isinstance(o,dict): return {k:(v if k in skipk else conv_json_obj(v,skipk)) for k,v in o.items()}
    if isinstance(o,list):
        if len(o)==2 and isinstance(o[0],str) and '法條' in o[0]: return o
        return [x if (isinstance(x,str) and '二、法條' in x[:60]) else conv_json_obj(x,skipk) for x in o]
    if isinstance(o,str): return conv_text(o)
    return o
def do_cards(f):
    t=open(f,encoding='utf-8').read(); k=t.find('var CARDS=')+len('var CARDS=')
    v,end=json.JSONDecoder().raw_decode(t[k:])
    v2=conv_json_obj(v)
    t2=t[:k]+json.dumps(v2,ensure_ascii=False)+t[k+end:]
    open(f,'w',encoding='utf-8').write(t2); return t!=t2
def do_json(f):
    d=json.load(open(f,encoding='utf-8')); d2=conv_json_obj(d)
    if d!=d2: json.dump(d2,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=1); return True
    return False
if __name__=='__main__':
    print('總覽',do_page('土地法_申論題分類總覽.html'))
    # src.html 另以 <body> 範圍＋保護 seg s2 處理（見 v823 紀錄）；本支不要重跑：轉換為冪等，但 JSON 會重排版
    for f in ['土地法_申論5分鐘衝刺.html','土地法_申論5分鐘_推理版.html']: print(f,do_cards(f))
    for f in ['exam_ver.json','exam_ver_more.json','exam_ver_off.json','lj_data.json']: print(f,do_json('tools/essay_land/data/'+f))
