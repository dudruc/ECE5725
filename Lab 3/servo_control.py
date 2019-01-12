#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab3 2018-10-10
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

#when duty cycle is 1.5ms
i=150
x =float(i)
pw = x/100
f = 1000/(20+pw)
dc = x/(2000+x)*100
p = GPIO.PWM(6, f)
p.start(dc)
print "now the frequency is "+str(f)+", the pulse width is "+str(pw)+", the duty cycle is "+str(dc)
time.sleep(3)
try:
    #because the number in range can only be integer,duty cycle is i/100 ms
    #rotate clockwise, faster
    for i in range(148, 128, -2):
    
        x =float(i)
        pw = x/100
        f = 1000/(20+pw)
        dc = x/(2000+x)*100
        #change the frequency and duty cycle
        p.ChangeFrequency(f)
        p.ChangeDutyCycle(dc)
        print "now the frequency is "+str(f)+", the pulse width is "+str(pw)+", the duty cycle is "+str(dc)
        time.sleep(3)
    #rotate conter-clockwise, faster
    for j in range(150, 172, 2):
    
        x =float(j)
        pw = x/100
        f = 1000/(20+pw)
        dc = x/(2000+x)*100
        p.ChangeFrequency(f)
        p.ChangeDutyCycle(dc)
        print "now the frequency is "+str(f)+", the pulse width is "+str(pw)+", the duty cycle is "+str(dc)
        time.sleep(3)

except KeyboardInterrupt:
    pass

p.stop()
GPIO.cleanup()

