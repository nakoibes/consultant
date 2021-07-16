from flask import Flask
from config import Config
from requests import Session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from application import routes
