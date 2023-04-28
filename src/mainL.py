import pygame
import socket
import racer


def main():
    RMName = "G17"
    RaceManagement = racer.RaceConnection(RMName)  # Establish connection to Race Management
    RaceManagement.start()  # Will prompt for name, number, and send an integer indicating what stream to record to.
    print("\nThis is now the value of racer.sendFeed: " + racer.sendFeed)
    print("Feel free to send this variable to tell the BBB which port to stream to!\n")

    CompName = "G17"
    port = 7007
    FromBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    FromBB.bind((socket.gethostbyname(CompName), port))
    while True:
        data = FromBB.recv(1024)  # buffer size is 1024 bytes
        decoded = data.decode()
        if decoded.startswith("!"):
            BB_IP = decoded[1:]  # Now BB_IP has been loaded with BeagleBone's IP.
            print(f"Got BB IP: {BB_IP}")
            bytes_udp = racer.sendFeed.encode()
            FromBB.sendto(bytes_udp, (BB_IP, port))  # Send UDP video link to BeagleBone.
            break
    FromBB.close()  # We do not want to receive any more information from the BeagleBone.

    ToBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket for sending to the BB. No more receiving.
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
                    printRightTrig = "{:03d}".format(right_trig_norm)

                    # SEND DATA TO RM
                    if left_trig_norm == 0:
                        RaceManagement.send_throttle(right_trig_norm)  # Send throttle data to RM if no reversing
                    else:
                        RaceManagement.send_throttle(left_trig_norm * -1)  # Send reverse data to RM if no throttle

                    s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}"
                    bytes_s = s.encode()
                    ToBB.sendto(bytes_s, (BB_IP, port))


if __name__ == "__main__":
    main()
