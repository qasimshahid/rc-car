import Adafruit_BBIO.PWM as PWM


class SteeringServo:
    def __init__(self):
        self.servoPin = "P9_14"  # Steering pins, P9_7, P9_1, P_14
        PWM.start(self.servoPin, 2, 50)

    def turnDegrees(self, desiredAngle):
        dutyCycle = 1. / 18. * desiredAngle + 2
        PWM.set_duty_cycle(self.servoPin, dutyCycle)
