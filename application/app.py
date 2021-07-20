from flask import Flask
from config import Config
from requests import Session
from flask_bootstrap import Bootstrap
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
mongo_client = MongoClient(host="localhost", port=27017)
db = mongo_client.get_database("consultant")

from application import routes
