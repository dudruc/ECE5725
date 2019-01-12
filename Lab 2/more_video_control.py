#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN)
GPIO.setup(26, GPIO.IN)
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
    if(not GPIO.input(5)):
        print(" ")
        print"Button 5 pressed..."
        cmd = 'echo "seek -30" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)
    if(not GPIO.input(26)):
        print(" ")
        print"Button 26 pressed..."
        cmd = 'echo "seek +30" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)
    if(not GPIO.input(27)):
        print(" ")
        print"Button 27 pressed..."
        cmd = 'echo "quit" > /home/pi/lab1/video_fifo'
        print subprocess.check_output(cmd, shell= True)


