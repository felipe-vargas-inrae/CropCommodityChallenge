# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

@Description Outliers detectetion

"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
import matplotlib.pyplot as plt


from Commodity import Commodity
from statsmodels.tsa.seasonal import seasonal_decompose

#from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step2"
FILE_NAME_2= RELATIVE_PATH+"CMO_MSP_Mandi_step1"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId","APMC"]


DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))

DF_SupportPrice= pd.read_csv("./%s%s"%(FILE_NAME_2,FILE_FORMAT))

DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%m-%d')

DF_SupportPrice["date"]=pd.to_datetime(DF_SupportPrice["year"], format='%Y')

#DF_Month=DF_Month[DF_Month["CommodityId"]==26]
#DF_Month=DF_Month[DF_Month["APMC"]=="Vai"]


commodityManager=Commodity()



def SeasonalityColumnRemove(DataFrame_View):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=1
    
    #pdf= PdfPages('./Reports/CommoditiesSeasonalAnalysis.pdf')
    
    dataset=None
    
    for name, group in by_group:
        
        
        group=group.sort_values("date")
        
        #plt.title(str(name)+"-"+realName+"-TS Plot")
        #for this comodity which is the APMC associated
        
        
        group["date"]=pd.to_datetime(group["date"])
        group=group.set_index("date")
        group=group.sort_index()
        
        # get minimum support price by year 
        
        
        DF_LocalPrice=DF_SupportPrice[DF_SupportPrice["CommodityId"]==name[0]]
        
        DF_LocalPrice["date"]=pd.to_datetime(DF_LocalPrice["date"])
        DF_LocalPrice=DF_LocalPrice.set_index("date")
        DF_LocalPrice=DF_LocalPrice.sort_index()
        
        
        minDate=group.index.min()
        maxDate=group.index.max()
        
        DF_LocalPrice=DF_LocalPrice.loc[minDate:maxDate]
        
        print(minDate)
        print(maxDate)
        print(DF_LocalPrice)
        
        supportPrice_TS=DF_LocalPrice["msprice"]
        
        
        #SELECTED 
        TYPE="additive"
        FREQ= 12
        frequency=FREQ
        
        
        ts_price=group["modal_price"]
        
        
        ts_price_12_mean=ts_price.rolling(frequency).mean()
        ts_price_12_std=ts_price.rolling(frequency).std()
        
        result=seasonal_decompose(ts_price, freq=frequency)
        #result.plot()
#        print(group.dtypes)
#        print(group)
#        print("SEASONAL")
        #print(result.seasonal)
        
        columnNameFuture=str(frequency)+"_past"
        
        
                          
        group[columnNameFuture]=group["modal_price"].shift(frequency)
        #group[columnNameFuture]=  group[columnNameFuture].fillna(0)
        
        group["modal_price"].shift(1) 
        
        # remove seasonality and trend
        group["modal_price_noseason"]=group["modal_price"] - group[columnNameFuture] 
        #group["modal_price_notrend"]=group["modal_price"] - group["modal_price"].shift(1) 
        
        group["modal_price_nostationary"]=group["modal_price_noseason"]-  group["modal_price"].shift(1)
        
        
        fig, ax  = plt.subplots(figsize=(8,8))
        plt.plot(group.index,group["modal_price"] , label="Series")
        plt.plot(group.index,group["modal_price_nostationary"], label="No Season- No Trend" ) 

        ts_price_12_mean.plot(label="12 month rolling mean")
        ts_price_12_std.plot(label="12 month rolling std")
        supportPrice_TS.plot(label="Minimum Support Price")
        #print(ts_price)
        #autocorrelation_plot(ts_price)
        
        ax.legend(loc='best')
        plt.xticks(rotation=90)
        plt.show()
        
        group.reset_index(level=0, inplace=True)
        if dataset is None:
           dataset=group
        else: 
           dataset=dataset.append(group, ignore_index=True) 
#           
        i=i+1
        
        if(i==MAX_I):
            break
        
    return dataset
    #pdf.close()
    #plt.show()


DF_Season=SeasonalityColumnRemove(DF_Month)

