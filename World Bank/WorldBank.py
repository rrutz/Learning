import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs

class WorldBank():

    def __init__(self):
        self.indicators = {"GDP" : "NY.GDP.MKTP.CD", "Population Growth": "SP.POP.GROW" }
        self.countries = self.getAllCountries()
        self.selectedCountry = 'USA'
        self.selectedIndicator = 'GDP'
        self.selectedData = None
        
    def getAllCountries( self ):
        par = {"per_page": '1000', 'format' : "json"}
        url = "http://api.worldbank.org/v2/countries"
        response = requests.get( url, params=par)
        if response == False:
            print('fail')
            return
        countries = [[],[]]
        for i in response.json()[1]:
            countries[0].append( i['id'] )
            countries[1].append( i['name'] )
        return countries

    def getData( self, country , indicator  ):
        #url = "http://api.worldbank.org/v2/countries/" + country + "/indicators/" + indicators[indicator] + "?per_page=1000&date=2000:2018&format=json"
   
        par = { "per_page": '1000', 'format' : "json", "date" : "2000:2018" }
        url = "http://api.worldbank.org/v2/countries/" + country + "/indicators/" + self.indicators[indicator]
        response = requests.get( url , params = par )
        if response == False:
            print('fail')
            return 

        df = pd.DataFrame()
        for i in response.json()[1]:
            df = df.append( pd.DataFrame( {'Country' : i['country']['value'], indicator :  i['value'] , 'Date' : i['date']  }, index=[0] ) )
        df = df.sort_values(by = 'Date')
        self.selectedData = df

    def plotData( self, country, indicator, ax ):
        df = self.selectedData
        ax.plot( df.Date, df[indicator], label = country )
        ax.set_title( country + ":" + indicator)
        ax.set_xlabel("Year")
        ax.set_ylabel(indicator)
        ax.legend(  )
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
        return ax

    def plotWorld( self, ax ):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cartopy.feature.OCEAN)

        shpfilename = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
        reader = shpreader.Reader(shpfilename)
        countries = reader.records()

        for country in countries:
            if country.attributes['ISO_A3'] == self.selectedCountry:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(), facecolor=(0, 0, 1))
            else:
                ax.add_geometries(country.geometry, ccrs.PlateCarree(),  facecolor=(0, 1, 0))
        return( ax )
