'''

This contains some useful routines I need for finding and analysing
frequencies in pulsating star lightcurves

'''
import multiprocessing

import numpy as np
import f90periodogram

try:
    import pyopencl as cl
    OPENCL = True
except ImportError:
    print("opencl not available")
    OPENCL = False


def periodogram_opencl(t, m, f):
    ''' Calculate the Deeming periodogram using numpy using a parallel O(N*N)
    algorithm. Parallelisation is obtained via opencl and could be run on a
    GPU.

    Inputs:
        t: numpy array containing timestamps
        m: numpy array containing measurements
        f: numpy array containing frequencies at which DFT must be
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

    # create a context and a job queue
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # create buffers to send to device
    mf = cl.mem_flags
    # input buffers
    times_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=t)
    mags_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=m)
    freqs_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=f)

    # output buffers
    amps_buffer = cl.Buffer(ctx, mf.WRITE_ONLY, f.nbytes)
    amps_g = np.empty_like(f)


    kernel = '''
    // Kernel to compute the deeming periodogram for a given frequency over a
    // set of data

    #define PYOPENCL_DEFINE_CDOUBLE
    #pragma OPENCL EXTENSION cl_khr_fp64: enable

    __kernel void periodogram(
            __global const double *times_g,
            __global const double *mags_g,
            __global const double *freqs_g,
            __global double *amps_g,
            const int datalength) {

        int gid = get_global_id(0);
        double this_frequency = freqs_g[gid];
        double realpart = 0.0;
        double imagpart = 0.0;
        double pi = 3.141592653589793;

        for (int i=0; i < datalength; i++){
            realpart = realpart + mags_g[i]*cos(2.0*pi*this_frequency*times_g[i]);
            imagpart = imagpart + mags_g[i]*sin(2.0*pi*this_frequency*times_g[i]);
        }
        amps_g[gid] = 2.0*sqrt(pow(realpart, 2) + pow(imagpart, 2))/datalength;
    }
    '''

    # read and compile the opencl kernel
    prg = cl.Program(ctx, kernel)
    try:
        prg.build()
    except:
        print("Error:")
        print(prg.get_build_info(ctx.devices,
                                 cl.program_build_info.LOG))
        raise

    # call the function and copy the values from the buffer to a numpy array
    prg.periodogram(queue, amps_g.shape, None,
                    times_g,
                    mags_g,
                    freqs_g,
                    amps_buffer,
                    np.int32(t.size))
    cl.enqueue_copy(queue, amps_g, amps_buffer)

    return amps_g


def periodogram_parallel(t, m, f, threads=None):
    ''' Calculate the Deeming periodogram using Fortran with OpenMP
    '''
    if not threads:
        threads = 4

    # strip nan
    valid = np.logical_not(np.isnan(m))
    t = t[valid]
    m = m[valid]

    ampsf90omp_2 = f90periodogram.periodogram2(t, m, f, t.size, f.size,
                                               threads)

    return ampsf90omp_2


def periodogram_numpy(t, m, freqs):
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


def deeming(times, values, frequencies=None, method='opencl'):
    ''' Calculate the Deeming periodogram of values at times.
    Inputs:
        times: numpy array containing time_stamps
        values: numpy array containing the measured values at times.
        frequencies: optional numpy array at which the periodogram will be
        calculated. If not given, (times.size) frequencies between 0 and
        the nyquist frequency will be used.
        method: One of 'opencl', 'openmp', 'numpy'.
            'opencl' requires `pyopencl` to be present as well as a working
            opencl driver. This method runs in parallel on the opencl device
            and is potentially the fastest of the 3. This option is default.

            'openmp' runs in parallel via openmp in fortran code. This can only
            run on your CPU. It defaults to the number of cores in your machine.

            'numpy' uses a serial implementation that only requires numpy to be
            installed. This one is probably the slowest of the 3 options for
            larger input data sizes

    Returns (frequency, amplitude) arrays.
    '''

    if frequencies is None:
        # frequencies array not given. Create one

        # find the smallest differnce between two successive timestamps and use
        # that for the nyquist calculation
        t = np.arange(times.size-1)
        smallest = np.min(times[t+1] - times[t])
        nyquist = 0.5 / smallest

        frequencies = np.linspace(0, nyquist, times.size)

    if method == 'opencl':
        amps = periodogram_opencl(times, values, frequencies)
    elif method == 'openmp':
        cores = multiprocessing.cpu_count()
        amps = periodogram_parallel(times, values, frequencies, cores)
    elif method == 'numpy':
        amps = periodogram_numpy(times, values, frequencies)
    else:
        raise ValueError("{} is not a valid method!".format(method))

    return frequencies, amps


def find_peak(frequencies, amplitudes):
    ''' Return the return (freq, amp) where amp is maximum'''

    ampmax = np.where(amplitudes == amplitudes.max())

    return float(frequencies[ampmax]), float(amplitudes[ampmax])
