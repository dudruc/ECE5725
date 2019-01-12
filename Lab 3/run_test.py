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

start=time.time()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN)
GPIO.setup(26, GPIO.IN)

#GPIO 6 and 19 as output
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pygame.init()
pygame.mouse.set_visible(False)
BLACK=0,0,0
WHITE=255,255,255
RED=255,0,0
GREEN=0,255,0
 
screen=pygame.display.set_mode((320, 240))
size=width,height=320,240
my_font=pygame.font.Font(None,20)

my_buttons1={(160,120):'STOP',(270,220):'QUIT',(60,30):'Left History',(260,30):'Right History',(80,220):'START'}
my_buttons2={(50,50):'Stop',(50,100):'Stop',(50,150):'Stop',(100,50):'0',(100,100):'0',(100,150):'0'}
my_buttons3={(250,50):'Stop',(250,100):'Stop',(250,150):'Stop',(300,50):'0',(300,100):'0',(300,150):'0'}

p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19,1000/21.5)
p.start(0)
q.start(0)

#temp is the time when start button pressed
#st2 is the time when resume button pressed
#st1 is the time when stop button pressed
color=RED
global temp
temp=time.time()
global st2
st2=0

#a function to change the history of left servo
def changebuttons2(text):
    my_buttons2[(50,150)]=my_buttons2[(50,100)]
    my_buttons2[(100,150)]=my_buttons2[(100,100)]
    my_buttons2[(50,100)]=my_buttons2[(50,50)]
    my_buttons2[(100,100)]=my_buttons2[(100,50)]
    my_buttons2[(50,50)]=text
    my_buttons2[(100,50)]=str(int(time.time()-temp))
    
#a function to change the history os right servo
def changebuttons3(text):
    my_buttons3[(250,150)]=my_buttons3[(250,100)]
    my_buttons3[(300,150)]=my_buttons3[(300,100)]
    my_buttons3[(250,100)]=my_buttons3[(250,50)]
    my_buttons3[(300,100)]=my_buttons3[(300,50)]
    my_buttons3[(250,50)]=text
    my_buttons3[(300,50)]=str(int(time.time()-temp))
    
#a function to stop two servo
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
  
#a function to draw on the piTFT screen
def scrdis():
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

