# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS


this scripts is for standarize the Commodity Code, 
We get the most of the names from the file of monthly data
to finally create the database(file) DB_Commodity.csv with an Id for each Crop Commodity

In this process we transform the names to upper case and remove special characters, to word space we use "_" as word separator  
"""

import pandas as pd
import os
import re


#Constans
os.chdir("../data")


DF_Month= pd.read_csv("./Monthly_data_cmo.csv")


DF_Month["CommodityCode"] = DF_Month["Commodity"].apply(lambda x: x.replace(" ","_").replace("(","_").upper())
DF_Month["CommodityCode"]= DF_Month["CommodityCode"].apply(lambda x: re.sub("(_)+", "_", x))
DF_Month["CommodityCode"]= DF_Month["CommodityCode"].apply(lambda x: re.sub("\W","", x)).sort_values()


Data_Commodity= DF_Month["CommodityCode"].unique()

DB_Commodity= pd.DataFrame(data=Data_Commodity, columns=["Commodity"])
DB_Commodity.index= range(1,len(DB_Commodity)+1)
DB_Commodity.to_csv("./DB/DB_Commodity.csv", index=True , index_label="CommodityId")




