import time
import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

last_state=0

while True:
    sensor_state = GPIO.input(4)*GPIO.input(17)*GPIO.input(27)
    #sensor_state = sum([GPIO.input(4) for i in range(10)] )
    if (sensor_state==0):
        while(sensor_state==0):
            sensor_state = GPIO.input(4)*GPIO.input(17)*GPIO.input(27)
        self.my_signal.emit()
        time.sleep(2)

        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
    """
    if(sensor_state==1 and last_state==0 ):
        print("Unbroken")
    if(sensor_state==0 and last_state==1):
        print("broken")
    last_state = sensor_state
    """
    time.sleep(.02)
