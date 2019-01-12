#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab3 2018-10-10
import pygame
from pygame.locals import*
import os
import RPi.GPIO as GPIO
import time

os.putenv('SDL_VIDEORIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

#record start time
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

pygame.init()
pygame.mouse.set_visible(False)
#set color
BLACK=0,0,0
WHITE=255,255,255
RED=255,0,0
GREEN=0,255,0
screen=pygame.display.set_mode((320, 240))
size=width,height=320,240
my_font=pygame.font.Font(None,20)

#use coordinates as values and the button name as key
#default history is "stop" and default time is "0"
my_buttons1={(160,120):'STOP',(270,220):'QUIT',(60,30):'Left History',(260,30):'Right History'}
my_buttons2={(50,50):'Stop',(50,100):'Stop',(50,150):'Stop',(100,50):'0',(100,100):'0',(100,150):'0'}
my_buttons3={(250,50):'Stop',(250,100):'Stop',(250,150):'Stop',(300,50):'0',(300,100):'0',(300,150):'0'}

#start servos as duty cycle = 0, which means stop
p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19,1000/21.5)
p.start(0)
q.start(0)

def GPIO17_callback(channel): 
    print(" ")
    print"Left servo, clockwise"
    p.ChangeFrequency(1000/21.3)
    p.ChangeDutyCycle(130/21.3)
def GPIO22_callback(channel): 
    print(" ")
    print"Left servo, counter-clockwise"
    p.ChangeFrequency(1000/21.7)
    p.ChangeDutyCycle(170/21.7)
def GPIO23_callback(channel): 
    print(" ")
    print"Right servo, clockwise"
    q.ChangeFrequency(1000/21.3)
    q.ChangeDutyCycle(130/21.3)
def GPIO5_callback(channel): 
    print(" ")
    print"Left servo, stop"
    p.ChangeFrequency(1000/21.5)
    p.ChangeDutyCycle(0)
def GPIO26_callback(channel): 
    print(" ")
    print"Right servo, stop"
    q.ChangeFrequency(1000/21.5)
    q.ChangeDutyCycle(0)
def GPIO27_callback(channel): 
    print(" ")
    print"Right servo, counter-clockwise"
    q.ChangeFrequency(1000/21.7)
    q.ChangeDutyCycle(170/21.7)
    
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)
GPIO.add_event_detect(23, GPIO.FALLING, callback=GPIO23_callback, bouncetime=300)
GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO5_callback, bouncetime=300)
GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO26_callback, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)

