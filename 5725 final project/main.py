import pygame # Import pygame graphics library 
import pygame.camera
from pygame.locals import*
import os
import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import cv2
import numpy as np
import sys



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
pygame.camera.init()
#pygame.mouse.set_visible(False)
BLACK=0,0,0
WHITE=255,255,255
RED=255,0,0
GREEN=0,255,0
 
screen=pygame.display.set_mode((320, 240))
size=width,height=320,240
my_font=pygame.font.Font(None,20)

my_buttons={'OWNER':(280,45),'WANDER':(280,100),'PBOOTH':(280,155),'QUIT':(280,210)}

p=GPIO.PWM(6,1000/21.5)
q=GPIO.PWM(19,1000/21.5)
p.start(0)
q.start(0)

global code_running
code_running=True
catini = pygame.image.load("/home/pi/final/cat/CAT4.png") 
catini = pygame.transform.scale(catini,(158,164))

ha=False
first=True
state=1
cat_wander1 = pygame.image.load("/home/pi/final/cat/CAT1.png") 
cat_wander1 = pygame.transform.scale(cat_wander1,(158,164))
cat_wander2 = pygame.image.load("/home/pi/final/cat/CAT8.png") 
cat_wander2 = pygame.transform.scale(cat_wander2,(158,164))
scared=False


fo=False
vision=False
find1 = pygame.image.load("/home/pi/final/cat/CAT5.png") 
find1 = pygame.transform.scale(find1,(158,164))
find2 = pygame.image.load("/home/pi/final/cat/CAT7.jpg") 
find2 = pygame.transform.scale(find2,(158,164))
find3 = pygame.image.load("/home/pi/final/cat/CAT2.png") 
find3 = pygame.transform.scale(find3,(158,164))
find4 = pygame.image.load("/home/pi/final/cat/CAT10.jpg") 
find4 = pygame.transform.scale(find4,(158,164))

pb=False
DEVICE = '/dev/video0'
SIZE = (320, 240)
FILENAME = 'capture.png'
catphoto1 = pygame.image.load("/home/pi/final/cat/CAT3.png") 
catphoto1 = pygame.transform.scale(catphoto1,(78,60))
catphoto2 = pygame.image.load("/home/pi/final/cat/mao.jpg") 
catphoto2 = pygame.transform.scale(catphoto2,(72,70))
catphoto3 = pygame.image.load("/home/pi/final/cat/kitty3.jpg") 
catphoto3 = pygame.transform.scale(catphoto3,(75,54))
catphoto4 = pygame.image.load("/home/pi/final/cat/tom.jpg") 
catphoto4 = pygame.transform.scale(catphoto4,(70,70))
catphoto=catphoto1
sh=False
choose=True

def bailout(channel):
    print(" ")
    print"button 27 pressed"
    code_running = False
  
#a function to draw on the piTFT screen
def scrdis():
    screen.fill(BLACK)
    for my_text, text_pos in my_buttons.items():
        text_surface=my_font.render(my_text, True, WHITE)
        rect=text_surface.get_rect(center=text_pos)
        screen.blit(text_surface, rect)

    
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    #time.sleep(0.6)
    
def find():
    p.ChangeFrequency(1000/21.51)
    p.ChangeDutyCycle(151/21.51)
    q.ChangeDutyCycle(0)
    scrdis()
    find_rect1 = find1.get_rect(center=(120,120))
    screen.blit(find1, find_rect1)
    text=my_font.render("looking for my owner", True, WHITE)
    screen.blit(text, (60,20))
    #time.sleep(0.02)
    #stop()
    back()
    
def back():
    if ultrasonic3.distance<0.15 and ultrasonic3.distance!=0:
        q.ChangeFrequency(1000/21.53)
        q.ChangeDutyCycle(153/21.53)
        p.ChangeFrequency(1000/21.47)
        p.ChangeDutyCycle(147/21.47)
        scrdis()
        catrect_wander2 = cat_wander2.get_rect(center=(120,120))
        screen.blit(cat_wander2, catrect_wander2)


GPIO.add_event_detect(27, GPIO.FALLING, callback=bailout, bouncetime=300)
scrdis()

