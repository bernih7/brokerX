import json
D=json.load(open('quiz_data.json'))
PRI=[('tl','特留分・扣減',(1223,1224,1225,1187)),('dw','代位繼承',(1140,)),('ss','喪失繼承權・回復請求',(1145,1146)),('pq','拋棄繼承',(1174,1175,1176)),
 ('yz','遺囑・遺贈',tuple(range(1186,1222))),('fg','遺產分割・歸扣',tuple(range(1164,1174))),('qc','限定責任・遺產清冊',(1156,1157,1158,1159,1160,1161,1162,1163)),
 ('sw','視為所得遺產（§1148-1）',()),('wr','無人承認繼承',tuple(range(1177,1186))),('ks','繼承開始與承受',(1147,1148,1149,1150,1151,1152,1153)),('sx','順序・應繼分',(1138,1139,1141,1144))]
def grp(q):
    ks=q['law']
    if '1148-1' in ks: return 'sw'
    for code,name,rng in PRI:
        if any(int(k.split('-')[0]) in rng and k!='1148-1' for k in ks): return code
    return 'sx'
if __name__=='__main__':
    for code,name,_ in PRI:
        L=[q for q in D['q'] if q['ch']=='E4' and grp(q)==code]
        print('==',name,len(L))
        for q in L: print('  ',q['k'],q['stem'][:60],q['law'])
