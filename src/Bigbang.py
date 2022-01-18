import numpy as np
import pandas as pd
from .material_constructor import Material


def big_bang(indexes, df, nodes, time, n_steps, layer_number):

    materials = []  # Material type present in the test (str)
    materials_summary = []  # Material instantiation
    materials_number = int(len(indexes))  # Amount of different materials present in the test

    # Obtaining the materials attributes
    for i in range(materials_number):
        idx = indexes[i]  # takes index i
        _type = df._get_value(idx, "Type")  # From de data frame (df) takes the str Type at the index i
        materials.append(_type)  # Add the str Type in the list materials

    # Obtaining the materials attributes
    df=df.set_index('Type')  # Type column is set as the index of the data frame
    for j in range(materials_number):
        _material = materials[j]  # takes each materials type to get attributes
        density = df.loc[_material, 'density']  # Takes density for each material
        e_modulus = df.loc[_material, 'e_modulus']  # Takes elastic modulus for each material
        thickness = df.loc[_material, 'thickness']  # Takes thickness for each material
        state = df.loc[_material, 'state']  # Takes state for each material
        bulk_modulus = df.loc[_material, 'bulk_modulus']  # Takes bulk modulus for each material

        # Material class instantiation
        material = Material(density, e_modulus, thickness, state, bulk_modulus)
        materials_summary.append(material)
    return






