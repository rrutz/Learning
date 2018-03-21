import sys
sys.path.append('C:\\Users\\Ruedi\\OneDrive\\Learning\\Learning\\World Bank')
import GUI_Plots_Pannel
import GUI_ListPannel
import WorldBank

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

class WIN( QWidget ):

    def __init__(self, parent = None):
        super(WIN, self).__init__(parent)
        self.worldBank = WorldBank.WorldBank()
        self.showFullScreen()
        self.setWindowTitle( "World Bank GUI" )

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.plots_Pannel = GUI_Plots_Pannel.GUI_Plots_Pannel( self.worldBank )
        self.listPannel = GUI_ListPannel.GUI_List_Pannel( self.worldBank, self.plots_Pannel )

        layout.addLayout( self.listPannel, 1 )
        layout.addLayout( self.plots_Pannel, 5 )

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WIN()
    sys.exit(app.exec_())