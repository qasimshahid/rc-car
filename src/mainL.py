import pygame
import ctrlserverclassL
import racer

def main():
    rmconnect = racer.RaceConnection("DANS-AIR")
    rmconnect.start()
    #controlServer = ctrlserverclassL.ControllerServer()
    #controlServer.establish_connection()  # Wait for connection to establish
    pygame.init()
    joystick = pygame.joystick.Joystick(0)  # Plugged into the laptop via USB
    joystick.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0 or event.axis == 4 or event.axis == 5:
                    left_stick_norm = round(((1 - joystick.get_axis(0)) / 2) * 70 + 70)  # DO NOT CHANGE!
                    printLeftStick = "{:04d}".format(left_stick_norm)
                    left_trig_norm = round((joystick.get_axis(4) + 1) * 50)  # map to 0-100
                    printLeftTrig = "{:03d}".format(left_trig_norm)
                    right_trig_norm = round((joystick.get_axis(5) + 1) * 50)  # map to 0-100
                    if left_trig_norm == 0:
                        rmconnect.send_throttle(right_trig_norm)
                    else:
                        rmconnect.send_throttle(left_trig_norm * -1)
                    printRightTrig = "{:03d}".format(right_trig_norm)
                    s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}"
                    #controlServer.send_msg(s)  # Send controller input to the BBB.


if __name__ == "__main__":
    main()
# 192.168.8.186 - use to connect
