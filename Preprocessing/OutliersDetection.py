# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"" 

@Description Outliers detectetion

"""

import pandas as pd
import os

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


#Constans
os.chdir("../data/Cleaned")
FILE_NAME= "Monthly_data_cmo_step1"
FILE_NAME_OUT="Monthly_data_cmo_step2"
FILE_FORMAT=".csv"
GrouperColumns=["CommodityId","APMC"]

DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))
DF_Month["date"]=DF_Month["Year"].astype(str) +"-"+ DF_Month["Month"].astype(str)
DF_Month["date"]=pd.to_datetime(DF_Month["date"], format='%Y-%B')

DF_Month=DF_Month[DF_Month["min_price"]>0]
DF_Month=DF_Month[DF_Month["max_price"]>0]
DF_Month=DF_Month[DF_Month["modal_price"]>0]


print(len(DF_Month.index))

#remove duplicates added
DF_Month=DF_Month.drop_duplicates(subset=["date","CommodityId","APMC"], keep='first')

#DF_Month=DF_Month[DF_Month["CommodityId"]==26]
#DF_Month=DF_Month[DF_Month["APMC"]=="Vai"]

def removeTsFewRecords(MyDataFrame):
    
    MyDataFrameInt=MyDataFrame.copy()
    
    DF_Count= MyDataFrameInt.groupby(["CommodityId","APMC"])["CommodityId"].count()

    count_before=len(DF_Count)

    ## filter the commodities-APMC which don't have at least 3 year of information
    filterCriterian=24.0#DF_Count.quantile(.25)
    DF_Count=DF_Count[DF_Count>=filterCriterian ]
    count_after=len(DF_Count)
    #DF_Count.plot.box()
    
    DF_Count=DF_Count.to_frame()
    DF_Count.columns=["Count"]
    
    DF_Count.reset_index(inplace=True)
    
    diff=count_before-count_after
    print("Clusters eliminated: "+ str(diff))
    #print(len(DF_Month))
    MyDataFrameInt=MyDataFrameInt.merge(DF_Count, how="inner")
    #print(len(DF_Month))
    
    return MyDataFrameInt[["date","APMC", "CommodityId", "min_price","max_price","modal_price","arrivals_in_qtl" ]]
    

def viewPlots(DataFrame_View):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=3
    for name, group in by_group:
        
        #group=group.sort_values("date")
        #plt.plot(group["date"], group['min_price'], label=name)
        #print(group)
        fig, ax  = plt.subplots(figsize=(20, 8))
        
        ax1= plt.subplot(1, 3, 1)
        plt.hist( group['min_price'])
        ax1.set_title(str(name)+"-Histogram")
        
        ax2=plt.subplot(1, 3, 2)
        plt.boxplot( group['min_price'] )
        ax2.set_title(str(name)+"-Box Plot")
        
        i=i+1
        
        if(i==MAX_I):
            break
        plt.plot(group['date'], group['min_price'], label=name)
    
    plt.show()

def removeOutliers(DataFrame_View, seriesValues):
    by_group = DataFrame_View.groupby(GrouperColumns)
    
    by_group=sorted(by_group,  # iterates pairs of (key, corresponding subDataFrame)
                key=lambda x: len(x[1]),  # sort by number of rows (len of subDataFrame)
                reverse=True)  # reverse the sort i.e. largest first
    
    i=0
    MAX_I=3
    THRESHOLD=2
    
    valuesNotOutliers=[]
    for name, group in by_group:
        #print(group)
        
        mean=group[seriesValues].mean()
        std=group[seriesValues].std()
        
        
        smaller=mean-THRESHOLD*std
        bigger=mean+THRESHOLD*std
        
#        print("set"+str(name))
#        print(mean)
#        print(std)
#        print(smaller)
#        print(bigger)
#        print(group.describe())
#        
        #print(len(group))
        group=group.query('@smaller <= %s <= @bigger'%(seriesValues))
        #print(len(group))
        
        if(len(valuesNotOutliers)==0):
            valuesNotOutliers = group.values
        else:
            valuesNotOutliers=np.concatenate((valuesNotOutliers,group.values))
        i=i+1
        #if(i==MAX_I):
            #print(valuesNotOutliers)
            #break
    
    resultDF=pd.DataFrame(valuesNotOutliers, columns=DataFrame_View.columns)
    
    
    for x in DataFrame_View.columns:
        resultDF[x]=resultDF[x].astype(DataFrame_View[x].dtypes.name)
        
    return resultDF
    
    
#viewPlots(DF_Explorer)

print(len(DF_Month.index))
DF_Explorer=removeTsFewRecords(DF_Month)
print(len(DF_Explorer.index))
DF_Explorer2=removeOutliers(DF_Explorer,"min_price")
print(len(DF_Explorer2.index))
DF_Explorer2=removeOutliers(DF_Explorer2,"max_price")
print(len(DF_Explorer2.index))
DF_Explorer2=removeOutliers(DF_Explorer2,"modal_price")
print(len(DF_Explorer2.index))
#DF_Explorer2=removeOutliers(DF_Explorer,"arrivals_in_qtl")
#print(len(DF_Explorer2.index))

DF_Explorer2=removeTsFewRecords(DF_Explorer2)
#viewPlots(DF_Explorer)

print("Explorer 2")

#DF_Month=DF_Month[DF_Month["APMC"]=="Satara"]
#DF_Month=DF_Month[DF_Month["CommodityId"]==27]

#viewPlots(DF_Explorer2)

DF_Explorer2.to_csv("./%s%s"%(FILE_NAME_OUT,FILE_FORMAT), index=False)
#DF_Explorer.plot()
#del DF_Explorer['CommodityId']
#del DF_Explorer['APMC']
#
#DF_SeparatedSeries=DF_Explorer[["APMC", "CommodityId"]].drop_duplicates()








