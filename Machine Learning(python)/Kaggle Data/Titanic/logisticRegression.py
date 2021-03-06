import sys
sys.path.append('C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic')
import GetData

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.utils import shuffle

def __main__():
    d_t = GetData.readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\train.csv" )
    d_v = GetData.readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\test.csv" )
    d_v.Fare[ pd.isna(d_v.Fare) ] = 400


    d = pd.concat( [d_v,d_t], axis = 0, join = "outer" )
    d = GetData.fillMissingAgeValues(d)
    d = GetData.addAgeDummies(d)


    # break up data
    d_t = d[ pd.isna( d.Survived ) == False ]
    d_t = shuffle(d_t)
    d_v = d[ pd.isna( d.Survived )  ].sort_values( ["PassengerId"] )

    
    predictors = [ "Fare", "Pclass1", "Pclass2", "Pclass2", "Sex", "Age", "child", "middle", "old" , 'childAge', 'middleAge','oldAge'  ]
    # predict model to get prediciton of error
    n  = d_t.shape[0]
    d_tt = d_t[0:(n-100)]
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_tt.loc[ :, predictors  ], y = d_tt["Survived"] )
    d_vv = d_t[(n-100):]
    p = reg.predict( X = d_vv.loc[ :,predictors  ])
    print( sum( d_vv["Survived"] == p ) / d_vv.shape[0]) 

    # fit full model
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_t.loc[ :, predictors  ], y = d_t["Survived"] )
    p = reg.predict( X = d_v.loc[ :, predictors  ])
    pd.DataFrame( {"PassengerId" : pd.to_numeric( d_v.PassengerId, downcast  = 'integer'), "Survived" : p}).to_csv( "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\prediction.csv", index  = False)


__main__()



