# 中文數字→阿拉伯數字（申論計算、金額、百分比、期間）；條文逐字區塊與「」引文內不動
import re
D={'零':0,'〇':0,'一':1,'二':2,'兩':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
U={'十':10,'百':100,'千':1000}
def small(t):
    if t=='':return 0
    n=0;cur=0
    for ch in t:
        if ch in D: cur=D[ch]
        elif ch in U:
            n+=(cur if cur else 1)*U[ch]; cur=0
        else: raise ValueError(t)
    return n+cur
def parse(t):
    core=t.split('點')[0]
    if len(core)>1 and not any(c in core for c in '十百千萬億'): raise ValueError('positional')
    if core and core[0] in '百千萬億': raise ValueError('bare unit')
    if re.search('[一二兩三四五六七八九][一二兩三四五六七八九]',core): raise ValueError('adjacent digits')
    # 支援 萬、億、點
    dec=''
    if '點' in t:
        t,d=t.split('點',1); dec='.'+''.join(str(D[c]) for c in d)
    v=0
    if '億' in t:
        a,t=t.split('億',1); v+=small(a)*10**8
    if '萬' in t:
        a,t=t.split('萬',1); v+=small(a)*10**4
    v+=small(t)
    return v,dec
def fmt(v,dec=''):
    return f'{v:,}'+dec
NUM='[零〇一二兩三四五六七八九十百千]'
P_MONEY=re.compile(r'(?<![第零〇一二兩三四五六七八九十百千萬．.])((?:%s|點)+萬|%s(?:%s|點|萬|億)*)(萬元|億元|元)'%(NUM,NUM,NUM))
P_PCT=re.compile(r'(?<![．.])(百分之|千分之)((?:%s|點)+)'%NUM)
P_UNIT=re.compile(r'(?<![第之生同統唯單任每逐零〇一二兩三四五六七八九十百千．.])(%s+)(個月|年|日|天|戶|倍|公畝|公頃|成)(?![立功效為份分本度份])'%NUM)
def conv_plain(s):
    def m1(m):
        a,u=m.group(1),m.group(2)
        try:
            if a.endswith('萬') and u=='元':
                v,d=parse(a[:-1]); return fmt(v,d)+'萬元'
            v,d=parse(a); return fmt(v,d)+u
        except Exception: return m.group(0)
    s=P_MONEY.sub(m1,s)
    def m2(m):
        try:
            v,d=parse(m.group(2)); return str(v)+d+('%' if m.group(1)=='百分之' else '‰')
        except Exception: return m.group(0)
    s=P_PCT.sub(m2,s)
    def m3(m):
        try:
            v,d=parse(m.group(1)); return str(v)+d+m.group(2)
        except Exception: return m.group(0)
    s=P_UNIT.sub(m3,s)
    return s
def conv_text(s):
    # 跳過「」內與 HTML 標籤內
    out=[];i=0;q=0
    parts=re.split(r'(<[^>]*>|「|」)',s)
    for p in parts:
        if p=='「': q+=1; out.append(p); continue
        if p=='」': q=max(0,q-1); out.append(p); continue
        if p.startswith('<') or q>0 or not p: out.append(p); continue
        out.append(conv_plain(p))
    return ''.join(out)
if __name__=='__main__':
    for t in ['本題甲成交價一千六百萬元減除取得成本一千萬元；費用按百分之三計算為四十八萬元，但以三十萬元為限','應納稅額為三百七十萬元×百分之三十五＝一百二十九點五萬元','持有二年以內百分之四十五、超過十年百分之十五','第十四條之五','一生一次','一年六個月','一萬二千元','千分之二','全國僅持有一戶','第一次','「三十日內」','重購後五年內','一定金額','同一年度','三分之二','二十年']:
        print(t,'→',conv_text(t))
