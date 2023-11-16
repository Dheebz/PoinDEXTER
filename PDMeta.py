

import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

class Meta(object):
    def __init__(self,df:pd.DataFrame):
        self.df = df  
        self.Measure = self.Measures(df)        
    
    class Measures(object):
        def __init__(self,df:pd.DataFrame):
            self.df = df 
            self.ColCount = df.shape[1]
            self.RowCount = df.shape[0]

        def ColumnCount(self,Column):
            #Get the Count of records in the dataframe coumn
            return self.df[Column].count() 

        def ColumnUnique(self,Column):
            #Get the Count of unique records in the dataframe coumn
            return self.df[Column].nunique()

        def ColumnNull(self,Column):
            #Get the Count of null records in the dataframe coumn
            return self.df[Column].isnull().sum()
        
        def ColumnType(self,Column):
            #Get the column data type
            return self.df[Column].dtype

        def ColumnMin(self,Column):
            #return the min for columns that are numeric
            if self.ColumnType(Column) in ['int64','float64']:
                return self.df[Column].min()
            else:
                return None

        def ColumnMax(self,Column):
            #return the max for columns that are numeric
            if self.ColumnType(Column) in ['int64','float64']:
                return self.df[Column].max()
            else:
                return None


        def ColumnMean(self,Column):
            #return the mean for columns that are numeric
            if self.ColumnType(Column) in ['int64','float64']:
                return self.df[Column].mean()
            else:
                return None

        def ColumnMedian(self,Column):
            #return the median for columns that are numeric
            if self.ColumnType(Column) in ['int64','float64']:
                return self.df[Column].median()
            else:
                return None
        
        def ColumnMode(self,Column):
            #return the mode for the column 
            return self.df[Column].mode()

    def GetMeta(self):
        records = []
        smeta = self.Measure
        for column in self.df.columns:
            records.append({
                'Column':column,
                'Count':smeta.ColumnCount(column),
                'Unique':smeta.ColumnUnique(column),
                'Null':smeta.ColumnNull(column),
                'Type':smeta.ColumnType(column),
                'Min':smeta.ColumnMin(column),
                'Max':smeta.ColumnMax(column),
                'Mean':smeta.ColumnMean(column),
                'Median':smeta.ColumnMedian(column),
                'Mode':smeta.ColumnMode(column)
            })
        return pd.DataFrame(records)

    def VisualiseNulls(self):
        rtn = sns.heatmap(self.df.isnull(),yticklabels=False,cbar=False,cmap='viridis')
        plt.title('DataFrame NULL Heatmap')
        return rtn