while code_running:

    time.sleep(0.02)
    scrdis()
    if ha==False and fo==False:
        catrectini= catini.get_rect(center=(120,120))
        screen.blit(catini, catrectini)
        pygame.display.flip()
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y = pos
            if x>260 and x<300:
                if y>85 and y<115:
                    print"wander mode started"
                    start=time.time()
                    ha=True
                    
                elif y>195 and y<220:
                    print"quit pressed"
                    code_running=False
                    
                elif y>30 and y<60:
                    print"find owner"
                    fo=True
                    vision=True
                elif y>140 and y<160:
                    print"take a picture!"
                    pb=True
        
                    
    if ha:
        
        time.sleep(0.02)
        if state==1:
            if first==True:
                start=time.time()
                first = False
            p.ChangeFrequency(1000/21.55)
            p.ChangeDutyCycle(155/21.55)
            q.ChangeFrequency(1000/21.45)
            q.ChangeDutyCycle(145/21.45)
            if time.time()-start >= 2:
                state=2
                first=True
                
        elif state==2:
            if first==True:
                start=time.time()
                first = False
                p.ChangeDutyCycle(0)
                q.ChangeFrequency(1000/21.45)
                q.ChangeDutyCycle(145/21.45)
            if time.time()-start >= 1:
                state=3
                first=True
                
        elif state==3:
            if first==True:
                start=time.time()
                first = False
            p.ChangeFrequency(1000/21.55)
            p.ChangeDutyCycle(155/21.55)
            q.ChangeFrequency(1000/21.45)
            q.ChangeDutyCycle(145/21.45)
            if time.time()-start >= 2:
                state=4
                first=True
                
        elif state==4:
            if first==True:
                start=time.time()
                first = False
                p.ChangeFrequency(1000/21.55)
                p.ChangeDutyCycle(155/21.55)
                q.ChangeDutyCycle(0)
            if time.time()-start >= 1:
                state=1
                first=True
        
        if state==5:
            p.ChangeDutyCycle(0)
            q.ChangeFrequency(1000/21.45)
            q.ChangeDutyCycle(145/21.45)
            print("l")
            print(ultrasonic1.distance)
            if ultrasonic1.distance > 0.25:
                state = 1
                first = True
            
        if state==6:
            q.ChangeDutyCycle(0)
            p.ChangeFrequency(1000/21.55)
            p.ChangeDutyCycle(155/21.55)
            print("r")
            if ultrasonic2.distance > 0.25:
                state = 1
                first = True
                
        if state==7:
            q.ChangeFrequency(1000/21.55)
            q.ChangeDutyCycle(155/21.55)
            p.ChangeFrequency(1000/21.45)
            p.ChangeDutyCycle(145/21.45)
            if ultrasonic1.distance < 0.25 and ultrasonic2.distance > 0.25:
                state = 5
              
            elif ultrasonic2.distance < 0.25 and ultrasonic1.distance > 0.25:
                state = 6
            
            elif ultrasonic1.distance > 0.25 and ultrasonic2.distance > 0.25:
                state = 1
                first = True
                
            if ultrasonic3.distance > 0.25:
                q.ChangeDutyCycle(0)
                p.ChangeFrequency(1000/21.55)
                p.ChangeDutyCycle(155/21.55)
                time.sleep(0.5)
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
            
        screen.fill(BLACK)
