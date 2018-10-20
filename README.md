# Crop Commodity Challenge

Social Crop challenge was about time series data, 
actually stock prices of agriculture commodities. 
Many crops and  APMC (Agricultural produce market committee)/mandi were collected with information about monthly price fluctuation.

The main tasks were:
* Data Preparation: remove outliers, missing, and duplicates, create Ids and standarize join columns like Commodity
* Data Exploration: view the behavior of the time series data, and plot it for better understand
* Data Analysis: Study time series data, try to guess seasonal behavior over many groups of commodity, APMC

For further information go to file Documents/Report.pdf
For definitions and data explanation go to file Documents/Definitions.pdf

# How to run the code?

The  scripts must be executed in a sequencial order because one step depends of others

## First 

Go to Folder Preprocesing an run 
```
 python OutliersDetection.py
 python PlotByCommodity.py
```

this commands will create these files:
```
data/Cleaned/Monthly_data_cmo_step2.csv
data/Reports/CommoditiesTS_modal_price.pdf
data/Reports/CommoditiesTS_min_price.pdf
data/Reports/CommoditiesTS_max_price.pdf
```

## Next Step 
Go to folder Analysis and run 
```
 python PlotSeasonalityDetection.py
```

this commands will create these files:
```
./Reports/CommoditiesSeasonalAnalysis.pdf
```

This report was useful to see the general behavior of the data 
moving the frequency value of seasonal component, for all the groups 
is shown three plots for quarterly, bianual, and anual, which is better for this specific group?,
in this plot you can see the seasonal component for an additive model and for a multiplicative model

## Next Step 
Continue in the folder Analysis and run 
```
 python SeasonalInferenceFrequency.py
```
this commands will create these files:
```
./data/Cleaned/Monthly_data_cmo_step3.csv
```
This file contains the dataset with frequency selected using a model for validation, 
and two rows for understanding fluctuations

## Finally run 

Continue in the folder Analysis and run 
```
 python PlotSeasonalDecomPriceSupport.py
 PlotSeasonalityDetection.py
```
Both scripts use the step3 data and the PlotSeasonalDecomPriceSupport file also use CMO_MSP_Mandi_step1.csv
for join combination to show price support compared with series

## Notebook
If you want to see a step by step explanation go to folder notebook an open the file 

# Versions of package
```
Python 3.6.0 :: Anaconda custom (64-bit)
numpy                              1.13.3
pandas                             0.22.0
matplotlib                         2.2.2
Levenshtein                        0.12.0
statsmodels                        0.9.0
```
