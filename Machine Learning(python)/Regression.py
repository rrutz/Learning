import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# ozone
d = pd.read_table( "C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\ozone.txt" )
y = np.log( d.ozone )
x = d.loc[: , ['radiation', 'temperature', 'wind']]
x.corr()

plt.subplot(2,2, 1)
plt.scatter( x = x.radiation, y = y)
plt.xlabel("radiation")
plt.subplot(2,2, 2)
plt.scatter( x = x.temperature, y = y)
plt.xlabel("temperature")
plt.subplot(2,2, 3)
plt.scatter( x = x.wind, y = y)
plt.xlabel("wind")

plt.show()


reg = linear_model.LinearRegression()
reg.fit( X = x.iloc[0:70, :], y = y[0:70])
p = np.exp(reg.predict( X = x.iloc[70: , :]))
plt.hist( np.exp(y[70:]) - p )
plt.show()
