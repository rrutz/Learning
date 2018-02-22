import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from scipy import stats

def generateDate( n = 10 ):
    d1 = pd.DataFrame( {'x' : np.random.normal( loc = 1.0, scale = 2.0, size = n), 'y' : np.random.normal( loc = 1.0, scale = 2.0, size = n), "class" : np.full( shape = (1,n), fill_value = 1)[0] } )
    d2 = pd.DataFrame( {'x' : np.random.normal( loc = 4.0, scale = 2.0, size = n), 'y' : np.random.normal( loc = 3.0, scale = 2.0, size = n), "class" : np.full( shape = (1,n), fill_value = 0)[0] } )
    return d1.append(d2)

d = generateDate()

reg = linear_model.LinearRegression()
reg.fit( X = d.loc[:,["x","class"]], y = d.y )
reg.predict( X = d.loc[:,["x","class"]])


x = np.array( [np.random.normal( loc = 1.0, scale = 2.0, size = 10), np.full( shape = (1,10), fill_value = 1)[0] ] )


stats.linregress( x= d.x, y = d["y"] )

ax = d1.plot.scatter( x = "x", y = "y", c = "red" )
d2.plot.scatter( x = "x", y = "y", c = "blue", ax = ax )
plt.plot([1,2,3,4])
plt.show()


x = np.random.random(10)
x1 = np.random.random(10)
y = np.random.random(10)
stats.linregress( np.array([x,x1]).reshape(2,10), y)