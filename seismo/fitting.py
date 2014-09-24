import numpy as np
import scipy.optimize as optimize


class signal(object):

    '''
        Class to represent a signal built from multiple sinewave components
    '''

    def __init__(self):
        ''' Initialise signal.
        Inputs:
            x: numpy array with e.g. timestamps
            y: numpy array with value at timestamps
            err: numpy array with error estimates
        '''
        self.components = []

    def add_component(self, component):
        ''' Add a component to the signal'''
        self.components.append(component)

    def eval_components(self, x):
        '''Evaluate the sum of the components at x'''

        _sum = (c.evaluate(x) for c in self.components)

        return np.sum(_sum)


class sinewave(object):

    ''' Class to represent a sinusoid'''

    def __init__(self, amplitude=None, frequency=None, phase=None,
                 constant=None):
        ''' Class to represent a sinusoid.'''

        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.constant = constant

    def evaluate(self, x):
        '''Given array or float x, return the sinusoid values'''
        a = self.amplitude
        f = self.frequency
        p = self.phase
        c = self.constant

        return a*np.sin(2*np.pi*f*x + p) + c