#lp us a flag for the loop of start button
#we use state to distinguish which different actions in one period of run_test
code_running=True
lp=False
state=0
while code_running:
    
    scrdis()
    
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y = pos
            if y>90 and y<150:
                if x<190 and x>130:
                    if my_buttons1[(160,120)]=="STOP":
                        my_buttons1[(160,120)]="RESUME"
                        color=GREEN
                        #make lp false to stop the loop
                        lp=False
                        p.ChangeDutyCycle(0)
                        q.ChangeDutyCycle(0)
                        #st1 is the time when stop button pressed 
                        st1=time.time()
                        temp1=my_buttons2[(50,50)]
                        temp2=my_buttons3[(250,50)]
                        
                        my_buttons2[(50,150)]=my_buttons2[(50,100)]
                        my_buttons2[(100,150)]=my_buttons2[(100,100)]
                        my_buttons2[(50,100)]=my_buttons2[(50,50)]
                        my_buttons2[(100,100)]=my_buttons2[(100,50)]
                        my_buttons2[(50,50)]="panic stop"
                        my_buttons2[(100,50)]=str(int(time.time()-temp))
                        
                        my_buttons3[(250,150)]=my_buttons3[(250,100)]
                        my_buttons3[(300,150)]=my_buttons3[(300,100)]
                        my_buttons3[(250,100)]=my_buttons3[(250,50)]
                        my_buttons3[(300,100)]=my_buttons3[(300,50)]
                        my_buttons3[(250,50)]="panic stop"
                        my_buttons3[(300,50)]=str(int(time.time()-temp))
                        
                        scrdis();
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
                        my_buttons2[(100,50)]=str(int(time.time()-temp))
                        
                        my_buttons3[(250,150)]=my_buttons3[(250,100)]
                        my_buttons3[(300,150)]=my_buttons3[(300,100)]
                        my_buttons3[(250,100)]=my_buttons3[(250,50)]
                        my_buttons3[(300,100)]=my_buttons3[(300,50)]
                        my_buttons3[(250,50)]=my_buttons3[(250,150)]
                        my_buttons3[(300,50)]=str(int(time.time()-temp))
                        
                        #because we use the time to determine which state in a period the servo should be in
                        #when resume pressed, st2-st1 is passed
                        #if we want to return the state when stop pressed
                        #we should record the time difference and get rid of them when determine which state it is in
                        st2=st2+time.time()-st1
                        scrdis()
                        #mark the flag true and resume the loop
                        lp=True
            if x>60 and x<100:
                if y<240 and y>200:
                    print"start pressed"
                    temp=time.time()
                    #make lp true to start the loop
                    lp=True
                    
            if x<290 and x>250:
                if y<240 and y>200:
                    print"Quit pressed"
                    lp=False
                    code_running=False
    #use the now-time minus the start time minus the time difference between stop button and resume button
    #to determine what action the servo should do and help track the action after stop button pressed
    if lp:
        #move the robot forward for 3 s
        if((time.time()-temp-st2)%12.0<=3 and (time.time()-temp-st2)%12.0>0):
            #use states as flags to make the history only print once in a loop
            if state==0:
                changebuttons2("Counter-Clk")
                changebuttons3("Clkwise")
                scrdis()
                state=1
                
            p.ChangeFrequency(1000/21.6)
            p.ChangeDutyCycle(160/21.6)
            q.ChangeFrequency(1000/21.4)
            q.ChangeDutyCycle(140/21.4)

        #make the robot stop for 1 second
        elif((time.time()-temp-st2)%12.0<=4 and (time.time()-temp-st2)%12.0>3):
            if state==1:
                changebuttons2("Stop")
                changebuttons3("Stop")
                scrdis()
                state=2
            stop()

        #make the robot backward for 3 seconds                        
        elif((time.time()-temp-st2)%12.0<=7 and (time.time()-temp-st2)%12.0>4):            
            if state==2:
                changebuttons2("Clkwise")
                changebuttons3("Counter-Clk")
                scrdis()
                state=3
                
            p.ChangeFrequency(1000/21.4)
            p.ChangeDutyCycle(140/21.4)
            q.ChangeFrequency(1000/21.6)
            q.ChangeDutyCycle(160/21.6)
        
        #make the robot stop for one second
        elif((time.time()-temp-st2)%12.0<=8 and (time.time()-temp-st2)%12.0>7):
            if state==3:
                changebuttons2("Stop")
                changebuttons3("Stop")
                scrdis()
                state=4
            stop()
                    
        #make the robot pivot left for one second
        elif((time.time()-temp-st2)%12.0<=9 and (time.time()-temp-st2)%12.0>8):
            if state==4:
                changebuttons3("Clkwise")
                scrdis()
                state=5
                
            q.ChangeFrequency(1000/21.4)
            q.ChangeDutyCycle(140/21.4)
        #make the robot stop for one second
        elif((time.time()-temp-st2)%12.0<=10 and (time.time()-temp-st2)%12.0>9):
            if state==5:
                changebuttons3("Stop")
                scrdis()
                state=6
            stop()
        #make the robot pivot right for one second
        elif((time.time()-temp-st2)%12.0<=11 and (time.time()-temp-st2)%12.0>10):
            if state==6:
                changebuttons2("Counter-Clk")
                scrdis()
                state=7
                
            p.ChangeFrequency(1000/21.6)
            p.ChangeDutyCycle(160/21.6)
        #make the robot stop for one second
        elif((time.time()-temp-st2)%12.0>11):
            if state==7:
                changebuttons2("Stop")
                scrdis()
                state=0
            stop()
    
    #time bail out
    elapsed_time=time.time()-start
    if elapsed_time >= 90:
        code_running=False
        
GPIO.cleanup()
