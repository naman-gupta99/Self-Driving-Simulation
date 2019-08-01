# simplest version = just go straight with 50% gas

import socket
import struct
import time
import math
import numpy as np
import matplotlib.pyplot as plt

soc_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in.bind(('', 4001))
ctr = 0

t = time.time()
steer_ang = 0
throttle = 0.4
f_vel = 0
c = 0
flag = False

t_data = np.arange(0, 3000)
v_data = np.zeros_like(t_data)

while time.time() < t + 20:
    data = struct.pack('fffiBB', 0, 0, 0, 0, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1

while c<3000 :
    data = struct.pack('fffiBB', steer_ang, throttle, 0, 1, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1
    curr_t = time.time()
    if curr_t - t >= 1 :
        t = curr_t
        if flag:
            steer_ang += 0.5
    binary_in = soc_in.recv(4096)
    data_in = struct.unpack('fffiffiffffffffffffffffffffffffiB'+('B' * 39)+('f' * 156)+'BB', binary_in)
    f_vel = math.sqrt((data_in[20] ** 2) + (data_in[21] ** 2))
    if c > 30 :
        throttle = (14 - f_vel)/14
    if f_vel >= 13.11 :
        flag = True
    v_data[c] = f_vel
    c += 1
    print(c, f_vel)

plt.plot(t_data, v_data)
plt.show()