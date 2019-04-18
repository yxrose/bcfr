import pickle
import os
import pandas as pd
from multiprocessing import Pool
import time

def hlg(gol,pp,scode):
    scg=gol.groupby(level=0).apply(lambda x:[(x.iloc[:,0]*scode).sum(),(x.iloc[:,1]*scode).sum()])
    ngt=pd.DataFrame(scg.tolist(),index=gol.index.levels[0])
    hbs=pd.concat([pd.DataFrame(gol.index.levels[0],index=gol.index.levels[0]),pp,ngt],axis=1)
    hbs.columns=range(0,5)
    if(len(hbs)==0):
        return [None]*(4+nfounder)
    if(hbs.shape[0]==1):
        return pd.DataFrame([hbs.iloc[0,0]]+hbs.iloc[0,:].tolist()).transpose()
    ml=[]
    ss=hbs.iloc[0,:].copy()
    ed=ss[0]
    for r in range(1,hbs.shape[0]):
        bon=hbs.iloc[r,:]
        natf1=(pd.isnull(bon[3])&pd.isnull(ss[3]))&(bon[4]==ss[4])
        natf2=(pd.isnull(bon[4])&pd.isnull(ss[4]))&(bon[3]==ss[3])
        natf3=(bon[3:5]==ss[3:5]).all()
        natf4=(pd.isnull(bon[3:5])&pd.isnull(ss[3:5])).all()
        tf=((natf1 or natf2 or natf3 or natf4) and ((bon[1]-ss[2])<50000))
        if(tf):
            ss.loc[2]=bon.loc[2]
        else:
            ml.append([ss[0],ed]+ss[1:len(ss)].tolist())
            ss=bon.copy()
        ed=bon[0]   
    ml.append([ss[0],ed]+ss[1:len(ss)].tolist())
    hif=pd.DataFrame(ml)
    return hif

    
def dilp(key,sht,cfn,lnm,scode):
    lst=[]
    for nm in lnm:
        roc=hlg(sht.loc[:,nm],cfn,scode=scode)
        lst.append(roc)
    print("finshed "+key)
    return(key,lst)















