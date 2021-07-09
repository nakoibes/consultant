# from flask import Flask
# from application.resource import MainResource
# from application.service import MainService
#

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'you-will-never-guess'
#     main_service = MainService()
#     main_function = MainResource.as_view("", service=main_service)
#     #search_function = SearchResource.as_view("search", service=main_service)
#     app.add_url_rule("/", view_func=main_function)
#     #app.add_url_rule("/search/<inn>", view_func=main_function)
#     #app.add_url_rule("/search/<inn>", view_func=search_function)
#     return app

from flask import Flask
from config import Config


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)
from application import routes
