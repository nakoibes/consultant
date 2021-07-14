from flask import Flask
from config import Config
from requests import Session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
session = Session()
bootstrap = Bootstrap(app)

from application import routes
