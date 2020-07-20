import socket
import numpy as np
import time
import struct
import math
import matplotlib.pyplot as plt

# Into the simulator
soc_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# From the simulator
soc_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in.bind(('', 4001))

epochs = 1500
ctr = 0

r_rear = 0.4572

flag1 = False
flag2 = False

t = time.time()
steer_ang = 0
steer_ang_rad = 0
throttle = 0.4

t_data = np.arange(0, epochs)
v_y_data = np.zeros_like(t_data, dtype=float)
v_x_data = np.zeros_like(t_data, dtype=float)
yaw_data = np.zeros_like(t_data, dtype=float)
sa_data = np.zeros_like(t_data, dtype=float)

while time.time() < t + 20 :
    data = struct.pack('fffiBB', 0, 0, 0, 0, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1

c = 0
counter = 0

while counter < epochs:
    # Into the simulator
    data = struct.pack('fffiBB', steer_ang, throttle, 0, 1, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1
    # From the simulator
    binary_in = soc_in.recv(4096)
    data_in = struct.unpack('fffiffiffffffffffffffffffffffffiB'+('B' * 39)+('f' * 156)+'BB', binary_in)

    v_gx = data_in[20]
    v_gy = data_in[21]
    omega = (data_in[9] + data_in[10]) / 2
    yaw = data_in[16]
    yaw_change = data_in[19]

    v_x = (v_gx * np.cos(-yaw)) - (v_gy * np.sin(-yaw))
    v_y = (v_gx * np.sin(-yaw)) + (v_gy * np.cos(-yaw))
    
    if v_x > 13.8 :
        flag1 = True
    if flag1 :
        c += 1
        throttle = 1.3 * (14 - v_x)
        if c == 50 :
            flag2 = True
    if flag2 :
        throttle = 1.3 * (14 - v_x)
        steer_ang_rad = - 0.11 - 0.096 * (-7.8594 - v_y) + 0.65 * (0.5049 - yaw_change)
        steer_ang = math.degrees(steer_ang_rad)
    
    v_y_data[counter] = v_y
    v_x_data[counter] = v_x
    yaw_data[counter] = yaw_change
    sa_data[counter] = steer_ang_rad

    counter += 1

    print(counter, throttle, steer_ang_rad, v_x, v_y, yaw_change)

plt.figure()
plt.title("Simulation Record")

plt.subplot(2, 2, 1)
plt.title('Lateral Velocity')
plt.plot(t_data, v_y_data)
plt.plot([0, 1499], [-7.8594, -7.8594], linestyle='dashed')

plt.subplot(2, 2, 2)
plt.title('Yaw Rate')
plt.plot(t_data, yaw_data)
plt.plot([0, 1499], [0.5049, 0.5049], linestyle='dashed')

plt.subplot(2, 2, 3)
plt.title('Steering Angle')
plt.plot(t_data, sa_data)
plt.plot([0, 1499], [-0.11, -0.11], linestyle='dashed')

plt.subplot(2, 2, 4)
plt.title('Longitudinal Velocity')
plt.plot(t_data, v_x_data)
plt.plot([0, 1499], [14, 14], linestyle='dashed')

plt.show()