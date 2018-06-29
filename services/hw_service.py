import time
import socket
import threading
import atexit
import RPi.GPIO as GPIO
import time
from AlphaBot import AlphaBot


#
# Config
#
base_port = 56000

#
# Init HW
#
Ab = AlphaBot()
DR = 16
DL = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

Ab.stop()

#
# Create sockets
#
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', base_port+10))
s.listen(5)

def exit_handler():
    global s
    s.close()

atexit.register(exit_handler)

#
# Main loop
#
while True:
    conn, addr = s.accept()
    msg = conn.recv(1024)
    
    if msg == b'motor forward':
        Ab.forward()
    elif msg == b'motor left':
        Ab.left()
    elif msg == b'motor right':
        Ab.right()
    elif msg == b'motor stop':
        Ab.stop()

    conn.close()

