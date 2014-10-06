''' seismo server.

In development. The idea is to create a server on a machine that has access to
GPUS, more CPUs etc and then call into it via the local network and use seismo
on it instead of running tasks on the local machine which may be slow or have
no GPU etc.

'''
import json

from flask import Flask, request
from flask.ext import restful

import seismo
import numpy as np

app = Flask(__name__)
api = restful.Api(app)


class SeismoServerApi(restful.Resource):
    def put(self):

        function = request.form['command']
        args = json.loads(request.form['args'])
        for i, arg in enumerate(args):
            # change the lists into numpy arrays
            if isinstance(arg, list):
                args[i] = np.array(arg)

        if function in dir(seismo):
            try:
                result = getattr(seismo, function)(*args)
            except Exception as exc:
                return "Problem calling {}.\
                    Exception given:\n{}".format(function, exc)
        else:
            return "Error"

        result = list(result)

        for i, res in enumerate(result):
            if isinstance(res, np.ndarray):
                result[i] = res.tolist()

        return json.dumps(result)

api.add_resource(SeismoServerApi, '/run_command')

if __name__ == '__main__':
    app.run(debug=True)
