## Welcome to EduStatTests
EduStatTests is free Python package for educational statistical analysis.


## Installing

You can install EduStatTests using the Python Package Index (PyPI)
    
**Requirements**
    
- NumPy
- Pandas
- SciPy

**PyPI Command**

    pip install EduStatTests
    
## How to Use EduStatTests

## Data

EduStatTests uses Pandas DataFrame as data format. You can use Excel, CSV format or Python dictionary object while creating the DataFrame.

**Loading data from CSV files**

CSV is a widely used data exchange format. In EduStatTests, the **LoadFromCSV** function is used to read and load CSV files into the DataFrame object.

The code below shows how to load data from CSV file into DataFrame object in EduStatTests.

    data=LoadFromCSV("drive/MyDrive/Datasets/test/test_data.csv")

**Loading data from Python Dictionary**

You can also load your data into the DataFrame in Python dictionary form by using the **LoadFromDict** function. The code below shows how to do this.

    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }
    
	data=LoadFromDict(dataDict)

## Tests

You can perform the following tests with EduStatTests.

 - Independent Samples T-Test


**Independent  Samples T-Test**

You can specify data in different formats as CSV or Python Dictionary. In the code example below, the data is used in Python dictionary format.

	from EduStatTests import *
    dataDict={
    "Gender": [1,1,0,0,1,1,0,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,1,1,0,1,1,1,0,1,1,0,1,0,0],
    "Attitude":[1,2,1,3,4,1,1,3,4,1,3,1,2,1,4,1,4,1,4,3,3,1,1,1,1,1,3,1,3,1,1,1,1,1,1,1,1,4,3,1,4,4,1,2,1,1,1,1,1,2,4,1,4,2,1,4,1,4,1,1,1]
    }
    
	dfObj=LoadFromDict(dataDict)
	results=IndTTest(dfObj,"Gender","Attitude")
	print(results)


 Analysis results are returned as a Python dictionary object. 

    {
    'groupStats': [
        {
        1: {
            'N': 34,
            'Mean': 2.0588235294117645,
            'StdDev': 1.324390688274108,
            'StdErr': 0.227131129214923
        }
        },
        {
        0: {
            'N': 27,
            'Mean': 1.7777777777777777,
            'StdDev': 1.12089707663561,
            'StdErr': 0.21571674297647797
        }
        }
    ],
    'TTest': {
        't': 0.8800707305476686,
        'df': 59,
        'sigTwoTailed': 0.382391731055874
    },
    'LeveneTest': {
        'F': 2.518867254548078,
        'sigTwoTailed': 0.1178367500254776
    },
    'WelchTest': {
        't': 0.8972082259877001,
        'sigTwoTailed': 0.37327099221741844
    }
    }

----------

 
