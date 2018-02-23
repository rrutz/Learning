import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model

def generateDate( n = 100 ):
    d1 = pd.DataFrame( {'x' : np.random.normal( loc = 1.0, scale = 2.0, size = n), 'y' : np.random.normal( loc = 1.0, scale = 2.0, size = n), "class" : np.full( shape = (1,n), fill_value = 1)[0] } )
    d2 = pd.DataFrame( {'x' : np.random.normal( loc = 4.0, scale = 2.0, size = n), 'y' : np.random.normal( loc = 3.0, scale = 2.0, size = n), "class" : np.full( shape = (1,n), fill_value = 0)[0] } )
    return d1.append(d2)


def linearClass():
    d_train = generateDate(200)

    # fit linear model
    reg = linear_model.LinearRegression()
    reg.fit( X = d_train.loc[:,["x","y"]], y = d_train["class"] )

    #plot data
    colors = np.where(d_train["class"]==1, 'r', 'b')
    d_train.plot.scatter( x = 'x', y = 'y', c = colors )
    xPlot = np.linspace(np.min(d.x), np.max(d.x))
    plt.plot( xPlot, (0.5 - reg.intercept_ - reg.coef_[0]*xPlot) / reg.coef_[1] ) 
    plt.show()

    # validation data
    d_val = generateDate(100)
    classification = np.where( reg.predict( X = d_val.loc[:,["x","y"]]) < 0.5, 0, 1)
    accuracy = np.sum( d_val["class"] == classification ) / classification.shape[0]
    print( accuracy )


def kMeans( k = 10 ):
    d_train = generateDate(100)

    def nearestNeigh( x, y, k = k ):
        distance = pd.DataFrame( { "dist" : (d_train.x - x)**2 + (d_train.y - y)**2 , "class" : d_train["class"] } )
        sortedDist = distance.sort_values( ["dist"] )
        percentage = np.sum( sortedDist.iloc[0:k ,0 ]  ) / k
        if percentage > 0.5:
            return 1
        return 0

    # fit data
    xx, yy = np.meshgrid(  np.linspace( np.min(d_train.x),  np.max(d_train.x) ),  np.linspace( np.min(d_train.y),  np.max(d_train.y)) )
    xx =  xx.flatten(); yy =  yy.flatten()
    classification = np.array( list( map( lambda x, y: nearestNeigh(x, y, k ) , xx , yy) ))

    # plot 
    colors1 = np.where( classification == 1, 'r', 'b')
    plt.scatter( x = xx, y = yy, c = colors1, s = 0.5 )
    colors2 = np.where(d_train["class"]==1, 'r', 'b')
    plt.scatter( x = d_train.x, y = d_train.y, c = colors2)
    plt.show()


linearClass()
kMeans( 2 )




