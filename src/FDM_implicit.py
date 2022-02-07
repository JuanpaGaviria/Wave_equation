import numpy as np
from .fdm_constructors import Input
from .fdm_constructors import ImplicitFormulation
from .fdm_constructors import StandingWave
from .fdm_constructors import InputWave



def fdm_implicit(materials_summary, interphase_position, material_dimensionless_length, nodes, dx, x, time, n_steps, dt,
                   initial_velocity, amplitude, period, input_time):

    # Matrix definition and vectors
    a = np.zeros((nodes - 2, nodes - 2))
    b = np.zeros(nodes - 2)
    uj0 = np.zeros(nodes - 2)  # Deformation in the present u^j
    uj1 = np.zeros(nodes - 2)  # Deformation in the future u^j+1
    uj_1 = np.zeros(nodes - 2)  # Deformation in the past u^j-1
    h = np.zeros((nodes, n_steps + 1))  # Matrix where the solution is stored after iteration
    _input = Input()
    _input.cosine_method(amplitude, period, input_time, dt)
    input_list = _input.input_list

    interphase_node = []
    for _interphase_position in range(len(interphase_position)):  # compute an integer value for each interphase
        value = round((round(interphase_position[_interphase_position], 2)) * nodes, 0)
        interphase_node.append(value)

    for j in range(0, n_steps):  # Implicit Finite Difference Method implementation
        if j == 0:
            interphase_count = 0
            node_count = 0
            u_left = input_list[node_count]
            formulation = InputWave()

            for node_count in range(0, nodes):
                if interphase_node[interphase_count] != interphase_node[-1]:  # Perform at all but the last material
                    if node_count == 0:  # first node
                        materials_summary[interphase_count].gamma_phi_m(dt, dx)
                        gamma = materials_summary[interphase_count].gamma
                        formulation.time_0_node_0(gamma, u_left, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count+1] = formulation.a_i_i1
                        b[node_count] = formulation.b

                    if node_count == 1:  # second node
                        materials_summary[interphase_count].gamma_phi_m(dt, dx)
                        phi = materials_summary[interphase_count].phi
                        formulation.time_0_node_1(phi, u_left, initial_velocity, dt, uj0[node_count])
                        a[node_count, node_count - 1] = formulation.a_i_i_1
                        a[node_count, node_count] = formulation.a_i_i
                        a[node_count, node_count + 1] = formulation.a_i_i1
                        a[node_count, node_count + 2] = formulation.a_i_i2
                        b[node_count] = formulation.b

                    if (node_count > 1) and (node_count < interphase_node[interphase_count] - 1) and \
                            (node_count != interphase_node[interphase_count-1]+1):  # central nodes
                        pass

                    if node_count == interphase_node[interphase_count] - 1:  # node that takes the interphase right
                        pass

                    if node_count == interphase_node[interphase_count]:  # interphase
                        interphase_count += 1

                    if node_count == interphase_node[interphase_count - 1] + 1:  # node that takes the interphase left
                        pass

                else:  # last material
                    if node_count == interphase_node[interphase_count - 1] + 1:  # takes a node at its left interphase
                        pass

                    if node_count < interphase_node[-1] and node_count < nodes - 4 and \
                            (node_count != interphase_node[interphase_count-1]+1):  # central nodes
                        pass

                    if node_count == nodes - 4:  # penultimate node
                        pass

                    if node_count == nodes - 3:  # last node
                        pass

        if j > 0:
            interphase_count = 0
            node_count = 0
            for node_count in range(0, nodes):
                if interphase_node[interphase_count] != interphase_node[-1]:
                    if node_count == 0:
                        pass

                    if node_count == 1:
                        pass

                    if (node_count > 1) and (node_count < interphase_node[interphase_count] - 1) and \
                            node_count != interphase_node[interphase_count-1]+1:
                        pass

                    if node_count == interphase_node[interphase_count] - 1:
                        pass

                    if node_count == interphase_node[interphase_count]:
                        pass
                        interphase_count += 1

                    if node_count == interphase_node[interphase_count - 1] + 1:
                        pass

                else:
                    if node_count == interphase_node[interphase_count - 1] + 1:  # takes a node at its left interphase
                        pass

                    if node_count < interphase_node[-1] and node_count < nodes - 4 and \
                            (node_count != interphase_node[interphase_count - 1] + 1):  # central nodes
                        pass

                    if node_count == nodes - 4:
                        pass

                    if node_count == nodes - 3:
                        pass

    return h
