#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import pygame # Import pygame graphics library 
import os # for OS calls
import time
import numpy
import RPi.GPIO as GPIO
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

#use GPIO27 as bail out button
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

size = width, height = 320, 240 
speed1 = [2,2]
speed2 = [1,1]
black = 0, 0, 0

screen = pygame.display.set_mode(size) 
ball1 = pygame.image.load("football.png") 
ballrect1 = ball1.get_rect()
ball2 = pygame.image.load("tennis_ball.png") 
ballrect2 = ball2.get_rect()
ballrect2.center= (200,200)

#set a flag, when 27 pressed, quit
f = 1;
while f:
    time.sleep(0.0002)
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
    #compare the sum of the radii of two balls and the distance between two balls. If they are the same, they collide and should change the direction of speed
    if numpy.sqrt((ballrect2.centerx - ballrect1.centerx)*(ballrect2.centerx - ballrect1.centerx) + (ballrect2.centery - ballrect1.centery)*(ballrect2.centery - ballrect1.centery)) <= (ballrect1.width+ballrect2.width)/2:
        speed1[0] = -speed1[0]
        speed1[1] = -speed1[1]
        speed2[0] = -speed2[0]
        speed2[1] = -speed2[1]

    if (not GPIO.input(27)):
        f = 0;

    screen.fill(black)  #Erase the Work space
    screen.blit(ball1, ballrect1)#Combine Ball surface with workspace surface
    screen.blit(ball2, ballrect2)
    pygame.display.flip()  #display workspace on screen

