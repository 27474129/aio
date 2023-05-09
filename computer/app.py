from flask import Flask

from computer.urls import add_urls


app = Flask(__name__)
add_urls(app)
