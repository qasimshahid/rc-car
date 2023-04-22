import socket
import servoBBB
import motorBBB
import racer


def main():
    rmconnect = racer.RaceConnection("G17")
    rmconnect.start()

    serverName = "G17"
    serverIP = socket.gethostbyname(serverName)
    print("Using this IP: " + serverIP + "\n")
    port = 7007
    buff = 64
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serverIP, port))
    servoControl = servoBBB.SteeringServo()
    motorControl = motorBBB.Motor()
    while True:
        message = sock.recv(buff)
        if len(message) != 19:
            continue
        if message:
            decode = message.decode()
            ls = int(decode[3:7])
            lt = int(decode[10:13])
            rt = int(decode[16:20])
            rt = 7.5 - (rt * 0.025)  # 7.5 to 5 for accelerate
            lt = 7.5 + (lt * 0.010)  # 7.5 to 8.5 for reverse
            servoControl.turnDegrees(ls)
            if lt != 7.5 and rt == 7.5:  # Reversing only allowed if right trigger is off and left trigger is not off.
                motorControl.changeRPM(lt)
                print(ls, lt)
            else:
                motorControl.changeRPM(rt)  # Else accelerate the car
                print(ls, lt, rt)
        else:
            print("Connection terminated")
            break
    rmconnect.stop()


if __name__ == "__main__":
    main()
