import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import seismo

matplotlib.style.use('ggplot')


def create_fake_data(N):
    ''' Given number of signal components N, return signal object containing N components with random frquencies, amplitudes and phases.
    '''

    signal = seismo.signal()

    print("Fake numbers")
    for i in range(N):
        amplitude = 0.05*np.random.rand()
        frequency = np.random.rand()*140
        phase = np.random.rand()*np.pi

        component = seismo.sinewave(amplitude, frequency, phase, 0)
        # add component to signal
        signal.add_component(component)

        print("{}, {}, {}".format(amplitude, frequency, phase))

    return signal


if __name__ == "__main__":
    # create some fake data
    t = np.linspace(0, 20, 10000)
    fakesignal = create_fake_data(10)

    # evaluate signal at times
    s = fakesignal.evaluate(t) + 0.1*np.random.randn(t.size)

    # subtract average, random numbers may not average to 0
    s -= np.average(s)
    s_original = np.zeros_like(s)
    s_original[:] = s[:]

    # cosine bell
    hann = np.hanning(s.size)

    # Need to know Nyquist (more or less)
    nyuquist = 0.5/((t[1] - t[0]))

    fittedsignal = seismo.fitting.signal()

    freqs0, amps0 = seismo.deeming(t, s)
    noise = 4*np.median(amps0)
    # Find and subtract signal, until no signals above 4*median amplitude in
    # DFT is found
    while True:
        # calculate the DFT
        # apply hanning / cosine bell first
        freqs, amps = seismo.deeming(t, s)

        # find peak and fit it
        fmax, amax = seismo.timeseries.find_peak(freqs, amps)

        if amax < noise:
            break

        fittedsignal.add_component(seismo.fitting.sinewave(amax, fmax, 3.14, 0))
        fittedsignal = fittedsignal.fit(t, s_original)

        # subtract fitted signals from observations
        s = s_original - fittedsignal.evaluate(t)

    print("Fitted")
    for comp in fittedsignal.components:
        a, f, p, c = comp.get_parameters()
        print("{} {} {} {}".format(a, f, p, c))

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.6, left=0.05, right=0.95, top=0.95,
                        bottom=0.05)

    plt.subplot(411)
    plt.title("Original Data + Fit", size=10, color='0.2')
    plt.plot(t, s_original, '.')
    t_line = np.linspace(t.min(), t.max(), 10*t.size)
    plt.plot(t_line, fittedsignal.evaluate(t_line), '-')

    plt.subplot(412)
    plt.title("DFT of Original data", size=10, color='0.2')
    plt.plot(freqs0, amps0)
    plt.hlines(np.median(amps0)*4, freqs.min(), freqs.max())

    plt.subplot(413)
    plt.title("Residuals", size=10, color='0.2')
    plt.plot(t, s_original - fittedsignal.evaluate(t), '.')

    plt.subplot(414)
    plt.title("DFT of prewhitened data", size=10, color='0.2')
    plt.plot(freqs, amps)
    plt.hlines(np.median(amps0)*4, freqs.min(), freqs.max())


    plt.show()
