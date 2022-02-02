import numpy as np
from .fdm_constructors import Input

def fdm_implicit(materials_summary, interphase_position, material_dimensionless_length, nodes, dx, x, time, n_steps, dt,
                   initial_velocity, amplitude, period):

    # Matrix definition and vectors
    a = np.zeros((nodes - 2, nodes - 2))
    b = np.zeros(nodes - 2)
    uj0 = np.zeros(nodes - 2)  # Deformation in the present u^j
    uj1 = np.zeros(nodes - 2)  # Deformation in the future u^j+1
    uj_1 = np.zeros(nodes - 2)  # Deformation in the past u^j-1
    h = np.zeros((nodes, n_steps + 1))  # Matrix where the solution is stored after iteration

    for j in range(0, n_steps):
        pass

    return h
