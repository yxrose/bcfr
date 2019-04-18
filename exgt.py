import re
import os
def pedgt(vcfname,CSdir,nfd):
    file=open(os.path.expanduser(vcfname),"r")
    wfile=open(CSdir+"diploid_genotype.txt",'w')
    for line in file:
        if line.startswith("#CHROM"):
            wd=line[1:].rstrip("\n").split('\t')
            del wd[2:9]
            print("The founders were the first %d samples in VCF file, and their names were %s" %(nfd, wd[2:(2+nfd)]))
            nwd=wd[0:2]+[x for x in wd[2:] for _ in range(2)]
            wfile.write("\t".join(nwd)+"\n")
        elif not line.startswith("#"):
            dat=line.rstrip("\n").split('\t')
            del dat[2:9]
            gt='\t'.join(dat[0:2]+[x[0:3] for x in dat[2:]])+'\n'
            pat1=r'\|'
            pat2=r'\/'
            combined_pat = r'|'.join((pat1, pat2))
            ngt=re.sub(combined_pat,"\t",gt)
            wfile.write(ngt)
    file.close()        
    wfile.close()


