import socket

print("First, please specify the IP address of the server. Form : 192.168.x.x."
      "\nIf you do not know the IP address, please run \"ifconfig\" on the beaglebone."
      "\nYou should scroll all the way down to the wlan0 section. "
      "From there, copy the IP address after \"inet\"")
IP = str(input("Enter IP address: "))
PORT = 7007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((IP, PORT))

message = sock.recv(2048)

print("Message received:", message)
