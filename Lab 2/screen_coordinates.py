#JIngyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import pygame
from pygame.locals import*
import os
import time
import RPi.GPIO as GPIO

timelimit = 30
start_time=time.time()

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

my_font=pygame.font.Font(None,30)
my_buttons={'start':(80,220),'quit':(240,220)}
screen.fill(BLACK)

def my_button(channel):
    print(" ")
    print"button 27 pressed"
    global code_running
    code_running = False


for my_text, text_pos in my_buttons.items():
    text_surface=my_font.render(my_text, True, WHITE)
    rect=text_surface.get_rect(center=text_pos)
    screen.blit(text_surface, rect)

pygame.display.flip()

code_running = True

GPIO.add_event_detect(27, GPIO.FALLING, callback=my_button, bouncetime=300)

while code_running:
    screen.fill(BLACK)
    for my_text, text_pos in my_buttons.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y=pos

            #get the touch position and show in a fixed position
            coordinates="touch at "+str(x)+","+str(y)
            text_surface=my_font.render(coordinates, True, WHITE)
            rect=text_surface.get_rect(center=(160,120))
            screen.blit(text_surface, rect)
            pygame.display.flip()
            print coordinates
                        
            if y>200:
                if x<100 and x>60:
                    print"start pressed"
                elif x>220 and x<260:
                    print"quit pressed"
                    code_running=False

    now=time.time()
    elapsed_time=now-start_time
    if elapsed_time >= timelimit:
        code_running=False
