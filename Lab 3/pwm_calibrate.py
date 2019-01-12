#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab3 2018-10-10
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

#f=46.51=1/(20+1.5)*1000
p = GPIO.PWM(6, 46.51)
#dc=1/21.5*100
p.start(6.977)
s = raw_input('Press return to stop:')
p.stop()

GPIO.cleanup()

