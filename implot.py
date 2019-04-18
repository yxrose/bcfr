import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt


def mtpl(x,ss):
    return x.apply(lambda y: (y.values*ss).sum())

def cvf(k,cgt,ss):
    indat=cgt.groupby(level=0).apply(mtpl,ss=ss)
    return (k,indat)

def ccvt(ddat,scode,nfd):
    ddat=np.log2(ddat)+1
    ddat.mask((ddat%1)!=0,nfd+1,inplace=True)
    ddat.mask(ddat<0,nfd+2,inplace=True)
    return ddat

def mosaic_plot(nf,chrs,nfd,fdn,csdir):
    cr=[x.shape[0] for x in nf]
    nr=sum(cr)
    tk=int((nr+300)/300)

    ypos=[]
    tt=0
    for x in cr:
        ypos.append((tt+x/2))
        tt=tt+x+tk
    
    blk=pd.Series([np.nan]*nf[0].shape[1],index=nf[0].columns)   
    blks=pd.concat([blk]*tk,axis=1) 
    ng=[pd.concat([x,blks.transpose()]) for x in nf]
    acrmat=pd.concat(ng,axis=0)
    wlr=acrmat.shape[1]/acrmat.shape[0]
    
    copan=['yellow', 'green', 'red', 'blue','gold','lime', 'pink','cyan']
    wb=['grey', 'black']
    col=copan[0:nfd]+wb
    zvals=acrmat.values
    cmap = mpl.colors.ListedColormap(col)
    bounds=[x+0.5 for x in range((nfd+3))]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    fig=plt.figure(1,figsize=(7,5))
    ax=plt.subplot(1,1,1)
    img=plt.imshow(zvals,interpolation='nearest',
                        cmap = cmap,norm=norm,aspect=wlr)
    ax.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off', # labels along the bottom edge are off
        labelleft='on'
        )
    ax.grid(False)
    
    ax.set_yticks(ypos)
    ax.set_yticklabels(chrs)
    cb=plt.colorbar(img,cmap=cmap,
                    norm=norm,boundaries=bounds)
    cb.ax.invert_yaxis()
    cb.set_ticks([x+0.5 for x in bounds])
    cb.set_ticklabels(fdn+['Non-unique', 'Missing'])
    
    plt.savefig(csdir+"whole_genome_bin_map.jpg",dpi=1000,bbox_inches='tight')


