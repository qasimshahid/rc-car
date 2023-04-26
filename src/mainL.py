import pygame
import ctrlserver
import racer


def main():
    RMName = "G17"
    RaceManagement = racer.RaceConnection(RMName)  # Establish connection to Race Management
    RaceManagement.start()  # Will prompt for name, number, and send an integer indicating what stream to record to.

    controlServer = ctrlserver.ControllerServer()
    controlServer.establish_connection()  # Wait for connection to establish
    pygame.init()
    joystick = pygame.joystick.Joystick(0)  # Plugged into the laptop via USB
    joystick.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0 or event.axis == 4 or event.axis == 5:
                    left_stick_norm = round(((1 - joystick.get_axis(0)) / 2) * 70 + 70)  # DO NOT CHANGE!
                    printLeftStick = "{:04d}".format(left_stick_norm)
                    left_trig_norm = round((joystick.get_axis(4) + 1) * 50)  # Map to 0-100
                    printLeftTrig = "{:03d}".format(left_trig_norm)
                    right_trig_norm = round((joystick.get_axis(5) + 1) * 50)  # Map to 0-100
                    if left_trig_norm == 0:
                        RaceManagement.send_throttle(right_trig_norm)  # Send throttle data to RM if no reversing
                    else:
                        RaceManagement.send_throttle(left_trig_norm * -1) # Send reverse data to RM if no throttle
                    printRightTrig = "{:03d}".format(right_trig_norm)
                    s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}"
                    controlServer.send_msg(s)  # Send controller input to the BBB.


if __name__ == "__main__":
    main()
# 192.168.8.186 - use to connect to BBB while BBB is not plugged in to the USB port of the laptop.
