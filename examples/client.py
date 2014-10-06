import requests
import json

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    x = np.linspace(0, 10, 5000)
    y = np.sin(2*np.pi*59*x) + np.sin(2*np.pi*33*x)

    url = 'http://localhost:5000/run_command'
    data = json.dumps((x.tolist(), y.tolist()))
    req = requests.put(url, data={'command': 'deeming', 'args': data})

    try:
        f, a = json.loads(req.json())
    except TypeError:
        print(req.json())

    plt.plot(f, a)
    plt.show()
