import matplotlib.pyplot as plt
import numpy as np

#dpi = 100
#fz = (5, 5)
_He = np.genfromtxt('explicit_solution.txt', delimiter=' ')
_Hi = np.genfromtxt('implicit_solution.txt', delimiter=' ')
_Ha = np.genfromtxt('analytical_solution.txt', delimiter=' ')
_H = np.genfromtxt('implicit_solution_fivepoints.txt', delimiter=' ')
x = np.linspace(0, 1, _He.shape[0])
fig, axs = plt.subplots(2)
fig.suptitle('Wave equation solution')
axs[0].set_title('Solution at initial time')
axs[0].plot(x, _He[:, 0], lw=1.5, color='k', label= 'explicit')
#axs[0].plot(x, _Hi[:, 0], lw=1.5, color='r', label= 'implicit')
axs[0].plot(x, _H[:, 0], lw=1.5, color='r', label= 'implicit_5p')
axs[0].plot(x, _Ha[:, 0], lw=1.5, color='b', marker = '*',label='analytical')

axs[1].set_title('Solution at 5 s')
axs[1].plot(x, _He[:, 500], lw=1.5, color='k', label= 'explicit')
#axs[1].plot(x, _Hi[:, 500], lw=1.5, color='r', label= 'implicit')
axs[1].plot(x, _H[:, 500], lw=1.5, color='r', label= 'implicit_5p')
axs[1].plot(x, _Ha[:, 500], lw=1.5, color='b',marker= '*', label= 'analytical')


axs[1].set_xlabel('x')
axs[0].set_ylabel('u')
axs[1].set_ylabel('u')
axs[0].grid()
axs[1].grid()
axs[0].legend()
axs[1].legend()

# set the spacing between subplots
fig.tight_layout()

plt.show()
