import numpy as np
import pandas as pd
from .material_constructor import Material


def big_bang(indexes, df, nodes, battery_map):

    materials = []  # Material type present in the test (str)
    materials_summary = []  # Material instantiation
    materials_number = int(len(indexes))  # Amount of different materials present in the test
    materials_thickness = []  # thickness
    material_dimensionless_length = []  # dimensional thickness
    interphase_position = []

    # Obtaining the materials type
    for i in range(materials_number):
        idx = indexes[i]  # takes index i
        _type = df._get_value(idx, "Type")  # From de data frame (df) takes the str Type at the index i
        materials.append(_type)  # Add the str Type in the list materials

    # Obtaining the materials attributes
    df = df.set_index('Type')  # Type column is set as the index of the data frame
    for j in range(materials_number):
        _material = materials[j]  # takes each materials type to get attributes
        density = df.loc[_material, 'density']  # Takes density for each material
        e_modulus = df.loc[_material, 'e_modulus']  # Takes elastic modulus for each material
        thickness = df.loc[_material, 'thickness']  # Takes thickness for each material
        state = df.loc[_material, 'state']  # Takes state for each material
        bulk_modulus = df.loc[_material, 'bulk_modulus']  # Takes bulk modulus for each material

        # Material class instantiation
        material = Material(density, e_modulus, state, bulk_modulus, thickness, _material)  # material instantiation
        materials_summary.append(material)  # stores each material in a list
        materials_thickness.append(material.thickness)  # stores each material thickness in a list

    # Length definition
    length = 0
    _dict = dict(zip(indexes, materials_thickness))  # creates a dictionary
    for _length in range(len(battery_map)):  # computes the total length
        _id = battery_map[_length]
        thick = _dict[_id]
        length = length + thick

    # dimensionless length definition
    for _dimensionless_length in range(len(battery_map)):  # computes the dimensionless thickness
        _id = battery_map[_dimensionless_length]
        dimensionless_thickness = _dict[_id] / length
        dimensionless_thickness = round(dimensionless_thickness, 2)  # rounds the value (this has to be tested when\
        # generating the nodes
        material_dimensionless_length.append(dimensionless_thickness)  # save each dimensionless thickness in a list

    # definition of the interphase positions
    positions = 0
    for i in range(len(material_dimensionless_length)):
        positions = positions + material_dimensionless_length[i]
        interphase_position.append(positions)

    dimensionless_length = 0
    for j in range(len(material_dimensionless_length)):  # checking total dimensionless length = 1
        dimensionless_length = dimensionless_length + material_dimensionless_length[j]
    if dimensionless_length != 1:
        print("WARM: dimensionless length has a problem", dimensionless_length)
    dx = dimensionless_length/(nodes-1)
    x = np.linspace(0, dimensionless_length, nodes)
    print("Bigbang has been successfully executed")
    return materials, materials_summary, materials_number, materials_thickness, material_dimensionless_length, length,\
        dx, x, interphase_position
