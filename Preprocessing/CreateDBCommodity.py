# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS
"""

import pandas as pd
import numpy as np
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


#CommodityByMonth=DF_Month["Commodity"].unique()
#CommodityByMonth.sort()



