import RPi.GPIO as GPIO
import datetime
import time
import os
import requests
import picamera

camera = picamera.PiCamera()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)    ## Read output from PIR motion sensor

while True:
    i = GPIO.input(11)     ## When output from motion sensor is LOW
    if i == 0:
        print("No intruders" , i)
        time.sleep(0.1)
    elif i == 1:           ## When output from motion sensor is HIGH
        print("Intruder Detected" , i)
        url = "http://karlredmond.pythonanywhere.com/motion_detected"
        loop_value = True
        camera.capture("image.jpg")
        data = { 'PiLocation' : "Study Room",'date' : datetime.datetime.now().strftime('%Y-%m-%d'), 'time': datetime.datetime.now().strftime('%H:%M:%S')}
        while loop_value: ## Keep trying request until server response with correct image size
            file = open('/home/pi/Desktop/Project/MotionSensor/image.jpg', 'rb')
##            print(requests.post(url, files={'image' : file}, data = data).text)
            if str(requests.post(url, files={'image' : file}, data = data).text) == str(os.stat('/home/pi/Desktop/Project/MotionSensor/image.jpg').st_size):
                print('Same Size')
                loop_value = False
                file.close()     
        time.sleep(5)