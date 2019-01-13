import cv2
import os
import numpy as np
import time
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor

#os.putenv('SDL_VIDEORIVER','fbcon')
#os.putenv('SDL_FBDEV','/dev/fb1')
#os.putenv('SDL_MOUSEDRV','TSLIB')
#os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
ultrasonic = DistanceSensor(echo=16, trigger=24)

p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19,1000/21.5)
p.start(0)
q.start(0)

def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    #time.sleep(0.6)
    
def find():
    p.ChangeFrequency(1000/21.51)
    p.ChangeDutyCycle(151/21.51)
    q.ChangeDutyCycle(0)
    #time.sleep(0.02)
    #stop()
    back()
    
def back():
    if ultrasonic.distance<0.1 and ultrasonic.distance!=0:
        q.ChangeFrequency(1000/21.51)
        q.ChangeDutyCycle(151/21.51)
        p.ChangeFrequency(1000/21.49)
        p.ChangeDutyCycle(149/21.49)
        #time.sleep(0.1)
        #stop()
        
    

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);


cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
global Id
Id=0

font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
while True:
    print(ultrasonic.distance)
    ret, frame =cam.read()
    im=cv2.flip(frame, -1)
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,1.2,5)
    f=False
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        
        if(conf<51):
            if(Id==1):
                Id="Zitao"
                
            elif(Id==2):
                Id="Jingyi"
                f=True
                xfacecenter = x+w/2
                if xfacecenter>110 and xfacecenter<210:
                    
                    if ultrasonic.distance>0.3 and ultrasonic.distance!=0:
                        print("xfacecenter = " + str (xfacecenter))
                        p.ChangeFrequency(1000/21.51)
                        p.ChangeDutyCycle(151/21.51)
                        q.ChangeFrequency(1000/21.49)
                        q.ChangeDutyCycle(149/21.49)
                        #time.sleep(0.1)
                        #stop()
                    else:
                        p.ChangeDutyCycle(0)
                        q.ChangeDutyCycle(0)
                        time.sleep(3)
                    
                    
                if xfacecenter>210:
                    p.ChangeFrequency(1000/21.51)
                    p.ChangeDutyCycle(151/21.51)
                    q.ChangeDutyCycle(0)
                    #time.sleep(0.02)
                    #stop()
                if xfacecenter<110:
                    p.ChangeDutyCycle(0)
                    q.ChangeFrequency(1000/21.49)
                    q.ChangeDutyCycle(149/21.49)
                    #time.sleep(0.02)
                    #stop()
                    
        else:
            Id="unknown"
            
        cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
    if(f==False):
        find()
            
    cv2.imshow('im',im)
        
    if cv2.waitKey(10) & 0xff==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()
