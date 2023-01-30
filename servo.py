from time import sleep
from machine import Pin, PWM


class Servo(object):
    """Object that implements the driver for the servo"""
    def __init__(self, pin: int = 15, hz: int = 50, maxPos: int = 180):
        self.position = 0
        self._servo = PWM(Pin(pin), hz)
        self.max_pose = maxPos

    def write_angle(self, pos):
        """Moves servo to the desired angle"""
        if pos <= 0:
            pos = 0
        if pos >= self.max_pose:
            pos = self.max_pose
        self.position = pos
        pos_buffer = (pos/180)*(128-26)
        self._servo.duty(int(pos_buffer)+26)

    def deinit(self):
        """Deinitialises the servo"""
        self._servo.deinit()


class ServoArm():
    """Object that implements the driver for the servo arm"""
    def __init__(self) -> None:
        self.horizontal_servo = Servo(pin=33)
        self.vertical_servo = Servo(pin=32, maxPos=90)
        self.set_horizontal_servo(0)
        self.set_vertical_servo(0)

    def get_servo_position(self):
        """Returns current position of the servos"""
        return (self.horizontal_servo.position, self.vertical_servo.position)

    def set_vertical_servo(self, degrees):
        """Sets the vertical Servo to desired angle"""
        self.vertical_servo.write_angle(degrees)

    def set_horizontal_servo(self, degrees):
        """Sets the horizontal Servo to desired angle"""
        self.horizontal_servo.write_angle(degrees)

    def add_horizontal_servo(self):
        """Moves horizontal servo by adding 10 degree to the current position"""
        self.horizontal_servo.write_angle(self.horizontal_servo.position+10)

    def add_vertical_servo(self):
        """Moves vertical servo by adding 10 degree to the current position"""
        self.vertical_servo.write_angle(self.vertical_servo.position+10)

    def subtract_horizontal_servo(self):
        """Moves horizontal servo by subtracting 10 degree to the current position"""
        self.horizontal_servo.write_angle(self.horizontal_servo.position-10)

    def subtract_vertical_servo(self):
        """Moves vertical servo by adding 10 degree to the current position"""
        self.vertical_servo.write_angle(self.vertical_servo.position-10)
