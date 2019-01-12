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

def GPIO17_callback(channel):
    print(" ")
    print"falling edge detected on 17"
    cmd = 'echo "pause" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)

def GPIO22_callback(channel):
    print(" ")
    print"falling edge detected on 22"
    cmd = 'echo "seek +10" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)

def GPIO23_callback(channel):
    print(" ")
    print"falling edge detected on 23"
    cmd = 'echo "seek -10" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)

def GPIO5_callback(channel):
    print(" ")
    print"falling edge detected on 5"
    cmd = 'echo "seek -30" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)
    
def GPIO26_callback(channel):
    print(" ")
    print"falling edge detected on 26"
    cmd = 'echo "seek +30" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO5_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)

try:
    print "Waiting for falling edge on port 27"
    #after 10s, quit
    GPIO.wait_for_edge(27, GPIO.FALLING, timeout=10000)
    print "Falling edge detected on port 27"
    cmd = 'echo "quit" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell= True)

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

