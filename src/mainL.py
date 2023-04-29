import pygame
import socket
import racer


mode = 2  # Put 2 here if in Race mode. 1 if just testing (No connection to RM)
controlTower = "G17"  # Put name of computer which has controlled connected.
port = 7007
BB_IP = ""


def main():
    if mode == 2:
        Race()
    elif mode == 1:
        Test()


def Race():
    global BB_IP
    print("Race Mode\n")
    RMName = "G17"
    RaceManagement = racer.RaceConnection(RMName)  # Establish connection to Race Management
    RaceManagement.start()  # Will prompt for name, number, and send an integer indicating what stream to record to.

    fromBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    fromBB.bind((socket.gethostbyname(controlTower), port))

    while True:
        data = fromBB.recv(1024)  # buffer size is 1024 bytes
        decoded = data.decode()
        if decoded.startswith("!"):
            BB_IP = decoded[1:]  # Now BB_IP has been loaded with BeagleBone's IP.
            print(f"Got BB IP: {BB_IP}")
            bytes_udp = RaceManagement.sendFeed.encode()
            fromBB.sendto(bytes_udp, (BB_IP, port))  # Send UDP video link to BeagleBone.
        elif decoded.startswith("R"):
            break  # UDP Address received by the BBB.
    fromBB.close()  # We do not want to receive any more information from the BeagleBone.

    toBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket for sending to the BB. No more receiving.
    control(RaceManagement, toBB)


def Test():
    global BB_IP
    print("Test Mode\n")
    video_feed = "None"  # Change as needed. Send "None" if no video testing needed.

    fromBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    fromBB.bind((socket.gethostbyname(controlTower), port))

    while True:
        data = fromBB.recv(64)
        decoded = data.decode()
        if decoded.startswith("!"):
            BB_IP = decoded[1:]  # Now BB_IP has been loaded with BeagleBone's IP.
            print(f"Got BB IP: {BB_IP}")
            bytes_video = video_feed.encode()
            fromBB.sendto(bytes_video, (BB_IP, port))
        elif decoded.startswith("R"):
            break
    fromBB.close()  # We do not want to receive any more information from the BeagleBone.

    toBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket for sending to the BB. No more receiving.
    control(None, toBB)


def control(RM, toBB):
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
                    if RM is not None:
                        if left_trig_norm == 0:
                            RM.send_throttle(right_trig_norm)  # Send throttle data to RM if no reversing
                        else:
                            RM.send_throttle(left_trig_norm * -1)  # Send reverse data to RM if no throttle

                    s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}" # Length 19
                    bytes_s = s.encode()
                    toBB.sendto(bytes_s, (BB_IP, port))


if __name__ == "__main__":
    main()
