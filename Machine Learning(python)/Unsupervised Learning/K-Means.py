import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generateData( numOfGroups ):
    d = pd.DataFrame()
    for i in range(numOfGroups):
        groupSize = np.random.randint(20, 45)
        d = pd.concat( [d, pd.DataFrame( { 'x': np.random.normal( np.random.normal(0, 5, 1), 2.0, groupSize), 'y': np.random.normal( np.random.normal(0, 5, 1), 2.0, groupSize), 'c' : str(i)} ) ] , axis = 0 )
    return d

def kMeans( d, numOfClasses, tol = 5 ):
    oldtotalDist = np.inf
    totalDist = np.inf
    classification = np.random.randint( 1, numOfClasses+1, size  = d.shape[0] )
     
    while( oldtotalDist == np.inf or (oldtotalDist-totalDist) > tol ):
        oldtotalDist = totalDist
        means = d.groupby( [classification] ).mean()
        dist = pd.DataFrame()
        for index, row in means.iterrows():
            dist = pd.concat( [dist, (d.x - row.x)**2 + (d.y - row.y )**2], axis = 1)
        dist.columns = np.arange(1,dist.shape[1]+1)
        totalDist = np.sum( dist.min( axis = 1 ) )
        classification = dist.idxmin(axis = 1 )

    return(  classification )
        
def __main__():
    numOfGroups = 5
    d = generateData( numOfGroups )
    classification = kMeans( d, 5)


    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    f.set_size_inches(15.5, 8.5)
    ax1.scatter( x = d.x, y =d.y, c = d.c)
    ax1.set_title("true grouping")
    ax2.scatter( x = d.x, y =d.y, c =classification)
    ax2.set_title("k-means grouping")
    plt.show()

__main__()


