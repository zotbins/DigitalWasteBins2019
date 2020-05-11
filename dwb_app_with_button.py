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
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from random import randint
from playsound import playsound
# from PyQt4.QtCore import pyqtSlot
# from PyQt4.QtGui import *

import time
import datetime
# from timer import Timer
#GLOBAL VARIABLES
r_id = None
gifFile = "200.gif"
input_list = [3]
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
    my_signal_4 = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        # if(self.my_signal_4.emit()):
        #     p

        # input_list = [0,0,1,3,4, 5, 6, 7, 8,9,20,20,3,3,0,1,0]
        self.my_signal.emit()
        # t = Timer()
        
        oldtime = time.time()
        while(input_list):
            print("input list: ",input_list)
            trash_counter = 0
            for i in input_list:
                if (i > 1 and i!=4):
                    
                    self.my_signal.emit()
                    # time.sleep(5)
                elif (i == 0):
                    trash_counter+=1
                    input_list.remove(i)
                    if(trash_counter == 5):
                        self.my_signal_2.emit()
                    else:
                        self.my_signal.emit()

                elif (i == 4):
                    input_list.remove(i)
                    self.my_signal_2.emit()
                    time.sleep(2)
                elif (i == 1):
                    input_list.remove(i)
                    self.my_signal_3.emit()

                

                    # self.my_signal.emit()
                # input_list.remove(i)
                print("inside for loop",input_list)
                print(i)
                # input_list.remove(i)
                time.sleep(3)

        #           
        print("input list is empty: ",input_list)


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
    


        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.call_dialog)
        self.BreakThread.my_signal_2.connect(self.call_dialog_2)
        self.BreakThread.my_signal_3.connect(self.call_dialog_3)
        self.BreakThread.my_signal_4.connect(self.call_dialog_4)


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
        self.dialogueTimer = QTimer(self)
        self.dialogueTimer.timeout.connect(self.change_image)
        print("iafter connecting to change image")
        self.dialogueTimer.start(5000)


        print("shown the image")    
        # ====Showing Widget======
        # self.showFullScreen() #uncomment this later. We do want fullscreen, but after we have a working image
        self.show()  # uncomment if you don't want fullscreen.

    def change_image(self):
        self.hide_all()
        print("in change_image function")
        self.imageIndex += 1
        if self.imageIndex >= self.images_size:
            self.imageIndex = 0
        x = self.imageIndex
        print("about to show the image")
        self.images_list[x].show()
        self.img_anim[x].start()
        print("after showing the image")
        

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
        x = randint(0,len(self.images_list)-1)
        self.hide_all()

        self.dialogueTimer.stop()
        self.dialog_list[n].show()      # start the animation of the selected dialogue
        self.dialog_anim[n].start()
        self.dialogueTimer.start(20000)
        # self.images_list[x].show()
        # self.img_anim[x].start()

        btn = QPushButton('Throw trash',self)
        wrong_trash_button = QPushButton('Wrong trash',self)
        trash_full_button = QPushButton('Trash is full',self)
        @pyqtSlot()
        def button1_click():
            input_list.append(0)
            print("input list after append: ",input_list)
            self.dialog_list[n].show()      # start the animation of the selected dialogue
            self.dialog_anim[n].start()
            # self.dialogueTimer.start(20000)

            ''' Tell when the button is clicked. '''
            print('clicked')
         
        
        @pyqtSlot()
        def wrong_trash_button_click():
            input_list.append(1)
            print("inwrong trash: ",input_list)

        @pyqtSlot()
        def trash_full_button_click():
            input_list.append(4)
            print("in full trash: ",input_list)
            
        btn.resize(100,100)
        btn.clicked.connect(button1_click)
        btn.show()

        wrong_trash_button.clicked.connect(wrong_trash_button_click)
        wrong_trash_button.resize(100,100)
        wrong_trash_button.move(0,200)
        wrong_trash_button.show()

        trash_full_button.clicked.connect(trash_full_button_click)
        trash_full_button.resize(100,100)
        trash_full_button.move(0,100)
        trash_full_button.show()


    def call_dialog_2(self):
        self.hide_all()
        self.dialogueTimer.stop()

        #Show text
        fulltrash_gif = QLabel(self)
        fulltrash_gif.setGeometry(550,10,900,900)
        fulltrash_pixmap = QMovie("images/" + r_id + "/fulltrash.gif", QByteArray(), self)
        fulltrash_pixmap.setCacheMode(QMovie.CacheAll)
        fulltrash_gif.setMovie(fulltrash_pixmap)
       
        self.bin_full.append(fulltrash_gif)
        fulltrash_gif.show()
        fulltrash_pixmap.start()
        playsound('alert.mp3')
        self.dialogueTimer.start(20000)

    def call_dialog_3(self):
        print("in call_dialog_3")
        self.hide_all()
        self.dialogueTimer.stop()
        l1 = QLabel(self)
        l1.setText("Wrong Bin! Should be in reycle.")
        l1.setFont(QtGui.QFont("Arial", 61, QtGui.QFont.Bold))
        l1.move(225,300)
        self.wrong_bin.append(l1)
        l1.show()
        l3 = QLabel(self)
        l3.setGeometry(350,350,650,650)
        # l1.move(800,190)
        # initialize the name of the gif file
        movie = QMovie("wrong.gif", QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        l3.setMovie(movie)
        self.wrong_bin.append(l3)
        l3.show()
        movie.start()
        playsound('Wrong.mp3')

    def call_dialog_4(self):
        self.hide_all()
        self.dialogueTimer.stop()
        btn = QPushButton('Throw trash',self)
        @pyqtSlot()
        def on_click():
            ''' Tell when the button is clicked. '''
            print('clicked')
            return 1;
         
        @pyqtSlot()
        def on_press():
            ''' Tell when the button is pressed. '''
            print('pressed')
         
        @pyqtSlot()
        def on_release():
            ''' Tell when the button is released. '''
            print('released')
        btn.resize(100,100)
        btn.clicked.connect(on_click)
        btn.pressed.connect(on_press)
        btn.released.connect(on_release)
        btn.show()


      




if __name__ == "__main__":
    # determines type of animations (compost, reycle, or landfill)
    with open('binType.txt','r') as f:
        r_id = f.read().strip()


    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword
