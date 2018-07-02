import RPi.GPIO as GPIO
import time
import threading

class Motors:

    def __init__(self,in1=12,in2=13,ena=6,in3=20,in4=21,enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        GPIO.setup(self.IN3,GPIO.OUT)
        GPIO.setup(self.IN4,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(0)
        self.PWMB.start(0)
        self.setMotors(0,0)

    def setMotors(self, left, right):
        if((right >= 0) and (right <= 100)):
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(right)
        elif((right < 0) and (right >= -100)):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.PWMA.ChangeDutyCycle(0 - right)
        if((left >= 0) and (left <= 100)):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif((left < 0) and (left >= -100)):
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)



class Servos:

    def __init__(self,in1=22,in2=27):
        self.IN1 = in1
        self.IN2 = in2

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        self.PWMA = GPIO.PWM(self.IN1,50)
        self.PWMB = GPIO.PWM(self.IN2,50)
        self.PWMA.start(7.5)
        self.PWMB.start(7.5)

        def program_worker():
            while True:
                if self.modified == 1:
                    self.modified = 2
                elif self.modified == 2:
                    self.releaseServos()
                    self.modified = 0
                time.sleep(0.2)

        self.modified = 1
        t = threading.Thread(target=program_worker)
        t.start()

    def setServos(self, pan, tilt):
        self.modified = 1
        self.PWMA.ChangeDutyCycle(3 + float(pan)/100*9)
        self.PWMB.ChangeDutyCycle(3 + float(tilt)/100*9)
    
    def releaseServos(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        

