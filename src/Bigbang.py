import numpy as np
import pandas as pd
from .material_constructor import Material


def big_bang(indexes, df, nodes, time, n_steps, battery_map):

    materials = []  # Material type present in the test (str)
    materials_summary = []  # Material instantiation
    materials_number = int(len(indexes))  # Amount of different materials present in the test
    materials_thickness = []

    # Obtaining the materials attributes
    for i in range(materials_number):
        idx = indexes[i]  # takes index i
        _type = df._get_value(idx, "Type")  # From de data frame (df) takes the str Type at the index i
        materials.append(_type)  # Add the str Type in the list materials
        print("check: Got the materials type")

    # Obtaining the materials attributes
    df = df.set_index('Type')  # Type column is set as the index of the data frame
    for j in range(materials_number):
        _material = materials[j]  # takes each materials type to get attributes
        density = df.loc[_material, 'density']  # Takes density for each material
        print("Check: Density of material ", j, " has been read")
        e_modulus = df.loc[_material, 'e_modulus']  # Takes elastic modulus for each material
        print("Check: elastic modulus of material ", j, " has been read")
        thickness = df.loc[_material, 'thickness']  # Takes thickness for each material
        print("Check: thickness of material ", j, " has been read")
        state = df.loc[_material, 'state']  # Takes state for each material
        print("Check: state of material ", j, " has been read")
        bulk_modulus = df.loc[_material, 'bulk_modulus']  # Takes bulk modulus for each material
        print("Check: bulk of material ", j, " has been read")

        # Material class instantiation
        material = Material(density, e_modulus, thickness, state, bulk_modulus, j)
        materials_summary.append(material)
        print("check: material has been added to the list")
        materials_thickness.append(material.thickness[-1])
        print("check: thickness has been added to the list")

    length = 0
    _dict = dict(zip(indexes, materials_thickness))
    for _length in range(len(battery_map)):
        _id = battery_map[_length]
        thick = _dict[_id]
        length = length + thick

    print("check: length has been computed:", length)

    return length,






