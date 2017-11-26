import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)    ## Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)    ## LED output pin

while True:
    i = GPIO.input(11)     ## When output from motion sensor is LOW
    if i == 0:
        print("No intruders" , i)
        GPIO.output(3, 0 ) ## Turn OFF LED
        time.sleep(0.1)
    elif i == 1:           ## When output from motion sensor is HIGH
        print("Intruder Detected" , i)
        url = "http://192.168.1.6:5000/motion_detected"
        GPIO.output(3,1)   ## Turn ON LED
        requests.get(url)
        time.sleep(5)