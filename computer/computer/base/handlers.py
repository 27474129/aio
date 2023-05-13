from flask.views import View
from flask import request


class BaseView(View):
    methods = ('OPTIONS', 'GET', 'POST', 'PUT', 'DELETE')

    def dispatch_request(self):
        if request.method == 'POST':
            return self.post()

        if request.method == 'GET':
            return self.get()

        if request.method == 'PUT':
            return self.put()

        return self.delete()

    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...
