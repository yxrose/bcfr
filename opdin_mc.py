import pandas as pd
from multiprocessing import Pool
from functools import partial
import time

def opdin(icb,irs,fdn):        
    for k in range(1,icb.shape[0]):
        ulk=irs.loc[icb.iloc[k-1,0]:icb.iloc[k-1,1],:]
        dbr=icb.iloc[k,:]
        if(dbr.stt-ulk.index[-1]>2000000):
            continue
        gt=dbr[fdn].astype(bool)    
        dfm=ulk[::-1]
        nr=dfm.shape[0]
        for i in range(nr):
            ix=dfm.index[i]
            row=dfm.iloc[i,:]  
            if not row.any():
                continue
            fc=gt&row
            if not (gt==fc).all():
                if (i>=(nr-1)) or not (gt&dfm.iloc[i+1,:]).any():
                    icb.iloc[k-1,1]=ix
                    break
    return icb
    "End of opdin"
def aop(key,fdname,mc,cb,rsim):
    derop=partial(opdin,fdn=fdname)
    mvp=[(cb[sht], rsim.iloc[:,sht].unstack()) for sht in range(len(cb))]
    pool=Pool(processes=mc)
    rst=pool.starmap(derop, mvp)
    pool.close()
    pool.join()
    return rst


