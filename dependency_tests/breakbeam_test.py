import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)    
GPIO.setup(4,GPIO.IN)

last_state=0

while True:
    sensor_state = GPIO.input(4)
    #sensor_state = sum([GPIO.input(4) for i in range(10)] )
    if (sensor_state==0):
        print(time.time())
    """
    if(sensor_state==1 and last_state==0 ):
        print("Unbroken") 
    if(sensor_state==0 and last_state==1):
        print("broken")
    last_state = sensor_state
    """
    time.sleep(.02)
