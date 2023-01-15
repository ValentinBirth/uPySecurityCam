from time import sleep
from machine import Pin, PWM

class Servo(object):
    def __init__(self, pin: int=15, hz: int=50):
        self._servo = PWM(Pin(pin),hz) 
        
    def writeAngle(self, pos):
        if pos <= 0:
            pos = 0
        if pos >= 180:
            pos = 180
        pos_buffer=(pos/180)*(128-26)
        self._servo.duty(int(pos_buffer)+26)
        
    def deinit(self):
        self._servo.deinit()

class ServoArm():
    def __init__(self) -> None:
        self.horizontal_servo = Servo(pin=32)
        self.vertical_servo = Servo(pin=33)

    def setVerticalServo(self, degrees):
        self.vertical_servo.writeAngle(degrees)

    def setHorizontalServo(self, degrees):
        self.horizontal_servo.writeAngle(degrees)

    def testHorizontal(self):
        for degree in range(0,179,1):
            self.set_horizontal_servo(degree)
            print("increasing -- "+str(degree))
        sleep(2)
        for degree in range(179,0,-1):
            self.set_horizontal_servo(degree)
            print("decreasing -- "+str(degree))