from flask.views import View
from flask import request


class BaseView(View):
    methods = ('OPTIONS', 'GET', 'POST', 'PUT', 'DELETE')

    def dispatch_request(self):
        if request.method == 'POST':
            return self._post()

        if request.method == 'GET':
            return self._get()

        if request.method == 'PUT':
            return self._put()

        return self._delete()

    def _get(self):
        ...

    def _post(self):
        ...

    def _put(self):
        ...

    def _delete(self):
        ...
