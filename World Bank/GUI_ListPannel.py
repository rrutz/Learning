from PyQt5.QtWidgets import QListWidget, QCheckBox, QGridLayout

class GUI_List_Pannel( QGridLayout ):

    def __init__(self, worldBank, plotPannel, parent = None):
        super(GUI_List_Pannel, self).__init__(parent)
        self.worldBank = worldBank
        self.plotPannel = plotPannel
        self.addCountryList()
        self.addIndicatorList()
        self.addCheckBox()

    def addCountryList( self ):
        self.countryList = QListWidget()
        self.countryList.addItems( self.worldBank.countries.keys() ) 
        self.countryList.currentItemChanged.connect(self.update)
        self.addWidget( self.countryList, 0, 0 )

    def addIndicatorList( self ):
        self.indicatorList = QListWidget()
        self.indicatorList.addItems( self.worldBank.indicators.keys() )
        self.indicatorList.currentItemChanged.connect( self.updateIndicator )
        self.addWidget( self.indicatorList, 0, 1 )

    def addCheckBox( self ):
        self.checkBox = QCheckBox( "Layer On?" )
        self.checkBox.stateChanged.connect( self.stateChanged )
        self.addWidget( self.checkBox, 1, 0, 2, 0 )

    def update( self ):
        selected_country = self.countryList.currentItem().text()
        self.worldBank.selectedCountry = self.worldBank.countries[selected_country]
        self.worldBank.getData( self.worldBank.selectedCountry, self.worldBank.selectedIndicator )
        self.plotPannel.updateCountryMap()
        self.plotPannel.updatePlots()
      
    def updateIndicator( self ):
        selected_indicator = self.indicatorList.currentItem().text()
        self.worldBank.selectedIndicator = selected_indicator
        self.worldBank.getData( self.worldBank.selectedCountry, self.worldBank.selectedIndicator )
        self.plotPannel.updatePlots()
        
    def stateChanged( self ):
        self.plotPannel.setLayerOn( self.checkBox.isChecked() )


