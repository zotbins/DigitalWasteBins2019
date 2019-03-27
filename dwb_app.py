"""
Dependencies:
sudo apt-get install qt5-default
sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools

Documentation:
https://www.riverbankcomputing.com/static/Docs/PyQt5/

Tutorials:
https://pythonspot.com/pyqt5/
https://www.tutorialspoint.com/pyqt/

SVG Display:
https://stackoverflow.com/questions/35129102/simple-way-to-display-svg-image-in-a-pyqt-window
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5 import QtCore, QtSvg
from PyQt5.QtGui import QPixmap

import time

class App(QWidget):

    def __init__(self):
        super().__init__() #inhreitance from QWidget
        self.title = 'PyQT Window'

        #determines where the window will be created
        self.left = 50
        self.top = 50

        #determines the size of the window

        self.width = 5038.176/10
        self.height = 9135.347/10

        #initialized the window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.statusBar().showMessage('Message in statusbar.')

        background = QLabel(self)
        back_pixmap = QPixmap('images/compost/compost_background.png') #image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(5038/10, 9135/10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        background.setPixmap(back_pixmap)

        label = QLabel(self)
        label.move(1508.264/10, 2132.126/10)
        pixmap = QPixmap('images/compost/c1.png')
        pixmap = pixmap.scaled(2000.000/10, 6000.000/10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        label.setPixmap(pixmap)

        # Uncomment to resize window size to be the same size as the image
        # self.resize(pixmap.width(), pixmap.height())

        #self.showFullScreen()
        self.show() #uncomment if you don't want fullscreen

if __name__ == "__main__":
    #creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) #'exec_' because 'exec' is already a keyword
