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

Animations:
http://zetcode.com/pyqt/qpropertyanimation/
https://www.programcreek.com/python/example/99577/PyQt5.QtCore.QPropertyAnimation
https://doc.qt.io/qtforpython/PySide2/QtCore/QAbstractAnimation.html
https://doc.qt.io/qtforpython/PySide2/QtCore/QAnimationGroup.html

PyQT Threading and Loops:
https://stackoverflow.com/questions/49886313/how-to-run-a-while-loop-with-pyqt5
https://kushaldas.in/posts/pyqt5-thread-example.html
https://doc.qt.io/qtforpython/PySide2/QtCore/QPropertyAnimation.html

Hiding Labels:
https://stackoverflow.com/questions/28599883/changing-a-labels-visibility-using-pyqt

PyQt Signals and Slots:
https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt,QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap

import time
import datetime

class WasteImage(QLabel):
    def __init__(self,parent,image_file):
        super().__init__(parent)
        pix = QPixmap(image_file)
        pix = pix.scaled(2000.000 / 10, 6000.000 / 10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.h = 2000.000/10
        self.w = 6000.000/10
        self.setPixmap(pix)

    def _set_pos(self, pos):
        self.move(pos.x(), pos.y())

    pos = pyqtProperty(QPointF, fset=_set_pos)

class Worker(QObject):
    finished = pyqtSignal() #give a finished signal
    def __init__(self,parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True
    def do_work(self):
        i = 1
        while self.continue_run:#give the loop a stoppable condition
            print(i)
            QThread.sleep(1)
            i += 1
        self.finished.emit() #emit the finished signal when the loop is done
    def stop(self):
        self.continue_run = False

class App(QWidget):

    stop_signal = pyqtSignal()

    wait_signal = False   #boolean to be used to wait between animations
    animation_number = 1  #int to be used to start an animation

    def __init__(self):
        super().__init__()#inhreitance from QWidget
        self.title = 'PyQT Window'

        #determines where the window will be created
        self.left = 50
        self.top = 50

        #determines the size of the window
        self.width = 5038.176/10
        self.height = 9135.347/10

        #determines background color of the window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        #initialized the window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.statusBar().showMessage('Message in statusbar.')

        #=======creating the Image Lables=======
        self.WasteImage1 = WasteImage(self, 'images/compost/c1.png')
        self.WasteImage2 = WasteImage(self, 'images/compost/c2.png')
        self.WasteImage3 = WasteImage(self, 'images/compost/c3.png')

        #define QPropertyAnimation Objects
        self.waste_anim1 = QPropertyAnimation(self.WasteImage1, b"pos")
        self.waste_anim2 = QPropertyAnimation(self.WasteImage2, b"pos")
        self.waste_anim3 = QPropertyAnimation(self.WasteImage3, b"pos")

        #hide the animations initially
        self.WasteImage1.hide()
        self.WasteImage2.hide()
        self.WasteImage3.hide()

        #defining the animations
        self.waste_anim1.setDuration(2000)  # 2 seconds
        self.waste_anim1.setStartValue(QPointF(10, 2132.126 / 10))
        self.waste_anim1.setEndValue(QPointF(1508.264 / 10, 2132.126 / 10))

        self.waste_anim2.setDuration(2000)  # 2 seconds
        self.waste_anim2.setStartValue(QPointF(10, 2132.126 / 10))
        self.waste_anim2.setEndValue(QPointF(1508.264 / 10, 2132.126 / 10))

        self.waste_anim3.setDuration(2000)  # 2 seconds
        self.waste_anim3.setStartValue(QPointF(10, 2132.126 / 10))
        self.waste_anim3.setEndValue(QPointF(1508.264 / 10, 2132.126 / 10))


        #=====Displaying the Background Frame Image===========
        background = QLabel(self)
        back_pixmap = QPixmap('images/compost/compost_background.png') #image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(5038/10, 9135/10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        background.setPixmap(back_pixmap)

        #=====Starting the animation========
        self.WasteImage1.show()
        self.waste_anim1.start()
        print(self.waste_anim1.state())
        print(self.waste_anim1.totalDuration())
        #self.waste_anim1.setPaused(True)

        #=====Thread========
        # self.thread = QThread()
        # self.worker = Worker(self)
        # self.stop_signal.connect(self.worker.stop) # connect stop signal to worker stop method
        # self.worker.moveToThread(self.thread)      # inherit from self.thread
        # self.thread.started.connect(self.worker.do_work) #when the thread starts, start worker
        # self.thread.finished.connect(self.worker.stop) #when the thread finishes, stop worker
        #
        # #start the thread
        # self.thread.start()
        # button = QPushButton('Stop', self)
        # button.move(100, 70)
        # button.clicked.connect(self.stop_thread)

        #====Showing Widget======
        #self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        self.show() #uncomment if you don't want fullscreen.

    def stop_thread(self):
        self.stop_signal.emit()

if __name__ == "__main__":
    #creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) #'exec_' because 'exec' is already a keyword
