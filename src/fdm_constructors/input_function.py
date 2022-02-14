import matplotlib.pyplot as plt
import json
from scipy import interpolate
import numpy as np


def input_f(_time, dt):
    f = open('signal.json')
    data = json.load(f)
    amplitude = []
    time = []

    for i, j in zip(data['amplitude'], data['time']):
        amplitude.append(i)
        time.append(j)
    # print(time)
    f.close()

    f = open('signal.json')
    data = json.load(f)
    amplitude = []
    time = []
    for i, j in zip(data['amplitude'], data['time']):
        amplitude.append(i)
        time.append(j)
        # print(time)
    f.close()
    function = interpolate.interp1d(time, amplitude)
    lowest = np.amin(time)
    highest = np.amax(time)
    new_time = np.arange(lowest, highest, dt)
    new_amplitude = function(new_time)  # use interpolation function returned by `interp1d`
    print(new_amplitude.shape)
    plt.plot(time, amplitude, 'o', new_time, new_amplitude, '-')
    return new_amplitude


# print(np.arange(0, 9.8e-07, 1e-9))
#_y = input_f(np.arange(0, 9.8e-06, 1e-7))
# print(_y)