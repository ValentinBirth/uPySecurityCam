from time import sleep
from machine import Pin, PWM

class ServoArm():
    def __init__(self) -> None:
        self.max_duty=9000
        self.min_duty=1000
        self.horizontal_servo_pin = PWM(Pin(13))
        self.vertical_servo_pin = PWM(Pin(12))
        self.horizontal_servo_pin.freq(50)
        self.vertical_servo_pin.freq(50)

    def set_vertical_servo(self, degrees):
        if degrees > 180:
            degrees=180
        if degrees < 0:
            degrees=0
        new_duty=self.min_duty+(self.max_duty-self.min_duty)*(degrees/180)
        self.vertical_servo_pin.duty_u16(int(new_duty))

    def set_horizontal_servo(self, degrees):
        if degrees > 180:
            degrees=180
        if degrees < 0:
            degrees=0
        new_duty=self.min_duty+(self.max_duty-self.min_duty)*(degrees/180)
        self.horizontal_servo_pin.duty_u16(int(new_duty))

    def test_horizontal_servo(self):
        for degree in range(0,180,1):
            self.set_horizontal_servo(degree)
            sleep(0.2)
            print("increasing -- "+str(degree))