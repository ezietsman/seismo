import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import seismo

matplotlib.style.use('ggplot')


def create_fake_data(N):

    signal = seismo.signal()

    print("Fake numbers")
    for i in range(N):
        amplitude = 0.05*np.random.rand()
        frequency = np.random.rand()*200
        phase = np.random.rand()*np.pi

        component = seismo.sinewave(amplitude, frequency, phase, 0)
        # add component to signal
        signal.add_component(component)

        print("{}, {}, {}".format(amplitude, frequency, phase))

    return signal

if __name__ == "__main__":
    # create some fake data
    t = np.linspace(0, 20, 2500)
    signal = create_fake_data(1)

    # evaluate signal at times
    s = signal.evaluate(t) + 0.01*np.random.rand(t.size)

    # Need to know Nyquist (more or less)
    nyuquist = 0.5/((t[1] - t[0]))



    # now calculate the DFT
    freqs, amps = seismo.deeming(t, s)
    # find peak and fit it
    fmax, amax = seismo.timeseries.find_peak(freqs, amps)
    print(fmax, amax)

    fitsig = seismo.fitting.signal()
    fitsig.add_component(seismo.fitting.sinewave(amax, fmax, 0.5, 0))
    fitsig.fit(t, s)

    plt.subplot(211)
    plt.plot(t, s, '.')

    plt.subplot(212)
    plt.plot(freqs, amps)
    plt.show()
