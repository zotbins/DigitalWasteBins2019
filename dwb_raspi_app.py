import time
import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

last_state=0

while True:
    sensor_state = GPIO.input(4)
    if (sensor_state==0):
        while(sensor_state==0):
            sensor_state = GPIO.input(4)
        print(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
