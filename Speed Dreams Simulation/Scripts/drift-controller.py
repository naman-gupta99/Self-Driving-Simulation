import socket
import struct
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# Into the simulator
soc_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# From the simulator
soc_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in.bind(('', 4001))

ctr = 0
steer_ang = 0
throttle = 0.2
t = time.time()

while time.time() < t + 20:
    data = struct.pack('fffiBB', 0, 0, 0, 0, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1

while True:
    # Into the simulator
    data = struct.pack('fffiBB', steer_ang, throttle, 0, 1, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1
    # From the simulator
    binary_in = soc_in.recv(4096)
    data_in = struct.unpack('fffiffiffffffffffffffffffffffffiB'+('B' * 39)+('f' * 156)+'BB', binary_in)
    f_vel = math.sqrt((data_in[20] ** 2) + (data_in[21] ** 2))
    l_vel = f_vel / np.tan(data_in[21] / data_in[20])
    phi_dot = data_in[19]
    if f_vel > 13.8 :
        throttle = 1.3*(14 - f_vel)
        steer_ang -= (0.11*(l_vel + 7.461843) - 0.7*(0.450844-phi_dot))
    print(throttle, steer_ang)