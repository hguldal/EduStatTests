import pandas as pd
import numpy as np
from scipy.stats import *

def LoadFromCSV(CSVPath):
  return pd.read_csv(CSVPath)

def LoadFromDict(dictData):
  return pd.DataFrame(dictData)

def LoadFromExcel(ExcelPath):
    return pd.read_csv(ExcelPath)

""" Pearson's, Spearman's and  D'Agostino's correlation test
Parameters (Input):
===================================================================================
df*        : Pandas DataFrame

*: Required Parameter

Return (Output):
===================================================================================
Type: dictionary
Description: Pearson's, Spearman's and  Kendall's correlation tests stats
"""

def Correlation(df):

  if df is None:
    raise Exception("No data loaded")

  pearsonCrls,spearmanCrls,kendallCrls =[],[],[]
 
  for column1 in df.columns:
   
    for column2 in df.columns:
 
      stat,p=pearsonr(df[column1], df[column2])
   
      resObj={
        column1 + "_" + column2:{
          "correlation":stat,
          "p":p
          }
        }
   
      pearsonCrls.append(resObj)

      stat, p = spearmanr(df[column1], df[column2])
   
      resObj={
        column1 + "_" + column2:{
        "correlation":stat,
        "p":p
        }
      }
   
      spearmanCrls.append(resObj)

      stat, p = kendalltau(df[column1], df[column2])
      
      resObj={
        column1 + "_" + column2:
        {
          "correlation":stat,
          "p":p
          }
      }
      
      kendallCrls.append(resObj)
  
  return {
      "TestName":"correlation",
      "Pearsons":pearsonCrls,
      "Spearmans":spearmanCrls,
      "Kendalls":kendallCrls
      }

""" Kolmogorov-Smirnov, Shapiro-Wilk and  D'Agostino's Normality Tests
Parameters (Input):
===================================================================================
df*        : Pandas DataFrame

*: Required Parameter

Return (Output):
===================================================================================
Type: dictionary
Description: Kolmogorov-Smirnov, Shapiro-Wilk and  D'Agostino's tests normality stats
"""
def Normality(df):

  if df is None:
    raise Exception("No data loaded")
  
  kolmogorovSmirnov,shapiroWilk,dAgostino =[],[],[]

  for column in df.columns:

    data=df[column]
    
    #Perform to Kolmogorov-Smirnov normality test
    stat,p=kstest(data, 'norm')

    resObj={
      column:{
          "normality":stat,
          "p":p
        }
      }

    kolmogorovSmirnov.append(resObj)
    
    #Perform to Shapiro normality test
    stat,p=shapiro(data)

    resObj={
      column:{
        "normality":stat,
        "p":p
        }
      }

    shapiroWilk.append(resObj)
    
    #Perform to D' Agostino's normality test
    stat,p=normaltest(data) 

    resObj={
      column:{
        "normality":stat,
        "p":p
        }
      }

    dAgostino.append(resObj)
    

  #return the results 
  return {
      'TestName':'normality',
      'KolmogorovSmirnov':kolmogorovSmirnov,
      'ShapiroWilk':shapiroWilk,
      'DAgostino':  dAgostino
      }

""" Independent T-Test
Parameters (Input):
==================================================
df        : Pandas DataFrame

variable1*: string
                Independent variable (X)
                Name of DataFrame column object

variable2*: string
                Dependent variable (Y)
                Name of DataFrame column object

*: Required Parameter

Return (Output):
===================================================
Type: dictionary
Description: T-Test Stats
"""
def IndTTest(df,variable1,variable2):

  if df is None:
    raise Exception("No data loaded")

  if len(df[variable1].value_counts().index)>2:
    raise Exception("The number of groups cannot be greater than 2")

  # Create a dictionary object for the store data and etc.
  dataCollection=dict()

  # Extract the groups from DataFrame and put into the dataCollection dictionary object
  for idx in df[variable1].value_counts().index:
    dataCollection[idx]={"data":df.query(variable1 + "==" + str(idx))[variable2]}

  # Extract the raw data from dictionary object to pass scipy.stats functions
  rawData=list()
  for item in dataCollection:
    rawData.append(dataCollection[item]["data"])

  data1,data2=rawData[0],rawData[1]

  # Calculate Indepentend T-Test
  result1 = ttest_ind(data1, data2)

  # Calculate Levent Test
  result2=levene(data1, data2,center='mean')

  # Calculate Indepentend Welch Test
  result3= ttest_ind(data1, data2,equal_var = False)

  # Calculate Degree of Freedom score
  dofF=len(data1)+len(data2)-2

  # Calculate group descriptive statistics
  groupStats=list()
  for item in dataCollection:
    group=dict()
    group[item]={"N":dataCollection[item]["data"].count(),
                   "Mean":dataCollection[item]["data"].mean(),
                   "StdDev":dataCollection[item]["data"].std(),
                   "StdErr": dataCollection[item]["data"].sem()
    }
    groupStats.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        "TestName":"indt",
        # Groups statistics
        "groupStats":groupStats,

        # T-Test results
        "TTest":{
            "t":result1[0],
            "df":dofF,
            "sigTwoTailed":result1[1]
        },

        # Levene test results
        "LeveneTest":
        {
         "F":result2[0],
         "sigTwoTailed":result2[1]

        },

        # Welch test results
        "WelchTest":{
            "t":result3[0],
            "sigTwoTailed":result3[1]
        }
  }

  return dictReturn


