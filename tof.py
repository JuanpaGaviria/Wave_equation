import numpy as np
import matplotlib.pyplot as plt

def tof(dt, n_steps):
    h = np.loadtxt('test_400n_2000it.csv', delimiter=',')
    node_zero = []
    node_one = []
    dt = 1e-7
    deformation = []
    times = []
    n_steps = 2000
    time = n_steps * dt

    for i in range(h.shape[1] - 3):

        u0 = h[0, i]
        u1 = h[0, i + 1]
        u2 = h[0, i + 2]
        u3 = h[0, i + 3]

        derivative_1 = (u1 - u0) / dt
        derivative_2 = (u3 - u2) / dt

        sign_1 = np.sign(derivative_1)
        sign_2 = np.sign(derivative_2)

        if sign_1 != sign_2:
            prom_deformation = (h[0, i + 1] + h[0, i + 2]) / 2
            iter_time = (i * time) / n_steps
            deformation.append(prom_deformation)
            times.append(iter_time)
