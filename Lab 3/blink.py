#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab3 2018-10-10
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

t = raw_input("please input time:")
#calculate the frequency
f = 1/float(t)
p = GPIO.PWM(6, f)
#50% duty cycle
p.start(50)
#stop after pressing any buttons
b=raw_input('Press return to stop:')
p.stop()

GPIO.cleanup()

