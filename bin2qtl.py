import pickle
import pandas as pd
import os  
import numpy as np
os.chdir('e:/project/C7HBK/emhet/script')
with open('../pkls/bimDic.pkl','rb') as f:
    reg,nb=pickle.load(f)

#gt=nb['chr01']
qd=dict()
for key in nb:
   qd[key]=nb[key].groupby(level=0,axis=1).apply(lambda x: x.iloc[:,0]&x.iloc[:,1]).groupby(level=0,axis=0).apply(lambda z: z.apply(lambda y: (y*[1,2]).sum()))

with open('../pkls/rqtl_format.pkl','wb') as f:
    pickle.dump(qd,f,pickle.HIGHEST_PROTOCOL)
lst=[]
for i in range(1,13):
    key='chr%02d' %i
    bpre='bin%02d' %i
    marker=reg[key].apply(lambda x:'_'.join([bpre,str(int(x.ppa/1000)),
              str(int(x.ppb/1000))]),axis=1)
    cnm=pd.DataFrame([i]*reg[key].shape[0],index=marker.tolist(),columns=['Cumber'])
    sht=pd.concat([cnm,qd[key].set_index(marker)],axis=1).T
    lst.append(sht)
    print(marker)
    
gts=pd.concat(lst,axis=1)
gts.replace(0,np.nan,inplace=True)
gts.index = gts.index.str.upper()

F7=pd.read_csv("C7_HBK F7.csv",na_values="-")
F8=pd.read_csv("C7_HBK F8.csv",na_values='-')
F7.Number=["K"+x[3:] for x in F7.Number]
F8.Number=["K"+x[3:] for x in F8.Number]
F7.set_index('Number',inplace=True)
F8.set_index('Number',inplace=True)

pheno=F7.merge(F8,how='outer',left_index=True,right_index=True)
cross=pd.merge(pheno,gts,how='right',left_index=True,right_index=True)
cross.to_csv('CH_for_rqtl.csv',index=False)
cross.to_csv('CH_with_index.csv')
