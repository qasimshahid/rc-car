import Adafruit_BBIO.PWM as PWM


#__init__ method that takes the pin number as an argument and starts the
# PWM signal with the given frequency and duty cycle.


#set_angle method takes an angle as an argument and calculates the
# corresponding duty cycle before setting it with
# the PWM.set_duty_cycle function.


#In the main block, an instance of the ServoController class is created
# with the pin number "P9_14". The while loop prompts the
# user for an angle input and calls the set_angle
# method on the servo instance with the desired angle.

class ServoController:
    def __init__(self, pin):
        self.pin = pin
        PWM.start(pin, 2, 50)

    def set_angle(self, angle):
        dutyCycle = 1.0/18.0 * angle + 2
        PWM.set_duty_cycle(self.pin, dutyCycle)

if __name__ == '__main__':
    servo = ServoController("P9_14")
    while True:
        desiredAngle = int(input("What Angle do You Want? "))
        servo.set_angle(desiredAngle)
