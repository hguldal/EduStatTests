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
                   "Mean":round(dataCollection[item]["data"].mean(),3),
                   "StdDev":round(dataCollection[item]["data"].std(),3),
                   "StdErr": round(dataCollection[item]["data"].sem(),3)
    }
    groupStats.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        "TestName":"indt",
        "Ind_Variable":variable1,
        "Dep_Variable":variable2,

        # Groups statistics
        "groupStats":groupStats,

        # T-Test results
        "TTest":{
            "t":round(result1[0],3),
            "df":dofF,
            "sigTwoTailed":round(result1[1],3)
        },

        # Levene test results
        "LeveneTest":
        {
         "F":round(result2[0],3),
         "sigTwoTailed":round(result2[1],3)

        },

        # Welch test results
        "WelchTest":{
            "t":round(result3[0],3),
            "sigTwoTailed":round(result3[1],3)
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

""" Html output for the Independent Samples T-Test Results  
Parameters (Input):
==================================================
testResult*        : Python dictionary returning from IndTTest function 

destination*: string
                
              Destination path for html file

*: Required Parameter

Return 
No return value:
"""

def HtmlOutputIndTTest(testResult,destination):
 
  import uuid

  htmlOutput='<html><head><metacontent="text/html;charset=UTF-8"http-equiv="content-type"><style>table,tr,th,td{border:1pxblacksolid;}</style></head><body><table><tr><tdcolspan="9"rowspan="1">IndependentSamplesTest</td></tr><tr><tdcolspan="2"rowspan="1"></td><tdcolspan="2"rowspan="1">Levene&rsquo;sTestforEqualityofVariances</td><tdcolspan="3"rowspan="1">T-TestforEqualityofVariances</td></tr><tr><tdcolspan="2"rowspan="1"></td><tdcolspan="1"rowspan="1">F</td><tdcolspan="1"rowspan="1">Sig.</td><tdcolspan="1"rowspan="1">t</td><tdcolspan="1"rowspan="1">df</td><tdcolspan="1"rowspan="1">Sig.(2-Tailed)</td></tr><tr><tdcolspan="1"rowspan="2">' + str(testResult['Ind_Variable']) + '</td><tdcolspan="1"rowspan="1">EqualVariancesAssumed</td><tdcolspan="1"rowspan="1">' + str(testResult['LeveneTest']['F']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['LeveneTest']['sigTwoTailed']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['TTest']['t']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['TTest']['df']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['TTest']['sigTwoTailed']) +'</td></tr><tr><tdcolspan="1"rowspan="1">EqualVariancesNotAssumed</td><tdcolspan="1"rowspan="1"></td><tdcolspan="1"rowspan="1"></td><tdcolspan="1"rowspan="1">'+ str(testResult['WelchTest']['t']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['TTest']['df']) +'</td><tdcolspan="1"rowspan="1">'+ str(testResult['WelchTest']['sigTwoTailed']) +'</td></tr></table></body></html>'
 
  outputFileName='IndTTest' + '_' +  str(uuid.uuid4().hex) + '.html'
  outputFile=open(destination + '/' + outputFileName,'wt')
 
  outputFile.write(htmlOutput)

  outputFile.close()
