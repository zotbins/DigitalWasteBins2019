import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from random import randint

import time
import time
import datetime
import RPi.GPIO as GPIO

#GLOBAL VARIABLES
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)


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
        while True:
            sensor_state = GPIO.input(4)
            if (sensor_state==0):
                while(sensor_state==0):
                    sensor_state = GPIO.input(4)
                self.my_signal.emit()
                time.sleep(2)
                print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


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

        # =======creating the Image Lables=======
        self.WasteImage1 = WasteImage(self, 'images/compost/c1.png')
        self.WasteImage2 = WasteImage(self, 'images/compost/c2.png')
        self.WasteImage3 = WasteImage(self, 'images/compost/c3.png')
        self.WasteDiag1 = WasteImage(self, 'images/compost/ant_dialog.png')

        # ======== new dimensions of pictures =========#
        self.WasteImage1.new_size(self.width / 1.5, self.height / 1.5)
        self.WasteImage2.new_size(self.width / 1.5, self.height / 1.5)
        self.WasteImage3.new_size(self.width / 1.5, self.height / 1.5)
        self.WasteDiag1.new_pos((self.width / 5.5), 10)
        self.WasteDiag1.new_size(self.width / 1.5, self.height / 1.5)

        # define QPropertyAnimation Objects

        # image animations
        self.waste_anim1 = QPropertyAnimation(self.WasteImage1, b"pos")
        self.waste_anim2 = QPropertyAnimation(self.WasteImage2, b"pos")
        self.waste_anim3 = QPropertyAnimation(self.WasteImage3, b"pos")

        # dialog animations
        self.waste_anim4 = QPropertyAnimation(self.WasteDiag1, b"pos")

        # hide the animations initially
        self.hide_all()

        # defining the animations
        self.waste_anim1.setDuration(2000)  # 2 seconds
        self.waste_anim1.setStartValue(QPointF(10, self.height / 4))
        self.waste_anim1.setEndValue(QPointF((self.width / 3.5), self.height / 4))

        self.waste_anim2.setDuration(2000)  # 2 seconds
        self.waste_anim2.setStartValue(QPointF(10, self.height / 4))
        self.waste_anim2.setEndValue(QPointF((self.width / 3.5), self.height / 4))

        self.waste_anim3.setDuration(2000)  # 2 seconds
        self.waste_anim3.setStartValue(QPointF(10, self.height / 4))
        self.waste_anim3.setEndValue(QPointF((self.width / 3.5), self.height / 4))

        self.waste_anim4.setDuration(1000)  # 2 seconds
        self.waste_anim4.setStartValue(QPointF((self.width / 5.5), 10))
        self.waste_anim4.setEndValue(QPointF((self.width / 5.5), self.height / 3))

        # ======All Lists defined here======
        self.images_list = [self.WasteImage1, self.WasteImage2, self.WasteImage3]
        self.diaglog_list = [self.WasteDiag1]
        self.waste_anim_list = [self.waste_anim1, self.waste_anim2, self.waste_anim3]

        # =====Displaying the Background Frame Image===========
        # background = QLabel(self)
        # back_pixmap = QPixmap('images/compost/compost_background.png')  # image.jpg (5038,9135)
        # back_pixmap = back_pixmap.scaled(self.width, self.height,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation) #,QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation
        # background.setPixmap(back_pixmap)

        self.background = WasteImage(self, 'images/compost/compost_background.png')
        self.background.new_size(self.width, self.height)
        self.background.new_pos(0, 0)


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
    # creating new class
    app = QApplication(sys.argv)
    ex = App()
sys.exit(app.exec_())  # 'exec_' because 'exec' is already a keyword