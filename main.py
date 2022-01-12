import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import os
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

import csv
import boto3
import json

import pymysql
#from aws_rds_python import *

#db = pymysql.connect('cypherdb.ctpwq4gznveu.us-east-2.rds.amazonaws.com','admin','cypherpervasive')
#cursor = db.cursor()

def report(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Unknown Person Detected'
    msg['From'] = 'ccpervasive@email.com'
    msg['To'] = 'michael.joseph1017@email.com'

    text = MIMEText("Stranger Detected! Call La Policia!")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("@gmail.com","password")
    server.sendmail("ccpervasive@gmail.com", 'michael.joseph1017@gmail.com',  msg.as_string())
    server.quit()

with open('new_user_credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

camera = PiCamera()
camera.rotation = 180

relay = 18
TRIG = 21
ECHO = 20
led = 23

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(led,GPIO.OUT)
GPIO.setup(relay, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(relay, 0)
locked = True
distance = 100
while locked:
    
    while distance > 10:
        
        GPIO.output(TRIG, False)
        print("Ultrasonic Measurement")
        # Allow module to settle
        time.sleep(1)
        # Send 10us pulse to trigger
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        start = time.time()

        while GPIO.input(ECHO)==0:
          start = time.time()

        while GPIO.input(ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start
        distancet = elapsed * 34300
        # That was the distance there and back so halve the value
        distance = distancet / 2

        print("Distance :", distance)
        print("Elaspsed time :", elapsed)


    print("Object Detected")
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/Desktop/livecapture.jpg')
    camera.stop_preview()
    photo = '/home/pi/Desktop/livecapture.jpg'
    
    s3_client = boto3.client('s3',
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key)
    s3_client.upload_file(photo, 'face-comparison-mja', 'live-capture')



    client = boto3.client('rekognition',
                          region_name='ap-southeast-1',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key)


    try:
        response = client.compare_faces(
                SourceImage={
                    'S3Object': {
                        'Bucket': 'face-comparison-mja',
                        'Name': 'live-capture'
                    }
                },
                TargetImage={
                    'S3Object': {
                        'Bucket': 'face-comparison-mja',
                        'Name': 'MJ.jpg'
                    }
                },
        )


    except:
        print("Face Not Recognized")
        time.sleep(0.5)
        report(photo)
        GPIO.output(relay, 0)
        break

    match = False
    for key, value in response.items():
        if key == 'FaceMatches' and value != '' and value != []:
            if(value[0]['Similarity'] > 95):
                match = True


    if(match):
        print('Face Recognized...')
        GPIO.output(23,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(relay, 0)
        #sendLog("Face Matched")
        #time.sleep(5)
        GPIO.output(relay, 1)
        time.sleep(5)
        GPIO.output(23,GPIO.LOW)
        GPIO.output(relay, 0)
        locked = False

    else:
        print('Unmatched Faces')
        time.sleep(0.5)
        report(photo)
        GPIO.output(relay, 0)
        break
        #sendLog("Unknown Face Detected.")
