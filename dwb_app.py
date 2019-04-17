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
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt,QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from random import randint

import time
import datetime

class WasteImage(QLabel):
    def __init__(self,parent,image_file):
        super().__init__(parent)

        self.image_file = image_file

        pix = QPixmap(self.image_file)
        pix = pix.scaled(2000.000 / 10, 6000.000 / 10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

        self.setPixmap(pix)
    def new_pos(self,x,y):
        self.move(x,y)
    def new_size(self,h,w):
        pix = QPixmap(self.image_file)
        pix = pix.scaled(h,w,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.setPixmap(pix)
    def _set_pos(self, pos):
        self.move(pos.x(), pos.y())

    pos = pyqtProperty(QPointF, fset=_set_pos)

class BreakBeamThread(QThread):
    my_signal = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        i = 0 
        while True:
            if(i%11==0 and i>0):
                self.my_signal.emit()
            i = randint(1,100)
            print(i)
            time.sleep(1)

    def __del__(self):
        self.wait()
        
class App(QWidget):

    stop_signal = pyqtSignal()

    wait_signal = False   #boolean to be used to wait between animations
    animation_num = 1  #int to be used to start an animation

    def __init__(self):
        super().__init__()#inhreitance from QWidget
        self.title = 'PyQT Window'

        #determines where the window will be created
        self.left = 50
        self.top = 50

        #determines the size of the window
        self.width = 5038.176/10
        self.height = 9135.347/10
        self.imageIndex = 0

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

        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.printHello)
        # self.statusBar().showMessage('Message in statusbar.')

        #=======creating the Image Lables=======
        self.WasteImage1 = WasteImage(self, 'images/compost/c1.png')
        self.WasteImage2 = WasteImage(self, 'images/compost/c2.png')
        self.WasteImage3 = WasteImage(self, 'images/compost/c3.png')

        self.WasteDiag1 = WasteImage(self, 'images/compost/ant_dialog.png') #517.841,1032.501
        self.WasteDiag1.new_pos(517.841/10,1032.501/10)
        self.WasteDiag1.new_size(3998.610 / 10,5473.709 / 10)

        #define QPropertyAnimation Objects
        self.waste_anim1 = QPropertyAnimation(self.WasteImage1, b"pos")
        self.waste_anim2 = QPropertyAnimation(self.WasteImage2, b"pos")
        self.waste_anim3 = QPropertyAnimation(self.WasteImage3, b"pos")

        self.waste_anim4 = QPropertyAnimation(self.WasteDiag1, b"pos")

        #hide the animations initially
        self.hide_all()

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

        self.waste_anim4.setDuration(1000)  # 2 seconds
        self.waste_anim4.setStartValue(QPointF(517.07/10, 10 ))
        self.waste_anim4.setEndValue(QPointF(517.07/10, 2620.71/10)) #517.07/10,2620.71/10

        #======All Lists defined here======
        self.images_list = [self.WasteImage1, self.WasteImage2, self.WasteImage3]
        self.diaglog_list = [self.WasteDiag1]
        self.waste_anim_list = [self.waste_anim1, self.waste_anim2, self.waste_anim3]


        #=====Displaying the Background Frame Image===========
        background = QLabel(self)
        back_pixmap = QPixmap('images/compost/compost_background.png') #image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(5038/10, 9135/10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        background.setPixmap(back_pixmap)

        #=====Starting the animation========
        #self.WasteImage1.show()
        #self.waste_anim1.start()
        #print(self.waste_anim1.state())
        #print(self.waste_anim1.totalDuration())

        #============QTimer============
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(5000)
        
        #====Showing Widget======
        #self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        self.show() #uncomment if you don't want fullscreen.

    def change_image(self):
        self.hide_all()
        img_obj = [self.WasteImage1, self.WasteImage2, self.WasteImage3]
        ani_obj = [self.waste_anim1, self.waste_anim2, self.waste_anim3]
        self.imageIndex += 1
        if self.imageIndex > 2:
            self.imageIndex = 0
        x = self.imageIndex
        img_obj[x].show()
        ani_obj[x].start()
    
    def hide_all(self):
        self.WasteImage1.hide()
        self.WasteImage2.hide()
        self.WasteImage3.hide()
        self.WasteDiag1.hide()

    def printHello(self):
        self.hide_all()
        self.timer.stop()
        self.WasteDiag1.show()
        self.waste_anim4.start()
        self.timer.start(5000)


if __name__ == "__main__":
    #creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) #'exec_' because 'exec' is already a keyword
