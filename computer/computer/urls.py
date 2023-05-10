from computer.mailing.handlers import MailingView


def add_urls(app):
    app.add_url_rule('/api/mailing', view_func=MailingView.as_view('mailing'))
