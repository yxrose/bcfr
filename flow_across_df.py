import numpy as np
import pandas as pd
from functools import partial
from multiprocessing import Pool
import os

def sliding(agt,bgt,seq):
    ss=agt==bgt
    ss[pd.isnull(agt)|pd.isnull(bgt)]=np.nan

    lst=[]
    for x in seq:
        ser=ss.loc[x[0]:x[1]]
        ix=pd.notnull(ser)
        dem=ix.sum()
        if(dem!=0):
            num=ser[ix].sum()
            ratio=num/dem
            lst.append(ratio)
        else:
            lst.append(np.nan)
    return lst
    #return pd.Series(lst,index=list(range(0,labx,step)))

def psht(fili,pig,seq,labx,step):
    xl=[]
    for i in range(pig.shape[1]):
        xl.append(sliding(pig.iloc[:,i],bgt=fili,seq=seq))
    smpi=pd.DataFrame(xl).T
    smpi.set_index([list(range(0,labx,step))],inplace=True)
    return smpi

def demn(key,nfd,mc=20,step=10000,window=50000,wkdir="./"):    
    position=pd.read_csv("".join([wkdir,"sheets/chrop_",key,".csv"]),index_col=0).POS
    t=position.tail(1)
    inv=list(range(0,int(t),step))
    mst=[]
    for x in inv:
        ab=position.index[(position>=x) & (position<x+window)]
        if not ab.empty:
            mst.append([int(ab[0]),int(ab[-1])])
        else:
            mst.append(["emp","emp"])
    
    gt=pd.read_csv("".join([wkdir,"sheets/genotype_",key,".csv"]),header=[0,1], index_col=0)
    
    pg=gt.iloc[:,range(0,(nfd*2),2)].copy()
    pg.columns=[a[0] for a in pg.columns]

    tuples=[(x[0],x[1],y) for x in gt.iloc[:,(nfd*2):] for y in pg.columns]
    ril=[gt[col_name].copy() for col_name in gt.iloc[:,(nfd*2):]]
    print("Genotype data shape on %s is (%d, %d) with %d founders, Start sliding from columns index %02d" %(key,gt.shape[0],gt.shape[1],nfd,nfd*2))
    del gt
    del position
    
    fixtri=partial(psht,pig=pg,seq=mst,labx=int(t),step=step)
    pool=Pool(processes=mc)        
    medf=pd.concat(pool.map(fixtri,ril), axis=1)
    pool.close()
    pool.join()
    
    print("%s IBS calculation finished" %key)
    cind=pd.MultiIndex.from_tuples(tuples)
    medf.columns=cind    
    return medf.stack(dropna=False)

def snow(key,win=50000,step=10000,wkdir="./"):
    pos=pd.read_csv("".join([wkdir,"sheets/chrop_",key,".csv"]),index_col=0).POS
    t=pos.tail(1)
    seq=range(0,int(t),step)
    n50k=[]
    for x in seq:
        itm=pos[(pos>=x) & (pos<x+win)]
        n50k.append(len(itm))
    return pd.Series(n50k,index=seq)
    




