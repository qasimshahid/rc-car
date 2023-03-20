import socket


def get_ip():  # courtesy of stack overflow, finds the primary ip address not the
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


PORT = 7007
beagleIP = get_ip()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((beagleIP, PORT))
sock.listen()

while True:
    clientSocket, address = sock.accept()
    print(f"Connection established from address {address}")
    clientSocket.send(bytes("Welcome!", "utf-8"))
    clientSocket.close()
