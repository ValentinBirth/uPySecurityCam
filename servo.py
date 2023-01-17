from time import sleep
from machine import Pin, PWM

class Servo(object):
    def __init__(self, pin: int=15, hz: int=50, maxPos: int=180):
        self.position = 0
        self._servo = PWM(Pin(pin),hz)
        self.maxPose = maxPos
        self.writeAngle(0) 
        
    def writeAngle(self, pos):
        if pos <= 0:
            pos = 0
        if pos >= self.maxPose:
            pos = self.maxPose
        self.position = pos
        pos_buffer=(pos/180)*(128-26)
        self._servo.duty(int(pos_buffer)+26)
        
    def deinit(self):
        self._servo.deinit()

class ServoArm():
    def __init__(self) -> None:
        self.horizontal_servo = Servo(pin=33)
        self.vertical_servo = Servo(pin=32, maxPos=90)

    def getServoPosition(self):
        return (self.horizontal_servo.position,self.vertical_servo.position)

    def setVerticalServo(self, degrees):
        self.vertical_servo.writeAngle(degrees)

    def setHorizontalServo(self, degrees):
        self.horizontal_servo.writeAngle(degrees)

    def addHorizontalServo(self):
        self.horizontal_servo.writeAngle(self.horizontal_servo.position+10)

    def addVerticalServo(self):
        self.vertical_servo.writeAngle(self.vertical_servo.position+10)

    def subtractHorizontalServo(self):
        self.horizontal_servo.writeAngle(self.horizontal_servo.position-5)

    def subtractVerticalServo(self):
        self.vertical_servo.writeAngle(self.vertical_servo.position-5)

    def testHorizontal(self):
        for degree in range(0,179,1):
            self.setHorizontalServo(degree)
            print("increasing -- "+str(degree))
        sleep(2)
        for degree in range(179,0,-1):
            self.setHorizontalServo(degree)
            print("decreasing -- "+str(degree))

    def testVertical(self):
        for degree in range(0,89,1):
            self.setVerticalServo(degree)
            print("increasing -- "+str(degree))
        sleep(2)
        for degree in range(89,0,-1):
            self.setVerticalServo(degree)
            print("decreasing -- "+str(degree))

    def testArm(self):
        self.testHorizontal()
        self.testVertical()