import socket
import numpy as np
import time
import struct
import math
import matplotlib.pyplot as plt

mass = 1000
l_front = 1.2865
l_rear = 1.2865
r_rear = 0.4572

soc_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc_in.bind(('', 4001))

ctr = 0
epochs = 3500

t = time.time()
steer_ang = 0
throttle = 0.4
v_x = 0
v_y = 0
c = 0
flag = False

t_data = np.arange(0, epochs)
v_data = np.zeros_like(t_data, dtype=float)
force_data = np.zeros_like(t_data, dtype=float)
sa_data = np.zeros_like(t_data, dtype=float)

while time.time() < t + 20 :
    data = struct.pack('fffiBB', 0, 0, 0, 0, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1

while c < epochs :
    data = struct.pack('fffiBB', steer_ang, throttle, 0, 1, 11, ctr & 0xFF)
    soc_out.sendto(data, ('127.0.0.1', 3001))
    ctr += 1
    
    if flag :
        steer_ang += 0.01

    binary_in = soc_in.recv(4096)
    data_in = struct.unpack('fffiffiffffffffffffffffffffffffiB'+('B' * 39)+('f' * 156)+'BB', binary_in)

    v_gx = data_in[20]
    v_gy = data_in[21]
    yaw = data_in[16]
    yaw_change = data_in[19]

    v_x = (v_gx * np.cos(-yaw)) - (v_gy * np.sin(-yaw))
    v_y = (v_gx * np.sin(-yaw)) + (v_gy * np.cos(-yaw))

    if c > 200 :
        throttle = 1.3 * (14 - v_x)

    if c == 1000 :
        flag = True

    if flag :
        sa_data[c-1000] = math.radians(steer_ang) - np.arctan(float((yaw_change*l_front)+v_y))/(float(v_x))
        force_data[c-1000] = (mass * v_x * yaw_change * l_rear)/((l_rear+l_front) * np.cos(math.radians(steer_ang)))
        v_data[c] = v_x

        print(c, v_x, v_y, sa_data[c-1000], force_data[c-1000], steer_ang)

    else :
        v_data[c] = v_x
        print(c, v_x, v_y)
    
    c += 1

it = 0
fin = epochs
temp_v = np.copy(v_data)
while it<fin :
    if sa_data[it] == 0 and force_data[it] == 0 :
        sa_data = np.delete(sa_data, it)
        force_data = np.delete(force_data, it)
        fin -= 1
    elif temp_v[it+1000] < 13.8 or temp_v[it+1000] > 14.2 :
        sa_data = np.delete(sa_data, it)
        force_data = np.delete(force_data, it)
        temp_v = np.delete(temp_v, it+1000)
        fin -= 1
    else :
        it += 1

save_data = []
for i in range(0, len(sa_data)) :
    arr = []
    arr.append(sa_data[i])
    arr.append(force_data[i])
    save_data.append(arr)

a = np.asarray(save_data)
np.savetxt("gen-data-front.csv", a, delimiter=",")

plt.figure()

plt.subplot(1, 2, 1)
plt.plot(sa_data, force_data)

plt.subplot(1, 2, 2)
plt.plot(t_data, v_data)

plt.show()