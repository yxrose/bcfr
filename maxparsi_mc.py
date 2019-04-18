import pandas as pd

def cus(key, hac):
    ass=[]
    df=pd.DataFrame(columns=['end','stt','ssz'])
    for item in hac:
        for i in range(0,item.shape[0]-1):
            temp=item.iloc[i+1,0]-item.iloc[i,1]
            if(temp==10000):
                ass.append(item.iloc[i,1])
            elif(temp<=2000000):
                df=df.append(pd.Series([item.iloc[i,1],item.iloc[i+1,0],temp],index=['end','stt','ssz']),ignore_index=True)
    uass=pd.Series(ass).value_counts().sort_index()
    df.drop_duplicates(inplace=True)
    df.sort_values(['ssz','end'],inplace=True)
    xs=[]
    for i in range(df.shape[0]):
        ttt=int((df.iloc[i,1]+df.iloc[i,0])/2)
        iv=df.iloc[i,2]
        if(int(iv/10000)%2==0):
            xs.append(ttt)
        else:
            xs.append(ttt-5000)
    xs=pd.Series(xs)
    
    def mps(item,uxs):
        nonlocal ass
        nonlocal uass
        for i in range(0,item.shape[0]-1):
            ivs=item.iloc[i+1,0]-item.iloc[i,1]
            if((ivs==10000)|(ivs>2000000)):
                continue
            pit=uass[(uass.index>=item.iloc[i,1])& (uass.index<item.iloc[i+1,0])]
            if(pit.size==0):
                qit=uxs[(uxs>=item.iloc[i,1])& (uxs<item.iloc[i+1,0])]                
                item.iloc[i,1]=qit.iloc[0]
                item.iloc[i+1,0]=qit.iloc[0]+10000
            else:
                idm=pit.idxmax()
                item.iloc[i,1]=idm
                item.iloc[i+1,0]=idm+10000
            ass.append(item.iloc[i,1])
            uass=pd.Series(ass).value_counts().sort_index()
    for x in hac:        
        mps(x,xs)
    return (key,hac)
"""end of cus"""


