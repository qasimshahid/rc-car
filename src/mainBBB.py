import socket
import servoBBB
import motorBBB


def main():
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
            rt = 7.5 - (rt * 0.025)  # 5 to 10
            servoControl.turnDegrees(ls)
            motorControl.changeRPM(rt)
            print(ls, lt, rt)
        else:
            print("Connection terminated")
            break


if __name__ == "__main__":
    main()
