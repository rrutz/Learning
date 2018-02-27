import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model

def generateDate( n ):
    d = pd.DataFrame( { 'x' : np.linspace(-20, 20, num = n) })
    d = pd.concat( [d, pd.DataFrame( { 'y' : 2.0*np.sin(d.x/ 3.0) + abs(np.cos(d.x))+ np.random.normal( scale = 0.5, size = n ) })], axis = 1)
    return d

def nearestNeighKernal( n = 50, k = 5 ):
    d = generateDate( n )

    def evenWeigthkeranl( x_in ):
        temp = pd.DataFrame( { "dist" : (d.x - x_in)**2, 'y' : d.y } )
        temp = temp.sort_values( ["dist"])
        return temp.iloc[ 0:k, : ].y.mean()

    def normalWeigthkeranl( x_in ):
        sigma = 3.0
        weights = stats.norm.pdf( d.x, loc  = x_in, scale = sigma )
        weights = weights / np.sum(weights)
        return np.sum( weights * d.y)

    def localLinearKernal( x_in ):
        sigma = 3.0
        weights = stats.norm.pdf( d.x, loc  = x_in, scale = sigma )
        weights = weights / np.sum(weights)

    


    xSpaced = np.linspace( np.min(d.x), np.max(d.x), num = 500).flatten()
    plt.scatter( x = d.x, y = d.y )
    plt.plot( xSpaced, 2.0*np.sin(xSpaced/ 3.0) + abs(np.cos(xSpaced)), label ="True" )
    plt.plot( xSpaced, list( map( evenWeigthkeranl, xSpaced )  ), label = "constant Weight" )
    plt.plot( xSpaced, list( map( normalWeigthkeranl, xSpaced )  ), label = "Normal Weight" )
    #plt.plot( xSpaced, list( map( localLinearKernal, xSpaced )  ), label = "Local Linear" )
    plt.legend()
    plt.show()

nearestNeighKernal(200, 30)