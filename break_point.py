import pandas as pd
from multiprocessing import Pool
from functools import partial
import time


def fick(costr,key,fdn,snkDic):
    flag=[True]*len(fdn)
    stt=0
    end=0
    lix=0
    ix=["stt","end"]+fdn
    hapin=pd.DataFrame(columns=ix)
    nr=costr.shape[0]
    for i in range(nr):
        index=costr.index[i]
        row=costr.iloc[i,:]   
        if not row.any():
            continue
        if((index-lix>2000000)):
            end=lix
            hapin=hapin.append(pd.Series([stt]+[end]+list(flag),index=ix),ignore_index=True)
            stt=index
            flag=row        
        else:       
            fcj=flag&row
            if not fcj.any():
                if (i<(nr-1)) and  (flag&costr.iloc[i+1,:]).any():
                    #print("%d  %d"%(nr, i))
                    continue

                end=lix
                hapin=hapin.append(pd.Series([stt]+[end]+list(flag),index=ix),ignore_index=True)
                stt=index
                flag=row
            else:
                flag=fcj
        lix=index    
    hapin=hapin.append(pd.Series([stt]+[index]+list(flag),index=ix),ignore_index=True)
    hapin=pd.merge(hapin,pd.DataFrame(snkDic[key].loc[list(hapin.stt)]),how="left",left_on="stt",right_index=True)
    return hapin 



def gick(kch,sht,mc,fdname,sinfo):
    input_list= [sht.loc[:,x].unstack() for x in  sht]
    fixtwo=partial(fick,key=kch,fdn=fdname,snkDic=sinfo)

    start_time=time.time()
    pool=Pool(processes=mc)
    bkil=pool.map(fixtwo,input_list)
    pool.close()
    pool.join()
    print("--- %s: %s seconds ---" %(kch, time.time()-start_time))    
    return bkil

