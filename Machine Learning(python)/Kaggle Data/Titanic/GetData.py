import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.utils import shuffle

def readIn( path ):
    d = pd.read_csv( path )
    n = d.shape[0]

    # dummy for sex
    d[ "Sex" ] =  np.where( d["Sex"]=="male", 1, 0)

    #dummy for class
    Pclass1 = np.zeros(n)
    Pclass1[ d["Pclass" ] == 1 ] = 1
    Pclass2 = np.zeros(n)
    Pclass2[ d["Pclass" ] == 2 ] = 1
    Pclass3 = np.zeros(n)
    Pclass3[ d["Pclass" ] == 3 ] = 1
    d = pd.concat( [d, pd.DataFrame({ 'Pclass1' : Pclass1 }), pd.DataFrame({ 'Pclass2' : Pclass2 }), pd.DataFrame({ 'Pclass3' : Pclass3 }) ], axis = 1)

    d = d.drop([ "Name", "Ticket", "Cabin", "Embarked"], axis=1)
    
    return d


# fill in missing data using linear model
def fillMissingAgeValues( d ):
    d = d.sort_values( ['Age']).reset_index()
    dd = d[ pd.isna(d.Age) == False ]
    reg_age = linear_model.LinearRegression()
    reg_age.fit( X = dd.loc[ :, ["Fare", "Pclass1", "Pclass2", "Pclass2", "Sex"]  ], y = dd["Age"] )
    p =  reg_age.predict( X = d[pd.isna(d.Age)].loc[ :, ["Fare", "Pclass1", "Pclass2", "Pclass2", "Sex"]  ] )
    d.loc[(d.Age.last_valid_index()+1):, "Age"] = p
    return shuffle(d)


# age group dummies
def addAgeDummies( d ):
    n  = d.shape[0]
    child = np.zeros(n)
    child[ d.Age <= 10] = 1
   
    middle = np.zeros(n)
    middle[ (d.Age > 10) & (d.Age <= 60 )] = 1
   
    old = np.zeros(n)
    old[ d.Age > 60] = 1
    
    d = pd.concat( [d, pd.DataFrame( { 'child' : child, 'middle' : middle   , 'old' : old    } ) ], axis = 1)
    return d


# age*group var 
def addAgeGroup( d ):
    childAge = d.child * d.Age
    middleAge = d.middle * d.Age
    oldAge = d.old * d.Age
    d = pd.concat( [d, pd.DataFrame( {    'childAge' :childAge, 'middleAge' :middleAge, 'oldAge' :oldAge    } ) ], axis = 1)
    return d




#################################################### # age groups #############################
def tryDifferentAgeGroups(dd):
    import matplotlib.pyplot as plt
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

