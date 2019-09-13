import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from random import randint

import json
import time
import datetime
#import RPi.GPIO as GPIO
import subprocess

#GLOBAL VARIABLES
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4,GPIO.IN)

r_id = None

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

        # while True:
        #     sensor_state = GPIO.input(4)
        #     if (sensor_state==0):
        #         while(sensor_state==0):
        #             sensor_state = GPIO.input(4)
        #         self.my_signal.emit()
        #         time.sleep(5)
        #         #print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

    def __del__(self):
        self.wait()

class BlackOutThread(QThread):
    my_signal = pyqtSignal()

    def __init__(self,starthour=0,endhour=8):
        """
        The starthour and the endhour variables represent the time range
        of when the blackout screen should be activated
        """
        QThread.__init__(self)
        self.starthour = starthour
        self.endhour = endhour
    def run(self):
        while True:
            #check if time is between 12AM and 8AM
            currentDatetime = datetime.datetime.now()
            currentHour  = int(currentDatetime.strftime('%H'))

            if (currentHour >= self.starthour and currentHour < self.endhour):
                self.my_signal.emit()
            time.sleep(300)

    def __del__(self):
        self.wait()

class App(QWidget):
    stop_signal = pyqtSignal()
    wait_signal = False  # boolean to be used to wait between animations
    animation_num = 1  # int to be used to start an animation

    def __init__(self):
        super().__init__()  # inhreitance from QWidget
        self.title = 'PyQT Window'

        # determines screen size
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)  # -1 = main monitor, 1 = secondary monitor

        # determines where the window will be created
        self.left = 50
        self.top = 50

        # determines the size of the window
        self.width = screenSize.width()
        self.height = screenSize.height()

        # this determines what image should be displayed for the main animation loop
        self.imageIndex = 0

        # determines background color of the window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # initialized the window
        self.initUI()

        #hides the cursor
        self.setCursor(Qt.BlankCursor)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.call_dialog)

        self.BlackThread = BlackOutThread()
        self.BlackThread.start()
        self.BlackThread.my_signal.connect(self.show_black)

         # ======= all list defined here ========
        self.images_list = []
        self.dialog_list = []
        self.img_anim = []
        self.dialog_anim = []

        # ========== black screen saver Image Label Object=======
        self.black_screen = QLabel(self)
        self.black_screen_pixmap = QPixmap("images/black_screen.png")  # image.jpg (5038,9135)
        self.black_screen_pixmap = self.black_screen_pixmap.scaled(self.width, self.height)
        #black_screen.setPixmap(black_screen_pixmap)

        # =======creating the Image Labels Objects=======
        foldername = "images/" + r_id + "/image_ani/"
        t = subprocess.run("ls {}*.png".format(foldername),shell=True, stdout=subprocess.PIPE)
        self.images_list = t.stdout.decode('utf-8').strip().split('\n')
        self.images_list = [WasteImage(self,obj) for obj in self.images_list] #now a list of image WasteImages
        self.images_size = len(self.images_list)

        foldername = "images/" + r_id + "/dialog_ani/"
        t = subprocess.run("ls {}*.png".format(foldername),shell=True, stdout=subprocess.PIPE)
        self.dialog_list = t.stdout.decode('utf-8').strip().split('\n')
        self.dialog_list = [WasteImage(self,obj) for obj in self.dialog_list]
        self.dial_size = len(self.dialog_list)

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
            obj.setDuration(5000)
            obj.setStartValue(QPointF((self.width / 5.5), 10))
            obj.setEndValue(QPointF((self.width / 5.5), self.height / 3))

        # =====Displaying the Background Frame Image===========
        background = QLabel(self)
        back_pixmap = QPixmap("images/" + r_id + "/background.png")  # image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(self.width, self.height)
        background.setPixmap(back_pixmap)

        # ============QTimer for animations============
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(5000)

        # ====Showing Widget======
        self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        #self.show()  # uncomment if you don't want fullscreen.

    def show_black(self):
        """
        This function shows a black screen
        """
        print("\n\n\nBLACKOUT!\n\n\n")

    def change_image(self):
        """
        This function changes the images of the waste and animates them
        in a loop.
        """
        self.hide_all()
        self.imageIndex += 1
        if self.imageIndex >= self.images_size:
            self.imageIndex = 0
        x = self.imageIndex
        self.images_list[x].show()
        self.img_anim[x].start()

    def hide_all(self):
        """
        This hides all the image objects.
        """
        for obj in self.images_list:
            obj.hide()
        for obj in self.dialog_list:
            obj.hide()

    def call_dialog(self):
        n = randint(0, self.dial_size - 1)
        self.hide_all()
        self.timer.stop()
        self.dialog_list[n].show()      # start the animation of the selected dialogue
        self.dialog_anim[n].start()
        self.timer.start(5000)


if __name__ == "__main__":
    # determines type of animations (compost, reycle, or landfill)
    with open('binType.txt','r') as f:
        r_id = f.read().strip()

    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword
