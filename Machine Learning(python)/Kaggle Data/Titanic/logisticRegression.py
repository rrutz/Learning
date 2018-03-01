import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.utils import shuffle


def readIn( path ):
    d = pd.read_csv( path )
    n = d.shape[0]

    # dummy for sex
    d["Sex" ] =  np.where( d["Sex"]=="male", 1, 0)

    #dummy for class
    Pclass1 = np.zeros(n)
    Pclass1[ d["Pclass" ] ==1 ] = 1
    Pclass2 = np.zeros(n)
    Pclass2[ d["Pclass" ] ==2 ] = 1
    Pclass3 = np.zeros(n)
    Pclass3[ d["Pclass" ] ==3 ] = 1
    d = pd.concat( [d, pd.DataFrame({ 'Pclass1' : Pclass1 }), pd.DataFrame({ 'Pclass2' : Pclass2 }), pd.DataFrame({ 'Pclass3' : Pclass3 }) ], axis = 1)

    d = d.drop([ "Name", "Ticket", "Cabin", "Embarked"], axis=1)
    
    return d, n


def fitModel():
    d_t, n_t = readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\train.csv" )
    d_v, n_v = readIn(  "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\test.csv" )
    d_v.Fare[ pd.isna(d_v.Fare) ] = 400
    d = pd.concat( [d_v,d_t], axis = 0, join = "outer" )
    d = d.sort_values( ['Age']).reset_index()


    # fill in missing data using linear model
    dd = d[ pd.isna(d.Age) == False ]
    reg_age = linear_model.LinearRegression()
    reg_age.fit( X = dd.loc[ :, ["Fare", "Pclass1", "Pclass2", "Pclass2", "Sex"]  ], y = dd["Age"] )
    p =  reg_age.predict( X = d[pd.isna(d.Age)].loc[ :, ["Fare", "Pclass1", "Pclass2", "Pclass2", "Sex"]  ] )
    d.loc[(d.Age.last_valid_index()+1):, "Age"] = p

    # age group dummies
    n  = d.shape[0]
    child = np.zeros(n)
    child[ d.Age <= 10] = 1
    childAge = child * d.Age
    middle = np.zeros(n)
    middle[ (d.Age > 10) & (d.Age <= 60 )] = 1
    middleAge = middle * d.Age
    old = np.zeros(n)
    old[ d.Age > 60] = 1
    oldAge = old * d.Age
    d = pd.concat( [d, pd.DataFrame( { 'child' : child, 'middle' : middle   , 'old' : old,   'childAge' :childAge, 'middleAge' :middleAge, 'oldAge' :oldAge    } ) ], axis = 1)


    # break up data
    d_t = d[ pd.isna( d.Survived ) == False ]
    d_t = shuffle(d_t)
    d_v = d[ pd.isna( d.Survived )  ].sort_values( ["PassengerId"] )

    
    # predict model to get prediciton of error
    n  = d_t.shape[0]
    d_tt = d_t[0:(n-100)]
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_tt.loc[ :, [ "Fare", "Pclass1", "Pclass2", "Pclass2", "Sex", "Age", "child", "middle", "old" , 'childAge', 'middleAge','oldAge'  ]  ], y = d_tt["Survived"] )
    d_vv = d_t[(n-100):]
    p = reg.predict( X = d_vv.loc[ :, [ "Fare", "Pclass1", "Pclass2", "Pclass2", "Sex", "Age", "child", "middle", "old" , 'childAge', 'middleAge','oldAge'     ]  ])
    print( sum( d_vv["Survived"] == p ) / d_vv.shape[0]) 

    # fit full model
    reg = linear_model.LogisticRegression()
    reg.fit( X = d_t.loc[ :, [  "Fare", "Pclass1", "Pclass2", "Pclass2", "Sex", "Age", "child", "middle", "old" , 'childAge', 'middleAge','oldAge'     ]  ], y = d_t["Survived"] )
    p = reg.predict( X = d_v.loc[ :, [  "Fare", "Pclass1", "Pclass2", "Pclass2", "Sex", "Age", "child", "middle", "old" , 'childAge', 'middleAge','oldAge'    ]  ])
    pd.DataFrame( {"PassengerId" : pd.to_numeric( d_v.PassengerId, downcast  = 'integer'), "Survived" : p}).to_csv( "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Kaggle Data\\Titanic\\prediction.csv", index  = False)




#################################################### # age groups #############################
surivedRateio = []
size = 10
for g in range(int(100/size)):
    t =  dd.s[  (dd.age > g*size) & (dd.age <= (g+1)*size) ].shape[0]
    if t != 0:
        surivedRateio.append(  dd.s[  (dd.age > g*size) & (dd.age <= (g+1)*size) ].sum() / t     )
    else:
        surivedRateio.append(0)
plt.bar( x = np.arange(size, 100+1, size) ,height = surivedRateio )
plt.ylim(ymax=1)
plt.show()


####################################################







