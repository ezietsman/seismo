import pyopencl as cl
import numpy as np

'''OpenCl version'''
lomb_txt64 = '''
  #define PYOPENCL_DEFINE_CDOUBLE
  #pragma OPENCL EXTENSION cl_khr_fp64: enable
  __kernel void lombscargle(__global const double *x,
                            __global const double *y,
                            __global const double *f,
                            __global double *P,
                            const int Nt)
{

  // Local variables
  int i = get_global_id(0);
  int j;
  double c, s, xc, xs, cc, ss, cs;
  double tau, c_tau, s_tau, c_tau2, s_tau2, cs_tau;
  double term0, term1;
  double local_f = f[i];

  xc = 0.;
  xs = 0.;
  cc = 0.;
  ss = 0.;
  cs = 0.;
  for(j = 0; j < Nt; j++)
    {
      c = cos(local_f * x[j]);
      s = sin(local_f * x[j]);

      xc += y[j] * c;
      xs += y[j] * s;
      cc += c * c;
      ss += s * s;
      cs += c * s;

     }

    tau = atan(2 * cs / (cc - ss)) / (2 * local_f);
    c_tau = cos(local_f  * tau);
    s_tau = sin(local_f  * tau);
    c_tau2 = c_tau * c_tau;
    s_tau2 = s_tau * s_tau;
    cs_tau = 2 * c_tau * s_tau;

    term0 = c_tau * xc + s_tau * xs;
    term1 = c_tau * xs - s_tau * xc;
    P[i] = 0.5 * (((term0 * term0) / (c_tau2 * cc + cs_tau * cs + s_tau2 * ss)) + ((term1 * term1) / (c_tau2 * ss - cs_tau * cs + s_tau2 * cc)));
  }'''

lomb_txt32 = '''
   __kernel void lombscargle(__global const float *x,
                            __global const float *y,
                            __global const float *f,
                            __global float *P,
                            const int Nt)
{

  // Local variables
  int i = get_global_id(0);
  int j;
  float c, s, xc, xs, cc, ss, cs;
  float tau, c_tau, s_tau, c_tau2, s_tau2, cs_tau;
  float term0, term1;
  float local_f = f[i];

  xc = 0.;
  xs = 0.;
  cc = 0.;
  ss = 0.;
  cs = 0.;
  for(j = 0; j < Nt; j++)
    {
      c = cos(local_f * x[j]);
      s = sin(local_f * x[j]);

      xc += y[j] * c;
      xs += y[j] * s;
      cc += c * c;
      ss += s * s;
      cs += c * s;

     }

    tau = atan(2 * cs / (cc - ss)) / (2 * local_f);
    c_tau = cos(local_f  * tau);
    s_tau = sin(local_f  * tau);
    c_tau2 = c_tau * c_tau;
    s_tau2 = s_tau * s_tau;
    cs_tau = 2 * c_tau * s_tau;

    term0 = c_tau * xc + s_tau * xs;
    term1 = c_tau * xs - s_tau * xc;
    P[i] = 0.5 * (((term0 * term0) / (c_tau2 * cc + cs_tau * cs + s_tau2 * ss)) + ((term1 * term1) / (c_tau2 * ss - cs_tau * cs + s_tau2 * cc)));
  }'''

def lomb_scargle(x, y, f):
    ''' lomb scargle periorodgram. If doesn't work try 32 bit version'''
    
    # double precision
    x = np.float64(x)
    y = np.float64(y)
    f = np.float64(f)
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    # make max arrays
    Nx, Nf = np.int32(x.shape[0]), np.int32(f.shape[0])
    # send data to card
    x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x)
    y_g = cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=y)
    f_g = cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=f)
    # make output
    pgram = np.empty_like(f)
    pgram_g = cl.Buffer(ctx, mf.WRITE_ONLY, pgram.nbytes)
    prg = cl.Program(ctx, lomb_txt64)

    try:
        prg.build()
    except RuntimeError:
        raise RuntimeError('Card not 64 bit compatible try lomb_scagle32')
        
    except:
        # 
        print("Error:")
        print(prg.get_build_info(ctx.devices[0], cl.program_build_info.LOG))
        raise

    prg.lombscargle(queue, pgram.shape, None, x_g, y_g, f_g, pgram_g, Nx)
    cl.enqueue_read_buffer(queue, pgram_g, pgram)

    return pgram

def lomb_scargle32(x, y, f):
    '''single percesion version of lomb-scargle'''
    x = np.float32(x)
    y = np.float32(y)
    f = np.float32(f)
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    # make max arrays
    Nx, Nf = np.int32(x.shape[0]), np.int32(f.shape[0])
    # send data to card
    x_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x)
    y_g = cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=y)
    f_g = cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=f)
    # make output
    pgram = np.empty_like(f)
    pgram_g = cl.Buffer(ctx, mf.WRITE_ONLY, pgram.nbytes)
    prg = cl.Program(ctx, lomb_txt32)

    try:
        prg.build()
    except:
        # 
        print("Error:")
        print(prg.get_build_info(ctx.devices[0], cl.program_build_info.LOG))
        raise

    prg.lombscargle(queue, pgram.shape, None, x_g, y_g, f_g, pgram_g, Nx)
    cl.enqueue_read_buffer(queue, pgram_g, pgram)

    return pgram
