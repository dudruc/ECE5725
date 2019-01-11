#Jingyi Wang(jw2527) Zitao Zheng(zz632) Lab 1 2018-09-12
import subprocess
#use subprocess to excuete 'echo'

a = raw_input("input:")
if a =='pause':
    cmd = 'echo "pause" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell=True)
# this line is for sending out the command

if a =='quit':
    cmd = 'echo "quit" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell=True)
