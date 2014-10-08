''' seismo server.

In development. The idea is to create a server on a machine that has access to
GPUS, more CPUs etc and then call into it via the local network and use seismo
on it instead of running tasks on the local machine which may be slow or have
no GPU etc.

'''
from flask import Flask, request
from flask.ext import restful

import seismo
import numpy as np
import utils

app = Flask(__name__)
api = restful.Api(app)


class SeismoServerApi(restful.Resource):
    def put(self):

        function = request.form['command']
        args = utils.unpickle_zip(request.form['args'])

        if function in dir(seismo):
            try:
                result = getattr(seismo, function)(*args)
            except Exception as exc:
                return utils.pickle_zip("Problem calling {}.\
                    Exception given:\n{}".format(function, str(exc)))
        else:
            return utils.pickle_zip("Error")

        return utils.pickle_zip(result)

api.add_resource(SeismoServerApi, '/run_command')

if __name__ == '__main__':
    app.run(debug=True)
