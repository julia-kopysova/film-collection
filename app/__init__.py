"""
Module initializes app
"""
from typing import Union, Tuple

from flask import Flask, request, jsonify, redirect, url_for, Response
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash


from app.config import Config
from app.models import User, db
from app.swagger import swaggerui_blueprint

migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.secret_key = '1234'
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(swaggerui_blueprint)
    login_manager.init_app(app)
    return app


application = create_app()
ma = Marshmallow(application)
api = Api(application)


from app import auth, pagination, search, urls, swagger
from app.resources.director_resources import DirectorListResource, DirectorResource
from app.resources.film_resources import FilmListResource, FilmResource
from app.resources.genre_resources import GenreListResource, GenreResource
from app.resources.user_resouces import UserListResource, UserResource