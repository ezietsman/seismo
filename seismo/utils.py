import pickle


def pickle_zip(obj):
    ''' Given an object, turn it into a zipped pickled object'''

    pkobj = pickle.dumps(obj)

    return pkobj

def unpickle_zip(obj):
    ''' Unzip and unpickle the object'''

    unpkobj = pickle.loads(obj)

    return unpkobj
