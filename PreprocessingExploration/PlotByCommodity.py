# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

This a simple report script for visualize all the crops commodities join in one graphic all the 
instutions that sell this product, then two study how is the general behavior of each crop

the results were tree pdf reports CommoditiesTS_<var_name>.pdf
Crops are ordered by the number of records, descending so you will see the most populated in the first plot
"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import pandas as pd
import matplotlib.pyplot as plt


from Commodity import Commodity

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
#DF_Month=DF_Month[DF_Month["APMC"]=="Barshi"]


commodityManager=Commodity()





def viewPlotsTS(DataFrame_View,myColumnValue):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=99999
    
    
    
    pdf= PdfPages('./Reports/CommoditiesTS_%s.pdf'%(myColumnValue))
    
    for name, group in by_group:
        
        group=group.sort_values("date")
        
        
        fig, ax  = plt.subplots(figsize=(20, 8))
        
        realName= commodityManager.getNameById(name)
        plt.title(str(name)+"-"+realName+"-TS Plot")
        #for this comodity which is the APMC associated
        apmcs=group["APMC"].unique()[:15]
        
        for index,item in enumerate(apmcs):
            groupFiltered=group[group["APMC"]==item]
            groupFiltered=groupFiltered.sort_values("date")
            plt.plot(groupFiltered["date"], groupFiltered[myColumnValue], label=item)   
            
        ax.legend(loc='best')
        
        
        pdf.savefig()  # saves the current figure into a pdf page
        
        
        i=i+1
        
        if(i==MAX_I):
            break
        
    pdf.close()
    #plt.show()


viewPlotsTS(DF_Month,"min_price")
viewPlotsTS(DF_Month,"max_price")
viewPlotsTS(DF_Month,"modal_price")