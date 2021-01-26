import os
import pickle
import pandas as pd
from multiprocessing import Pool

directory="./plainfile/"
if not os.path.exists(directory):
    os.makedirs(directory)

with open('../birds/pkls/bim8Dic.pkl','rb') as f:
    regDic, nbDic = pickle.load(f)

def af(x):
    tf=(not x.any()) or (pd.isnull(x).all()) or (~x.astype(bool).any())
    if(tf):
        x[:]=True
    dv=1/x.sum()
    return x*dv


def kaf(key,df):
    return (key, df.groupby(axis=1,level=0).apply(lambda indv:indv.groupby(level=0,axis=0).apply(lambda sc: af(sc.iloc[:,0])+af(sc.iloc[:,1]))).reset_index(level=0,drop=True) )


pool=Pool(processes=6)
fqDic=dict(pool.starmap(kaf,nbDic.items()))

with open('regfqDic.pkl','wb') as f:
    pickle.dump([regDic,fqDic],f,pickle.HIGHEST_PROTOCOL)

for key in fqDic:
    chr=fqDic[key]
    chr.to_csv("".join(["./plainfile/gt_",key,".txt"]),sep='\t',header=False) 

for key in regDic:
    stt=regDic[key].iloc[:,0]
    bnm=pd.Series(["".join(['bin_',str(x)]) for x in stt],index=stt.index)
    ccc=pd.Series([int(key[4:])]*stt.size,index=stt.index)
    cm=stt/250000
    mp=pd.concat([bnm,ccc,cm,stt],axis=1)
    mp.columns=['markers','chr','cm','bp']
    mp.to_csv("".join(["./plainfile/map_",key,".txt"]),sep='\t',index=False) 
