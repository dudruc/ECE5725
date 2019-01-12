#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import pygame
from pygame.locals import*
import os
import time
import RPi.GPIO as GPIO

#after 30s, the program will end 
timelimit = 30
start_time=time.time()

os.putenv('SDL_VIDEORIVER','fbcon') #Display on piTFT
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB') #Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

#set GPIO27 as the physical bail out button
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False) #turn off the mouse cursor
WHITE=255,255,255
BLACK=0,0,0
screen=pygame.display.set_mode((320,240))

my_font=pygame.font.Font(None,50)
#the button text and position
my_buttons={'quit':(80,180)}
screen.fill(BLACK)

def my_button(channel):
    print(" ")
    print"button 27 pressed"
    global code_running
    code_running = False


for my_text, text_pos in my_buttons.items():
    #combine the button surfaces and display on the screen
    text_surface=my_font.render(my_text, True, WHITE)
    rect=text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)

pygame.display.flip()

code_running = True

GPIO.add_event_detect(27, GPIO.FALLING, callback=my_button, bouncetime=300)

while code_running:
    #scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()

            #find which quarter of the screen we touched
            x,y=pos
            
            if y>120 and x<160:
                print"quit pressed"
                code_running=False

    now=time.time()
    elapsed_time=now-start_time
    if elapsed_time >= timelimit:
        code_running=False
