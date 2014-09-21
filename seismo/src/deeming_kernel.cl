// Kernel to compute the deeming periodogram for a given frequency over a set
// of data

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
