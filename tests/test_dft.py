'''Tests for DFT functions'''

import numpy as np

from seismo import timeseries


def create_data():
    ''' Creates a fake data set for testing'''
    x = np.linspace(0, 10, 10)
    y = np.sin(x)
    f = np.linspace(0, 10, 10)
    a_correct = np.array([0.24185187,  0.56910886,  0.13692586,  0.1021499,
                          0.07603825, 0.90524571,  0.08660415,  0.18495361,
                          0.5947502,  0.46954945])

    return x, y, f, a_correct


def test_periodogram_numpy():
    ''' Test the numpy implementation of the periodogram'''
    x, y, f, a_correct = create_data()
    a = timeseries.periodogram_numpy(x, y, f)
    assert(np.allclose(a, a_correct))


def test_periodogram_parallel_1thread():
    ''' Test the fortran implementation of the periodogram'''
    x, y, f, a_correct = create_data()

    a = timeseries.periodogram_parallel(x, y, f, 1)
    assert(np.allclose(a, a_correct))


def test_periodogram_parallel_2thread():
    ''' Test the fortran implementation of the periodogram'''
    x, y, f, a_correct = create_data()

    a = timeseries.periodogram_parallel(x, y, f, 2)
    assert(np.allclose(a, a_correct))


def test_periodogram_parallel_4thread():
    ''' Test the fortran implementation of the periodogram'''
    x, y, f, a_correct = create_data()

    a = timeseries.periodogram_parallel(x, y, f, 4)
    assert(np.allclose(a, a_correct))


def test_periodogram_opencl():
    ''' Test the opencl implementation of the periodogram'''
    x, y, f, a_correct = create_data()

    a = timeseries.periodogram_opencl(x, y, f)
    assert(np.allclose(a, a_correct))
