import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from scipy import stats
from sklearn.utils import shuffle

def generateDate( n ):
    d = pd.DataFrame( { 'x' : np.linspace(-25, 25, num = n) })
    d = pd.concat( [d, pd.DataFrame( { 'y' :4.0*np.sin(d.x) + np.random.normal( scale = 0.5, size = n )  + 5.0})], axis = 1)
    return  shuffle(d)



def __main__():
    n = 100
    max_df = 50
    numOfSim = 20
    errorsOnTrainAll = np.zeros(max_df -1 )
    errorsOnValidAll = np.zeros(max_df -1)
    reg = linear_model.LinearRegression( )
    for sim in range(numOfSim):
        d = generateDate( n )
        errorsOnTrain = []
        errorsOnVal = []
        for df in range(1, max_df):
            x = pd.DataFrame()

            for mean in np.linspace(-25,25, num = df ) :
                x = pd.concat( [ x,  pd.Series( stats.norm.pdf( d.x, loc = mean)) ], axis = 1 )
            reg.fit(X = x.iloc[ 0:70, :], y = d.y[0:70])
           
  
            errorOnVal = np.sum( ( np.abs(reg.predict( x.iloc[ 70:, :] ) - d.y[70:]) ) ) / 30.0
            errorOnTrain = np.sum( ( np.abs(reg.predict( x.iloc[ 0:70, :] ) - d.y[0:70]) )) / 70.0
            errorsOnTrain.append(errorOnTrain)
            errorsOnVal.append( min( 5, errorOnVal))
            
            errorsOnTrainAll[df-1] += errorOnTrain
            errorsOnValidAll[df-1] += errorOnVal

        plt.plot( np.arange(1, max_df),  errorsOnVal, c = 'r', alpha = 0.2)
        plt.plot( np.arange(1, max_df), errorsOnTrain, c = 'b',  alpha = 0.2)
        
    plt.plot( np.arange(1, max_df),errorsOnValidAll / (numOfSim), c = 'r', linewidth = 4.0)
    plt.plot( np.arange(1, max_df), errorsOnTrainAll/ (numOfSim), c = 'b', linewidth = 4.0)
    plt.show()

__main__()
  

   
