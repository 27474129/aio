from flask import Flask

from sources.urls import add_urls


app = Flask(__name__)
add_urls(app)
