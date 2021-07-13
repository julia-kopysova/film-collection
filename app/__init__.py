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

migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.secret_key = '1234'
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    return app


application = create_app()
ma = Marshmallow(application)
api = Api(application)


# app = Flask(__name__)
# app.config.from_object("app.config.Config")
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
#
# ma = Marshmallow(app)
# api = Api(app)
#
#


@application.route('/')
def hello_world():
    """
    Hello Word method
    :return:
    """
    return 'Hello World!!!!'


@application.route('/login')
def login():
    return 'Login'


# @application.route('/signup', methods=['POST'])
# def signup() -> Union[Response, Tuple[str, int]]:
#     username = request.json['username']
#     first_name = request.json['first_name']
#     last_name = request.json['last_name']
#     email = request.json['email']
#     password = request.json['password']
#
#     user = User.query.filter_by(email=email).first()
#
#     if user:
#         return 'This email already exists', 405
#
#     new_user = User(
#         username=username,
#         first_name=first_name,
#         last_name=last_name,
#         email=email,
#         password=generate_password_hash(password, method='sha256'),
#         is_superuser=False)
#
#     db.session.add(new_user)
#     db.session.commit()
#     return 'added', 202
#     # return redirect(url_for('auth.login'))

# @app.route('/foo')
# def foo():
#     return 'foo000'


# @app.route('/genres/', methods=['GET'])
# def get_genres():
#     # all_genres = Genre.query.all()
#     return 'lalala'
from app import auth, pagination, search