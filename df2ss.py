import pandas as pd
import os

def creatSheet(CSdir):
    mgt=pd.read_csv(CSdir+"diploid_genotype.txt",sep='\t')
    #print("Information of variable mgt:")
    #print(mgt.info())
    mgt.CHROM=mgt.CHROM.apply(str).str.replace("chr","")
    tc=mgt.loc[:,['CHROM',"POS"]]

    gt=mgt.iloc[:,2:]
    tuples=[(a,b) for a in list(gt.columns)[::2] for b in ['s1','s2']]
    cind=pd.MultiIndex.from_tuples(tuples)
    gt.columns=cind

    clst=[]
    for x,y in tc.groupby('CHROM'):
        tok='chr%s'%x
        y.to_csv("".join([CSdir,"sheets/chrop_",tok,".csv"]))
        clst.append(tok)
    cfile=open(CSdir+"chrom_names.txt",'w')
    for x in clst:
        cfile.write("%s\n" %x)
    cfile.close()
    for m,n in gt.groupby(tc.CHROM): 
        n.to_csv("".join([CSdir,"sheets/genotype_chr",m,".csv"]))
    os.remove(CSdir+"diploid_genotype.txt")
    


