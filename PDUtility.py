import pandas as pd 
import numpy as np 

#Generate a Class LoadUtilities
class Utilities(object):
    def __init__(self):
        pass 

    def LoadDataFrame(self,path:str,method=None,sep=None):
        #attempt to get the file extension from path
        if method == None:
            method = self.__GetFileExtension(path)
        
        #Initialise an empty dataframe
        df = pd.DataFrame()

        if method.lower() == 'csv':
            df = self.__LoadCSV(path,sep)
        elif method.lower() == 'xlsx':
            df = self.__LoadExcel(path)
        elif method.lower() == 'json':
            df = self.__LoadJSON(path)
        else:
            raise Exception(f'Invalid Method: {method} is not supported')
        return df

    def __GetFileExtension(self,path:str):
        try:
            return path.split('.')[-1]
        except:
            raise Exception(f'Invalid File Path: No Extension for {path}')

    def __LoadCSV(self,path:str,sep=',',):
        try:
            return pd.read_csv(path,sep=sep)
        except:
            raise Exception(f'Invalid File Path: {path} is not a valid CSV file')

    def __LoadExcel(self,path:str):
        try:
            return pd.read_excel(path)
        except:
            raise Exception(f'Invalid File Path: {path} is not a valid Excel file')

    def __LoadJSON(self,path:str):
        try:
            return pd.read_json(path)
        except:
            raise Exception(f'Invalid File Path: {path} is not a valid JSON file')
