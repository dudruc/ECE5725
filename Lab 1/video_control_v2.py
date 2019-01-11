#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab 1 2018-09-12

import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(0.2)
    if(not GPIO.input(17)):
        print(" ")
        print"Button 17 pressed..."
        cmd = 'echo "pause" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)
    if(not GPIO.input(22)):
        print(" ")
        print"Button 22 pressed..."
        cmd = 'echo "seek +10" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)
    if(not GPIO.input(23)):
        print(" ")
        print"Button 23 pressed..."
        cmd = 'echo "seek -10" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)
    if(not GPIO.input(27)):
        print(" ")
        print"Button 27 pressed..."
        cmd = 'echo "quit" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)


