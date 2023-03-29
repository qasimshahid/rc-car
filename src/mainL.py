import pygame
import ctrlserverclassL


def main():
    controlServer = ctrlserverclassL.ControllerServer()
    controlServer.establish_connection()  # wait for connection to establish

    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0 or event.axis == 4 or event.axis == 5:
                    left_stick_norm = round(joystick.get_axis(0) * 100)
                    printLeftStick = "{:03d}".format(left_stick_norm)
                    if 15 > left_stick_norm > -15:
                        left_stick_norm = 0  # dead zone
                    printLeftStick = "{:04d}".format(left_stick_norm)
                    left_trig_norm = round((joystick.get_axis(4) + 1) * 50)
                    printLeftTrig = "{:03d}".format(left_trig_norm)
                    right_trig_norm = round((joystick.get_axis(5) + 1) * 50)
                    printRightTrig = "{:03d}".format(right_trig_norm)
                    s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}"
                    controlServer.send_msg(s)


if __name__ == "__main__":
    main()
