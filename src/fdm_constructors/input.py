import json
import numpy as np
from scipy.interpolate import interp1d


def input_f(_time):
    f = open('signal.json')
    data = json.load(f)
    amplitude = []
    time = []

    for i, j in zip(data['amplitude'], data['time']):
        amplitude.append(i)
        time.append(j)
    # print(time)
    f.close()

    amplitude = np.array(amplitude)
    time = np.array(time)

    t = _time

    f_interpolate = interp1d(time, amplitude)

    intv = []
    zeros = []

    for i in t:

        if i >= np.amin(time) and i < np.amax(time):

            intv.append(i)

        else:

            zeros.append(i)

    pred_1 = f_interpolate(np.array(intv))

    pred_0 = np.zeros(len(zeros))
    pred = np.concatenate([pred_0, pred_1])
    print(f"zeros: {zeros}")
    print(f"{t.shape}")
    return pred


# print(np.arange(0, 9.8e-07, 1e-9))
#_y = input_f(np.arange(0, 9.8e-06, 1e-7))
# print(_y)