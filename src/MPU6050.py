import smbus
import socket

class MPU6050:
    def __init__(self, bus_num=1, address=0x68):
        self.bus = smbus.SMBus(bus_num)
        self.address = address
        self.PWR_MGMT_1 = 0x6B
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F

        # Wake up the MPU-6050
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0)

    def read_raw_values(self):
        # Read the high and low bytes for each axis
        x_out_h = self.bus.read_byte_data(self.address, self.ACCEL_XOUT_H)
        x_out_l = self.bus.read_byte_data(self.address, self.ACCEL_XOUT_H+1)
        y_out_h = self.bus.read_byte_data(self.address, self.ACCEL_YOUT_H)
        y_out_l = self.bus.read_byte_data(self.address, self.ACCEL_YOUT_H+1)
        z_out_h = self.bus.read_byte_data(self.address, self.ACCEL_ZOUT_H)
        z_out_l = self.bus.read_byte_data(self.address, self.ACCEL_ZOUT_H+1)

        # Convert the 16-bit values to signed integers
        x_out = (x_out_h << 8) | x_out_l
        if x_out > 32767:
            x_out -= 65536
        y_out = (y_out_h << 8) | y_out_l
        if y_out > 32767:
            y_out -= 65536
        z_out = (z_out_h << 8) | z_out_l
        if z_out > 32767:
            z_out -= 65536

        return (x_out, y_out, z_out)

# Create an instance of the MPU6050 class
accel = MPU6050()

"""

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8043))


# Read the accelerometer values continuously and send them to the TCP port
while True:
    x, y, z = accel.read_raw_values()
    # Convert values to string and concatenate with a separator
    data = str(x) + ',' + str(y) + ',' + str(z)
    sock.sendall(data.encode())
    
"""

