import socket

print("First, please specify the IP address of the server. Form : 192.168.x.x."
      "\nIf you do not know the IP address, please run \"ifconfig / ipconfig\"."
      "\nYou should scroll all the way down to the wlan0 section. "
      "From there, copy the IP address after \"inet\"")
serverIP = str(input("Enter IP address: "))
print("Using this IP: " + serverIP + "\n")
port = 7007
buff = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((serverIP, port))

message = sock.recv(buff)
print(f"Message from Server: {message.decode()}")

