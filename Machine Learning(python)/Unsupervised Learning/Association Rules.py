# The Apriori Algorithm
import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

def getDate():
    marketingData = pd.read_csv("C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\Machine Learning(python)\\Unsupervised Learning\\Marketing.csv"  )
    marketingData =marketingData.dropna( axis = 0 )
    n = marketingData.shape[0]
    
    col =  marketingData.loc[ :,  ["ANNUAL INCOME" ]]
    incomeDf = pd.DataFrame(  { \
                                    "Income: Less than $10,000"  : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "Income: $10,000 to $14,999" : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "Income: $15,000 to $19,999" : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "Income: $20,000 to $24,999" : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "Income: $25,000 to $29,999" : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "Income: $30,000 to $39,999" : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "Income: $40,000 to $49,999" : np.where( col == 7, 1, 0 ).flatten(),  \
                                    "Income: $50,000 to $74,999" : np.where( col == 8, 1, 0 ).flatten(),  \
                                    "Income: $75,000 or more"    : np.where( col == 9, 1, 0 ).flatten() \
                            }   )

    col =  marketingData.loc[ :,  ["SEX" ]]
    sexDf = pd.DataFrame( { \
                                "Male"   : np.where( col == 1, 1, 0 ).flatten(), \
                                "Female" : np.where( col == 2, 1, 0 ).flatten() \
                        } )


    col =  marketingData.loc[ :,  ["MARITAL STATUS" ]]
    MARITALDf = pd.DataFrame(  { \
                                    "MARITAL: Married"                      : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "MARITAL: Living together, not married" : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "MARITAL: Divorced or separated"        : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "MARITAL: Widowed"                      : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "MARITAL: Single, never married"        : np.where( col == 5, 1, 0 ).flatten() \
                            }   )


    col =  marketingData.loc[ :,  ["AGE" ]]
    ageDf = pd.DataFrame(  { \
                                    "AGE: 14 thru 17" : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "AGE: 18 thru 24" : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "AGE: 25 thru 34" : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "AGE: 35 thru 44" : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "AGE: 45 thru 54" : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "AGE: 55 thru 64" : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "AGE:65 and Over" : np.where( col == 7, 1, 0 ).flatten() \
                            }   )

    col =  marketingData.loc[ :,  ["EDUCATION" ]]
    educationDf = pd.DataFrame(  { \
                                    "EDUCATION: Grade 8 or less"        : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "EDUCATION: Grades 9 to 11"         : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "EDUCATION: Graduated high school"  : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "EDUCATION: 1 to 3 years of college": np.where( col == 4, 1, 0 ).flatten(),  \
                                    "EDUCATION: College graduate"       : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "EDUCATION: Grad Study"             : np.where( col == 6, 1, 0 ).flatten()  \
                            }   )

    col =  marketingData.loc[ :,  ["OCCUPATION" ]]
    occipationDf = pd.DataFrame(  { \
                                    "OCCUPATION: Professional/Managerial"        : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Sales Worker"                   : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Factory Worker/Laborer/Driver"  : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Clerical/Service Worker"        : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Homemaker"                      : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Student, HS or College"         : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Military"                       : np.where( col == 7, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Retired"                        : np.where( col == 8, 1, 0 ).flatten(),  \
                                    "OCCUPATION: Unemployed"                     : np.where( col == 9, 1, 0 ).flatten()  \
                            }   )

    col =  marketingData.loc[ :,  ["Lived Here how long" ]]
    LivedDf = pd.DataFrame(  { \
                                    "LIVED: Less than one year"     : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "LIVED: One to three years"     : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "LIVED: Four to six years"      : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "LIVED: Seven to ten years"     : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "LIVED: More than ten years"    : np.where( col == 5, 1, 0 ).flatten() \
                            }   )


    col =  marketingData.loc[ :,  ["DUAL INCOMES"] ]
    dualDf = pd.DataFrame(  { \
                                    "DUAL: Not Married"     : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "DUAL: Yes"             : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "DUAL: Nos"             : np.where( col == 3, 1, 0 ).flatten() \
                            }   )


    col =  marketingData.loc[ :,  ["PERSONS IN YOUR HOUSEHOLD" ]]
    houseHoldSizeDf = pd.DataFrame(  { \
                                    "HOUSEHOLD SIZE: One"           : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Two"           : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Three"         : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Four"          : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Five"          : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Six"           : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Seven"         : np.where( col == 7, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Eight"         : np.where( col == 8, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE: Nine or more"  : np.where( col == 9, 1, 0 ).flatten()  \
                            }   )

    col =  marketingData.loc[ :,  ["PERSONS IN HOUSEHOLD UNDER 18" ]]
    houseHoldSizeUnder18Df = pd.DataFrame(  { \
                                    "HOUSEHOLD SIZE 18: One"           : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Two"           : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Three"         : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Four"          : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Five"          : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Six"           : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Seven"         : np.where( col == 7, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Eight"         : np.where( col == 8, 1, 0 ).flatten(),  \
                                    "HOUSEHOLD SIZE 18: Nine or more"  : np.where( col == 9, 1, 0 ).flatten()  \
                            }   )

    col =  marketingData.loc[ :,  ["HOUSEHOLDER STATUS"] ]
    houseHolderDf = pd.DataFrame(  { \
                                    "HOUSEHOLDER: Own"                          : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "HOUSEHOLDER: Rent"                         : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "HOUSEHOLDER: Live with Parents/Family"     : np.where( col == 3, 1, 0 ).flatten() \
                            }   )


    col =  marketingData.loc[ :,  ["TYPE OF HOME" ]]
    HomeTypeDf = pd.DataFrame(  { \
                                    "HOME_TYPE: House"          : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "HOME_TYPE: Condominium"    : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "HOME_TYPE: Apartment"      : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "HOME_TYPE: Mobile Home"    : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "HOME_TYPE: Other"          : np.where( col == 5, 1, 0 ).flatten() \
                            }   )


    col =  marketingData.loc[ :,  ["ETHNIC CLASSIFICATION" ]]
    EthniceDf = pd.DataFrame(  { \
                                    "ETHNIC: American Indian"   : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "ETHNIC: Asian"             : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "ETHNIC: Black"             : np.where( col == 3, 1, 0 ).flatten(),  \
                                    "ETHNIC: East Indian"       : np.where( col == 4, 1, 0 ).flatten(),  \
                                    "ETHNIC: Hispanic"          : np.where( col == 5, 1, 0 ).flatten(),  \
                                    "ETHNIC: Pacific Islander"  : np.where( col == 6, 1, 0 ).flatten(),  \
                                    "ETHNIC: White"             : np.where( col == 7, 1, 0 ).flatten(),  \
                                    "ETHNIC: Other"             : np.where( col == 8, 1, 0 ).flatten() \
                            }   )

    col =  marketingData.loc[ :,  ["WHAT LANGUAGE IS SPOKEN MOST OFTEN IN YOUR HOME?"] ]
    languageDf = pd.DataFrame(  { \
                                    "LANGUAGE: English"     : np.where( col == 1, 1, 0 ).flatten(),  \
                                    "LANGUAGE: Spanish"     : np.where( col == 2, 1, 0 ).flatten(),  \
                                    "LANGUAGE: OtherNos"    : np.where( col == 3, 1, 0 ).flatten() \
                            }   )

    return( pd.concat( [incomeDf, sexDf, MARITALDf, ageDf, educationDf, occipationDf, LivedDf, dualDf, houseHoldSizeDf, houseHoldSizeUnder18Df, houseHolderDf, HomeTypeDf, EthniceDf, languageDf ], axis = 1  ) )


marketingData = getDate()
support = 0.10
confidence = 0.7
# get single-item sets
x = (marketingData.mean( axis = 0) >= support)
marketingData = marketingData.loc[ : , x ]

# gets the rest of the item sets
k = marketingData.shape[1]
K = { "size 1": list( range(0,k)) }
size = 2
largestGroupSize = k
Association = []
while largestGroupSize > 0:

    if size == 2:
        temp = []
        for i in range(k):
            temp.append(i)
        newGroupings =   list( combinations( temp , size) ) 

    else:
        newGroupings = []
        for group in largestSizeGroupings:
            for i in range(k):
                if i not in group:
                    t = list(group + (i, ))
                    t.sort()
                    t = tuple(t)
                    if t not in newGroupings:
                        if len( set( list( combinations( t , size-1) ) ) - set( largestSizeGroupings ) ) == 0:
                            newGroupings.append( t )
 
    largestSizeGroupings = []
    for group in newGroupings:
        if np.mean(  marketingData.iloc[ :,  list(group) ].sum( axis = 1)  == size ) >= support:
            largestSizeGroupings.append( group )


    largestGroupSize = len(largestSizeGroupings)
    
    if largestGroupSize > 0:
        K["size "+str(size)] = largestSizeGroupings
        if size > 2:
            for group in largestSizeGroupings:
                subset = list( combinations( group , size-1) )
                for subGroup in subset:
                    c =  (np.sum((marketingData.iloc[ :,  list(group) ].sum( axis = 1)  == size)) /  np.sum((marketingData.iloc[ :,  list(subGroup) ].sum( axis = 1)  == size -1)))
                    if c  > confidence :
                        Association.append( { "confidence" : c, 'antecedent' : tuple( subGroup ), 'consequent' : group, 'support' :  np.mean(  marketingData.iloc[ :,  list(group) ].sum( axis = 1)  == size )  } )

    size += 1

Association = sorted( Association, key = lambda k: k["confidence"], reverse=True)[0:10]

f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
ax1.barh(  np.arange(10),    list( map( lambda d: d["support"], Association )),  tick_label = list( map( lambda d: str( d["consequent"]), Association ))  )
ax1.set_title("Support")
ax2.barh(  np.arange(10),    list( map( lambda d: d["confidence"], Association )),  tick_label = list( map( lambda d: str( d["antecedent"]), Association ))  )
ax2.set_title("Confidence")
plt.show()

