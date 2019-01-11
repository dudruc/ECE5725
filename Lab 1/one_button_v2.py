#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab 1 2018-09-12

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
#set for broadcom numbering
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2) 
#give some sleep time so only one response for one push-button
#to show that button is pressed
    if(not GPIO.input(17)):
        print(" ")
        print"Button 17 pressed..."


