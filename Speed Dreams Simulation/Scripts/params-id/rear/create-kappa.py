import numpy as np
import matplotlib.pyplot as plt

data = []
prev_data = np.genfromtxt('gen-data-kappa.csv', delimiter=',')

data.extend(prev_data)

v_y_data = []
kappa_data = []

for i in data :
    v_y_data.append(i[0])
    kappa_data.append(i[1])

plt.title('Longitudinal Slip')
plt.ylabel('Longitudinal Slip')
plt.plot(v_y_data, kappa_data, linewidth=2)
plt.show()