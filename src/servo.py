import Adafruit_BBIO.PWM as PWM

servoPin = "P9_14"
PWM.start(servoPin, 2, 50)
while (1):
    desiredAngle = float(input("What Angle do You Want"))
    dutyCycle = 1. / 18. * desiredAngle + 2
    PWM.set_duty_cycle(servoPin, dutyCycle)

