#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab3 2018-10-10
import RPi.GPIO as GPIO
import time

start=time.time()
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN)
GPIO.setup(26, GPIO.IN)

GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19, 1000/21.5)
p.start(0)
q.start(0)

#using interrupt to detect the button pressing
#write functions for each buttons, full speed
def GPIO17_callback(channel): 
    print(" ")
    print"Left servo, clockwise"
    p.ChangeFrequency(1000/(20+1.3))
    p.ChangeDutyCycle(130/(20+1.3))
def GPIO22_callback(channel): 
    print(" ")
    print"Left servo, counter-clockwise"
    p.ChangeFrequency(1000/(20+1.7))
    p.ChangeDutyCycle(170/(20+1.7))
def GPIO23_callback(channel): 
    print(" ")
    print"Right servo, clockwise"
    q.ChangeFrequency(1000/(20+1.3))
    q.ChangeDutyCycle(130/(20+1.3))
def GPIO5_callback(channel): 
    print(" ")
    print"Left servo, stop"
    p.ChangeFrequency(1000/(20+1.5))
    p.ChangeDutyCycle(0)
def GPIO26_callback(channel): 
    print(" ")
    print"Right servo, stop"
    q.ChangeFrequency(1000/(20+1.5))
    q.ChangeDutyCycle(0)
def GPIO27_callback(channel): 
    print(" ")
    print"Right servo, counter-clockwise"
    q.ChangeFrequency(1000/(20+1.7))
    q.ChangeDutyCycle(170/(20+1.7))
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO5_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

#hold for 15s and quit the program
while time.time()-start<=15:
    pass
    
GPIO.cleanup()

