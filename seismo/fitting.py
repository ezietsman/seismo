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

    def evaluate(self, x):
        '''Evaluate the sum of the components at x'''

        _sum = (c.evaluate(x) for c in self.components)

        return np.sum(_sum)

    def _eval_from_list(self, _list, times, values):
        ''' given list of parameters of all components

        '''

        # to evaluate from th given parameters, make a new signal object

        _sig = signal()

        for i in range(0, len(_list), 4):
            a, f, p, c = _list[i:i+4]
            _sine = sinewave(a, f, p, c)
            _sig.add_component(_sine)

        return values - _sig.evaluate(times)

    def fit(self, times, values):
        ''' Do a least squares fit of all the components in the signal to the
        given times and values

        Return new signal with the same number components but with updated
        values
        '''

        _args = []

        # make a list containing all the parameters of the components
        for comp in self.components:
            params = comp.get_parameters()
            for p in params:
                _args.append(p)

        solution = optimize.leastsq(self._eval_from_list, _args, args=(times,
                                                                       values))

        print(solution)


class sinewave(object):

    ''' Class to represent a sinusoid'''

    def __init__(self, amplitude=1.0, frequency=0.0, phase=0.5,
                 constant=0.0):
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

    def get_parameters(self):
        ''' returns (amplitude, frequency, phase, constant'''
        a = self.amplitude
        f = self.frequency
        p = self.phase
        c = self.constant
        return a, f, p, c
