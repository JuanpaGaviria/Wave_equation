import numpy as np
from numpy.linalg import inv
import matplotlib.pylab as plt
import winsound

nodes = 100
distance = 1
dx = distance/(nodes-1)
_x = np.linspace(0, distance, nodes-2)
f = np.sin(np.pi * _x)
phi = np.zeros((nodes-2, nodes-2))
c = 10
time = 1
n_steps = 1000
dt = time/(n_steps-1)
elastic_modulus = 1
density = 2
initial_velocity = 1
k = ((elastic_modulus*dt**2)/density)

def phi_matrix_f(node, _x):
    for row in range(node-2):
        for col in range(node-2):
            r = np.linalg.norm(_x[row]-_x[col])
            phi[row, col] = np.sqrt(r**2 + c**2)
    return phi


def fo_phi_f(_x, node):
    fo_phi = np.zeros((node-2, node-2))
    for row in range(node-2):
        for col in range(node-2):
            r = np.linalg.norm(_x[row] - _x[col])
            fo_phi[row, col] = ((r**2+c**2)**(-1/2))*(_x[row]-_x[col])
    return fo_phi


def so_phi_f(_x, node):
    so_phi = np.zeros((node-2, node-2))
    for row in range(nodes-2):
        for col in range(nodes-2):
            r = np.linalg.norm(_x[row] - _x[col])
            so_phi[row, col] = c**2/((c**2+r**2)**(3/2))
    return so_phi


#phi_derivative = fo_phi_f(_x, nodes)
#fo_rbf = np.dot(phi_derivative, alpha)
#fo_phi_analytical = np.cos(_x)

uj0 = np.zeros(nodes-2)
uj1 = np.zeros(nodes-2)
uj_1 = np.zeros(nodes-2)
h = np.zeros((nodes, n_steps+1))  # Matrix where the solution is stored after iteration
u_left = 0
u_right = 0
uj0t = np.hstack([u_left, uj0, u_right])
h[:, 0] = uj0t

for _i in range(len(uj_1)):
    uj_1[_i] = (f[_i] - initial_velocity*dt)

for j in range(0, n_steps):
    if j == 0:
        _phi = phi_matrix_f(nodes, _x)
        alpha = np.linalg.solve(_phi, f)
        function_rbf = np.dot(_phi, alpha)

        _so_phi = so_phi_f(_x, nodes)
        so_rbf = np.dot(_so_phi, alpha)
        so_function_analytical = -np.sin(_x)

        #k_so_rbf = np.dot(k, so_rbf)
        k_so_rbf = k * so_rbf
        uj1 = k_so_rbf + f
        uj1t = np.hstack([u_left, uj1, u_right])
        h[:, j+1] = uj1t[:]
        uj_1 = uj0
        uj0 = uj1

    if j > 0:
        _phi = phi_matrix_f(nodes, _x)
        alpha = np.linalg.solve(_phi, uj0)
        function_rbf = np.dot(_phi, alpha)

        _so_phi = so_phi_f(_x, nodes)
        so_rbf = np.dot(_so_phi, alpha)
        so_function_analytical = -np.sin(_x)

        #k_so_rbf = np.dot(k, so_rbf)
        k_so_rbf = k * so_rbf
        uj1 = k_so_rbf + (2*uj0)-uj_1
        uj1t = np.hstack([u_left, uj1, u_right])
        h[:, j+1] = uj1t[:]
        uj_1 = uj0
        uj0 = uj1

duration = 1000  # milliseconds
freq = 380  # Hz
winsound.Beep(freq, duration)

x = np.linspace(0, distance, nodes)

for i in range(0, n_steps + 1, 1):
    plt.cla()  # borra pantalla anterior del plot
    #plt.xlim(0, 1.)
    #plt.ylim(-1, 1)
    _iteration = i
    plt.plot(x, h[:, i], color='r', label=_iteration)
    plt.legend()
    plt.grid()
    plt.pause(0.00000000000000001)
