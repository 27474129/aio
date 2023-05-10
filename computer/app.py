from flask import Flask

from computer.urls import add_urls
from computer.constants import DEBUG


app = Flask(__name__)
add_urls(app)
app.run(debug=DEBUG, port=5003)
