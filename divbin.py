import pandas as pd
import numpy as np

def crsl(bin,cdat,fdn):
    lss=[]
    ms=pd.Series([np.nan]*len(fdn),index=fdn)
    for sam in cdat: 
        ix=(sam.stt<=bin[0])&(sam.end>=bin[1])
        if(ix.any()):
            sls=sam.loc[ix,fdn].squeeze()
            lss.append(sls)
        else:
            lss.append(ms)
    return(pd.concat(lss))


def rsl(key,cdat,fdname,lines,pairs):
    bns=pd.Series()
    tls=pd.Series()
    for lg in cdat:
        bns=bns.append(lg.iloc[:,0])
        tls=tls.append(lg.iloc[:,1])
    ubn=pd.DataFrame({'pos':pd.unique(bns.values),'lab':1})
    utl=pd.DataFrame({'pos':pd.unique(tls.values),'lab':2})
    cutter=pd.concat([ubn,utl]).sort_values('pos')

    brg=pd.DataFrame(columns=['stt','end'])
    for i in range(1,cutter.shape[0]):
        cta=cutter.lab.iloc[i-1]  
        ctb=cutter.lab.iloc[i]
        if(((cta==2)&(ctb==2))):
            rst=pd.Series([cutter.pos.iloc[i-1]+10000,cutter.pos.iloc[i] ],index=['stt','end'])
            brg=brg.append(rst,ignore_index=True)
        elif(((cta==1)&(ctb==1))):
            rst=pd.Series([cutter.pos.iloc[i-1],cutter.pos.iloc[i]-10000 ],index=['stt','end'])
            brg=brg.append(rst,ignore_index=True)
        elif((cta==1)&(ctb==2)):
            rst=pd.Series([cutter.pos.iloc[i-1],cutter.pos.iloc[i] ],index=['stt','end'])
            brg=brg.append(rst,ignore_index=True)    
    brg.drop_duplicates(inplace=True)
    arg=brg.stt.tolist()
    arg.pop(0)
    arg.append(np.nan)
    crg=brg.end.tolist()
    del crg[-1]
    crg=[np.nan]+crg
    ix=(((brg.stt==crg)|(brg.stt==arg))&(brg.stt==brg.end)).tolist()
    iy=[not x for x in ix]
    brg=brg.loc[iy,:]
    cnb=brg.apply(crsl,cdat=cdat,fdn=fdname,axis=1)
    tuples=list(zip(lines,pairs,cnb.columns))
    cnb.columns=pd.MultiIndex.from_tuples(tuples)
    return (key,[brg, cnb.stack(dropna=False)])
'''end of rsl'''