""" Mann-Whitney U Test
Parameters (Input):
==================================================
df        : Pandas DataFrame

variable1*: string
                Independent variable (X)
                Name of DataFrame column object

variable2*: string
                Dependent variable (Y)
                Name of DataFrame column object

*: Required Parameter

Return (Output):
===================================================
Type: dictionary
Description: Mann-Whitney U Test Stats
"""
def MannWhitneyU(df,variable1,variable2):

  if df is None:
    raise Exception("No data loaded")

  if len(df[variable1].value_counts().index)>2:
    raise Exception("The number of groups cannot be greater than 2")

  # Create a dictionary object for the store data and etc.
  dataCollection=dict()

  # Extract the groups from DataFrame and put into the dataCollection dictionary object
  for idx in df[variable1].value_counts().index:
    dataCollection[idx]={"data":df.query(variable1 + "==" + str(idx))[variable2]}

  # Extract the raw data from dictionary object to pass scipy.stats functions
  rawData=list()
  for item in dataCollection:
    rawData.append(dataCollection[item]["data"])

  data1,data2=rawData[0],rawData[1]

  # Calculate Mann-Whitney U Test
  result = mannwhitneyu(data1, data2)

  # Calculate Degree of Freedom score
  dofF=len(data1)+len(data2)-2

  # Calculate group descriptive statistics
  groupStats=list()
  for item in dataCollection:
    group=dict()
    group[item]={"N":dataCollection[item]["data"].count(),
                   "Mean":dataCollection[item]["data"].mean(),
                   "StdDev":dataCollection[item]["data"].std(),
                   "StdErr": dataCollection[item]["data"].sem()
    }
    groupStats.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        "TestName":"mannwhitneyu",
        # Groups statistics
        "groupStats":groupStats,

        # Mann-Whitney U Test results
        "MannWhitneyUTest":{
            "u":result[0],
            "df":dofF,
            "sigTwoTailed":result[1]
        }
  }

  return dictReturn

def Output(testResult,destination):
 
  import uuid

  outputFileTemplateName=''
  outputType=''
 
  if testResult['TestName']=='indt':
    outputFileTemplateName='indttest.html'
    outputType='IndTTest'
  
  templateFile=open('outputs/' + outputFileTemplateName, "rt")
  outputFileName=outputType + '_' +  str(uuid.uuid4().hex) + '.html'
  
  outputFile=open(destination + outputFile,'wt')

  for line in templateFile:
      newLine=line.replace('{{F}}',str(testResult['LeveneTest']['F']))
      newLine=line.replace('{{lsig}}',str(testResult['LeveneTest']['sigTwoTailed']))
      newLine=line.replace('{{t}}',str(testResult['TTest']['t']))
      newLine=line.replace('{{df}}',str(testResult['TTest']['df']))
      newLine=line.replace('{{tsig2}}',str(testResult['TTest']['sigTwoTailed'])) 
      
      newLine=line.replace('{{wt}}',str(testResult['WelchTest']['t'])) 
      newLine=line.replace('{{wdf}}',str(testResult['WelchTest']['df']))
      newLine=line.replace('{{wsig2}}',str(testResult['WelchTest']['sigTwoTailed'])) 
      outputFile.write(newLine)

  templateFile.close()
  outputFile.close()
