# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:40:57 2018

@author: LFVARGAS


this script if for add the column commodity Id to make easy to join this data with othe data using the same entity
but sometimes with diferent name and formats

we take the raw data ./data/CMO_MSP_Mandi.csv and return a new file with the addition of the id,
sometimes words are similar but write in a different way we use Levenshtein distance to find 
the crop commodity with similar name, like soybean and soyabean, and use the same Id, when we don't
find any crop in the database similar we should consider to add this one as a new commodity
"""



import pandas as pd
import os
import re
from Levenshtein import *

#Constans
os.chdir("../data")
FILE_NAME= "CMO_MSP_Mandi"
FILE_DB_NAME="./DB/DB_Commodity"
FILE_FORMAT=".csv"
STEP="_step1"
JOIN_TYPE="left"

#MonthlyData
COLUMN_JOIN_LEFT="CommodityStandar"
COLUMN_LEFT_TRANSFORM="commodity"

#DB
COLUMN_JOIN_RIGHT="Commodity"
COLUMN_ID="CommodityId"

#TRANSFORMATIONS 
ReplaceSpaces=lambda x: x.replace(" ","_").replace("(","_").upper()
ReplaceManyByOne=lambda x: re.sub("(_)+", "_", x)
ReplaceSpecials=lambda x: re.sub("\W","", x)


DF_Month= pd.read_csv("./%s%s"%(FILE_NAME,FILE_FORMAT))
DB_Commodity= pd.read_csv("%s%s"%(FILE_DB_NAME,FILE_FORMAT))


DF_Month[COLUMN_JOIN_LEFT] = DF_Month[COLUMN_LEFT_TRANSFORM].apply(ReplaceSpaces)
DF_Month[COLUMN_JOIN_LEFT]= DF_Month[COLUMN_JOIN_LEFT].apply(ReplaceManyByOne)
DF_Month[COLUMN_JOIN_LEFT]= DF_Month[COLUMN_JOIN_LEFT].apply(ReplaceSpecials).sort_values()


## ONCE WE RUN searchClose
DF_Month[COLUMN_JOIN_LEFT]= DF_Month[COLUMN_JOIN_LEFT].replace({"SOYABEAN":"SOYBEAN"})


DF3 = DF_Month.merge(DB_Commodity, how=JOIN_TYPE, left_on=[COLUMN_JOIN_LEFT], right_on=[COLUMN_JOIN_RIGHT])

DF_Validator= DF3[DF3[COLUMN_ID].isnull()]



# TRY TO FIND THE WORD THAT IS CLOSER TO THE CURRENT COMMODITY TRANSFORMED IF IT DOESN'T EXISTIS
# PROBABLY THIS COMMODITY WOULDN'T BE IN THE DATABASE
def searchClose(x, seriesNames):
    currentMinDis=999
    currentName=""
    for item in seriesNames:
        dist=distance(x,item)
        if(dist<currentMinDis):
            currentName=item
            currentMinDis=dist
            
    return currentName
    

# all the commodities  should have and ID this is a validation 
if(len(DF_Validator)>0):
    DF_Validator["CLOSEST_WORD"]=DF_Validator[COLUMN_JOIN_LEFT].apply(lambda x: searchClose(x, DB_Commodity[COLUMN_JOIN_RIGHT]))
    print("Some commodities haven't matched with database information please review it")        
else:
    del  DF_Month[COLUMN_JOIN_LEFT]
    DF_Month[COLUMN_ID]=DF3[COLUMN_ID]
    DF_Month.to_csv("./Cleaned/%s%s%s"%(FILE_NAME,STEP,FILE_FORMAT), index=False)
    print("Matcher Commodity for monthly data was Created")