##      show the cat on the screen
        if ultrasonic1.distance < 0.25 or ultrasonic2.distance < 0.25 or ultrasonic3.distance < 0.25:
            if scared == False:
                pygame.mixer.music.load('meow.wav')
                pygame.mixer.music.play()
                scared=True
            catrect_wander2 = cat_wander2.get_rect(center=(120,120))
            screen.blit(cat_wander2, catrect_wander2)
        else:
            if scared==True:
                scared=False
            catrect_wander1 = cat_wander1.get_rect(center=(120,120))
            screen.blit(cat_wander1, catrect_wander1)
        
        #my_words={'OWNER':(280,70),'WANDER':(280,120),'QUIT':(280,170)}
        
        for my_text, text_pos in my_buttons.items():
            text_surface=my_font.render(my_text, True, WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
            
        pygame.display.flip()
        if (not GPIO.input(23)):
            p.ChangeDutyCycle(0)
            q.ChangeDutyCycle(0)
            ha=False
            
    if fo:
        recognizer = cv2.createLBPHFaceRecognizer()
        recognizer.load('trainer/trainer.yml')
        cascadePath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);


        cam = cv2.VideoCapture(0)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

        font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
        while vision:
            print(ultrasonic3.distance)
            ret, frame =cam.read()
            im=cv2.flip(frame, -1)
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray,1.2,5)
            f=False
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                scrdis()
                if(conf<51):
                    if(Id==1):
                        Id="Zitao"
                
                    elif(Id==2):
                        Id="Jingyi"
                        f=True
                        xfacecenter = x+w/2
                        if xfacecenter>110 and xfacecenter<210:
                            if ultrasonic3.distance>0.15 or ultrasonic3.distance==0:
                                print("xfacecenter = " + str (xfacecenter))
                                p.ChangeFrequency(1000/21.51)
                                p.ChangeDutyCycle(151/21.51)
                                q.ChangeFrequency(1000/21.49)
                                q.ChangeDutyCycle(149/21.49)
                                find_rect3 = find3.get_rect(center=(120,120))
                                screen.blit(find3, find_rect3)
                                text=my_font.render("on my way!", True, WHITE)
                                screen.blit(text, (60,20))
                        #time.sleep(0.1)
                        #stop()
                            if ultrasonic3.distance<=0.15 and ultrasonic3.distance!=0:
                                p.ChangeDutyCycle(0)
                                q.ChangeDutyCycle(0)
                                find_rect4 = find4.get_rect(center=(120,120))
                                screen.blit(find4, find_rect4)
                                text=my_font.render("find you!", True, WHITE)
                                screen.blit(text, (60,20))
                                time.sleep(2)
                                vision=False
                                fo=False
                    
                    
                        if xfacecenter>210:
                            p.ChangeFrequency(1000/21.51)
                            p.ChangeDutyCycle(151/21.51)
                            q.ChangeDutyCycle(0)
                            find_rect3 = find3.get_rect(center=(120,120))
                            screen.blit(find3, find_rect3)
                            text=my_font.render("on my way!", True, WHITE)
                            screen.blit(text, (60,20))
                    #time.sleep(0.02)
                    #stop()
                        if xfacecenter<110:
                            p.ChangeDutyCycle(0)
                            q.ChangeFrequency(1000/21.49)
                            q.ChangeDutyCycle(149/21.49)
                            find_rect3 = find3.get_rect(center=(120,120))
                            screen.blit(find3, find_rect3)
                            text=my_font.render("on my way!", True, WHITE)
                            screen.blit(text, (60,20))
                    #time.sleep(0.02)
                    #stop()
                    
                else:
                    Id="unknown"
                    find_rect2 = find2.get_rect(center=(120,120))
                    screen.blit(find2, find_rect2)
                    text=my_font.render("I don't know you", True, WHITE)
                    screen.blit(text, (60,20))
                
                cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
            if(f==False):
                find()
            pygame.display.flip()
            #cv2.imshow('im',im)
        
            if (not GPIO.input(23)):
                vision=False
    
        cam.release()
        cv2.destroyAllWindows()
        p.ChangeDutyCycle(0)
        q.ChangeDutyCycle(0)
        fo=False
    if pb:
        while choose==True:
            scrdis()
            catrectphoto1 = catphoto1.get_rect(center=(60,60))
            screen.blit(catphoto1, catrectphoto1)
            catrectphoto2 = catphoto2.get_rect(center=(180,60))
            screen.blit(catphoto2, catrectphoto2)
            catrectphoto3 = catphoto3.get_rect(center=(60,180))
            screen.blit(catphoto3, catrectphoto3)
            catrectphoto4 = catphoto4.get_rect(center=(180,180))
            screen.blit(catphoto4, catrectphoto4)
            pygame.display.flip()
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos=pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos=pygame.mouse.get_pos()
                    x,y = pos
                    if y>40 and y<80:
                        if x>40 and x<80:
                            catphoto=catphoto1
                            choose=False
                        elif x>160 and x<200:
                            catphoto=catphoto2
                            choose=False
                    if y>160 and y<200:
                        if x>40 and x<80:
                            catphoto=catphoto3
                            choose=False
                        elif x>160 and x<200:
                            catphoto=catphoto4
                            choose=False
            
        if sh==False:
            display = pygame.display.set_mode(SIZE, 0)
            camera = pygame.camera.Camera(DEVICE, SIZE)
            camera.start()
            x=70
            y=80
            #screen = pygame.surface.Surface(SIZE, 0, display)
        #screen = pygame.surface.Surface(SIZE, 0, display)
            capture = True
        while capture:
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos=pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos=pygame.mouse.get_pos()
                    x,y = pos
            scrdis()
            screenn = camera.get_image()
            screenn=pygame.transform.rotate(screenn,180)
            screen.blit(screenn, (0,0))
            catrectphoto = catphoto.get_rect(center=(x,y))
            screen.blit(catphoto, catrectphoto)
            pygame.display.update()
            if(not GPIO.input(22)):
                pygame.mixer.music.load('ka.wav')
                pygame.mixer.music.play()
                pygame.image.save(screen, FILENAME)
                sh=True          
                camera.stop()
                scrdis()
                capture=False
                
            if(not GPIO.input(23))and sh ==False:
                camera.stop()
                capture=False
                choose=True
                pb=False
            
                            
        if sh == True:
            
            com = pygame.image.load("/home/pi/final/capture.png") 
            com = pygame.transform.scale(com,(240,180))
            comrect = com.get_rect(center=(120,120))
            screen.blit(com, comrect)
            pygame.display.flip()
            time.sleep(3)
            choose=True
            pb=False
            sh=False
        
    
GPIO.cleanup()
