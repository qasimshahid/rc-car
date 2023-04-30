import socket
import servoBBB
import motorBBB


def main():
    BB_IP = get_ip()  # Beaglebone IP.
    print("This is the BeagleBone's IP: " + BB_IP + "\n")
    port = 7007
    buff = 19

    controlName = "G17"
    controlIP = socket.gethostbyname(controlName)
    print("This is control's IP: " + controlIP)
    MESSAGE = f"!{BB_IP}".encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((BB_IP, port))  # Receive the UDP link from server.
    sock.sendto(MESSAGE, (controlIP, port))  # Send BB IP to server.

    udp_link = ""
    while True:
        message = sock.recv(64)
        decoded = message.decode()
        if decoded.startswith("u"):
            udp_link = decoded
            sock.sendto(b"Received", (controlIP, port))
            break
        elif decoded == "None":
            sock.sendto(b"Received", (controlIP, port))
            udp_link = "Nowhere, no video supplied."
            break
    print("This is where I will stream to: " + udp_link)

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


if __name__ == "__main__":
    main()
