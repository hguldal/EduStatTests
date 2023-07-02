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

  def IndependedTTest(self,variable1,variable2):
    data,groups=[],[]
    
    if self.data is None:
      raise Exception("No data loaded")

    if len(self.data[variable1].value_counts().index)>2:
      raise Exception("The number of groups cannot be greater than 2")

    for idx in self.data[variable1].value_counts().index:
      data.append(self.data.query(variable1 + "==" + str(idx))[variable2])
      groups.append(int(idx))

    data1,data2=data[0],data[1]
    result1 = ttest_ind(data1, data2)
    result2=levene(data1, data2)
    result3= ttest_ind(data1, data2,equal_var = False)
    dofF=len(data1)+len(data2)-2

    dictReturn={
        "groupStats":{"N":self.data[variable1].value_counts().to_dict()},

        "equalVariancesAssumed":{
            "ttestForEqualityOfMeans": {
                "t":result1[0],
                "df":dofF,
                "sigTwoTailed":result1[1]
            }

        }
    }

    return dictReturn