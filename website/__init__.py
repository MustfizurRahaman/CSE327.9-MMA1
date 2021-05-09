from flask import Flask
from os import  path

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Hasnat'

    from .model import model
    app.register_blueprint(model, url_prefix='/')

    return app