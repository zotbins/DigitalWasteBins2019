import sys
import os
import time
import datetime
import requests
import json
from random import randint

# PyQT related imports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPointF, pyqtProperty, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap

# Raspberry PI Related imports
import RPi.GPIO as GPIO
from picamera import PiCamera

#GLOBAL VARIABLES
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

r_id = None

JSONPATH = "/home/pi/ZBinData/binData.json"
DBPATH = "/home/pi/ZBinData/zotbin.db"
BREAKBEAM_COOL_DOWN_TIME = 2
CAMERA_WARMUP_DURATION = 2

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
        self.bininfo = self.parseJSON()
        self.url = self.bininfo["tippersurl"]
        self.bin_id = self.bininfo["binID"]
        self.obs_type = 5
        self.sensor_id = self.bin_id + 'B'
        QThread.__init__(self)

    def run(self):
        while True:
            sensor_state = GPIO.input(4)
            if (sensor_state==0):
                while(sensor_state==0):
                    sensor_state = GPIO.input(4)
                # === Send Signal to Trigger Dialog Animation ===
                self.my_signal.emit()
                # === Send Current Timestamp to Database ===
                self._recordBreakBeamData()
                # === Take Picture of the Trash ===
                # TODO: take a picture of the trash using our camera and send it to the database
                self._sendPicture()

    def _recordBreakBeamData(self):
        """
        Send the current timestamp to the breakbeam database.
        """
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print("[BreakBeamThread] break beam triggered at: ", timestamp)
        self.update_tippers(timestamp)

    def _sendPicture(self):
        """
        Take a picture of the trash using our camera and send it to the database.
        """
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        imgName = "/home/pi/DWB/DigitalWasteBins2019/images/dataPics/"+ timestamp + "_" + self.bin_id + ".jpg" #"<timestamp>_<BinID>.jpg"

        try:
            # === Take the Picture with the Raspberry Pi ===
            camera = PiCamera()
            camera.start_preview() #warm up the camera
            time.sleep(CAMERA_WARMUP_DURATION)
            camera.capture(imgName)
            camera.stop_preview()
            camera.close()

            # === Send the Picture to the ZotBins API ==

            imgFile = open(imgName, 'rb')
            API_response = requests.post(self.url + "/image", files={"file": imgFile})
            print("API Response:", API_response)

        except Exception as e:
            time.sleep(BREAKBEAM_COOL_DOWN_TIME)
            print("error_message", repr(e))
            return
        finally:
            imgFile.close()
            camera.close()

        # === Delete the Image that was Automatically saved ===
        # TODO: deal with data backup. Use the API_response variable
        try:
            os.remove(imgName)
        except Exception as e:
            print("Image Removing:",e)

    def update_tippers(self, timestamp):
        d = list()
        headers = {
        	"Content-Type": "application/json",
        	"Accept": "application/json"
        }
        d.append({"timestamp": timestamp, "payload": {"timestamp":timestamp},
                    "sensor_id": self.sensor_id, "type": self.obs_type})
        try:
            r = requests.post(self.url, data=json.dumps(d), headers=headers)
            print(r.content)
        except Exception as e:
            print(e)
            return

    def parseJSON(self):
        """
        This function parses the json file in the absolute path
        of '/home/pi/ZBinData/binData.json' and returns a dictionary
        """
        with open(JSONPATH) as bindata:
        	bininfo = eval( bindata.read() )["bin"][0]
        return bininfo

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
            obj.setDuration(2000) #change this to determine the speed of the animation
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

        # ============Animation Related QTimer============
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

    def call_dialog(self):
        n = randint(0, self.dial_size - 1)
        self.hide_all()
        self.timer.stop()
        self.dialog_list[n].show()      # start the animation of the selected dialogue
        self.dialog_anim[n].start()
        self.timer.start(20000)

if __name__ == "__main__":
    # determines type of animations (compost, reycle, or landfill)
    with open('binType.txt','r') as f:
        r_id = f.read().strip()

    # creating new class
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_()) # 'exec_' because 'exec' is already a keyword
