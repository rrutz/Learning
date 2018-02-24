import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def generateDate( n = 100 ):
    d1 = pd.DataFrame( { 'x' : np.random.normal( loc = 1, scale = 0.5, size = n ),  'y' : np.random.normal( loc = 1, scale = 0.5, size = n ), 'c' : np.full(shape = (1,n), fill_value = 1 )[0] } )
    d2 = pd.DataFrame( { 'x' : np.random.normal( loc = 5, scale = 0.5, size = n ),  'y' : np.random.normal( loc = 2, scale = 0.5, size = n ), 'c' : np.full(shape = (1,n), fill_value = 2 )[0] } )
    d3 = pd.DataFrame( { 'x' : np.random.normal( loc = 10, scale = 0.5, size = n ), 'y' : np.random.normal( loc = 3, scale = 0.5, size = n ), 'c' : np.full(shape = (1,n), fill_value = 3 )[0] } )
    d4 = pd.DataFrame( { 'x' : np.random.normal( loc = 1, scale = 0.5, size = n ),  'y' : np.random.normal( loc = 3, scale = 0.5, size = n ), 'c' : np.full(shape = (1,n), fill_value = 4 )[0] } )
    return( pd.concat( [d1, d2, d3, d4 ] ) )


def LDA():
    cov = d.loc[: , ["x", "y"] ].cov() 
    means = pd.DataFrame( { 'x' : d.groupby("c")['x'].mean(), 'y' : d.groupby("c")['y'].mean() })

    def classify( x, y ): 
        density = list( map( lambda mean_x, mean_y:  multivariate_normal.pdf( [x, y] , mean = [mean_x, mean_y] , cov = cov ), means.x, means.y ) )
        return np.argmax(density) + 1

    xx, yy = np.meshgrid( np.linspace( np.min(d.x), np.max(d.x) ),  np.linspace( np.min(d.y), np.max(d.y)) )
    xx = xx.flatten(); yy = yy.flatten()
    classifications = list( map( classify, xx, yy  ) )


    colors = ['red','green','blue', 'black']
    plt.scatter( x = xx, y = yy, c = classifications, cmap=matplotlib.colors.ListedColormap(colors), s  = 0.5)
    plt.scatter( x = d.x, y=d.y, c = d.c, cmap=matplotlib.colors.ListedColormap(colors) )
    plt.show()

def QDA():
    cov = d.groupby("c")
    covs = []
    for i in range(k):
        covs.append(cov.get_group(i+1).cov().iloc[ 1:3, 1:3 ])
    means = pd.DataFrame( { 'x' : d.groupby("c")['x'].mean(), 'y' : d.groupby("c")['y'].mean() })

    def classify( x, y ): 
        density = list( map( lambda mean_x, mean_y, cov_in:  multivariate_normal.pdf( [x, y] , mean = [mean_x, mean_y] , cov = cov_in ), means.x, means.y, covs  ) )
        return np.argmax(density) + 1
  
    xx, yy = np.meshgrid( np.linspace( np.min(d.x), np.max(d.x) ),  np.linspace( np.min(d.y), np.max(d.y)) )
    xx = xx.flatten(); yy = yy.flatten()
    classifications = list( map( classify, xx, yy  ) )

    colors = ['red','green','blue', 'black']
    plt.scatter( x = xx, y = yy, c = classifications, cmap=matplotlib.colors.ListedColormap(colors), s  = 0.5)
    plt.scatter( x = d.x, y=d.y, c = d.c, cmap=matplotlib.colors.ListedColormap(colors) )
    plt.show()


d = generateDate(35)
k = 4
LDA()
QDA()


