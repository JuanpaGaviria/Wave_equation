import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import winsound
from src import Bigbang
from src.battery_construction import battery_structure
from src.FDM_implicit import fdm_implicit

"""material selection
0, 2: anode charged, anode discharged 
1, 3: cathode charged, cathode discharged
6: separator
4,5,7,8,9: others (check csv)
10, 11: benzene electrolyte, carbon tetrachloride electrolyte 
"""
indexes = [1, 2, 3]  # materials definition
fold_number = 3  # Layers conformed by the materials defined

nodes, n_steps = 250, 6000
dt = 1e-7/4
time = n_steps * dt
initial_velocity, amplitude, period, input_time = 0, 2, 2, 0.1

url = './src/database/materials_properties.csv'
df = pd.read_csv(url)

battery_interfaces, battery_layers, battery_map = battery_structure(indexes, fold_number)
materials, materials_summary, materials_number, materials_thickness, material_dimensionless_length, length,\
        dx, x, interphase_position, summary_e_modulus, gamma_map, phi_map = Bigbang.big_bang(indexes, df, nodes,
                                                                                             battery_map, dt)
H = fdm_implicit(materials_summary, interphase_position, nodes, dx, x, time, n_steps, dt,
                 initial_velocity, amplitude, period, input_time, battery_map, summary_e_modulus, gamma_map,
                 phi_map)
