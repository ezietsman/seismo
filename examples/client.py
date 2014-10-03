import requests
import pickle

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    x = np.linspace(0, 10, 1000)
    y = np.sin(2*np.pi*59*x)

    url = 'http://localhost:5000/run_command'
    data = pickle.dumps((x, y))
    req = requests.put(url, data={'command': 'fast_deeming', 'args': data})

    f, a, t, m = pickle.loads(req.json())

    plt.plot(f, a)
    plt.show()
