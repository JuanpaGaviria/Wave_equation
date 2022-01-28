import matplotlib.pyplot as plt
import numpy as np

dpi = 100
fz = (5, 5)
_He = np.genfromtxt('explicit_solution.txt', delimiter=' ')
_Hi = np.genfromtxt('implicit_solution.txt', delimiter=' ')
_Ha = np.genfromtxt('analytical_solution.txt', delimiter=' ')
x = np.linspace(0, 1, _He.shape[0])
fig = plt.figure(dpi=dpi, figsize=fz)
plt.plot(x, _He[:, 0], lw=1.5, color='k', label= 'Iteration 0 explicit')
plt.plot(x, _Hi[:, 0], lw=1.5, color='r', marker='o', label= 'Iteration 0 implicit')
plt.plot(x, _Ha[:, 0], lw=1.5, color='b', marker = '*',label='Iteration 0 analytical')
plt.plot(x, _He[:, 500], lw=1.5, color='k', label= 'Iteration 500 explicit')
plt.plot(x, _Hi[:, 500], lw=1.5, color='r',marker= 'o', label= 'Iteration 500 implicit')
plt.plot(x, _Ha[:, 500], lw=1.5, color='b',marker= '*', label= 'Iteration 500 analytical')
plt.grid()
plt.legend()
plt.show()
