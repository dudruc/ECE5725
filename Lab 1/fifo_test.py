import subprocess

a = raw_input("input:")
if a =='pause':
    cmd = 'echo "pause" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell=True)
if a =='quit':
    cmd = 'echo "quit" > /home/pi/lab1/video_fifo'
    print subprocess.check_output(cmd, shell=True)
