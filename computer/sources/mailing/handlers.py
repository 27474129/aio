from flask.views import View


class MailingView(View):
    def dispatch_request(self):
        return self.get()

    def get(self):
        return 'Hello, from zxc'
