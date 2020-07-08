import numpy as np
import matplotlib.pyplot as plt

data = []
prev_data = np.genfromtxt('gen-data-front.csv', delimiter=',')

for i in prev_data :
    arr = []
    arr.append(-i[0])
    arr.append(-i[1])
    data.insert(0, arr)

data.extend(prev_data)

a = np.asarray(data)
np.savetxt("res-front.csv", a, delimiter=",")

sa_data = []
force_data = []
force_app_data = []

for i in data :
    sa_data.append(i[0])
    force_data.append(i[1])
    force_app_data.append(47940 * np.sin(0.1379 * np.arctan(5.115 * i[0])))

plt.title('Force VS Slip Angle - Front')
plt.xlabel('Slip Angle, rad')
plt.ylabel('Force, N')
plt.plot(sa_data, force_data, linewidth=10)
plt.plot(sa_data, force_app_data)
plt.legend(['Simulation data', 'Magic Formula'])
plt.show()