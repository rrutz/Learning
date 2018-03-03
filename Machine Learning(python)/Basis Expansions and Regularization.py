import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# data
def generateData( low, high, n ):
    d = pd.DataFrame( { 'x' : np.linspace(low, high, num = n) })
    d = pd.concat( [ pd.DataFrame( { 'y' : 2.0*np.sin(d.x/ 3.0) + abs(np.cos(d.x))+ np.random.normal( scale = 0.5, size = n ) }), d], axis = 1)
    return d

# break into groups into dummy variables
def breakIntoGroups( data, size, low, groupNum, n  ):
    for g in range(groupNum):
        arr = np.zeros( n )
        if g == (groupNum-1):
            arr[ data.x>=(low+size*g) ] = 1
        else:
            arr[  (data.x>=(low+size*g)) & ( data.x < low+size*(g+1))   ] = 1
        data = pd.concat( [data, pd.DataFrame( { 'group ' + str(g) : arr   }) ], axis = 1)
    return data

# pieceWise constant
def piecewiseConstant( d, n, groupNum, low, high ):
    size = int( (high-low) /groupNum)
    d = breakIntoGroups( d, size , low, groupNum, n   )

    reg = linear_model.LinearRegression( fit_intercept = False)
    reg.fit( X = d.iloc[ : , 2:], y = d.y )

    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = breakIntoGroups(xx, size, low, groupNum, 50 )
    yy = reg.predict(X = xx.iloc[ : , 1:])

    for g in range(groupNum):
        xxx = xx.x[ xx[ "group " + str(g) ] == 1 ]
        yyy = yy[ xx[ "group " + str(g) ] == 1 ]
        plt.plot( xxx,  yyy, c ="red" )
    plt.title("pieceWise constant")

# pieceWise linear. 
def piecewiseLinear( d, n, groupNum, low, high):
    size = int( (high-low) /groupNum)
    d = breakIntoGroups( d, size , low, groupNum, n   )

    # add x 
    for g in range(groupNum):
        d = pd.concat( [d,  ( d.loc[ :, ["group " + str(g)]].multiply( d.x, axis = "index") ).rename(columns= {"group " + str(g): "x*group " + str(g)})  ] , axis = 1 )

    # fit model
    reg = linear_model.LinearRegression( )
    reg.fit( X =  d.iloc[ : , 2:] , y = d.y )

    # make data up for plot
    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = breakIntoGroups(xx, size, low, groupNum, 50 )
    for g in range(groupNum):
        xx = pd.concat( [xx,  ( xx.loc[ :, ["group " + str(g)]].multiply( xx.x, axis = "index") ).rename(columns= {"group " + str(g): "x*group " + str(g)})  ] , axis = 1 )
    yy = reg.predict(X = xx.iloc[:, 1:] )

    # plot curves
    for g in range(groupNum):
        xxx = xx.x[ xx[ "group " + str(g) ] == 1 ]
        yyy = yy[ xx[ "group " + str(g) ] == 1 ]
        plt.plot( xxx,  yyy, c = "red" )
    plt.title("pieceWise linear")



# continuous pieceWise  linear
def contPiecewiseLinear( d, n, groupNum, low, high ):
    size = int( (high-low) /groupNum)
    
    # add x 
    for g in range(1, groupNum):
        d = pd.concat( [d, pd.DataFrame( {"group " + str(g):  np.maximum(d.x-g*size, 0) })  ] , axis = 1 )

    # fit model
    reg = linear_model.LinearRegression()
    reg.fit( X =  d.iloc[ : , 1:] , y = d.y )

    # make data up for plot
    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    for g in range(1, groupNum):
        xx = pd.concat( [xx, pd.DataFrame( {"group " + str(g):  np.maximum(xx.x-g*size, 0) })  ] , axis = 1 )
    yy = reg.predict(X = xx )

    # plot curves
    plt.plot( xx.x,  yy, c = "red" )
    plt.title("continuous pieceWise  linear")

