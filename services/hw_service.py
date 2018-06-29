import time
import socket
import threading
import atexit
import RPi.GPIO as GPIO
import time
from drivers import Motor


#
# Config
#
base_port = 56000

#
# Init HW
#
# General
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Motors
motor = Motor()


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
    
    if msg[:6] == b'motor ':
        l, r = msg[6:].decode('ascii').split(' ')
        motor.setMotor(float(l), float(r))

    conn.close()

