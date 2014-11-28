import numpy as np

from seismo import lomb_scargle
from scipy.signal import lombscargle as sci_lomb_scargle

def create_data():
    ''' Creates a fake data set for testing'''
    # un-evenly sampled data
    x = np.sort(np.random.rand(100)*20)
    w = 1.
    y = np.sin(w*x)
    f = np.linspace(0.01, 10, 100)
    # get close to peak w
    a_correct = np.array([w,w+2e-2, w+1e-2])

    return x, y, f, a_correct

def test_scipy_example():
    '''Compares scipy's implementation to OpenCL'''
    # amplitude
    A = 2.
    # frequency
    w = 2.
    phi = 0.5 * np.pi
    nin = 1000
    nout = 100000
    # Fraction of points to select
    frac_points = 0.9 
    r = np.random.rand(nin)
    x = np.linspace(0.01, 10*np.pi, nin)
    x = x[r >= frac_points]
    y = A * np.sin(w*x+phi)
     # For normalization of the periodogram
    normval = x.shape[0]
    f = np.linspace(0.01, 10, nout)
    # get periodogram
    pgram_sci = sci_lomb_scargle(x, y, f)
    pgram_cl = lomb_scargle(x, y, f)
    assert(np.allclose(pgram_sci, pgram_cl))



def test_lomb_scargle_scipy():
    '''Test scipy implementation of lomb scagle'''
     x, y, f, a_correct = create_data()
     a = sci_lomb_scargle(x, y, f)
     assert(np.allclose(f[a.argmax()], a_correct,.02,0))


def test_lomb_scargle_opencl():
    '''Test OpenCL implementation of lomb scagle'''
     x, y, f, a_correct = create_data()
     a = lomb_scargle(x, y, f)
     # a bit of error since unevenly spaced
     assert(np.allclose(f[a.argmax(), a_correct,.02,0))
