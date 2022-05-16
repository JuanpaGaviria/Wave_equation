# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 10:19:04 2022

@author: EQ01
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

h = np.loadtxt('h_400_discharged.csv', delimiter=',')
n_steps = 20000
dimensionless_length = 1
nodes = 400

x = np.linspace(0, dimensionless_length, nodes)

for i in range(0, n_steps + 1, 15):
    plt.cla()  # borra pantalla anterior del plot
    plt.xlim(0, 1.)
    plt.ylim(-0.0001, 0.0001)
    _iteration = i
    plt.plot(x, h[:, i], color='r', label=_iteration)
    plt.legend()
    plt.grid()
    plt.pause(0.00000000000000001)