import numpy as np
import scipy.optimize as optimize


class signal(object):

    '''
        Class to represent a signal built from multiple sinewave components
    '''

    def __init__(self):
        ''' Initialise signal. '''
        self.components = []

    def add_component(self, component):
        ''' Add a component to the signal'''
        self.components.append(component)

    def evaluate(self, x):
        '''Evaluate the sum of the components at x'''

        _sum = (c.evaluate(x) for c in self.components)

        return np.sum(_sum)

    def _residuals_from_last_components(self, _list, times, values):
        ''' Keep current compnents fixed, vary only new component'''
        _sig = signal()
        for comp in self.components[:-1]:
            _sig.add_component(comp)

        a, f, p = _list
        _sine = sinewave(a, f, p, 0)
        _sig.add_component(_sine)

        return values - _sig.evaluate(times)

    def _residuals_from_all_components(self, _list, times, values):
        ''' given list of parameters of all components, times and values,
        return residuals between function calculated from _list and values
        '''
        _sig = signal()

        for i in range(0, len(_list), 3):
            a, f, p = _list[i:i+3]
            _sine = sinewave(a, f, p, 0)
            _sig.add_component(_sine)

        return values - _sig.evaluate(times)

    def fit(self, times, values):
        ''' Do a least squares fit of all the components in the signal to the
        given times and values

        Return new signal with the same number components but with updated
        values
        '''

        _args = self.components[-1].get_parameters()[:-1]

        solution = optimize.leastsq(self._residuals_from_last_components,
                                    _args,
                                    args=(times, values),
                                    full_output=True)

        params, cov, infodict, mesg, ier = solution

        if ier not in [1, 2, 3, 4]:
            print("Solution 1 was not found: reason given:\n{}".format(mesg))

        a, f, p = params
        self.components[-1] = sinewave(a, f, p, 0)

        # now fit all signals at once
        _args = []
        for comp in self.components:
            for param in comp.get_parameters()[:-1]:
                _args.append(param)

        solution = optimize.leastsq(self._residuals_from_all_components,
                                    _args,
                                    args=(times, values),
                                    full_output=True)

        params, cov, infodict, mesg, ier = solution

        if ier not in [1, 2, 3, 4]:
            print("Solution 2 was not found: reason given:\n{}".format(mesg))

        self.components = []

        for i in range(0, len(params), 3):
            a, f, p = params[i: i+3]
            # some of the amplitudes come out negative, fix those
            if a < 0:
                a = abs(a)
                if p > np.pi:
                    p -= np.pi
                else:
                    p += np.pi

            self.add_component(sinewave(a, f, p, 0))



        return  self


class sinewave(object):

    ''' Class to represent a sinusoid'''

    def __init__(self, amplitude=1.0, frequency=1.0, phase=0.5,
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
