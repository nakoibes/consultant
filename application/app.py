
from flask import Flask
from config import Config
from requests import Session

app = Flask(__name__)
app.config.from_object(Config)
session = Session()
from application import routes
