import psycopg2 as pg
import matplotlib.pyplot as plt

def __main__():
    print( "Enter password: ", end = "")
    password = input()
    try:
        conn = pg.connect( "dbname='Test' user='postgres' host='localhost' password=%s" %( password ) )
    except:
        print( "Failed to connect to database" )
        return 0
    
    cur = conn.cursor()
    cur.execute("select price from  land_registry_price_paid_uk where price < 1000000;")

    prices = []
    for row in cur.fetchall():
        prices.append( float(row[0]) )

    plt.hist(prices)
    plt.title( "Histogram of House Prices" )
    plt.xlabel( "Price" )
    plt.ylabel( "Count" )
    plt.show()
    return 1

__main__()