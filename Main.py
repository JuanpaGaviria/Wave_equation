import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import winsound
from src import Bigbang
from src.battery_construction import battery_structure

"""material selection
0, 2: anode charged, anode discharged 
1, 3: cathode charged, cathode discharged
6: separator
4,5,7,8,9: others (check csv)
10, 11: benzene electrolyte, carbon tetrachloride electrolyte 
"""
indexes = [1, 2, 3]  # materials definition
fold_number = 6  # Layers conformed by the materials defined
url = './src/database/materials_properties.csv'
df = pd.read_csv(url)


print("hola mundo")


