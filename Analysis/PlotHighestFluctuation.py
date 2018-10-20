# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 
This script is to show the groups with a high fluctuation
this step use Monthly_data_cmo_step3 where we create a column to save
the rate of fluctuation to monthly and frequency(inside the group) prices
finaly this file return a new file flagging every group which show a fluctuated behavior
I use the quantile 90% to take by means of the by commodity set

"""

import  os,sys
sys.path.append('../Factory')# commodity folder 

import numpy as np
import pandas as pd
from pandas.tools.plotting import autocorrelation_plot
import matplotlib.pyplot as plt


from Commodity import Commodity
from matplotlib.backends.backend_pdf import PdfPages
#Constans
os.chdir("../")#AFFECT ALL THE EXETCUTION

RELATIVE_PATH="./data/Cleaned/"

FILE_NAME= RELATIVE_PATH+"Monthly_data_cmo_step3"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId","APMC"]


DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))

DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%m-%d')


commodityManager=Commodity()


def flagMostFluctuation(DataFrame_View):
    by_group = DataFrame_View.groupby(["CommodityId"])
    
#    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
#                key=lambda x: len(x["rate_monthly_fluc"]),  # sort by number of rows (len of subDataFrame)
#                reverse=True)  # reverse the sort i.e. largest first
    dataset= None
    print(len(by_group))
    for name, group in by_group:
        rate_monthly_fluc=group["rate_monthly_fluc"]
        rate_frequency_fluc=group["rate_frequency_fluc"]
        
        LIMIT=.9
        limitMonth=rate_monthly_fluc.quantile(LIMIT)
        limitFreq=rate_frequency_fluc.quantile(LIMIT)
        
#        rate_monthly_fluc.hist(label="Month")
#        plt.show()
#        rate_frequency_fluc.hist(label="Freq")
#        plt.show()
#        print(limitMonth)
#        print(limitFreq)
        
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

def viewFlagged(DataFrame_View):  
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    pdf= PdfPages('./Reports/GroupsHighFluctuation.pdf')
    
    for name, group in by_group:
        
        isHighFreq=group["Highest_Fluctuation_Freq"].iloc[0]
        isHighMonth=group["Highest_Fluctuation_Month"].iloc[0]
        if(isHighFreq or isHighMonth):
            realName= commodityManager.getNameById(name[0])
            displayName=str(name[0])+"-"+realName
            displayName=displayName+"-"+name[1]
            
            fig, ax  = plt.subplots(figsize=(8,10))
            ax.set_title(displayName)
            
            group=group.sort_values("date")
            
            
            group["date"]=pd.to_datetime(group["date"])
            group=group.set_index("date")
            group=group.sort_index()
            
            plt.plot(group.index,group["modal_price"] , label="Series")
            
            
            ax.legend(loc='best')
            
            plt.xticks(rotation=90)
            
            
            
            
    pdf.close()
        
DF_flag=flagMostFluctuation(DF_Month)
viewFlagged(DF_flag)

