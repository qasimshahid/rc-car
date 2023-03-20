import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


buff = 1024
port = 7007
hostIP = get_ip()
print("Host IP: " + hostIP)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((hostIP, port))
sock.listen(1)

clientSocket, clientAddress = sock.accept()
print(f"Connection established from address {clientAddress}")
clientSocket.send(bytes("Hello!", "utf-8"))


sock.close()
