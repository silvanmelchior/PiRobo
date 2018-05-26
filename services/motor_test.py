import os
import time
import threading
import atexit
import socket
import shutil

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor


#
# Config
#
cfg = {
    'touch_speed': 250,
    'keyboard_speed': 100,
    'com_port': 56565
}


#
# Init
#
mh = Adafruit_MotorHAT(addr=0x60)
motor_l = mh.getMotor(3)
motor_r = mh.getMotor(1)


#
# Auto-Shutdown at the end
#
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


#
# Cmd handling
#
def cmd_handle(cmd):

    #
    # Manual Web Ctrl
    #
    if cmd[:11] == b'key update ':
        dir_f = cmd[11:12] == b'1'
        dir_l = cmd[13:14] == b'1'
        dir_b = cmd[15:16] == b'1'
        dir_r = cmd[17:18] == b'1'
        motor_l.setSpeed(cfg['keyboard_speed'])
        motor_r.setSpeed(cfg['keyboard_speed'])
        if dir_f and dir_l:
            motor_l.run(Adafruit_MotorHAT.RELEASE)
            motor_r.run(Adafruit_MotorHAT.FORWARD)
        elif dir_f and dir_r:
            motor_l.run(Adafruit_MotorHAT.FORWARD)
            motor_r.run(Adafruit_MotorHAT.RELEASE)
        elif dir_f:
            motor_l.run(Adafruit_MotorHAT.FORWARD)
            motor_r.run(Adafruit_MotorHAT.FORWARD)
        elif dir_l:
            motor_l.run(Adafruit_MotorHAT.BACKWARD)
            motor_r.run(Adafruit_MotorHAT.FORWARD)
        elif dir_r:
            motor_l.run(Adafruit_MotorHAT.FORWARD)
            motor_r.run(Adafruit_MotorHAT.BACKWARD)
        elif dir_b:
            motor_l.run(Adafruit_MotorHAT.BACKWARD)
            motor_r.run(Adafruit_MotorHAT.BACKWARD)
        else:
            motor_l.run(Adafruit_MotorHAT.RELEASE)
            motor_r.run(Adafruit_MotorHAT.RELEASE)

    elif cmd[:11] == b'touch move ':
        x,y = cmd[11:].decode('utf-8').split(' ')
        x = float(x)
        y = float(y)
        if y <= 50:
            motor_l.run(Adafruit_MotorHAT.FORWARD)
            motor_r.run(Adafruit_MotorHAT.FORWARD)
            speed = (50-y)/50*cfg['touch_speed']
            sign = 1
        else:
            motor_l.run(Adafruit_MotorHAT.BACKWARD)
            motor_r.run(Adafruit_MotorHAT.BACKWARD)
            speed = (y-50)/50*cfg['touch_speed']
            sign = -1
        l = min(1,1 - (50-x)/50)
        r = min(1,1 - (x-50)/50)
        l = int(speed*l)
        r = int(speed*r)
        motor_l.setSpeed(l)
        motor_r.setSpeed(r)
        l_save = float(l)/cfg['touch_speed'] * sign
        r_save = float(r)/cfg['touch_speed'] * sign
        
    elif cmd[:9] == b'touch end':
        motor_l.run(Adafruit_MotorHAT.RELEASE);
        motor_r.run(Adafruit_MotorHAT.RELEASE);

    elif cmd[:11] == b'touch start':
        pass

    #
    # Direct Ctrl
    #
    elif cmd[:6] == b'speed ':
        l,r = cmd[6:].decode('utf-8').split(' ')
        l = int(float(l)*255)
        r = int(float(r)*255)
        if l >= 255:
            l = 255
        elif l <= -255:
            l = -255
        if r >= 255:
            r = 255
        elif r <= -255:
            r = -255
        if l >= 0:
            motor_l.run(Adafruit_MotorHAT.FORWARD)
            motor_l.setSpeed(l)
        else:
            motor_l.run(Adafruit_MotorHAT.BACKWARD)
            motor_l.setSpeed(-l)
        if r >= 0:
            motor_r.run(Adafruit_MotorHAT.FORWARD)
            motor_r.setSpeed(r)
        else:
            motor_r.run(Adafruit_MotorHAT.BACKWARD)
            motor_r.setSpeed(-r)

    elif cmd[:3] == b'end':
        motor_l.run(Adafruit_MotorHAT.RELEASE);
        motor_r.run(Adafruit_MotorHAT.RELEASE);
        
    else:
        print('unknown cmd: ' + cmd.decode('utf-8'))
        
            
#
# Main-Loop
#
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', cfg['com_port']))
    s.listen(1)
    conn, addr = s.accept()
    while True:
        data = conn.recv(1024)
        if not data: break
        cmd_handle(data)
    conn.close()

