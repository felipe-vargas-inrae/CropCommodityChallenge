# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

This script is for showing the relationship between some commodities 
and the support price, and to visualize the deseasonalize data

"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from Commodity import Commodity

from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step3"
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
    MAX_I=99999
    
    pdf= PdfPages('./Reports/GroupsSupporPriceAnalysis.pdf')
    
    dataset=None
    
    for name, group in by_group:
        
        realName= commodityManager.getNameById(name[0])
        displayName=str(name[0])+"-"+realName
        displayName=displayName+"-"+name[1]
                       
        group=group.sort_values("date")
        
        #plt.title(str(name)+"-"+realName+"-TS Plot")
        #for this comodity which is the APMC associated
        
        
        group["date"]=pd.to_datetime(group["date"])
        group=group.set_index("date")
        group=group.sort_index()
        
        # get minimum support price by year 
        
        
        DF_LocalPrice=DF_SupportPrice[DF_SupportPrice["CommodityId"]==name[0]]
        
        if(len(DF_LocalPrice)==0):
            break
        
        DF_LocalPrice["date"]=pd.to_datetime(DF_LocalPrice["date"])
        DF_LocalPrice=DF_LocalPrice.set_index("date")
        DF_LocalPrice=DF_LocalPrice.sort_index()
        
        
        minDate=group.index.min()
        maxDate=group.index.max()
        
        DF_LocalPrice=DF_LocalPrice.loc[minDate:maxDate]
        
        
        
        supportPrice_TS=np.log(DF_LocalPrice["msprice"])
        
        
        #SELECTED 
        TYPE="additive"
        FREQ= 12
        frequency=group["Frequenc_Seasonality"].iloc[0]
        print(frequency)
        
        ts_price_log=np.log(group["modal_price"])
        
        
        ts_price_freq_mean=ts_price_log.rolling(frequency).mean()
        ts_price_freq_std=ts_price_log.rolling(frequency).std()
     
        
        
        group["modal_price_nostationary"]=ts_price_log - ts_price_freq_mean
        
        fig, ax  = plt.subplots(figsize=(8,15))
        ax.set_title(displayName)
        plt.plot(group.index,ts_price_log , label="Series")
        plt.plot(group.index,group["modal_price_nostationary"], label="No Season- No Trend Moving Average" ) 

        ts_price_freq_mean.plot(label="%s month rolling mean"%frequency)
        ts_price_freq_std.plot(label="%s month rolling std"%frequency)
        supportPrice_TS.plot(label="Minimum Support Price")
        #print(ts_price)
        #autocorrelation_plot(ts_price)
        
        ax.legend(loc='best')
        
        plt.xticks(rotation=90)
        
        
        pdf.savefig()  # saves the current figure into a pdf page
        
        group.reset_index(level=0, inplace=True)
        if dataset is None:
           dataset=group
        else: 
           dataset=dataset.append(group, ignore_index=True) 
#           
        i=i+1
        
        if(i==MAX_I):
            break
    pdf.close()
    
    return dataset
    #pdf.close()
    #plt.show()


DF_Season=SeasonalityColumnRemove(DF_Month)

