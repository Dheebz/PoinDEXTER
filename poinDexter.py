import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns


class Fill(object):
    def __init__(self,DataFrame:pd.DataFrame):
        self.DataFrame = DataFrame

    def FillColumnWithValue(self,ColumnName:str,FillValue):
        self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(FillValue)
        return (self.DataFrame)

    def FillColumnWithMethod(self,ColumnName:str,Method:str):
        Method = Method.upper()
        if Method == 'MEAN':
            self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(self.DataFrame[ColumnName].mean())
        elif Method == 'MEDIAN':
            self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(self.DataFrame[ColumnName].median())
        elif Method == 'MODE':
            self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(self.DataFrame[ColumnName].mode())
        elif Method == 'MIN':
            self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(self.DataFrame[ColumnName].min())
        elif Method == 'MAX':
            self.DataFrame[ColumnName] = self.DataFrame[ColumnName].fillna(self.DataFrame[ColumnName].max())
        else:
            Exception(f'Method "{Method}" Not Recognised')
        return (self.DataFrame)

    def FillColumnWithMethodGroupedBy(self,ColumnName:str,GroupedBy:list,Method:str):
        Method = Method.upper()
        if Method == 'MEAN':
            self.DataFrame[ColumnName] = self.DataFrame.groupby(GroupedBy)[ColumnName].transform(lambda x: x.fillna(x.mean()))
        elif Method == 'MEDIAN':
            self.DataFrame[ColumnName] = self.DataFrame.groupby(GroupedBy)[ColumnName].transform(lambda x: x.fillna(x.median()))
        elif Method == 'MODE':
            self.DataFrame[ColumnName] = self.DataFrame.groupby(GroupedBy)[ColumnName].transform(lambda x: x.fillna(x.mode()))
        elif Method == 'MIN':
            self.DataFrame[ColumnName] = self.DataFrame.groupby(GroupedBy)[ColumnName].transform(lambda x: x.fillna(x.min()))
        elif Method == 'MAX':
            self.DataFrame[ColumnName] = self.DataFrame.groupby(GroupedBy)[ColumnName].transform(lambda x: x.fillna(x.max()))
        else:
            Exception(f'Method "{Method}" Not Recognised')
        return (self.DataFrame)

    


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
        #Return a seaborn heatmap of the null records 
        return sns.heatmap(self.df.isnull(),yticklabels=False,cbar=False,cmap='viridis')


class PaletteMaker(object):
    def __init__(self,SeedColor,Steps,PaletteType:str):
        self.HexSeed = SeedColor
        self.RGBSeed = colors.hex2color(self.HexSeed)
        self.HSVSeed = colors.rgb_to_hsv(self.RGBSeed)
        self.Steps = Steps
        self.StepSize = (1.0 / self.Steps)
        self.PaletteType = PaletteType.upper()
        self.Palette = []
        self.PaletteBar = None

    def MakePalette(self):
        if self.PaletteType == 'MONOCHROMATIC':
            self.Palette = self._MakeMonochromatic()
        elif self.PaletteType == 'ANALOGOUS':
            self.Palette = self._MakeAnalogous()
        elif self.PaletteType == 'COMPLEMENTARY':
            self.Palette = self._MakeComplementary()
        elif self.PaletteType == 'TRIADIC':
            self.Palette = self._MakeTriadic()
        elif self.PaletteType == 'TETRADIC':
            self.Palette = self._MakeTetradic()
        elif self.PaletteType == 'SHADE':
            self.Palette = self._MakeShade()
        else:
            #Raise Excpetion Pallete Tpe not Recognised
            Exception(f'Palette Type "{self.PaletteType}" Not Recognised')
        return self.Palette
    

    def _MakeMonochromatic(self):
        self.Palette = []
        ind = 0
        while len(self.Palette) < self.Steps:
            H = self.HSVSeed[0]
            S = self.HSVSeed[1]
            V = 0 + (ind*self.StepSize)
            HSV = (H,S,V)
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        return (self.Palette)


    def _MakeAnalogous(self):
        self.Palette = []
        ind = 0
        while len(self.Palette) < self.Steps:
            H = 0 + (ind * self.StepSize)
            S = self.HSVSeed[1]
            V = self.HSVSeed[2]
            HSV = (H,S,V)
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        return (self.Palette)


    def _MakeComplementary(self):
        self.Palette = []
        ind = 0 
        while len(self.Palette) < self.Steps:
            H = 0.5 + (ind * self.StepSize)
            S = self.HSVSeed[1]
            V = self.HSVSeed[2]
            HSV = (H,S,V)
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        #unique self.palette
        return (self.Palette)

    def _MakeTriadic(self):
        self.Palette = []
        ind = 0
        while len(self.Palette) < self.Steps:
            H = 0.33 + (ind * self.StepSize)
            S = self.HSVSeed[1]
            V = self.HSVSeed[2]
            HSV = (H,S,V)
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        return (self.Palette)


    def _MakeTetradic(self):
        self.Palette = []
        ind = 0
        while len(self.Palette) < self.Steps:
            H = 0.25 + (ind * self.StepSize)
            S = self.HSVSeed[1]
            V = self.HSVSeed[2]
            HSV = (H,S,V)
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        return (self.Palette)

    def _MakeShade(self):
        self.Palette = []
        ind = 0
        while len(self.Palette) < self.Steps:
            H = self.HSVSeed[0]
            S = 0 + (ind * self.StepSize)
            V = self.HSVSeed[2]
            HSV = (H,S,V)
        
            self.Palette.append(colors.hsv_to_rgb([H,S,V]))
            ind += 1
        return (self.Palette)

    def ShowPalette(self):
        self.MakePalette()
        #Add Palette Type to Title
        self.PaletteBar = sns.palplot(self.Palette)
        plt.title(self.PaletteType)
        return self.PaletteBar
    
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
