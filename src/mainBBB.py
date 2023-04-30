import socket
import servoBBB
import motorBBB
import subprocess


previous = (105, 7.5, 7.5)  # Values of the previous controller input
ffmpegCmd = ["ffmpeg", "-c:v", "mjpeg", "-s", "640x360", "-i", "/dev/video0",
             "-nostdin", "-loglevel", "panic", "-c:v", "copy", "-tune", "zerolatency",
             "-muxdelay", "0.1", "-g", "0", "-f", "mjpeg", "INDEX 20: LINK GOES HERE"]


def main():
    global previous
    global ffmpegCmd
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
    while True:  # Program will block here until we send a link to stream to. Use reconnect in mainL, press start.
        message = sock.recv(32)
        decoded = message.decode()
        if decoded.startswith("L"):  # This happens when we send controller data when reconnecting, just ignore it.
            continue
        if decoded.startswith("u"):  # This means we received a UDP link to stream to.
            udp_link = decoded
            sock.sendto(b"Received", (controlIP, port))  # Confirm to ControlTower that we received a video link.
            break
        elif decoded.startswith("N"):
            sock.sendto(b"Received", (controlIP, port))
            udp_link = "No video link supplied. Will not be streaming."
            break

    print("This is where I will stream to: " + udp_link)
    if not udp_link.startswith("N"):  # This means that we have an actual UDP link to stream to. Run ffmpeg command.
        ffmpegCmd[20] = udp_link  # Put UDP link into ffmpegCmd list.
        p = subprocess.Popen(ffmpegCmd)  # Run ffmpeg as a background task, no logs. Will not block.
        print(f"Ffmpeg command ran, streaming to {ffmpegCmd[20]}")

    servoControl = servoBBB.SteeringServo()  # Steering control
    motorControl = motorBBB.Motor()  # Motor control
    while True:
        try:
            message = sock.recv(buff)
            decode = message.decode()
        except (KeyboardInterrupt, Exception):  # If we want to exit the program, or any other exception.
            print("Ctrl-C signal received, stopping the car...")
            motorControl.changeRPM(7.5)  # Stop the car on exception.
            exit(-1)
        try:
            ls = int(decode[3:7])
        except Exception:  # If our message doesn't match the format, this will throw an Exception.
            continue
        lt = int(decode[10:13])
        rt = int(decode[16:20])
        rt = 7.5 - (rt * 0.025)  # 7.5 to 5 for accelerate
        lt = 7.5 + (lt * 0.010)  # 7.5 to 8.5 for reverse
        if previous == (ls, lt, rt):
            continue  # If values haven't changed, continue.
        servoControl.turnDegrees(ls)
        if lt != 7.5 and rt == 7.5:  # Reversing only allowed if right trigger is off and left trigger is not off.
            motorControl.changeRPM(lt)
            print(ls, lt)
        else:
            motorControl.changeRPM(rt)  # Else accelerate the car
            print(ls, lt, rt)
        previous = (ls, lt, rt)  # Set current values as previous in preparation for next iteration.


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
