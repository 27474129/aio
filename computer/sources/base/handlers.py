from flask.views import View

from sources.constants import NOT_ALLOWED


class BaseView(View):
    allowed_methods = ('OPTIONS', 'GET', 'POST', 'PUT', 'DELETE')

    def dispatch_request(self):
        if self.request.method not in self.allowed_method:
            return
