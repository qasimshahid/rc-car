import socket
import servoBBB
import motorBBB


def get_ip():  # courtesy of stack overflow,
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def main():
    BB_IP = get_ip()  # Beaglebone IP.
    print("This is the BeagleBone's IP: " + BB_IP + "\n")
    port = 7007
    buff = 19

    serverName = "G17"
    serverIP = socket.gethostbyname(serverName)
    MESSAGE = f"!{BB_IP}".encode()  # Send the BBB IP to the server.
    sockToServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockToServer.sendto(MESSAGE, (serverIP, port))
    while True:
        message, adr = sockToServer.recv(50)
        message.decode()
        if message.startswith("u"):
            udp_link = message
            break
    sockToServer.close()  # We now have the UDP link to stream to and need no more information from the laptop.
    print(udp_link)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
    sock.bind((BB_IP, port))  # Bind to the server IP and port
    servoControl = servoBBB.SteeringServo()  # Steering control
    motorControl = motorBBB.Motor()  # Motor control
    while True:
        message = sock.recv(buff)
        if len(message) == 19:
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


if __name__ == "__main__":
    main()
