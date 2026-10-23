import re,json,sys
def grab(fn,var):
    s=open(fn,encoding='utf-8').read()
    i=s.index(var); i=s.index('=',i)+1
    k=i
    while s[k] in ' \n\t': k+=1
    op=s[k]; cl={'[':']','{':'}'}[op]; d=0; ins=False; esc=False; j=k
    while j<len(s):
        c=s[j]
        if ins:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c=='"': ins=False
        else:
            if c=='"': ins=True
            elif c==op: d+=1
            elif c==cl:
                d-=1
                if d==0: break
        j+=1
    return json.loads(s[k:j+1])
