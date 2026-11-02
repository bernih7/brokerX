# 申論專練卷完整版勘誤（考場版撰寫時發現）。可重跑
import os,json
R=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','..'))
FIX=[('依第4條第5款包含經紀人與經紀營業員','依第4條第7款包含經紀人與經紀營業員'),
     ('未經validate之敘述','未經查證之敘述'),
     ('乙為加盟經營者，依第18條應於廣告、市招、名片等明顯處標明加盟店或加盟經營字樣','乙為加盟經營者，依第18條應併標明加盟經營，並依廣告處理原則第三點（三）於廣告、市招、名片等明顯處標明加盟店或加盟經營字樣')]
for f in ['經紀法規_申論專練卷.html','tools/essay_jj/mock2/mock2.json','tools/essay_jj/lj_in/in_mock2.json','tools/essay_jj/exam_ver/src/todo_full.json']:
    p=os.path.join(R,f); s=open(p,encoding='utf-8').read(); n=0
    for a,b in FIX:
        if a in s: s=s.replace(a,b); n+=1
    open(p,'w',encoding='utf-8').write(s); print(f,n)
