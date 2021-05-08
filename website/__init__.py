from flask import Flask, render_template
from os import environ
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Secret Key!
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

    # URI of database
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)

    # 404 custom error page
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error_404.html"), 404

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import Medicine

    return app
