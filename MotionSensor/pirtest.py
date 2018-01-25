from flask import Flask, request
from flask_cors import CORS, cross_origin
from OpenSSL import SSL
from threading import Thread
import pygame
import os

UPLOAD_FOLDER = 'static/MotionSensorImages'
ALLOWED_EXTENSIONS = set(['jpg', 'wav'])

context = SSL.Context(SSL.SSLv23_METHOD)

app = Flask(__name__)
CORS(app)

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

def thread_for_motion_sensor():
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

thread = Thread(target = thread_for_motion_sensor)
##thread.start()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello World2'

@app.route('/mic_test', methods=['GET', 'POST'])
def mic_test():
    print('Somewhere')
    if request.method == 'POST':
        if 'file' not in request.files:
            print("File Not in Request")
            return "Woopsie, no file found"
        file = request.files['file']
        if file.filename == '':
            print("No Selected File")
            return "Woopsie, no selected file"
        if file and allowed_file(file.filename):
            data = request.form
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print(str(os.stat))
            pygame.mixer.init()
            pygame.mixer.music.load(app.config['UPLOAD_FOLDER'] + "/securityMessage.wav")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
    
    return 'Hello World'

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host = '0.0.0.0', port = 8081)
    thread.join()
    
