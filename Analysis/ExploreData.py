# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

@Description Outliers detectetion

"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import numpy as np
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
import matplotlib.pyplot as plt


from Commodity import Commodity
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
#from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step2"
FILE_NAME_2= RELATIVE_PATH+"CMO_MSP_Mandi_step1"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId","APMC"]

FILE_OUT= RELATIVE_PATH+"Monthly_data_cmo_step3"

DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))

DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%m-%d')

#DF_Month=DF_Month[DF_Month["CommodityId"]==26]
#DF_Month=DF_Month[DF_Month["APMC"]=="Vai"]


commodityManager=Commodity()

def testStationary(TimeSeries):
    #print("Result of Dickey Fullier Test")
    
    
    TimeSeries=TimeSeries.dropna()
    dftest=adfuller(TimeSeries, autolag="AIC")
    dfoutput= pd.Series(dftest[0:4], index=["Test Stat","P-Value","#Lags Used", "Number of Observarions"])
    
    for key,value in dftest[4].items():
        dfoutput["Critical Value: %s"%key]=value
    #print("P-value",dfoutput["P-Value"])
    
    return dfoutput["P-Value"]
            


def SeasonalityColumnRemove(DataFrame_View):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=999
    
    #pdf= PdfPages('./Reports/CommoditiesSeasonalAnalysis.pdf')
    
    dataset=None
    
    
    countUmbral=0
    countAllGroups=len(by_group)
    for name, group in by_group:
        
        
        group=group.sort_values("date")
        
        #plt.title(str(name)+"-"+realName+"-TS Plot")
        #for this comodity which is the APMC associated
        
        
        group["date"]=pd.to_datetime(group["date"])
        group=group.set_index("date")
        group=group.sort_index()
        
       
        
        #SELECTED 
        TYPE="additive"
        FREQ= [1,3,6,12]
        #frequency=FREQ
        ts_price=group["modal_price"]
        ts_price_log=np.log(group["modal_price"])
        
        ts_price_used=ts_price_log
        
        print("######## New Item %d %s #############"%(name))
        testStationary(ts_price)
        
        THRESHOLD_pvalue=0.3
        currentP=99
        currentFreq=99
        
        
        
        for frequency in FREQ:
            #print("*********This is for %d***************"%frequency)
        
            ts_price_freq_mean=ts_price_used.rolling(frequency).mean()
            ts_price_freq_std=ts_price_used.rolling(frequency).std()
            
            result=seasonal_decompose(ts_price, freq=frequency)
            
            
            # remove seasonality and trend
            group["modal_price_nostationary_ma"]=ts_price_used- ts_price_freq_mean
                 
            
            group['log_ret_monthly'] = np.log(group["modal_price"]) - np.log(group["modal_price"].shift(1))
            group['log_ret_frequency'] = np.log(group["modal_price"]) - np.log(group["modal_price"].shift(frequency))
            
            #group["modal_price_nostationary_diff"]=group["modal_price"]-  group["modal_price"].shift(1)- group["modal_price"].shift(frequency)
            
  
            localP=testStationary(group["modal_price_nostationary_ma"])
            #localP=testStationary(group["modal_price_nostationary_diff"])
            
            if(localP<currentP):
                currentP=localP
                currentFreq=frequency
        
        
                #Commodity Frequency Fluctuation
                group['rate_monthly_fluc']=np.mean(group['log_ret_monthly']**2)
                
                #Monthly Frequency Fluctuation
                group['rate_frequency_fluc']=np.mean(group['log_ret_frequency']**2)
                
                
            
            
        del group['log_ret_monthly']
        del group['log_ret_frequency'] 
        
        group["Frequenc_Seasonality"]= currentFreq   
        print("Best P Value::::::")
        print("P-value",currentP)
        print("Frequency",currentFreq)
        
        if(currentP > THRESHOLD_pvalue):
            countUmbral += 1
       
            group.reset_index(level=0, inplace=True)
            if dataset is None:
               dataset=group
            else: 
               dataset=dataset.append(group, ignore_index=True) 
#           
        i=i+1
        
        if(i==MAX_I):
            break
    
    
    print("didn't pass the Test of Stationary::",countUmbral)
    print("Total Groups ::",countAllGroups)
    
    
    #Step3
    dataset.to_csv("./%s%s"%(FILE_OUT,FILE_FORMAT), index=False)
    
    return dataset

def flagMostFluctuation(DataFrame_View):
    by_group = DataFrame_View.groupby(["Commodity"])
    
#    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
#                key=lambda x: len(x["rate_monthly_fluc"]),  # sort by number of rows (len of subDataFrame)
#                reverse=True)  # reverse the sort i.e. largest first
    dataset= None
    for name, group in by_group:
        rate_monthly_fluc=group["rate_monthly_fluc"]
        rate_frequency_fluc=group["rate_frequency_fluc"]
        
        LIMIT=.7
        limitMonth=rate_monthly_fluc.quantile(LIMIT)
        limitFreq=rate_monthly_fluc.quantile(LIMIT)
        
        def comparable(x,y):
            if(x>y):
                return True
            else:
                return False
        
        group["Highest_Fluctuation_Month"]=rate_monthly_fluc.apply(lambda x: comparable(x,limitMonth))
        group["Highest_Fluctuation_Freq"]=rate_frequency_fluc.apply(lambda x: comparable(x,limitFreq))
        
        if dataset is None:
            dataset=group
        else: 
            dataset=dataset.append(group, ignore_index=True) 
               
    return dataset   
        
SeasonalityColumnRemove(DF_Month)

#DF_Season= pd.read_csv("./%s%s"%(FILE_OUT,FILE_FORMAT))

#DF_Season_Flag=flagMostFluctuation(DF_Season)

