import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from random import randint

import json
import requests
import time
import time
import datetime

SIMULATE_BREAK = None #used to determine if running on Pi or other system

try:
    import RPi.GPIO as GPIO
    SIMULATE_BREAK = False
except:
    import RPi_DUMMY.GPIO as GPIO
    SIMULATE_BREAK = True

import RPi_DUMMY.GPIO as GPIO
SIMULATE_BREAK = True

import subprocess

import sqlite3

MY_ZBIN_PATH = '../ZotBins_RaspPi'
MY_DB_PATH = '../ZBinData/zotbin.db'
PI_ZBIN_PATH = '../../ZotBins_RaspPi'
PI_DB_PATH = '/home/pi/ZBinData/zotbin.db'

sys.path.append(PI_ZBIN_PATH)
from ZBinClassDev import Dummy
sys.path.remove(PI_ZBIN_PATH)

#GLOBAL VARIABLES
GPIO_BREAK = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4,GPIO.IN)

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
        if SIMULATE_BREAK:
            self.db_path = PI_DB_PATH
        else:
            self.db_path = PI_DB_PATH

    def run(self):
        while True:
            if not SIMULATE_BREAK:
                sensor_state = GPIO.input(4)
                if (sensor_state==0):
                    while(sensor_state==0):
                        sensor_state = GPIO.input(4)
                    self.my_signal.emit()
                    self.add_data_to_local()
                    time.sleep(5)
            else:
                i = randint(1, 100)
                print("[BreakBeamThread] i = ", i)
                if (i % 5 == 0 and i > 0):
                    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                    print("[BreakBeamThread] break beam triggered")
                    print("[BreakBeamThread]: ", datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
                    self.my_signal.emit()
                    self.add_data_to_local(timestamp)
                    #self.update_tippers()
                time.sleep(2)

    def add_data_to_local(self, timestamp):
        """
        This function adds timestamp, weight, and distance data
        to the SQLite data base located in "/home/pi/ZBinData/zotbin.db"
        timestamp<str>: in the format '%Y-%m-%d %H:%M:%S'
        weight<float>: float that represents weight in grams
        distance<float>: float that represents distance in cm
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS "BREAKBEAM" (
        "TIMESTAMP" TEXT NOT NULL
        );
        ''')
        conn.execute("INSERT INTO BREAKBEAM (TIMESTAMP)\nVALUES ('{}')".format(timestamp))
        conn.commit()
        conn.close()

    def update_tippers(self):
        if SIMULATE_BREAK:
            print("[ZotBinThread] update_tippers called")
        else:
            print("[ZotBinThread] update_tippers called")

        d = list()
        tippersurl = "http://sensoria.ics.uci.edu:8059/observation/add"
        headers = {
        	"Content-Type": "application/json",
        	"Accept": "application/json"
        }
        cmd_str = "SELECT * from BREAKBEAM"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(cmd_str)
        for row in cursor:
            timestamp = row
            try:
                d.append({"timestamp": timestamp, "payload": {"time":timestamp},
                            "sensor_id": "ZotBinBreakBeam", "type": 11})
            except Exception as e:
                self.catch(e,"Tippers probably disconnected.")
                return

        r = requests.post(tippersurl, data=json.dumps(d), headers=headers)
        #after updating tippers delete from local database
        conn.execute("DELETE from BREAKBEAM")
        conn.commit()

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
        self.setCursor(Qt.BlankCursor)

        self.ZotBin = Dummy()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # =============Threads================
        self.BreakThread = BreakBeamThread()
        self.BreakThread.start()
        self.BreakThread.my_signal.connect(self.call_dialog)

         # ======= all list defined here ========
        self.images_list = []
        self.dialog_list = []
        self.img_anim = []
        self.dialog_anim = []


        # =======creating the Image Lables=======
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
            obj.setDuration(3500)
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

        self.timerLocal = QTimer(self)
        self.timerLocal.timeout.connect(self.call_dummy_func)
        self.timerLocal.start(3000) # 5 min
        #
        # self.timerTippers = QTimer(self)
        # self.timerTippers.timeout.connect(self.update_tippers_zbins)
        # self.timerTippers.start(10000) # 15 min

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

    def call_dialog(self):
        n = randint(0, self.dial_size - 1)
        self.hide_all()
        self.timer.stop()
        self.dialog_list[n].show()      # start the animation of the selected dialogue
        self.dialog_anim[n].start()
        self.timer.start(5000)

    def init_raspi():
        #raspi general setup
        if not SIMULATE_BREAK:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_BspeREAK, GPIO.IN)

    def call_dummy_func(self):
        self.ZotBin.do_something()

    # def update_local_zbins(self):
    #     try:
    #         #=========Measure the Weight===============================
    #         weight = self.ZotBin.measure_weight()
    #         #========Measure the Distance==============================
    #         distance = self.ZotBin.measure_dist()
    #         #=========Extract timestamp=================================
    #         timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #
    #         #=========Write to Local===================================
    #         self.ZotBin.add_data_to_local(timestamp,weight,distance)
    #         self.BreakThread.add_data_to_local(timestamp)
    #     except Exception as e:
    #         self.catch(e)
    #
    #
    # def update_tippers_zbins(self):
    #     #uploads the local database to tippers.
    #     #Basically everytime
    #     t = self.ZotBin
    #     t.update_tippers(t.weightSensorID,t.weightType,t.ultrasonicSensorID, t.ultrasonicType, t.headers, t.bininfo)
    #     self.BreakThread.update_tippers()



if __name__ == "__main__":
    # determines type of animations (compost, reycle, or landfill)
    if not SIMULATE_BREAK:
        with open('binType.txt','r') as f:
            r_id = f.read().strip()
    else:
        r_id = "compost"
    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword
