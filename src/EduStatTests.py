import pandas as pd
import numpy as np
from scipy.stats import *

class EduStatTests:

  def __init__(self):
    self.data=None

  def LoadFromCSV(self,CSVPath):
    self.data = pd.read_csv(CSVPath)

  def LoadFromExcel(self,ExcelPath):
    self.data = pd.read_csv(ExcelPath)

""" Independent T-Test
Parameters:
================================================== 
  self:       Instance of the EduStatTests class
              

  variable1*: string                
              Independent variable (X) 
              Name of DataFrame column object

  variable2*: string
              Dependent variable (Y)
              Name of DataFrame column object
  
  *: Required Parameter

Return:
===================================================
Type: dictionary
Description: T-Test Stats
"""
  def IndTTest(self,variable1,variable2):
    dataCollection=dict()

    if self.data is None:
      raise Exception("No data loaded")

    if len(self.data[variable1].value_counts().index)>2:
      raise Exception("The number of groups cannot be greater than 2")

    for idx in self.data[variable1].value_counts().index:
      dataCollection[idx]={"data":self.data.query(variable1 + "==" + str(idx))[variable2]}

    rawData=list()
    for item in dataCollection:
      rawData.append(dataCollection[item]["data"])

    data1,data2=rawData[0],rawData[1]
    result1 = ttest_ind(data1, data2)
    result2=levene(data1, data2,center='mean')
    result3= ttest_ind(data1, data2,equal_var = False)
    dofF=len(data1)+len(data2)-2
    groupStats=list()
    for item in dataCollection:
      group=dict()
      group[item]={"N":dataCollection[item]["data"].count(),
                   "Mean":dataCollection[item]["data"].mean(),
                   "StdDev":dataCollection[item]["data"].std()
      }
      groupStats.append(group)
    
    dictReturn={
        "groupStats":groupStats,

        "TTest":{
            "t":result1[0],
            "df":dofF,
            "sigTwoTailed":result1[1]
        },
        "LeveneTest":
        {
         "F":result2[0],
         "sigTwoTailed":result2[1]
            
        },
        "WelchTest":{
            "t":result3[0],
            "sigTwoTailed":result3[1]
        }
    }

    return dictReturn