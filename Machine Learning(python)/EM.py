# EM for Mixture Model

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# true values
pie_t = 0.3 + np.random.uniform( -0.05, 0.05)
n = 100
n1 = round( n * pie_t )
n2 = n - n1
u1_t = 2
u2_t = 8
var1_t = 3
var2_t = 2

# make data up
data =  np.concatenate([ np.random.normal( u1_t, var1_t**0.5, n1),  np.random.normal( u2_t, var2_t**0.5, n2)] )
x_range = np.linspace( np.min(data), np.max(data))
plt.hist( data, density  = True )


# initialize parameter
p = 0.5
u1 = np.random.choice( data )
u2 = np.random.choice( data )
var1 = np.var(data)
var2 = var1
plt.plot( x_range, stats.norm.pdf( x_range, u1, var1**0.5 ), label = "Group 1: step "+str(0) , c = 'r' )
plt.plot( x_range, stats.norm.pdf( x_range, u2, var2**0.5 ), label = "Group 2: step "+str(0) , c = 'b' )

# EM alg
for i in range(1,30):
    e = (p*stats.norm.pdf( data, u2, var2**0.5 )) / (  (1-p)*stats.norm.pdf( data, u1, var1**0.5 ) + p*stats.norm.pdf( data, u2, var2**0.5 )    ) 
    u1 = np.sum( (1-e)*data ) / np.sum( 1- e )
    u2 = np.sum( e*data ) / np.sum( e )
    var1 = np.sum( (1-e)* (data-u1)**2) / np.sum( 1- e )
    var2 = np.sum( e* (data-u2)**2) / np.sum( e )
    p = np.sum(e) / n

plt.plot( x_range, stats.norm.pdf( x_range, u1, var1**0.5 ), label = "Group 1: step "+str(0) , c = 'r' )
plt.plot( x_range, stats.norm.pdf( x_range, u2, var2**0.5 ), label = "Group 2: step "+str(0) , c = 'b' )
plt.show()
