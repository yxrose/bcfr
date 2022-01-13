# -*- coding: utf-8 -*
"""
Created on Sat Jan 13 18:31:50 2018

@author: lenovo
"""
import pandas as pd
import numpy as np

    
def retrench(key,cgt,rgc,nfd): 
    regout=[]
    nbout=[]
    a=range(1,rgc.shape[0])
    if len(a)==0 :
        return (key, [rgc,cgc])
    ct=cgt.iloc[a[-1]*nfd:(a[-1]*nfd+nfd),:]
    current=ct.reset_index(level=0,drop=True)
    mix=ct.index
    count=0
    for j in reversed(a):
        lt=cgt.iloc[(j*nfd-nfd):j*nfd,:]
        last=lt.reset_index(level=0,drop=True)
        if(last.isnull().all().all()):
           count=count+1
           continue
        if(((last==current)|last.isnull()|current.isnull()).all().all()):
            lmat=last.notnull()
            last=last.where(lmat,current)
            rgc.iloc[j-1,1]=rgc.iloc[j,1]
        else:
            nbout.append(current.set_index(mix))
            regout.append(rgc.iloc[j+count,:])  
            count=0
        current=last
        mix=lt.index
    nbout.append(last.set_index(lt.index))
    regout.append(rgc.iloc[0,:])
    xreg=pd.concat(regout,axis=1).transpose().sort_index()
    xnb=pd.concat(nbout).sort_index()
    return (key,[xreg,xnb])


