import json
import numpy as np


class Input:

    def __init__(self):
        self.input_list = None
        self.uj0_initial = None

    def signal(self, dt, n_steps):  # Signal that enters the domain
        f = open('signal.json')  # open the .json file
        data = json.load(f)
        amplitude = []
        time = []
        for i, j in zip(data['amplitude'], data['time']):  # saves amplitude vs time values
            amplitude.append(i)
            time.append(j)
        f.close()
        self.input_list = None

    def cosine_method(self, amplitude, period, input_time, dt):  # Cosine function that enter the domain
        self.input_list = []
        for _time in range(input_time):
            initial_amplitude = amplitude*np.cos(-(2*np.pi*_time*dt/period))
            self.input_list.append(initial_amplitude)

    def standing_wave(self, x):  # Standing wave, gives an initial deformation
        self.uj0_initial = np.exp(-((x-0.5)/0.1)**2)
