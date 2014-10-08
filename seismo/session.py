''' Contains classes to connect to a remote session
'''
import requests
import json

import seismo
import numpy as np
from . import utils


class RemoteFunction(object):
    '''
    This class represents a remote function that can be called on a
    seismo-server
    '''
    def __init__(self, name, host='http://localhost', port=5000):
        '''
        Initialise this with the name of the remote function. This is meant
        to be one of the functions as part of seismo
        '''
        self.name = name
        self.host = host
        self.port = port
        # create remote url command
        self.command_url = "{}:{}/run_command".format(self.host, self.port)

    def __call__(self, *args):
        ''' Function that calls name(*args) on remote server'''
        payload = utils.pickle_zip(args)
        data = {'command': self.name, 'args': payload}
        req = requests.put(self.command_url, data=data)

        try:
            result = utils.unpickle_zip(req.json())
        except TypeError:
            print(req.json())

        return result


class Session(object):

    '''
    Represents a session

    '''

    def __init__(self, host='http://localhost', port=5000):
        ''' Returns instance of session

        arguments
        ---------

        host : IP address of the host to connnect to. Defaults to
               'http://localhost'
        port : Port number of the host. Defaults to 5000

        '''

        self.host = host
        self.port = port

        self.register_functions()

    def register_functions(self):
        ''' Register all seismo functions as methods on self'''

        # must register functions so we can call e.g.
        # Session = session()
        # f, a = Session.deeming(t, m)

        funcs = ['deeming', 'fast_deeming', 'signal', 'sinewave']
        for func in funcs:
            remote_func = RemoteFunction(func, self.host, self.port)
            # set docstring
            seismo_func = getattr(seismo, func)
            remote_func.__doc__ = seismo_func.__doc__

            self.__setattr__(func, remote_func)


if __name__ == "__main__":

    session = Session()
