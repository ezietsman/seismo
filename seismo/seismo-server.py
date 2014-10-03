''' seismo server.

In development. The idea is to create a server on a machine that has access to
GPUS, more CPUs etc and then call into it via the local network and use seismo
on it instead of running tasks on the local machine which may be slow or have
no GPU etc.

'''
import pickle

from flask import Flask, request
from flask.ext import restful

import seismo

app = Flask(__name__)
api = restful.Api(app)


class SeismoServerApi(restful.Resource):
    def put(self):
        function = request.form['command']
        args = pickle.loads(request.form['args'])

        if function in dir(seismo):
            result = getattr(seismo, function)(*args)
        else:
            return "Error"

        return pickle.dumps(result)

api.add_resource(SeismoServerApi, '/run_command')

if __name__ == '__main__':
    app.run()
