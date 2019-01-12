#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# We use GPIO5 and GPIO26 as two additional buttons

GPIO.setup(5, GPIO.IN)
GPIO.setup(26, GPIO.IN)


b = True
while b:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        print(" ")
        print"Button 17 pressed..."
    if(not GPIO.input(22)):
        print(" ")
        print"Button 22 pressed..."
    if(not GPIO.input(23)):
        print(" ")
        print"Button 23 pressed..."
    if(not GPIO.input(5)):
        print(" ")
        print"Button 5 pressed..."
    if(not GPIO.input(26)):
        print(" ")
        print"Button 26 pressed..."
    if(not GPIO.input(27)):
        print(" ")
        print"Button 27 pressed..."
        #when the quit button is pressed, break the loop
        b= False


