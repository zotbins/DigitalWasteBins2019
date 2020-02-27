"""
Authors: Owen Yang, Tristan Samonte, Anthony Esmeralda, TingTing Tsai, Alpine Tang, Andy Tran, Martin Gomez
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
import os
from PyQt5.QtCore import Qt, QByteArray, QSettings, QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QSizePolicy, QVBoxLayout, QAction, QPushButton
from PyQt5.QtGui import QMovie
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore, QtWidgets, QtSvg, QtGui
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from random import randint

import time
import datetime
# from timer import Timer
#GLOBAL VARIABLES
r_id = None
gifFile = "200.gif"
class GifPlayer(QWidget):
    def __init__(self, title, gifFile, parent=None):
        super().__init__(parent)
        QWidget.__init__(self, parent)
        self.movie = QMovie(gifFile, QByteArray(), self)
        size = self.movie.scaledSize()
        self.setGeometry(200, 200, size.width(), size.height())
        self.setWindowTitle(title)
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movie_screen.setAlignment(Qt.AlignCenter)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
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
    my_signal_2 = pyqtSignal()
    my_signal_3 = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        input_list = [0,0,1,3,4, 5, 6, 7, 8,9,20,20,3,3,0,1,0]
        # t = Timer()
        oldtime = time.time()
        for i in input_list:
            if (i > 1):
                self.my_signal.emit()
            elif (i == 0):
                # t.start()
                # t.sleep(4)
                # sleep(40)
                if time.time() - oldtime > 30:
                    print("more than 30 sec")
                    self.my_signal_2.emit()
            elif (i == 1):
                # t.start()
                # t.sleep(4)
                # sleep(40)
                self.my_signal_3.emit()

        #             
 

            # i = randint(1, 100)
            print(i)
            time.sleep(2)
        # i = 0
        # while True:
        #     if (i % 11 == 0 and i > 0):
        #         self.my_signal.emit()
        #     i = randint(1, 100)
        #     print(i)
        #     time.sleep(2)
        # while True:
            # if (i > 0):
            #     self.my_signal.emit()
            # # i = randint(1, 100)
            # print(i)
            # time.sleep(2)

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
        self.imageIndex = 0

        # determines background color of the window
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # initialized the window
        self.initUI()

        #hides the cursor
        # self.setCursor(Qt.BlankCursor)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #make a label in main window
        #DISPLY SVG IMAGE THROUGH THIS
        # viewer = QtSvg.QSvgWidget(self)
        # viewer.setGeometry(1150,450,150,150)
        # viewer.load('trash.svg')
        # viewer.show()
        #DISPLY GIF IMAGE THROUGH THIS
        # label = QLabel(self)
        # #position it to top right
        # label.move(950,190)
        # #initialize the name of the gif file
        # movie = QMovie("200.gif", QByteArray(), self)
        # movie.setCacheMode(QMovie.CacheAll)
        # label.setMovie(movie)

        # movie.start()
 


        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.call_dialog)
        self.BreakThread.my_signal_2.connect(self.call_dialog_2)
        self.BreakThread.my_signal_3.connect(self.call_dialog_3)

         # ======= all list defined here ========
        self.images_list = []
        self.dialog_list = []
        self.img_anim = []
        self.dialog_anim = []
        self.wrong_bin =[]
        self.bin_full = []


        # =======creating the Image Lables=======
        foldername = "images/" + r_id + "/image_ani/"
        #t = subprocess.run("ls {}*.png".format(foldername),shell=True, stdout=subprocess.PIPE)
        t = os.listdir(foldername)
        self.images_list = list(filter(lambda x: ".png" in x, t ) )
        self.images_list = [WasteImage(self,foldername+obj) for obj in self.images_list] #now a list of image WasteImages
        self.images_size = len(self.images_list)

        foldername = "images/" + r_id + "/dialog_ani/"
        t = os.listdir(foldername)
        self.dialog_list = list(filter(lambda x: ".png" in x, t ) )
        self.dialog_list = [WasteImage(self,foldername+obj) for obj in self.dialog_list]
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
            obj.setDuration(2000) #in milliseconds
            obj.setStartValue(QPointF(10,self.height / 4))
            obj.setEndValue(QPointF((self.width / 3.5), self.height / 4))

        for obj in self.dialog_anim:
            obj.setDuration(800) #change this to determine the speed of the animation
            obj.setStartValue(QPointF((self.width / 5.5), self.height))
            obj.setEndValue(QPointF((self.width / 5.5), self.height / 3))

        # =====Displaying the Background Frame Image===========
        background = QLabel(self)
        back_pixmap = QPixmap("images/" + r_id + "/background.png")  # image.jpg (5038,9135)
        back_pixmap = back_pixmap.scaled(self.width, self.height)
        background.setPixmap(back_pixmap)

        # ============QTimer============
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change_image)
        self.timer.start(5000)

        # ====Showing Widget======
        # self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        self.show()  # uncomment if you don't want fullscreen.

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
        for obj in self.wrong_bin:
            obj.hide()
        for obj in self.bin_full:
            obj.hide()


    def call_dialog(self):
        n = randint(0, self.dial_size - 1)
        self.hide_all()
        self.timer.stop()
        self.dialog_list[n].show()      # start the animation of the selected dialogue
        self.dialog_anim[n].start()
        self.timer.start(20000)
    def call_dialog_2(self):
        self.hide_all()
        self.timer.stop()

        #Show text
        l1 = QLabel(self)
        l2 = QLabel(self)
        # l1.setGeometry(950,450,300,300)
        l1.setText("This trash can is full. :(")
        l2.setText("Please use another one!")
        l1.setFont(QtGui.QFont("Arial", 61, QtGui.QFont.Bold))
        l2.setFont(QtGui.QFont("Arial", 61, QtGui.QFont.Bold))
        l1.move(350,400)
        l2.move(350,500)
        self.bin_full.append(l1)
        self.bin_full.append(l2)
        l1.show()
        l2.show()

        #SVG IMAGE
        # viewer = QtSvg.QSvgWidget(self)
        # viewer.setGeometry(950,450,150,150)
        # viewer.load('trash.svg')
        # viewer.show()

        #GIF  
        l3 = QLabel(self)
        l3.setGeometry(1020,550,325,325)
        # l1.move(800,190)
        # initialize the name of the gif file
        movie = QMovie("fulltrash.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        l3.setMovie(movie)
        l3.show()
        movie.start()
    def call_dialog_3(self):
        self.hide_all()
        self.timer.stop()
        l1 = QLabel(self)
        l1.setText("Wrong Bin! Should be in reycle.")
        l1.setFont(QtGui.QFont("Arial", 61, QtGui.QFont.Bold))
        l1.move(305,400)
        self.wrong_bin.append(l1)
        l1.show()
        l3 = QLabel(self)
        l3.setGeometry(10,10,500,500)
        # l1.move(800,190)
        # initialize the name of the gif file
        movie = QMovie("wrong.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        l3.setMovie(movie)
        self.wrong_bin.append(l3)
        l3.show()
        movie.start()
      




if __name__ == "__main__":
    # determines type of animations (compost, reycle, or landfill)
    with open('binType.txt','r') as f:
        r_id = f.read().strip()


    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword

    # from PyQt5 import QtWidgets
    # from PyQt5 import QtSvg
    # import sys

    # app = QtWidgets.QApplication(sys.argv)

    # viewer = QtSvg.QSvgWidget()
    # viewer.setGeometry(50,50,209,258)
    # viewer.load('trash.svg')
    # viewer.show()

    # app.exec()
