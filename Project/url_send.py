import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
from datetime import datetime
import os
import smtplib
import requests

url = 'URL FOR UPLOAD IMAGE'
sensor = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
previous_state = False
current_state = False


while True:
    previous_state = current_state
    current_state = GPIO.input(sensor)

    if current_state != previous_state:
      new_state = "HIGH" if current_state else "LOW"
      print("GPIO pin %s is %s" % (sensor, new_state))

    if current_state:
      cap = cv2.VideoCapture(0)
      ret, frame = cap.read()
      cap = cv2.VideoCapture(0)
      print("Saving Photo")

    picname = datetime.now().strftime("%y-%m-%d-%H-%M")
    picname = picname+'.jpg'
    cv2.imwrite(picname, frame)

    attach = picname
    files = {'media': open(attach, 'rb').read()}
    requests.post(url, files=files)

    os.remove(picname)