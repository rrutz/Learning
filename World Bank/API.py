import requests
import pandas as pd
import json

import matplotlib.pyplot as plt
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDialog, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QListWidget, QCheckBox  
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class BB():

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





class GUI( QWidget ):

    def __init__(self, parent = None):
        super(GUI, self).__init__(parent)
        self.worldBank = BB()
        self.layerOn = False

        self.addCountryList()
        self.addIndicatorList()
        self.addCheckBox()
        self.addFigures()
        self.createWindow()
     
    def addCountryList( self ):
        self.countryList = QListWidget()
        self.countryList.addItems( self.worldBank.countries[1] )
        self.countryList.currentItemChanged.connect(self.update)

    def addIndicatorList( self ):
        self.indicatorList = QListWidget()
        self.indicatorList.addItems( self.worldBank.indicators.keys() )
        self.indicatorList.currentItemChanged.connect( self.updateIndicator )

    def addFigures( self ):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.figure_world = plt.figure()
        self.canvas_world = FigureCanvas(self.figure_world)

    def addCheckBox( self ):
        self.checkBox = QCheckBox( "Layer On?" )
        self.checkBox.stateChanged.connect( self.stateChanged )

    def createWindow( self ):
       self.setGeometry( 100,100,800,800 )
       self.setWindowTitle( "World Bank GUI" )

       layout = QHBoxLayout()
       self.setLayout(layout)
       layout.addWidget( self.countryList, 1 )
       layout.addWidget( self.indicatorList, 1 )
       layout.addWidget( self.checkBox, 1 )

       plot_layout = QVBoxLayout(  )
       self.update()
       plot_layout.addWidget(self.canvas )   
       plot_layout.addWidget( self.canvas_world )
       layout.addLayout( plot_layout, 5 )
       self.show()

    def update( self ):
        selected_index = self.countryList.currentRow()
        self.worldBank.selectedCountry = self.worldBank.countries[0][ selected_index ]
        self.worldBank.getData( self.worldBank.selectedCountry, self.worldBank.selectedIndicator )
        self.updatePlots()
      
    def updateIndicator( self ):
        selected_indicator = self.indicatorList.currentItem().text()
        self.worldBank.selectedIndicator = selected_indicator
        self.worldBank.getData( self.worldBank.selectedCountry, self.worldBank.selectedIndicator )
        self.updatePlots()
        
    def stateChanged( self ):
        if( self.checkBox.isChecked()):
            self.layerOn = True
        else:
            self.layerOn = False


    def updatePlots( self ):
        if self.layerOn == False:
            self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax = self.worldBank.plotData(self.worldBank.selectedCountry, self.worldBank.selectedIndicator, ax )
        self.canvas.draw()

        self.figure_world.clear()
        ax = self.figure_world.add_subplot(111)
        ax = self.worldBank.plotWorld( ax )
        self.canvas_world.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    d = GUI()
    sys.exit(app.exec_())