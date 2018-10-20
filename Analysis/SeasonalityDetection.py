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
import matplotlib.pyplot as plt


from Commodity import Commodity
from statsmodels.tsa.seasonal import seasonal_decompose

from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step2"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId"]

DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))
DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%m-%d')

#DF_Month=DF_Month[DF_Month["CommodityId"]==26]
#DF_Month=DF_Month[DF_Month["APMC"]=="Vai"]


commodityManager=Commodity()





def viewPlotsTS(DataFrame_View):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=9999
    
    pdf= PdfPages('./Reports/CommoditiesSeasonalAnalysis.pdf')
    
    for name, group in by_group:
        
        group=group.sort_values("date")
        
        
        realName= commodityManager.getNameById(name)
        displayName=str(name)+"-"+realName
        #plt.title(str(name)+"-"+realName+"-TS Plot")
        #for this comodity which is the APMC associated
        apmcs=group["APMC"].unique()[:1]
        
        for index,item in enumerate(apmcs):
            groupFiltered=group[group["APMC"]==item]
            groupFiltered=groupFiltered.sort_values("date")
            
            groupFiltered["date"]=pd.to_datetime(group["date"])
            groupFiltered=groupFiltered.set_index("date")
            groupFiltered=groupFiltered.sort_index()
            
            groupFiltered=groupFiltered[["modal_price"]]
            
            
            
            fig, ax  = plt.subplots(figsize=(20, 8))
            ax.set_title(realName)
            FREQ= [3,6,12]   
            for ite in range(3) :
                frequency=FREQ[ite]
                result=seasonal_decompose(groupFiltered, model='additive', freq=frequency)
                result2=seasonal_decompose(groupFiltered,freq=frequency,model='multiplicative')
                
                ax1= plt.subplot(1, 3, ite+1)
                plt.plot(groupFiltered.index, groupFiltered['modal_price'], label="Original")
                plt.plot(groupFiltered.index, result.seasonal, label="Seasonal  Additive")
                plt.plot(groupFiltered.index, result2.seasonal, label="Seasonal  Multiplicative")
                ax1.set_title("%s Frequency: %s Months"%(displayName,frequency))
                ax1.legend(loc='best')
                plt.xticks(rotation=90)
        
        pdf.savefig()  # saves the current figure into a pdf page
        
        i=i+1
        
        if(i==MAX_I):
            break
    pdf.close()
    #plt.show()


viewPlotsTS(DF_Month)

#
#DF_Month["date"]=pd.to_datetime(DF_Month["date"])
#DF_Month=DF_Month.set_index("date")
#DF_Month=DF_Month.sort_index()
#
#del DF_Month["CommodityId"]
#del DF_Month["APMC"]
#del DF_Month["min_price"]
#del DF_Month["max_price"]
#del DF_Month["arrivals_in_qtl"]
##
#PERIOD=12
#DF_Month["12M_change_pct"]= DF_Month.pct_change(PERIOD)
#
#plt.clf()  # clear the plot space
#DF_Month["12M_change_pct"].plot.hist(bins=50)
#plt.xlabel('adjusted close 1-year percent change')
#plt.show()
#
#
#DF_Month['12M_future_close']=DF_Month['min_price'].shift(-PERIOD)
#
#DF_Month['12M_future_close_pct']= DF_Month['12M_future_close'].pct_change(PERIOD)


#FREQ=6
#plt.clf()  # clear the plot space
#result=seasonal_decompose(DF_Month, model='additive', freq=FREQ)
##result.plot()
#plt.show()
##
#plt.clf()  # clear the plot space
#result2=seasonal_decompose(DF_Month,freq=FREQ,model='multiplicative')
##result2.plot()
#plt.show()
#
#fig, ax  = plt.subplots()
#plt.plot(DF_Month.index, DF_Month['modal_price'], label="Original")
#plt.plot(DF_Month.index, result.seasonal, label="seasonal  additive")
#plt.plot(DF_Month.index, result2.seasonal, label="seasonal  multiplicative")
#ax.legend(loc='best')
