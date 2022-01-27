import pickle
import pandas as pd
import os  
import numpy as np

CSdir=os.path.join("output_dir", '')
NUM_OF_CHROM=12

reg,nb=pd.read_pickle(CSdir+'/pkls/bimDic.pkl')

qd=dict()
for key in nb:
   qd[key]=nb[key].groupby(level=0,axis=1).apply(lambda x: x.iloc[:,0]&x.iloc[:,1]).groupby(level=0,axis=0).apply(lambda z: z.apply(lambda y: (y*[1,2]).sum()))

with open(CSdir+'/pkls/rqtl_format.pkl','wb') as f:
    pickle.dump(qd,f,pickle.HIGHEST_PROTOCOL)
    
lst=[]
for i in range(1,NUM_OF_CHROM+1):
    key='chr%02d' %i
    bpre='bin%02d' %i
    marker=reg[key].apply(lambda x:'_'.join([bpre,str(int(x.stt/1000)),
              str(int(x.end/1000))]),axis=1)
    cnm=pd.DataFrame([i]*reg[key].shape[0],index=marker.tolist(),columns=['Cumber'])
    sht=pd.concat([cnm,qd[key].set_index(marker)],axis=1).T
    lst.append(sht)
    print(marker)
    
gts=pd.concat(lst,axis=1)
gts.replace(0,np.nan,inplace=True)
gts.index = gts.index.str.upper()
gts.T.to_csv("bins.csv")
gts=gts[1:gts.shape[0]]
####gts is the genotype main part of rqtl input file. the load in to Rqtl success, need phenotype file.
###please read "cross" file format in Rqtl manual, and merge phenotype and genotype to form "cross" file. 

#pheno=pd.read_csv("your_phenotype_file.csv")
###pheno may need to be reformat as to your orgnization of your file
chrlab=gts.columns.str.replace("bin","").str.split("_").str.get(0).tolist()
sttpos=gts.columns.str.replace("bin","").str.split("_").str.get(1).tolist()
tcd=pd.DataFrame([chrlab,sttpos],columns=gts.columns)
gtplus=pd.concat([tcd,gts])

pheno=pd.DataFrame(np.random.randint(80,120,gts.shape[0]),index=gts.index,columns=["random_pheno"])
cross=pd.merge(pheno,gtplus,how='right',left_index=True,right_index=True)


cross.to_csv('CH_for_rqtl.csv',index=False)
cross.to_csv('CH_with_index.csv')