# pieceWise quad
def piecewiseQuad( d, n, groupNum, low, high ):
    size = int( (high-low) /groupNum)
    d = breakIntoGroups( d, size , low, groupNum, n   )

    # add x and x^2 
    for g in range(groupNum):
        d = pd.concat( [d,  ( d.loc[ :, ["group " + str(g)]].multiply( d.x, axis = "index") ).rename(columns= {"group " + str(g): "x*group " + str(g)})  ] , axis = 1 )
        d = pd.concat( [d,  ( d.loc[ :, ["group " + str(g)]].multiply( d.x**2, axis = "index") ).rename(columns= {"group " + str(g): "x^2*group " + str(g)})  ] , axis = 1 )

    # fit model
    reg = linear_model.LinearRegression( fit_intercept  = False )
    reg.fit( X =  d.iloc[ : , 2:] , y = d.y )

    # make data up for plot
    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = breakIntoGroups(xx, size, low, groupNum, 50 )
    for g in range(groupNum):
        xx = pd.concat( [xx,  ( xx.loc[ :, ["group " + str(g)]].multiply( xx.x, axis = "index") ).rename(columns= {"group " + str(g): "x*group " + str(g)})  ] , axis = 1 )
        xx = pd.concat( [xx,  ( xx.loc[ :, ["group " + str(g)]].multiply( xx.x**2, axis = "index") ).rename(columns= {"group " + str(g): "x^2*group " + str(g)})  ] , axis = 1 )
    yy = reg.predict(X = xx.iloc[:, 1:] )

    # plot curves
    for g in range(groupNum):
        xxx = xx.x[ xx[ "group " + str(g) ] == 1 ]
        yyy = yy[ xx[ "group " + str(g) ] == 1 ]
        plt.plot( xxx,  yyy, c = "red" )
    plt.title("pieceWise quad")
  
   
# continuous pieceWise  Quad
def cubicSpline( d, n, groupNum, low, high ):

    size = int((high-low)/groupNum)
    
    d = pd.concat( [ d, pd.DataFrame( {"x^2" : d.x**2 }),  pd.DataFrame( {"x^3" : d.x**3 }) ], axis = 1)
    for g in range(1, groupNum):
        d = pd.concat( [d, pd.DataFrame( {"bx-a"+str(g) : np.maximum(0, d.x - (low + g*size) )**3 }) ] , axis = 1 )

    # fit model
    reg = linear_model.LinearRegression( )
    reg.fit( X =  d.iloc[ : , 1:] , y = d.y )

    # make data up for plot
    xx = pd.DataFrame( {"x" : np.linspace(  np.min(d.x), np.max(d.x)) } )
    xx = pd.concat( [ xx, pd.DataFrame( {"x^2" : xx.x**2 }), pd.DataFrame( {"x^3" : xx.x**3 }) ], axis = 1)
    for g in range(1, groupNum):
        xx = pd.concat( [xx, pd.DataFrame( {"bx-a"+str(g) : np.maximum(0, (xx.x - (low + g*size)))**3 }) ] , axis = 1 )
    yy = reg.predict(X = xx )

    # plot curves
    plt.plot( xx.x,  yy, c = "red" )
    plt.title("continuous pieceWise  Quad")
    

n = 75
numOfGroups = 8
low = -10
high = 30
d = generateData(low, high, n )

plt.subplot(231)
plt.scatter( x = d.x, y = d.y, c = "black")
piecewiseConstant( d, n, numOfGroups, low, high )

plt.subplot(232)
plt.scatter( x = d.x, y = d.y, c = "black")
piecewiseLinear( d, n, numOfGroups, low, high)

plt.subplot(233)
plt.scatter( x = d.x, y = d.y, c = "black")
contPiecewiseLinear( d, n, numOfGroups, low, high )

plt.subplot(234)
plt.scatter( x = d.x, y = d.y, c = "black")
piecewiseQuad( d, n, numOfGroups, low, high )

plt.subplot(235)
plt.scatter( x = d.x, y = d.y, c = "black")
cubicSpline( d, n, numOfGroups, low, high )

plt.show()


