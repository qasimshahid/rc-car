import socket
import time


def get_ip(): # courtesy of stack overflow,
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


class ControllerServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buff = 64
        self.port = 7007
        self.delay = 0.008  # 125 Hz polling rate, original Xbox One controller, 8 milliseconds
        self.client = None
        self.host_ip = get_ip()
        print("Host IP: " + self.host_ip)

    def establish_connection(self):
        self.sock.bind((self.host_ip, self.port))
        self.sock.listen(1)
        client_socket, client_address = self.sock.accept()
        self.client = client_socket
        print(f"Connection established from address {client_address}")

    def close_connection(self):
        self.sock.close()

    def send_msg(self, string):
        self.client.send(bytes(string, "utf-8"))
        time.sleep(self.delay)


