import pygame
from pygame.locals import*
import os
import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

os.putenv('SDL_VIDEORIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
ultrasonic2 = DistanceSensor(echo=13, trigger=4)
ultrasonic1 = DistanceSensor(echo=26, trigger=5)
ultrasonic3 = DistanceSensor(echo=16, trigger=24)

pygame.init()
pygame.mouse.set_visible(False)
BLACK=0,0,0
WHITE=255,255,255
RED=255,0,0
GREEN=0,255,0
 
screen=pygame.display.set_mode((320, 240))
size=width,height=320,240
my_font=pygame.font.Font(None,20)

my_buttons={'OWNER':(280,50),'BALL':(280,100),'WANDER':(280,150),'QUIT':(280,200)}

p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19,1000/21.5)
p.start(0)
q.start(0)

code_running=True
lp=False

first=True
state=1
tempstate=0

def bailout(channel):
    print(" ")
    print"button 27 pressed"
    global code_running
    code_running = False
    GPIO.cleanup()
    
#a function to stop two servo
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
  
#a function to draw on the piTFT screen
def scrdis():
    screen.fill(BLACK)
    
    for my_text, text_pos in my_buttons.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
    
    pygame.display.flip()
    
#a funtion to turn the direction in order to avoid hitting the wall
def turn():
    p.ChangeDutyCycle(0)
    q.ChangeFrequency(1000/21.4)
    q.ChangeDutyCycle(140/21.4)
    print(ultrasonic.distance)
    time.sleep(0.5)
    state = 0



GPIO.add_event_detect(27, GPIO.FALLING, callback=bailout, bouncetime=300)

while code_running:
    
    scrdis()

    
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y = pos
            if x>260 and x<300:
                if y>140 and y<160:
                    print"wander mode started"
                    start=time.time()
                    lp=True
                    
            if x>260 and x<300:
                if y>190 and y<210:
                    print"quit pressed"
                    code_running=False
                    
                    
    if lp:
        time.sleep(0.02)
        if state==1:
            if first==True:
                start=time.time()
                first = False
            p.ChangeFrequency(1000/21.6)
            p.ChangeDutyCycle(160/21.6)
            q.ChangeFrequency(1000/21.4)
            q.ChangeDutyCycle(140/21.4)
            if time.time()-start >= 2:
                state=2
                first=True
                
        if state==2:
            if first==True:
                start=time.time()
                first = False
                p.ChangeDutyCycle(0)
                q.ChangeFrequency(1000/21.4)
                q.ChangeDutyCycle(140/21.4)
            if time.time()-start >= 1:
                state=3
                first=True
                
        if state==3:
            if first==True:
                start=time.time()
                first = False
            p.ChangeFrequency(1000/21.6)
            p.ChangeDutyCycle(160/21.6)
            q.ChangeFrequency(1000/21.4)
            q.ChangeDutyCycle(140/21.4)
            if time.time()-start >= 2:
                state=4
                first=True
                
        if state==4:
            if first==True:
                start=time.time()
                first = False
                p.ChangeFrequency(1000/21.6)
                p.ChangeDutyCycle(160/21.6)
                q.ChangeDutyCycle(0)
            if time.time()-start >= 1:
                state=1
                first=True
        
        if state==5:
            p.ChangeDutyCycle(0)
            q.ChangeFrequency(1000/21.4)
            q.ChangeDutyCycle(140/21.4)
            print("l")
            print(ultrasonic1.distance)
            if ultrasonic1.distance > 0.25:
                state = 1
                first = True
            
        if state==6:
            q.ChangeDutyCycle(0)
            p.ChangeFrequency(1000/21.6)
            p.ChangeDutyCycle(160/21.6)
            print("r")
            if ultrasonic2.distance > 0.25:
                state = 1
                first = True
                
        if state==7:
            q.ChangeFrequency(1000/21.6)
            q.ChangeDutyCycle(160/21.6)
            p.ChangeFrequency(1000/21.4)
            p.ChangeDutyCycle(140/21.4)
            if ultrasonic1.distance < 0.25 and ultrasonic2.distance > 0.25:
                state = 5
              
            if ultrasonic2.distance < 0.25 and ultrasonic1.distance > 0.25:
                state = 6
            
            if ultrasonic1.distance > 0.25 and ultrasonic2.distance > 0.25:
                state = 1
                first = True
                
            if ultrasonic3.distance > 0.25:
                
                state = 1
                first = True
            
          
        if ultrasonic1.distance < 0.25 and ultrasonic2.distance > 0.25:
            state = 5
              
        if ultrasonic2.distance < 0.25 and ultrasonic1.distance > 0.25:
            state = 6
            
        if ultrasonic1.distance < 0.25 and ultrasonic2.distance < 0.25:
            state = 7
        if ultrasonic3.distance <0.25:
            state=7

            

GPIO.cleanup()
