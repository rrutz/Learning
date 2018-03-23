from PyQt5.QtWidgets import QVBoxLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GUI_Plots_Pannel( QVBoxLayout ):

    def __init__( self, worldBank , parent = None):
        super( GUI_Plots_Pannel, self ).__init__( parent )
        self.worldBank = worldBank
        self.addFigures()
        self.layerOn = False

    def addFigures( self ):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.addWidget( self.canvas )   
        self.figure_world = plt.figure()
        self.canvas_world = FigureCanvas(self.figure_world)
        self.addWidget( self.canvas_world )

    def updatePlots( self ):
        if self.layerOn == False:
            self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax = self.worldBank.plotData(self.worldBank.selectedCountry, self.worldBank.selectedIndicator, ax )
        self.canvas.draw()

    def updateCountryMap( self ):
        self.figure_world.clear()
        ax = self.figure_world.add_subplot(111)
        ax = self.worldBank.plotWorld( ax )
        self.canvas_world.draw()

    def setLayerOn( self, bool ):
        self.layerOn = bool
