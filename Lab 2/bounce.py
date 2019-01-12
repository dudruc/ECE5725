#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab2 2018-09-26
import pygame # Import pygame graphics library 
import os # for OS calls
os.putenv('SDL_VIDEODRIVER', 'fbcon') #display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()

#ser the screen size,speed and the background color
size = width, height = 320, 240 
speed = [2,2]
black = 0, 0, 0

screen = pygame.display.set_mode(size) 
ball = pygame.image.load("football.png") 
#get the rectangular area of the ball
ballrect = ball.get_rect()

while 1:
    ballrect = ballrect.move(speed)
    #change speed
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)  #Erase the Work space
    screen.blit(ball, ballrect)  #Combine Ball surface with workspace surface
    pygame.display.flip()  #display workspace on screen
