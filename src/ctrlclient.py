import socket
serverIP = str(input("Enter IP address: "))
print("Using this IP: " + serverIP + "\n")
port = 7007
buff = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, port))
while True:
    message = sock.recv(buff)
    if message:
        print(f"Message from Server: {message.decode()}")
    else:
        print("Connection terminated")
        break

