import sys
sys.path.append('C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic')
import GetData
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.utils import shuffle

def addSplines( d, predictors, numOfSplines ):
    import rpy2.robjects as ro
    import rpy2.robjects.numpy2ri
    rpy2.robjects.numpy2ri.activate()
    ro.r.require("splines")

    bs = ro.r['bs']
    predictors = [ "Fare","Age"  ]
    n = d.shape[0]
    for p in predictors:
        x = np.array ( d.loc[ : , p ]  )
        x = bs( x, numOfSplines)
        x = np.array( list(x)).reshape( numOfSplines ,n)
        for i in range(numOfSplines):
            d = pd.concat( [ d,  pd.DataFrame( { "bs "+str(p)+str(i) : x[i , :]  } ) ]   , axis = 1  )

    return d

def __main__():
    # get data
    d_t = GetData.readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\train.csv" )
    d_v = GetData.readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\test.csv" )
    d_v.Fare[ pd.isna(d_v.Fare) ] = 400


    d = pd.concat( [d_v,d_t], axis = 0, join = "outer" )
    d = GetData.fillMissingAgeValues(d)
    d = GetData.addAgeDummies(d)
    d = GetData.addAgeGroup( d )

    numOfSplines = 3
    d = addSplines( d, ["Fare", "Age"], numOfSplines )

    # break up data
    d_t = d[ pd.isna( d.Survived ) == False ]
    d_t = shuffle(d_t)
    d_v = d[ pd.isna( d.Survived )  ].sort_values( ["PassengerId"] )

  
    # predict model to get prediciton of error
    predictors = [ "Fare", "Pclass1", "Pclass2", "Pclass3", "Sex", "Age", "child", "middle", "old" ]
    for p in  ["Fare", "Age"]:
        for i in range(numOfSplines):
            predictors.append( "bs "+str(p)+str(i) )

    n  = d_t.shape[0]
    d_tt = d_t[0:(n-400)]
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_tt.loc[ :, predictors  ], y = d_tt["Survived"] )
    d_vv = d_t[(n-400):]
    p = reg.predict( X = d_vv.loc[ :,predictors  ])
    print( sum( d_vv["Survived"] == p ) / d_vv.shape[0]) 

    # fit full model
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_t.loc[ :, predictors  ], y = d_t["Survived"] )
    p = reg.predict( X = d_v.loc[ :, predictors  ])
    pd.DataFrame( {"PassengerId" : pd.to_numeric( d_v.PassengerId, downcast  = 'integer'), "Survived" : p}).to_csv( "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\prediction.csv", index  = False)


__main__()



