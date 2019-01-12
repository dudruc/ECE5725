#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab4 2018-10-24

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)

#input frequency
f1 = raw_input("please input frequency:")
f=float(f1)
p = GPIO.PWM(13, f)
#50% duty cycle
p.start(50)
#stop after pressing any buttons
b=raw_input('Press return to stop:')
p.stop()

GPIO.cleanup()

