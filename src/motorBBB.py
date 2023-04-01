import Adafruit_BBIO.PWM as PWM


class Motor:
    def __init__(self):
        self.servoPin = "P9_16"
        PWM.start(self.servoPin, 0, 50)
        PWM.set_duty_cycle("P9_16", 7.5)

    def changeRPM(self, num):
        if 10 > num > 5:
            dutyCycle = num
            PWM.set_duty_cycle(self.servoPin, dutyCycle)

