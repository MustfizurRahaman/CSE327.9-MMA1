from flask import Flask, render_template
from os import environ
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
        Returns the flask app after configuring it with secret key and database
        registers views via blueprint
        handles any missing or non existing route by displaying a custom error page

        :param NULL: None

        :type NULL: None

        :return: None

        :rtype: None
    """

    app = Flask(__name__)

    # Secret Key!
    app.config['SECRET_KEY'] = "Life Pharma"

    # URI of database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)

    # 404 custom error page
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error_404.html"), 404

    # Register views in app blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Medicine

    return app