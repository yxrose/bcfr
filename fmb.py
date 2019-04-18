# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 09:08:29 2018

@author: lenovo
"""
import pandas as pd
  
def fnn(y,k,er,nfd):
    m=k
    n=k
    while(m>=0):
        tu=y.iloc[m*nfd:(m*nfd+nfd)]
        if(not tu.isnull().all()):
            break
        m=m-1
    while(n<=er):
        td=y.iloc[n*nfd:(n*nfd+nfd)]
        if(not td.isnull().all()):
            break
        n=n+1
    return (tu, td)
        

      
def fmb(x,rit,dr,nfd):
    sl=[]       
    for i in range(rit.shape[0]):
        cbin=x.iloc[i*nfd:(i*nfd+nfd)]
        if(not cbin.isnull().all()):
            sl.append(cbin)
            continue
        ut,dt=fnn(x,i,dr,nfd=nfd)
        ub=rit.loc[ut.index.get_values()[0][0],:][1]
        db=rit.loc[dt.index.get_values()[0][0],:][0]
        uz= ut.reset_index(level=0,drop=True)
        dz= dt.reset_index(level=0,drop=True)
        if(db-ub>=2000000):
            sl.append(cbin)
            continue
        if( (i==0) and (dz.notnull().all()) ):
            dz.index=cbin.index
            cbin=dz
        elif( (i==dr) and (uz.notnull().all())):
            uz.index=cbin.index
            cbin=uz
        elif( (i>0) and (i <dr) and (uz==dz).all() ):
            uz.index=cbin.index
            cbin=uz
        sl.append(cbin)
    return pd.concat(sl)

def hocf(key,rit,nit,nfd):
    dr=rit.shape[0]-1  
    oit=nit.apply(fmb,rit=rit,dr=dr,nfd=nfd)  
    return (key,oit)

