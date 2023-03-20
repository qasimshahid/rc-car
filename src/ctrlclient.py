import socket

print("First, please specify the IP address of the server. Form : 192.168.x.x")  #192.168.1.250
IP = input()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.250", 7007))

message = sock.recv(2048)

print("Message received:", message)