#set the stop circle color is red
color=RED
code_running=True
while code_running:
    time.sleep(0.2)
    #for the history, move the last history to the second line and move the second line to the third line.
    #put the action on the first line and calculate the time
    if(not GPIO.input(17)):
        my_buttons2[(50,150)]=my_buttons2[(50,100)]
        my_buttons2[(100,150)]=my_buttons2[(100,100)]
        my_buttons2[(50,100)]=my_buttons2[(50,50)]
        my_buttons2[(100,100)]=my_buttons2[(100,50)]
        my_buttons2[(50,50)]="Clkwise"
        my_buttons2[(100,50)]=str(int(time.time()-start))
    
    if(not GPIO.input(22)):
        my_buttons2[(50,150)]=my_buttons2[(50,100)]
        my_buttons2[(100,150)]=my_buttons2[(100,100)]
        my_buttons2[(50,100)]=my_buttons2[(50,50)]
        my_buttons2[(100,100)]=my_buttons2[(100,50)]
        my_buttons2[(50,50)]="Counter-Clk"
        my_buttons2[(100,50)]=str(int(time.time()-start))
            
    if(not GPIO.input(5)):
        my_buttons2[(50,150)]=my_buttons2[(50,100)]
        my_buttons2[(100,150)]=my_buttons2[(100,100)]
        my_buttons2[(50,100)]=my_buttons2[(50,50)]
        my_buttons2[(100,100)]=my_buttons2[(100,50)]
        my_buttons2[(50,50)]="Stop"
        my_buttons2[(100,50)]=str(int(time.time()-start))
    
    if(not GPIO.input(23)):
        my_buttons3[(250,150)]=my_buttons3[(250,100)]
        my_buttons3[(300,150)]=my_buttons3[(300,100)]
        my_buttons3[(250,100)]=my_buttons3[(250,50)]
        my_buttons3[(300,100)]=my_buttons3[(300,50)]
        my_buttons3[(250,50)]="Clkwise"
        my_buttons3[(300,50)]=str(int(time.time()-start))
            
    if(not GPIO.input(27)):
        my_buttons3[(250,150)]=my_buttons3[(250,100)]
        my_buttons3[(300,150)]=my_buttons3[(300,100)]
        my_buttons3[(250,100)]=my_buttons3[(250,50)]
        my_buttons3[(300,100)]=my_buttons3[(300,50)]
        my_buttons3[(250,50)]="Counter-Clk"
        my_buttons3[(300,50)]=str(int(time.time()-start))
            
    if(not GPIO.input(26)):
        my_buttons3[(250,150)]=my_buttons3[(250,100)]
        my_buttons3[(300,150)]=my_buttons3[(300,100)]
        my_buttons3[(250,100)]=my_buttons3[(250,50)]
        my_buttons3[(300,100)]=my_buttons3[(300,50)]
        my_buttons3[(250,50)]="Stop"
        my_buttons3[(300,50)]=str(int(time.time()-start))

    #design button function
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y = pos
            if y>90 and y<150:
                if x<190 and x>130:
                    #when stop presses, change the circle color to green, change the duty cycle of two servos to 0 to make it stop.
                    #and change the history of two wheels
                    #record the action when stop pressed
                    if my_buttons1[(160,120)]=="STOP":
                        my_buttons1[(160,120)]="RESUME"
                        color=GREEN
                        p.ChangeDutyCycle(0)
                        q.ChangeDutyCycle(0)
                        temp1=my_buttons2[(50,50)]
                        temp2=my_buttons3[(250,50)]
                        
                        my_buttons2[(50,150)]=my_buttons2[(50,100)]
                        my_buttons2[(100,150)]=my_buttons2[(100,100)]
                        my_buttons2[(50,100)]=my_buttons2[(50,50)]
                        my_buttons2[(100,100)]=my_buttons2[(100,50)]
                        my_buttons2[(50,50)]="panic stop"
                        my_buttons2[(100,50)]=str(int(time.time()-start))
                        
                        my_buttons3[(250,150)]=my_buttons3[(250,100)]
                        my_buttons3[(300,150)]=my_buttons3[(300,100)]
                        my_buttons3[(250,100)]=my_buttons3[(250,50)]
                        my_buttons3[(300,100)]=my_buttons3[(300,50)]
                        my_buttons3[(250,50)]="panic stop"
                        my_buttons3[(300,50)]=str(int(time.time()-start))
                    #when resume pressed, change the circle color to red, resume the movement according to the record from stop button
                    elif my_buttons1[(160,120)]=="RESUME":
                        my_buttons1[(160,120)]="STOP"
                        color=RED
                        if temp1== "Clkwise":
                            p.ChangeFrequency(1000/21.3)
                            p.ChangeDutyCycle(130/21.3)
                        elif temp1=="Counter-Clk":
                            p.ChangeFrequency(1000/21.7)
                            p.ChangeDutyCycle(170/21.7)
                        elif temp1=="Stop":
                            p.ChangeDutyCycle(0)
                            
                        if temp2== "Clkwise":
                            q.ChangeFrequency(1000/21.3)
                            q.ChangeDutyCycle(130/21.3)
                        elif temp2=="Counter-Clk":
                            q.ChangeFrequency(1000/21.7)
                            q.ChangeDutyCycle(170/21.7)
                        elif temp2=="Stop":
                            q.ChangeDutyCycle(0)
                            
                        my_buttons2[(50,150)]=my_buttons2[(50,100)]
                        my_buttons2[(100,150)]=my_buttons2[(100,100)]
                        my_buttons2[(50,100)]=my_buttons2[(50,50)]
                        my_buttons2[(100,100)]=my_buttons2[(100,50)]
                        my_buttons2[(50,50)]=my_buttons2[(50,150)]
                        my_buttons2[(100,50)]=str(int(time.time()-start))
                        
                        my_buttons3[(250,150)]=my_buttons3[(250,100)]
                        my_buttons3[(300,150)]=my_buttons3[(300,100)]
                        my_buttons3[(250,100)]=my_buttons3[(250,50)]
                        my_buttons3[(300,100)]=my_buttons3[(300,50)]
                        my_buttons3[(250,50)]=my_buttons3[(250,150)]
                        my_buttons3[(300,50)]=str(int(time.time()-start))
            #when quit pressed, change the flag to false and quit the program
            if x<290 and x>250:
                if y<240 and y>200:
                    print"Quit pressed"
                    code_running=False
            
    #draw and flip on the screen after every loop
    screen.fill(BLACK)
    
    pygame.draw.circle(screen,color,[160,120],30)
    
    for text_pos, my_text in my_buttons1.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
            
    for text_pos, my_text in my_buttons2.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)

    for text_pos, my_text in my_buttons3.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)
    pygame.display.flip()
    
    #time bail out
    elapsed_time=time.time()-start
    if elapsed_time >= 90:
        code_running=False
        
GPIO.cleanup()

