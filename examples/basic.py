import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from seismo import fitting
from seismo import timeseries

matplotlib.style.use('ggplot')


if __name__ == "__main__":
    # create some fake data
    t = np.linspace(0, 20, 10000)

    # let's add some random sine waves
    N_signals = 5

    signal = fitting.signal()

    for i in range(N_signals):
        amplitude = 0.01*np.random.rand()
        frequency = np.random.rand()*200
        phase = np.random.rand()*np.pi

        component = fitting.sinewave(amplitude, frequency, phase, 0)
        # add component to signal
        signal.add_component(component)

    # evaluate signal at times
    s = signal.eval_components(t) + 0.025*np.random.randn(t.size)

    # now calculate the DFT
    # Need to know Nyquist (more or less)
    nyuquist = 0.5/((t[1] - t[0]))

    # need to know freq resolution and oversample
    fres = 1.0/(t[-1] - t[0])
    freqs = np.linspace(0, nyuquist, 5*int(nyuquist/fres))
    amps = timeseries.periodogram_opencl(t, s, freqs)

    # make some plots
    plt.subplot(211)
    plt.plot(t, s, '.')
    plt.xlabel("Time (days)")
    plt.ylabel("Magnitude")
    ymin, ymax = plt.ylim()
    plt.ylim(2*ymax, 2*ymin)

    plt.subplot(212)
    plt.plot(freqs, amps)
    plt.xlabel(r"Frequency (day$^{-1}$)")
    plt.ylabel("Amplitude (mag)")

    plt.show()
