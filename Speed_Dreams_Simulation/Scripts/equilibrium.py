from scipy.optimize import root
import numpy as np
import math
import matplotlib.pyplot as plt
import os

m = 1000
l_r = 1.2865
l_f = 1.2865

v_x = 14
delta = 0

B_r = 57.64
C_r = 0.03489
D_r = 131700
B_f = 5.115
C_f = 0.1379
D_f = 47940

delta_arr = np.arange(-0.35, 0.35, 0.0006)
delta_d_arr = np.arange(-0.35, 0.35, 0.0006)

def fun_F_ry(phi_dot) :
    return m * v_x * phi_dot
    
def fun_alpha_r(phi_dot) :
    F_ry = fun_F_ry(phi_dot)

    return np.tan(np.arcsin(F_ry/D_r)/C_r)/B_r

def fun_F_fy(phi_dot) :
    F_ry = fun_F_ry(phi_dot)

    return F_ry * l_r/(l_f * np.cos(delta))

def fun_alpha_f(phi_dot) :
    F_fy = fun_F_fy(phi_dot)

    return np.tan(np.arcsin(F_fy/D_f)/C_f)/B_f

def fun_primary(p) :
    v_y, phi_dot = p
    alpha_r = fun_alpha_r(phi_dot)
    alpha_f = fun_alpha_f(phi_dot)

    F = []
    F.append(alpha_r - np.arctan((phi_dot * l_r - v_y)/v_x))
    F.append(alpha_f + np.arctan((phi_dot * l_r + v_y)/v_x) - delta)
    return F

def func_val(p) :
    return root(fun_primary, p, method='lm', options={'diag': [27, 10]}).x

phi_dot_arr = np.zeros_like(delta_arr, dtype=float)
v_y_arr = np.zeros_like(delta_arr, dtype=float)
phi_dot_ld_arr = np.zeros_like(delta_arr, dtype=float)
v_y_ld_arr = np.zeros_like(delta_arr, dtype=float)
phi_dot_rd_arr = np.zeros_like(delta_arr, dtype=float)
v_y_rd_arr = np.zeros_like(delta_arr, dtype=float)

for i in range(len(delta_arr)) :
    load = ['/', '-', '\\', '|']
    print(load[i%4])
    delta = delta_arr[i]
    val = func_val([0, 0])
    v_y_arr[i] = val[0]
    phi_dot_arr[i] = val[1]
    delta = delta_arr[i]
    val = func_val([-12, 0.5])
    v_y_ld_arr[i] = val[0]
    phi_dot_ld_arr[i] = val[1]
    val = func_val([12, -0.5])
    v_y_rd_arr[i] = val[0]
    phi_dot_rd_arr[i] = val[1]
    os.system('cls')

delta_arr = np.delete(delta_arr, [128, 129, 130, 131, 132, 133, 134, 1033, 1034, 1035, 1036, 1037, 1038, 1039])
phi_dot_arr = np.delete(phi_dot_arr, [128, 129, 130, 131, 132, 133, 134, 1033, 1034, 1035, 1036, 1037, 1038, 1039])
v_y_arr = np.delete(v_y_arr, [128, 129, 130, 131, 132, 133, 134, 1033, 1034, 1035, 1036, 1037, 1038, 1039])

print('delta', delta_d_arr[500], 'phi', phi_dot_ld_arr[500], 'v_y', v_y_ld_arr[500])

plt.figure()

plt.subplot(1, 2, 1)
plt.title('Yaw Change vs Steering Angle')
plt.xlabel('Steering Angle, rad')
plt.ylabel('Yaw Change, rad/s')
plt.plot(delta_arr, phi_dot_arr, color="#5df542", linewidth=3)
plt.plot(delta_d_arr, phi_dot_ld_arr, color="#ff0000", linewidth=3)
plt.plot(delta_d_arr, phi_dot_rd_arr, color="#ff9d00", linewidth=3)
plt.legend(['Normal Driving', 'Left Drift', 'Right Drift'])

plt.subplot(1, 2, 2)
plt.title('Lateral Velocity vs Steering Angle')
plt.xlabel('Steering Angle, rad')
plt.ylabel('Lateral Velocity, m/s')
plt.plot(delta_arr, v_y_arr, color="#5df542", linewidth=3)
plt.plot(delta_d_arr, v_y_ld_arr, color="#ff0000", linewidth=3)
plt.plot(delta_d_arr, v_y_rd_arr, color="#ff9d00", linewidth=3)
plt.legend(['Normal Driving', 'Left Drift', 'Right Drift'])

plt.show()