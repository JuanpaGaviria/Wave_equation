import json


def input_f(dt, n_steps):
    f = open('signal.json')
    data = json.load(f)
    amplitude = []
    time = []
    for i, j in zip(data['amplitude'], data['time']):
        amplitude.append(i)
        time.append(j)
    print(time)
    f.close()

