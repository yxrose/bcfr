import pickle
import pandas as pd

idx=pd.IndexSlice

def sbs(x,ns):
    x[x<0.95]=0
    return x*ns

def cstr(faw,hq=0.99,ibd=False):
    colmax=faw.max()
    law=(faw==colmax)&(faw!=0)
    for x,nd in law.groupby(level=0,axis=1):
        stc=(nd[x].s1&nd[x].s2).sum()
        if(stc==0):
            law.loc[:,idx[x,faw[x].columns[colmax[x]<hq].tolist()]]=False
    if not ibd:
        return law
    sl=law.sum(axis=1)   
    if(sum(sl>0)>2):
        cc=law.loc[:,law.sum(axis=0)==1]
        ul=cc.T.drop_duplicates().T
        if(ul.shape[1]==2):
            law.loc[list(ul.sum(axis=1)==0),:]=False
        elif(ul.shape[1]>2):
            law.loc[list(ul.sum(axis=1)==0),:]=False
            temp=law*faw
            cser=temp.mean(axis=1)
            ki=cser.nlargest(n=2).index
            law.loc[~law.index.isin(ki)]=False    
    return(law)


def itcu(kfi,fichr,cit=None):    
    if cit is None:
        gar=fichr.groupby(level=0).apply(cstr)
    else:
        gar=pd.concat([fichr.loc[:,lines].groupby(level=0).apply(cstr,ibd=True) for lines in cit],axis=1)
    return (kfi,gar)



    
