import numpy as np
import matplotlib.pyplot as plt
import matplotlib

import seismo

if __name__ == '__main__':
    # make data
    A = 2.
    # frequency
    w = 1.
    # phase
    phi = 0.5 * np.pi
    nin = 1000
    nout = 100000
    # Fraction of points to select
    frac_points = 0.9
    
    # Randomly select a fraction of an array with timesteps:
    r = np.random.rand(nin)
    x = np.linspace(0.01, 10*np.pi, nin)
    x = x[r >= frac_points]
    # For normalization of the periodogram
    normval = x.shape[0] 
 
    # Plot a sine wave for the selected times:

    y = A * np.sin(w*x+phi)
    # Define the array of frequencies for which to compute the periodogram:
    f = np.linspace(0.01, 10, nout)
 
    # Calculate Lomb-Scargle periodogram:

    pgram = seismo.lomb_scargle(x, y, f)

    # Make a plot of the input data:
    
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'b+')

    # Then plot the normalized periodogram:

    plt.subplot(2, 1, 2)
    plt.plot(f, np.sqrt(4*(pgram/normval)))

    # plot freq of sine curve
    plt.plot([w,w], [np.sqrt(4*(pgram/normval)).min(), np.sqrt(4*(pgram/normval)).max() + 1],'r')
    plt.show()
