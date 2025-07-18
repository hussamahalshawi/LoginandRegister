
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_class):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(config_class)
    mongo.init_app(app)
    app.secret_key = 'your_secret_key'
    # تسجيل البلوبرينت
    from .routes import auth
    app.register_blueprint(auth)

    return app