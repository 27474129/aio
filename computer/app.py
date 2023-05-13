from flask import Flask

from computer.urls import add_urls
from computer.constants import DEBUG
from computer.config import PORT


app = Flask(__name__)
add_urls(app)
app.run(debug=DEBUG, port=PORT)
