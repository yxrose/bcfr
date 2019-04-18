import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from  matplotlib.patches import Rectangle
from matplotlib import patches


def pinch(brp,bingt,nfd,fili,chrs,fdn,figdir):
    def imoc(qc,lc,xpc,clv,wd=1.5,adj=0.01):
        nonlocal ax
        qc=qc/1000000
        for i in range(qc.shape[0]):
            #print(i)
            y=qc.iloc[i,0]
            h=qc.iloc[i,1] - qc.iloc[i,0] + adj       
            lis1=lc.s1.iloc[i,:].tolist()
            lis2=lc.s2.iloc[i,:].tolist()
            col1=[x for (x,z) in zip(clv,lis1) if (z==True)]
            col2=[x for (x,z) in zip(clv,lis2) if (z==True)]
            
            if len(col1)>1:
                col1=['grey']
            elif len(col1)==0:
                col1=['black']
            if len(col2)>1:
                col2=['grey']
            elif len(col2)==0:
                col2=['black']
         
            ax.add_patch(
                Rectangle(
                    (xpc, y),   # (x,y)
                    wd/2,          # width
                    h,          # height
                    facecolor=col1[0],
                    edgecolor=None,
                    linewidth=0
                )
                
            )
            ax.add_patch(
                Rectangle(
                    (xpc+wd/2, y),   # (x,y)
                    wd/2,          # width
                    h,          # height
                    facecolor=col2[0],
                    edgecolor=None,
                    linewidth=0
                )
                
            )

    mag=dict()
    for key in bingt:
        mag[key]=bingt[key].loc[:,fili].unstack()

    copan=['yellow', 'green', 'red', 'blue','gold','lime', 'pink','cyan']
    wb=['grey', 'black']
    lcn=len(chrs)
    xpa=list(range(1,lcn*3+2,3)) 
    fig,ax = plt.subplots(1,1,figsize=(10*(lcn/12),10))     

    i=1
    for key in chrs:
        imoc(brp[key],mag[key],xpa[i],copan[0:nfd])
        ax.text(xpa[i],-1,key,va='center',fontsize=14)
        i+=1

    plt.ylim([max([int(brp[key].iloc[:,1].tail(1)) for key in brp])/1000000,0])    
    plt.xlim([2,len(chrs)*3+3])    
    plt.tick_params(
        axis='both',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',     # ticks along the bottom edge are off
        labelsize=12,
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off

    ax.text(-0.8,20,"Mb",fontsize=14,rotation=90)     
    ax.legend(fdn+['Non-unique','Missing'],
               loc=4,fontsize=12,fancybox=None,
               frameon=False
               )

    leg = ax.get_legend()
    col=copan[0:nfd]+wb
    for i in range(len(col)):
        leg.legendHandles[i].set_color(col[i])

    outfile="".join([figdir,"haplotype_",str(fili),".jpg"])
    plt.savefig(outfile,dpi=1000,bbox_inches='tight')
