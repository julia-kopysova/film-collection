"""
Module initializes app
"""
import logging

import click
from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from app.config import Config
from app.models import User, db
from app.swagger import swaggerui_blueprint

migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    """
    Function for creating application
    :param config_class: class with config for application
    :return: application
    """
    app = Flask(__name__)
    app.secret_key = '1234'
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(swaggerui_blueprint)
    login_manager.init_app(app)

    # docker exec NAME CONTAINER cat logs.log

    logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="a",
                        format='%(asctime)s:%(levelname)s:%(message)s')
    return app


application = create_app()
ma = Marshmallow(application)
api = Api(application)

# docker exec -i NAME_CONTAINER flask create_admin USERNAME EMAIL PASSWORD


@application.cli.command("create_admin")
@click.argument("username")
@click.argument("email")
@click.argument("password")
def create_admin(username, email, password):
    """
    For creation superuser in start app
    :param username: username of admin
    :param email: email of admin
    :param password: password of admin
    :return: None
    """
    user = User.query.filter_by(username=username, email=email).first()
    if user is None:
        db.session.add(User(username=username,
                            first_name="Admin",
                            last_name="Admin",
                            email=email,
                            password=generate_password_hash(password),
                            is_superuser=True))
        db.session.commit()
    else:
        print("Admin exists")


from app import auth, pagination, search, urls, swagger
from app.resources.director_resources import DirectorListResource, DirectorResource
from app.resources.film_resources import FilmListResource, FilmResource
from app.resources.genre_resources import GenreListResource, GenreResource
from app.resources.user_resouces import UserListResource, UserResource
