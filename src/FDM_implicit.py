import numpy as np
from .fdm_constructors import input_f
from .fdm_constructors import StandingWave  # Standing wave
from .fdm_constructors import InputWave  # Traveling wave
from .fdm_constructors import BCs  # Boundary conditions
import matplotlib.pyplot as plt
import winsound


def fdm_implicit(materials_summary, interphase_position, nodes, dx, x, time, n_steps, dt, initial_velocity, amplitude,
                 period, input_time, battery_map, summary_e_modulus, gamma_map, phi_map):

    # Matrix definition and vectors
    a = np.zeros((nodes - 2, nodes - 2))
    b = np.zeros(nodes - 2)
    uj0 = np.zeros(nodes - 2)  # Deformation in the present u^j
    uj1 = np.zeros(nodes - 2)  # Deformation in the future u^j+1
    uj_1 = np.zeros(nodes - 2)  # Deformation in the past u^j-1
    h = np.zeros((nodes, n_steps + 1))  # Matrix where the solution is stored after iteration

    interphase_node = []
    for _interphase_position in range(len(interphase_position)):  # compute an integer value for each interphase
        value = round((round(interphase_position[_interphase_position], 3)) * nodes, 0)
        interphase_node.append(value)

    _y = input_f(np.arange(0, 9.4e-07, dt), dt)

    for j in range(0, n_steps):  # Implicit Finite Difference Method implementation
        condition = True  # Used to know when is the last material
        formulation = InputWave()  # Wave that get into the domain
        bc = BCs()
        u_right = 0
        if j == 0:
            u_left = _y[j]
            interphase_count = 0
            for node_count in range(0, nodes):
                if (interphase_node[interphase_count] < interphase_node[-1] + 1) and (condition is True):  # Perform at
                    # all but the last material
                    if node_count == 0:  # first node
                        gamma = gamma_map[interphase_count]
                        formulation.time_0_node_0(gamma, u_left, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count+1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == 1:  # second node
                        phi = phi_map[interphase_count]
                        formulation.time_0_node_1(phi, u_left, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if (node_count > 1) and (node_count < interphase_node[interphase_count] - 1) and \
                            (node_count != interphase_node[interphase_count - 1] + 1):  # central nodes
                        phi = phi_map[interphase_count]
                        formulation.time_0_internal_node(phi, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if node_count == interphase_node[interphase_count] - 1:  # node that takes the interphase right
                        gamma = gamma_map[interphase_count]
                        formulation.time_0_node__1_interphase(gamma, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == interphase_node[interphase_count]:  # interphase
                        material_1 = battery_map[interphase_count]
                        e_modulus_1 = summary_e_modulus[material_1]
                        material_2 = battery_map[interphase_count + 1]
                        e_modulus_2 = summary_e_modulus[material_2]
                        formulation.alpha_m(e_modulus_1, e_modulus_2)
                        alpha = formulation.alpha
                        formulation.time_0_interphase(alpha)
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b
                        interphase_count += 1

                    if node_count == interphase_node[interphase_count - 1] + 1:  # node that takes the interphase left
                        gamma = gamma_map[interphase_count]
                        formulation.time_0_node_1_interphase(gamma, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if interphase_count == len(interphase_node):
                        condition = False
                        interphase_count -= 1

                else:  # last material
                    if node_count == interphase_node[interphase_count] + 1:  # takes a node at its left interphase
                        gamma = gamma_map[interphase_count]
                        formulation.time_0_node_1_interphase(gamma, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if (node_count > interphase_node[-1] + 1) and (node_count < nodes - 4): # central nodes
                        phi = phi_map[interphase_count]
                        formulation.time_0_internal_node(phi, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if node_count == nodes - 4:  # penultimate node
                        phi = phi_map[interphase_count]
                        formulation.time_0_penultimate_node(phi, initial_velocity, dt, u_right, uj0[node_count])
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == nodes - 3:  # last node
                        gamma = gamma_map[interphase_count]
                        formulation.time_0_last_node(gamma, initial_velocity, dt, u_right, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        b[node_count] = formulation.b

            #  uj1 = np.linalg.solve(a, b)
            a_inverse = np.linalg.pinv(a)
            uj1 = np.dot(a_inverse, b)
            uj1t = np.hstack([u_left, uj1, u_right])
            h[:, j+1] = uj1t[:]
            uj_1 = uj0
            uj0 = uj1

        if j > 0:
            if j < len(_y):
                u_left = _y[j]
            elif (j > len(_y)) and (j < (len(_y) + 5000)):
                u_left = 0
            else:
                bc.left_soft_bc(uj0[0], uj0[1])
                u_left = bc.u_left_value
            interphase_count = 0
            for node_count in range(0, nodes):
                if (interphase_node[interphase_count] < interphase_node[-1] + 1) and (condition is True):  # Perform at
                    # all but the last material
                    if node_count == 0:
                        gamma = gamma_map[interphase_count]
                        formulation.node_0(gamma, uj0[node_count], uj_1[node_count], u_left)
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == 1:
                        phi = phi_map[interphase_count]
                        formulation.node_1(phi, uj0[node_count], uj_1[node_count], u_left)
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if (node_count > 1) and (node_count < interphase_node[interphase_count] - 1) and \
                            (node_count != interphase_node[interphase_count - 1] + 1):  # central nodes
                        phi = phi_map[interphase_count]
                        formulation.internal_node(phi, uj0[node_count], uj_1[node_count])
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if node_count == interphase_node[interphase_count] - 1:  # node that takes the interphase right
                        gamma = gamma_map[interphase_count]
                        formulation.node__1_interphase(gamma, uj0[node_count], uj_1[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == interphase_node[interphase_count]:  # interphase
                        material_1 = battery_map[interphase_count]
                        e_modulus_1 = summary_e_modulus[material_1]
                        material_2 = battery_map[interphase_count + 1]
                        e_modulus_2 = summary_e_modulus[material_2]
                        formulation.alpha_m(e_modulus_1, e_modulus_2)
                        alpha = formulation.alpha
                        formulation.interphase(alpha)
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b
                        interphase_count += 1

                    if node_count == interphase_node[interphase_count - 1] + 1:  # node that takes the interphase left
                        gamma = gamma_map[interphase_count]
                        formulation.node_1_interphase(gamma, uj0[node_count], uj_1[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if interphase_count == len(interphase_node):
                        condition = False
                        interphase_count -= 1

                else:
                    if node_count == interphase_node[interphase_count] + 1:  # takes a node at its left interphase
                        gamma = gamma_map[interphase_count]
                        formulation.node_1_interphase(gamma, uj0[node_count], uj_1[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if (node_count > interphase_node[-1] + 1) and (node_count < nodes - 4):  # central nodes
                        phi = phi_map[interphase_count]
                        formulation.internal_node(phi, uj0[node_count], uj_1[node_count])
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if node_count == nodes - 4:
                        phi = phi_map[interphase_count]
                        formulation.penultimate_node(phi, uj0[node_count], uj_1[node_count], u_right)
                        a[node_count, node_count - 2] = formulation.a_i_i_2
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == nodes - 3:
                        gamma = gamma_map[interphase_count]
                        formulation.last_node(gamma, uj0[node_count], uj_1[node_count], u_right)
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        b[node_count] = formulation.b

            #  uj1 = np.linalg.solve(a, b)
            a_inverse = np.linalg.pinv(a)
            uj1 = np.dot(a_inverse, b)
            uj1t = np.hstack([u_left, uj1, u_right])
            h[:, j + 1] = uj1t[:]
            uj_1 = uj0
            uj0 = uj1

    duration = 1000  # milliseconds
    freq = 380  # Hz
    winsound.Beep(freq, duration)

    for i in range(0, n_steps + 1, 15):
        plt.cla()  # borra pantalla anterior del plot
        plt.xlim(0, 1.)
        #plt.ylim(-0.000001, 0.000001)
        _iteration = i
        plt.plot(x, h[:, i], color='r', label=_iteration)
        plt.legend()
        plt.grid()
        plt.pause(0.00000000000000001)

    return h
