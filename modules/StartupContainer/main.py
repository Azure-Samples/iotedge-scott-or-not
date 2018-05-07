# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import argparse
import os
import random
import time
import sys
import socket
import requests
import io

from threading import Thread
from time import sleep
from flask import Flask, request, redirect, url_for, jsonify

COUNTER = 0
# pull camera images and stream data to image recognition service
def stream_camera_data(camera):
      while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg')
            stream.seek(0)
            image = {'image': stream }
            
            try:
                global COUNTER
                COUNTER = COUNTER + 1
                if COUNTER > 1000:
                    COUNTER = 0
                f = open('/home/pi/image/analyzing' + str(COUNTER) + '.jpg', 'wb') 
                f.write(stream.read())
                f.close()
                stream.seek(0)
                print('sending to classifier', AZURE_ML_HOSTNAME)
                requests.post('http://' + socket.gethostbyname(AZURE_ML_HOSTNAME) + ':8080/classify', files=image)
      
            except Exception as e:
                  print(e)

def startup():
    print ( "\nPython %s\n" % sys.version )
    print ( "IoT Hub Module for Python" )

    global AZURE_ML_HOSTNAME
    AZURE_ML_HOSTNAME = os.environ.get('AZURE_ML_HOSTNAME')

def obj_camera():
    if os.environ.get('DEVICE') == 'RPI':
        print( "\nRunning on linux...")
        import picamera
        camera = picamera.PiCamera()
        camera.rotation = 180
        camera.resolution = (640, 480)
        camera.start_preview()
        return camera
    else:
        from utils import camera
        return camera

def flash_yes():
    from utils import flash
    flash.flash_yes()

def flash_no():
    from utils import flash
    flash.flash_no()

# Start web server
application = Flask(__name__)

@application.route('/yes', methods=['POST'])
def yes():
    if os.environ.get('DEVICE') == 'RPI':
        flash_yes()
        return 'OK'
    return 'No Sense Hat'

@application.route('/no', methods=['POST'])
def no():
    if os.environ.get('DEVICE') == 'RPI':
        flash_no()
        return 'OK'
    return 'No Sense Hat'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port',
        type=int,
        default=8082,
        help='Port for http server to listen on.'
    )
    FLAGS, unparsed = parser.parse_known_args()

    startup()

    # create camera object and start camera stream
    cam = obj_camera()

    background_thread = Thread(target=stream_camera_data, args=(cam, ))
    background_thread.start()

    application.run(host='0.0.0.0', port=FLAGS.port)    