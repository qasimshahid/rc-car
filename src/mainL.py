import pygame
import socket
import racer

mode = 2  # Put 2 here if in Race mode. 1 if just testing (No connection to RM)
controlTower = "G17"  # Put name of computer which has the controller connected to it.
port = 7007
BB_IP = ""
video_feed_test = "None"  # Change as needed. Send "None" if no video testing needed.


def main():
    if mode == 2:  # Race Mode
        Race()
    elif mode == 1:  # Testing Mode
        Test()


def Race():
    global BB_IP
    print("Race Mode\n")
    RMName = "G17"
    RaceManagement = racer.RaceConnection(RMName)  # Establish connection to Race Management
    RaceManagement.start()  # Will prompt for name, number, and send an integer indicating what stream to record to.

    connect(RaceManagement, 0)  # Send to RM, 0 implies we are connecting for the first time.

    toBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control(RaceManagement, toBB)  # Throttle IS being sent to RM.


def Test():
    global BB_IP
    global video_feed_test
    print("Test Mode\n")

    connect(None, 0)  # Do not send to RM, 0 implies we are connecting for the first time.

    toBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket for sending to the BB. No more receiving.
    control(None, toBB)  # Throttle IS NOT being sent to RM.


def connect(RaceManagement, rec):
    global BB_IP
    fromBB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    fromBB.bind((socket.gethostbyname(controlTower), port))

    #  Rec stands for reconnect. If we lose connection, we can use a simple press instead of restarting the program.
    if rec == 1:  # On press of the "START" button, send a string for the video link when reconnecting.
        if RaceManagement is not None:
            bytes_udp = RaceManagement.sendFeed.encode()
        else:
            bytes_udp = video_feed_test.encode()
        fromBB.sendto(bytes_udp, (BB_IP, port))  # Send UDP video link to BeagleBone.

    else:
        while True:
            data = fromBB.recv(64)
            decoded = data.decode()
            if decoded.startswith("!"):
                BB_IP = decoded[1:]  # Now BB_IP has been loaded with BeagleBone's IP.
                print(f"Got BB IP: {BB_IP}")
                if RaceManagement is not None:
                    bytes_udp = RaceManagement.sendFeed.encode()
                else:
                    bytes_udp = video_feed_test.encode()
                fromBB.sendto(bytes_udp, (BB_IP, port))  # Send UDP video link to BeagleBone.
            elif decoded.startswith("R"):
                break  # UDP Address received by the BBB.


def control(RM, toBB):
    pygame.init()
    joystick = pygame.joystick.Joystick(0)  # Plugged into the laptop via USB
    joystick.init()

    previous_input = (0, 0, 0)  # Used to store the previous input
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

                    if (left_stick_norm, left_trig_norm, right_trig_norm) != previous_input:
                        #  We only want to send controller data when inputs change, otherwise it's a waste.
                        s = f"LS:{printLeftStick}LT:{printLeftTrig}RT:{printRightTrig}"  # Length 19
                        bytes_s = s.encode()
                        toBB.sendto(bytes_s, (BB_IP, port))
                        previous_input = (left_stick_norm, left_trig_norm, right_trig_norm)  # Make previous input.

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7:
                    print("Reconnect button pressed...")
                    if RM is not None:
                        connect(RM, 1)
                    else:
                        connect(None, 1)


if __name__ == "__main__":
    main()
