import time
import socket
import threading
import atexit
import RPi.GPIO as GPIO
import time
import drivers


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
# Instances
motors = drivers.Motors()
servos = drivers.Servos()
pan_bak = 0.5
tilt_bak = 0.5


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
        motors.setMotors(float(l)*100, float(r)*100)

    elif msg[:6] == b'servo ':
        pan, tilt = msg[6:].decode('ascii').split(' ')
        pan, tilt = float(pan), float(tilt)
        if abs(pan-pan_bak) > 0.03 or abs(tilt-tilt_bak) > 0.03:
            servos.setServos(pan*100, tilt*100)
            pan_bak, tilt_bak = pan, tilt

    conn.close()

