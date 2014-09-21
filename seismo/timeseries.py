'''

This contains some useful routines I need for finding and analysing
frequencies in pulsating star lightcurves

'''

import numpy as np
import f90periodogram

def periodogram_parallel(t, m, f, threads=None):
    ''' Calculate the Deeming periodogram using Fortran with OpenMP
    '''
    if not threads:
        threads = 4

    # strip nan
    valid = np.logical_not(np.isnan(m))
    t = t[valid]
    m = m[valid]

    ampsf90omp_2 = f90periodogram.periodogram2(t, m, f, t.size, f.size, threads)

    return ampsf90omp_2


def periodogram(t, m, freqs):
    ''' Calculate the Deeming periodogram using numpy using a serial O(N*N)
    algorithm.

    Inputs:
        t: numpy array containing timestamps
        m: numpy array containing measurements
        freqs: numpy array containing frequencies at which DFT must be
        calculated

    Returns:
        amplitudes: numpy array of len(freqs) containing amplitudes of
        periodogram

    Note: This routine strips datapoints if it is nan
    '''

    # strip nan
    valid = np.logical_not(np.isnan(m))
    t = t[valid]
    m = m[valid]

    # calculate the dft
    amps = np.zeros(freqs.size, dtype='float')
    twopit = 2.0*np.pi*t
    for i, f in enumerate(freqs):
        twopift = f*twopit
        real = (m*np.cos(twopift)).sum()
        imag = (m*np.sin(twopift)).sum()
        amps[i] = real**2 + imag**2

    amps = 2.0*np.sqrt(amps)/t.size

    return amps
