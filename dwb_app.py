"""
Just Testing the branch
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
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from random import randint
import json
import random

import time
import datetime


r_id = 'recycling'

class WasteImage(QLabel):
    def __init__(self, parent, image_file):
        super().__init__(parent)
        self.image_file = image_file

        pix = QPixmap(self.image_file)
        pix = pix.scaled(2000.000 / 10, 6000.000 / 10, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)

        self.setPixmap(pix)

    def new_pos(self, x, y):
        self.move(x, y)

    def new_size(self, h, w):
        pix = QPixmap(self.image_file)
        pix = pix.scaled(h, w, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
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
            if (i % 11 == 0 and i > 0):
                self.my_signal.emit()
            i = randint(1, 100)
            print(i)
            time.sleep(2)

    def __del__(self):
        self.wait()


class App(QWidget):
    stop_signal = pyqtSignal()
    wait_signal = False  # boolean to be used to wait between animations
    animation_num = 1  # int to be used to start an animation

    def __init__(self):
        super().__init__()  # inhreitance from QWidget
        self.title = 'PyQT Window'

        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)  # -1 = main monitor, 1 = secondary monitor
        # determines where the window will be created
        self.left = 50
        self.top = 50

        # determines the size of the window
        self.width = screenSize.width()
        self.height = screenSize.height()
        self.imageIndex = 0

        # determines background color of the window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # initialized the window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.printHello)
        # self.statusBar().showMessage('Message in statusbar.')

        # ======= all list defined here ========
        self.images_list = []
        self.dialog_list = []
        self.img_anim = []
        self.dialog_anim = []

        # ======= reading json files ===========
        with open('images.json') as json_file:
            data = json.load(json_file)
        self.images_size = len(data[r_id]['images'])
        self.dial_size = len(data[r_id]['dialogue'])
        # =======creating the Image Lables=======
        for obj in data[r_id]['images']:
            self.images_list.append(WasteImage(self, obj))
        
        for obj in data[r_id]['dialogue']:
            self.dialog_list.append(WasteImage(self, obj))

        # ======== new dimensions of pictures =========#

        for obj in self.images_list:
            obj.new_size(self.width / 1.5, self.height / 1.5)
        
        for obj in self.dialog_list:
            obj.new_pos(self.width / 5.5, 10)
            obj.new_size(self.width/ 1.5, self.height / 1.5)
        # define QPropertyAnimation Objects

        # image animations
        for obj in self.images_list:
            self.img_anim.append(QPropertyAnimation(obj, b"pos"))
      
        # dialog animations
        for obj in self.dialog_list:
            self.dialog_anim.append(QPropertyAnimation(obj, b"pos"))

        # hide the animations initially
        self.hide_all()

        # defining the animations
        for obj in self.img_anim:
            obj.setDuration(2000)
            obj.setStartValue(QPointF(10,self.height / 4))
            obj.setEndValue(QPointF((self.width / 3.5), self.height / 4))

        for obj in self.dialog_anim:
            obj.setDuration(2000)
            obj.setStartValue(QPointF((self.width / 5.5), 10))
            obj.setEndValue(QPointF((self.width / 5.5), self.height / 3))


        # ======All Lists defined here======
        #self.images_list = [self.WasteImage1, self.WasteImage2, self.WasteImage3]
        #self.diaglog_list = [self.WasteDiag1]
        #self.waste_anim_list = [self.waste_anim1, self.waste_anim2, self.waste_anim3]

        # =====Displaying the Background Frame Image===========
        background = QLabel(self)
        back_pixmap = QPixmap(data[r_id]['background'][0])  # image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(self.width, self.height)
        background.setPixmap(back_pixmap)

        # =====Starting the animation========
        # self.WasteImage1.show()
        # self.waste_anim1.start()
        # print(self.waste_anim1.state())
        # print(self.waste_anim1.totalDuration())

        # ============QTimer============
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(5000)

        # ====Showing Widget======
        self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        #self.show()  # uncomment if you don't want fullscreen.

    def change_image(self):
        self.hide_all()
        self.imageIndex += 1
        if self.imageIndex >= self.images_size:
            self.imageIndex = 0
        x = self.imageIndex
        self.images_list[x].show()
        self.img_anim[x].start()

    def hide_all(self):
        for obj in self.images_list:
            obj.hide()
        for obj in self.dialog_list:
            obj.hide()



    def printHello(self):

        n = randint(0, self.dial_size - 1)

        self.hide_all()
        self.timer.stop()
        self.dialog_list[n].show()      #self.WasteDiag1.show()
        self.dialog_anim[n].start()    #self.waste_anim4.start()
        self.timer.start(5000)


if __name__ == "__main__":
    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword
