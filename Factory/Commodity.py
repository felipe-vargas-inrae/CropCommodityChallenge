class Commodity:
    'Common base class for all Commodities'
    empCount = 0
    Db={}
    
    FILE="./data/DB/DB_Commodity.csv"
    KEY="CommodityId"
    VALUE='Commodity'
    
    def __init__(self):
        import pandas as pd  
        import os
        print(os.getcwd())
        
       
        
        DbDf=pd.read_csv(self.FILE)
        DbDf=DbDf.set_index(self.KEY)
        self.Db=DbDf.to_dict('index') 
        
        for k, v in self.Db.items():
            self.Db[k] = v[self.VALUE]
        
    def getNameById(self,id):
        return self.Db[id]
    
    def getCount(self):
        return self.empCount
            
       
     