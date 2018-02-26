import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# data
def generateData( n = 50 ):
    d = pd.DataFrame( { 'x' : np.linspace(-20, 20, num = n) })
    d = pd.concat( [d, pd.DataFrame( { 'y' : 2.0*np.sin(d.x/ 3.0) + abs(np.cos(d.x))+ np.random.normal( scale = 0.5, size = n ) })], axis = 1)
    return d

# break into groups
def breakIntoGroups( data, groupNum = 3, n = 50 ):
    size = int(np.floor( n / groupNum ))
    for g in range(groupNum):
        arr = np.zeros( n )
        if g == (groupNum-1):
            arr[ (size*g): ] = 1
        else:
            arr[ (size*g):(size*(g+1))] = 1
        data = pd.concat( [data, pd.DataFrame( { 'group ' + str(g) : arr   }) ], axis = 1)
    return data

# pieceWise constant
def piecewiseConstant():
    groupNum = 3
    n = 50
    d = generateData( n )
    d = breakIntoGroups( d, groupNum , n )

    reg = linear_model.LinearRegression( fit_intercept = False)
    reg.fit( X = d.iloc[ : , 2:], y = d.y )

    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = breakIntoGroups(xx)
    yy = reg.predict(X = xx.iloc[ : , 1:])

    plt.scatter( x = d.x, y = d.y)
    for g in range(groupNum):
        xxx = xx.x[ xx[ "group " + str(g) ] == 1 ]
        yyy = yy[ xx[ "group " + str(g) ] == 1 ]
        plt.plot( xxx,  yyy )
    plt.show()

# pieceWise linear
def piecewiseLinear():
    groupNum = 3
    n = 50
    d = generateData( n )
    d = breakIntoGroups( d, groupNum , n )

    reg = linear_model.LinearRegression( fit_intercept = False)
    reg.fit( X = pd.concat( [ d.iloc[ : , 2:], d.iloc[ : , 2:].multiply( d.x, axis = "index")  ] ,axis = 1), y = d.y )

    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = breakIntoGroups(xx)
    yy = reg.predict(X = pd.concat( [xx.iloc[:, 1:], xx.iloc[:, 1:].multiply( xx.x, axis = "index") ], axis =1   ) )

    plt.scatter( x = d.x, y = d.y)
    for g in range(groupNum):
        xxx = xx.x[ xx[ "group " + str(g) ] == 1 ]
        yyy = yy[ xx[ "group " + str(g) ] == 1 ]
        plt.plot( xxx,  yyy )
    plt.show()

# pieceWise quad
def piecewiseQuad():
    groupNum = 3
    n = 50
    d = generateData( n )
    d = breakIntoGroups( d, groupNum , n )

    reg = linear_model.LinearRegression( fit_intercept = False)
    

piecewiseConstant()
piecewiseLinear()

