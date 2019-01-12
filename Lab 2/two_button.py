#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import pygame
from pygame.locals import*
import os
import time
import numpy
import RPi.GPIO as GPIO

timelimit = 30
start_time=time.time()

#show in piTFT
os.putenv('SDL_VIDEORIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False)
WHITE=255,255,255
BLACK=0,0,0
screen=pygame.display.set_mode((320,240))
size=width,height=320,240

ball1=pygame.image.load("football.png")
ballrect1=ball1.get_rect()
ball2=pygame.image.load("tennis_ball.png")
ballrect2=ball2.get_rect()
ballrect2.center=(200,200)
speed1=[2,2]
speed2=[1,1]
#set a flag for ball, if start button pressed, initialize two balls
global ball
ball = False

my_font=pygame.font.Font(None,30)
my_buttons={'start':(80,220),'quit':(240,220)}
screen.fill(BLACK)

def my_button(channel):
    print(" ")
    print"button 27 pressed"
    global code_running
    code_running = False

#show buttons on the screen after running the program
for my_text, text_pos in my_buttons.items():
    text_surface=my_font.render(my_text, True, WHITE)
    rect=text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)

pygame.display.flip()

#the default value of code_running is true
code_running = True

GPIO.add_event_detect(27, GPIO.FALLING, callback=my_button, bouncetime=300)

while code_running:
    if ball:
        time.sleep(0.002)
        ballrect1 = ballrect1.move(speed1)
        if ballrect1.left < 0 or ballrect1.right > width:
            speed1[0] = -speed1[0]
        if ballrect1.top < 0 or ballrect1.bottom > height:
            speed1[1] = -speed1[1]

        ballrect2 = ballrect2.move(speed2)
        if ballrect2.left < 0 or ballrect2.right > width:
            speed2[0] = -speed2[0]
        if ballrect2.top < 0 or ballrect2.bottom > height:
            speed2[1] = -speed2[1]

        if numpy.sqrt((ballrect2.centerx - ballrect1.centerx)*(ballrect2.centerx - ballrect1.centerx) + (ballrect2.centery - ballrect1.centery)*(ballrect2.centery - ballrect1.centery)) <= (ballrect1.width+ballrect2.width)/2:
            speed1[0] = -speed1[0]
            speed1[1] = -speed1[1]
            speed2[0] = -speed2[0]
            speed2[1] = -speed2[1]

        screen.fill(BLACK)  #Erase the Work space
        screen.blit(ball1, ballrect1)#Combine Ball surface with workspace surface
        screen.blit(ball2, ballrect2)
        
        #show buttons after start
        for my_text, text_pos in my_buttons.items():
            text_surface=my_font.render(my_text, True, WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
        
        #show coordinates after start
        coordinates="touch at "+str(x)+","+str(y)
        text_surface=my_font.render(coordinates, True, WHITE)
        rect=text_surface.get_rect(center=(160,120))
        screen.blit(text_surface, rect)
        pygame.display.flip()

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y=pos
            screen.fill(BLACK)
            coordinates="touch at "+str(x)+","+str(y)
            for my_text, text_pos in my_buttons.items():
                #show buttons before start
                text_surface=my_font.render(coordinates, True, WHITE)
                rect=text_surface.get_rect(center=(160,120))
                screen.blit(text_surface, rect)
                #show coordinates before start
                text_surface=my_font.render(my_text, True, WHITE)
                rect=text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            pygame.display.flip()
            print coordinates
                        
            if y>200:
                if x<100 and x>60:
                    #after pressing start, the flag sets true and the screen starts showing two ball animation
                    print"start pressed"
                    ball = True
                elif x>220 and x<260:
                    print"quit pressed"
                    code_running=False

    #time out
    now=time.time()
    elapsed_time=now-start_time
    if elapsed_time >= timelimit:
        code_running=False
